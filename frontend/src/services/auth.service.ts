import type { ChangePasswordPayload, LoginCredentials, MeResponse } from '../types'
import api from './api'

export async function login(credentials: LoginCredentials): Promise<MeResponse> {
  const response = await api.post<MeResponse>('/auth/login', credentials)
  return response.data
}

export async function logout(): Promise<void> {
  await api.post('/auth/logout')
}

export async function refresh(): Promise<MeResponse> {
  const response = await api.post<MeResponse>('/auth/refresh')
  return response.data
}

export async function me(): Promise<MeResponse> {
  const response = await api.get<MeResponse>('/auth/me')
  return response.data
}

export async function changePassword(payload: ChangePasswordPayload): Promise<MeResponse> {
  const response = await api.post<MeResponse>('/auth/change-password', payload)
  return response.data
}
