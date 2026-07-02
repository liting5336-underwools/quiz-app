interface FinishedScreenProps {
  totalQuestions: number
  completedCount: number
  wrongCount: number
  onReviewWrong: () => void
  onReset: () => void
}

export function FinishedScreen({
  totalQuestions,
  completedCount,
  wrongCount,
  onReviewWrong,
  onReset,
}: FinishedScreenProps) {
  const correctCount = completedCount - wrongCount
  const score = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0

  const getGradeInfo = () => {
    if (score >= 90) return { emoji: '🌟', text: '优秀！', color: 'text-green-600 dark:text-green-400' }
    if (score >= 70) return { emoji: '👍', text: '良好！', color: 'text-blue-600 dark:text-blue-400' }
    if (score >= 60) return { emoji: '💪', text: '及格！', color: 'text-amber-600 dark:text-amber-400' }
    return { emoji: '📚', text: '继续加油！', color: 'text-red-600 dark:text-red-400' }
  }

  const grade = getGradeInfo()

  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 p-8 max-w-md w-full text-center">
        <div className="text-6xl mb-4">{grade.emoji}</div>
        <h2 className="text-2xl font-bold mb-1">刷题完成！</h2>
        <p className={`text-lg font-medium mb-6 ${grade.color}`}>{grade.text}</p>

        {/* Score Circle */}
        <div className="relative w-32 h-32 mx-auto mb-6">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50" cy="50" r="42"
              fill="none"
              stroke="currentColor"
              strokeWidth="8"
              className="text-slate-100 dark:text-slate-700"
            />
            <circle
              cx="50" cy="50" r="42"
              fill="none"
              stroke="currentColor"
              strokeWidth="8"
              strokeDasharray={`${2 * Math.PI * 42}`}
              strokeDashoffset={`${2 * Math.PI * 42 * (1 - score / 100)}`}
              strokeLinecap="round"
              className="text-indigo-500 dark:text-indigo-400 transition-all duration-1000"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-3xl font-bold text-foreground">{score}</span>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-green-50 dark:bg-green-900/20 rounded-xl p-3">
            <div className="text-xl font-bold text-green-600 dark:text-green-400">{correctCount}</div>
            <div className="text-xs text-green-600/70 dark:text-green-400/70">正确</div>
          </div>
          <div className="bg-red-50 dark:bg-red-900/20 rounded-xl p-3">
            <div className="text-xl font-bold text-red-500 dark:text-red-400">{wrongCount}</div>
            <div className="text-xs text-red-500/70 dark:text-red-400/70">错误</div>
          </div>
          <div className="bg-slate-50 dark:bg-slate-700/50 rounded-xl p-3">
            <div className="text-xl font-bold text-foreground">{totalQuestions}</div>
            <div className="text-xs text-muted-foreground">总题数</div>
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          {wrongCount > 0 && (
            <button
              onClick={onReviewWrong}
              className="w-full py-3 px-4 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-medium hover:from-amber-600 hover:to-orange-600 transition-all shadow-lg shadow-amber-200 dark:shadow-amber-900/30"
            >
              📝 复习错题 ({wrongCount}题)
            </button>
          )}
          <button
            onClick={onReset}
            className="w-full py-3 px-4 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded-xl font-medium hover:bg-slate-200 dark:hover:bg-slate-600 transition-all"
          >
            🔄 重新开始
          </button>
        </div>
      </div>
    </div>
  )
}
