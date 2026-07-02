export interface Question {
  id: number;
  type: "single";
  question: string;
  options: string[];
  answer: string;
  explanation: string;
}

export interface QuizProgress {
  currentIndex: number;
  answers: Record<number, string>;
  wrongQuestions: number[];
  completedQuestions: number[];
}
