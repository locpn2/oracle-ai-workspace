import { Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { ReactFlowProvider } from '@xyflow/react'
import { Layout } from './components/common/Layout'
import { LoginPage } from './pages/LoginPage'
import { ERDPage } from './pages/ERDPage'
import { QueryPage } from './pages/QueryPage'
import { SchemaPage } from './pages/SchemaPage'
import { useAuthStore } from './stores/authStore'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

function App() {
  return (
    <>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Navigate to="/erd" replace />} />
          <Route path="erd" element={
            <ReactFlowProvider>
              <ERDPage />
            </ReactFlowProvider>
          } />
          <Route path="query" element={<QueryPage />} />
          <Route path="schema" element={<SchemaPage />} />
        </Route>
      </Routes>
    </>
  )
}

export default App
