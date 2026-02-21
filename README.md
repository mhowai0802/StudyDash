# StudyDash

A study progress tracker with AI assistant for managing multiple university courses. Built with React + TypeScript (frontend) and Python Flask (backend).

## Features

- **Dashboard** with progress rings, XP system, and deadline countdowns
- **Course Management** with weekly topic breakdowns and material storage
- **Material Uploads** — upload PDFs, add video links, organized per course/week
- **XP & Leveling System** — earn XP for completing materials, level up from Beginner to Grandmaster
- **AI Study Assistant** — chat with AI about course topics, get explanations
- **AI Quiz Generator** — generate practice quizzes for any week/topic
- **AI Summarizer** — auto-summarize uploaded PDF materials
- **AI Study Planner** — get a personalized weekly study plan based on your progress
- **Deadline Tracker** — color-coded urgency, sorted chronologically
- **Pre-populated** with three courses: NLP & LLM, CVPR, IT Forum

## Quick Start

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit .env with your API key
python app.py
```

Backend runs at http://localhost:5001

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

## Tech Stack

- **Frontend**: React 19, TypeScript, Vite, React Router, Lucide Icons, React Markdown
- **Backend**: Python, Flask, Flask-CORS, PyPDF2
- **AI**: HKBU GenAI API (GPT-4.1)
- **Storage**: JSON file + local filesystem for uploaded materials
