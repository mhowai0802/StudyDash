import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import CoursePage from "./pages/CoursePage";
import DeadlinesPage from "./pages/DeadlinesPage";
import RevisionMaterialsPage from "./pages/RevisionMaterialsPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/course/:courseId" element={<CoursePage />} />
            <Route path="/deadlines" element={<DeadlinesPage />} />
            <Route path="/revision-materials" element={<RevisionMaterialsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
