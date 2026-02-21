import { useState, useMemo } from "react";
import { ChevronLeft, ChevronRight, Check, Plus, Trash2, Clock } from "lucide-react";
import type { Course, Deadline, StudyTask, TaskCategories } from "../types";

interface CalendarEvent {
  id: string;
  title: string;
  type: "lecture" | "lab" | "quiz" | "deadline" | "talk" | "project" | "exam" | "holiday";
  courseId: string;
  color: string;
}

interface MonthlyCalendarProps {
  courses: Course[];
  deadlines: Deadline[];
  studyTasks: StudyTask[];
  taskCategories: TaskCategories;
  onToggleTask: (id: string) => void;
  onAddTask: (task: { date: string; course_id: string; title: string; hours: number; category: string }) => void;
  onDeleteTask: (id: string) => void;
}

const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

const EVENT_STYLES: Record<string, { bg: string; border: string }> = {
  lecture: { bg: "rgba(99,102,241,0.15)", border: "#6366f1" },
  lab: { bg: "rgba(16,185,129,0.15)", border: "#10b981" },
  quiz: { bg: "rgba(244,63,94,0.18)", border: "#f43f5e" },
  deadline: { bg: "rgba(245,158,11,0.15)", border: "#f59e0b" },
  talk: { bg: "rgba(16,185,129,0.12)", border: "#10b981" },
  project: { bg: "rgba(168,85,247,0.15)", border: "#a855f7" },
  exam: { bg: "rgba(244,63,94,0.2)", border: "#f43f5e" },
  holiday: { bg: "rgba(245,158,11,0.08)", border: "#f59e0b" },
};

const COURSE_COLORS: Record<string, string> = {
  nlp: "#6366f1",
  cvpr: "#f59e0b",
  "it-forum": "#10b981",
};

function getMonthDays(year: number, month: number) {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  let startWeekday = firstDay.getDay() - 1;
  if (startWeekday < 0) startWeekday = 6;

  const days: { date: Date; isCurrentMonth: boolean }[] = [];

  for (let i = startWeekday - 1; i >= 0; i--) {
    const d = new Date(year, month, -i);
    days.push({ date: d, isCurrentMonth: false });
  }

  for (let d = 1; d <= lastDay.getDate(); d++) {
    days.push({ date: new Date(year, month, d), isCurrentMonth: true });
  }

  const remaining = 7 - (days.length % 7);
  if (remaining < 7) {
    for (let i = 1; i <= remaining; i++) {
      days.push({ date: new Date(year, month + 1, i), isCurrentMonth: false });
    }
  }

  return days;
}

