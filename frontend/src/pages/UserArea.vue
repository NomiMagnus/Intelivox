<template>
  <div class="space-y-6">
    <Card>
      <div class="grid gap-6 lg:grid-cols-2">
        <div>
          <h1 class="text-3xl font-semibold text-white">User Area</h1>
          <p class="mt-2 text-slate-400">View and update your profile details.</p>
        </div>
        <div class="rounded-3xl bg-slate-950/90 p-6 text-slate-300 ring-1 ring-white/10">
          <p class="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Signed in as</p>
          <p class="mt-3 text-xl font-semibold text-white">Intelivox User</p>
          <p class="text-slate-400">user@intelivox.local</p>
        </div>
      </div>
    </Card>

    <Card>
      <h2 class="text-xl font-semibold text-white">Account details</h2>
      <div class="mt-6 grid gap-4 sm:grid-cols-2">
        <div>
          <label class="block text-sm text-slate-400">Full name</label>
          <input class="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-slate-100 outline-none" value="Intelivox User" />
        </div>
        <div>
          <label class="block text-sm text-slate-400">Email address</label>
          <input class="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-slate-100 outline-none" value="user@intelivox.local" />
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
