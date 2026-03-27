import { Outlet, Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'
import {
  Database,
  Search,
  LayoutGrid,
  LogOut,
  Menu,
  X,
} from 'lucide-react'
import { useState } from 'react'

const navItems = [
  { path: '/erd', label: 'ERD Viewer', icon: Database },
  { path: '/query', label: 'Query', icon: Search },
  { path: '/schema', label: 'Schema', icon: LayoutGrid },
]

export function Layout() {
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Database className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">OracleVision</span>
            </div>

            {/* Desktop Nav */}
            <nav className="hidden md:flex items-center gap-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-blue-50 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {item.label}
                  </Link>
                )
              })}
            </nav>

            {/* User & Mobile Menu */}
            <div className="flex items-center gap-4">
              <div className="hidden md:flex items-center gap-3">
                <span className="text-sm text-gray-600">{user?.name}</span>
                <button
                  onClick={logout}
                  className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
              <button
                className="md:hidden p-2 text-gray-600"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Nav */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200 bg-white">
            <div className="px-4 py-3 space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium ${
                      isActive
                        ? 'bg-blue-50 text-blue-700'
                        : 'text-gray-600'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    {item.label}
                  </Link>
                )
              })}
              <button
                onClick={logout}
                className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 w-full"
              >
                <LogOut className="w-5 h-5" />
                Logout
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Outlet />
      </main>
    </div>
  )
}
