import { type FormEvent, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useLogin } from '@/hooks/queries'
import { AxiosError } from 'axios'

export default function LoginForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const login = useLogin()

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    login.mutate({ username, password })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="login-username">Username</Label>
        <Input
          id="login-username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="login-password">Password</Label>
        <Input
          id="login-password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      {login.isError && (
        <p className="text-sm text-destructive">
          {login.error instanceof AxiosError
            ? login.error.response?.data?.non_field_errors?.[0] ?? 'Login failed.'
            : 'Login failed.'}
        </p>
      )}
      <Button type="submit" className="w-full" disabled={login.isPending}>
        {login.isPending ? 'Logging in...' : 'Log in'}
      </Button>
    </form>
  )
}
