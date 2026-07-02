import { useQuiz } from './hooks/useQuiz'
import { ProgressBar } from './components/ProgressBar'
import { QuestionCard } from './components/QuestionCard'
import { Navigation } from './components/Navigation'
import { QuestionGrid } from './components/QuestionGrid'
import { FinishedScreen } from './components/FinishedScreen'

function App() {
  const {
    progress,
    currentQuestion,
    selectedAnswer,
    mode,
    totalQuestions,
    progressPercent,
    wrongQuestionsList,
    isWrongReviewMode,
    handleAnswer,
    handleNext,
    handlePrev,
    goToQuestion,
    resetProgress,
    startWrongReview,
    exitWrongReview,
  } = useQuiz()

  // Finished screen
  if (mode === 'finished') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-slate-950 dark:to-indigo-950">
        <div className="max-w-3xl mx-auto px-4 py-8">
          <header className="text-center mb-8">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              中国近代史刷题
            </h1>
          </header>
          <FinishedScreen
            totalQuestions={totalQuestions}
            completedCount={progress.completedQuestions.length}
            wrongCount={progress.wrongQuestions.length}
            onReviewWrong={startWrongReview}
            onReset={resetProgress}
          />
        </div>
      </div>
    )
  }

  // Wrong review mode - no question available
  if (isWrongReviewMode && wrongQuestionsList.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-slate-950 dark:to-indigo-950">
        <div className="max-w-3xl mx-auto px-4 py-8">
          <div className="text-center py-20">
            <p className="text-muted-foreground">暂无错题，继续加油！</p>
            <button onClick={exitWrongReview} className="mt-4 text-indigo-500 hover:text-indigo-600">
              返回
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (!currentQuestion) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-slate-950 dark:to-indigo-950 flex items-center justify-center">
        <p className="text-muted-foreground">加载中...</p>
      </div>
    )
  }

  const hasAnswered = selectedAnswer !== null

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-slate-950 dark:to-indigo-950">
      <div className="max-w-3xl mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-6">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            中国近代史刷题
          </h1>
          <p className="text-muted-foreground mt-1 text-sm">
            {isWrongReviewMode
              ? `错题复习 (${wrongQuestionsList.length}题)`
              : `共 ${totalQuestions} 题 · 已完成 ${progress.completedQuestions.length} 题`
            }
          </p>
        </header>

        {/* Progress Bar */}
        {!isWrongReviewMode && (
          <div className="mb-4">
            <ProgressBar
              current={progress.currentIndex}
              total={totalQuestions}
              percent={progressPercent}
              completedCount={progress.completedQuestions.length}
              wrongCount={progress.wrongQuestions.length}
            />
          </div>
        )}

        {/* Wrong review header */}
        {isWrongReviewMode && (
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-amber-600 dark:text-amber-400">
                📝 错题复习模式
              </span>
              <span className="text-sm text-muted-foreground">
                第 {progress.currentIndex + 1} / {wrongQuestionsList.length} 题
              </span>
            </div>
          </div>
        )}

        {/* Main Content */}
        <div className="space-y-4">
          {/* Question Card */}
          <QuestionCard
            question={currentQuestion}
            selectedAnswer={selectedAnswer}
            onAnswer={handleAnswer}
          />

          {/* Navigation */}
          <Navigation
            currentIndex={progress.currentIndex}
            totalQuestions={isWrongReviewMode ? wrongQuestionsList.length : totalQuestions}
            onPrev={handlePrev}
            onNext={handleNext}
            hasAnswered={hasAnswered}
            isWrongReview={isWrongReviewMode}
            onExitWrongReview={exitWrongReview}
          />

          {/* Question Grid (only in normal mode) */}
          {!isWrongReviewMode && (
            <QuestionGrid
              total={totalQuestions}
              currentIndex={progress.currentIndex}
              completedQuestions={progress.completedQuestions}
              wrongQuestions={progress.wrongQuestions}
              onSelect={goToQuestion}
            />
          )}
        </div>
      </div>
    </div>
  )
}

export default App
