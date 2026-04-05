import { useOutletContext } from 'react-router'
import { Button } from '@/components/ui/button'
import { useLogout } from '@/hooks/queries'
import type { User } from '@/api/models'

export default function DashboardPage() {
  const user = useOutletContext<User>()
  const logout = useLogout()

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-2xl font-bold">Welcome, {user.username}</h1>
      <Button variant="outline" onClick={() => logout.mutate()}>
        Log out
      </Button>
    </div>
  )
}
