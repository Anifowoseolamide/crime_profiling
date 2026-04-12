import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Layout from '../layout/Layout';

export function ProtectedRoute({ requiredRole = null }) {
  const { isAuthenticated, officer, loading } = useAuth();

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-surface-light dark:bg-surface">
        <div className="text-accent-blue font-mono text-sm animate-pulse">AUTHENTICATING...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && officer?.accessLevel < requiredRole) {
    return (
      <Layout>
        <div className="flex flex-col items-center justify-center h-full gap-4 text-center">
          <div className="text-accent-red text-5xl">🔒</div>
          <h2 className="text-xl font-bold text-text-primary-light dark:text-text-primary">Access Denied</h2>
          <p className="text-gray-400 text-sm">Your role does not have permission to view this area.</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <Outlet />
    </Layout>
  );
}
