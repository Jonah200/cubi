import { useOutletContext } from 'react-router'
import type { User } from '@/api/models'
import { useSolves, useStats, useSolveStream } from '@/hooks/queries'
import SolveSidebar from './components/SolveSidebar'
import DeviceStatusBar from './components/DeviceStatusBar'
import WelcomeHeader from './components/WelcomeHeader'
import MostRecentSolve from './components/MostRecentSolve'
import CurrentAverages from './components/CurrentAverages'
import BestStatsGrid from './components/BestStatsGrid'

export default function DashboardPage() {
  const user = useOutletContext<User>()
  const { data: solves = [] } = useSolves()
  const { data: stats } = useStats()

  useSolveStream()

  return (
    <div className="grid h-screen grid-cols-[240px_1fr]">
      <SolveSidebar solves={solves} user={user} />
      <main className="flex flex-col gap-8 overflow-y-auto p-8">
        <DeviceStatusBar />
        <WelcomeHeader firstName={user.firstName} />
        <div className="grid max-w-[80%] grid-cols-2 gap-x-4 gap-y-8">
          <MostRecentSolve time={stats?.mostRecent ?? null} />
          <CurrentAverages ao5={stats?.averageOf5 ?? null} ao10={stats?.averageOf10 ?? null} />
          {stats && <BestStatsGrid stats={stats} />}
        </div>
      </main>
    </div>
  )
}
