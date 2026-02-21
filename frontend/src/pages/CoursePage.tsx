import { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import {
  ChevronDown,
  ChevronRight,
  Upload,
  Link2,
  Trash2,
  FileText,
  Video,
  BookOpen,
  FlaskConical,
  Check,
  ExternalLink,
  Sparkles,
  Brain,
} from "lucide-react";
import {
  getCourse,
  uploadMaterial,
  deleteMaterial,
  toggleMaterial,
  assignMaterialWeek,
  aiQuiz,
  aiSummarize,
  aiExplain,
} from "../api/client";
import type { CourseDetail, Material, QuizQuestion } from "../types";
import ReactMarkdown from "react-markdown";

interface CoursePageProps {
  onStatsUpdate: () => void;
}

const TYPE_ICONS: Record<string, typeof FileText> = {
  lecture_slides: FileText,
  textbook_chapter: BookOpen,
  video: Video,
  lab_exercise: FlaskConical,
  quiz_prep: Brain,
};

const MATERIAL_TYPES = [
  { value: "lecture_slides", label: "Lecture Slides" },
  { value: "textbook_chapter", label: "Textbook Chapter" },
  { value: "video", label: "Video" },
  { value: "lab_exercise", label: "Lab Exercise" },
  { value: "quiz_prep", label: "Quiz Prep" },
  { value: "paper", label: "Paper" },
  { value: "note", label: "Note" },
  { value: "other", label: "Other" },
];

export default function CoursePage({ onStatsUpdate }: CoursePageProps) {
  const { courseId } = useParams<{ courseId: string }>();
  const [course, setCourse] = useState<CourseDetail | null>(null);
  const [expandedWeek, setExpandedWeek] = useState<number | null>(null);
  const [tab, setTab] = useState<"weeks" | "assessment" | "materials">("weeks");

  // Upload state
  const [addingToWeek, setAddingToWeek] = useState<number | null>(null);
  const [uploadMode, setUploadMode] = useState<"file" | "link">("file");
  const [uploadTitle, setUploadTitle] = useState("");
  const [uploadType, setUploadType] = useState("lecture_slides");
  const [uploadUrl, setUploadUrl] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  // AI state
  const [quizData, setQuizData] = useState<{ questions: QuizQuestion[] } | null>(null);
  const [quizWeek, setQuizWeek] = useState<number | null>(null);
  const [quizLoading, setQuizLoading] = useState(false);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [showResults, setShowResults] = useState(false);
  const [summarizing, setSummarizing] = useState<string | null>(null);
  const [summary, setSummary] = useState<{ id: string; text: string } | null>(null);
  const [explaining, setExplaining] = useState<number | null>(null);
  const [explanation, setExplanation] = useState<{ week: number; text: string } | null>(null);

  const reload = () => {
    if (courseId) getCourse(courseId).then(setCourse);
  };

  useEffect(() => {
    reload();
  }, [courseId]);

  if (!course) return <div className="loading"><span className="spinner" /> Loading course...</div>;

  const weekMaterials = (week: number) =>
    course.materials.filter((m) => m.week === week);

  const isCompleted = (id: string) =>
    course.completed_material_ids.includes(id);

  const handleToggle = async (id: string) => {
    await toggleMaterial(id);
    reload();
    onStatsUpdate();
  };

  const handleUpload = async () => {
    if (addingToWeek === null || !courseId) return;
    const formData = new FormData();
    formData.append("course_id", courseId);
    formData.append("week", String(addingToWeek));
    formData.append("title", uploadTitle);
    formData.append("type", uploadType);

    if (uploadMode === "file" && fileRef.current?.files?.[0]) {
      formData.append("file", fileRef.current.files[0]);
      if (!uploadTitle) formData.set("title", fileRef.current.files[0].name);
    } else {
      formData.append("url", uploadUrl);
    }

    await uploadMaterial(formData);
    setUploadTitle("");
    setUploadUrl("");
    setAddingToWeek(null);
    if (fileRef.current) fileRef.current.value = "";
    reload();
    onStatsUpdate();
  };

  const handleDelete = async (id: string) => {
    if (confirm("Delete this material?")) {
      await deleteMaterial(id);
      reload();
      onStatsUpdate();
    }
  };

  const handleQuiz = async (week: number, topic: string) => {
    setQuizLoading(true);
    setQuizWeek(week);
    setSelectedAnswers({});
    setShowResults(false);
    try {
      const data = await aiQuiz(courseId!, week, topic);
      setQuizData(data);
    } catch {
      setQuizData(null);
    }
    setQuizLoading(false);
  };

  const handleSummarize = async (m: Material) => {
    setSummarizing(m.id);
    try {
      const result = await aiSummarize(m.id);
      setSummary({ id: m.id, text: result.summary });
    } catch {
      setSummary({ id: m.id, text: "Could not summarize this material." });
    }
    setSummarizing(null);
  };

  const handleExplain = async (week: number, topic: string) => {
    setExplaining(week);
    try {
      const result = await aiExplain(topic, courseId!);
      setExplanation({ week, text: result.explanation });
    } catch {
      setExplanation({ week, text: "Could not generate explanation." });
    }
    setExplaining(null);
  };

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
        <button className={`tab ${tab === "materials" ? "active" : ""}`} onClick={() => setTab("materials")}>
          All Materials ({course.materials.length})
        </button>
        <button className={`tab ${tab === "assessment" ? "active" : ""}`} onClick={() => setTab("assessment")}>
          Assessment
        </button>
      </div>

      {tab === "assessment" && (
        <div className="card" style={{ maxWidth: 600 }}>
          <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 16 }}>Assessment Breakdown</h3>
          <table className="assessment-table">
            <thead>
              <tr>
                <th>Component</th>
                <th>Weight</th>
              </tr>
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

      {tab === "materials" && (
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
            <div style={{ fontSize: 14, color: "var(--text-secondary)" }}>
              {course.materials.filter((m) => isCompleted(m.id)).length}/{course.materials.length} completed
            </div>
          </div>
          <div className="material-list">
            {course.materials
              .slice()
              .sort((a, b) => a.week - b.week)
              .map((m) => {
              const done = isCompleted(m.id);
              const Icon = TYPE_ICONS[m.type] || FileText;
              return (
                <div key={m.id} className={`material-item ${done ? "completed" : ""}`}>
                  <div
                    className={`material-check ${done ? "done" : ""}`}
                    onClick={() => handleToggle(m.id)}
                  >
                    {done && <Check size={12} color="white" />}
                  </div>
                  <Icon size={14} color="var(--text-muted)" />
                  <span className={`material-title ${done ? "done" : ""}`}>
                    {m.title || m.file_name || "Untitled"}
                  </span>
                  <select
                    className="form-select"
                    style={{ flex: "none", width: "auto", minWidth: 130, fontSize: 11, padding: "4px 8px" }}
                    value={m.week}
                    onChange={async (e) => {
                      await assignMaterialWeek(m.id, parseInt(e.target.value));
                      reload();
                    }}
                    onClick={(e) => e.stopPropagation()}
                  >
                    <option value={0}>Unassigned</option>
                    {course.weeks.map((w) => (
                      <option key={w.week} value={w.week}>
                        W{w.week}: {w.topic.length > 25 ? w.topic.slice(0, 25) + "..." : w.topic}
                      </option>
                    ))}
                  </select>
                  <span className="material-type">{m.type.replace("_", " ")}</span>
                  <span className="material-xp">+{m.xp} XP</span>
                  <div className="material-actions">
                    {m.file_path && (
                      <button
                        onClick={() => window.open(`http://localhost:5001/api/materials/file/${courseId}/${m.file_path!.split("/").pop()}`, "_blank")}
                        title="Open file"
                      >
                        <ExternalLink size={14} />
                      </button>
                    )}
                    {m.url && (
                      <button onClick={() => window.open(m.url, "_blank")} title="Open link">
                        <ExternalLink size={14} />
                      </button>
                    )}
                    {m.file_path && (
                      <button
                        onClick={() => handleSummarize(m)}
                        disabled={summarizing === m.id}
                        title="AI Summarize"
                      >
                        <Sparkles size={14} />
                      </button>
                    )}
                    <button onClick={() => handleDelete(m.id)} title="Delete">
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
          {course.materials.length === 0 && (
            <div style={{ padding: 40, textAlign: "center", color: "var(--text-muted)" }}>
              No materials yet. Upload files or run the Moodle downloader.
            </div>
          )}

          {summary && (
            <div className="card" style={{ marginTop: 16, background: "var(--bg-primary)" }}>
              <h4 style={{ fontSize: 14, fontWeight: 600, marginBottom: 8, color: "var(--accent-emerald)" }}>
                AI Summary
              </h4>
              <div className="ai-content">
                <ReactMarkdown>{summary.text}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      )}

      {tab === "weeks" && (
        <div>
          {course.weeks.map((w) => {
            const materials = weekMaterials(w.week);
            const completedCount = materials.filter((m) => isCompleted(m.id)).length;
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
                      {materials.length > 0 && (
                        <span style={{ marginLeft: 8 }}>
                          &middot; {completedCount}/{materials.length} materials
                        </span>
                      )}
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

                    {/* AI actions */}
                    {w.status !== "holiday" && (
                      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
                        <button
                          className="btn btn-sm btn-secondary"
                          onClick={() => handleExplain(w.week, w.topic + ": " + w.details)}
                          disabled={explaining === w.week}
                        >
                          <Brain size={14} />
                          {explaining === w.week ? "Explaining..." : "AI Explain"}
                        </button>
                        <button
                          className="btn btn-sm btn-secondary"
                          onClick={() => handleQuiz(w.week, w.topic + ": " + w.details)}
                          disabled={quizLoading && quizWeek === w.week}
                        >
                          <Sparkles size={14} />
                          {quizLoading && quizWeek === w.week ? "Generating..." : "AI Quiz"}
                        </button>
                      </div>
                    )}

                    {/* AI Explanation */}
                    {explanation && explanation.week === w.week && (
                      <div className="card" style={{ marginBottom: 16, background: "var(--bg-primary)" }}>
                        <h4 style={{ fontSize: 14, fontWeight: 600, marginBottom: 8, color: "var(--accent-sky)" }}>
                          <Brain size={14} style={{ verticalAlign: "middle", marginRight: 4 }} />
                          AI Explanation
                        </h4>
                        <div className="ai-content">
                          <ReactMarkdown>{explanation.text}</ReactMarkdown>
                        </div>
                      </div>
                    )}

                    {/* AI Quiz */}
                    {quizData && quizWeek === w.week && quizData.questions && (
                      <div style={{ marginBottom: 16 }}>
                        <h4 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, color: "var(--accent-amber)" }}>
                          <Sparkles size={14} style={{ verticalAlign: "middle", marginRight: 4 }} />
                          Practice Quiz
                        </h4>
                        {quizData.questions.map((q, qi) => (
                          <div key={qi} className="quiz-question">
                            <div className="quiz-question-text">
                              {qi + 1}. {q.question}
                            </div>
                            {q.options.map((opt) => {
                              const letter = opt.charAt(0);
                              const isSelected = selectedAnswers[qi] === letter;
                              const isCorrect = showResults && letter === q.correct;
                              const isWrong = showResults && isSelected && letter !== q.correct;
                              return (
                                <div
                                  key={opt}
                                  className={`quiz-option ${isSelected ? "selected" : ""} ${isCorrect ? "correct" : ""} ${isWrong ? "wrong" : ""}`}
                                  onClick={() => {
                                    if (!showResults)
                                      setSelectedAnswers((prev) => ({ ...prev, [qi]: letter }));
                                  }}
                                >
                                  {showResults && isCorrect && <Check size={14} color="var(--accent-emerald)" />}
                                  {opt}
                                </div>
                              );
                            })}
                            {showResults && q.explanation && (
                              <div className="quiz-explanation">{q.explanation}</div>
                            )}
                          </div>
                        ))}
                        {!showResults && (
                          <button className="btn btn-primary" onClick={() => setShowResults(true)}>
                            Check Answers
                          </button>
                        )}
                      </div>
                    )}

                    {/* Materials */}
                    <div className="material-list">
                      {materials.map((m) => {
                        const done = isCompleted(m.id);
                        const Icon = TYPE_ICONS[m.type] || FileText;
                        return (
                          <div key={m.id} className={`material-item ${done ? "completed" : ""}`}>
                            <div
                              className={`material-check ${done ? "done" : ""}`}
                              onClick={() => handleToggle(m.id)}
                            >
                              {done && <Check size={12} color="white" />}
                            </div>
                            <Icon size={14} color="var(--text-muted)" />
                            <span className={`material-title ${done ? "done" : ""}`}>
                              {m.title || m.file_name || "Untitled"}
                            </span>
                            <span className="material-type">{m.type.replace("_", " ")}</span>
                            <span className="material-xp">+{m.xp} XP</span>
                            <div className="material-actions">
                              {m.file_path && (
                                <button
                                  onClick={() => window.open(`http://localhost:5001/api/materials/file/${courseId}/${m.file_path!.split("/").pop()}`, "_blank")}
                                  title="Open file"
                                >
                                  <ExternalLink size={14} />
                                </button>
                              )}
                              {m.url && (
                                <button onClick={() => window.open(m.url, "_blank")} title="Open link">
                                  <ExternalLink size={14} />
                                </button>
                              )}
                              {m.file_path && (
                                <button
                                  onClick={() => handleSummarize(m)}
                                  disabled={summarizing === m.id}
                                  title="AI Summarize"
                                >
                                  <Sparkles size={14} />
                                </button>
                              )}
                              <button onClick={() => handleDelete(m.id)} title="Delete">
                                <Trash2 size={14} />
                              </button>
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    {/* Summary display */}
                    {summary && summary.id && materials.some((m) => m.id === summary.id) && (
                      <div className="card" style={{ marginTop: 12, background: "var(--bg-primary)" }}>
                        <h4 style={{ fontSize: 14, fontWeight: 600, marginBottom: 8, color: "var(--accent-emerald)" }}>
                          AI Summary
                        </h4>
                        <div className="ai-content">
                          <ReactMarkdown>{summary.text}</ReactMarkdown>
                        </div>
                      </div>
                    )}

                    {/* Add material */}
                    {addingToWeek === w.week ? (
                      <div style={{ marginTop: 12, padding: 16, background: "var(--bg-tertiary)", borderRadius: 10 }}>
                        <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
                          <button
                            className={`btn btn-sm ${uploadMode === "file" ? "btn-primary" : "btn-secondary"}`}
                            onClick={() => setUploadMode("file")}
                          >
                            <Upload size={14} /> Upload File
                          </button>
                          <button
                            className={`btn btn-sm ${uploadMode === "link" ? "btn-primary" : "btn-secondary"}`}
                            onClick={() => setUploadMode("link")}
                          >
                            <Link2 size={14} /> Add Link
                          </button>
                        </div>
                        <div className="form-row">
                          <input
                            className="form-input"
                            placeholder="Title"
                            value={uploadTitle}
                            onChange={(e) => setUploadTitle(e.target.value)}
                          />
                          <select
                            className="form-select"
                            value={uploadType}
                            onChange={(e) => setUploadType(e.target.value)}
                          >
                            {MATERIAL_TYPES.map((t) => (
                              <option key={t.value} value={t.value}>{t.label}</option>
                            ))}
                          </select>
                        </div>
                        {uploadMode === "file" ? (
                          <input
                            type="file"
                            ref={fileRef}
                            className="form-input"
                            accept=".pdf,.pptx,.docx,.txt,.py,.ipynb,.mp4,.zip"
                            style={{ marginBottom: 12 }}
                          />
                        ) : (
                          <input
                            className="form-input"
                            placeholder="URL (e.g., YouTube link)"
                            value={uploadUrl}
                            onChange={(e) => setUploadUrl(e.target.value)}
                            style={{ marginBottom: 12 }}
                          />
                        )}
                        <div style={{ display: "flex", gap: 8 }}>
                          <button className="btn btn-primary btn-sm" onClick={handleUpload}>
                            Save Material
                          </button>
                          <button className="btn btn-secondary btn-sm" onClick={() => setAddingToWeek(null)}>
                            Cancel
                          </button>
                        </div>
                      </div>
                    ) : (
                      w.status !== "holiday" && (
                        <button
                          className="btn btn-sm btn-secondary"
                          style={{ marginTop: 12 }}
                          onClick={() => setAddingToWeek(w.week)}
                        >
                          + Add Material
                        </button>
                      )
                    )}
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
