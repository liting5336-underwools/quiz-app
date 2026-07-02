interface QuestionGridProps {
  total: number
  currentIndex: number
  completedQuestions: number[]
  wrongQuestions: number[]
  onSelect: (index: number) => void
}

export function QuestionGrid({
  total,
  currentIndex,
  completedQuestions,
  wrongQuestions,
  onSelect,
}: QuestionGridProps) {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 p-4">
      <h3 className="text-sm font-medium text-muted-foreground mb-3">题目导航</h3>
      <div className="grid grid-cols-10 gap-1.5">
        {Array.from({ length: total }, (_, i) => {
          const isCurrent = i === currentIndex
          const isCompleted = completedQuestions.includes(i)
          const isWrong = wrongQuestions.includes(i)
          const isCorrect = isCompleted && !isWrong

          let btnStyle = 'bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-600'

          if (isCurrent) {
            btnStyle = 'bg-indigo-500 text-white ring-2 ring-indigo-300 dark:ring-indigo-700'
          } else if (isWrong) {
            btnStyle = 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400'
          } else if (isCorrect) {
            btnStyle = 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400'
          }

          return (
            <button
              key={i}
              onClick={() => onSelect(i)}
              className={`w-full aspect-square rounded-lg text-xs font-medium transition-all ${btnStyle}`}
              title={`第 ${i + 1} 题`}
            >
              {i + 1}
            </button>
          )
        })}
      </div>
      <div className="flex items-center gap-4 mt-3 pt-3 border-t border-slate-100 dark:border-slate-700 text-xs text-muted-foreground">
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-green-100 dark:bg-green-900/30" />
          <span>正确</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-red-100 dark:bg-red-900/30" />
          <span>错误</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded bg-indigo-500" />
          <span>当前</span>
        </div>
      </div>
    </div>
  )
}
