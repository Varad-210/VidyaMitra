import { useState } from "react";
import { User, Bell, Shield, Palette } from "lucide-react";

const SettingsPage = () => {
  const [name, setName] = useState("Aarav Sharma");
  const [email, setEmail] = useState("aarav@example.com");
  const [notifications, setNotifications] = useState({
    email: true,
    quiz: true,
    interview: false,
  });

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-foreground">Settings</h1>
        <p className="mt-1 text-sm text-muted-foreground">Manage your account preferences.</p>
      </div>

      {/* Profile */}
      <div className="rounded-xl border border-border bg-card p-5 card-shadow">
        <div className="flex items-center gap-2 mb-4">
          <User className="h-5 w-5 text-primary" />
          <h3 className="text-sm font-semibold text-foreground">Profile</h3>
        </div>
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium text-foreground">Full Name</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1.5 w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
            />
          </div>
          <div>
            <label className="text-sm font-medium text-foreground">Email</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1.5 w-full rounded-lg border border-border bg-background px-3 py-2.5 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
            />
          </div>
          <button className="rounded-lg gradient-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground hover:opacity-90 transition-opacity">
            Save Changes
          </button>
        </div>
      </div>

      {/* Notifications */}
      <div className="rounded-xl border border-border bg-card p-5 card-shadow">
        <div className="flex items-center gap-2 mb-4">
          <Bell className="h-5 w-5 text-primary" />
          <h3 className="text-sm font-semibold text-foreground">Notifications</h3>
        </div>
        <div className="space-y-3">
          {[
            { key: "email" as const, label: "Email notifications" },
            { key: "quiz" as const, label: "Quiz reminders" },
            { key: "interview" as const, label: "Interview tips" },
          ].map((item) => (
            <label key={item.key} className="flex items-center justify-between cursor-pointer">
              <span className="text-sm text-foreground">{item.label}</span>
              <button
                onClick={() =>
                  setNotifications({ ...notifications, [item.key]: !notifications[item.key] })
                }
                className={`relative h-6 w-11 rounded-full transition-colors ${
                  notifications[item.key] ? "bg-primary" : "bg-border"
                }`}
              >
                <span
                  className={`absolute top-0.5 left-0.5 h-5 w-5 rounded-full bg-card shadow transition-transform ${
                    notifications[item.key] ? "translate-x-5" : ""
                  }`}
                />
              </button>
            </label>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
