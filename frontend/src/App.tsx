import { Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import AuditReport from './pages/AuditReport';
import Dashboard from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel';
import Login from './pages/Login';
import Signup from './pages/Signup';
import FixSelection from './pages/FixSelection';
import Layout from './components/Layout';

function App() {
  return (
    <div className="min-h-screen bg-ghost font-sans antialiased">
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<LandingPage />} />
          <Route path="audit/:auditId" element={<AuditReport />} />
          <Route path="fixes/:auditId" element={<FixSelection />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="admin" element={<AdminPanel />} />
          <Route path="login" element={<Login />} />
          <Route path="signup" element={<Signup />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
