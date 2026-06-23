<template>
  <div class="space-y-6">
    <Card>
      <div class="grid gap-6 lg:grid-cols-2">
        <div>
          <p class="neo-label">{{ $t('userArea.label') }}</p>
          <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">{{ $t('userArea.title') }}</h1>
          <p class="mt-2 text-neo-muted">{{ $t('userArea.subtitle') }}</p>
        </div>
        <div class="neo-inset p-6">
          <p class="neo-label">{{ $t('userArea.signedInAs') }}</p>
          <p class="mt-3 text-xl font-semibold text-white">Intelivox User</p>
          <p class="text-neo-muted">user@intelivox.local</p>
        </div>
      </div>
    </Card>

    <Card>
      <h2 class="text-xl font-semibold text-white">{{ $t('userArea.accountDetails') }}</h2>
      <div class="mt-6 grid gap-4 sm:grid-cols-2">
        <div>
          <label class="neo-label">{{ $t('userArea.fullName') }}</label>
          <input class="neo-inset mt-2 w-full px-4 py-3 text-white" value="Intelivox User" />
        </div>
        <div>
          <label class="neo-label">{{ $t('userArea.emailAddress') }}</label>
          <input class="neo-inset mt-2 w-full px-4 py-3 text-white" value="user@intelivox.local" />
        </div>
      </div>
      <div class="mt-6 flex flex-wrap gap-3">
        <Button>{{ $t('userArea.saveChanges') }}</Button>
        <Button variant="secondary">{{ $t('userArea.disconnect') }}</Button>
      </div>
    </Card>

    <Card>
      <Settings />
    </Card>
  </div>
</template>

<script setup lang="ts">
import Card from '../components/ui/Card.vue'
import Button from '../components/ui/Button.vue'
import Settings from './Settings.vue';
</script>
