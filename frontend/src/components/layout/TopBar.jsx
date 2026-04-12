import { Sun, Moon, Bell, Menu } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';

export default function TopBar({ onMenuClick }) {
  const { isDark, toggle } = useTheme();
  const { officer } = useAuth();

  return (
    <header className="h-14 flex items-center justify-between px-4 lg:px-6 border-b border-border-color-light dark:border-border-color bg-card-light dark:bg-card sticky top-0 z-10 flex-shrink-0">
      {/* Left: hamburger (mobile) + system name */}
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuClick}
          className="lg:hidden p-1.5 rounded-md text-gray-500 hover:bg-gray-100 dark:hover:bg-white/10"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div className="hidden sm:flex items-center gap-2">
          <span className="text-xs font-mono text-gray-400 uppercase tracking-widest">
            Lagos State Police Command
          </span>
          <span className="h-3.5 w-px bg-gray-300 dark:bg-gray-600" />
          <span className="text-xs font-mono text-accent-blue uppercase tracking-widest">
            Intelligence Division
          </span>
        </div>
      </div>

      {/* Right: notifications, theme, officer */}
      <div className="flex items-center gap-2">
        {/* Notification Bell */}
        <button className="relative p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors">
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-accent-red rounded-full animate-pulse" />
        </button>

        {/* Theme toggle */}
        <button
          onClick={toggle}
          className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors"
          title="Toggle theme"
        >
          {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>

        {/* Officer badge */}
        <div className="hidden sm:flex items-center gap-2 pl-2 border-l border-border-color-light dark:border-border-color">
          <img
            src={`https://ui-avatars.com/api/?name=${encodeURIComponent(officer?.name || 'Officer')}&background=1d4ed8&color=fff&size=80`}
            alt="Officer"
            className="w-7 h-7 rounded-full"
          />
          <div className="hidden md:block">
            <div className="text-xs font-semibold text-text-primary-light dark:text-text-primary leading-tight">{officer?.name}</div>
            <div className="text-[10px] text-gray-400 font-mono">{officer?.station}</div>
          </div>
        </div>
      </div>
    </header>
  );
}
