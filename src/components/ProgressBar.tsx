interface ProgressBarProps {
  current: number
  total: number
  percent: number
  completedCount: number
  wrongCount: number
}

export function ProgressBar({ current, total, percent, completedCount, wrongCount }: ProgressBarProps) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-sm">
        <span className="text-muted-foreground">
          第 <span className="font-medium text-foreground">{current + 1}</span> / {total} 题
        </span>
        <div className="flex items-center gap-3">
          <span className="text-green-600 dark:text-green-400">
            已完成 {completedCount}
          </span>
          {wrongCount > 0 && (
            <span className="text-red-500 dark:text-red-400">
              错题 {wrongCount}
            </span>
          )}
        </div>
      </div>
      <div className="h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  )
}
