import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import routes from './router'
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

createApp(App).use(pinia).use(router).use(PrimeVue).mount('#app')
