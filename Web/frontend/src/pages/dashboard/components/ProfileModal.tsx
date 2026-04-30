import { useNavigate } from 'react-router'
import type { User } from '@/api/models'
import { useLogout } from '@/hooks/queries'
import { Button } from '@/components/ui/button'
import Modal from '@/components/Modal'

type ProfileModalProps = {
  user: User
  open: boolean
  onOpenChange: (open: boolean) => void
}

export default function ProfileModal({ user, open, onOpenChange }: ProfileModalProps) {
  const navigate = useNavigate()
  const { mutate: signOut } = useLogout()

  const handleSignOut = () => {
    signOut(undefined, {
      onSuccess: () => navigate('/login'),
    })
  }

  return (
    <Modal open={open} onOpenChange={onOpenChange} title="My Profile">
      <div className="flex flex-col gap-4">
        <div className="flex flex-col gap-1">
          <p className="text-sm text-muted-foreground">Name</p>
          <p className="font-medium">{user.firstName} {user.lastName}</p>
        </div>
        <div className="flex flex-col gap-1">
          <p className="text-sm text-muted-foreground">Username</p>
          <p className="font-medium">{user.username}</p>
        </div>
        <div className="flex flex-col gap-1">
          <p className="text-sm text-muted-foreground">Email</p>
          <p className="font-medium">{user.email || '—'}</p>
        </div>
        <Button onClick={handleSignOut}>
          Sign Out
        </Button>
      </div>
    </Modal>
  )
}
