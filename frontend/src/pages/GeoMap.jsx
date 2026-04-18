import { useState, useCallback } from 'react';
import CrimeMap from '../components/map/CrimeMap';
import { MapPin, Layers } from 'lucide-react';

export default function GeoMap() {
  const [filters, setFilters] = useState({
    wanted: true,
    highRisk: true,
    monitored: true,
    hotspots: true
  });

  const [counts, setCounts] = useState({ wanted: 0, highRisk: 0, monitored: 0 });

  const toggle = (key) => setFilters(f => ({ ...f, [key]: !f[key] }));

  const handleCountsChange = useCallback((newCounts) => {
    setCounts(newCounts);
  }, []);

  const Badge = ({ count, active }) => (
    <span className={`ml-1 text-[10px] font-bold rounded-full px-1.5 py-0.5 min-w-[18px] text-center inline-block transition-colors ${
      active
        ? 'bg-current/20 text-current'
        : 'bg-gray-200 dark:bg-gray-700 text-gray-400'
    }`}>
      {count}
    </span>
  );

  return (
    <div className="space-y-4 animate-fade-in h-full flex flex-col">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-lg font-bold text-text-primary-light dark:text-text-primary flex items-center gap-2">
            <MapPin className="w-5 h-5 text-accent-blue" />
            Geo-Intelligence Map
          </h1>
          <p className="text-xs text-gray-500 font-mono">Real-time crime hotspot &amp; sighting overlay · Lagos State</p>
        </div>

        {/* Filter buttons with live counts */}
        <div className="flex items-center gap-2 text-xs font-mono flex-wrap">
          {/* Wanted */}
          <button
            onClick={() => toggle('wanted')}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg transition-all border font-semibold ${
              filters.wanted
                ? 'bg-accent-red/10 border-accent-red/30 text-accent-red'
                : 'border-transparent text-gray-400 hover:text-gray-500 dark:hover:text-gray-300'
            }`}
          >
            <span className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${filters.wanted ? 'bg-accent-red' : 'bg-gray-400'}`} />
            Wanted
            <Badge count={counts.wanted} active={filters.wanted} />
          </button>

          {/* High Risk */}
          <button
            onClick={() => toggle('highRisk')}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg transition-all border font-semibold ${
              filters.highRisk
                ? 'bg-accent-amber/10 border-accent-amber/30 text-accent-amber'
                : 'border-transparent text-gray-400 hover:text-gray-500 dark:hover:text-gray-300'
            }`}
          >
            <span className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${filters.highRisk ? 'bg-accent-amber' : 'bg-gray-400'}`} />
            High Risk
            <Badge count={counts.highRisk} active={filters.highRisk} />
          </button>

          {/* Monitored */}
          <button
            onClick={() => toggle('monitored')}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg transition-all border font-semibold ${
              filters.monitored
                ? 'bg-accent-blue/10 border-accent-blue/30 text-accent-blue'
                : 'border-transparent text-gray-400 hover:text-gray-500 dark:hover:text-gray-300'
            }`}
          >
            <span className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${filters.monitored ? 'bg-accent-blue' : 'bg-gray-400'}`} />
            Monitored
            <Badge count={counts.monitored} active={filters.monitored} />
          </button>

          {/* Hotspots */}
          <button
            onClick={() => toggle('hotspots')}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg transition-all border font-semibold ${
              filters.hotspots
                ? 'bg-gray-100 border-gray-300 dark:bg-gray-800 dark:border-gray-600 text-gray-600 dark:text-gray-300'
                : 'border-transparent text-gray-400 hover:text-gray-500 dark:hover:text-gray-300'
            }`}
          >
            <Layers className={`w-3 h-3 flex-shrink-0 ${filters.hotspots ? '' : 'opacity-50'}`} />
            Hotspots
          </button>
        </div>
      </div>

      <div className="flex-1" style={{ minHeight: '500px' }}>
        <CrimeMap
          height="100%"
          showAllLayers
          filters={filters}
          onCountsChange={handleCountsChange}
        />
      </div>
    </div>
  );
}
