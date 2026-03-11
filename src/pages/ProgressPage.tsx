import { useState, useEffect } from "react";
import { StatCard, DashboardCard } from "@/components/DashboardCards";
import { FileText, MessageSquare, BookOpen, Award } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  BarChart,
  Bar,
} from "recharts";
import { authService } from "../services/authService";
import { progressService } from "../services/progressService";

const ProgressPage = () => {
  const [user, setUser] = useState(null);
  const [progressData, setProgressData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadProgressData = async () => {
      try {
        setLoading(true);
        setError("");

        // Get current user
        const userData = await authService.getCurrentUser();
        setUser(userData);

        // Get user progress
        const progress = await progressService.getUserProgress(userData.id);
        setProgressData(progress);

      } catch (err) {
        console.error("Progress data loading error:", err);
        setError("Failed to load progress data");
      } finally {
        setLoading(false);
      }
    };

    loadProgressData();
  }, []);

  // Mock data fallbacks
  const resumeHistory = progressData?.timeline?.filter(t => t.metric_type === "resume_score").map(t => ({
    date: new Date(t.created_at).toLocaleDateString('en', { month: 'short' }),
    score: t.metric_value
  })) || [
    { date: "Jan", score: 52 },
    { date: "Feb", score: 60 },
    { date: "Mar", score: 68 },
    { date: "Apr", score: 72 },
    { date: "May", score: 78 },
  ];

  const quizScores = progressData?.quiz_scores || [
    { quiz: "Python", score: 80 },
    { quiz: "SQL", score: 90 },
    { quiz: "ML", score: 60 },
    { quiz: "Cloud", score: 45 },
    { quiz: "DSA", score: 70 },
  ];

  const stats = progressData?.statistics || {
    resume_score: 78,
    interview_score: 65,
    quizzes_completed: 8,
    study_hours: 34
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-muted rounded w-48 mb-2"></div>
          <div className="h-4 bg-muted rounded w-96"></div>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="h-24 bg-muted rounded"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <div className="p-4 rounded-lg bg-destructive/10 text-destructive">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Progress Tracker</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Track your learning journey and improvements.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Resume Score" value={78} icon={FileText} trend={{ value: "+26 overall", positive: true }} variant="primary" />
        <StatCard title="Quiz Avg" value="69%" icon={BookOpen} trend={{ value: "+15%", positive: true }} variant="success" />
        <StatCard title="Interviews" value={5} icon={MessageSquare} subtitle="completed" />
        <StatCard title="Skills Learned" value={12} icon={Award} variant="warning" />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <DashboardCard title="Resume Score Over Time">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={resumeHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="date" fontSize={12} stroke="hsl(var(--muted-foreground))" />
                <YAxis fontSize={12} stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "0.5rem",
                    fontSize: "0.75rem",
                  }}
                />
                <Line type="monotone" dataKey="score" stroke="hsl(var(--primary))" strokeWidth={2} dot={{ fill: "hsl(var(--primary))" }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </DashboardCard>

        <DashboardCard title="Quiz Performance">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={quizScores}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="quiz" fontSize={12} stroke="hsl(var(--muted-foreground))" />
                <YAxis fontSize={12} stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "0.5rem",
                    fontSize: "0.75rem",
                  }}
                />
                <Bar dataKey="score" fill="hsl(var(--chart-2))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </DashboardCard>
      </div>

      {/* Skills progress */}
      <DashboardCard title="Skills Progress">
        <div className="space-y-4">
          {[
            { skill: "Python", progress: 85 },
            { skill: "SQL", progress: 70 },
            { skill: "Machine Learning", progress: 55 },
            { skill: "React", progress: 78 },
            { skill: "Cloud Computing", progress: 40 },
          ].map((s) => (
            <div key={s.skill}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-foreground">{s.skill}</span>
                <span className="text-xs text-muted-foreground">{s.progress}%</span>
              </div>
              <div className="h-2 rounded-full bg-accent overflow-hidden">
                <div
                  className="h-full rounded-full gradient-primary transition-all duration-500"
                  style={{ width: `${s.progress}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </DashboardCard>
    </div>
  );
};

export default ProgressPage;
