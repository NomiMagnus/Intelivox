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

export async function updateResidentByPhone(mobilePhone: string, data: any): Promise<Resident> {
  const residents = await searchResidents(mobilePhone)
  if (residents.length === 0) {
    throw new Error('Resident not found')
  }
  const residentId = residents[0].id
  const response = await api.patch<Resident>(`/residents/${residentId}`, data)
  return response.data
}

export async function createResident(data: any): Promise<Resident> {
  const response = await api.post<Resident>('/residents', data)
  return response.data
}
