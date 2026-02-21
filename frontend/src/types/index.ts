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
  total_materials?: number;
  completed_materials?: number;
  total_weeks?: number;
}

export interface CourseDetail extends Course {
  materials: Material[];
  completed_material_ids: string[];
  completed_count: number;
}

export interface Material {
  id: string;
  course_id: string;
  week: number;
  title: string;
  type: string;
  xp: number;
  created_at: string;
  file_path?: string | null;
  file_name?: string | null;
  url?: string;
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

export interface Level {
  level: number;
  name: string;
  xp_required: number;
}

export interface Stats {
  xp: number;
  level: {
    current: Level;
    next: Level | null;
    xp: number;
    xp_to_next: number;
  };
  total_materials: number;
  completed_materials: number;
  material_progress: number;
  total_deadlines: number;
  completed_deadlines: number;
  per_course: Record<string, { name: string; total: number; completed: number; progress: number }>;
  xp_values: Record<string, number>;
  levels: Level[];
}

export interface ChatEntry {
  id: string;
  course_id: string;
  user_message: string;
  ai_reply: string;
  timestamp: string;
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correct: string;
  explanation: string;
}
