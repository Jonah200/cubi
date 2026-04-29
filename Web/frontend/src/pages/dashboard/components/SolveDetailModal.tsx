import type { Solve } from '@/api/models'
import Modal from '@/components/Modal'
import { formatTime } from '@/lib/utils'

type SolveDetailModalProps = {
  solve: Solve | null
  open: boolean
  onOpenChange: (open: boolean) => void
}

export default function SolveDetailModal({ solve, open, onOpenChange }: SolveDetailModalProps) {
  if (!solve) return null

  return (
    <Modal open={open} onOpenChange={onOpenChange} title={`Solve #${solve.solveNo}`}>
      <div className="space-y-8">
        <div>
          <span className="text-lg text-muted-foreground">Time</span>
          <p className="font-heading text-7xl font-bold">{formatTime(solve.solveTime)}</p>
        </div>
        <div>
          <span className="text-lg text-muted-foreground">Scramble</span>
          <p className="font-mono text-lg">{solve.scramble}</p>
        </div>
        <div>
          <span className="text-lg text-muted-foreground">Date</span>
          <p className="text-lg">{new Date(solve.createdAt).toLocaleString()}</p>
        </div>
      </div>
    </Modal>
  )
}
