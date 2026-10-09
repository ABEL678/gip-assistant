import { Link, Outlet, useLocation } from "react-router-dom"
import { Building2 } from "lucide-react"

export function Layout() {
  const location = useLocation()

  const navItems = [
    { to: "/", label: "Проекты" },
  ]

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto flex h-14 items-center gap-6 px-4">
          <Link to="/" className="flex items-center gap-2 font-semibold">
            <Building2 className="h-5 w-5" />
            <span>ГИП-Ассистент</span>
          </Link>
          <nav className="flex items-center gap-4 text-sm">
            {navItems.map((item) => {
              const isActive =
                item.to === "/"
                  ? location.pathname === "/"
                  : location.pathname.startsWith(item.to)
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={
                    isActive
                      ? "text-foreground font-medium"
                      : "text-muted-foreground hover:text-foreground transition-colors"
                  }
                >
                  {item.label}
                </Link>
              )
            })}
          </nav>
        </div>
      </header>
      <main className="container mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}