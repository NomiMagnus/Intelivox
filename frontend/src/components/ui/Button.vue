<template>
  <button
    :class="['rounded-2xl px-4 py-2 text-sm font-semibold transition', variantClasses]"
    :type="type"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { defineProps } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
  },
  type: {
    type: String,
    default: 'button',
  },
})

const variantClasses = computed(() => {
  return props.variant === 'secondary'
    ? 'bg-slate-800 text-slate-100 ring-1 ring-white/10 hover:bg-slate-700'
    : 'bg-sky-500 text-slate-950 hover:bg-sky-400'
})
</script>
