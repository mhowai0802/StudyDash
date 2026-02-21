import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  BookOpen,
  CalendarClock,
  Bot,
  Brain,
  Eye,
  Mic,
} from "lucide-react";
import type { Stats } from "../types";

interface SidebarProps {
  stats: Stats | null;
}

const courseLinks = [
  { to: "/course/nlp", label: "NLP & LLM", color: "#6366f1", icon: Brain },
  { to: "/course/cvpr", label: "CVPR", color: "#f59e0b", icon: Eye },
  { to: "/course/it-forum", label: "IT Forum", color: "#10b981", icon: Mic },
];

export default function Sidebar({ stats }: SidebarProps) {
  const xpProgress = stats?.level.next
    ? ((stats.xp - stats.level.current.xp_required) /
        (stats.level.next.xp_required - stats.level.current.xp_required)) *
      100
    : 100;

  return (
    <nav className="sidebar">
      <div className="sidebar-logo">StudyDash</div>
      <div className="sidebar-subtitle">Study Progress Tracker</div>

      <div className="sidebar-section">Overview</div>
      <NavLink
        to="/"
        end
        className={({ isActive }) =>
          `sidebar-link ${isActive ? "active" : ""}`
        }
      >
        <LayoutDashboard size={18} />
        <span>Dashboard</span>
      </NavLink>
      <NavLink
        to="/deadlines"
        className={({ isActive }) =>
          `sidebar-link ${isActive ? "active" : ""}`
        }
      >
        <CalendarClock size={18} />
        <span>Deadlines</span>
      </NavLink>
      <NavLink
        to="/ai"
        className={({ isActive }) =>
          `sidebar-link ${isActive ? "active" : ""}`
        }
      >
        <Bot size={18} />
        <span>AI Assistant</span>
      </NavLink>

      <div className="sidebar-section">Courses</div>
      {courseLinks.map((c) => (
        <NavLink
          key={c.to}
          to={c.to}
          className={({ isActive }) =>
            `sidebar-link ${isActive ? "active" : ""}`
          }
        >
          <span className="course-dot" style={{ background: c.color }} />
          <span>{c.label}</span>
        </NavLink>
      ))}

      {stats && (
        <div className="xp-card">
          <div className="xp-card-level">
            Level {stats.level.current.level}
          </div>
          <div className="xp-card-title">{stats.level.current.name}</div>
          <div className="xp-bar-bg">
            <div
              className="xp-bar-fill"
              style={{ width: `${Math.min(xpProgress, 100)}%` }}
            />
          </div>
          <div className="xp-bar-text">
            {stats.xp} XP
            {stats.level.next &&
              ` / ${stats.level.next.xp_required} XP to ${stats.level.next.name}`}
          </div>
        </div>
      )}
    </nav>
  );
}
