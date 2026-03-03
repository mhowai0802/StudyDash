import { useState, useEffect } from "react";
import { Save, TestTube, CheckCircle, XCircle, Loader2, Eye, EyeOff } from "lucide-react";
import { getSettings, updateSettings, testSettings } from "../api/client";
import type { ApiSettings } from "../api/client";

export default function SettingsPage() {
  const [settings, setSettings] = useState<ApiSettings>({
    api_key: "",
    base_url: "",
    model: "",
    api_version: "",
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ ok: boolean; message: string } | null>(null);
  const [saved, setSaved] = useState(false);
  const [showKey, setShowKey] = useState(false);

  useEffect(() => {
    getSettings()
      .then((s) => { setSettings(s); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setSaved(false);
    setTestResult(null);
    try {
      await updateSettings(settings);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } finally {
      setSaving(false);
    }
  };

  const handleTest = async () => {
    setTesting(true);
    setTestResult(null);
    try {
      const result = await testSettings();
      setTestResult(result);
    } catch {
      setTestResult({ ok: false, message: "Failed to connect to backend" });
    } finally {
      setTesting(false);
    }
  };

  if (loading) {
    return (
      <div style={{ padding: 40, textAlign: "center", color: "var(--text-muted)" }}>
        <Loader2 size={24} className="spin" /> Loading settings...
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 640, margin: "0 auto" }}>
      <h1 className="page-title" style={{ marginBottom: 8 }}>Settings</h1>
      <p style={{ color: "var(--text-secondary)", fontSize: 14, marginBottom: 28 }}>
        Configure the AI API connection for chat, quiz generation, summarization, and study planning.
      </p>

      <div className="settings-card">
        <div className="settings-section-title">API Configuration</div>

        <div className="settings-field">
          <label className="settings-label">API Key</label>
          <div style={{ display: "flex", gap: 8 }}>
            <input
              className="form-input"
              type={showKey ? "text" : "password"}
              value={settings.api_key}
              onChange={(e) => setSettings({ ...settings, api_key: e.target.value })}
              placeholder="Enter your API key"
              style={{ flex: 1, fontFamily: showKey ? "monospace" : "inherit" }}
            />
            <button
              className="btn btn-sm btn-secondary"
              onClick={() => setShowKey(!showKey)}
              title={showKey ? "Hide" : "Show"}
              style={{ minWidth: 38 }}
            >
              {showKey ? <EyeOff size={15} /> : <Eye size={15} />}
            </button>
          </div>
        </div>

        <div className="settings-field">
          <label className="settings-label">Base URL</label>
          <input
            className="form-input"
            value={settings.base_url}
            onChange={(e) => setSettings({ ...settings, base_url: e.target.value })}
            placeholder="https://genai.hkbu.edu.hk/api/v0/rest"
            style={{ fontFamily: "monospace", fontSize: 13 }}
          />
        </div>

        <div style={{ display: "flex", gap: 16 }}>
          <div className="settings-field" style={{ flex: 1 }}>
            <label className="settings-label">Model</label>
            <input
              className="form-input"
              value={settings.model}
              onChange={(e) => setSettings({ ...settings, model: e.target.value })}
              placeholder="gpt-4.1"
              style={{ fontFamily: "monospace", fontSize: 13 }}
            />
          </div>
          <div className="settings-field" style={{ flex: 1 }}>
            <label className="settings-label">API Version</label>
            <input
              className="form-input"
              value={settings.api_version}
              onChange={(e) => setSettings({ ...settings, api_version: e.target.value })}
              placeholder="2024-12-01-preview"
              style={{ fontFamily: "monospace", fontSize: 13 }}
            />
          </div>
        </div>

        <div style={{ display: "flex", gap: 10, marginTop: 8 }}>
          <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
            {saving ? <Loader2 size={15} className="spin" /> : <Save size={15} />}
            {saving ? "Saving..." : "Save"}
          </button>
          <button className="btn btn-secondary" onClick={handleTest} disabled={testing}>
            {testing ? <Loader2 size={15} className="spin" /> : <TestTube size={15} />}
            {testing ? "Testing..." : "Test Connection"}
          </button>
        </div>

        {saved && (
          <div className="settings-toast settings-toast-success">
            <CheckCircle size={15} /> Settings saved to .env
          </div>
        )}

        {testResult && (
          <div className={`settings-toast ${testResult.ok ? "settings-toast-success" : "settings-toast-error"}`}>
            {testResult.ok ? <CheckCircle size={15} /> : <XCircle size={15} />}
            {testResult.message}
          </div>
        )}
      </div>
    </div>
  );
}
