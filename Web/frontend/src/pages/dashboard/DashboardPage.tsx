import { useOutletContext } from 'react-router'
import type { User } from '@/api/models'
import { mockSolves } from '@/mock/solves'
import { mockStats } from '@/mock/stats'
import SolveSidebar from './components/SolveSidebar'
import DeviceStatusBar from './components/DeviceStatusBar'
import WelcomeHeader from './components/WelcomeHeader'
import MostRecentSolve from './components/MostRecentSolve'
import CurrentAverages from './components/CurrentAverages'
import BestStatsGrid from './components/BestStatsGrid'

export default function DashboardPage() {
  const user = useOutletContext<User>()
  return (
    <div className="grid h-screen grid-cols-[240px_1fr]">
      <SolveSidebar solves={mockSolves} />
      <main className="flex flex-col gap-8 overflow-y-auto p-8">
        <DeviceStatusBar />
        <WelcomeHeader username={user.username} />
        <div className="grid max-w-[80%] grid-cols-2 gap-x-4 gap-y-8">
          <MostRecentSolve time={mockStats.mostRecent} />
          <CurrentAverages ao5={mockStats.averageOf5} ao10={mockStats.averageOf10} />
          <BestStatsGrid stats={mockStats} />
        </div>
      </main>
    </div>
  )
}
