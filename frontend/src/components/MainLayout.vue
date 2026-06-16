<template>
  <div class="min-h-screen bg-slate-950 text-slate-100">
    <div class="mx-auto flex min-h-screen max-w-[1600px] gap-6 p-4 lg:p-6">
      <main class="flex-1 rounded-3xl bg-slate-900/90 p-4 shadow-2xl shadow-black/40 ring-1 ring-white/10 lg:p-6">
        <router-view />
      </main>
      <aside class="w-full max-w-sm rounded-3xl border border-white/10 bg-slate-900/90 p-4 shadow-2xl shadow-black/30 lg:w-80">
        <Sidebar />
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from './Sidebar.vue'
</script>
