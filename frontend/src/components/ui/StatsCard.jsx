export default function StatsCard({ icon: Icon, label, value, color = 'blue', trend }) {
  const colors = {
    blue:  { bg: 'bg-accent-blue/10',  text: 'text-accent-blue',  icon: 'text-accent-blue'  },
    red:   { bg: 'bg-accent-red/10',   text: 'text-accent-red',   icon: 'text-accent-red'   },
    amber: { bg: 'bg-accent-amber/10', text: 'text-accent-amber', icon: 'text-accent-amber' },
    green: { bg: 'bg-accent-green/10', text: 'text-accent-green', icon: 'text-accent-green' },
  }[color];

  return (
    <div className="card-bg p-4 rounded-xl flex items-center gap-4 hover:shadow-md transition-shadow duration-200">
      <div className={`w-11 h-11 rounded-xl ${colors.bg} flex items-center justify-center flex-shrink-0`}>
        <Icon className={`w-5 h-5 ${colors.icon}`} />
      </div>
      <div className="min-w-0">
        <div className="text-2xl font-bold font-mono text-text-primary-light dark:text-text-primary">
          {value}
        </div>
        <div className="text-xs text-gray-500 dark:text-gray-400 truncate">{label}</div>
      </div>
      {trend && (
        <div className="ml-auto text-xs font-mono text-accent-green">
          ▲ {trend}
        </div>
      )}
    </div>
  );
}
