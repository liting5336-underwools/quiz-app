import { useState, useEffect, useCallback } from 'react'
import questionsData from '../data/questions.json'
import type { Question, QuizProgress } from '../types/question'

const questions = questionsData as Question[]
const STORAGE_KEY = 'quiz-progress'

function loadProgress(): QuizProgress {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) return JSON.parse(saved)
  } catch {}
  return {
    currentIndex: 0,
    answers: {},
    wrongQuestions: [],
    completedQuestions: [],
  }
}

function saveProgress(progress: QuizProgress) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress))
}

export function useQuiz() {
  const [progress, setProgress] = useState<QuizProgress>(loadProgress)
  const [showResult, setShowResult] = useState(false)
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null)
  const [mode, setMode] = useState<'quiz' | 'wrong-review' | 'finished'>('quiz')

  // Persist progress
  useEffect(() => {
    saveProgress(progress)
  }, [progress])

  const currentQuestion = questions[progress.currentIndex]
  const totalQuestions = questions.length
  const progressPercent = (progress.completedQuestions.length / totalQuestions) * 100

  const handleAnswer = useCallback((answer: string) => {
    if (selectedAnswer) return // Already answered
    setSelectedAnswer(answer)

    const isCorrect = answer === currentQuestion.answer
    const newProgress = { ...progress }

    newProgress.answers[progress.currentIndex] = answer

    if (!isCorrect && !newProgress.wrongQuestions.includes(progress.currentIndex)) {
      newProgress.wrongQuestions = [...newProgress.wrongQuestions, progress.currentIndex]
    }

    if (!newProgress.completedQuestions.includes(progress.currentIndex)) {
      newProgress.completedQuestions = [...newProgress.completedQuestions, progress.currentIndex]
    }

    setProgress(newProgress)
  }, [selectedAnswer, currentQuestion, progress])

  const handleNext = useCallback(() => {
    if (progress.currentIndex < totalQuestions - 1) {
      setProgress(prev => ({ ...prev, currentIndex: prev.currentIndex + 1 }))
      setSelectedAnswer(null)
      setShowResult(false)
    } else {
      setMode('finished')
    }
  }, [progress.currentIndex, totalQuestions])

  const handlePrev = useCallback(() => {
    if (progress.currentIndex > 0) {
      setProgress(prev => ({ ...prev, currentIndex: prev.currentIndex - 1 }))
      setSelectedAnswer(null)
      setShowResult(false)
    }
  }, [progress.currentIndex])

  const goToQuestion = useCallback((index: number) => {
    setProgress(prev => ({ ...prev, currentIndex: index }))
    setSelectedAnswer(null)
    setShowResult(false)
  }, [])

  const resetProgress = useCallback(() => {
    const newProgress: QuizProgress = {
      currentIndex: 0,
      answers: {},
      wrongQuestions: [],
      completedQuestions: [],
    }
    setProgress(newProgress)
    setSelectedAnswer(null)
    setShowResult(false)
    setMode('quiz')
  }, [])

  const startWrongReview = useCallback(() => {
    if (progress.wrongQuestions.length === 0) return
    setMode('wrong-review')
    setProgress(prev => ({ ...prev, currentIndex: 0 }))
    setSelectedAnswer(null)
    setShowResult(false)
  }, [progress.wrongQuestions])

  const exitWrongReview = useCallback(() => {
    setMode('quiz')
    setProgress(prev => ({ ...prev, currentIndex: 0 }))
    setSelectedAnswer(null)
    setShowResult(false)
  }, [])

  // For wrong review mode, we use wrongQuestions as the question list
  const wrongQuestionsList = progress.wrongQuestions.map(idx => questions[idx])
  const currentWrongQuestion = wrongQuestionsList[progress.currentIndex]
  const isWrongReviewMode = mode === 'wrong-review'

  return {
    // State
    progress,
    currentQuestion: isWrongReviewMode ? currentWrongQuestion : currentQuestion,
    selectedAnswer,
    showResult,
    mode,
    totalQuestions,
    progressPercent,
    wrongQuestionsList,
    isWrongReviewMode,

    // Actions
    handleAnswer,
    handleNext,
    handlePrev,
    goToQuestion,
    resetProgress,
    startWrongReview,
    exitWrongReview,
    setSelectedAnswer,
    setShowResult,
  }
}
