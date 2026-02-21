import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import {
  BookOpen,
  Calendar,
  Trophy,
  Zap,
  ArrowRight,
  Sparkles,
  CheckCircle,
  Clock,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import {
  getCourses,
  getDeadlines,
  getStats,
  getStudyTasks,
  toggleStudyTask,
  addStudyTask,
  deleteStudyTask,
  aiStudyPlan,
} from "../api/client";
import type { Course, Deadline, Stats, StudyTask, TaskCategories } from "../types";
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
  const [studyTasks, setStudyTasks] = useState<StudyTask[]>([]);
  const [taskCategories, setTaskCategories] = useState<TaskCategories>({});
  const [studyPlan, setStudyPlan] = useState<string>("");
  const [loadingPlan, setLoadingPlan] = useState(false);
  const [showAIPlan, setShowAIPlan] = useState(false);
  const nav = useNavigate();

  const reload = useCallback(() => {
    getCourses().then(setCourses);
    getDeadlines().then(setDeadlines);
    getStats().then(setStats);
    getStudyTasks().then((data) => {
      setStudyTasks(data.tasks);
      setTaskCategories(data.categories);
    });
  }, []);

  useEffect(() => { reload(); }, [reload]);

  const handleToggleTask = async (id: string) => {
    await toggleStudyTask(id);
    reload();
    onStatsUpdate();
  };

  const handleAddTask = async (task: { date: string; course_id: string; title: string; hours: number; category: string }) => {
    await addStudyTask(task);
    reload();
  };

  const handleDeleteTask = async (id: string) => {
    await deleteStudyTask(id);
    reload();
  };

  const handleGeneratePlan = async () => {
    setLoadingPlan(true);
    setShowAIPlan(true);
    try {
      const result = await aiStudyPlan();
      setStudyPlan(result.plan);
    } catch {
      setStudyPlan("Could not generate study plan. Make sure the backend is running.");
    }
    setLoadingPlan(false);
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
          {stats && (
            <div className="dash-stat">
              <Trophy size={16} color="var(--accent-indigo)" />
              <span className="dash-stat-value">{stats.xp}</span>
              <span className="dash-stat-label">XP</span>
            </div>
          )}
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
          {stats && (
            <div className="dash-stat">
              <BookOpen size={16} color="var(--accent-emerald)" />
              <span className="dash-stat-value">{stats.completed_materials}/{stats.total_materials}</span>
              <span className="dash-stat-label">Materials</span>
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
          onToggleTask={handleToggleTask}
          onAddTask={handleAddTask}
          onDeleteTask={handleDeleteTask}
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

      {/* AI Study Plan - collapsible */}
      <section className="dash-section">
        <div className="dash-ai-bar" onClick={() => !studyPlan && !loadingPlan ? handleGeneratePlan() : setShowAIPlan(!showAIPlan)}>
          <div className="dash-ai-bar-left">
            <Sparkles size={18} color="var(--accent-indigo)" />
            <span className="dash-ai-bar-title">AI Study Plan</span>
            {!studyPlan && !loadingPlan && (
              <span className="dash-ai-bar-hint">Click to generate a personalized plan</span>
            )}
          </div>
          <div className="dash-ai-bar-right">
            {!studyPlan && !loadingPlan && (
              <button className="btn btn-sm btn-primary" onClick={(e) => { e.stopPropagation(); handleGeneratePlan(); }}>
                <Zap size={14} /> Generate
              </button>
            )}
            {loadingPlan && (
              <span className="dash-ai-loading">
                <span className="spinner" style={{ width: 14, height: 14, borderWidth: 2, marginRight: 6 }} />
                Generating...
              </span>
            )}
            {studyPlan && !loadingPlan && (
              <>
                <button className="btn btn-sm btn-secondary" onClick={(e) => { e.stopPropagation(); handleGeneratePlan(); }}>
                  <Zap size={14} /> Regenerate
                </button>
                {showAIPlan ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
              </>
            )}
          </div>
        </div>
        {showAIPlan && studyPlan && (
          <div className="dash-ai-content">
            <div className="ai-content">
              <ReactMarkdown>{studyPlan}</ReactMarkdown>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
