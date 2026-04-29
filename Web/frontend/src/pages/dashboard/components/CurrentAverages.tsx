import { formatTime } from '@/lib/utils'

type CurrentAveragesProps = {
  ao5: number | null
  ao10: number | null
}

function AverageCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col px-4">
      <span className="font-heading text-7xl tabular-nums">{value}</span>
      <span className="text-xl font-semibold uppercase tracking-wide text-muted-foreground">
        {label}
      </span>
    </div>
  )
}

export default function CurrentAverages({ ao5, ao10 }: CurrentAveragesProps) {
  return (
    <div className="flex flex-col justify-start gap-6">
      <AverageCard label="Current Average of 5" value={ao5 !== null ? formatTime(ao5) : '—'} />
      <AverageCard label="Current Average of 10" value={ao10 !== null ? formatTime(ao10) : '—'} />
    </div>
  )
}
