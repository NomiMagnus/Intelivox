<template>
  <div class="flex h-full flex-col gap-6">
  <div class="hero">
      <img :src="heroImg" class="base" width="170" height="179" alt="" />
      <img :src="vueLogo" class="framework" alt="Vue logo" />
      <img :src="viteLogo" class="vite" alt="Vite logo" />
    </div>
    <div class="border-b border-white/10 pb-4">
      <div class="text-2xl font-semibold">Intelivox</div>
      <p class="mt-1 text-sm text-slate-400">Control center and resident dashboard</p>
    </div>

    <nav class="flex flex-col gap-2">
      <SidebarLink to="/" icon="pi pi-home" />
      <SidebarLink to="/update" icon="pi pi-pencil" />
      <SidebarLink to="/search" icon="pi pi-search" />
      <SidebarLink to="/settings" icon="pi pi-cog" />
      <SidebarLink to="/user" icon="pi pi-user" />
    </nav>

    <div class="mt-auto rounded-3xl bg-slate-950/80 p-4 text-sm text-slate-300 ring-1 ring-white/10">
      <div class="font-semibold text-slate-100">Quick status</div>
      <p class="mt-2 text-slate-400">Local environment: <span class="font-medium text-sky-300">dev</span></p>
      <p class="mt-1 text-slate-400">API URL: <span class="font-medium text-slate-100">{{ apiUrl }}</span></p>
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
