import { useState, useEffect, useCallback } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import CoursePage from "./pages/CoursePage";
import DeadlinesPage from "./pages/DeadlinesPage";
import AIPage from "./pages/AIPage";
import { getStats } from "./api/client";
import type { Stats } from "./types";

export default function App() {
  const [stats, setStats] = useState<Stats | null>(null);

  const refreshStats = useCallback(() => {
    getStats().then(setStats).catch(() => {});
  }, []);

  useEffect(() => {
    refreshStats();
  }, [refreshStats]);

  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar stats={stats} />
        <main className="main-content">
          <Routes>
            <Route
              path="/"
              element={<Dashboard onStatsUpdate={refreshStats} />}
            />
            <Route
              path="/course/:courseId"
              element={<CoursePage onStatsUpdate={refreshStats} />}
            />
            <Route path="/deadlines" element={<DeadlinesPage />} />
            <Route path="/ai" element={<AIPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
