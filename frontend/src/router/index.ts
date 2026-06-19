import type { RouteRecordRaw } from 'vue-router'
import Home from '../pages/Home.vue'
import SearchResidents from '../pages/SearchResidents.vue'
import UpdateResident from '../pages/UpdateResident.vue'
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
    path: '/update',
    name: 'UpdateResident',
    component: UpdateResident,
  },
  {
    path: '/user',
    name: 'UserArea',
    component: UserArea,
  },
]

export default routes
