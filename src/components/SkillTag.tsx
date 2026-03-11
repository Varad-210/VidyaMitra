interface SkillTagProps {
  label: string;
  variant?: "default" | "primary" | "success" | "warning" | "destructive";
}

const tagVariants = {
  default: "bg-accent text-accent-foreground",
  primary: "bg-primary/10 text-primary",
  success: "bg-success/10 text-success",
  warning: "bg-warning/10 text-warning",
  destructive: "bg-destructive/10 text-destructive",
};

export function SkillTag({ label, variant = "default" }: SkillTagProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${tagVariants[variant]}`}
    >
      {label}
    </span>
  );
}
