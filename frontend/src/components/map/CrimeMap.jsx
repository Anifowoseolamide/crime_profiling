import { useEffect, useState, useCallback, useRef } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { api } from '../../services/api';
import { RefreshCw } from 'lucide-react';

const severityColor = { HIGH: '#FF3B3B', MEDIUM: '#F59E0B', LOW: '#3B82F6' };

// Inner component that auto-fits the map when data changes
function AutoFit({ markers }) {
  const map = useMap();
  const fitted = useRef(false);
  useEffect(() => {
    if (!fitted.current && markers.length > 0) {
      const bounds = markers.map(m => [m.lat, m.lng]);
      try { map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 }); } catch (_) {}
      fitted.current = true;
    }
  }, [markers, map]);
  return null;
}

export default function CrimeMap({
  height = '300px',
  showAllLayers = false,
  filters = { wanted: true, highRisk: true, monitored: true, hotspots: true },
  onCountsChange
}) {
  const [hotspots, setHotspots] = useState([]);
  const [wantedSubjects, setWantedSubjects] = useState([]);
  const [otherSubjects, setOtherSubjects] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      // Fetch warrants list + ALL subjects in parallel
      const [hRes, wRes, allRes] = await Promise.all([
        api.getHotspots(),
        // Pull subjects directly by WANTED status — catches scan-flagged without formal warrant
        api.searchSubjects('', 'WANTED'),
        api.searchSubjects()
      ]);

      setHotspots(Array.isArray(hRes) ? hRes : []);

      const seenCoords = new Set();
      const enforceSeparation = (s) => {
        if (!s.coordinates?.lat) return s;
        let { lat, lng } = s.coordinates;
        let key = `${lat.toFixed(4)},${lng.toFixed(4)}`;
        let attempts = 0;
        // If coordinate exists near here, shift it out slightly (~30 meters)
        while (seenCoords.has(key) && attempts < 10) {
          attempts++;
          lat += (Math.random() - 0.5) * 0.0006;
          lng += (Math.random() - 0.5) * 0.0006;
          key = `${lat.toFixed(4)},${lng.toFixed(4)}`;
        }
        seenCoords.add(key);
        return { ...s, coordinates: { lat, lng } };
      };

      const wantedWithCoords = wRes
        .filter(s => s.coordinates?.lat && s.coordinates?.lng)
        .map(enforceSeparation);
        
      const wantedIds = new Set(wRes.map(s => s.id));

      const others = allRes
        .filter(s => !wantedIds.has(s.id) && s.coordinates?.lat && s.coordinates?.lng)
        .map(enforceSeparation);

      setWantedSubjects(wantedWithCoords);
      setOtherSubjects(others);

      // Report counts up to parent
      if (onCountsChange) {
        const highRiskCount = others.filter(s => s.risk_level === 'HIGH' || s.risk_level === 'EXTREME').length;
        const monitoredCount = others.filter(s => s.risk_level !== 'HIGH' && s.risk_level !== 'EXTREME').length;
        onCountsChange({
          wanted: wantedWithCoords.length,
          highRisk: highRiskCount,
          monitored: monitoredCount,
        });
      }
    } catch (err) {
      console.error('Map fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [onCountsChange]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Build flat list of all visible coords for AutoFit
  const allMarkers = [
    ...wantedSubjects.map(s => ({ lat: s.coordinates.lat, lng: s.coordinates.lng })),
    ...otherSubjects.map(s => ({ lat: s.coordinates.lat, lng: s.coordinates.lng })),
  ];

  return (
    <div style={{ height }} className="rounded-xl overflow-hidden border border-border-color-light dark:border-border-color relative">
      {/* Refresh Button */}
      <button
        onClick={fetchData}
        title="Refresh map data"
        className={`absolute top-4 right-4 z-[1000] p-2 bg-white dark:bg-card-dark rounded-lg shadow-lg hover:bg-gray-50 dark:hover:bg-white/5 transition-all ${loading ? 'opacity-50' : ''}`}
        disabled={loading}
      >
        <RefreshCw className={`w-4 h-4 text-gray-500 ${loading ? 'animate-spin' : ''}`} />
      </button>

      <MapContainer
        center={[6.5244, 3.3792]}
        zoom={12}
        maxZoom={19}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={showAllLayers}
      >
        <TileLayer
          attribution='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012'
          url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"
          maxZoom={19}
        />

        {/* Auto-fit map to markers on first load */}
        {allMarkers.length > 0 && <AutoFit markers={allMarkers} />}

        {/* Crime Hotspots */}
        {filters.hotspots && hotspots.map((h, i) => (
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
        {filters.wanted && wantedSubjects.map((s, i) => (
          <CircleMarker
            key={`wanted-${s.id || i}`}
            center={[s.coordinates.lat, s.coordinates.lng]}
            radius={9}
            pathOptions={{ color: '#FF3B3B', fillColor: '#FF3B3B', fillOpacity: 0.85, weight: 2 }}
          >
            <Popup>
              <div className="text-xs font-mono p-1">
                <div className="font-bold text-red-600 mb-1">{s.name}</div>
                <div className="bg-red-50 text-red-600 px-2 py-0.5 rounded text-[9px] font-bold uppercase inline-block mb-1">⚠ WANTED</div>
                <div className="text-[10px] text-gray-500">Last seen: {s.location || '—'}</div>
                {s.lastSeen && <div className="text-[9px] text-gray-400 mt-1">{new Date(s.lastSeen).toLocaleString()}</div>}
              </div>
            </Popup>
          </CircleMarker>
        ))}

        {/* High Risk & Monitored subjects */}
        {otherSubjects.map((s, i) => {
          const isHighRisk = s.risk_level === 'HIGH' || s.risk_level === 'EXTREME';
          if (isHighRisk && !filters.highRisk) return null;
          if (!isHighRisk && !filters.monitored) return null;

          const color = isHighRisk ? '#F59E0B' : '#3B82F6';
          const label = isHighRisk ? 'HIGH RISK' : 'MONITORED';
          const badgeClass = isHighRisk ? 'bg-amber-50 text-amber-600' : 'bg-blue-50 text-blue-600';

          return (
            <CircleMarker
              key={`other-${s.id || i}`}
              center={[s.coordinates.lat, s.coordinates.lng]}
              radius={8}
              pathOptions={{ color, fillColor: color, fillOpacity: 0.8, weight: 2 }}
            >
              <Popup>
                <div className="text-xs font-mono p-1">
                  <div className="font-bold mb-1" style={{ color }}>{s.name}</div>
                  <div className={`${badgeClass} px-2 py-0.5 rounded text-[9px] font-bold uppercase inline-block mb-1`}>{label}</div>
                  <div className="text-[10px] text-gray-500">Last seen: {s.location || '—'}</div>
                  {s.lastSeen && <div className="text-[9px] text-gray-400 mt-1">{new Date(s.lastSeen).toLocaleString()}</div>}
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
}
