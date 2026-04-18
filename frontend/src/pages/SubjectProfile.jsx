import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import StatusBadge from '../components/ui/StatusBadge';
import ConfidenceMeter from '../components/ui/ConfidenceMeter';
import Timeline from '../components/ui/Timeline';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import { ArrowLeft, MapPin, FileText, Camera, AlertTriangle } from 'lucide-react';

const TABS = ['Overview', 'Timeline', 'Offences', 'Mugshots'];

export default function SubjectProfile() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [subject, setSubject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [tab, setTab] = useState('Overview');
  const [updatingRisk, setUpdatingRisk] = useState(false);

  useEffect(() => {
    setLoading(true);
    api.getSubject(id)
      .then(setSubject)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return (
    <div className="space-y-4 animate-fade-in">
      <SkeletonLoader hasImage lines={3} />
      <SkeletonLoader lines={4} />
    </div>
  );

  if (error) return (
    <div className="card-bg rounded-xl p-8 text-center space-y-2">
      <div className="text-3xl">⚠️</div>
      <div className="text-sm text-accent-red font-mono">{error}</div>
      <button onClick={() => navigate(-1)} className="text-xs text-accent-blue hover:underline">Go back</button>
    </div>
  );

  if (!subject) return null;

  const borderMap = { WANTED: 'border-accent-red', WATCHLIST: 'border-accent-amber', CLEARED: 'border-accent-green' };
  const canEditRisk = user?.accessLevel >= 2;

  const handleUpdateRisk = async (newRisk) => {
    try {
      setUpdatingRisk(true);
      await api.updateSubject(id, { risk_level: newRisk });
      setSubject(prev => ({ ...prev, risk_level: newRisk }));
    } catch(err) {
      alert("Failed to update risk level: " + err.message);
    } finally {
      setUpdatingRisk(false);
    }
  };

  return (
    <div className="space-y-4 animate-fade-in">
      {/* Back btn */}
      <button onClick={() => navigate(-1)} className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-text-primary-light dark:hover:text-text-primary transition-colors font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back
      </button>

      {/* Header card */}
      <div className="card-bg rounded-2xl p-5 space-y-4">
        <div className="flex items-start gap-4 flex-wrap">
          <div className="relative flex-shrink-0">
            <img
              src={subject.mugshotUrl}
              alt={subject.name}
              className={`w-24 h-24 rounded-xl object-cover border-3 ${borderMap[subject.status] || 'border-gray-400'} grayscale`}
              style={{ borderWidth: '3px' }}
            />
            {subject.status === 'WANTED' && (
              <div className="absolute -top-1.5 -right-1.5 bg-accent-red rounded-full p-1">
                <AlertTriangle className="w-3 h-3 text-white" />
              </div>
            )}
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-xs font-mono text-gray-400 mb-0.5">{subject.id}</div>
            <h1 className="text-xl font-bold text-text-primary-light dark:text-text-primary">{subject.name}</h1>
            <div className="text-xs text-gray-500 mb-2">AKA: {subject.aliases?.join(', ') || 'None'}</div>
            <StatusBadge status={subject.status} size="lg" />
          </div>
        </div>

        {subject.confidence && (
          <ConfidenceMeter score={subject.confidence} />
        )}

        {/* Actions */}
        <div className="flex flex-wrap gap-2 pt-1">
          <button onClick={() => navigate('/field-scan')} className="btn-primary flex items-center gap-1.5 text-sm py-2">
            <Camera className="w-3.5 h-3.5" /> New Scan
          </button>
          <button onClick={() => navigate(`/offences/new?subject_id=${id}`)} className="btn-danger flex items-center gap-1.5 text-sm py-2">
            <FileText className="w-3.5 h-3.5" /> Log Offence
          </button>
          {subject.status !== 'WANTED' && (
            <button onClick={() => navigate(`/wanted/new?subject_id=${id}`)} className="btn-secondary flex items-center gap-1.5 text-sm py-2 text-accent-red border-accent-red/30 hover:bg-accent-red/10">
              <AlertTriangle className="w-3.5 h-3.5" /> Declare Wanted
            </button>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-border-color-light dark:border-border-color">
        {TABS.map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2.5 text-sm font-medium transition-all relative ${
              tab === t
                ? 'text-accent-blue'
                : 'text-gray-500 dark:text-gray-400 hover:text-text-primary-light dark:hover:text-text-primary'
            }`}
          >
            {t}
            {tab === t && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-accent-blue rounded-t-full" />}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {tab === 'Overview' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="card-bg rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-mono font-bold text-gray-400 uppercase tracking-widest">Personal Details</div>
              {canEditRisk && subject.status !== 'WANTED' && (
                <div className="flex items-center gap-2">
                  {updatingRisk && <div className="text-[10px] text-gray-400 animate-pulse">Updating...</div>}
                  <select 
                    value={subject.risk_level || 'LOW'}
                    onChange={(e) => handleUpdateRisk(e.target.value)}
                    disabled={updatingRisk}
                    className="text-[10px] font-mono border border-border-color-light dark:border-border-color rounded bg-transparent p-1 text-gray-500 focus:outline-none focus:ring-1 focus:ring-accent-blue"
                  >
                    <option value="LOW">Set Risk: LOW</option>
                    <option value="MEDIUM">Set Risk: MEDIUM</option>
                    <option value="HIGH">Set Risk: HIGH</option>
                    <option value="EXTREME">Set Risk: EXTREME</option>
                  </select>
                </div>
              )}
            </div>
            {[
              { label: 'Full Name', value: subject.name },
              { label: 'Aliases', value: subject.aliases?.join(', ') || '—' },
              { label: 'Status', value: subject.status },
              { label: 'Risk Level', value: subject.risk_level || 'LOW' },
              { label: 'Last Known Location', value: subject.location },
            ].map(({ label, value }) => (
              <div key={label}>
                <div className="text-[10px] font-mono text-gray-400 uppercase tracking-wider">{label}</div>
                <div className="text-sm text-text-primary-light dark:text-text-primary font-medium">{value}</div>
              </div>
            ))}
          </div>
          {subject.warrantDetails && (
            <div className="card-bg rounded-xl p-4 space-y-3 border border-accent-red/20">
              <div className="text-xs font-mono font-bold text-accent-red uppercase tracking-widest flex items-center gap-2">
                <AlertTriangle className="w-3.5 h-3.5" /> Active Warrant
              </div>
              {[
                { label: 'Reason', value: subject.warrantDetails.reason },
                { label: 'Issued By', value: subject.warrantDetails.issuedBy },
                { label: 'Issue Date', value: subject.warrantDetails.date },
              ].map(({ label, value }) => (
                <div key={label}>
                  <div className="text-[10px] font-mono text-gray-400 uppercase tracking-wider">{label}</div>
                  <div className="text-sm text-text-primary-light dark:text-text-primary font-medium">{value}</div>
                </div>
              ))}
            </div>
          )}
          <div className="card-bg rounded-xl p-4 col-span-full">
            <div className="flex items-center gap-2 text-xs font-mono font-bold text-gray-400 uppercase tracking-widest mb-2">
              <MapPin className="w-3.5 h-3.5" /> Last Known Location
            </div>
            <div className="text-sm text-text-primary-light dark:text-text-primary">{subject.location}</div>
            <div className="text-xs font-mono text-gray-400">
              {subject.coordinates?.lat.toFixed(4)}, {subject.coordinates?.lng.toFixed(4)}
            </div>
          </div>
        </div>
      )}

      {tab === 'Timeline' && (
        <div className="card-bg rounded-xl p-5">
          <Timeline events={subject.timeline || []} />
          {(!subject.timeline || subject.timeline.length === 0) && (
            <div className="text-sm text-gray-400 text-center py-4">No timeline events recorded</div>
          )}
        </div>
      )}

      {tab === 'Offences' && (
        <div className="card-bg rounded-xl overflow-hidden">
          <div className="px-4 py-3 border-b border-border-color-light dark:border-border-color flex items-center justify-between">
            <span className="text-sm font-semibold text-text-primary-light dark:text-text-primary">Offence History</span>
            <span className="text-xs font-mono text-gray-400">{subject.offences?.length || 0} records</span>
          </div>
          {subject.offences?.length === 0 ? (
            <div className="py-8 text-center text-sm text-gray-400">No offences on record</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 dark:bg-white/5 text-[10px] font-mono text-gray-400 uppercase tracking-wider">
                    {['Code', 'Type', 'Date', 'Location', 'Officer'].map(h => (
                      <th key={h} className="text-left px-4 py-2.5">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-color-light dark:divide-border-color">
                  {subject.offences?.map(o => (
                    <tr key={o.code} className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                      <td className="px-4 py-3 font-mono text-xs text-accent-blue">{o.code}</td>
                      <td className="px-4 py-3 font-medium text-text-primary-light dark:text-text-primary">{o.type}</td>
                      <td className="px-4 py-3 text-xs text-gray-500 font-mono">{new Date(o.date).toLocaleDateString('en-NG')}</td>
                      <td className="px-4 py-3 text-xs text-gray-500">{o.location}</td>
                      <td className="px-4 py-3 text-xs text-gray-500">{o.officer}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {tab === 'Mugshots' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {subject.mugshots?.map((m, i) => (
            <div key={m.id} className="card-bg rounded-xl overflow-hidden flex flex-col">
              <img src={m.image_url} alt={`Mugshot ${i+1}`} className="w-full h-48 object-cover grayscale" />
              <div className="p-4 space-y-2">
                <div className="flex justify-between items-start">
                  <div className="text-[10px] font-mono text-gray-500 uppercase tracking-widest">
                    {m.is_primary ? 'Primary Mugshot' : `Variant ${i+1}`}
                  </div>
                  <div className="text-[10px] font-mono text-gray-400">
                    {new Date(m.capture_date).toLocaleDateString()}
                  </div>
                </div>
                {m.latitude && m.longitude ? (
                  <div className="pt-2 border-t border-border-color-light dark:border-border-color">
                    <div className="flex items-center gap-1.5 text-xs text-accent-blue font-medium">
                      <MapPin className="w-3.5 h-3.5" /> Captured Location
                    </div>
                    <a 
                      href={`https://www.google.com/maps?q=${m.latitude},${m.longitude}`} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-[11px] font-mono text-gray-500 hover:text-accent-blue transition-colors mt-0.5 block"
                    >
                      {m.latitude.toFixed(4)}, {m.longitude.toFixed(4)} (Open in Maps)
                    </a>
                  </div>
                ) : (
                  <div className="text-[11px] text-gray-400 italic">No location data captured</div>
                )}
              </div>
            </div>
          ))}
          {(!subject.mugshots || subject.mugshots.length === 0) && (
            <div className="col-span-full py-12 text-center text-sm text-gray-400 card-bg rounded-xl">
              No mugshots found for this subject
            </div>
          )}
        </div>
      )}
    </div>
  );
}
