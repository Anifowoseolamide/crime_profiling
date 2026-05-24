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
  const [page, setPage] = useState(1);
  const [maxPages, setMaxPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    setLoading(true);
    api.getAuditList(page).then(res => {
      setLogs(res.results || res);
      if (res.count) {
        setTotalCount(res.count);
        setMaxPages(Math.ceil(res.count / 10)); // Default DRF PAGE_SIZE = 10
      }
    }).finally(() => setLoading(false));
  }, [page]);

  // Role guard
  if (officer?.accessLevel < 2) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4 text-center animate-fade-in">
        <Shield className="w-12 h-12 text-gray-400" />
        <h2 className="text-lg font-bold text-text-primary-light dark:text-text-primary">Access Restricted</h2>
        <p className="text-sm text-gray-400">You do not have permission to view audit logs.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4 animate-fade-in flex flex-col h-[calc(100vh-6rem)]">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-bold text-text-primary-light dark:text-text-primary flex items-center gap-2">
            <ClipboardList className="w-5 h-5 text-accent-blue" />
            System Audit Log
          </h1>
          <p className="text-xs text-gray-500 font-mono">All officer activity · Role-restricted · Tamper-evident</p>
        </div>
        <a 
          href={`${import.meta.env.VITE_API_BASE_URL.replace('/api', '')}/api/audit/export/`}
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-2 text-xs font-mono text-gray-500 border border-border-color-light dark:border-border-color rounded-lg px-3 py-2 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors"
        >
          <Download className="w-3.5 h-3.5" /> Export CSV
        </a>
      </div>

      <div className="card-bg rounded-xl overflow-hidden flex flex-col flex-1">
        <div className="px-4 py-3 border-b border-border-color-light dark:border-border-color flex items-center justify-between bg-surface-light dark:bg-card-dark shrink-0">
          <span className="text-sm font-semibold text-text-primary-light dark:text-text-primary">Activity Records</span>
          <span className="text-xs font-mono text-gray-400">{totalCount || logs.length} total entries</span>
        </div>

        <div className="flex-1 overflow-auto">
          {loading ? (
            <div className="p-4 space-y-4">{[1, 2, 3, 4, 5].map(i => <SkeletonLoader key={i} lines={2} />)}</div>
          ) : logs.length === 0 ? (
            <div className="py-12 text-center text-sm text-gray-400">No audit entries found</div>
          ) : (
            <table className="w-full text-sm min-w-[800px]">
              <thead className="sticky top-0 bg-gray-50 dark:bg-surface border-b border-border-color-light dark:border-border-color">
                <tr className="text-[10px] font-mono text-gray-400 uppercase tracking-wider">
                  {['Log ID', 'Timestamp', 'Officer Badge', 'Action', 'Target', 'IP Address'].map(h => (
                    <th key={h} className="text-left px-4 py-2.5 whitespace-nowrap">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-border-color-light dark:divide-border-color">
                {logs.map(log => (
                  <tr key={log.id} className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-mono text-xs text-gray-400">{log.id.slice(0,8)}</td>
                    <td className="px-4 py-3 font-mono text-xs text-text-primary-light dark:text-text-primary whitespace-nowrap">
                      {new Date(log.timestamp).toLocaleString('en-NG')}
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-accent-blue font-bold whitespace-nowrap">
                      {log.officer ? `${log.officer.rank || ''} ${log.officer.full_name || ''}`.trim() : 'SYSTEM'}
                    </td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-300">
                        {log.action}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-gray-500 max-w-[200px] truncate" title={`${log.target_type} - ${log.target_id || ''}`}>
                      {log.target_type} {log.target_id ? `(${log.target_id.slice(0, 8)})` : ''}
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-gray-400">{log.ip_address || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Pagination Controls */}
        <div className="px-4 py-3 border-t border-border-color-light dark:border-border-color flex items-center justify-between bg-surface-light dark:bg-card-dark shrink-0">
          <button 
            disabled={page === 1 || loading} 
            onClick={() => setPage(page - 1)} 
            className="px-4 py-1.5 text-xs font-mono border border-border-color-light dark:border-border-color rounded-lg hover:bg-gray-50 dark:hover:bg-white/5 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="text-xs font-mono text-gray-500">Page {page} of {maxPages || 1}</span>
          <button 
            disabled={page >= maxPages || loading} 
            onClick={() => setPage(page + 1)} 
            className="px-4 py-1.5 text-xs font-mono border border-border-color-light dark:border-border-color rounded-lg hover:bg-gray-50 dark:hover:bg-white/5 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
