<template>
  <div class="space-y-6">
    <div class="neo-hero p-6">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p class="neo-label">Residents</p>
          <h1 class="mt-2 text-3xl font-semibold tracking-tight text-white">Search Residents</h1>
          <p class="mt-2 text-neo-muted">Search and browse resident records from the backend service.</p>
        </div>
        <div class="flex w-full max-w-md flex-col gap-3 sm:flex-row sm:items-center">
          <Input v-model="searchTerm" placeholder="Search by name, room, or status" />
          <Button @click="searchResidents">Search</Button>
        </div>
      </div>
    </div>

    <Card>
      <div class="flex flex-col gap-3">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 class="text-xl font-semibold text-white">Residents list</h2>
            <p class="text-sm text-neo-muted">Found {{ store.residentCount }} residents</p>
          </div>
          <Button variant="secondary" @click="loadResidents">Reload</Button>
        </div>

        <div v-if="store.loading" class="neo-inset p-6 text-neo-muted">Loading residents...</div>

        <div v-else-if="store.error" class="rounded-neo border border-red-500/20 bg-red-500/10 p-6 text-red-200">
          {{ store.error }}
        </div>

        <div v-else-if="store.residency.length === 0" class="neo-inset p-6 text-neo-muted">
          No residents loaded yet. Click Reload to fetch data.
        </div>

        <div class="grid gap-4 md:grid-cols-2">
          <template v-for="resident in store.residency" :key="resident.id">
            <div class="neo-raised p-4 transition duration-200 hover:shadow-neo-glow">
              <div class="flex items-center justify-between gap-3">
                <div>
                  <h3 class="text-lg font-semibold text-white">{{ resident.first_name }} {{ resident.last_name }}</h3>
                  <p class="text-sm text-neo-muted">Type: {{ resident.type }}</p>
                </div>
                <span class="neo-inset rounded-full px-3 py-1 text-xs text-neo-muted">{{ resident.status }}</span>
              </div>
              <div class="mt-3 space-y-1 text-sm text-neo-muted">
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
