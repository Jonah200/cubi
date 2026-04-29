import { useState } from 'react'
import { User as UserIcon } from 'lucide-react'
import { Button } from '@/components/ui/button'
import type { Solve, User } from '@/api/models'
import SolveHistoryItem from './SolveHistoryItem'
import SolveDetailModal from './SolveDetailModal'
import ProfileModal from './ProfileModal'

type SolveSidebarProps = {
  solves: Solve[]
  user: User
}

export default function SolveSidebar({ solves, user }: SolveSidebarProps) {
  const [profileOpen, setProfileOpen] = useState(false)
  const [selectedSolve, setSelectedSolve] = useState<Solve | null>(null)

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
            onClick={() => setSelectedSolve(solve)}
          />
        ))}
      </div>
      <div className="p-4">
        <Button variant="outline" className="w-full py-5" onClick={() => setProfileOpen(true)}>
          <UserIcon className="mr-2 h-4 w-4" />
          My Profile
        </Button>
      </div>
      <SolveDetailModal
        solve={selectedSolve}
        open={selectedSolve !== null}
        onOpenChange={(open) => { if (!open) setSelectedSolve(null) }}
      />
      <ProfileModal user={user} open={profileOpen} onOpenChange={setProfileOpen} />
    </div>
  )
}
