import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

export default function DeviceStatusBar() {
  return (
    <div className="flex items-center gap-3">
      <Badge variant="outline" className="gap-1.5">
        <span className="inline-block h-2 w-2 rounded-full bg-red-500" />
        No device connected
      </Badge>
      <Button variant="link" className="h-auto p-0 text-sm">
        Connect now
      </Button>
    </div>
  )
}
