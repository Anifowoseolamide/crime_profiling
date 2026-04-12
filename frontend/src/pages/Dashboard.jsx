import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import StatsCard from '../components/ui/StatsCard';
import StatusBadge from '../components/ui/StatusBadge';
import CrimeMap from '../components/map/CrimeMap';
import { Users, Briefcase, Bell, Camera, AlertTriangle, ChevronRight, Clock } from 'lucide-react';



const actTypeColor = {
  SCAN: 'text-accent-blue',
  WARRANT: 'text-accent-red',
  OFFENCE: 'text-accent-amber',
  VIEW: 'text-gray-400',
};

export default function Dashboard() {
  const navigate = useNavigate();
  const { officer } = useAuth();
  const [wantedList, setWantedList] = useState([]);
  const [activityFeed, setActivityFeed] = useState([]);
  const [stats, setStats] = useState({
    total_subjects: 0,
    active_cases: 0,
    alerts_today: 0,
    scans_today: 0
  });

  useEffect(() => {
    api.getWantedList().then(setWantedList);
    api.getAuditLog().then(setActivityFeed).catch(console.error);
    api.getStats().then(setStats).catch(console.error);
  }, []);

  const greeting = () => {
    const h = new Date().getHours();
    if (h < 12) return 'Good morning';
    if (h < 17) return 'Good afternoon';
    return 'Good evening';
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header row */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <div className="text-xs font-mono text-gray-400 uppercase tracking-widest">{greeting()},</div>
          <h1 className="text-xl font-bold text-text-primary-light dark:text-text-primary">{officer?.name}</h1>
          <div className="text-xs text-gray-500 font-mono">{officer?.station} · {officer?.role}</div>
        </div>
        <button
          id="start-field-scan-btn"
          onClick={() => navigate('/field-scan')}
          className="flex items-center gap-2 bg-accent-blue hover:bg-blue-600 text-white px-5 py-3 rounded-xl font-semibold text-sm transition-all shadow-lg shadow-accent-blue/25 hover:shadow-accent-blue/40"
        >
          <Camera className="w-4 h-4" />
          Start Field Scan
        </button>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <StatsCard icon={Users}       label="Total Subjects"  value={stats.total_subjects}  color="blue"  trend="+0" />
        <StatsCard icon={Briefcase}   label="Active Cases"    value={stats.active_cases}   color="amber" />
        <StatsCard icon={Bell}        label="Alerts Today"    value={stats.alerts_today}    color="red" />
        <StatsCard icon={Camera}      label="Scans Today"     value={stats.scans_today}   color="green" trend="+0" />
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Alert panel */}
        <div className="lg:col-span-1 card-bg rounded-xl overflow-hidden">
          <div className="flex items-center justify-between px-4 py-3 border-b border-border-color-light dark:border-border-color">
            <div className="flex items-center gap-2 text-sm font-semibold text-text-primary-light dark:text-text-primary">
              <AlertTriangle className="w-4 h-4 text-accent-red" />
              Active Alerts
            </div>
            <span className="text-xs bg-accent-red/15 text-accent-red font-mono px-2 py-0.5 rounded-full">
              {wantedList.length} WANTED
            </span>
          </div>
          <div className="divide-y divide-border-color-light dark:divide-border-color">
            {wantedList.map(s => (
              <button
                key={s.id}
                onClick={() => navigate(`/subjects/${s.id}`)}
                className="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors text-left"
              >
                <div className="relative flex-shrink-0">
                  <img src={s.mugshotUrl} alt={s.name} className="w-10 h-10 rounded-lg object-cover" />
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-accent-red rounded-full animate-pulse border-2 border-card-light dark:border-card" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold text-text-primary-light dark:text-text-primary truncate">{s.name}</div>
                  <div className="text-xs text-gray-500 truncate">{s.location}</div>
                </div>
                <StatusBadge status={s.status} />
              </button>
            ))}
            {wantedList.length === 0 && (
              <div className="px-4 py-6 text-center text-sm text-gray-400">No active alerts</div>
            )}
          </div>
          <div className="px-4 py-2.5 border-t border-border-color-light dark:border-border-color">
            <button onClick={() => navigate('/wanted')} className="text-xs text-accent-blue hover:underline flex items-center gap-1">
              View all wanted <ChevronRight className="w-3 h-3" />
            </button>
          </div>
        </div>

        {/* Map */}
        <div className="lg:col-span-2 card-bg rounded-xl overflow-hidden">
          <div className="flex items-center justify-between px-4 py-3 border-b border-border-color-light dark:border-border-color">
            <div className="text-sm font-semibold text-text-primary-light dark:text-text-primary">Crime Hotspot Overview</div>
            <button onClick={() => navigate('/map')} className="text-xs text-accent-blue hover:underline flex items-center gap-1">
              Full map <ChevronRight className="w-3 h-3" />
            </button>
          </div>
          <CrimeMap height="260px" />
        </div>
      </div>

      {/* Activity feed */}
      <div className="card-bg rounded-xl overflow-hidden">
        <div className="flex items-center gap-2 px-4 py-3 border-b border-border-color-light dark:border-border-color">
          <Clock className="w-4 h-4 text-gray-400" />
          <div className="text-sm font-semibold text-text-primary-light dark:text-text-primary">Recent Activity</div>
        </div>
        <div className="divide-y divide-border-color-light dark:divide-border-color">
          {activityFeed.map(a => (
            <div key={a.id} className="flex items-start gap-3 px-4 py-3">
              <div className="font-mono text-xs text-gray-400 w-16 flex-shrink-0 pt-0.5">{a.time}</div>
              <div className="flex-1 min-w-0">
                <div className="text-sm text-text-primary-light dark:text-text-primary">
                  <span className="font-medium">{a.officer}</span>
                  {' — '}
                  <span className={actTypeColor[a.type]}>{a.action}</span>
                </div>
                <div className="text-xs font-mono text-gray-400">{a.subject}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
