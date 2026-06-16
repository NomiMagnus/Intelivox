import { useAuthStore } from '../stores/auth'

export function useAuth() {
  const store = useAuthStore()

  function updateUserName(name: string) {
    store.updateUser({ name })
  }

  return {
    user: store.user,
    userName: store.userName,
    userEmail: store.userEmail,
    updateUserName,
  }
}
