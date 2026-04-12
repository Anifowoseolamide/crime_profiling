import CrimeMap from '../components/map/CrimeMap';
import { MapPin, Layers } from 'lucide-react';

export default function GeoMap() {
  return (
    <div className="space-y-4 animate-fade-in h-full flex flex-col">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-text-primary-light dark:text-text-primary flex items-center gap-2">
            <MapPin className="w-5 h-5 text-accent-blue" />
            Geo-Intelligence Map
          </h1>
          <p className="text-xs text-gray-500 font-mono">Real-time crime hotspot & sighting overlay · Lagos State</p>
        </div>
        <div className="hidden sm:flex items-center gap-3 text-xs font-mono">
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-accent-red inline-block" />Wanted</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-accent-amber inline-block" />High Risk</span>
          <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-full bg-accent-blue inline-block" />Monitored</span>
        </div>
      </div>
      <div className="flex-1" style={{ minHeight: '500px' }}>
        <CrimeMap height="100%" showAllLayers />
      </div>
    </div>
  );
}
