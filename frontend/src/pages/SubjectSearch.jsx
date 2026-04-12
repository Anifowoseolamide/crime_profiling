import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import StatusBadge from '../components/ui/StatusBadge';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import { Search, Filter, UserPlus } from 'lucide-react';

const STATUS_FILTERS = ['ALL', 'WANTED', 'WATCHLIST', 'CLEARED'];

export default function SubjectSearch() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const t = setTimeout(() => {
      setLoading(true);
      api.searchSubjects(query, statusFilter).then(r => {
        setResults(r);
        setLoading(false);
      });
    }, 300);
    return () => clearTimeout(t);
  }, [query, statusFilter]);

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 className="text-lg font-bold text-text-primary-light dark:text-text-primary">Subject Registry</h1>
          <p className="text-xs text-gray-500 font-mono">NCPRS — National Criminal Profiling & Records System</p>
        </div>
        <button
          onClick={() => navigate('/records/new')}
          className="btn-primary flex items-center gap-2 text-sm"
        >
          <UserPlus className="w-4 h-4" /> New Record
        </button>
      </div>

      {/* Search + Filter */}
      <div className="card-bg rounded-xl p-4 space-y-3">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            id="subject-search"
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Search by name, ID, or alias..."
            className="input-field pl-9"
          />
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <Filter className="w-3.5 h-3.5 text-gray-400" />
          {STATUS_FILTERS.map(f => (
            <button
              key={f}
              onClick={() => setStatusFilter(f)}
              className={`px-3 py-1 rounded-full text-xs font-mono font-medium transition-all ${
                statusFilter === f
                  ? 'bg-accent-blue text-white'
                  : 'bg-gray-100 dark:bg-white/5 text-gray-500 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-white/10'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      <div className="card-bg rounded-xl overflow-hidden">
        <div className="px-4 py-3 border-b border-border-color-light dark:border-border-color flex items-center justify-between">
          <span className="text-sm font-semibold text-text-primary-light dark:text-text-primary">Results</span>
          <span className="text-xs font-mono text-gray-400">{results.length} records</span>
        </div>

        {loading ? (
          <div className="p-4 space-y-4">
            {[1, 2, 3].map(i => <SkeletonLoader key={i} hasImage lines={2} />)}
          </div>
        ) : results.length === 0 ? (
          <div className="py-12 text-center">
            <div className="text-3xl mb-2">🔍</div>
            <div className="text-sm text-gray-400">No records match your search</div>
          </div>
        ) : (
          <div className="divide-y divide-border-color-light dark:divide-border-color">
            {results.map(subj => (
              <button
                key={subj.id}
                onClick={() => navigate(`/subjects/${subj.id}`)}
                className="w-full flex items-center gap-4 px-4 py-3.5 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors text-left group"
              >
                <img
                  src={subj.mugshotUrl}
                  alt={subj.name}
                  className="w-12 h-12 rounded-xl object-cover flex-shrink-0 grayscale group-hover:grayscale-0 transition-all"
                />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-semibold text-sm text-text-primary-light dark:text-text-primary">{subj.name}</span>
                    <StatusBadge status={subj.status} />
                  </div>
                  <div className="text-xs font-mono text-gray-400 mt-0.5">{subj.id}</div>
                  <div className="text-xs text-gray-500 truncate">Last seen: {subj.location}</div>
                </div>
                <div className="text-gray-400 group-hover:text-accent-blue transition-colors text-xs font-mono hidden sm:block">
                  {new Date(subj.lastSeen).toLocaleDateString('en-NG')}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
