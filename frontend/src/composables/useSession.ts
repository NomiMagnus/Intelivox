import { onBeforeUnmount, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Sliding refresh keeps the 20-min cookie alive while the user is active.
const REFRESH_INTERVAL_MS = 15 * 60 * 1000
// Auto-logout after this much inactivity (no mouse/keyboard/touch).
const IDLE_TIMEOUT_MS = 30 * 60 * 1000

const ACTIVITY_EVENTS = ['mousemove', 'mousedown', 'keydown', 'click', 'scroll', 'touchstart']

/**
 * Drives the authenticated session lifecycle. Mount once (in App.vue):
 * - refreshes the token on an interval so an active session never expires
 * - logs the user out after 30 minutes of inactivity
 */
export function useSession() {
  const auth = useAuthStore()
  const router = useRouter()

  let refreshTimer: number | undefined
  let idleTimer: number | undefined

  function clearTimers() {
    if (refreshTimer) window.clearInterval(refreshTimer)
    if (idleTimer) window.clearTimeout(idleTimer)
    refreshTimer = undefined
    idleTimer = undefined
  }

  async function onIdle() {
    await auth.logout()
    const locale = (router.currentRoute.value.params.locale as string) ?? 'he'
    router.push({ name: 'Login', params: { locale } })
  }

  function resetIdleTimer() {
    if (!auth.isAuthenticated) return
    if (idleTimer) window.clearTimeout(idleTimer)
    idleTimer = window.setTimeout(onIdle, IDLE_TIMEOUT_MS)
  }

  function start() {
    clearTimers()
    refreshTimer = window.setInterval(() => {
      if (auth.isAuthenticated) auth.refresh()
    }, REFRESH_INTERVAL_MS)
    resetIdleTimer()
    ACTIVITY_EVENTS.forEach((evt) => window.addEventListener(evt, resetIdleTimer, { passive: true }))
  }

  function stop() {
    clearTimers()
    ACTIVITY_EVENTS.forEach((evt) => window.removeEventListener(evt, resetIdleTimer))
  }

  onMounted(() => {
    if (auth.isAuthenticated) start()
    watch(
      () => auth.isAuthenticated,
      (authed) => (authed ? start() : stop()),
    )
  })

  onBeforeUnmount(stop)
}
