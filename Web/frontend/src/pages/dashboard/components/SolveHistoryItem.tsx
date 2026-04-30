import { formatTime } from '@/lib/utils'

type SolveHistoryItemProps = {
  solveNo: number
  solveTime: number
  onClick?: () => void
}

export default function SolveHistoryItem({ solveNo, solveTime, onClick }: SolveHistoryItemProps) {
  return (
    <div className="flex cursor-pointer items-center justify-between px-4 py-4 hover:bg-muted/50" onClick={onClick}>
      <span className="text-sm text-muted-foreground">{solveNo}</span>
      <span className="font-mono text-sm font-medium">{formatTime(solveTime)}</span>
    </div>
  )
}
