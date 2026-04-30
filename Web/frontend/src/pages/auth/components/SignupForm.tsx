import { type FormEvent, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useSignup } from '@/hooks/queries'
import { AxiosError } from 'axios'

export default function SignupForm() {
  const [username, setUsername] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [localError, setLocalError] = useState('')
  const signupMutation = useSignup()

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setLocalError('')
    if (password !== confirmPassword) {
      setLocalError('Passwords do not match.')
      return
    }
    signupMutation.mutate({ username, firstName, lastName, email, password })
  }

  const error = localError
    || (signupMutation.isError
      ? signupMutation.error instanceof AxiosError
        ? Object.values(signupMutation.error.response?.data ?? {}).flat().join(' ')
        : 'Signup failed.'
      : '')

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="signup-username">Username</Label>
        <Input
          id="signup-username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="signup-first-name">First name</Label>
        <Input
          id="signup-first-name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="signup-last-name">Last name</Label>
        <Input
          id="signup-last-name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="signup-email">Email</Label>
        <Input
          id="signup-email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="signup-password">Password</Label>
        <Input
          id="signup-password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="signup-confirm">Confirm password</Label>
        <Input
          id="signup-confirm"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </div>
      {error && <p className="text-sm text-destructive">{error}</p>}
      <Button type="submit" className="w-full" disabled={signupMutation.isPending}>
        {signupMutation.isPending ? 'Signing up...' : 'Sign up'}
      </Button>
    </form>
  )
}
