import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router'
import { useMe } from '@/hooks/queries'
import AuthPage from '@/pages/auth/AuthPage'
import DashboardPage from '@/pages/dashboard/DashboardPage'

function ProtectedRoute() {
  const { data: user, isLoading } = useMe()

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-muted-foreground">Loading...</p>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <Outlet context={user} />
}

function GuestRoute() {
  const { data: user, isLoading } = useMe()

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-muted-foreground">Loading...</p>
      </div>
    )
  }

  if (user) {
    return <Navigate to="/" replace />
  }

  return <Outlet />
}

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<GuestRoute />}>
          <Route path="/login" element={<AuthPage />} />
        </Route>
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<DashboardPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
