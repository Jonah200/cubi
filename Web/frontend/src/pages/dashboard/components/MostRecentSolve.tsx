import { formatTime } from '@/lib/utils'

type MostRecentSolveProps = {
  time: number
}

export default function MostRecentSolve({ time }: MostRecentSolveProps) {
  return (
    <div className="flex flex-col">
      <span className="text-9xl font-bold tabular-nums">{formatTime(time)}</span>
      <span className="text-base font-semibold uppercase tracking-wide text-muted-foreground">
        Most Recent
      </span>
    </div>
  )
}
