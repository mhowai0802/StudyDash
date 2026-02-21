import os
import json
import uuid
from datetime import datetime, date
from pathlib import Path

import requests as http_requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from course_data import INITIAL_COURSES, INITIAL_DEADLINES, XP_VALUES, LEVELS
from study_plan_data import INITIAL_STUDY_TASKS, TASK_CATEGORIES

load_dotenv()

app = Flask(__name__)
CORS(app)

DATA_DIR = Path(__file__).parent / "data"
MATERIALS_DIR = Path(__file__).parent / "materials"
PROGRESS_FILE = DATA_DIR / "progress.json"

DATA_DIR.mkdir(exist_ok=True)
MATERIALS_DIR.mkdir(exist_ok=True)
for cid in ["nlp", "cvpr", "it-forum"]:
    (MATERIALS_DIR / cid).mkdir(exist_ok=True)


def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return init_progress()


def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def init_progress():
    data = {
        "courses": INITIAL_COURSES,
        "deadlines": INITIAL_DEADLINES,
        "study_tasks": INITIAL_STUDY_TASKS,
        "materials": [],
        "xp": 0,
        "completed_materials": [],
        "chat_history": [],
    }
    save_progress(data)
    return data


def ensure_study_tasks(data):
    """Backfill study_tasks if missing from older data files."""
    if "study_tasks" not in data:
        data["study_tasks"] = INITIAL_STUDY_TASKS
        save_progress(data)
    return data


def get_level(xp):
    current = LEVELS[0]
    for lvl in LEVELS:
        if xp >= lvl["xp_required"]:
            current = lvl
    next_lvl = None
    for lvl in LEVELS:
        if lvl["xp_required"] > xp:
            next_lvl = lvl
            break
    return {
        "current": current,
        "next": next_lvl,
        "xp": xp,
        "xp_to_next": next_lvl["xp_required"] - xp if next_lvl else 0,
    }


# ─── API Routes ───


@app.route("/api/courses", methods=["GET"])
def get_courses():
    data = load_progress()
    courses_summary = []
    for course in data["courses"]:
        total_weeks = len([w for w in course["weeks"] if w.get("status") != "holiday"])
        course_materials = [m for m in data["materials"] if m["course_id"] == course["id"]]
        completed = [m for m in course_materials if m["id"] in data["completed_materials"]]
        courses_summary.append({
            **course,
            "total_materials": len(course_materials),
            "completed_materials": len(completed),
            "total_weeks": total_weeks,
        })
    return jsonify(courses_summary)


@app.route("/api/course/<course_id>", methods=["GET"])
def get_course(course_id):
    data = load_progress()
    course = next((c for c in data["courses"] if c["id"] == course_id), None)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    course_materials = [m for m in data["materials"] if m["course_id"] == course_id]
    completed = [m for m in course_materials if m["id"] in data["completed_materials"]]
    return jsonify({
        **course,
        "materials": course_materials,
        "completed_material_ids": data["completed_materials"],
        "total_materials": len(course_materials),
        "completed_count": len(completed),
    })


@app.route("/api/materials", methods=["POST"])
def add_material():
    data = load_progress()
    file = request.files.get("file")
    material = {
        "id": str(uuid.uuid4()),
        "course_id": request.form.get("course_id"),
        "week": int(request.form.get("week", 0)),
        "title": request.form.get("title", ""),
        "type": request.form.get("type", "other"),
        "xp": XP_VALUES.get(request.form.get("type", "other"), 10),
        "created_at": datetime.now().isoformat(),
    }

    if file:
        safe_name = f"{material['id']}_{file.filename}"
        save_path = MATERIALS_DIR / material["course_id"] / safe_name
        file.save(str(save_path))
        material["file_path"] = str(save_path)
        material["file_name"] = file.filename
    else:
        material["url"] = request.form.get("url", "")
        material["file_path"] = None
        material["file_name"] = None

    data["materials"].append(material)
    save_progress(data)
    return jsonify(material), 201


@app.route("/api/materials/<material_id>", methods=["DELETE"])
def delete_material(material_id):
    data = load_progress()
    material = next((m for m in data["materials"] if m["id"] == material_id), None)
    if not material:
        return jsonify({"error": "Not found"}), 404

    if material.get("file_path") and os.path.exists(material["file_path"]):
        os.remove(material["file_path"])

    data["materials"] = [m for m in data["materials"] if m["id"] != material_id]
    data["completed_materials"] = [mid for mid in data["completed_materials"] if mid != material_id]
    save_progress(data)
    return jsonify({"ok": True})


