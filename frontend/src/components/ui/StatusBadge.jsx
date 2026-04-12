export default function StatusBadge({ status, size = 'sm' }) {
  const cfg = {
    WANTED:    { bg: 'bg-red-500/15',   text: 'text-accent-red',   border: 'border-accent-red/30',   label: '⚠ WANTED' },
    WATCHLIST: { bg: 'bg-amber-500/15', text: 'text-accent-amber', border: 'border-accent-amber/30', label: '● WATCHLIST' },
    CLEARED:   { bg: 'bg-green-500/15', text: 'text-accent-green', border: 'border-accent-green/30', label: '✓ CLEARED' },
  }[status] || { bg: 'bg-gray-500/15', text: 'text-gray-400', border: 'border-gray-400/30', label: status };

  const sz = size === 'lg' ? 'px-3 py-1 text-sm' : 'px-2 py-0.5 text-[10px]';

  return (
    <span className={`inline-flex items-center rounded-full border font-mono font-bold tracking-widest ${cfg.bg} ${cfg.text} ${cfg.border} ${sz}`}>
      {cfg.label}
    </span>
  );
}
