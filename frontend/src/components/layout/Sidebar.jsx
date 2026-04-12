import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  LayoutDashboard, Camera, Users, AlertTriangle,
  Map, ClipboardList, LogOut, Shield
} from 'lucide-react';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard', minAccess: 1 },
  { to: '/field-scan', icon: Camera, label: 'Field Scan', minAccess: 1 },
  { to: '/subjects', icon: Users, label: 'Subjects', minAccess: 1 },
  { to: '/wanted', icon: AlertTriangle, label: 'Wanted', minAccess: 1 },
  { to: '/map', icon: Map, label: 'Geo-Intel Map', minAccess: 1 },
  { to: '/audit', icon: ClipboardList, label: 'Audit Log', minAccess: 2 },
];

export default function Sidebar({ mobileOpen, onClose }) {
  const { officer, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/70 z-20 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside className={`
        fixed left-0 top-0 h-full z-30 w-64 flex flex-col
        bg-card-light dark:bg-card border-r border-border-color-light dark:border-border-color
        transform transition-transform duration-300 ease-in-out
        ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 lg:static lg:z-auto
      `}>
        {/* Logo */}
        <div className="p-5 border-b border-border-color-light dark:border-border-color flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-accent-blue flex items-center justify-center flex-shrink-0">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="text-sm font-bold text-text-primary-light dark:text-text-primary leading-tight tracking-wider uppercase">
              LagosCP
            </div>
            <div className="text-[10px] text-gray-400 font-mono tracking-widest uppercase">
              Intelligence Division
            </div>
          </div>
        </div>

        {/* Officer info */}
        <div className="px-4 py-3 border-b border-border-color-light dark:border-border-color">
          <div className="flex items-center gap-3">
            <img
              src={`https://ui-avatars.com/api/?name=${encodeURIComponent(officer?.name || 'Officer')}&background=1d4ed8&color=fff&size=80`}
              alt="Officer"
              className="w-9 h-9 rounded-full"
            />
            <div className="overflow-hidden">
              <div className="text-xs font-semibold text-text-primary-light dark:text-text-primary truncate">
                {officer?.name}
              </div>
              <div className="text-[10px] text-gray-400 font-mono">{officer?.badgeId}</div>
            </div>
          </div>
          <div className="mt-2 px-2 py-0.5 bg-accent-blue/10 text-accent-blue text-[10px] font-mono rounded-full w-fit">
            {officer?.role}
          </div>
        </div>

        {/* Nav items */}
        <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
          {navItems
            .filter(item => (officer?.accessLevel || 0) >= item.minAccess)
            .map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              onClick={onClose}
              className={({ isActive }) => `
                flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200
                ${isActive
                  ? 'bg-accent-blue text-white shadow-lg shadow-accent-blue/20'
                  : 'text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-white/5 hover:text-text-primary-light dark:hover:text-text-primary'
                }
              `}
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Logout */}
        <div className="p-3 border-t border-border-color-light dark:border-border-color">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-red-50 dark:hover:bg-accent-red/10 hover:text-accent-red transition-all duration-200"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>
    </>
  );
}
