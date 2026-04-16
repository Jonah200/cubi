import { Button } from '@/components/ui/button'
import type { Solve } from '@/mock/solves'
import SolveHistoryItem from './SolveHistoryItem'

type SolveSidebarProps = {
  solves: Solve[]
}

export default function SolveSidebar({ solves }: SolveSidebarProps) {
  return (
    <div className="flex h-screen flex-col border-r">
      <div className="border-b px-4 py-3">
        <h2 className="text-lg font-semibold">Cubi</h2>
      </div>
      <div className="flex-1 overflow-y-auto">
        {solves.map((solve) => (
          <SolveHistoryItem
            key={solve.solveNo}
            solveNo={solve.solveNo}
            solveTime={solve.solveTime}
          />
        ))}
      </div>
      <div className="p-4">
        <Button variant="outline" className="w-full">
          My Profile
        </Button>
      </div>
    </div>
  )
}
