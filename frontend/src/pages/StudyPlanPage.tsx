import { useState } from "react";
import { Zap, Sparkles, RefreshCw } from "lucide-react";
import { aiStudyPlan } from "../api/client";
import ReactMarkdown from "react-markdown";

export default function StudyPlanPage() {
  const [plan, setPlan] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [generatedAt, setGeneratedAt] = useState<string>("");

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await aiStudyPlan();
      setPlan(result.plan);
      setGeneratedAt(new Date().toLocaleString("en-GB", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" }));
    } catch {
      setPlan("Could not generate study plan. Check your API settings and make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <div>
          <h1 className="page-title" style={{ marginBottom: 4 }}>
            <Sparkles size={22} color="var(--accent-indigo)" style={{ verticalAlign: "middle", marginRight: 8 }} />
            AI Study Plan
          </h1>
          <p style={{ color: "var(--text-secondary)", fontSize: 13, margin: 0 }}>
            Generate a personalized 7-day plan based on your progress and deadlines
          </p>
        </div>
        <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
          {loading ? (
            <>
              <span className="spinner" style={{ width: 14, height: 14, borderWidth: 2 }} />
              Generating...
            </>
          ) : plan ? (
            <><RefreshCw size={15} /> Regenerate</>
          ) : (
            <><Zap size={15} /> Generate Plan</>
          )}
        </button>
      </div>

      {!plan && !loading && (
        <div className="settings-card" style={{ textAlign: "center", padding: "48px 24px" }}>
          <Sparkles size={40} color="var(--text-muted)" style={{ marginBottom: 16, opacity: 0.4 }} />
          <p style={{ color: "var(--text-muted)", fontSize: 14, margin: 0 }}>
            Click <strong>Generate Plan</strong> to create an AI-powered study plan tailored to your courses, deadlines, and progress.
          </p>
        </div>
      )}

      {loading && !plan && (
        <div className="settings-card" style={{ textAlign: "center", padding: "48px 24px" }}>
          <span className="spinner" style={{ width: 28, height: 28, borderWidth: 3, marginBottom: 16 }} />
          <p style={{ color: "var(--text-secondary)", fontSize: 14, margin: 0 }}>
            Analyzing your courses, deadlines, and progress...
          </p>
        </div>
      )}

      {plan && (
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
