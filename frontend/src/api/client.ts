import axios from "axios";
import type {
  Course,
  CourseDetail,
  Deadline,
  Stats,
  Material,
  ChatEntry,
  StudyTask,
  TaskCategories,
} from "../types";

const api = axios.create({ baseURL: "http://localhost:5001/api" });

export const getCourses = () => api.get<Course[]>("/courses").then((r) => r.data);

export const getCourse = (id: string) =>
  api.get<CourseDetail>(`/course/${id}`).then((r) => r.data);

export const getDeadlines = () =>
  api.get<Deadline[]>("/deadlines").then((r) => r.data);

export const toggleDeadline = (id: string) =>
  api.patch<Deadline>(`/deadlines/${id}/toggle`).then((r) => r.data);

export const getStats = () => api.get<Stats>("/stats").then((r) => r.data);

export const uploadMaterial = (formData: FormData) =>
  api.post<Material>("/materials", formData).then((r) => r.data);

export const deleteMaterial = (id: string) =>
  api.delete(`/materials/${id}`).then((r) => r.data);

export const toggleMaterial = (id: string) =>
  api.patch(`/materials/${id}/complete`).then((r) => r.data);

export const aiChat = (message: string, courseId: string) =>
  api
    .post<ChatEntry>("/ai/chat", { message, course_id: courseId })
    .then((r) => r.data);

export const aiQuiz = (courseId: string, week?: number, topic?: string) =>
  api
    .post("/ai/quiz", { course_id: courseId, week, topic })
    .then((r) => r.data);

export const aiSummarize = (materialId: string) =>
  api.post("/ai/summarize", { material_id: materialId }).then((r) => r.data);

export const aiExplain = (topic: string, courseId: string) =>
  api
    .post("/ai/explain", { topic, course_id: courseId })
    .then((r) => r.data);

export const aiStudyPlan = () =>
  api.post("/ai/study-plan").then((r) => r.data);

export const getStudyTasks = () =>
  api
    .get<{ tasks: StudyTask[]; categories: TaskCategories }>("/study-tasks")
    .then((r) => r.data);

export const toggleStudyTask = (id: string) =>
  api.patch<StudyTask>(`/study-tasks/${id}/toggle`).then((r) => r.data);

export const addStudyTask = (task: {
  date: string;
  course_id: string;
  title: string;
  hours: number;
  category: string;
}) => api.post<StudyTask>("/study-tasks", task).then((r) => r.data);

export const deleteStudyTask = (id: string) =>
  api.delete(`/study-tasks/${id}`).then((r) => r.data);
