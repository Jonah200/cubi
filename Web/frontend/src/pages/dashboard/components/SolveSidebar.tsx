import { useState } from 'react'
import { Button } from '@/components/ui/button'
import type { Solve, User } from '@/api/models'
import SolveHistoryItem from './SolveHistoryItem'
import ProfileModal from './ProfileModal'

type SolveSidebarProps = {
  solves: Solve[]
  user: User
}

export default function SolveSidebar({ solves, user }: SolveSidebarProps) {
  const [profileOpen, setProfileOpen] = useState(false)

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
        <Button variant="outline" className="w-full" onClick={() => setProfileOpen(true)}>
          My Profile
        </Button>
      </div>
      <ProfileModal user={user} open={profileOpen} onOpenChange={setProfileOpen} />
    </div>
  )
}
