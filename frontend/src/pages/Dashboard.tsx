import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  BookOpen,
  Calendar,
  Trophy,
  Zap,
  ArrowRight,
  Sparkles,
} from "lucide-react";
import { getCourses, getDeadlines, getStats, aiStudyPlan } from "../api/client";
import type { Course, Deadline, Stats } from "../types";
import ProgressRing from "../components/ProgressRing";
import MonthlyCalendar from "../components/MonthlyCalendar";
import ReactMarkdown from "react-markdown";

interface DashboardProps {
  onStatsUpdate: () => void;
}

export default function Dashboard({ onStatsUpdate }: DashboardProps) {
  const [courses, setCourses] = useState<Course[]>([]);
  const [deadlines, setDeadlines] = useState<Deadline[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [studyPlan, setStudyPlan] = useState<string>("");
  const [loadingPlan, setLoadingPlan] = useState(false);
  const nav = useNavigate();

  useEffect(() => {
    getCourses().then(setCourses);
    getDeadlines().then(setDeadlines);
    getStats().then(setStats);
  }, []);

  const handleGeneratePlan = async () => {
    setLoadingPlan(true);
    try {
      const result = await aiStudyPlan();
      setStudyPlan(result.plan);
    } catch {
      setStudyPlan("Could not generate study plan. Make sure the backend is running.");
    }
    setLoadingPlan(false);
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">
          Welcome back! Here's your study overview.
        </p>
      </div>

      {/* Quick Stats Row */}
      {stats && (
        <div className="card-grid card-grid-3" style={{ marginBottom: 24 }}>
          <div className="card" style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div style={{ padding: 12, borderRadius: 12, background: "rgba(99,102,241,0.1)" }}>
              <Trophy size={24} color="var(--accent-indigo)" />
            </div>
            <div>
              <div style={{ fontSize: 24, fontWeight: 800 }}>{stats.xp} XP</div>
              <div style={{ fontSize: 13, color: "var(--text-secondary)" }}>
                Level {stats.level.current.level}: {stats.level.current.name}
              </div>
            </div>
          </div>
          <div className="card" style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div style={{ padding: 12, borderRadius: 12, background: "rgba(16,185,129,0.1)" }}>
              <BookOpen size={24} color="var(--accent-emerald)" />
            </div>
            <div>
              <div style={{ fontSize: 24, fontWeight: 800 }}>
                {stats.completed_materials}/{stats.total_materials}
              </div>
              <div style={{ fontSize: 13, color: "var(--text-secondary)" }}>
                Materials Completed
              </div>
            </div>
          </div>
          <div className="card" style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div style={{ padding: 12, borderRadius: 12, background: "rgba(245,158,11,0.1)" }}>
              <Calendar size={24} color="var(--accent-amber)" />
            </div>
            <div>
              <div style={{ fontSize: 24, fontWeight: 800 }}>
                {stats.completed_deadlines}/{stats.total_deadlines}
              </div>
              <div style={{ fontSize: 13, color: "var(--text-secondary)" }}>
                Deadlines Done
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Monthly Calendar */}
      <div style={{ marginBottom: 24 }}>
        <MonthlyCalendar courses={courses} deadlines={deadlines} />
      </div>

      {/* Bottom row: Course cards + AI Study Plan */}
      <div className="card-grid card-grid-2" style={{ marginBottom: 24 }}>
        {/* Course summary cards stacked */}
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {courses.map((c) => {
            const progress =
              c.total_materials && c.completed_materials != null
                ? Math.round((c.completed_materials / c.total_materials) * 100)
                : 0;
            return (
              <div
                key={c.id}
                className="card course-card"
                style={{ borderTopColor: c.color }}
                onClick={() => nav(`/course/${c.id}`)}
              >
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                      <span style={{ width: 10, height: 10, borderRadius: "50%", background: c.color, flexShrink: 0 }} />
                      <span style={{ fontSize: 15, fontWeight: 700 }}>{c.code}</span>
                      <span style={{ fontSize: 12, color: "var(--text-muted)" }}>{c.schedule}</span>
                    </div>
                    <div className="course-card-stats" style={{ borderTop: "none", paddingTop: 0, marginTop: 0 }}>
                      <div className="course-card-stat">
                        <strong>{c.completed_materials || 0}</strong>/{c.total_materials || 0} materials
                      </div>
                      <div className="course-card-stat">
                        <strong>{c.total_weeks}</strong> weeks
                      </div>
                    </div>
                  </div>
                  <ProgressRing progress={progress} size={48} strokeWidth={4} color={c.color} />
                </div>
              </div>
            );
          })}
          <button
            className="btn btn-secondary"
            style={{ width: "100%", justifyContent: "center" }}
            onClick={() => nav("/deadlines")}
          >
            <Calendar size={16} /> View All Deadlines <ArrowRight size={14} />
          </button>
        </div>

        {/* AI Study Plan */}
        <div className="card" style={{ alignSelf: "start" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
            <h3 style={{ fontSize: 16, fontWeight: 700 }}>
              <Sparkles size={16} style={{ marginRight: 6, verticalAlign: "middle" }} />
              AI Study Plan
            </h3>
            <button
              className="btn btn-sm btn-primary"
              onClick={handleGeneratePlan}
              disabled={loadingPlan}
            >
              {loadingPlan ? (
                <><span className="spinner" style={{ width: 14, height: 14, borderWidth: 2 }} /> Generating...</>
              ) : (
                <><Zap size={14} /> Generate Plan</>
              )}
            </button>
          </div>
          {studyPlan ? (
            <div className="ai-content" style={{ maxHeight: 400, overflowY: "auto" }}>
              <ReactMarkdown>{studyPlan}</ReactMarkdown>
            </div>
          ) : (
            <div style={{ padding: 20, textAlign: "center", color: "var(--text-muted)", fontSize: 13 }}>
              Click "Generate Plan" to get a personalized AI study plan based on your current progress and upcoming deadlines.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
