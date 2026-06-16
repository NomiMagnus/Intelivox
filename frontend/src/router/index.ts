import type { RouteRecordRaw } from 'vue-router'
import Home from '../pages/Home.vue'
import SearchResidents from '../pages/SearchResidents.vue'
import Settings from '../pages/Settings.vue'
import UserArea from '../pages/UserArea.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/search',
    name: 'SearchResidents',
    component: SearchResidents,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
  },
  {
    path: '/user',
    name: 'UserArea',
    component: UserArea,
  },
]

export default routes
