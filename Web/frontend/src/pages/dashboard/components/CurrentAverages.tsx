import { formatTime } from '@/lib/utils'

type CurrentAveragesProps = {
  ao5: number
  ao10: number
}

function AverageCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col px-4">
      <span className="text-6xl font-bold tabular-nums">{value}</span>
      <span className="text-base font-semibold uppercase tracking-wide text-muted-foreground">
        {label}
      </span>
    </div>
  )
}

export default function CurrentAverages({ ao5, ao10 }: CurrentAveragesProps) {
  return (
    <div className="flex flex-col justify-start gap-6">
      <AverageCard label="Average of 5" value={formatTime(ao5)} />
      <AverageCard label="Average of 10" value={formatTime(ao10)} />
    </div>
  )
}
