import { useEffect, useState } from "react";
import { Zap, Sparkles, RefreshCw, ChevronDown, ChevronRight } from "lucide-react";
import {
  getCourses,
  getDeadlines,
  getAllMaterials,
  getStudyTasks,
  aiStudyPlan,
} from "../api/client";
import type { Course, Deadline, Material, StudyTask } from "../types";

const SEVEN_DAYS_MS = 7 * 24 * 60 * 60 * 1000;
import ReactMarkdown from "react-markdown";

const COURSE_COLORS: Record<string, string> = {
  nlp: "#6366f1",
  cvpr: "#f59e0b",
};

function CheckboxGroup({
  title,
  items,
  selectedIds,
  onToggle,
  onToggleAll,
  renderLabel,
  defaultOpen = true,
}: {
  title: string;
  items: { id: string }[];
  selectedIds: Set<string>;
  onToggle: (id: string) => void;
  onToggleAll: (select: boolean) => void;
  renderLabel: (item: any) => React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  const allSelected = items.length > 0 && items.every((i) => selectedIds.has(i.id));
  const noneSelected = items.every((i) => !selectedIds.has(i.id));

  return (
    <div className="sp-checkbox-group">
      <div className="sp-group-header" onClick={() => setOpen(!open)}>
        {open ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        <span className="sp-group-title">{title}</span>
        <span className="sp-group-count">
          {items.filter((i) => selectedIds.has(i.id)).length}/{items.length}
        </span>
        <button
          className="sp-toggle-all"
          onClick={(e) => {
            e.stopPropagation();
            onToggleAll(noneSelected || !allSelected);
          }}
        >
          {allSelected ? "Deselect all" : "Select all"}
        </button>
      </div>
      {open && (
        <div className="sp-group-items">
          {items.length === 0 ? (
            <div className="sp-empty">No items</div>
          ) : (
            items.map((item) => (
              <label key={item.id} className="sp-checkbox-row">
                <input
                  type="checkbox"
                  checked={selectedIds.has(item.id)}
                  onChange={() => onToggle(item.id)}
                />
                <span className="sp-checkbox-label">{renderLabel(item)}</span>
              </label>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default function StudyPlanPage() {
  const [plan, setPlan] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [generatedAt, setGeneratedAt] = useState<string>("");

  const [courses, setCourses] = useState<Course[]>([]);
  const [deadlines, setDeadlines] = useState<Deadline[]>([]);
  const [materials, setMaterials] = useState<Material[]>([]);
  const [tasks, setTasks] = useState<StudyTask[]>([]);

  const [selectedDeadlines, setSelectedDeadlines] = useState<Set<string>>(new Set());
  const [selectedMaterials, setSelectedMaterials] = useState<Set<string>>(new Set());
  const [selectedTasks, setSelectedTasks] = useState<Set<string>>(new Set());

  const now = new Date();
  const sevenDaysCutoff = new Date(now.getTime() + SEVEN_DAYS_MS).toISOString().split("T")[0];

  useEffect(() => {
    const load = async () => {
      const [courseList, deadlineList, materialList, taskResult] = await Promise.all([
        getCourses(),
        getDeadlines(),
        getAllMaterials(),
        getStudyTasks(),
      ]);
      setCourses(courseList);
      setDeadlines(deadlineList);
      setMaterials(materialList);
      setTasks(taskResult.tasks);

      setSelectedDeadlines(new Set(deadlineList.filter((d) => !d.done).map((d) => d.id)));
      setSelectedMaterials(new Set(materialList.filter((m) => !m.completed).map((m) => m.id)));
      const cutoff = new Date(Date.now() + SEVEN_DAYS_MS).toISOString().split("T")[0];
      setSelectedTasks(
        new Set(taskResult.tasks.filter((t) => !t.done && t.date <= cutoff).map((t) => t.id))
      );
    };
    load();
  }, []);

  const toggle = (set: Set<string>, id: string): Set<string> => {
    const next = new Set(set);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    return next;
  };

  const toggleAll = (items: { id: string }[], select: boolean): Set<string> => {
    if (select) return new Set(items.map((i) => i.id));
    return new Set();
  };

  const pendingDeadlines = deadlines.filter((d) => !d.done);
  const pendingMaterials = materials.filter((m) => !m.completed);
  const pendingTasks = tasks.filter((t) => !t.done && t.date <= sevenDaysCutoff);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await aiStudyPlan({
        course_ids: courses.map((c) => c.id),
        deadline_ids: Array.from(selectedDeadlines),
        material_ids: Array.from(selectedMaterials),
        task_ids: Array.from(selectedTasks),
      });
      setPlan(result.plan);
      setGeneratedAt(
        new Date().toLocaleString("en-GB", {
          day: "numeric",
          month: "short",
          year: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        })
      );
    } catch {
      setPlan(
        "Could not generate study plan. Check your API settings and make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const courseName = (courseId: string) =>
    courses.find((c) => c.id === courseId)?.name || courseId;

  return (
    <div style={{ maxWidth: 800, margin: "0 auto" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 20,
        }}
      >
        <div>
          <h1 className="page-title" style={{ marginBottom: 4 }}>
            <Sparkles
              size={22}
              color="var(--accent-indigo)"
              style={{ verticalAlign: "middle", marginRight: 8 }}
            />
            AI Study Plan
          </h1>
          <p style={{ color: "var(--text-secondary)", fontSize: 13, margin: 0 }}>
            Select what to include, then generate a personalized 7-day plan
          </p>
        </div>
        <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
          {loading ? (
            <>
              <span className="spinner" style={{ width: 14, height: 14, borderWidth: 2 }} />
              Generating...
            </>
          ) : plan ? (
            <>
              <RefreshCw size={15} /> Regenerate
            </>
          ) : (
            <>
              <Zap size={15} /> Generate Plan
            </>
          )}
        </button>
      </div>

      <div className="settings-card" style={{ marginBottom: 20 }}>
        <CheckboxGroup
          title="Deadlines"
          items={pendingDeadlines}
          selectedIds={selectedDeadlines}
          onToggle={(id) => setSelectedDeadlines(toggle(selectedDeadlines, id))}
          onToggleAll={(sel) => setSelectedDeadlines(toggleAll(pendingDeadlines, sel))}
          defaultOpen={false}
          renderLabel={(d: Deadline) => (
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: COURSE_COLORS[d.course_id] || "var(--text-muted)",
                  flexShrink: 0,
                }}
              />
              <span>{d.title}</span>
              <span style={{ color: "var(--text-muted)", fontSize: 11 }}>
                {new Date(d.date + "T00:00:00").toLocaleDateString("en-GB", {
                  day: "numeric",
                  month: "short",
                })}
              </span>
            </span>
          )}
        />
        <CheckboxGroup
          title="Materials"
          items={pendingMaterials}
          selectedIds={selectedMaterials}
          onToggle={(id) => setSelectedMaterials(toggle(selectedMaterials, id))}
          onToggleAll={(sel) => setSelectedMaterials(toggleAll(pendingMaterials, sel))}
          defaultOpen={false}
          renderLabel={(m: Material) => (
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: COURSE_COLORS[m.course_id] || "var(--text-muted)",
                  flexShrink: 0,
                }}
              />
              <span>{m.title || m.file_name || "Untitled"}</span>
              <span style={{ color: "var(--text-muted)", fontSize: 11 }}>
                {courseName(m.course_id)}
                {m.week > 0 ? ` W${m.week}` : ""}
              </span>
            </span>
          )}
        />
        <CheckboxGroup
          title="Tasks (next 7 days)"
          items={pendingTasks}
          selectedIds={selectedTasks}
          onToggle={(id) => setSelectedTasks(toggle(selectedTasks, id))}
          onToggleAll={(sel) => setSelectedTasks(toggleAll(pendingTasks, sel))}
          defaultOpen={false}
          renderLabel={(t: StudyTask) => (
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: COURSE_COLORS[t.course_id] || "var(--text-muted)",
                  flexShrink: 0,
                }}
              />
              <span>{t.title}</span>
              <span style={{ color: "var(--text-muted)", fontSize: 11 }}>
                {new Date(t.date + "T00:00:00").toLocaleDateString("en-GB", {
                  day: "numeric",
                  month: "short",
                })}{" "}
                | {t.hours}h
              </span>
            </span>
          )}
        />
      </div>

      {loading && (
        <div className="settings-card" style={{ textAlign: "center", padding: "48px 24px" }}>
          <span
            className="spinner"
            style={{ width: 28, height: 28, borderWidth: 3, marginBottom: 16 }}
          />
          <p style={{ color: "var(--text-secondary)", fontSize: 14, margin: 0 }}>
            Analyzing your selections and generating plan...
          </p>
        </div>
      )}

      {plan && !loading && (
        <div className="settings-card">
          {generatedAt && (
            <div style={{ fontSize: 11, color: "var(--text-muted)", marginBottom: 12 }}>
              Generated {generatedAt}
            </div>
          )}
          <div className="ai-content">
            <ReactMarkdown>{plan}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}
