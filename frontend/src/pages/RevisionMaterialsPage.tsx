import { useEffect, useState } from "react";
import { Check, AlertTriangle } from "lucide-react";
import { getCourses, getStudyTasks, toggleStudyTask } from "../api/client";
import type { Course, StudyTask } from "../types";

const COURSE_COLORS: Record<string, string> = {
  nlp: "#6366f1",
  cvpr: "#f59e0b",
  "it-forum": "#10b981",
};

type TabType = "all" | "overdue" | "in_progress" | "done";

export default function RevisionMaterialsPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [studyTasks, setStudyTasks] = useState<StudyTask[]>([]);
  const [tab, setTab] = useState<TabType>("all");

  const loadData = async () => {
    const [courseList, taskResult] = await Promise.all([
      getCourses(), getStudyTasks(),
    ]);
    setCourses(courseList);
    setStudyTasks(taskResult.tasks);
  };

  useEffect(() => { loadData(); }, []);

  const today = new Date().toISOString().split("T")[0];

  const courseNameMap: Record<string, string> = {};
  courses.forEach((c) => { courseNameMap[c.id] = c.name; });

  const sorted = [...studyTasks].sort((a, b) => a.date.localeCompare(b.date));

  const overdueCount = sorted.filter((t) => !t.done && t.date < today).length;
  const inProgressCount = sorted.filter((t) => !t.done && t.date >= today).length;
  const doneCount = sorted.filter((t) => t.done).length;

  const filtered = sorted.filter((t) => {
    if (tab === "overdue") return !t.done && t.date < today;
    if (tab === "in_progress") return !t.done && t.date >= today;
    if (tab === "done") return t.done;
    return true;
  });

  const handleToggleTask = async (id: string) => {
    await toggleStudyTask(id);
    loadData();
  };

  const formatDate = (dateStr: string) =>
    new Date(dateStr + "T00:00:00").toLocaleDateString("en-GB", {
      weekday: "short", day: "numeric", month: "short",
    });

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Revision</h1>
        <p className="page-subtitle">All study tasks in one place.</p>
      </div>

      <div className="tabs">
        <button className={`tab ${tab === "all" ? "active" : ""}`} onClick={() => setTab("all")}>All ({sorted.length})</button>
        <button className={`tab ${tab === "overdue" ? "active" : ""}`} onClick={() => setTab("overdue")}>Overdue ({overdueCount})</button>
        <button className={`tab ${tab === "in_progress" ? "active" : ""}`} onClick={() => setTab("in_progress")}>In Progress ({inProgressCount})</button>
        <button className={`tab ${tab === "done" ? "active" : ""}`} onClick={() => setTab("done")}>Done ({doneCount})</button>
      </div>

      <div className="card" style={{ padding: 0, overflow: "auto" }}>
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ width: 40 }} />
              <th>Title</th>
              <th>Course</th>
              <th>Date</th>
              <th>Type</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={6} style={{ textAlign: "center", padding: 40, color: "var(--text-muted)" }}>No items in this category.</td></tr>
            ) : (
              filtered.map((t) => {
                const overdue = !t.done && t.date < today;
                const daysOverdue = overdue
                  ? Math.ceil((new Date().getTime() - new Date(t.date + "T00:00:00").getTime()) / 86400000)
                  : 0;
                return (
                  <tr key={t.id} style={{ opacity: t.done ? 0.55 : 1 }}>
                    <td>
                      <div className={`deadline-checkbox ${t.done ? "done" : ""}`} onClick={() => handleToggleTask(t.id)}>
                        {t.done && <Check size={12} color="white" />}
                      </div>
                    </td>
                    <td>
                      <span className={t.done ? "line-through" : ""}>{t.title}</span>
                      {t.hours > 0 && <span style={{ marginLeft: 8, fontSize: 11, color: "var(--text-muted)" }}>{t.hours}h</span>}
                    </td>
                    <td>
                      <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
                        <span style={{ width: 8, height: 8, borderRadius: "50%", background: COURSE_COLORS[t.course_id] || "var(--text-muted)", flexShrink: 0 }} />
                        {courseNameMap[t.course_id] || t.course_id || "—"}
                      </span>
                    </td>
                    <td style={{ whiteSpace: "nowrap" }}>{formatDate(t.date)}</td>
                    <td style={{ textTransform: "capitalize", fontSize: 12 }}>{t.category.replace("-", " ")}</td>
                    <td>
                      {t.done ? (
                        <span className="status-badge status-done">Done</span>
                      ) : overdue ? (
                        <span className="status-badge status-overdue"><AlertTriangle size={10} /> {daysOverdue}d overdue</span>
                      ) : (
                        <span className="status-badge status-upcoming">Upcoming</span>
                      )}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
