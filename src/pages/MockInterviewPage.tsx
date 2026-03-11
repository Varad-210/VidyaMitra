import { useState, useRef, useEffect } from "react";
import { Send, Bot, User } from "lucide-react";
import { interviewService } from "../services/interviewService";
import { useNavigate } from "react-router-dom";

interface Message {
  role: "ai" | "user";
  text: string;
}

interface InterviewSession {
  id: number;
  current_question_index: number;
  questions: string[];
  status: string;
}

const MockInterviewPage = () => {
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", text: "Welcome to your mock interview! I'll be asking you a series of questions to help you prepare. Let's begin by setting up your interview session." },
  ]);
  const [input, setInput] = useState("");
  const [session, setSession] = useState<InterviewSession | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [jobRole, setJobRole] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("beginner");
  const [isStarted, setIsStarted] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const startInterview = async () => {
    if (!jobRole.trim()) {
      setError("Please enter a job role");
      return;
    }

    setIsLoading(true);
    setError("");

    try {
      const interviewData = await interviewService.startInterview({
        job_role: jobRole,
        experience_level: experienceLevel,
        num_questions: 5
      });

      setSession(interviewData);
      setIsStarted(true);

      // Add first question
      if (interviewData.questions && interviewData.questions.length > 0) {
        setMessages([
          { role: "ai", text: `Great! Let's start your ${jobRole} interview. Here's your first question:` },
          { role: "ai", text: interviewData.questions[0] },
        ]);
      }
    } catch (err) {
      setError(err.detail || "Failed to start interview");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || !session) return;

    const userMessage = { role: "user" as const, text: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      // Submit answer
      const answerData = await interviewService.submitAnswer({
        interview_id: session.id,
        question: session.questions[session.current_question_index] || "",
        answer: input
      });

      // Get feedback and next question
      const feedback = await interviewService.getInterviewFeedback(session.id);

      const nextQuestionIndex = session.current_question_index + 1;
      
      if (nextQuestionIndex < session.questions.length) {
        // Add feedback and next question
        setTimeout(() => {
          setMessages([
            ...newMessages,
            { role: "ai", text: feedback.feedback || "Good answer! Let's move to the next question." },
            { role: "ai", text: session.questions[nextQuestionIndex] },
          ]);
          setSession({
            ...session,
            current_question_index: nextQuestionIndex
          });
          setIsLoading(false);
        }, 1000);
      } else {
        // Interview completed
        setTimeout(() => {
          setMessages([
            ...newMessages,
            { role: "ai", text: feedback.feedback || "Great job! You've completed the mock interview." },
            { role: "ai", text: `Your overall interview score: ${feedback.overall_score || 72}/100. ${feedback.improvement_suggestions || "Keep practicing to improve!"}` },
          ]);
          setIsLoading(false);
        }, 1000);
      }
    } catch (err) {
      setError(err.detail || "Failed to submit answer");
      setIsLoading(false);
    }
  };

  const progress = session ? ((session.current_question_index + 1) / session.questions.length) * 100 : 0;

  return (
    <div className="flex flex-col h-[calc(100vh-7rem)]">
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-foreground">Mock Interview</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Practice with AI-powered interview simulation.
        </p>

        {/* Error message */}
        {error && (
          <div className="mt-2 p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
            {error}
          </div>
        )}

        {/* Setup form */}
        {!isStarted && (
          <div className="mt-4 p-4 rounded-xl border border-border bg-card">
            <h3 className="text-lg font-semibold text-foreground mb-4">Interview Setup</h3>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-foreground">Job Role</label>
                <input
                  type="text"
                  value={jobRole}
                  onChange={(e) => setJobRole(e.target.value)}
                  className="mt-1.5 w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                  placeholder="e.g., Software Engineer, Data Analyst"
                  disabled={isLoading}
                />
              </div>
              <div>
                <label className="text-sm font-medium text-foreground">Experience Level</label>
                <select
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                  className="mt-1.5 w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                  disabled={isLoading}
                >
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>
              <button
                onClick={startInterview}
                disabled={isLoading || !jobRole.trim()}
                className="w-full rounded-lg gradient-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity disabled:opacity-50"
              >
                {isLoading ? "Starting Interview..." : "Start Interview"}
              </button>
            </div>
          </div>
        )}

        {/* Progress */}
        {isStarted && session && (
          <div className="mt-3 flex items-center gap-3">
            <div className="flex-1 h-2 rounded-full bg-accent overflow-hidden">
              <div
                className="h-full rounded-full gradient-primary transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
            <span className="text-xs font-medium text-muted-foreground">
              {session.current_question_index + 1}/{session.questions.length}
            </span>
          </div>
        )}
      </div>

      {/* Chat */}
      <div className="flex-1 overflow-y-auto rounded-xl border border-border bg-card p-4 space-y-4">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex gap-3 ${m.role === "user" ? "flex-row-reverse" : ""}`}
          >
            <div
              className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
                m.role === "ai" ? "bg-primary/10" : "gradient-primary"
              }`}
            >
              {m.role === "ai" ? (
                <Bot className="h-4 w-4 text-primary" />
              ) : (
                <User className="h-4 w-4 text-primary-foreground" />
              )}
            </div>
            <div
              className={`max-w-[75%] rounded-xl px-4 py-3 text-sm ${
                m.role === "ai"
                  ? "bg-accent text-foreground"
                  : "gradient-primary text-primary-foreground"
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      {isStarted && (
        <div className="mt-4 flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Type your answer..."
            className="flex-1 rounded-xl border border-border bg-card px-4 py-3 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim() || !session}
            className="flex h-12 w-12 items-center justify-center rounded-xl gradient-primary text-primary-foreground hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {isLoading ? (
              <div className="animate-spin h-5 w-5 border-2 border-primary-foreground border-t-transparent rounded-full" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default MockInterviewPage;
