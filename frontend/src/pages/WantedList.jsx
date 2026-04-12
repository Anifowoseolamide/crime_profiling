import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import StatusBadge from '../components/ui/StatusBadge';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import { AlertTriangle, ChevronRight, RefreshCw } from 'lucide-react';

const priorityClasses = {
  CRITICAL: 'border-l-accent-red shadow-red-500/10 shadow-lg bg-red-50 dark:bg-red-950/20',
  HIGH:     'border-l-accent-amber',
  MEDIUM:   'border-l-accent-blue',
};
const priorityBadge = {
  CRITICAL: 'bg-accent-red/15 text-accent-red border-accent-red/30',
  HIGH:     'bg-accent-amber/15 text-accent-amber border-accent-amber/30',
  MEDIUM:   'bg-accent-blue/15 text-accent-blue border-accent-blue/30',
};

export default function WantedList() {
  const navigate = useNavigate();
  const [wanted, setWanted] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = async () => {
    const data = await api.getWantedList();
    setWanted(data);
    setLoading(false);
    setRefreshing(false);
  };

  useEffect(() => { load(); }, []);

  const handleRefresh = () => {
    setRefreshing(true);
    load();
  };

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-text-primary-light dark:text-text-primary flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-accent-red" />
            Wanted List
          </h1>
          <p className="text-xs text-gray-500 font-mono">Active warrants — Lagos State</p>
        </div>
        <button
          onClick={handleRefresh}
          className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors"
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-3">
        {Object.entries(priorityBadge).map(([p, cls]) => (
          <span key={p} className={`px-3 py-1 rounded-full text-xs font-mono font-bold border ${cls}`}>
            {p}
          </span>
        ))}
      </div>

      {/* List */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="card-bg rounded-xl p-4"><SkeletonLoader hasImage lines={2} /></div>
          ))}
        </div>
      ) : wanted.length === 0 ? (
        <div className="card-bg rounded-xl py-16 text-center text-gray-400">
          <div className="text-3xl mb-2">✅</div>
          <div className="text-sm">No active warrants at this time</div>
        </div>
      ) : (
        <div className="space-y-3">
          {wanted.map(s => (
            <button
              key={s.id}
              onClick={() => navigate(`/subjects/${s.id}`)}
              className={`w-full card-bg rounded-xl p-4 flex items-center gap-4 border-l-4 text-left transition-all hover:shadow-md ${priorityClasses[s.priority] || ''}`}
            >
              <div className="relative flex-shrink-0">
                <img src={s.mugshotUrl} alt={s.name} className="w-14 h-14 rounded-xl object-cover grayscale" />
                {s.priority === 'CRITICAL' && (
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-accent-red rounded-full flex items-center justify-center">
                    <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                  </div>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap mb-1">
                  <span className="font-bold text-text-primary-light dark:text-text-primary">{s.name}</span>
                  <StatusBadge status={s.status} />
                  {s.priority && (
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold border ${priorityBadge[s.priority]}`}>
                      {s.priority}
                    </span>
                  )}
                </div>
                <div className="text-xs font-mono text-gray-400">{s.id}</div>
                <div className="text-xs text-gray-500">{s.warrantDetails?.reason}</div>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-400 flex-shrink-0" />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
