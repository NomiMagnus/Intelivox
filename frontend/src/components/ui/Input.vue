<template>
  <input
    class="w-full rounded-2xl border border-white/10 bg-slate-950/90 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-400/20"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])
</script>
