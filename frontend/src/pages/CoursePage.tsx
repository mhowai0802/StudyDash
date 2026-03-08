import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { ChevronDown, ChevronRight, Check } from "lucide-react";
import { getCourse, getProject, toggleMilestone } from "../api/client";
import type { Course } from "../types";

export default function CoursePage() {
  const { courseId } = useParams<{ courseId: string }>();
  const [course, setCourse] = useState<Course | null>(null);
  const [expandedWeek, setExpandedWeek] = useState<number | null>(null);
  const [tab, setTab] = useState<"weeks" | "assessment" | "project">("weeks");
  const [project, setProject] = useState<any>(null);

  const reload = () => {
    if (courseId) {
      getCourse(courseId).then(setCourse);
      getProject(courseId).then(setProject).catch(() => setProject(null));
    }
  };

  useEffect(() => { reload(); }, [courseId]);

  if (!course) return <div className="loading"><span className="spinner" /> Loading course...</div>;

  return (
    <div>
      <div className="page-header">
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 4 }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", background: course.color }} />
          <h1 className="page-title">{course.code}</h1>
        </div>
        <p className="page-subtitle">{course.name}</p>
        <div style={{ fontSize: 13, color: "var(--text-muted)", marginTop: 4 }}>
          {course.instructor} &middot; {course.schedule} &middot; {course.venue}
        </div>
      </div>

      <div className="tabs">
        <button className={`tab ${tab === "weeks" ? "active" : ""}`} onClick={() => setTab("weeks")}>
          Weekly Topics
        </button>
        {project && (
          <button className={`tab ${tab === "project" ? "active" : ""}`} onClick={() => setTab("project")}>
            Project
          </button>
        )}
        <button className={`tab ${tab === "assessment" ? "active" : ""}`} onClick={() => setTab("assessment")}>
          Assessment
        </button>
      </div>

      {tab === "project" && project && (
        <div>
          <div className="card" style={{ marginBottom: 20 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
              <div>
                <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 4 }}>{project.title}</h3>
                <div style={{ fontSize: 13, color: "var(--text-secondary)" }}>{project.type}</div>
              </div>
              <div style={{ textAlign: "right", fontSize: 12, color: "var(--text-muted)" }}>
                <div>Presentation: {new Date(project.presentation_date + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short" })}</div>
                <div>Report due: {project.report_deadline}</div>
              </div>
            </div>
            <p style={{ fontSize: 14, color: "var(--text-secondary)", lineHeight: 1.6, marginBottom: 16 }}>
              {project.summary}
            </p>
            <div style={{ fontSize: 13, color: "var(--text-muted)" }}>
              Presentation format: {project.presentation}
            </div>
          </div>

          <div className="card" style={{ marginBottom: 20 }}>
            <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 4 }}>Milestones</h3>
            <div style={{ fontSize: 12, color: "var(--text-secondary)", marginBottom: 16 }}>
              {project.milestones.filter((m: any) => m.done).length}/{project.milestones.length} completed
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              {project.milestones.map((m: any) => {
                const due = new Date(m.due + "T00:00:00");
                const now = new Date();
                const isPast = due < now && !m.done;
                const daysLeft = Math.ceil((due.getTime() - now.getTime()) / 86400000);
                return (
                  <div
                    key={m.id}
                    style={{
                      display: "flex", alignItems: "center", gap: 10,
                      padding: "10px 14px", borderRadius: 8,
                      background: m.done ? "rgba(16,185,129,0.06)" : isPast ? "rgba(244,63,94,0.06)" : "var(--bg-tertiary)",
                      borderLeft: `4px solid ${m.done ? "var(--accent-emerald)" : isPast ? "var(--accent-rose)" : "var(--border)"}`,
                    }}
                  >
                    <div
                      className={`deadline-checkbox ${m.done ? "done" : ""}`}
                      onClick={async () => { await toggleMilestone(courseId!, m.id); reload(); }}
                    >
                      {m.done && <Check size={12} color="white" />}
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: 14, fontWeight: 500, textDecoration: m.done ? "line-through" : "none", color: m.done ? "var(--text-muted)" : "var(--text-primary)" }}>
                        {m.title}
                      </div>
                    </div>
                    <div style={{ fontSize: 11, color: isPast ? "var(--accent-rose)" : "var(--text-muted)", whiteSpace: "nowrap" }}>
                      {due.toLocaleDateString("en-GB", { day: "numeric", month: "short" })}
                      {!m.done && (
                        <span style={{ marginLeft: 6 }}>
                          {daysLeft < 0 ? `${Math.abs(daysLeft)}d overdue` : daysLeft === 0 ? "Today" : `${daysLeft}d left`}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {project.topic_ideas && (
            <div className="card">
              <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 12 }}>Topic Ideas</h3>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {project.topic_ideas.map((idea: string, i: number) => (
                  <div key={i} style={{ padding: "8px 14px", borderRadius: 8, background: "var(--bg-tertiary)", fontSize: 13, color: "var(--text-secondary)", border: "1px solid var(--border)" }}>
                    {idea}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {tab === "assessment" && (
        <div className="card" style={{ maxWidth: 600 }}>
          <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 16 }}>Assessment Breakdown</h3>
          <table className="assessment-table">
            <thead>
              <tr><th>Component</th><th>Weight</th></tr>
            </thead>
            <tbody>
              <tr>
                <td style={{ fontWeight: 600 }}>Continuous Assessment</td>
                <td style={{ fontWeight: 600 }}>{course.assessment.continuous.weight}%</td>
              </tr>
              {course.assessment.continuous.components.map((comp, i) => (
                <tr key={i}>
                  <td style={{ paddingLeft: 24 }}>{comp.name}</td>
                  <td>{typeof comp.weight === "number" ? `${comp.weight}%` : comp.weight}</td>
                </tr>
              ))}
              <tr>
                <td style={{ fontWeight: 600 }}>Final Examination</td>
                <td style={{ fontWeight: 600 }}>{course.assessment.exam.weight}%</td>
              </tr>
              <tr>
                <td colSpan={2} style={{ color: "var(--accent-rose)", fontSize: 12 }}>
                  {course.assessment.exam.note}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {tab === "weeks" && (
        <div>
          {course.weeks.map((w) => {
            const isExpanded = expandedWeek === w.week;
            return (
              <div key={w.week} className="week-item">
                <div className="week-header" onClick={() => setExpandedWeek(isExpanded ? null : w.week)}>
                  {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                  <div className="week-number" style={w.status === "missed" ? { background: "rgba(244,63,94,0.15)", color: "var(--accent-rose)" } : {}}>
                    {w.week}
                  </div>
                  <div className="week-info">
                    <div className="week-topic">{w.topic}</div>
                    <div className="week-date">
                      {new Date(w.date + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })}
                    </div>
                  </div>
                  <div className="week-badges">
                    {w.has_lab && <span className="week-badge lab">LAB</span>}
                    {w.has_quiz && <span className="week-badge quiz">QUIZ</span>}
                    {w.status === "missed" && <span className="week-badge missed">MISSED</span>}
                    {w.status === "holiday" && <span className="week-badge holiday">HOLIDAY</span>}
                  </div>
                </div>
                {isExpanded && (
                  <div className="week-content">
                    <div className="week-details">{w.details}</div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
