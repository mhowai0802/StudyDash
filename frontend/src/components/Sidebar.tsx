import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  CalendarClock,
  Bot,
  Sparkles,
  Brain,
  Eye,
  Mic,
  Settings,
} from "lucide-react";
const courseLinks = [
  { to: "/course/nlp", label: "NLP & LLM", color: "#6366f1", icon: Brain },
  { to: "/course/cvpr", label: "CVPR", color: "#f59e0b", icon: Eye },
  { to: "/course/it-forum", label: "IT Forum", color: "#10b981", icon: Mic },
];

export default function Sidebar() {
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
      <NavLink
        to="/study-plan"
        className={({ isActive }) =>
          `sidebar-link ${isActive ? "active" : ""}`
        }
      >
        <Sparkles size={18} />
        <span>AI Study Plan</span>
      </NavLink>

      <NavLink
        to="/settings"
        className={({ isActive }) =>
          `sidebar-link ${isActive ? "active" : ""}`
        }
      >
        <Settings size={18} />
        <span>Settings</span>
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

    </nav>
  );
}