function formatDateKey(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export default function MonthlyCalendar({
  courses,
  deadlines,
  studyTasks,
  taskCategories,
  onToggleTask,
  onAddTask,
  onDeleteTask,
}: MonthlyCalendarProps) {
  const today = new Date();
  const [currentYear, setCurrentYear] = useState(today.getFullYear());
  const [currentMonth, setCurrentMonth] = useState(today.getMonth());
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newCourse, setNewCourse] = useState("");
  const [newHours, setNewHours] = useState("1");
  const [newCategory, setNewCategory] = useState("review");

  const courseColorMap = useMemo(() => {
    const m: Record<string, string> = {};
    courses.forEach((c) => { m[c.id] = c.color; });
    return m;
  }, [courses]);

  const eventsMap = useMemo(() => {
    const map: Record<string, CalendarEvent[]> = {};

    const addEvent = (dateStr: string, event: CalendarEvent) => {
      if (!map[dateStr]) map[dateStr] = [];
      map[dateStr].push(event);
    };

    courses.forEach((course) => {
      course.weeks.forEach((w) => {
        const dateStr = w.date;
        if (w.status === "holiday") {
          addEvent(dateStr, { id: `${course.id}-w${w.week}-holiday`, title: `${course.code}: Holiday`, type: "holiday", courseId: course.id, color: courseColorMap[course.id] || "#6366f1" });
          return;
        }
        addEvent(dateStr, { id: `${course.id}-w${w.week}-lecture`, title: `${course.code}: ${w.topic}`, type: "lecture", courseId: course.id, color: courseColorMap[course.id] || "#6366f1" });
        if (w.has_lab) addEvent(dateStr, { id: `${course.id}-w${w.week}-lab`, title: `${course.code}: ${w.lab_name || "Lab"}`, type: "lab", courseId: course.id, color: courseColorMap[course.id] || "#6366f1" });
        if (w.has_quiz) addEvent(dateStr, { id: `${course.id}-w${w.week}-quiz`, title: `${course.code}: ${w.quiz_name || "Quiz"}`, type: "quiz", courseId: course.id, color: courseColorMap[course.id] || "#6366f1" });
      });
    });

    deadlines.forEach((d) => {
      let type: CalendarEvent["type"] = "deadline";
      if (d.type === "exam") type = "exam";
      else if (d.type === "project") type = "project";
      else if (d.type === "talk") type = "talk";
      addEvent(d.date, { id: `dl-${d.id}`, title: d.title, type, courseId: d.course_id, color: courseColorMap[d.course_id] || "#f59e0b" });
    });

    return map;
  }, [courses, deadlines, courseColorMap]);

  const tasksMap = useMemo(() => {
    const map: Record<string, StudyTask[]> = {};
    studyTasks.forEach((t) => {
      if (!map[t.date]) map[t.date] = [];
      map[t.date].push(t);
    });
    return map;
  }, [studyTasks]);

  const days = getMonthDays(currentYear, currentMonth);
  const todayKey = formatDateKey(today);
  const monthLabel = new Date(currentYear, currentMonth).toLocaleDateString("en-US", { month: "long", year: "numeric" });

  const prevMonth = () => {
    if (currentMonth === 0) { setCurrentMonth(11); setCurrentYear((y) => y - 1); }
    else setCurrentMonth((m) => m - 1);
    setSelectedDate(null);
    setShowAddForm(false);
  };

  const nextMonth = () => {
    if (currentMonth === 11) { setCurrentMonth(0); setCurrentYear((y) => y + 1); }
    else setCurrentMonth((m) => m + 1);
    setSelectedDate(null);
    setShowAddForm(false);
  };

  const goToday = () => {
    setCurrentYear(today.getFullYear());
    setCurrentMonth(today.getMonth());
    setSelectedDate(todayKey);
  };

  const handleDayClick = (dateKey: string) => {
    setSelectedDate(dateKey === selectedDate ? null : dateKey);
    setShowAddForm(false);
  };

  const handleAddTask = () => {
    if (!newTitle.trim() || !selectedDate) return;
    onAddTask({ date: selectedDate, course_id: newCourse, title: newTitle.trim(), hours: parseFloat(newHours) || 1, category: newCategory });
    setNewTitle("");
    setNewHours("1");
    setShowAddForm(false);
  };

  const selectedEvents = selectedDate ? eventsMap[selectedDate] || [] : [];
  const selectedTasks = selectedDate ? tasksMap[selectedDate] || [] : [];
  const selectedDayHours = selectedTasks.reduce((sum, t) => sum + t.hours, 0);
  const selectedDayDone = selectedTasks.filter((t) => t.done).length;

  return (
    <div className="calendar-wrapper">
      {/* Header */}
      <div className="calendar-header">
        <div className="calendar-nav">
          <button className="calendar-nav-btn" onClick={prevMonth}><ChevronLeft size={18} /></button>
          <h2 className="calendar-month-label">{monthLabel}</h2>
          <button className="calendar-nav-btn" onClick={nextMonth}><ChevronRight size={18} /></button>
        </div>
        <button className="btn btn-sm btn-secondary" onClick={goToday}>Today</button>
      </div>

      {/* Legend */}
      <div className="calendar-legend">
        {[
          { type: "lecture", label: "Lecture" },
          { type: "lab", label: "Lab" },
          { type: "quiz", label: "Quiz" },
          { type: "deadline", label: "Deadline" },
          { type: "project", label: "Project" },
          { type: "exam", label: "Exam" },
          { type: "holiday", label: "Holiday" },
        ].map((l) => (
          <div key={l.type} className="calendar-legend-item">
            <span className="calendar-legend-dot" style={{ background: EVENT_STYLES[l.type].border }} />
            {l.label}
          </div>
        ))}
        <div style={{ borderLeft: "1px solid var(--border)", height: 16, margin: "0 4px" }} />
        <div className="calendar-legend-item">
          <span className="calendar-legend-dot" style={{ background: "#22d3ee", borderRadius: "50%" }} />
          Study Task
        </div>
      </div>

      {/* Weekday headers */}
      <div className="calendar-grid calendar-grid-header">
        {WEEKDAYS.map((d) => (
          <div key={d} className="calendar-weekday">{d}</div>
        ))}
      </div>

      {/* Day cells */}
      <div className="calendar-grid calendar-grid-days">
        {days.map(({ date, isCurrentMonth }, idx) => {
          const key = formatDateKey(date);
          const isToday = key === todayKey;
          const isSelected = key === selectedDate;
          const dayEvents = eventsMap[key] || [];
          const dayTasks = tasksMap[key] || [];
          const doneCount = dayTasks.filter((t) => t.done).length;
          const totalTasks = dayTasks.length;
          const allItems = [
            ...dayEvents.map((e) => ({ kind: "event" as const, ...e })),
            ...dayTasks.map((t) => ({ kind: "task" as const, ...t })),
          ];

          return (
            <div
              key={idx}
              className={[
                "calendar-day",
                !isCurrentMonth && "calendar-day-outside",
                isToday && "calendar-day-today",
                isSelected && "calendar-day-selected",
                allItems.length > 0 && "calendar-day-has-events",
              ].filter(Boolean).join(" ")}
              onClick={() => handleDayClick(key)}
            >
              <div className="calendar-day-number">
                {isToday ? (
                  <span className="calendar-today-badge">{date.getDate()}</span>
                ) : (
                  date.getDate()
                )}
                {totalTasks > 0 && (
                  <span className="calendar-task-count" style={{ color: doneCount === totalTasks ? "var(--accent-emerald)" : "var(--text-muted)" }}>
                    {doneCount}/{totalTasks}
                  </span>
                )}
              </div>
              {/* Full pills (hidden on mobile via CSS) */}
              <div className="calendar-day-events">
                {dayEvents.slice(0, 2).map((ev) => (
                  <div
                    key={ev.id}
                    className="calendar-event-pill"
                    style={{ background: EVENT_STYLES[ev.type]?.bg, borderLeft: `3px solid ${EVENT_STYLES[ev.type]?.border}` }}
                    title={ev.title}
                  >
                    <span className="calendar-event-pill-text">{ev.title}</span>
                  </div>
                ))}
                {dayTasks.slice(0, 2).map((t) => {
                  const catColor = taskCategories[t.category]?.color || "#22d3ee";
                  return (
                    <div
                      key={t.id}
                      className={`calendar-event-pill calendar-task-pill ${t.done ? "calendar-task-done" : ""}`}
                      style={{ background: `${catColor}15`, borderLeft: `3px solid ${catColor}` }}
                      title={t.title}
                    >
                      <span className="calendar-event-pill-text">{t.title}</span>
                    </div>
                  );
                })}
                {allItems.length > 4 && (
                  <div className="calendar-event-more">+{allItems.length - 4} more</div>
                )}
              </div>
              {/* Compact dot indicators (visible on mobile only) */}
              {(dayEvents.length > 0 || dayTasks.length > 0) && (
                <div className="calendar-day-dots">
                  {dayEvents.slice(0, 4).map((ev) => (
                    <span key={ev.id} className="calendar-dot" style={{ background: EVENT_STYLES[ev.type]?.border }} />
                  ))}
                  {dayTasks.length > 0 && (
                    <span className="calendar-dot" style={{ background: doneCount === totalTasks ? "var(--accent-emerald)" : "#22d3ee" }} />
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Selected day detail panel */}
      {selectedDate && (
        <div className="calendar-detail">
          <div className="calendar-detail-header" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              {new Date(selectedDate + "T00:00:00").toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" })}
              {selectedTasks.length > 0 && (
                <span style={{ marginLeft: 12, fontSize: 13, color: "var(--text-secondary)" }}>
                  <Clock size={12} style={{ verticalAlign: "middle", marginRight: 3 }} />
                  {selectedDayHours}h planned &middot; {selectedDayDone}/{selectedTasks.length} done
                </span>
              )}
            </div>
            <button className="btn btn-sm btn-primary" onClick={() => setShowAddForm(!showAddForm)}>
              <Plus size={14} /> Add Task
            </button>
          </div>

          {/* Add task form */}
          {showAddForm && (
            <div style={{ padding: "12px 0", borderBottom: "1px solid var(--border)" }}>
              <div className="form-row">
                <input className="form-input" placeholder="What do you need to do?" value={newTitle} onChange={(e) => setNewTitle(e.target.value)} style={{ flex: 2 }} />
                <select className="form-select" value={newCourse} onChange={(e) => setNewCourse(e.target.value)}>
                  <option value="">No course</option>
                  <option value="nlp">NLP</option>
                  <option value="cvpr">CVPR</option>
                  <option value="it-forum">IT Forum</option>
                </select>
              </div>
              <div className="form-row">
                <select className="form-select" value={newCategory} onChange={(e) => setNewCategory(e.target.value)}>
                  {Object.entries(taskCategories).map(([k, v]) => (
                    <option key={k} value={k}>{v.label}</option>
                  ))}
                </select>
                <input className="form-input" type="number" min="0.5" step="0.5" value={newHours} onChange={(e) => setNewHours(e.target.value)} style={{ maxWidth: 80 }} placeholder="Hours" />
                <button className="btn btn-primary btn-sm" onClick={handleAddTask}>Add</button>
                <button className="btn btn-secondary btn-sm" onClick={() => setShowAddForm(false)}>Cancel</button>
              </div>
            </div>
          )}

          {/* Course events */}
          {selectedEvents.length > 0 && (
            <div style={{ marginBottom: 16 }}>
              <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.5px", color: "var(--text-muted)", marginBottom: 8, marginTop: 12 }}>
                Course Events
              </div>
              <div className="calendar-detail-list">
                {selectedEvents.map((ev) => {
                  const style = EVENT_STYLES[ev.type];
                  return (
                    <div key={ev.id} className="calendar-detail-item" style={{ background: style?.bg, borderLeft: `4px solid ${style?.border}` }}>
                      <div className="calendar-detail-item-type">{ev.type.toUpperCase()}</div>
                      <div className="calendar-detail-item-title">{ev.title}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Study tasks */}
          <div>
            <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.5px", color: "var(--text-muted)", marginBottom: 8, marginTop: selectedEvents.length > 0 ? 0 : 12 }}>
              Study Tasks {selectedTasks.length > 0 && `(${selectedDayDone}/${selectedTasks.length})`}
            </div>
            {selectedTasks.length === 0 ? (
              <div style={{ fontSize: 13, color: "var(--text-muted)", padding: "8px 0" }}>
                No study tasks planned. Click "Add Task" to create one.
              </div>
            ) : (
              <div className="calendar-detail-list">
                {selectedTasks.map((t) => {
                  const cat = taskCategories[t.category];
                  const catColor = cat?.color || "#22d3ee";
                  const courseColor = COURSE_COLORS[t.course_id] || "var(--text-muted)";
                  return (
                    <div
                      key={t.id}
                      className="calendar-task-detail-item"
                      style={{ borderLeft: `4px solid ${catColor}`, opacity: t.done ? 0.6 : 1 }}
                    >
                      <div
                        className={`calendar-task-check ${t.done ? "done" : ""}`}
                        onClick={(e) => { e.stopPropagation(); onToggleTask(t.id); }}
                        style={{ borderColor: t.done ? "var(--accent-emerald)" : catColor }}
                      >
                        {t.done && <Check size={12} color="white" />}
                      </div>
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div className={`calendar-task-title ${t.done ? "done" : ""}`}>{t.title}</div>
                        <div className="calendar-task-meta">
                          {t.course_id && (
                            <span style={{ display: "inline-flex", alignItems: "center", gap: 4 }}>
                              <span style={{ width: 6, height: 6, borderRadius: "50%", background: courseColor }} />
                              {t.course_id.toUpperCase()}
                            </span>
                          )}
                          <span style={{ color: catColor, fontWeight: 600 }}>{cat?.label || t.category}</span>
                          <span><Clock size={10} style={{ verticalAlign: "middle" }} /> {t.hours}h</span>
                        </div>
                      </div>
                      <button
                        className="calendar-task-delete"
                        onClick={(e) => { e.stopPropagation(); onDeleteTask(t.id); }}
                        title="Delete task"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
