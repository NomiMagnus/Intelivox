import { defineStore } from 'pinia'
import type { User } from '../types'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: {
      id: 'user-1',
      name: 'Intelivox User',
      email: 'user@intelivox.local',
      role: 'admin',
    } as User,
  }),
  getters: {
    userName: (state) => state.user.name,
    userEmail: (state) => state.user.email,
  },
  actions: {
    updateUser(user: Partial<User>) {
      this.user = { ...this.user, ...user }
    },
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'intelivox-auth',
        storage: localStorage,
        paths: ['user'],
      },
    ],
  },
})
