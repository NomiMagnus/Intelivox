import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import routes from './router'
import i18n, { isSupportedLocale } from './i18n'
import { applyDirection } from './i18n/direction'
import { useLocaleStore } from './stores/locale'
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

app.mount('#app')
