import { defineStore } from 'pinia'
import type { ChangePasswordPayload, LoginCredentials, User } from '../types'
import * as authService from '../services/auth.service'

interface AuthState {
  user: User | null
  isAdmin: boolean
  hydrated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAdmin: false,
    hydrated: false,
  }),
  getters: {
    isAuthenticated: (state) => state.user !== null,
    mustChangePassword: (state) => state.user?.must_change_password === true,
    displayName: (state) =>
      state.user
        ? [state.user.first_name, state.user.last_name].filter(Boolean).join(' ') || state.user.username
        : '',
    userEmail: (state) => state.user?.email ?? '',
  },
  actions: {
    async login(credentials: LoginCredentials) {
      const res = await authService.login(credentials)
      this.user = res.user
      this.isAdmin = res.is_admin
      this.hydrated = true
    },
    async logout() {
      try {
        await authService.logout()
      } finally {
        this.user = null
        this.isAdmin = false
      }
    },
    async refresh() {
      try {
        const res = await authService.refresh()
        this.user = res.user
        this.isAdmin = res.is_admin
      } catch {
        this.user = null
        this.isAdmin = false
      }
    },
    // Called once on app startup: the cookie is the source of truth.
    async hydrate() {
      try {
        const res = await authService.me()
        this.user = res.user
        this.isAdmin = res.is_admin
      } catch {
        this.user = null
        this.isAdmin = false
      } finally {
        this.hydrated = true
      }
    },
    async changePassword(payload: ChangePasswordPayload) {
      const res = await authService.changePassword(payload)
      this.user = res.user
      this.isAdmin = res.is_admin
    },
  },
})
