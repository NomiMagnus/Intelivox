<template>
  <button
    :class="[variant === 'secondary' ? 'neo-btn-secondary' : 'neo-btn-primary', 'px-5 py-3']"
    :type="type as 'button' | 'submit' | 'reset'"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
defineProps({
  variant: {
    type: String,
    default: 'primary',
  },
  type: {
    type: String,
    default: 'button',
  },
})
</script>
