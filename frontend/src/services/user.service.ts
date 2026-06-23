import type { Role, User, UserCreatePayload } from '../types'
import api from './api'

export async function fetchUsers(q?: string): Promise<User[]> {
  const response = await api.get<User[]>('/users', { params: q ? { q } : undefined })
  return response.data
}

export async function getUser(id: string): Promise<User> {
  const response = await api.get<User>(`/users/${id}`)
  return response.data
}

export async function createUser(payload: UserCreatePayload): Promise<User> {
  const response = await api.post<User>('/users', payload)
  return response.data
}

export async function updateUser(id: string, data: Partial<User>): Promise<User> {
  const response = await api.patch<User>(`/users/${id}`, data)
  return response.data
}

// Soft delete: the backend flips the user to inactive, it is never removed.
export async function deleteUser(id: string): Promise<User> {
  const response = await api.delete<User>(`/users/${id}`)
  return response.data
}

export async function fetchRoles(): Promise<Role[]> {
  const response = await api.get<Role[]>('/roles')
  return response.data
}

export async function assignRole(
  userId: string,
  payload: { role_code: string; start_date?: string; end_date?: string },
): Promise<User> {
  const response = await api.post<User>(`/users/${userId}/roles`, payload)
  return response.data
}
