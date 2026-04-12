import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { api } from '../../services/api';

const severityColor = { HIGH: '#FF3B3B', MEDIUM: '#F59E0B', LOW: '#3B82F6' };

export default function CrimeMap({ height = '300px', showAllLayers = false }) {
  const [hotspots, setHotspots] = useState([]);
  const [wantedSubjects, setWantedSubjects] = useState([]);

  useEffect(() => {
    // Fetch Hotspots
    api.getHotspots()
      .then(res => setHotspots(res))
      .catch(console.error);

    // Fetch Wanted Subjects for mapping
    api.getWantedList()
      .then(res => setWantedSubjects(res.filter(s => s.coordinates?.lat && s.coordinates?.lng)))
      .catch(console.error);
  }, []);

  return (
    <div style={{ height }} className="rounded-xl overflow-hidden border border-border-color-light dark:border-border-color">
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
            radius={h.count}
            pathOptions={{
              color: severityColor[h.severity],
              fillColor: severityColor[h.severity],
              fillOpacity: 0.3,
              weight: 2
            }}
          >
            <Popup>
              <div className="text-xs font-mono">
                <div className="font-bold">{h.name}</div>
                <div>Severity: {h.severity}</div>
                <div>Incidents: {h.count}</div>
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
              <div className="text-xs font-mono">
                <div className="font-bold text-red-600">{s.name}</div>
                <div>⚠ WANTED</div>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
