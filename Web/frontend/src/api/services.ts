import { api } from './api-client'
import type { AuthResponse, LoginRequest, SignupRequest, User } from './models'

export async function fetchCsrf(): Promise<void> {
  await api.get('/auth/csrf/')
}

export async function login(data: LoginRequest): Promise<AuthResponse> {
  const res = await api.post<AuthResponse>('/auth/login/', data)
  return res.data
}

export async function signup(data: SignupRequest): Promise<AuthResponse> {
  const res = await api.post<AuthResponse>('/auth/signup/', data)
  return res.data
}

export async function logout(): Promise<void> {
  await api.post('/auth/logout/')
}

export async function getMe(): Promise<User> {
  const res = await api.get<User>('/auth/me/')
  return res.data
}
