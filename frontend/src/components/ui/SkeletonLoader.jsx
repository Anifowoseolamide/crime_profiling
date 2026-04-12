export default function SkeletonLoader({ lines = 3, hasImage = false }) {
  return (
    <div className="animate-pulse space-y-3">
      {hasImage && (
        <div className="w-20 h-20 bg-gray-200 dark:bg-white/10 rounded-xl" />
      )}
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="h-4 bg-gray-200 dark:bg-white/10 rounded"
          style={{ width: `${85 - i * 15}%` }}
        />
      ))}
    </div>
  );
}
