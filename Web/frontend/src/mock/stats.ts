export type DashboardStats = {
  mostRecent: number
  averageOf5: number
  averageOf10: number
  bestSingle: number
  bestAo5: number
  bestAo10: number
  bestAo50: number
}

export const mockStats: DashboardStats = {
  mostRecent: 12.34,
  averageOf5: 13.38,
  averageOf10: 13.95,
  bestSingle: 10.98,
  bestAo5: 12.74,
  bestAo10: 13.95,
  bestAo50: 14.22,
}
