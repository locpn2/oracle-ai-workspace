import { Link, useLocation, Outlet } from 'react-router-dom'
import clsx from 'clsx'

const navItems = [
  { path: '/connections', label: 'Kết nối', icon: '🔗' },
  { path: '/erd', label: 'ERD', icon: '📊' },
  { path: '/ai-query', label: 'AI Truy vấn', icon: '🤖' },
  { path: '/groups', label: 'Nhóm dữ liệu', icon: '📁' },
  { path: '/vector', label: 'Vector DB', icon: '🔢' },
]

function Layout() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-primary-600">OracleVision</h1>
              <span className="ml-2 text-sm text-gray-500">AI Database Visualization</span>
            </div>
            <nav className="flex space-x-1" role="navigation" aria-label="Main navigation">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={clsx(
                    'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                    'focus-visible:outline-2 focus-visible:outline-primary-500',
                    location.pathname === item.path
                      ? 'bg-primary-50 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  )}
                  aria-current={location.pathname === item.path ? 'page' : undefined}
                >
                  <span aria-hidden="true">{item.icon}</span>
                  <span className="ml-1">{item.label}</span>
                </Link>
              ))}
            </nav>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-sm text-gray-500">
            OracleVision - AI-Powered Database Visualization Platform
          </p>
        </div>
      </footer>
    </div>
  )
}

export default Layout