@app.route("/api/materials/<material_id>/complete", methods=["PATCH"])
def toggle_material_complete(material_id):
    data = load_progress()
    material = next((m for m in data["materials"] if m["id"] == material_id), None)
    if not material:
        return jsonify({"error": "Not found"}), 404

    if material_id in data["completed_materials"]:
        data["completed_materials"].remove(material_id)
        data["xp"] -= material.get("xp", 0)
    else:
        data["completed_materials"].append(material_id)
        data["xp"] += material.get("xp", 0)

        # Check week completion bonus
        week_materials = [
            m for m in data["materials"]
            if m["course_id"] == material["course_id"] and m["week"] == material["week"]
        ]
        if all(m["id"] in data["completed_materials"] for m in week_materials) and len(week_materials) > 0:
            data["xp"] += XP_VALUES["week_complete_bonus"]

    save_progress(data)
    return jsonify({
        "completed": material_id in data["completed_materials"],
        "xp": data["xp"],
        "level": get_level(data["xp"]),
    })


@app.route("/api/materials/file/<path:filepath>", methods=["GET"])
def serve_material(filepath):
    full_path = MATERIALS_DIR / filepath
    if not full_path.exists():
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(full_path.parent, full_path.name)


@app.route("/api/deadlines", methods=["GET"])
def get_deadlines():
    data = load_progress()
    today = date.today().isoformat()
    deadlines = sorted(data["deadlines"], key=lambda d: d["date"])
    for d in deadlines:
        if d["date"] < today and not d["done"]:
            d["urgency"] = "overdue"
        elif d["date"] <= (date.today().__str__()):
            d["urgency"] = "today"
        else:
            days_away = (date.fromisoformat(d["date"]) - date.today()).days
            if days_away <= 7:
                d["urgency"] = "this_week"
            elif days_away <= 14:
                d["urgency"] = "next_week"
            else:
                d["urgency"] = "future"
    return jsonify(deadlines)


@app.route("/api/deadlines/<deadline_id>/toggle", methods=["PATCH"])
def toggle_deadline(deadline_id):
    data = load_progress()
    deadline = next((d for d in data["deadlines"] if d["id"] == deadline_id), None)
    if not deadline:
        return jsonify({"error": "Not found"}), 404
    deadline["done"] = not deadline["done"]
    save_progress(data)
    return jsonify(deadline)


@app.route("/api/stats", methods=["GET"])
def get_stats():
    data = load_progress()
    total_materials = len(data["materials"])
    completed = len(data["completed_materials"])
    total_deadlines = len(data["deadlines"])
    completed_deadlines = len([d for d in data["deadlines"] if d["done"]])

    per_course = {}
    for course in data["courses"]:
        cm = [m for m in data["materials"] if m["course_id"] == course["id"]]
        cc = [m for m in cm if m["id"] in data["completed_materials"]]
        per_course[course["id"]] = {
            "name": course["name"],
            "total": len(cm),
            "completed": len(cc),
            "progress": round(len(cc) / len(cm) * 100) if cm else 0,
        }

    return jsonify({
        "xp": data["xp"],
        "level": get_level(data["xp"]),
        "total_materials": total_materials,
        "completed_materials": completed,
        "material_progress": round(completed / total_materials * 100) if total_materials else 0,
        "total_deadlines": total_deadlines,
        "completed_deadlines": completed_deadlines,
        "per_course": per_course,
        "xp_values": XP_VALUES,
        "levels": LEVELS,
    })


# ─── Study Tasks Endpoints ───


@app.route("/api/study-tasks", methods=["GET"])
def get_study_tasks():
    data = ensure_study_tasks(load_progress())
    return jsonify({"tasks": data["study_tasks"], "categories": TASK_CATEGORIES})


