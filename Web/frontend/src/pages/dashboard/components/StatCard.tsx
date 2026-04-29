import { Card, CardContent } from '@/components/ui/card'
type StatCardProps = {
  label: string
  value: string
}

export default function StatCard({ label, value }: StatCardProps) {
  return (
    <Card className="ring-0 bg-white shadow-[0_0_8px_rgba(0,0,0,0.1)]">
      <CardContent className="flex flex-col py-4">
        <span className="font-heading text-7xl tabular-nums">{value}</span>
        <span className="text-xl font-semibold uppercase tracking-wide text-muted-foreground">
          {label}
        </span>
      </CardContent>
    </Card>
  )
}
