<template>
  <RouterLink
    :to="to"
    class="group flex flex-col items-center gap-1 rounded-neo px-2 py-2 text-center transition duration-200 lg:flex-row lg:gap-3 lg:px-4 lg:py-3 lg:text-left"
    active-class="lg:bg-neo-elevated"
  >
    <span
      :class="[
        'neo-nav-icon text-base',
        isActive ? 'neo-nav-icon-active' : 'group-hover:text-white',
      ]"
    >
      <i :class="icon" aria-hidden="true"></i>
    </span>
    <span class="text-[10px] font-medium text-neo-muted transition group-hover:text-white lg:text-sm" :class="{ 'text-white': isActive }">
      {{ label }}
    </span>
  </RouterLink>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'

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

const route = useRoute()

const label = computed(() => {
  return props.to === '/'
    ? 'Home'
    : props.to
        .slice(1)
        .replace(/-/g, ' ')
        .replace(/\b\w/g, (ch) => ch.toUpperCase())
})

const isActive = computed(() => route.path === props.to)
</script>
