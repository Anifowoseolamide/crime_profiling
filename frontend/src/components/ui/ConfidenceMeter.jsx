export default function ConfidenceMeter({ score }) {
  const color =
    score >= 90 ? 'bg-accent-green'
    : score >= 70 ? 'bg-accent-amber'
    : 'bg-accent-red';

  const label =
    score >= 90 ? 'HIGH CONFIDENCE'
    : score >= 70 ? 'MODERATE CONFIDENCE'
    : 'LOW CONFIDENCE — VERIFY';

  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs font-mono">
        <span className="text-gray-400">{label}</span>
        <span className="font-bold text-text-primary-light dark:text-text-primary">{score}%</span>
      </div>
      <div className="w-full h-1.5 bg-gray-200 dark:bg-white/10 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}
