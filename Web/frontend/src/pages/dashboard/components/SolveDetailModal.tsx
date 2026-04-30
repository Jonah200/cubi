import { useState } from 'react'
import type { Solve } from '@/api/models'
import Modal from '@/components/Modal'
import { Button } from '@/components/ui/button'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { useDeleteSolve } from '@/hooks/queries'
import { formatTime } from '@/lib/utils'
import { Trash2 } from 'lucide-react'

type SolveDetailModalProps = {
  solve: Solve | null
  open: boolean
  onOpenChange: (open: boolean) => void
}

export default function SolveDetailModal({ solve, open, onOpenChange }: SolveDetailModalProps) {
  const [confirmOpen, setConfirmOpen] = useState(false)
  const deleteSolve = useDeleteSolve()

  if (!solve) return null

  function handleDelete() {
    deleteSolve.mutate(solve!.id, {
      onSuccess: () => {
        setConfirmOpen(false)
        onOpenChange(false)
      },
    })
  }

  return (
    <Modal open={open} onOpenChange={onOpenChange} title={`Solve #${solve.solveNo}`}>
      <Popover open={confirmOpen} onOpenChange={setConfirmOpen}>
        <PopoverTrigger
          render={
            <Button
              variant="ghost"
              size="icon-sm"
              className="absolute top-2 right-10"
            />
          }
        >
          <Trash2 />
          <span className="sr-only">Delete solve</span>
        </PopoverTrigger>
        <PopoverContent align="end" className="w-52">
          <p className="text-sm">Are you sure you want to delete this solve?</p>
          <div className="flex gap-2 justify-end">
            <Button variant="outline" size="sm" onClick={() => setConfirmOpen(false)}>
              No
            </Button>
            <Button variant="destructive" size="sm" onClick={handleDelete} disabled={deleteSolve.isPending}>
              Yes
            </Button>
          </div>
        </PopoverContent>
      </Popover>

      <div className="space-y-8">
        <div>
          <span className="text-lg text-muted-foreground">Time</span>
          <p className="font-heading text-7xl">{formatTime(solve.solveTime)}</p>
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
