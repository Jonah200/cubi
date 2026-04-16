import { formatTime } from '@/lib/utils'

type SolveHistoryItemProps = {
  solveNo: number
  solveTime: number
}

export default function SolveHistoryItem({ solveNo, solveTime }: SolveHistoryItemProps) {
  return (
    <div className="flex items-center justify-between px-4 py-4 hover:bg-muted/50">
      <span className="text-sm text-muted-foreground">{solveNo}</span>
      <span className="font-mono text-sm font-medium">{formatTime(solveTime)}</span>
    </div>
  )
}
