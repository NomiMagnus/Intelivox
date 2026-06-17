<template>
  <input
    class="neo-inset w-full px-4 py-3 text-sm text-white transition duration-200 placeholder:text-neo-muted focus:ring-2 focus:ring-neo-accent/30"
    :value="modelValue"
    @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

defineEmits(['update:modelValue'])
</script>
