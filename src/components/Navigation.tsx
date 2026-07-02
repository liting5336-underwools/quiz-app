interface NavigationProps {
  currentIndex: number
  totalQuestions: number
  onPrev: () => void
  onNext: () => void
  hasAnswered: boolean
  isWrongReview?: boolean
  onExitWrongReview?: () => void
}

export function Navigation({
  currentIndex,
  totalQuestions,
  onPrev,
  onNext,
  hasAnswered,
  isWrongReview,
  onExitWrongReview,
}: NavigationProps) {
  const isFirst = currentIndex === 0
  const isLast = currentIndex === totalQuestions - 1

  return (
    <div className="flex items-center justify-between gap-3">
      <div className="flex gap-2">
        {isWrongReview && onExitWrongReview && (
          <button
            onClick={onExitWrongReview}
            className="px-4 py-2.5 text-sm font-medium rounded-xl border border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
          >
            ← 返回全部
          </button>
        )}
        <button
          onClick={onPrev}
          disabled={isFirst}
          className={`px-4 py-2.5 text-sm font-medium rounded-xl border transition-all ${
            isFirst
              ? 'border-slate-100 dark:border-slate-800 text-slate-300 dark:text-slate-600 cursor-not-allowed'
              : 'border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700 hover:border-slate-300 dark:hover:border-slate-500'
          }`}
        >
          ← 上一题
        </button>
      </div>

      <button
        onClick={onNext}
        disabled={!hasAnswered}
        className={`px-6 py-2.5 text-sm font-medium rounded-xl transition-all ${
          hasAnswered
            ? isLast
              ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:from-indigo-600 hover:to-purple-600 shadow-lg shadow-indigo-200 dark:shadow-indigo-900/30'
              : 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:from-indigo-600 hover:to-purple-600 shadow-lg shadow-indigo-200 dark:shadow-indigo-900/30'
            : 'bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-500 cursor-not-allowed'
        }`}
      >
        {isLast ? '完成' : '下一题 →'}
      </button>
    </div>
  )
}
