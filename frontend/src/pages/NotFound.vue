<template>
  <div class="flex min-h-full flex-1 items-center justify-center py-12">
    <div class="neo-hero w-full max-w-xl p-8 text-center lg:p-12">
      <p class="neo-label">{{ content.label }}</p>
      <h1 class="mt-3 text-6xl font-semibold tracking-tight text-white lg:text-7xl">
        {{ content.code }}
      </h1>
      <h2 class="mt-4 text-xl font-semibold text-white lg:text-2xl">{{ content.title }}</h2>
      <p class="mx-auto mt-3 max-w-md text-neo-muted">{{ content.message }}</p>

      <div class="mt-8 flex flex-col justify-center gap-3 sm:flex-col">
        <Button @click="goHome">Back to home</Button>
        <Button variant="secondary" @click="goBack">Go back</Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Button from '../components/ui/Button.vue'

const route = useRoute()
const router = useRouter()

const forbidden = computed(() => route.meta.forbidden === true)

const content = computed(() =>
  forbidden.value
    ? {
        label: 'Access denied',
        code: '403',
        title: 'You don’t have permission',
        message: 'You don’t have permission to view this page. If you believe this is a mistake, contact your administrator.',
      }
    : {
        label: 'Page not found',
        code: '404',
        title: 'This page doesn’t exist',
        message: 'The page you are looking for may have been moved, renamed, or never existed.',
      },
)

function goHome() {
  router.push('/')
}

function goBack() {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>
