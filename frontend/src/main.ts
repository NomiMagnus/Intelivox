import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import routes from './router'
import i18n, { isSupportedLocale } from './i18n'
import { applyDirection } from './i18n/direction'
import { useLocaleStore } from './stores/locale'
import { useAuthStore } from './stores/auth'
import './style.css'

import PrimeVue from 'primevue/config'
import 'primevue/resources/themes/saga-blue/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(pinia).use(router).use(PrimeVue).use(i18n)

// Keep i18n locale, document direction, and the persisted choice in sync with
// the URL's locale prefix (guaranteed valid by the route's locale matcher).
router.beforeEach((to) => {
  const loc = to.params.locale
  if (isSupportedLocale(loc)) {
    i18n.global.locale.value = loc
    useLocaleStore().setLocale(loc)
    applyDirection(loc)
  }
})

// Auth guard: the httpOnly cookie is the source of truth, so hydrate once via
// /auth/me before resolving the first navigation, then gate access.
router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.hydrated) {
    await auth.hydrate()
  }

  const locale = (isSupportedLocale(to.params.locale) ? to.params.locale : 'he') as string

  if (to.meta.public || to.meta.forbidden) return true

  if (!auth.isAuthenticated) {
    return { name: 'Login', params: { locale } }
  }

  if (auth.mustChangePassword && to.name !== 'ChangePassword') {
    return { name: 'ChangePassword', params: { locale } }
  }

  if (to.meta.admin && !auth.isAdmin) {
    return { name: 'Forbidden', params: { locale } }
  }

  return true
})

app.mount('#app')
