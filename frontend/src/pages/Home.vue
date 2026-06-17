<template>
  <div class="space-y-6 lg:space-y-8">
    <div class="neo-hero p-6 lg:p-8">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p class="neo-label">Welcome</p>
          <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white lg:text-4xl">Welcome to Intelivox</h1>
          <p class="mt-3 max-w-2xl text-neo-muted">
            A scalable frontend structure designed for resident search, configuration, and user management.
          </p>
        </div>
        <div class="flex flex-col gap-3 sm:flex-row">
          <Button>Open dashboard</Button>
          <Button variant="secondary">View residents</Button>
        </div>
      </div>
    </div>

    <div class="grid gap-4 lg:grid-cols-2 lg:gap-6">
      <Card>
        <h2 class="text-xl font-semibold text-white lg:text-2xl">Project architecture</h2>
        <ul class="mt-4 space-y-2 text-sm text-neo-muted lg:text-base">
          <li>• Clean folder separation for pages, stores, services, and composables</li>
          <li>• Right-side navigation panel with main content area on left</li>
          <li>• Tailwind utility styling with responsive design</li>
          <li>• TypeScript support and environment-based API configuration</li>
        </ul>
      </Card>
      <Card>
        <h2 class="text-xl font-semibold text-white lg:text-2xl">Get started</h2>
        <p class="mt-4 text-sm text-neo-muted lg:text-base">
          Use the sidebar to navigate between pages and build the resident search workflow next. The app is ready to
          expand with backend integration and authentication later.
        </p>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '../components/ui/Button.vue'
import Card from '../components/ui/Card.vue'
</script>
