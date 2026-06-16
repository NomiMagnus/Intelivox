import type { Resident } from '../types'
import api from './api'

export async function fetchResidents(): Promise<Resident[]> {
  const response = await api.get<Resident[]>('/residents')
  return response.data
}

export async function searchResidents(term: string): Promise<Resident[]> {
  const response = await api.get<Resident[]>('/residents', {
    params: { q: term },
  })
  return response.data
}
