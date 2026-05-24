import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../services/api';
import { ArrowLeft, CheckCircle, Loader2, AlertTriangle, ShieldAlert } from 'lucide-react';

export default function DeclareWanted() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errors, setErrors] = useState({});
  const [form, setForm] = useState({
    subjectId: searchParams.get('subject_id') || '',
    warrantNumber: `WR-${Math.floor(10000 + Math.random() * 90000)}`,
    issuingAuthority: 'Lagos State Police Command',
    reason: '',
    priority: 'ROUTINE',
    expiryDate: ''
  });

  const set = (field, val) => {
    setForm(prev => ({ ...prev, [field]: val }));
    if (errors[field]) setErrors(prev => {
      const { [field]: _, ...rest } = prev;
      return rest;
    });
  };

  const validate = () => {
    const e = {};
    if (!form.subjectId) e.subjectId = 'Subject ID is required';
    if (!form.warrantNumber) e.warrantNumber = 'Warrant Number is required';
    if (!form.reason) e.reason = 'Reason for warrant is required';
    if (!form.priority) e.priority = 'Priority is required';
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    
    setLoading(true);
    try {
      await api.declareWanted(form);
      setSuccess(true);
      setTimeout(() => navigate(`/subjects/${form.subjectId}`), 2000);
    } catch (err) {
      setErrors({ submit: err.message });
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4 animate-fade-in text-center">
        <div className="bg-accent-red/10 p-6 rounded-full">
          <ShieldAlert className="w-16 h-16 text-accent-red animate-pulse" />
        </div>
        <h2 className="text-2xl font-bold text-text-primary-light dark:text-text-primary">Warrant Issued Successfully</h2>
        <p className="text-gray-500 max-w-sm">The subject has been flagged as WANTED across the state profiling system.</p>
        <div className="text-xs font-mono text-gray-400">Redirecting to profile...</div>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto space-y-6 animate-fade-in px-4">
      <button onClick={() => navigate(-1)} className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-text-primary-light dark:hover:text-text-primary transition-colors font-mono">
        <ArrowLeft className="w-3.5 h-3.5" /> Back
      </button>

      <div className="space-y-1">
        <h1 className="text-2xl font-bold text-text-primary-light dark:text-text-primary flex items-center gap-2">
          <AlertTriangle className="text-accent-red w-6 h-6" /> Issue Warrant
        </h1>
        <p className="text-sm text-gray-500 font-mono">Declare Subject as Wanted / At Large</p>
      </div>

      <form onSubmit={handleSubmit} className="card-bg rounded-2xl p-6 space-y-5 border border-accent-red/20 shadow-xl shadow-accent-red/5">
        
        {/* Subject ID */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Subject Index (UUID) *</label>
          <input
            type="text"
            value={form.subjectId}
            onChange={e => set('subjectId', e.target.value)}
            className={`input-field font-mono text-sm ${errors.subjectId ? 'border-accent-red' : ''}`}
            placeholder="00000000-0000-0000-0000-000000000000"
          />
          {errors.subjectId && <p className="text-xs text-accent-red mt-1 font-mono">{errors.subjectId}</p>}
        </div>

        <div className="grid grid-cols-2 gap-4">
          {/* Warrant Number */}
          <div>
            <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Warrant # *</label>
            <input
              type="text"
              value={form.warrantNumber}
              onChange={e => set('warrantNumber', e.target.value)}
              className="input-field font-mono text-sm"
            />
          </div>

          {/* Priority */}
          <div>
            <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Priority Level *</label>
            <select
              value={form.priority}
              onChange={e => set('priority', e.target.value)}
              className="input-field"
            >
              <option value="ROUTINE">ROUTINE</option>
              <option value="URGENT">URGENT</option>
              <option value="CRITICAL">CRITICAL</option>
            </select>
          </div>
        </div>

        {/* Issuing Authority */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Issuing Authority *</label>
          <input
            type="text"
            value={form.issuingAuthority}
            onChange={e => set('issuingAuthority', e.target.value)}
            className="input-field"
          />
        </div>

        {/* Reason */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Basis for Warrant *</label>
          <textarea
            value={form.reason}
            onChange={e => set('reason', e.target.value)}
            className={`input-field min-h-[100px] py-3 ${errors.reason ? 'border-accent-red' : ''}`}
            placeholder="e.g. Absconded from custody during trial for Armed Robbery..."
          ></textarea>
          {errors.reason && <p className="text-xs text-accent-red mt-1 font-mono">{errors.reason}</p>}
        </div>

        {/* Expiry */}
        <div>
          <label className="block text-xs font-mono text-gray-500 uppercase tracking-wider mb-1.5">Expiry Date (Optional)</label>
          <input
            type="date"
            value={form.expiryDate}
            onChange={e => set('expiryDate', e.target.value)}
            className="input-field"
          />
        </div>

        {errors.submit && (
          <div className="bg-accent-red/10 border border-accent-red/20 rounded-lg p-3 text-xs text-accent-red font-mono">
            {errors.submit}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="btn-danger w-full py-4 rounded-xl font-bold flex items-center justify-center gap-2 mt-4 shadow-lg shadow-accent-red/20"
        >
          {loading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <>
              <ShieldAlert className="w-5 h-5" /> ISSUE STATE-WIDE WARRANT
            </>
          )}
        </button>
      </form>
    </div>
  );
}
