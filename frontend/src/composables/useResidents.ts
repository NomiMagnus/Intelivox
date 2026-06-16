import { ref } from 'vue'
import { useResidentsStore } from '../stores/residents'
import { fetchResidents, searchResidents } from '../services/resident.service'

export function useResidents() {
  const store = useResidentsStore()
  const query = ref('')

  async function loadResidents() {
    store.setLoading(true)
    store.setError('')
    try {
      const residents = await fetchResidents()
      store.setResidents(residents)
    } catch (error) {
      store.setError('Unable to fetch residents')
    } finally {
      store.setLoading(false)
    }
  }

  async function search(term: string) {
    store.setLoading(true)
    store.setError('')
    try {
      const residents = await searchResidents(term)
      store.setResidents(residents)
    } catch (error) {
      store.setError('Unable to search residents')
    } finally {
      store.setLoading(false)
    }
  }

  return { store, query, loadResidents, search }
}
