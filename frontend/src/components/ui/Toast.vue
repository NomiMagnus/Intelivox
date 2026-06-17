<template>
  <Transition name="toast">
    <div v-if="show" :class="['neo-raised fixed right-4 top-4 z-[100] px-6 py-4', typeClasses]">
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
  success: 'text-green-200',
  error: 'text-red-200',
  info: 'text-neo-accent'
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
