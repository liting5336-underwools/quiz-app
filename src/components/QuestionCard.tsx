import type { Question } from '../types/question'

interface QuestionCardProps {
  question: Question
  selectedAnswer: string | null
  onAnswer: (answer: string) => void
  showResult?: boolean
}

const optionLabels = ['A', 'B', 'C', 'D']

export function QuestionCard({ question, selectedAnswer, onAnswer, showResult = true }: QuestionCardProps) {
  const isCorrect = selectedAnswer === question.answer

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 overflow-hidden">
      {/* Question Header */}
      <div className="p-6 pb-4 border-b border-slate-100 dark:border-slate-700">
        <div className="flex items-start gap-3">
          <span className="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400 text-sm font-bold shrink-0">
            {question.id}
          </span>
          <p className="text-base leading-relaxed text-foreground">
            {question.question}
          </p>
        </div>
      </div>

      {/* Options */}
      <div className="p-6 space-y-3">
        {question.options.map((option, index) => {
          const letter = optionLabels[index]
          const isSelected = selectedAnswer === letter
          const isCorrectOption = letter === question.answer

          let optionStyle = 'border-slate-200 dark:border-slate-600 hover:border-indigo-300 dark:hover:border-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/20'

          if (selectedAnswer) {
            if (isCorrectOption) {
              optionStyle = 'border-green-400 dark:border-green-500 bg-green-50 dark:bg-green-900/20 ring-2 ring-green-400 dark:ring-green-500'
            } else if (isSelected && !isCorrectOption) {
              optionStyle = 'border-red-400 dark:border-red-500 bg-red-50 dark:bg-red-900/20 ring-2 ring-red-400 dark:ring-red-500'
            } else {
              optionStyle = 'border-slate-200 dark:border-slate-600 opacity-60'
            }
          }

          return (
            <button
              key={letter}
              onClick={() => !selectedAnswer && onAnswer(letter)}
              disabled={!!selectedAnswer}
              className={`w-full text-left p-4 rounded-xl border-2 transition-all duration-200 ${optionStyle} ${
                !selectedAnswer ? 'cursor-pointer active:scale-[0.98]' : 'cursor-default'
              }`}
            >
              <div className="flex items-center gap-3">
                <span className={`inline-flex items-center justify-center w-8 h-8 rounded-lg text-sm font-bold shrink-0 ${
                  selectedAnswer
                    ? isCorrectOption
                      ? 'bg-green-500 text-white'
                      : isSelected
                        ? 'bg-red-500 text-white'
                        : 'bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400'
                    : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'
                }`}>
                  {letter}
                </span>
                <span className="text-sm leading-relaxed">{option.substring(2).trim()}</span>
              </div>
            </button>
          )
        })}
      </div>

      {/* Explanation */}
      {selectedAnswer && showResult && question.explanation && (
        <div className={`px-6 py-4 border-t ${
          isCorrect
            ? 'bg-green-50/80 dark:bg-green-900/10 border-green-100 dark:border-green-900/30'
            : 'bg-amber-50/80 dark:bg-amber-900/10 border-amber-100 dark:border-amber-900/30'
        }`}>
          <div className="flex items-start gap-2">
            <span className={`text-lg shrink-0 ${isCorrect ? '' : 'mt-0.5'}`}>
              {isCorrect ? '✅' : '❌'}
            </span>
            <div>
              <p className={`text-sm font-medium mb-1 ${
                isCorrect ? 'text-green-700 dark:text-green-400' : 'text-amber-700 dark:text-amber-400'
              }`}>
                {isCorrect ? '回答正确！' : `回答错误，正确答案是 ${question.answer}`}
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {question.explanation}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
