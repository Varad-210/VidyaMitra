import { useState, useEffect } from "react";
import { CheckCircle, XCircle, Clock, ArrowRight } from "lucide-react";
import { quizService } from "../services/quizService";

interface Question {
  question: string;
  options: string[];
  correct: number;
}

interface QuizSession {
  id: number;
  questions: Question[];
  current_question: number;
  total_questions: number;
  category: string;
  difficulty: string;
}

const QuizPage = () => {
  const [session, setSession] = useState<QuizSession | null>(null);
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState<number | null>(null);
  const [answers, setAnswers] = useState<(number | null)[]>([]);
  const [showResult, setShowResult] = useState(false);
  const [timeLeft, setTimeLeft] = useState(30);
  const [isLoading, setIsLoading] = useState(false);
  const [isStarted, setIsStarted] = useState(false);
  const [category, setCategory] = useState("general");
  const [difficulty, setDifficulty] = useState("medium");
  const [error, setError] = useState("");
  const [quizResults, setQuizResults] = useState(null);

  useEffect(() => {
    const timer = setInterval(() => {
      if (timeLeft > 0 && isStarted && !showResult) {
        setTimeLeft(timeLeft - 1);
      } else if (timeLeft === 0 && isStarted && !showResult) {
        handleNext();
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, isStarted, showResult]);

  const startQuiz = async () => {
    setIsLoading(true);
    setError("");

    try {
      const quizData = await quizService.startQuiz({
        category,
        num_questions: 5,
        difficulty
      });

      // Convert API response to QuizSession format
      const quizSession: QuizSession = {
        id: quizData.id,
        questions: quizData.questions || [],
        current_question: 0,
        total_questions: quizData.questions?.length || 5,
        category,
        difficulty
      };

      setSession(quizSession);
      setIsStarted(true);
      setTimeLeft(30);
    } catch (err) {
      setError(err.detail || "Failed to start quiz");
    } finally {
      setIsLoading(false);
    }
  };

  const handleNext = async () => {
    if (!session) return;

    const newAnswers = [...answers, selected];
    setAnswers(newAnswers);
    setSelected(null);

    // Submit answer to API
    if (selected !== null) {
      try {
        await quizService.submitQuizAnswer({
          quiz_attempt_id: session.id,
          question_id: current,
          answer: session.questions[current].options[selected]
        });
      } catch (err) {
        console.error("Failed to submit answer:", err);
      }
    }

    if (current + 1 < session.questions.length) {
      setCurrent(current + 1);
      setTimeLeft(30);
    } else {
      // Quiz completed - get results
      try {
        const results = await quizService.getQuizResults(session.id);
        setQuizResults(results);
        setShowResult(true);
      } catch (err) {
        console.error("Failed to get quiz results:", err);
        setShowResult(true);
      }
    }
  };

  const score = session ? answers.filter((a, i) => a === session.questions[i].correct).length : 0;

  if (showResult) {
    return (
      <div className="mx-auto max-w-lg space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-foreground">Quiz Complete!</h1>
          <p className="mt-1 text-sm text-muted-foreground">Here are your results</p>
        </div>

        <div className="rounded-xl border border-border bg-card p-8 text-center card-shadow">
          <div className="mx-auto flex h-24 w-24 items-center justify-center rounded-full bg-primary/10 mb-4">
            <span className="text-3xl font-bold text-primary">{score}/{session?.questions.length || 5}</span>
          </div>
          <p className="text-lg font-semibold text-foreground">
            {score >= 4 ? "Excellent!" : score >= 3 ? "Good job!" : "Keep practicing!"}
          </p>
          <p className="mt-1 text-sm text-muted-foreground">
            You scored {Math.round((score / (session?.questions.length || 5)) * 100)}%
          </p>
        </div>

        <div className="space-y-3">
          {session?.questions.map((q, i) => (
            <div key={i} className="flex items-start gap-3 rounded-lg border border-border bg-card p-3">
              {answers[i] === q.correct ? (
                <CheckCircle className="h-5 w-5 shrink-0 text-success mt-0.5" />
              ) : (
                <XCircle className="h-5 w-5 shrink-0 text-destructive mt-0.5" />
              )}
              <div>
                <p className="text-sm text-foreground">{q.question}</p>
                <p className="text-xs text-muted-foreground mt-1">
                  Correct: {q.options[q.correct]}
                </p>
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={() => { setCurrent(0); setAnswers([]); setShowResult(false); setSelected(null); setIsStarted(false); setSession(null); }}
          className="w-full rounded-lg gradient-primary px-4 py-3 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity"
        >
          Retry Quiz
        </button>
      </div>
    );
  }

  const q = session?.questions[current];

  if (!isStarted) {
    return (
      <div className="mx-auto max-w-lg space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Quiz</h1>
          <p className="mt-1 text-sm text-muted-foreground">Test your knowledge</p>
        </div>

        {error && (
          <div className="p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
            {error}
          </div>
        )}

        <div className="rounded-xl border border-border bg-card p-6 card-shadow">
          <h3 className="text-lg font-semibold text-foreground mb-4">Quiz Setup</h3>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-foreground">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="mt-1.5 w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                disabled={isLoading}
              >
                <option value="general">General</option>
                <option value="programming">Programming</option>
                <option value="database">Database</option>
                <option value="cloud">Cloud Computing</option>
                <option value="algorithms">Algorithms</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-foreground">Difficulty</label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="mt-1.5 w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                disabled={isLoading}
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            <button
              onClick={startQuiz}
              disabled={isLoading}
              className="w-full rounded-lg gradient-primary px-4 py-3 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {isLoading ? "Starting Quiz..." : "Start Quiz"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-lg space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Quiz</h1>
        <p className="mt-1 text-sm text-muted-foreground">Test your knowledge</p>
      </div>

      {/* Progress */}
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-muted-foreground">
          Question {current + 1} of {session?.questions.length || 5}
        </span>
        <div className="flex items-center gap-1 text-xs text-muted-foreground">
          <Clock className="h-3.5 w-3.5" />
          {timeLeft}s
        </div>
      </div>
      <div className="h-2 rounded-full bg-accent overflow-hidden">
        <div
          className="h-full rounded-full gradient-primary transition-all duration-300"
          style={{ width: `${((current + 1) / (session?.questions.length || 5)) * 100}%` }}
        />
      </div>

      {/* Question */}
      <div className="rounded-xl border border-border bg-card p-6 card-shadow">
        <p className="text-base font-medium text-foreground">{q?.question || "Loading question..."}</p>
        <div className="mt-4 space-y-2">
          {q?.options.map((opt, i) => (
            <button
              key={i}
              onClick={() => setSelected(i)}
              className={`w-full rounded-lg border px-4 py-3 text-left text-sm transition-all ${
                selected === i
                  ? "border-primary bg-primary/5 text-foreground"
                  : "border-border bg-card text-foreground hover:border-primary/40"
              }`}
            >
              <span className="mr-2 font-medium text-muted-foreground">
                {String.fromCharCode(65 + i)}.
              </span>
              {opt}
            </button>
          ))}
        </div>
      </div>

      <button
        onClick={handleNext}
        disabled={selected === null}
        className="w-full flex items-center justify-center gap-2 rounded-lg gradient-primary px-4 py-3 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity disabled:opacity-40"
      >
        {current + 1 < (session?.questions.length || 5) ? "Next Question" : "Finish Quiz"}
        <ArrowRight className="h-4 w-4" />
      </button>
    </div>
  );
};

export default QuizPage;
