import { api } from './api-client'
import type { AuthResponse, DashboardStats, Device, LoginRequest, SignupRequest, Solve, User } from './models'

export async function fetchCsrf(): Promise<void> {
  await api.get('/auth/csrf/')
}

export async function login(data: LoginRequest): Promise<AuthResponse> {
  const res = await api.post<AuthResponse>('/auth/login/', data)
  return res.data
}

export async function signup(data: SignupRequest): Promise<AuthResponse> {
  const res = await api.post<AuthResponse>('/auth/signup/', {
    username: data.username,
    first_name: data.firstName,
    last_name: data.lastName,
    email: data.email,
    password: data.password,
  })
  return res.data
}

export async function logout(): Promise<void> {
  await api.post('/auth/logout/')
}

export async function getMe(): Promise<User> {
  const res = await api.get<User>('/auth/me/')
  return res.data
}

export async function getSolves(): Promise<Solve[]> {
  const res = await api.get<Solve[]>('/solves/')
  return res.data
}

export async function getStats(): Promise<DashboardStats> {
  const res = await api.get<DashboardStats>('/stats/')
  return res.data
}

export async function associateDevice(code: string): Promise<Device> {
  const res = await api.post<Device>('/devices/associate/', { code })
  return res.data
}
