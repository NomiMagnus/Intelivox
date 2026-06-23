import type { RouteRecordRaw } from 'vue-router'
import { RouterView } from 'vue-router'
import Home from '../pages/Home.vue'
import SearchResidents from '../pages/SearchResidents.vue'
import UpdateResident from '../pages/UpdateResident.vue'
import UserArea from '../pages/UserArea.vue'
import NotFound from '../pages/NotFound.vue'
import { SUPPORTED_LOCALES } from '../i18n'
import { resolvePreferredLocale } from '../stores/locale'

// e.g. "he|en" — generated from SUPPORTED_LOCALES so new languages match automatically.
const localePattern = SUPPORTED_LOCALES.join('|')

const routes: RouteRecordRaw[] = [
  {
    // All app routes live under a locale prefix: /he/..., /en/...
    path: `/:locale(${localePattern})`,
    component: RouterView, // pass-through; renders the matched child
    children: [
      { path: '', name: 'Home', component: Home },
      { path: 'search', name: 'SearchResidents', component: SearchResidents },
      { path: 'update', name: 'UpdateResident', component: UpdateResident },
      { path: 'user', name: 'UserArea', component: UserArea },
      { path: 'forbidden', name: 'Forbidden', component: NotFound, meta: { forbidden: true } },
      { path: ':pathMatch(.*)*', name: 'NotFound', component: NotFound },
    ],
  },
  {
    // Unprefixed or unknown-locale paths -> redirect into the preferred locale.
    path: '/:pathMatch(.*)*',
    redirect: (to) => {
      const target = resolvePreferredLocale()
      const rest = to.path === '/' ? '' : to.path
      return `/${target}${rest}`
    },
  },
]

export default routes
