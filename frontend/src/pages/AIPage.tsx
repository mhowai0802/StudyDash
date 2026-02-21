import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Sparkles } from "lucide-react";
import { aiChat } from "../api/client";
import ReactMarkdown from "react-markdown";

interface Message {
  role: "user" | "ai";
  content: string;
  timestamp: string;
}

const COURSE_OPTIONS = [
  { id: "", label: "General" },
  { id: "nlp", label: "NLP & LLM" },
  { id: "cvpr", label: "CVPR" },
  { id: "it-forum", label: "IT Forum" },
];

const QUICK_PROMPTS = [
  "Explain the Transformer architecture",
  "What are N-gram language models?",
  "Explain image segmentation techniques",
  "How does object detection work in CVPR?",
  "Compare Word2Vec and GloVe",
  "What is the attention mechanism?",
  "Explain CNN for image classification",
  "What are the main NLP preprocessing steps?",
];

export default function AIPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [courseId, setCourseId] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (text?: string) => {
    const msg = text || input.trim();
    if (!msg || loading) return;
    setInput("");

    const userMsg: Message = {
      role: "user",
      content: msg,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const result = await aiChat(msg, courseId);
      const aiMsg: Message = {
        role: "ai",
        content: result.ai_reply,
        timestamp: result.timestamp,
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "Sorry, I couldn't process your request. Make sure the backend server is running.",
          timestamp: new Date().toISOString(),
        },
      ]);
    }
    setLoading(false);
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">
          <Bot size={28} style={{ verticalAlign: "middle", marginRight: 8 }} />
          AI Study Assistant
        </h1>
        <p className="page-subtitle">
          Ask questions about your courses, get explanations, and study smarter.
        </p>
      </div>

      <div className="card chat-container">
        {/* Course selector */}
        <div style={{ padding: "12px 16px", borderBottom: "1px solid var(--border)", display: "flex", alignItems: "center", gap: 12 }}>
          <span style={{ fontSize: 13, color: "var(--text-secondary)" }}>Context:</span>
          {COURSE_OPTIONS.map((c) => (
            <button
              key={c.id}
              className={`btn btn-sm ${courseId === c.id ? "btn-primary" : "btn-secondary"}`}
              onClick={() => setCourseId(c.id)}
            >
              {c.label}
            </button>
          ))}
        </div>

        <div className="chat-messages">
          {messages.length === 0 && (
            <div style={{ textAlign: "center", padding: "40px 20px" }}>
              <Sparkles size={40} color="var(--accent-indigo)" style={{ marginBottom: 16 }} />
              <h3 style={{ fontSize: 18, fontWeight: 700, marginBottom: 8 }}>
                How can I help you study?
              </h3>
              <p style={{ fontSize: 14, color: "var(--text-secondary)", marginBottom: 24, maxWidth: 400, margin: "0 auto 24px" }}>
                Ask me about any topic from your courses. I can explain concepts,
                help you prepare for quizzes, and answer your questions.
              </p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
                {QUICK_PROMPTS.map((p) => (
                  <button
                    key={p}
                    className="btn btn-sm btn-secondary"
                    onClick={() => handleSend(p)}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((m, i) => (
            <div key={i} className={`chat-msg ${m.role}`}>
              <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
                {m.role === "user" ? (
                  <User size={14} />
                ) : (
                  <Bot size={14} />
                )}
                <span style={{ fontSize: 11, opacity: 0.7 }}>
                  {m.role === "user" ? "You" : "StudyDash AI"}
                </span>
              </div>
              {m.role === "ai" ? (
                <div className="ai-content">
                  <ReactMarkdown>{m.content}</ReactMarkdown>
                </div>
              ) : (
                m.content
              )}
            </div>
          ))}

          {loading && (
            <div className="chat-msg ai">
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span className="spinner" style={{ width: 16, height: 16, borderWidth: 2 }} />
                Thinking...
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="chat-input-row">
          <input
            className="form-input"
            placeholder="Ask about NLP, CVPR, or any study topic..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            disabled={loading}
          />
          <button className="btn btn-primary" onClick={() => handleSend()} disabled={loading}>
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
