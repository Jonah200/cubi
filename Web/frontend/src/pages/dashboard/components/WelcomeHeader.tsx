type WelcomeHeaderProps = {
  firstName: string
}

export default function WelcomeHeader({ firstName }: WelcomeHeaderProps) {
  return <h1 className="text-3xl">Welcome back, {firstName}</h1>
}
