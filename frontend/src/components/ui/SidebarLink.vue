<template>
  <RouterLink :to="to" class="group flex items-center gap-3 rounded-3xl px-4 py-3 text-sm font-medium transition hover:bg-slate-800 hover:text-white" active-class="bg-slate-800 text-white">
    <span class="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-950 text-slate-300 transition duration-200 group-hover:bg-sky-500 group-hover:text-white">
      <i :class="icon" aria-hidden="true"></i>
    </span>
    <span>{{ label }}</span>
  </RouterLink>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { defineProps, computed } from 'vue'

const props = defineProps({
  to: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
    required: true,
  },
})

const label = computed(() => {
  return props.to === '/'
    ? 'Home'
    : props.to
        .slice(1)
        .replace(/-/g, ' ')
        .replace(/\b\w/g, (ch) => ch.toUpperCase())
})
</script>
