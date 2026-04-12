import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { ProtectedRoute } from './components/auth/ProtectedRoute';

import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import FieldScan from './pages/FieldScan';
import SubjectSearch from './pages/SubjectSearch';
import SubjectProfile from './pages/SubjectProfile';
import WantedList from './pages/WantedList';
import LogOffence from './pages/LogOffence';
import CreateRecord from './pages/CreateRecord';
import GeoMap from './pages/GeoMap';
import AuditLog from './pages/AuditLog';
import DeclareWanted from './pages/DeclareWanted';

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public */}
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Navigate to="/login" replace />} />

            {/* Protected — all roles */}
            <Route element={<ProtectedRoute requiredRole={1} />}>
              <Route path="/dashboard"     element={<Dashboard />} />
              <Route path="/field-scan"    element={<FieldScan />} />
              <Route path="/subjects"      element={<SubjectSearch />} />
              <Route path="/subjects/:id"  element={<SubjectProfile />} />
              <Route path="/wanted"        element={<WantedList />} />
              <Route path="/wanted/new"    element={<DeclareWanted />} />
              <Route path="/offences/new"  element={<LogOffence />} />
              <Route path="/records/new"   element={<CreateRecord />} />
              <Route path="/map"           element={<GeoMap />} />
            </Route>

            {/* Protected — Supervisor+ only */}
            <Route element={<ProtectedRoute requiredRole={2} />}>
              <Route path="/audit" element={<AuditLog />} />
            </Route>

            {/* 404 → dashboard */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}
