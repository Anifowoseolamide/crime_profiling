import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../services/api';
import { ArrowLeft, CheckCircle, Loader2, MapPin, Upload } from 'lucide-react';

const OFFENCE_TYPES = [
  'Armed Robbery', 'Assault', 'Fraud - Cyber', 'Fraud - Financial',
  'Drug Trafficking', 'Murder', 'Kidnapping', 'Theft', 'Vandalism', 'Other'
];

export default function LogOffence() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [stations, setStations] = useState([]);
  const [form, setForm] = useState({
    subjectId: searchParams.get('subject_id') || '', 
    type: '', date: '', location: '', notes: '', stationId: ''
  });

  useEffect(() => {
    api.getStations().then(data => {
      setStations(data.results || data);
    }).catch(console.error);
  }, []);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(null);
  const [errors, setErrors] = useState({});

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const validate = () => {
    const e = {};
    if (!form.type) e.type = 'Offence type is required';
    if (!form.stationId) e.stationId = 'Station is required';
    if (!form.date) e.date = 'Date is required';
    if (!form.location) e.location = 'Location is required';
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    try {
      const result = await api.logOffence(form);
      setSuccess(result.offenceCode);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="max-w-lg mx-auto animate-fade-in">
        <div className="card-bg rounded-2xl p-8 flex flex-col items-center gap-4 text-center">
          <div className="w-16 h-16 rounded-2xl bg-accent-green/15 flex items-center justify-center">
            <CheckCircle className="w-8 h-8 text-accent-green" />
          </div>
          <div>
            <div className="text-lg font-bold text-text-primary-light dark:text-text-primary">Offence Logged</div>
            <div className="text-xs text-gray-400 font-mono mt-1">Reference Code</div>
            <div className="text-xl font-bold font-mono text-accent-blue mt-1">{success}</div>
          </div>
          <div className="flex gap-3 w-full pt-2">
            <button onClick={() => navigate('/subjects')} className="flex-1 btn-primary py-3 text-sm">View Subjects</button>
            <button onClick={() => navigate('/dashboard')} className="flex-1 py-3 text-sm border border-border-color-light dark:border-border-color rounded-md text-gray-500 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors">Dashboard</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto space-y-4 animate-fade-in">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-text-primary-light dark:hover:text-text-primary transition-colors font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back
      </button>

      <div>
        <h1 className="text-lg font-bold text-text-primary-light dark:text-text-primary">Log Offence</h1>
        <p className="text-xs text-gray-500 font-mono">All fields marked are required. Activity is monitored.</p>
      </div>

      <form onSubmit={handleSubmit} className="card-bg rounded-2xl p-5 space-y-4">
        {/* Subject ID */}
        <div>
          <label className="form-label block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Subject ID (optional)</label>
          <input
            type="text"
            value={form.subjectId}
            onChange={e => set('subjectId', e.target.value)}
            placeholder="e.g. SUBJ-L-99821"
            className="input-field font-mono"
          />
        </div>

        {/* Offence type */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Offence Type *</label>
          <select
            value={form.type}
            onChange={e => set('type', e.target.value)}
            className={`input-field ${errors.type ? 'border-accent-red' : ''}`}
          >
            <option value="">Select type...</option>
            {OFFENCE_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          {errors.type && <p className="text-xs text-accent-red mt-1 font-mono">{errors.type}</p>}
        </div>

        {/* Police Station */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Police Station *</label>
          <select
            value={form.stationId}
            onChange={e => set('stationId', e.target.value)}
            className={`input-field ${errors.stationId ? 'border-accent-red' : ''}`}
          >
            <option value="">Select station...</option>
            {stations.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
          {errors.stationId && <p className="text-xs text-accent-red mt-1 font-mono">{errors.stationId}</p>}
        </div>

        {/* Date */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Incident Date *</label>
          <input
            type="date"
            value={form.date}
            onChange={e => set('date', e.target.value)}
            className={`input-field ${errors.date ? 'border-accent-red' : ''}`}
          />
          {errors.date && <p className="text-xs text-accent-red mt-1 font-mono">{errors.date}</p>}
        </div>

        {/* Location */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Location *</label>
          <div className="relative">
            <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={form.location}
              onChange={e => set('location', e.target.value)}
              placeholder="e.g. Oshodi Underbridge, Lagos"
              className={`input-field pl-9 ${errors.location ? 'border-accent-red' : ''}`}
            />
          </div>
          {errors.location && <p className="text-xs text-accent-red mt-1 font-mono">{errors.location}</p>}
        </div>

        {/* Notes */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Notes</label>
          <textarea
            rows={3}
            value={form.notes}
            onChange={e => set('notes', e.target.value)}
            placeholder="Describe the incident..."
            className="input-field resize-none"
          />
        </div>

        {/* Evidence upload */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Evidence (photos)</label>
          <label className="flex items-center gap-3 cursor-pointer border border-dashed border-border-color-light dark:border-border-color rounded-lg px-4 py-3 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
            <Upload className="w-4 h-4 text-gray-400" />
            <span className="text-xs text-gray-500">Click to upload evidence photos</span>
            <input type="file" multiple accept="image/*" className="hidden" />
          </label>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full btn-danger py-3 text-sm font-semibold disabled:opacity-60"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" /> Submitting...
            </span>
          ) : 'Submit Offence Report'}
        </button>
      </form>
    </div>
  );
}
