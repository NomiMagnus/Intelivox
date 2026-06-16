<template>
  <Transition name="toast">
    <div v-if="show" :class="['fixed top-4 right-4 z-[100] rounded-xl border px-6 py-4 shadow-xl', typeClasses]">
      <p class="font-medium">{{ message }}</p>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  message: string
  type?: 'success' | 'error' | 'info'
  duration?: number
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  duration: 3000
})

const show = ref(false)

const typeClasses = {
  success: 'bg-green-950 border-green-500/50 text-green-100',
  error: 'bg-red-950 border-red-500/50 text-red-100',
  info: 'bg-slate-950 border-sky-500/50 text-sky-100'
}[props.type]

let timeoutId: number | null = null

watch(() => props.message, (newMessage) => {
  if (newMessage) {
    show.value = true
    if (timeoutId) clearTimeout(timeoutId)
    timeoutId = window.setTimeout(() => {
      show.value = false
    }, props.duration)
  }
}, { immediate: true })
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
