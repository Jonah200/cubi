type WelcomeHeaderProps = {
  username: string
}

export default function WelcomeHeader({ username }: WelcomeHeaderProps) {
  return <h1 className="text-3xl font-bold">Welcome back, {username}</h1>
}
