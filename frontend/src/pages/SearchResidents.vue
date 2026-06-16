<template>
  <div class="space-y-6">
    <div class="rounded-3xl border border-white/10 bg-slate-950/90 p-6 shadow-xl shadow-black/20">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 class="text-3xl font-semibold text-white">Search Residents</h1>
          <p class="mt-2 text-slate-400">Search and browse resident records from the backend service.</p>
        </div>
        <div class="flex w-full max-w-md items-center gap-3">
          <Input v-model="searchTerm" placeholder="Search by name, room, or status" />
          <Button @click="searchResidents">Search</Button>
        </div>
      </div>
    </div>

    <div>
      <Card>
        <div class="flex flex-col gap-3">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 class="text-xl font-semibold text-white">Residents list</h2>
              <p class="text-sm text-slate-400">Found {{ store.residentCount }} residents</p>
            </div>
            <Button variant="secondary" @click="loadResidents">Reload</Button>
          </div>

          <div v-if="store.loading" class="rounded-3xl border border-slate-800 bg-slate-950/80 p-6 text-slate-300">
            Loading residents...
          </div>

          <div v-else-if="store.error" class="rounded-3xl border border-red-500/20 bg-red-500/10 p-6 text-red-200">
            {{ store.error }}
          </div>

          <div v-else-if="store.residency.length === 0" class="rounded-3xl border border-white/10 bg-slate-950/80 p-6 text-slate-400">
            No residents loaded yet. Click Reload to fetch data.
          </div>

          <div class="grid gap-4 md:grid-cols-2">
            <template v-for="resident in store.residency" :key="resident.id">
              <div class="rounded-3xl border border-white/10 bg-slate-950/90 p-4 transition hover:border-sky-500/50 hover:bg-slate-900/95">
                <div class="flex items-center justify-between gap-3">
                  <div>
                    <h3 class="text-lg font-semibold text-white">{{ resident.firstName }} {{ resident.lastName }}</h3>
                    <p class="text-sm text-slate-400">Room: {{ resident.room }}</p>
                  </div>
                  <span class="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">{{ resident.status }}</span>
                </div>
                <div class="mt-3 space-y-1 text-sm text-slate-400">
                  <p v-if="resident.mobile_phone" class="flex items-center gap-4"><i class="pi pi-mobile" /> {{ resident.mobile_phone }}</p>
                  <p v-if="resident.home_phone" class="flex items-center gap-4"><i class="pi pi-home" /> {{ resident.home_phone }}</p>
                  <p v-if="resident.work_phone" class="flex items-center gap-4"><i class="pi pi-briefcase" /> {{ resident.work_phone }}</p>
                  <p v-if="resident.email" class="flex items-center gap-4"><i class="pi pi-envelope" /> {{ resident.email }}</p>
                </div>
              </div>
            </template>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useResidents } from '../composables/useResidents'
import Input from '../components/ui/Input.vue'
import Button from '../components/ui/Button.vue'
import Card from '../components/ui/Card.vue'

const { store, loadResidents, search } = useResidents()
const searchTerm = ref('')

function searchResidents() {
  search(searchTerm.value)
}

loadResidents()
</script>
