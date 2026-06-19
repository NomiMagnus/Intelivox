<template>
  <div class="flex h-full flex-col gap-4 lg:gap-6">
    <div class="hero hidden lg:block">
      <img :src="heroImg" class="base" width="170" height="179" alt="" />
      <img :src="vueLogo" class="framework" alt="Vue logo" />
      <img :src="viteLogo" class="vite" alt="Vite logo" />
    </div>

    <div class="hidden border-b border-white/[0.06] pb-4 lg:block">
      <p class="neo-label">Dashboard</p>
      <div class="mt-1 text-2xl font-semibold tracking-tight">Intelivox</div>
      <p class="mt-1 text-sm text-neo-muted">Control center and resident dashboard</p>
    </div>

    <nav class="flex items-center justify-between gap-1 overflow-x-auto lg:flex-col lg:items-stretch lg:gap-2">
      <SidebarLink to="/" icon="pi pi-home" />
      <SidebarLink to="/update" icon="pi pi-pencil" />
      <SidebarLink to="/search" icon="pi pi-search" />
      <SidebarLink to="/user" icon="pi pi-user" />
    </nav>

    <div class="neo-raised mt-auto hidden p-4 text-sm lg:block">
      <div class="font-semibold">Quick status</div>
      <p class="mt-2 text-neo-muted">
        Local environment:
        <span class="font-medium text-neo-accent">dev</span>
      </p>
      <p class="mt-1 truncate text-neo-muted">
        API URL:
        <span class="font-medium text-white">{{ apiUrl }}</span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SidebarLink from './ui/SidebarLink.vue'
import viteLogo from '../assets/vite.svg'
import heroImg from '../assets/hero.png'
import vueLogo from '../assets/vue.svg'

const apiUrl = computed(() => import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000')
</script>
