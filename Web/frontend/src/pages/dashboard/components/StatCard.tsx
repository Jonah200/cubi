import { Card, CardContent } from '@/components/ui/card'
import { cn } from '@/lib/utils'

type StatCardProps = {
  label: string
  value: string
  variant?: 'primary' | 'white'
}

export default function StatCard({ label, value, variant = 'primary' }: StatCardProps) {
  return (
    <Card className={cn('ring-0', variant === 'primary' ? 'bg-primary/15' : 'bg-white')}>
      <CardContent className="flex flex-col py-4">
        <span className="text-6xl font-bold tabular-nums">{value}</span>
        <span className="text-base font-semibold uppercase tracking-wide text-muted-foreground">
          {label}
        </span>
      </CardContent>
    </Card>
  )
}
