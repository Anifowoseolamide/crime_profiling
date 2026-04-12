const iconMap = {
  ARREST:   { symbol: '🔒', color: 'border-accent-red bg-accent-red/10 text-accent-red' },
  WARRANT:  { symbol: '⚠', color: 'border-accent-amber bg-accent-amber/10 text-accent-amber' },
  SIGHTING: { symbol: '👁', color: 'border-accent-blue bg-accent-blue/10 text-accent-blue' },
  REPORT:   { symbol: '📋', color: 'border-gray-400 bg-gray-400/10 text-gray-400' },
};

export default function Timeline({ events = [] }) {
  return (
    <div className="relative pl-4">
      {/* Vertical line */}
      <div className="absolute left-4 top-3 bottom-3 w-px bg-gray-200 dark:bg-white/10" />
      <div className="space-y-5">
        {events.map((evt, i) => {
          const cfg = iconMap[evt.type] || iconMap.REPORT;
          return (
            <div key={i} className="relative flex items-start gap-4 pl-6">
              <div className={`absolute -left-0.5 w-8 h-8 rounded-full border-2 flex items-center justify-center text-sm flex-shrink-0 ${cfg.color}`}>
                {cfg.symbol}
              </div>
              <div className="pt-0.5">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className={`text-xs font-mono font-bold ${cfg.color.split(' ').find(c => c.startsWith('text-'))}`}>
                    {evt.type}
                  </span>
                  <span className="text-xs text-gray-400 font-mono">
                    {new Date(evt.date).toLocaleDateString('en-NG', { year: 'numeric', month: 'short', day: 'numeric' })}
                  </span>
                </div>
                <p className="text-sm text-text-primary-light dark:text-text-primary mt-0.5">{evt.notes}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
