import { useEffect } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { getMe, getSolves, getStats, login, logout, signup } from '@/api/services'
import type { DashboardStats, LoginRequest, SignupRequest, Solve } from '@/api/models'
import { queryKeys } from './query-keys'

export function useMe() {
  return useQuery({
    queryKey: queryKeys.me,
    queryFn: getMe,
    retry: false,
  })
}

export function useLogin() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: LoginRequest) => login(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.me }),
  })
}

export function useSignup() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: SignupRequest) => signup(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.me }),
  })
}

export function useLogout() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: logout,
    onSuccess: () => queryClient.setQueryData(queryKeys.me, null),
  })
}

export function useSolves() {
  return useQuery<Solve[]>({
    queryKey: queryKeys.solves,
    queryFn: getSolves,
  })
}

export function useStats() {
  return useQuery<DashboardStats>({
    queryKey: queryKeys.stats,
    queryFn: getStats,
  })
}

export function useSolveStream() {
  const queryClient = useQueryClient()

  useEffect(() => {
    const es = new EventSource('/api/solves/stream/')

    es.addEventListener('solve', (e) => {
      const solve: Solve = JSON.parse(e.data)

      queryClient.setQueryData<Solve[]>(queryKeys.solves, (old) =>
        old ? [solve, ...old] : [solve],
      )

      queryClient.invalidateQueries({ queryKey: queryKeys.stats })
    })

    return () => es.close()
  }, [queryClient])
}
