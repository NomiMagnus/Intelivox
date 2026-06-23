import { storeToRefs } from 'pinia'
import { useAuthStore } from '../stores/auth'

export function useAuth() {
  const store = useAuthStore()
  const { user, isAuthenticated, isAdmin, displayName, userEmail, mustChangePassword } =
    storeToRefs(store)

  return {
    user,
    isAuthenticated,
    isAdmin,
    displayName,
    userEmail,
    mustChangePassword,
    login: store.login,
    logout: store.logout,
    changePassword: store.changePassword,
  }
}
