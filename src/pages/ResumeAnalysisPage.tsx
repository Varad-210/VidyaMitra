import { CheckCircle, XCircle, AlertTriangle, Lightbulb } from "lucide-react";
import { DashboardCard } from "@/components/DashboardCards";
import { SkillTag } from "@/components/SkillTag";

const strengths = [
  "Strong project experience section",
  "Good use of action verbs",
  "Relevant technical skills listed",
  "Clean formatting and structure",
];

const missing = [
  "Tableau",
  "Cloud Computing (AWS/GCP)",
  "System Design",
  "CI/CD Pipelines",
];

const suggestions = [
  "Add quantifiable achievements to each role",
  "Include a professional summary section",
  "Add relevant certifications",
  "Optimize for ATS with industry keywords",
];

const detectedSkills = [
  "Python", "JavaScript", "React", "SQL", "Git", "Node.js", "MongoDB", "REST APIs",
];

const ResumeAnalysisPage = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Resume Analysis</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          AI-generated insights from your uploaded resume.
        </p>
      </div>

      {/* Score */}
      <div className="rounded-xl border border-primary/20 bg-primary/5 p-6 card-shadow">
        <div className="flex flex-col sm:flex-row items-center gap-6">
          <div className="relative flex h-28 w-28 items-center justify-center">
            <svg className="-rotate-90" width={112} height={112}>
              <circle cx={56} cy={56} r={48} fill="none" stroke="hsl(var(--border))" strokeWidth={8} />
              <circle
                cx={56} cy={56} r={48} fill="none"
                stroke="hsl(var(--primary))" strokeWidth={8}
                strokeDasharray={301.6} strokeDashoffset={301.6 * 0.22}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute flex flex-col items-center">
              <span className="text-3xl font-bold text-foreground">78</span>
              <span className="text-xs text-muted-foreground">/100</span>
            </div>
          </div>
          <div>
            <h2 className="text-lg font-semibold text-foreground">Good Resume</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Your resume scores above average. Address the suggestions below to reach 90+.
            </p>
          </div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Detected Skills */}
        <DashboardCard title="Detected Skills">
          <div className="flex flex-wrap gap-2">
            {detectedSkills.map((s) => (
              <SkillTag key={s} label={s} variant="success" />
            ))}
          </div>
        </DashboardCard>

        {/* Missing Skills */}
        <DashboardCard title="Missing Skills">
          <div className="flex flex-wrap gap-2">
            {missing.map((s) => (
              <SkillTag key={s} label={s} variant="destructive" />
            ))}
          </div>
        </DashboardCard>

        {/* Strengths */}
        <DashboardCard title="Strengths">
          <ul className="space-y-3">
            {strengths.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-foreground">
                <CheckCircle className="h-4 w-4 mt-0.5 shrink-0 text-success" />
                {s}
              </li>
            ))}
          </ul>
        </DashboardCard>

        {/* Suggestions */}
        <DashboardCard title="Improvement Suggestions">
          <ul className="space-y-3">
            {suggestions.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-foreground">
                <Lightbulb className="h-4 w-4 mt-0.5 shrink-0 text-warning" />
                {s}
              </li>
            ))}
          </ul>
        </DashboardCard>
      </div>
    </div>
  );
};

export default ResumeAnalysisPage;
