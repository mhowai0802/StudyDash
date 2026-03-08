import axios from "axios";
import type {
  Course,
  Deadline,
  StudyTask,
  TaskCategories,
} from "../types";

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:5001/api" });

export const getCourses = () => api.get<Course[]>("/courses").then((r) => r.data);

export const getCourse = (id: string) =>
  api.get<Course>(`/course/${id}`).then((r) => r.data);

export const getDeadlines = () =>
  api.get<Deadline[]>("/deadlines").then((r) => r.data);

export const toggleDeadline = (id: string) =>
  api.patch<Deadline>(`/deadlines/${id}/toggle`).then((r) => r.data);

export const getProject = (courseId: string) =>
  api.get(`/project/${courseId}`).then((r) => r.data);

export const toggleMilestone = (courseId: string, milestoneId: string) =>
  api.patch(`/project/${courseId}/milestone/${milestoneId}/toggle`).then((r) => r.data);

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

export const updateStudyTask = (
  id: string,
  updates: Partial<{ date: string; title: string; hours: number; category: string; course_id: string }>
) => api.patch<StudyTask>(`/study-tasks/${id}`, updates).then((r) => r.data);

export const deleteStudyTask = (id: string) =>
  api.delete(`/study-tasks/${id}`).then((r) => r.data);
