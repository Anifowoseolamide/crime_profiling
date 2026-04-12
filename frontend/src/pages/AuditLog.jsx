import { useEffect, useState } from 'react';
import { api } from '../services/api';
import SkeletonLoader from '../components/ui/SkeletonLoader';
import { ClipboardList, Download, Shield } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const actionColor = {
  FIELD_SCAN:   'text-accent-blue bg-accent-blue/10',
  ISSUE_WARRANT:'text-accent-red bg-accent-red/10',
  VIEW_PROFILE: 'text-gray-400 bg-gray-400/10',
  LOG_OFFENCE:  'text-accent-amber bg-accent-amber/10',
};

export default function AuditLog() {
  const { officer } = useAuth();
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getAuditLog().then(setLogs).finally(() => setLoading(false));
  }, []);

  // Role guard (also enforced in router, this is a UI-level guard)
  if (officer?.accessLevel < 2) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4 text-center">
        <Shield className="w-12 h-12 text-gray-400" />
        <h2 className="text-lg font-bold text-text-primary-light dark:text-text-primary">Access Restricted</h2>
        <p className="text-sm text-gray-400">You do not have permission to view audit logs.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-text-primary-light dark:text-text-primary flex items-center gap-2">
            <ClipboardList className="w-5 h-5 text-accent-blue" />
            System Audit Log
          </h1>
          <p className="text-xs text-gray-500 font-mono">All officer activity · Role-restricted · Tamper-evident</p>
        </div>
        <button className="flex items-center gap-2 text-xs font-mono text-gray-500 border border-border-color-light dark:border-border-color rounded-lg px-3 py-2 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors">
          <Download className="w-3.5 h-3.5" /> Export CSV
        </button>
      </div>

      <div className="card-bg rounded-xl overflow-hidden">
        <div className="px-4 py-3 border-b border-border-color-light dark:border-border-color flex items-center justify-between">
          <span className="text-sm font-semibold text-text-primary-light dark:text-text-primary">Activity Records</span>
          <span className="text-xs font-mono text-gray-400">{logs.length} entries</span>
        </div>

        {loading ? (
          <div className="p-4 space-y-4">{[1, 2, 3].map(i => <SkeletonLoader key={i} lines={2} />)}</div>
        ) : logs.length === 0 ? (
          <div className="py-12 text-center text-sm text-gray-400">No audit entries found</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm min-w-[600px]">
              <thead>
                <tr className="bg-gray-50 dark:bg-white/5 text-[10px] font-mono text-gray-400 uppercase tracking-wider">
                  {['Log ID', 'Timestamp', 'Officer Badge', 'Action', 'Subject', 'IP Address'].map(h => (
                    <th key={h} className="text-left px-4 py-2.5">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-border-color-light dark:divide-border-color">
                {logs.map(log => (
                  <tr key={log.id} className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-mono text-xs text-gray-400">{log.id}</td>
                    <td className="px-4 py-3 font-mono text-xs text-text-primary-light dark:text-text-primary">
                      {new Date(log.timestamp).toLocaleString('en-NG')}
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-accent-blue">{log.officer}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold ${actionColor[log.action] || 'text-gray-400 bg-gray-400/10'}`}>
                        {log.action}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-gray-500">{log.subject}</td>
                    <td className="px-4 py-3 font-mono text-xs text-gray-400">{log.ip}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
