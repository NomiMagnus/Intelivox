<template>
  <div class="space-y-6">
    <div class="rounded-3xl border border-white/10 bg-slate-950/90 p-6 shadow-xl shadow-black/20">
      <h1 class="text-3xl font-semibold text-white">Settings</h1>
      <p class="mt-2 text-slate-400">Adjust application preferences and interface options.</p>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <Card>
        <h2 class="text-xl font-semibold text-white">General</h2>
        <div class="mt-4 space-y-4">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-slate-300">Theme mode</label>
            <select class="w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none">
              <option>Dark</option>
              <option>Light</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="block text-sm font-medium text-slate-300">Data refresh</label>
            <select class="w-full rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none">
              <option>Manual</option>
              <option>Auto</option>
            </select>
          </div>
        </div>
      </Card>

      <Card>
        <h2 class="text-xl font-semibold text-white">Notifications</h2>
        <div class="mt-4 space-y-4">
          <label class="flex items-center gap-4 text-sm text-slate-300">
            <input type="checkbox" class="h-5 w-5 rounded border-white/10 bg-slate-950 text-sky-500 focus:ring-sky-400" checked />
            Enable resident alerts
          </label>
          <label class="flex items-center gap-4 text-sm text-slate-300">
            <input type="checkbox" class="h-5 w-5 rounded border-white/10 bg-slate-950 text-sky-500 focus:ring-sky-400" />
            Receive email notifications
          </label>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts"></script>
