import { useEffect, useState } from "react";
import { Check, AlertTriangle } from "lucide-react";
import { getDeadlines, toggleDeadline } from "../api/client";
import type { Deadline } from "../types";

const COURSE_NAMES: Record<string, string> = {
  nlp: "NLP & LLM",
  cvpr: "Computer Vision",
  "it-forum": "IT Forum",
};

const COURSE_COLORS: Record<string, string> = {
  nlp: "#6366f1",
  cvpr: "#f59e0b",
  "it-forum": "#10b981",
};

export default function DeadlinesPage() {
  const [deadlines, setDeadlines] = useState<Deadline[]>([]);
  const [filter, setFilter] = useState<"all" | "pending" | "done">("all");

  const reload = () => getDeadlines().then(setDeadlines);
  useEffect(() => { reload(); }, []);

  const handleToggle = async (id: string) => {
    await toggleDeadline(id);
    reload();
  };

  const today = new Date().toISOString().split("T")[0];

  const filtered = deadlines
    .filter((d) => {
      if (filter === "pending") return !d.done;
      if (filter === "done") return d.done;
      return true;
    })
    .sort((a, b) => a.date.localeCompare(b.date));

  const overdueCount = deadlines.filter((d) => !d.done && d.date < today).length;

  const formatDate = (dateStr: string) =>
    new Date(dateStr + "T00:00:00").toLocaleDateString("en-GB", {
      weekday: "short", day: "numeric", month: "short", year: "numeric",
    });

  const getDaysLabel = (dateStr: string) => {
    const days = Math.ceil(
      (new Date(dateStr + "T00:00:00").getTime() - new Date().getTime()) / 86400000
    );
    if (days < 0) return `${Math.abs(days)}d overdue`;
    if (days === 0) return "Today";
    return `${days}d left`;
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Deadlines</h1>
        <p className="page-subtitle">Track all your assessments and submissions across courses.</p>
      </div>

      {overdueCount > 0 && (
        <div className="card" style={{ marginBottom: 20, display: "flex", alignItems: "center", gap: 12, background: "rgba(244,63,94,0.08)", borderColor: "rgba(244,63,94,0.2)" }}>
          <AlertTriangle size={20} color="var(--accent-rose)" />
          <div>
            <div style={{ fontWeight: 600, color: "var(--accent-rose)" }}>{overdueCount} overdue deadline{overdueCount > 1 ? "s" : ""}</div>
            <div style={{ fontSize: 13, color: "var(--text-secondary)" }}>Take action now to minimize grade impact.</div>
          </div>
        </div>
      )}

      <div className="tabs">
        <button className={`tab ${filter === "all" ? "active" : ""}`} onClick={() => setFilter("all")}>All ({deadlines.length})</button>
        <button className={`tab ${filter === "pending" ? "active" : ""}`} onClick={() => setFilter("pending")}>Pending ({deadlines.filter((d) => !d.done).length})</button>
        <button className={`tab ${filter === "done" ? "active" : ""}`} onClick={() => setFilter("done")}>Done ({deadlines.filter((d) => d.done).length})</button>
      </div>

      <div className="card" style={{ padding: 0, overflow: "auto" }}>
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ width: 40 }} />
              <th>Title</th>
              <th>Course</th>
              <th>Date</th>
              <th>Status</th>
              <th>Weight</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={7} style={{ textAlign: "center", padding: 40, color: "var(--text-muted)" }}>No deadlines in this category.</td></tr>
            ) : (
              filtered.map((d) => {
                const overdue = !d.done && d.date < today;
                return (
                  <tr key={d.id} style={{ opacity: d.done ? 0.55 : 1 }}>
                    <td>
                      <div className={`deadline-checkbox ${d.done ? "done" : ""}`} onClick={() => handleToggle(d.id)}>
                        {d.done && <Check size={12} color="white" />}
                      </div>
                    </td>
                    <td>
                      <span className={d.done ? "line-through" : ""}>{d.title}</span>
                    </td>
                    <td>
                      <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
                        <span style={{ width: 8, height: 8, borderRadius: "50%", background: COURSE_COLORS[d.course_id] || "var(--text-muted)", flexShrink: 0 }} />
                        {COURSE_NAMES[d.course_id] || d.course_id}
                      </span>
                    </td>
                    <td style={{ whiteSpace: "nowrap" }}>{formatDate(d.date)}</td>
                    <td>
                      {d.done ? (
                        <span className="status-badge status-done">Done</span>
                      ) : overdue ? (
                        <span className="status-badge status-overdue">{getDaysLabel(d.date)}</span>
                      ) : (
                        <span className="status-badge status-upcoming">{getDaysLabel(d.date)}</span>
                      )}
                    </td>
                    <td style={{ fontWeight: 600, fontSize: 12 }}>{d.weight}</td>
                    <td style={{ textTransform: "capitalize", fontSize: 12 }}>{d.type}</td>
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
