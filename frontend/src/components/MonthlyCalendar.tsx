import { useState, useMemo } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Course, Deadline } from "../types";

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
  onEventClick?: (date: string, events: CalendarEvent[]) => void;
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

function getMonthDays(year: number, month: number) {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  // JS getDay: 0=Sun, we want 0=Mon
  let startWeekday = firstDay.getDay() - 1;
  if (startWeekday < 0) startWeekday = 6;

  const days: { date: Date; isCurrentMonth: boolean }[] = [];

  // Previous month padding
  for (let i = startWeekday - 1; i >= 0; i--) {
    const d = new Date(year, month, -i);
    days.push({ date: d, isCurrentMonth: false });
  }

  // Current month days
  for (let d = 1; d <= lastDay.getDate(); d++) {
    days.push({ date: new Date(year, month, d), isCurrentMonth: true });
  }

  // Next month padding to complete last row
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

export default function MonthlyCalendar({ courses, deadlines, onEventClick }: MonthlyCalendarProps) {
  const today = new Date();
  const [currentYear, setCurrentYear] = useState(today.getFullYear());
  const [currentMonth, setCurrentMonth] = useState(today.getMonth());
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  const courseColorMap = useMemo(() => {
    const m: Record<string, string> = {};
    courses.forEach((c) => { m[c.id] = c.color; });
    return m;
  }, [courses]);

  // Build events map keyed by date string
  const eventsMap = useMemo(() => {
    const map: Record<string, CalendarEvent[]> = {};

    const addEvent = (dateStr: string, event: CalendarEvent) => {
      if (!map[dateStr]) map[dateStr] = [];
      map[dateStr].push(event);
    };

    // Course weeks -> lectures, labs, quizzes
    courses.forEach((course) => {
      course.weeks.forEach((w) => {
        const dateStr = w.date;
        if (w.status === "holiday") {
          addEvent(dateStr, {
            id: `${course.id}-w${w.week}-holiday`,
            title: `${course.code}: Holiday`,
            type: "holiday",
            courseId: course.id,
            color: courseColorMap[course.id] || "#6366f1",
          });
          return;
        }

        addEvent(dateStr, {
          id: `${course.id}-w${w.week}-lecture`,
          title: `${course.code}: ${w.topic}`,
          type: "lecture",
          courseId: course.id,
          color: courseColorMap[course.id] || "#6366f1",
        });

        if (w.has_lab) {
          addEvent(dateStr, {
            id: `${course.id}-w${w.week}-lab`,
            title: `${course.code}: ${w.lab_name || "Lab"}`,
            type: "lab",
            courseId: course.id,
            color: courseColorMap[course.id] || "#6366f1",
          });
        }

        if (w.has_quiz) {
          addEvent(dateStr, {
            id: `${course.id}-w${w.week}-quiz`,
            title: `${course.code}: ${w.quiz_name || "Quiz"}`,
            type: "quiz",
            courseId: course.id,
            color: courseColorMap[course.id] || "#6366f1",
          });
        }
      });
    });

    // Deadlines
    deadlines.forEach((d) => {
      let type: CalendarEvent["type"] = "deadline";
      if (d.type === "exam") type = "exam";
      else if (d.type === "project") type = "project";
      else if (d.type === "talk") type = "talk";

      addEvent(d.date, {
        id: `dl-${d.id}`,
        title: d.title,
        type,
        courseId: d.course_id,
        color: courseColorMap[d.course_id] || "#f59e0b",
      });
    });

    return map;
  }, [courses, deadlines, courseColorMap]);

  const days = getMonthDays(currentYear, currentMonth);
  const todayKey = formatDateKey(today);
  const monthLabel = new Date(currentYear, currentMonth).toLocaleDateString("en-US", {
    month: "long",
    year: "numeric",
  });

  const prevMonth = () => {
    if (currentMonth === 0) { setCurrentMonth(11); setCurrentYear((y) => y - 1); }
    else setCurrentMonth((m) => m - 1);
    setSelectedDate(null);
  };

  const nextMonth = () => {
    if (currentMonth === 11) { setCurrentMonth(0); setCurrentYear((y) => y + 1); }
    else setCurrentMonth((m) => m + 1);
    setSelectedDate(null);
  };

  const goToday = () => {
    setCurrentYear(today.getFullYear());
    setCurrentMonth(today.getMonth());
    setSelectedDate(todayKey);
  };

  const handleDayClick = (dateKey: string) => {
    setSelectedDate(dateKey === selectedDate ? null : dateKey);
    if (onEventClick && eventsMap[dateKey]) {
      onEventClick(dateKey, eventsMap[dateKey]);
    }
  };

  const selectedEvents = selectedDate ? eventsMap[selectedDate] || [] : [];

  return (
    <div className="calendar-wrapper">
      {/* Header */}
      <div className="calendar-header">
        <div className="calendar-nav">
          <button className="calendar-nav-btn" onClick={prevMonth}>
            <ChevronLeft size={18} />
          </button>
          <h2 className="calendar-month-label">{monthLabel}</h2>
          <button className="calendar-nav-btn" onClick={nextMonth}>
            <ChevronRight size={18} />
          </button>
        </div>
        <button className="btn btn-sm btn-secondary" onClick={goToday}>
          Today
        </button>
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
            <span
              className="calendar-legend-dot"
              style={{ background: EVENT_STYLES[l.type].border }}
            />
            {l.label}
          </div>
        ))}
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

          return (
            <div
              key={idx}
              className={[
                "calendar-day",
                !isCurrentMonth && "calendar-day-outside",
                isToday && "calendar-day-today",
                isSelected && "calendar-day-selected",
                dayEvents.length > 0 && "calendar-day-has-events",
              ]
                .filter(Boolean)
                .join(" ")}
              onClick={() => handleDayClick(key)}
            >
              <div className="calendar-day-number">
                {isToday ? (
                  <span className="calendar-today-badge">{date.getDate()}</span>
                ) : (
                  date.getDate()
                )}
              </div>
              <div className="calendar-day-events">
                {dayEvents.slice(0, 3).map((ev) => (
                  <div
                    key={ev.id}
                    className="calendar-event-pill"
                    style={{
                      background: EVENT_STYLES[ev.type]?.bg,
                      borderLeft: `3px solid ${EVENT_STYLES[ev.type]?.border}`,
                    }}
                    title={ev.title}
                  >
                    <span className="calendar-event-pill-text">{ev.title}</span>
                  </div>
                ))}
                {dayEvents.length > 3 && (
                  <div className="calendar-event-more">+{dayEvents.length - 3} more</div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected day detail panel */}
      {selectedDate && (
        <div className="calendar-detail">
          <div className="calendar-detail-header">
            {new Date(selectedDate + "T00:00:00").toLocaleDateString("en-GB", {
              weekday: "long",
              day: "numeric",
              month: "long",
              year: "numeric",
            })}
          </div>
          {selectedEvents.length === 0 ? (
            <div className="calendar-detail-empty">No events on this day.</div>
          ) : (
            <div className="calendar-detail-list">
              {selectedEvents.map((ev) => {
                const style = EVENT_STYLES[ev.type];
                return (
                  <div
                    key={ev.id}
                    className="calendar-detail-item"
                    style={{ background: style?.bg, borderLeft: `4px solid ${style?.border}` }}
                  >
                    <div className="calendar-detail-item-type">{ev.type.toUpperCase()}</div>
                    <div className="calendar-detail-item-title">{ev.title}</div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
