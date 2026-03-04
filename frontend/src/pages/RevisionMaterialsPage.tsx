import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Check,
  FileText,
  Video,
  BookOpen,
  FlaskConical,
  Brain,
  ExternalLink,
  ListTodo,
  AlertTriangle,
} from "lucide-react";
import {
  getCourses,
  getAllMaterials,
  getStudyTasks,
  toggleMaterial,
  toggleStudyTask,
} from "../api/client";
import type { Course, Material, StudyTask } from "../types";

const TYPE_ICONS: Record<string, typeof FileText> = {
  lecture_slides: FileText,
  textbook_chapter: BookOpen,
  video: Video,
  lab_exercise: FlaskConical,
  quiz_prep: Brain,
};

const COURSE_COLORS: Record<string, string> = {
  nlp: "#6366f1",
  cvpr: "#f59e0b",
};

type TabType = "all" | "overdue" | "in_progress" | "done";

type RevisionItem =
  | { type: "task"; data: StudyTask }
  | { type: "material"; data: Material; courseId: string };

export default function RevisionMaterialsPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [materials, setMaterials] = useState<Material[]>([]);
  const [studyTasks, setStudyTasks] = useState<StudyTask[]>([]);
  const [tab, setTab] = useState<TabType>("all");

  const loadData = async () => {
    const [courseList, materialList, taskResult] = await Promise.all([
      getCourses(),
      getAllMaterials(),
      getStudyTasks(),
    ]);
    setCourses(courseList);
    setMaterials(materialList);
    setStudyTasks(taskResult.tasks);
  };

  useEffect(() => {
    loadData();
  }, []);

  const today = new Date().toISOString().split("T")[0];
  const overdueTasks = studyTasks.filter((t) => !t.done && t.date < today);
  const inProgressTasks = studyTasks.filter((t) => !t.done && t.date >= today);
  const doneTasks = studyTasks.filter((t) => t.done);
  const inProgressMaterials = materials.filter((m) => !(m.completed ?? false));
  const doneMaterials = materials.filter((m) => m.completed ?? false);

  const isItemOverdue = (item: RevisionItem) =>
    item.type === "task" && !item.data.done && item.data.date < today;
  const isItemInProgress = (item: RevisionItem) =>
    (item.type === "task" && !item.data.done && item.data.date >= today) ||
    (item.type === "material" && !(item.data.completed ?? false));
  const isItemDone = (item: RevisionItem) =>
    (item.type === "task" && item.data.done) || (item.type === "material" && (item.data.completed ?? false));

  const allRevisionItems: RevisionItem[] = [
    ...studyTasks.map((t) => ({ type: "task" as const, data: t })),
    ...materials.map((m) => ({ type: "material" as const, data: m, courseId: m.course_id })),
  ].sort((a, b) => {
    const getSortKey = (item: RevisionItem) => {
      if (item.type === "task") return item.data.date;
      return "9999-99-99";
    };
    return getSortKey(a).localeCompare(getSortKey(b));
  });

  const handleToggleTask = async (id: string) => {
    await toggleStudyTask(id);
    loadData();
  };

  const handleToggleMaterial = async (id: string) => {
    await toggleMaterial(id);
    loadData();
  };

  const getMaterialUrl = (m: Material, courseId: string) => {
    if (m.file_path) {
      if (m.file_path.startsWith("http")) return m.file_path;
      const filename = m.file_path.split(/[/\\]/).pop();
      return `http://localhost:5001/api/materials/file/${courseId}/${filename}`;
    }
    return m.url || null;
  };

  const filteredRevisionItems = allRevisionItems.filter((item) => {
    if (tab === "overdue") return isItemOverdue(item);
    if (tab === "in_progress") return isItemInProgress(item);
    if (tab === "done") return isItemDone(item);
    return true;
  });

  const renderItems = () => (
    <div className="revision-materials-list">
      {filteredRevisionItems.length === 0 ? (
        <div style={{ padding: 40, textAlign: "center", color: "var(--text-muted)" }}>
          No items in this category.
        </div>
      ) : (
        filteredRevisionItems.map((item) => {
          if (item.type === "task") {
            const t = item.data;
            const overdue = !t.done && t.date < today;
            const daysOverdue = overdue
              ? Math.ceil((new Date().getTime() - new Date(t.date + "T00:00:00").getTime()) / 86400000)
              : 0;
            return (
              <div key={`t-${t.id}`} className="revision-material-item revision-item-task">
                <div
                  className={`material-check ${t.done ? "done" : ""}`}
                  onClick={() => handleToggleTask(t.id)}
                >
                  {t.done && <Check size={12} color="white" />}
                </div>
                <span
                  className="revision-course-dot"
                  style={{ background: COURSE_COLORS[t.course_id] || "var(--text-muted)" }}
                />
                <ListTodo size={14} color="var(--text-muted)" />
                <div className="revision-material-info">
                  <span className={`revision-material-title ${t.done ? "done" : ""}`}>{t.title}</span>
                  <div className="revision-material-meta">
                    <span>
                      {new Date(t.date + "T00:00:00").toLocaleDateString("en-GB", {
                        weekday: "short",
                        day: "numeric",
                        month: "short",
                      })}
                    </span>
                    <span>{t.hours}h</span>
                    <span style={{ textTransform: "capitalize" }}>{t.category}</span>
                  </div>
                </div>
                {overdue && (
                  <span className="revision-status-badge revision-badge-overdue">
                    <AlertTriangle size={10} /> {daysOverdue}d overdue
                  </span>
                )}
                <span className="revision-type-badge revision-badge-task">Task</span>
              </div>
            );
          }

          const m = item.data;
          const Icon = TYPE_ICONS[m.type] || FileText;
          const course = courses.find((c) => c.id === item.courseId);
          const materialUrl = getMaterialUrl(m, item.courseId);

          return (
            <div key={`m-${m.id}`} className="revision-material-item">
              <div
                className={`material-check ${m.completed ? "done" : ""}`}
                onClick={() => handleToggleMaterial(m.id)}
              >
                {m.completed && <Check size={12} color="white" />}
              </div>
              <span
                className="revision-course-dot"
                style={{ background: COURSE_COLORS[item.courseId] || "var(--text-muted)" }}
              />
              <Icon size={14} color="var(--text-muted)" />
              <div className="revision-material-info">
                <span className={`revision-material-title ${m.completed ? "done" : ""}`}>
                  {m.title || m.file_name || "Untitled"}
                </span>
                <div className="revision-material-meta">
                  <Link to={`/course/${item.courseId}`} className="revision-course-link">
                    {course?.name || item.courseId}
                  </Link>
                  {m.week > 0 && <span>Week {m.week}</span>}
                  <span className="revision-material-type">{m.type.replace("_", " ")}</span>
                </div>
              </div>
              {materialUrl && (
                <button
                  className="revision-open-btn"
                  onClick={() => window.open(materialUrl, "_blank")}
                  title="Open"
                >
                  <ExternalLink size={14} />
                </button>
              )}
              <span className="revision-type-badge revision-badge-material">Material</span>
            </div>
          );
        })
      )}
    </div>
  );

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Revision</h1>
        <p className="page-subtitle">
          All revision materials and study tasks in one place.
        </p>
      </div>

      <div className="tabs">
        <button
          className={`tab ${tab === "all" ? "active" : ""}`}
          onClick={() => setTab("all")}
        >
          All ({allRevisionItems.length})
        </button>
        <button
          className={`tab ${tab === "overdue" ? "active" : ""}`}
          onClick={() => setTab("overdue")}
        >
          Overdue ({overdueTasks.length})
        </button>
        <button
          className={`tab ${tab === "in_progress" ? "active" : ""}`}
          onClick={() => setTab("in_progress")}
        >
          In Progress ({inProgressTasks.length + inProgressMaterials.length})
        </button>
        <button
          className={`tab ${tab === "done" ? "active" : ""}`}
          onClick={() => setTab("done")}
        >
          Done ({doneTasks.length + doneMaterials.length})
        </button>
      </div>

      <div className="card">
        {renderItems()}
      </div>
    </div>
  );
}
