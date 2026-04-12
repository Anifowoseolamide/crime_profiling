import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Shield, Eye, EyeOff, AlertCircle } from 'lucide-react';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ badgeId: '', password: '' });
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(form.badgeId, form.password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface-light dark:bg-surface flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background watermark */}
      <div className="watermark" aria-hidden="true" />

      {/* Grid overlay */}
      <div className="absolute inset-0 opacity-[0.03] dark:opacity-[0.04]"
        style={{ backgroundImage: 'linear-gradient(rgba(59,130,246,1) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,1) 1px, transparent 1px)', backgroundSize: '40px 40px' }}
      />

      <div className="relative z-10 w-full max-w-md animate-fade-in">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-accent-blue shadow-lg shadow-accent-blue/30 mb-4">
            <Shield className="w-8 h-8 text-white" />
          </div>
          <div className="text-xs font-mono text-gray-400 tracking-[0.3em] uppercase mb-1">
            Lagos State Police Command
          </div>
          <h1 className="text-2xl font-bold text-text-primary-light dark:text-text-primary">
            LagosCP Intelligence
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Restricted access — authorised personnel only
          </p>
        </div>

        {/* Card */}
        <div className="card-bg rounded-2xl p-6 shadow-xl shadow-black/10 dark:shadow-black/40">
          {/* Demo hint */}
          <div className="bg-accent-blue/10 border border-accent-blue/20 rounded-lg px-3 py-2 mb-5 text-xs font-mono text-accent-blue space-y-0.5">
            <div className="font-bold uppercase tracking-wider">Demo Credentials</div>
            <div>Field Officer: <span className="text-text-primary-light dark:text-text-primary">1024-FO</span></div>
            <div>Supervisor:    <span className="text-text-primary-light dark:text-text-primary">2048-SV</span></div>
            <div>Admin:         <span className="text-text-primary-light dark:text-text-primary">9999-AD</span></div>
            <div>Password (all): <span className="text-text-primary-light dark:text-text-primary">password123</span></div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-mono text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1.5">
                Badge Number
              </label>
              <input
                id="badge-number"
                type="text"
                value={form.badgeId}
                onChange={e => setForm(f => ({ ...f, badgeId: e.target.value }))}
                placeholder="e.g. 1024-FO"
                className="input-field font-mono"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-mono text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-1.5">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPass ? 'text' : 'password'}
                  value={form.password}
                  onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
                  placeholder="Enter password"
                  className="input-field pr-10"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPass(s => !s)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
                >
                  {showPass ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {error && (
              <div className="flex items-center gap-2 text-accent-red text-sm bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-3 text-sm font-semibold tracking-wide disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Authenticating...
                </span>
              ) : 'Authenticate'}
            </button>
          </form>
        </div>

        <div className="text-center mt-4 text-xs text-gray-400 font-mono">
          ENCRYPTED SESSION · ACTIVITY MONITORED · V2.4.1
        </div>
      </div>
    </div>
  );
}
