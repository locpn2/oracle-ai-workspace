import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import ConnectionsPage from './pages/ConnectionsPage'
import ERDPage from './pages/ERDPage'
import AIQueryPage from './pages/AIQueryPage'
import GroupsPage from './pages/GroupsPage'
import VectorPage from './pages/VectorPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/connections" replace />} />
          <Route path="connections" element={<ConnectionsPage />} />
          <Route path="erd" element={<ERDPage />} />
          <Route path="ai-query" element={<AIQueryPage />} />
          <Route path="groups" element={<GroupsPage />} />
          <Route path="vector" element={<VectorPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