@app.route("/api/study-tasks/<task_id>/toggle", methods=["PATCH"])
def toggle_study_task(task_id):
    data = ensure_study_tasks(load_progress())
    task = next((t for t in data["study_tasks"] if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Not found"}), 404
    task["done"] = not task["done"]
    save_progress(data)
    return jsonify(task)


@app.route("/api/study-tasks", methods=["POST"])
def add_study_task():
    data = ensure_study_tasks(load_progress())
    body = request.json
    task = {
        "id": str(uuid.uuid4()),
        "date": body.get("date"),
        "course_id": body.get("course_id", ""),
        "title": body.get("title", ""),
        "hours": body.get("hours", 1),
        "category": body.get("category", "review"),
        "done": False,
    }
    data["study_tasks"].append(task)
    save_progress(data)
    return jsonify(task), 201


@app.route("/api/study-tasks/<task_id>", methods=["DELETE"])
def delete_study_task(task_id):
    data = ensure_study_tasks(load_progress())
    data["study_tasks"] = [t for t in data["study_tasks"] if t["id"] != task_id]
    save_progress(data)
    return jsonify({"ok": True})


# ─── AI Endpoints ───


def call_ai(messages, temperature=0.7, max_tokens=1000):
    api_key = os.getenv("HKBU_API_KEY")
    base_url = os.getenv("HKBU_BASE_URL")
    model = os.getenv("HKBU_MODEL", "gpt-4.1")
    api_version = os.getenv("HKBU_API_VERSION", "2024-12-01-preview")

    url = f"{base_url}/deployments/{model}/chat/completions?api-version={api_version}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": api_key,
    }
    payload = {
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": 1,
        "stream": False,
    }
    resp = http_requests.post(url, json=payload, headers=headers, timeout=60)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    return f"AI Error ({resp.status_code}): {resp.text}"


@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    body = request.json
    user_message = body.get("message", "")
    course_context = body.get("course_id", "")

    data = load_progress()
    course = next((c for c in data["courses"] if c["id"] == course_context), None)
    course_info = f"Course: {course['name']}. Topics covered: {', '.join(w['topic'] for w in course['weeks'])}." if course else ""

    system_prompt = (
        "You are StudyDash AI, a helpful study assistant for a university student in Hong Kong. "
        "You help with course material understanding, exam preparation, and study strategies. "
        f"{course_info} "
        "Be concise, clear, and educational. Use examples when helpful. "
        "If asked about a topic, explain it at an appropriate academic level."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    reply = call_ai(messages)
    chat_entry = {
        "id": str(uuid.uuid4()),
        "course_id": course_context,
        "user_message": user_message,
        "ai_reply": reply,
        "timestamp": datetime.now().isoformat(),
    }
    data["chat_history"].append(chat_entry)
    save_progress(data)
    return jsonify(chat_entry)


@app.route("/api/ai/quiz", methods=["POST"])
def ai_generate_quiz():
    body = request.json
    course_id = body.get("course_id", "")
    week = body.get("week", None)
    topic = body.get("topic", "")

    data = load_progress()
    course = next((c for c in data["courses"] if c["id"] == course_id), None)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    if week:
        week_data = next((w for w in course["weeks"] if w["week"] == week), None)
        topic = f"{week_data['topic']}: {week_data['details']}" if week_data else topic

    system_prompt = (
        "You are a quiz generator for university courses. Generate a quiz with 5 multiple-choice questions. "
        "Format your response as JSON with this structure: "
        '{"questions": [{"question": "...", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "correct": "A", "explanation": "..."}]}'
    )
    user_prompt = f"Generate a quiz about: {topic} for the course {course['name']}."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    reply = call_ai(messages, temperature=0.5, max_tokens=2000)
    try:
        clean = reply.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
        quiz_data = json.loads(clean)
    except (json.JSONDecodeError, IndexError):
        quiz_data = {"raw": reply}

    return jsonify(quiz_data)


@app.route("/api/ai/summarize", methods=["POST"])
def ai_summarize():
    """Summarize uploaded PDF content."""
    body = request.json
    material_id = body.get("material_id", "")

    data = load_progress()
    material = next((m for m in data["materials"] if m["id"] == material_id), None)
    if not material or not material.get("file_path"):
        return jsonify({"error": "Material not found or no file"}), 404

    try:
        reader = PdfReader(material["file_path"])
        text = ""
        for page in reader.pages[:20]:
            text += page.extract_text() or ""
        text = text[:8000]
    except Exception as e:
        return jsonify({"error": f"Could not read PDF: {str(e)}"}), 400

    messages = [
        {"role": "system", "content": "You are a study assistant. Summarize the following lecture/document content into clear, concise study notes with key points and important concepts. Use bullet points and headers."},
        {"role": "user", "content": f"Summarize this document:\n\n{text}"},
    ]

    summary = call_ai(messages, max_tokens=1500)
    return jsonify({"summary": summary, "material_id": material_id})


@app.route("/api/ai/explain", methods=["POST"])
def ai_explain():
    """Explain a specific topic in depth."""
    body = request.json
    topic = body.get("topic", "")
    course_id = body.get("course_id", "")

    data = load_progress()
    course = next((c for c in data["courses"] if c["id"] == course_id), None)
    course_name = course["name"] if course else "your course"

    messages = [
        {"role": "system", "content": f"You are a university tutor for {course_name}. Explain topics clearly with examples, analogies, and key takeaways. Structure your explanation with headers and bullet points."},
        {"role": "user", "content": f"Explain this topic in detail: {topic}"},
    ]

    explanation = call_ai(messages, max_tokens=2000)
    return jsonify({"explanation": explanation, "topic": topic})


@app.route("/api/ai/study-plan", methods=["POST"])
def ai_study_plan():
    """Generate a personalized study plan based on current progress."""
    data = load_progress()
    today = date.today().isoformat()

    progress_summary = []
    for course in data["courses"]:
        cm = [m for m in data["materials"] if m["course_id"] == course["id"]]
        cc = [m for m in cm if m["id"] in data["completed_materials"]]
        upcoming = [d for d in data["deadlines"] if d["course_id"] == course["id"] and not d["done"] and d["date"] >= today]
        progress_summary.append(
            f"{course['name']}: {len(cc)}/{len(cm)} materials completed. "
            f"Upcoming deadlines: {', '.join(d['title'] + ' (' + d['date'] + ')' for d in upcoming[:3])}"
        )

    messages = [
        {"role": "system", "content": "You are a study planner. Based on the student's current progress and upcoming deadlines, create a focused, actionable study plan for the next 7 days. Be specific about what to study each day and for how long."},
        {"role": "user", "content": f"Today is {today}. Here's my progress:\n" + "\n".join(progress_summary)},
    ]

    plan = call_ai(messages, max_tokens=1500)
    return jsonify({"plan": plan, "generated_at": today})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
