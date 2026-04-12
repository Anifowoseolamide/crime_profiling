import { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [officer, setOfficer] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem('lagoscp_token');
    const storedOfficer = localStorage.getItem('lagoscp_officer');
    if (storedToken && storedOfficer) {
      setToken(storedToken);
      setOfficer(JSON.parse(storedOfficer));
    }
    setLoading(false);
  }, []);

  const login = async (badgeId, password) => {
    const result = await api.login(badgeId, password);
    localStorage.setItem('lagoscp_token', result.token);
    localStorage.setItem('lagoscp_officer', JSON.stringify(result.user));
    setToken(result.token);
    setOfficer(result.user);
    return result;
  };

  const logout = () => {
    localStorage.removeItem('lagoscp_token');
    localStorage.removeItem('lagoscp_officer');
    setToken(null);
    setOfficer(null);
  };

  return (
    <AuthContext.Provider value={{ officer, token, login, logout, isAuthenticated: !!token, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
