<template>
  <div class="space-y-6 lg:space-y-8">
    <div class="neo-hero p-6 lg:p-8">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p class="neo-label">{{ $t('home.welcomeLabel') }}</p>
          <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white lg:text-4xl">{{ $t('home.welcomeTitle') }}</h1>
          <p class="mt-3 max-w-2xl text-neo-muted">
            {{ $t('home.welcomeSubtitle') }}
          </p>
        </div>
        <div class="flex flex-col gap-3 sm:flex-row">
          <Button>{{ $t('home.openDashboard') }}</Button>
          <Button variant="secondary">{{ $t('home.viewResidents') }}</Button>
        </div>
      </div>
    </div>

    <div class="grid gap-4 lg:grid-cols-2 lg:gap-6">
      <Card>
        <h2 class="text-xl font-semibold text-white lg:text-2xl">{{ $t('home.architectureTitle') }}</h2>
        <ul class="mt-4 space-y-2 text-sm text-neo-muted lg:text-base">
          <li>• {{ $t('home.arch1') }}</li>
          <li>• {{ $t('home.arch2') }}</li>
          <li>• {{ $t('home.arch3') }}</li>
          <li>• {{ $t('home.arch4') }}</li>
        </ul>
      </Card>
      <Card>
        <h2 class="text-xl font-semibold text-white lg:text-2xl">{{ $t('home.getStartedTitle') }}</h2>
        <p class="mt-4 text-sm text-neo-muted lg:text-base">
          {{ $t('home.getStartedBody') }}
        </p>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '../components/ui/Button.vue'
import Card from '../components/ui/Card.vue'
</script>
