<template>
  <div class="space-y-8">
    <div class="rounded-3xl border border-white/10 bg-slate-950/90 p-8 shadow-2xl shadow-black/20">
      <div class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 class="text-4xl font-semibold text-white">Welcome to Intelivox</h1>
          <p class="mt-3 max-w-2xl text-slate-400">A scalable frontend structure designed for resident search, configuration, and user management.</p>
        </div>
        <div class="space-x-3">
          <button class="rounded-2xl bg-sky-500 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-sky-400">Open dashboard</button>
          <button class="rounded-2xl border border-white/10 bg-slate-800 px-5 py-3 text-sm font-semibold text-slate-100 transition hover:bg-slate-700">View residents</button>
        </div>
      </div>
    </div>

    <div class="grid gap-6 lg:grid-cols-2">
      <div class="rounded-3xl border border-white/10 bg-slate-950/90 p-6 shadow-xl shadow-black/20">
        <h2 class="text-2xl font-semibold text-white">Project architecture</h2>
        <ul class="mt-4 space-y-2 text-slate-300">
          <li>• Clean folder separation for pages, stores, services, and composables</li>
          <li>• Right-side navigation panel with main content area on left</li>
          <li>• Tailwind utility styling with responsive design</li>
          <li>• TypeScript support and environment-based API configuration</li>
        </ul>
      </div>
      <div class="rounded-3xl border border-white/10 bg-slate-950/90 p-6 shadow-xl shadow-black/20">
        <h2 class="text-2xl font-semibold text-white">Get started</h2>
        <p class="mt-4 text-slate-400">Use the sidebar to navigate between pages and build the resident search workflow next. The app is ready to expand with backend integration and authentication later.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>
