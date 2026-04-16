import { formatTime } from '@/lib/utils'
import type { DashboardStats } from '@/mock/stats'
import StatCard from './StatCard'

type BestStatsGridProps = {
  stats: DashboardStats
}

export default function BestStatsGrid({ stats }: BestStatsGridProps) {
  return (
    <div className="col-span-2 grid grid-cols-2 gap-4">
      <StatCard label="Best Single" value={formatTime(stats.bestSingle)} />
      <StatCard label="Best Average of 5" value={formatTime(stats.bestAo5)} />
      <StatCard label="Best Average of 10" value={formatTime(stats.bestAo10)} />
      <StatCard label="Best Average of 50" value={formatTime(stats.bestAo50)} />
    </div>
  )
}
