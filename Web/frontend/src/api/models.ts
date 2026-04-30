export type User = {
  id: number
  username: string
  firstName: string
  lastName: string
  email: string
  hasDevice: boolean
}

export type LoginRequest = {
  username: string
  password: string
}

export type SignupRequest = {
  username: string
  firstName: string
  lastName: string
  email?: string
  password: string
}

export type AuthResponse = {
  id: number
  username: string
}

export type Solve = {
  solveNo: number
  scramble: string
  solveTime: number
  createdAt: string
}

export type Device = {
  deviceId: string
  deviceName: string
}

export type DashboardStats = {
  mostRecent: number | null
  averageOf5: number | null
  averageOf10: number | null
  bestSingle: number | null
  bestAo5: number | null
  bestAo10: number | null
  bestAo50: number | null
}
