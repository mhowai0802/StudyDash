export interface Assessment {
  continuous: {
    weight: number;
    components: { name: string; weight: number | string }[];
  };
  exam: { weight: number; note: string };
}

export interface Week {
  week: number;
  date: string;
  topic: string;
  details: string;
  has_lab: boolean;
  lab_name?: string;
  has_quiz: boolean;
  quiz_name?: string;
  status: string;
}

export interface Course {
  id: string;
  name: string;
  code: string;
  instructor: string;
  ta: string;
  schedule: string;
  venue: string;
  color: string;
  assessment: Assessment;
  weeks: Week[];
  total_weeks?: number;
  total_tasks?: number;
  completed_tasks?: number;
}

export interface Deadline {
  id: string;
  course_id: string;
  title: string;
  date: string;
  weight: string;
  type: string;
  done: boolean;
  urgency?: string;
}

export interface StudyTask {
  id: string;
  date: string;
  course_id: string;
  title: string;
  hours: number;
  category: string;
  done: boolean;
}

export interface TaskCategory {
  label: string;
  color: string;
}

export type TaskCategories = Record<string, TaskCategory>;
