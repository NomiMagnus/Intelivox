<template>
  <div class="space-y-6">
    <div class="neo-hero p-6">
      <p class="neo-label">Preferences</p>
      <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">Settings</h1>
      <p class="mt-2 text-neo-muted">Adjust application preferences and interface options.</p>
    </div>

    <div class="grid gap-4 lg:grid-cols-2 lg:gap-6">
      <Card>
        <h2 class="text-xl font-semibold text-white">General</h2>
        <div class="mt-4 space-y-4">
          <div class="space-y-2">
            <label class="neo-label">Theme mode</label>
            <select class="neo-select mt-1">
              <option>Dark</option>
              <option>Light</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="neo-label">Data refresh</label>
            <select class="neo-select mt-1">
              <option>Manual</option>
              <option>Auto</option>
            </select>
          </div>
        </div>
      </Card>

      <Card>
        <h2 class="text-xl font-semibold text-white">Notifications</h2>
        <div class="mt-4 space-y-4">
          <label class="flex items-center gap-4 text-sm text-neo-muted">
            <input type="checkbox" class="h-5 w-5 rounded border-white/10 bg-neo-bg text-neo-accent focus:ring-neo-accent/30" checked />
            Enable resident alerts
          </label>
          <label class="flex items-center gap-4 text-sm text-neo-muted">
            <input type="checkbox" class="h-5 w-5 rounded border-white/10 bg-neo-bg text-neo-accent focus:ring-neo-accent/30" />
            Receive email notifications
          </label>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts"></script>
