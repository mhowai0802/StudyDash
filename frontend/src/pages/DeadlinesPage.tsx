import { useEffect, useState } from "react";
import { Check, Calendar, AlertTriangle } from "lucide-react";
import { getDeadlines, toggleDeadline } from "../api/client";
import type { Deadline } from "../types";

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

  const filtered = deadlines.filter((d) => {
    if (filter === "pending") return !d.done;
    if (filter === "done") return d.done;
    return true;
  });

  const overdueCount = deadlines.filter((d) => !d.done && d.date < today).length;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Deadlines</h1>
        <p className="page-subtitle">
          Track all your assessments and submissions across courses.
        </p>
      </div>

      {overdueCount > 0 && (
        <div
          className="card"
          style={{
            marginBottom: 20,
            display: "flex",
            alignItems: "center",
            gap: 12,
            background: "rgba(244,63,94,0.08)",
            borderColor: "rgba(244,63,94,0.2)",
          }}
        >
          <AlertTriangle size={20} color="var(--accent-rose)" />
          <div>
            <div style={{ fontWeight: 600, color: "var(--accent-rose)" }}>
              {overdueCount} overdue deadline{overdueCount > 1 ? "s" : ""}
            </div>
            <div style={{ fontSize: 13, color: "var(--text-secondary)" }}>
              Take action now to minimize grade impact.
            </div>
          </div>
        </div>
      )}

      <div className="tabs">
        <button className={`tab ${filter === "all" ? "active" : ""}`} onClick={() => setFilter("all")}>
          All ({deadlines.length})
        </button>
        <button className={`tab ${filter === "pending" ? "active" : ""}`} onClick={() => setFilter("pending")}>
          Pending ({deadlines.filter((d) => !d.done).length})
        </button>
        <button className={`tab ${filter === "done" ? "active" : ""}`} onClick={() => setFilter("done")}>
          Done ({deadlines.filter((d) => d.done).length})
        </button>
      </div>

      <div className="card">
        {filtered.map((d) => {
          const daysAway = Math.ceil(
            (new Date(d.date + "T00:00:00").getTime() - new Date().getTime()) / 86400000
          );
          const courseColors: Record<string, string> = {
            nlp: "#6366f1",
            cvpr: "#f59e0b",
            "it-forum": "#10b981",
          };
          return (
            <div key={d.id} className="deadline-item">
              <div
                className={`deadline-checkbox ${d.done ? "done" : ""}`}
                onClick={() => handleToggle(d.id)}
              >
                {d.done && <Check size={12} color="white" />}
              </div>
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: courseColors[d.course_id] || "var(--text-muted)",
                  flexShrink: 0,
                }}
              />
              <div className="deadline-info">
                <div className={`deadline-title ${d.done ? "done" : ""}`}>
                  {d.title}
                </div>
                <div className="deadline-meta">
                  <span>
                    <Calendar size={12} style={{ verticalAlign: "middle", marginRight: 2 }} />
                    {new Date(d.date + "T00:00:00").toLocaleDateString("en-GB", {
                      weekday: "short",
                      day: "numeric",
                      month: "short",
                      year: "numeric",
                    })}
                  </span>
                  <span>
                    {daysAway < 0
                      ? `${Math.abs(daysAway)} days overdue`
                      : daysAway === 0
                      ? "Today"
                      : `${daysAway} days left`}
                  </span>
                  <span style={{ fontWeight: 600 }}>{d.weight}</span>
                  <span style={{ textTransform: "capitalize" }}>{d.type}</span>
                </div>
              </div>
              {d.urgency && !d.done && (
                <span className={`urgency-badge urgency-${d.urgency}`}>
                  {d.urgency === "overdue"
                    ? "OVERDUE"
                    : d.urgency.replace("_", " ").toUpperCase()}
                </span>
              )}
            </div>
          );
        })}
        {filtered.length === 0 && (
          <div style={{ padding: 40, textAlign: "center", color: "var(--text-muted)" }}>
            No deadlines in this category.
          </div>
        )}
      </div>
    </div>
  );
}
