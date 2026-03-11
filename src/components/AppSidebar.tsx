import { NavLink, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Upload,
  FileSearch,
  Map,
  MessageSquare,
  HelpCircle,
  BarChart3,
  Settings,
  ChevronLeft,
  GraduationCap,
  X,
} from "lucide-react";

const navItems = [
  { label: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
  { label: "Resume Upload", icon: Upload, path: "/resume-upload" },
  { label: "Resume Analysis", icon: FileSearch, path: "/resume-analysis" },
  { label: "Career Roadmap", icon: Map, path: "/roadmap" },
  { label: "Mock Interview", icon: MessageSquare, path: "/interview" },
  { label: "Quiz", icon: HelpCircle, path: "/quiz" },
  { label: "Progress Tracker", icon: BarChart3, path: "/progress" },
  { label: "Settings", icon: Settings, path: "/settings" },
];

interface AppSidebarProps {
  collapsed: boolean;
  onToggle: () => void;
  onClose: () => void;
}

export function AppSidebar({ collapsed, onToggle, onClose }: AppSidebarProps) {
  const location = useLocation();

  return (
    <div className="flex h-full flex-col border-r border-border bg-card">
      {/* Logo */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-border">
        <div className="flex items-center gap-2 overflow-hidden">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg gradient-primary">
            <GraduationCap className="h-5 w-5 text-primary-foreground" />
          </div>
          {!collapsed && (
            <span className="text-lg font-semibold text-foreground whitespace-nowrap">
              VidyaMitra
            </span>
          )}
        </div>
        <button
          onClick={onToggle}
          className="hidden lg:flex h-7 w-7 items-center justify-center rounded-md text-muted-foreground hover:bg-accent transition-colors"
        >
          <ChevronLeft
            className={`h-4 w-4 transition-transform ${collapsed ? "rotate-180" : ""}`}
          />
        </button>
        <button
          onClick={onClose}
          className="flex lg:hidden h-7 w-7 items-center justify-center rounded-md text-muted-foreground hover:bg-accent"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={onClose}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground"
              } ${collapsed ? "justify-center px-2" : ""}`}
              title={collapsed ? item.label : undefined}
            >
              <item.icon className="h-5 w-5 shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </NavLink>
          );
        })}
      </nav>

      {/* Bottom */}
      {!collapsed && (
        <div className="p-4 border-t border-border">
          <div className="rounded-lg bg-primary/5 p-3">
            <p className="text-xs font-medium text-foreground">Pro Tip</p>
            <p className="mt-1 text-xs text-muted-foreground">
              Upload your resume to get personalized career insights.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
