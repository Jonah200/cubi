import { formatTime } from '@/lib/utils'

type MostRecentSolveProps = {
  time: number | null
}

export default function MostRecentSolve({ time }: MostRecentSolveProps) {
  return (
    <div className="flex flex-col">
      <span className="font-heading text-9xl tabular-nums">{time !== null ? formatTime(time) : '—'}</span>
      <span className="font-label text-xl uppercase tracking-[0.1em] text-muted-foreground">
        Most Recent
      </span>
    </div>
  )
}
