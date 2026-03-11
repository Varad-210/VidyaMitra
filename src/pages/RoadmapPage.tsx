import { useState, useEffect } from "react";
import { CheckCircle, Circle, BookOpen, Award } from "lucide-react";
import { SkillTag } from "@/components/SkillTag";
import { authService } from "../services/authService";
import { recommendationService } from "../services/recommendationService";

const RoadmapPage = () => {
  const [user, setUser] = useState(null);
  const [roadmapData, setRoadmapData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadRoadmapData = async () => {
      try {
        setLoading(true);
        setError("");

        // Get current user
        const userData = await authService.getCurrentUser();
        setUser(userData);

        // Get career roadmap
        const roadmap = await recommendationService.getCareerRoadmap(userData.id);
        setRoadmapData(roadmap);

      } catch (err) {
        console.error("Roadmap data loading error:", err);
        setError("Failed to load roadmap data");
      } finally {
        setLoading(false);
      }
    };

    loadRoadmapData();
  }, []);

  // Mock data fallbacks
  const roadmap = roadmapData?.weekly_roadmap || [
    {
      week: "Week 1",
      title: "Python Advanced",
      description: "Master decorators, generators, async programming",
      status: "completed" as const,
      skills: ["Decorators", "Generators", "AsyncIO"],
    },
    {
      week: "Week 2",
      title: "Data Visualization",
      description: "Learn Tableau, Matplotlib, and Seaborn",
      status: "current" as const,
      skills: ["Tableau", "Matplotlib", "Seaborn"],
    },
    {
      week: "Week 3",
      title: "SQL Projects",
      description: "Build complex queries, optimize performance",
      status: "upcoming" as const,
      skills: ["Window Functions", "Indexing", "Query Optimization"],
    },
    {
      week: "Week 4",
      title: "Portfolio Building",
      description: "Create GitHub portfolio, deploy projects",
      status: "upcoming" as const,
    skills: ["GitHub", "Deployment", "Documentation"],
  },
  {
    week: "Week 5",
    title: "Cloud Computing",
    description: "AWS fundamentals, EC2, S3, Lambda",
    status: "upcoming" as const,
    skills: ["AWS", "EC2", "S3", "Lambda"],
  },
];

  const certifications = roadmapData?.certifications || [
    { name: "AWS Cloud Practitioner", provider: "Amazon", priority: "High" },
    { name: "Google Data Analytics", provider: "Google", priority: "Medium" },
    { name: "Tableau Desktop Specialist", provider: "Tableau", priority: "High" },
  ];

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-muted rounded w-48 mb-2"></div>
          <div className="h-4 bg-muted rounded w-96"></div>
        </div>
        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="h-32 bg-muted rounded"></div>
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
        <h1 className="text-2xl font-bold text-foreground">Career Roadmap</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Your personalized learning path based on skill gap analysis.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Timeline */}
        <div className="lg:col-span-2 space-y-0">
          {roadmap.map((item, i) => (
            <div key={i} className="flex gap-4">
              {/* Line */}
              <div className="flex flex-col items-center">
                <div
                  className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 ${
                    item.status === "completed"
                      ? "border-success bg-success/10"
                      : item.status === "current"
                      ? "border-primary bg-primary/10"
                      : "border-border bg-card"
                  }`}
                >
                  {item.status === "completed" ? (
                    <CheckCircle className="h-4 w-4 text-success" />
                  ) : (
                    <Circle
                      className={`h-4 w-4 ${
                        item.status === "current" ? "text-primary" : "text-muted-foreground"
                      }`}
                    />
                  )}
                </div>
                {i < roadmap.length - 1 && (
                  <div
                    className={`w-0.5 flex-1 ${
                      item.status === "completed" ? "bg-success" : "bg-border"
                    }`}
                  />
                )}
              </div>

              {/* Content */}
              <div
                className={`mb-6 flex-1 rounded-xl border p-4 card-shadow ${
                  item.status === "current"
                    ? "border-primary/30 bg-primary/5"
                    : "border-border bg-card"
                }`}
              >
                <span className="text-xs font-semibold text-primary">{item.week}</span>
                <h3 className="mt-1 text-sm font-semibold text-foreground">{item.title}</h3>
                <p className="mt-1 text-xs text-muted-foreground">{item.description}</p>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {item.skills.map((s) => (
                    <SkillTag key={s} label={s} variant={item.status === "completed" ? "success" : "default"} />
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Certifications */}
        <div className="rounded-xl border border-border bg-card p-5 card-shadow h-fit">
          <div className="flex items-center gap-2 mb-4">
            <Award className="h-5 w-5 text-primary" />
            <h3 className="text-sm font-semibold text-foreground">Suggested Certifications</h3>
          </div>
          <div className="space-y-3">
            {certifications.map((c, i) => (
              <div key={i} className="rounded-lg border border-border p-3">
                <p className="text-sm font-medium text-foreground">{c.name}</p>
                <p className="text-xs text-muted-foreground">{c.provider}</p>
                <SkillTag
                  label={c.priority}
                  variant={c.priority === "High" ? "destructive" : "warning"}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RoadmapPage;
