import { Card, CardContent } from '@/components/ui/card'
type StatCardProps = {
  label: string
  value: string
}

export default function StatCard({ label, value }: StatCardProps) {
  return (
    <Card className="ring-0 bg-white shadow-[0_0_2px_rgba(0,0,0,0.25)]">
      <CardContent className="flex flex-col py-4">
        <span className="font-heading text-6xl tabular-nums">{value}</span>
        <span className="font-label text-xl uppercase tracking-[0.1em] text-muted-foreground">
          {label}
        </span>
      </CardContent>
    </Card>
  )
}
