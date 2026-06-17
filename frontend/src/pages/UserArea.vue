<template>
  <div class="space-y-6">
    <Card>
      <div class="grid gap-6 lg:grid-cols-2">
        <div>
          <p class="neo-label">Profile</p>
          <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">User Area</h1>
          <p class="mt-2 text-neo-muted">View and update your profile details.</p>
        </div>
        <div class="neo-inset p-6">
          <p class="neo-label">Signed in as</p>
          <p class="mt-3 text-xl font-semibold text-white">Intelivox User</p>
          <p class="text-neo-muted">user@intelivox.local</p>
        </div>
      </div>
    </Card>

    <Card>
      <h2 class="text-xl font-semibold text-white">Account details</h2>
      <div class="mt-6 grid gap-4 sm:grid-cols-2">
        <div>
          <label class="neo-label">Full name</label>
          <input class="neo-inset mt-2 w-full px-4 py-3 text-white" value="Intelivox User" />
        </div>
        <div>
          <label class="neo-label">Email address</label>
          <input class="neo-inset mt-2 w-full px-4 py-3 text-white" value="user@intelivox.local" />
        </div>
      </div>
      <div class="mt-6 flex flex-wrap gap-3">
        <Button>Save changes</Button>
        <Button variant="secondary">Disconnect</Button>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import Card from '../components/ui/Card.vue'
import Button from '../components/ui/Button.vue'
</script>
