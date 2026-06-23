<template>
  <div class="flex h-full flex-col gap-4 lg:gap-6">
    <div class="hero hidden lg:block">
      <img :src="heroImg" class="base" width="170" height="179" alt="" />
      <img :src="vueLogo" class="framework" alt="Vue logo" />
      <img :src="viteLogo" class="vite" alt="Vite logo" />
    </div>

    <div class="hidden border-b border-white/[0.06] pb-4 lg:block">
      <p class="neo-label">{{ $t('sidebar.dashboard') }}</p>
      <div class="mt-1 text-2xl font-semibold tracking-tight">{{ $t('sidebar.brand') }}</div>
      <p class="mt-1 text-sm text-neo-muted">{{ $t('sidebar.tagline') }}</p>
    </div>

    <nav class="flex items-center justify-between gap-1 overflow-x-auto lg:flex-col lg:items-stretch lg:gap-2">
      <SidebarLink name="Home" label-key="nav.home" icon="pi pi-home" />
      <SidebarLink name="UpdateResident" label-key="nav.update" icon="pi pi-pencil" />
      <SidebarLink name="SearchResidents" label-key="nav.search" icon="pi pi-search" />
      <SidebarLink name="UserArea" label-key="nav.user" icon="pi pi-user" />
      <SidebarLink v-if="auth.isAdmin" name="UserManagement" label-key="nav.users" icon="pi pi-users" />
      <SidebarLink
        v-if="auth.isAuthenticated"
        label-key="nav.logout"
        icon="pi pi-sign-out"
        is-button
        @click="handleLogout"
      />
      <SidebarLink v-else name="Login" label-key="nav.login" icon="pi pi-sign-in" />
    </nav>

    <div class="neo-raised mt-auto hidden p-4 text-sm lg:block">
      <div class="font-semibold">{{ $t('sidebar.quickStatus') }}</div>
      <p class="mt-2 text-neo-muted">
        {{ $t('sidebar.localEnv') }}
        <span class="font-medium text-neo-accent">dev</span>
      </p>
      <p class="mt-1 truncate text-neo-muted">
        {{ $t('sidebar.apiUrl') }}
        <span class="font-medium text-white">{{ apiUrl }}</span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import SidebarLink from './ui/SidebarLink.vue'
import viteLogo from '../assets/vite.svg'
import heroImg from '../assets/hero.png'
import vueLogo from '../assets/vue.svg'

const apiUrl = computed(() => import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000')

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const { locale } = useI18n()

async function handleLogout() {
  await auth.logout()
  const loc = (route.params.locale as string) ?? locale.value
  router.push({ name: 'Login', params: { locale: loc } })
}
</script>
