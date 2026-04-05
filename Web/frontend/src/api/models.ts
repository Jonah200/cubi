export type User = {
  id: number
  username: string
  email: string
}

export type LoginRequest = {
  username: string
  password: string
}

export type SignupRequest = {
  username: string
  email?: string
  password: string
}

export type AuthResponse = {
  id: number
  username: string
}
