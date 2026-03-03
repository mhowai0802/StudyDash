import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import {
  BookOpen,
  Calendar,
  ArrowRight,
  CheckCircle,
  Clock,
} from "lucide-react";
import {
  getCourses,
  getCourse,
  getDeadlines,
  getStudyTasks,
  toggleStudyTask,
  addStudyTask,
  deleteStudyTask,
  updateStudyTask,
} from "../api/client";
import type { Course, Deadline, StudyTask, TaskCategories, Material } from "../types";
import ProgressRing from "../components/ProgressRing";
import MonthlyCalendar from "../components/MonthlyCalendar";


export default function Dashboard() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [deadlines, setDeadlines] = useState<Deadline[]>([]);
  const [studyTasks, setStudyTasks] = useState<StudyTask[]>([]);
  const [taskCategories, setTaskCategories] = useState<TaskCategories>({});
  const [allMaterials, setAllMaterials] = useState<Material[]>([]);
  const nav = useNavigate();

  const reload = useCallback(() => {
    getCourses().then((data) => {
      setCourses(data);
      // Collect materials from all courses
      Promise.all(data.map((c) => getCourse(c.id))).then((details) => {
        const mats = details.flatMap((d) => d.materials || []);
        setAllMaterials(mats);
      });
    });
    getDeadlines().then(setDeadlines);
    getStudyTasks().then((data) => {
      setStudyTasks(data.tasks);
      setTaskCategories(data.categories);
    });
  }, []);

  useEffect(() => { reload(); }, [reload]);

  const handleToggleTask = async (id: string) => {
    await toggleStudyTask(id);
    reload();
  };

  const handleAddTask = async (task: { date: string; course_id: string; title: string; hours: number; category: string }) => {
    await addStudyTask(task);
    reload();
  };

  const handleDeleteTask = async (id: string) => {
    await deleteStudyTask(id);
    reload();
  };

  const handleUpdateTask = async (id: string, updates: Partial<{ date: string; title: string; hours: number; category: string; course_id: string }>) => {
    await updateStudyTask(id, updates);
    reload();
  };

  const todayKey = new Date().toISOString().split("T")[0];
  const todayTasks = studyTasks.filter((t) => t.date === todayKey);
  const todayDone = todayTasks.filter((t) => t.done).length;
  const todayHours = todayTasks.reduce((s, t) => s + t.hours, 0);

  return (
    <div className="dash">
      {/* Header with inline stats */}
      <div className="dash-header">
        <div className="dash-header-left">
          <h1 className="dash-title">Dashboard</h1>
          <p className="dash-subtitle">Your study command center</p>
        </div>
        <div className="dash-stats-row">
          <div className="dash-stat">
            <CheckCircle size={16} color="#22d3ee" />
            <span className="dash-stat-value">{todayDone}/{todayTasks.length}</span>
            <span className="dash-stat-label">Today</span>
          </div>
          {todayHours > 0 && (
            <div className="dash-stat">
              <Clock size={16} color="var(--accent-amber)" />
              <span className="dash-stat-value">{todayHours}h</span>
              <span className="dash-stat-label">Planned</span>
            </div>
          )}
        </div>
      </div>

      {/* Full-width Calendar */}
      <section className="dash-calendar">
        <MonthlyCalendar
          courses={courses}
          deadlines={deadlines}
          studyTasks={studyTasks}
          taskCategories={taskCategories}
          materials={allMaterials}
          onToggleTask={handleToggleTask}
          onAddTask={handleAddTask}
          onDeleteTask={handleDeleteTask}
          onUpdateTask={handleUpdateTask}
        />
      </section>

      {/* Courses strip */}
      <section className="dash-section">
        <div className="dash-section-header">
          <h2 className="dash-section-title">Courses</h2>
          <button className="btn btn-sm btn-secondary" onClick={() => nav("/deadlines")}>
            <Calendar size={14} /> Deadlines <ArrowRight size={14} />
          </button>
        </div>
        <div className="dash-courses">
          {courses.map((c) => {
            const progress =
              c.total_materials && c.completed_materials != null
                ? Math.round((c.completed_materials / c.total_materials) * 100)
                : 0;
            return (
              <div
                key={c.id}
                className="dash-course-card"
                onClick={() => nav(`/course/${c.id}`)}
              >
                <div className="dash-course-accent" style={{ background: c.color }} />
                <div className="dash-course-body">
                  <div className="dash-course-top">
                    <div>
                      <div className="dash-course-code">{c.code}</div>
                      <div className="dash-course-schedule">{c.schedule}</div>
                    </div>
                    <ProgressRing progress={progress} size={44} strokeWidth={4} color={c.color} />
                  </div>
                  <div className="dash-course-bottom">
                    <span><strong>{c.completed_materials || 0}</strong>/{c.total_materials || 0} materials</span>
                    <span><strong>{c.total_weeks}</strong> weeks</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

    </div>
  );
}
