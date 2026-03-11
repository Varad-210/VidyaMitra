import { useState, useEffect } from "react";
import {
  FileText,
  MessageSquare,
  TrendingUp,
  BookOpen,
  Target,
  Clock,
} from "lucide-react";
import { StatCard, DashboardCard } from "@/components/DashboardCards";
import { SkillTag } from "@/components/SkillTag";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { authService } from "../services/authService";
import { progressService } from "../services/progressService";
import { recommendationService } from "../services/recommendationService";

const DashboardPage = () => {
  const [user, setUser] = useState(null);
  const [progressData, setProgressData] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setLoading(true);
        setError("");

        // Get current user
        const userData = await authService.getCurrentUser();
        setUser(userData);

        // Get user progress
        const progress = await progressService.getProgressSummary(userData.id);
        setProgressData(progress);

        // Get skill recommendations
        const recs = await recommendationService.getSkillRecommendations(userData.id);
        setRecommendations(recs);

      } catch (err: any) {
        console.error("Dashboard data loading error:", err);
        // Handle different error formats
        let errorMessage = "Failed to load dashboard data";
        
        if (typeof err === 'string') {
          errorMessage = err;
        } else if (err?.detail) {
          if (typeof err.detail === 'string') {
            errorMessage = err.detail;
          } else if (err.detail?.msg) {
            errorMessage = err.detail.msg;
          } else if (err.detail?.message) {
            errorMessage = err.detail.message;
          }
        } else if (err?.message) {
          errorMessage = err.message;
        } else if (err?.error) {
          errorMessage = err.error;
        }
        
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  // Mock data fallbacks
  const skillData = progressData?.skills || [
    { name: "Python", score: 85 },
    { name: "SQL", score: 70 },
    { name: "ML", score: 55 },
    { name: "React", score: 78 },
    { name: "Cloud", score: 40 },
  ];

  const activities = progressData?.timeline || [
    { text: "Completed Python Quiz", time: "2 hours ago", icon: BookOpen },
    { text: "Resume analyzed", time: "5 hours ago", icon: FileText },
    { text: "Mock interview completed", time: "1 day ago", icon: MessageSquare },
    { text: "Roadmap updated", time: "2 days ago", icon: Target },
  ];

  const stats = progressData?.statistics || {
    resume_score: 78,
    interview_score: 65,
    skills_learned: 12,
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
        <h1 className="text-2xl font-bold text-foreground">Dashboard</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Welcome back, {user?.full_name || "User"}. Here's your career readiness overview.
        </p>
      </div>

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Resume Score"
          value={stats.resume_score}
          subtitle="out of 100"
          icon={FileText}
          trend={{ value: "12% this month", positive: true }}
          variant="primary"
        />
        <StatCard
          title="Interview Score"
          value={stats.interview_score}
          subtitle="out of 100"
          icon={MessageSquare}
          trend={{ value: "8% this week", positive: true }}
          variant="success"
        />
        <StatCard
          title="Skills Learned"
          value={stats.skills_learned}
          subtitle="of 20 target"
          icon={TrendingUp}
          variant="warning"
        />
        <StatCard
          title="Study Hours"
          value={`${stats.study_hours}h`}
          subtitle="this month"
          icon={Clock}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Skill Chart */}
        <DashboardCard title="Skill Proficiency" className="lg:col-span-2">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={skillData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="name" fontSize={12} stroke="hsl(var(--muted-foreground))" />
                <YAxis fontSize={12} stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "0.5rem",
                    fontSize: "0.75rem",
                  }}
                />
                <Bar dataKey="score" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </DashboardCard>

        {/* Recent Activity */}
        <DashboardCard title="Recent Activity">
          <div className="space-y-4">
            {activities.map((a, i) => (
              <div key={i} className="flex items-start gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-accent">
                  <a.icon className="h-4 w-4 text-muted-foreground" />
                </div>
                <div>
                  <p className="text-sm text-foreground">{a.text}</p>
                  <p className="text-xs text-muted-foreground">{a.time}</p>
                </div>
              </div>
            ))}
          </div>
        </DashboardCard>
      </div>

      {/* Skills */}
      <div className="grid gap-6 lg:grid-cols-2">
        <DashboardCard title="Recommended Skills">
          <div className="flex flex-wrap gap-2">
            {recommendations?.trending_skills?.slice(0, 5).map((skill, i) => (
              <SkillTag key={i} label={skill.skill} variant="primary" />
            )) || (
              <>
                <SkillTag label="Tableau" variant="primary" />
                <SkillTag label="Cloud Computing" variant="primary" />
                <SkillTag label="Docker" variant="primary" />
                <SkillTag label="System Design" variant="primary" />
                <SkillTag label="Data Visualization" variant="primary" />
              </>
            )}
          </div>
        </DashboardCard>
        <DashboardCard title="Skills to Improve">
          <div className="flex flex-wrap gap-2">
            {recommendations?.trending_skills?.slice(5, 8).map((skill, i) => (
              <SkillTag key={i} label={skill.skill} variant={i === 0 ? "destructive" : "warning"} />
            )) || (
              <>
                <SkillTag label="Machine Learning" variant="warning" />
                <SkillTag label="Cloud Infrastructure" variant="destructive" />
                <SkillTag label="SQL Advanced" variant="warning" />
              </>
            )}
          </div>
        </DashboardCard>
      </div>
    </div>
  );
};

export default DashboardPage;
