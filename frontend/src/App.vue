<script setup lang="ts">
import MainLayout from './components/MainLayout.vue'
import { useSession } from './composables/useSession'

useSession()
</script>

<template>
  <MainLayout />
</template>
