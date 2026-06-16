import { defineStore } from 'pinia'
import type { Resident } from '../types'

export const useResidentsStore = defineStore('residents', {
  state: () => ({
    residency: [] as Resident[],
    loading: false,
    error: '',
  }),
  getters: {
    residentCount: (state) => state.residency.length,
  },
  actions: {
    setResidents(residents: Resident[]) {
      this.residency = residents
    },
    setLoading(value: boolean) {
      this.loading = value
    },
    setError(message: string) {
      this.error = message
    },
  },
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'intelivox-residents',
        storage: localStorage,
        paths: ['residency'],
      },
    ],
  },
})
