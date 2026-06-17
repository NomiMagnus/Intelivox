<template>
  <div class="neo-bg min-h-screen text-white">
    <div class="mx-auto flex min-h-screen max-w-[1600px] flex-col-reverse gap-4 p-4 lg:flex-row lg:gap-6 lg:p-6">
      <main class="neo-panel flex-1 p-4 lg:p-6">
        <router-view />
      </main>
      <aside class="neo-panel w-full shrink-0 p-3 lg:w-80 lg:p-4">
        <Sidebar />
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from './Sidebar.vue'
</script>
