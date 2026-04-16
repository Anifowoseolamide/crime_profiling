import { useEffect, useState, useCallback } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { api } from '../../services/api';
import { RefreshCw } from 'lucide-react';

const severityColor = { HIGH: '#FF3B3B', MEDIUM: '#F59E0B', LOW: '#3B82F6' };

export default function CrimeMap({ height = '300px', showAllLayers = false }) {
  const [hotspots, setHotspots] = useState([]);
  const [wantedSubjects, setWantedSubjects] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [hRes, wRes] = await Promise.all([
        api.getHotspots(),
        api.getWantedList()
      ]);
      setHotspots(hRes);
      setWantedSubjects(wRes.filter(s => s.coordinates?.lat && s.coordinates?.lng));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <div style={{ height }} className="rounded-xl overflow-hidden border border-border-color-light dark:border-border-color relative">
      {/* Refresh Button */}
      <button 
        onClick={fetchData}
        className={`absolute top-4 right-4 z-[1000] p-2 bg-white dark:bg-card-dark rounded-lg shadow-lg hover:bg-gray-50 dark:hover:bg-white/5 transition-all ${loading ? 'opacity-50' : ''}`}
        disabled={loading}
      >
        <RefreshCw className={`w-4 h-4 text-gray-500 ${loading ? 'animate-spin' : ''}`} />
      </button>

      <MapContainer
        center={[6.5244, 3.3792]}
        zoom={12}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={showAllLayers}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Crime Hotspots */}
        {hotspots.map((h, i) => (
          <CircleMarker
            key={`hotspot-${i}`}
            center={[h.lat, h.lng]}
            radius={h.count + 5}
            pathOptions={{
              color: severityColor[h.severity],
              fillColor: severityColor[h.severity],
              fillOpacity: 0.3,
              weight: 2
            }}
          >
            <Popup>
              <div className="text-xs font-mono p-1">
                <div className="font-bold border-b border-gray-100 pb-1 mb-1">{h.name}</div>
                <div className="flex items-center gap-2">
                  <span className="text-gray-400 uppercase text-[9px]">Severity:</span>
                  <span className="font-bold" style={{ color: severityColor[h.severity] }}>{h.severity}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-gray-400 uppercase text-[9px]">Incidents:</span>
                  <span className="font-bold">{h.count}</span>
                </div>
              </div>
            </Popup>
          </CircleMarker>
        ))}

        {/* Wanted subjects */}
        {wantedSubjects.map((s, i) => (
          <CircleMarker
            key={`wanted-${i}`}
            center={[s.coordinates.lat, s.coordinates.lng]}
            radius={8}
            pathOptions={{ color: '#FF3B3B', fillColor: '#FF3B3B', fillOpacity: 0.8 }}
          >
            <Popup>
              <div className="text-xs font-mono p-1">
                <div className="font-bold text-red-600 mb-1">{s.name}</div>
                <div className="bg-red-50 text-red-600 px-2 py-0.5 rounded text-[9px] font-bold uppercase inline-block mb-1">⚠ WANTED</div>
                <div className="text-[10px] text-gray-500">Last seen: {s.location}</div>
                {s.lastSeen && <div className="text-[9px] text-gray-400 mt-1">{new Date(s.lastSeen).toLocaleString()}</div>}
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
