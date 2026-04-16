import { formatTime } from '@/lib/utils'
import type { DashboardStats } from '@/api/models'
import StatCard from './StatCard'

type BestStatsGridProps = {
  stats: DashboardStats
}

export default function BestStatsGrid({ stats }: BestStatsGridProps) {
  return (
    <div className="col-span-2 grid grid-cols-2 gap-4">
      <StatCard label="Best Single" value={stats.bestSingle !== null ? formatTime(stats.bestSingle) : '—'} />
      <StatCard label="Best Average of 5" value={stats.bestAo5 !== null ? formatTime(stats.bestAo5) : '—'} />
      <StatCard label="Best Average of 10" value={stats.bestAo10 !== null ? formatTime(stats.bestAo10) : '—'} />
      <StatCard label="Best Average of 50" value={stats.bestAo50 !== null ? formatTime(stats.bestAo50) : '—'} />
    </div>
  )
}
