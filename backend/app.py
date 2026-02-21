import os
import uuid
from datetime import datetime, date
from pathlib import Path

import requests as http_requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from database import (
    db, Course, Week, Deadline, StudyTask, Material,
    ChatHistory, UserStats, seed_from_initial_data, migrate_from_json,
)
from course_data import XP_VALUES, LEVELS
from study_plan_data import TASK_CATEGORIES
from project_data import COURSE_PROJECTS

load_dotenv()

app = Flask(__name__)
CORS(app)

DATA_DIR = Path(__file__).parent / "data"
MATERIALS_DIR = Path(__file__).parent / "materials"
DATA_DIR.mkdir(exist_ok=True)
MATERIALS_DIR.mkdir(exist_ok=True)
for cid in ["nlp", "cvpr", "it-forum"]:
    (MATERIALS_DIR / cid).mkdir(exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATA_DIR / 'studydash.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    json_path = DATA_DIR / "progress.json"
    if json_path.exists():
        migrate_from_json(app, json_path)
    else:
        seed_from_initial_data(app)


def get_xp():
    stats = UserStats.query.get(1)
    return stats.xp if stats else 0


def set_xp(val):
    stats = UserStats.query.get(1)
    if not stats:
        stats = UserStats(id=1, xp=val)
        db.session.add(stats)
    else:
        stats.xp = val
    db.session.commit()


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
        "current": current, "next": next_lvl, "xp": xp,
        "xp_to_next": next_lvl["xp_required"] - xp if next_lvl else 0,
    }


# ─── Course Routes ───


@app.route("/api/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    result = []
    for c in courses:
        d = c.to_dict()
        total_weeks = len([w for w in c.weeks if w.status != "holiday"])
        mats = Material.query.filter_by(course_id=c.id).all()
        completed = [m for m in mats if m.completed]
        d["total_materials"] = len(mats)
        d["completed_materials"] = len(completed)
        d["total_weeks"] = total_weeks
        result.append(d)
    return jsonify(result)


@app.route("/api/course/<course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    d = course.to_dict()
    mats = Material.query.filter_by(course_id=course_id).all()
    completed = [m for m in mats if m.completed]
    d["materials"] = [m.to_dict() for m in mats]
    d["completed_material_ids"] = [m.id for m in completed]
    d["total_materials"] = len(mats)
    d["completed_count"] = len(completed)
    return jsonify(d)


# ─── Project Routes ───


@app.route("/api/project/<course_id>", methods=["GET"])
def get_project(course_id):
    project = COURSE_PROJECTS.get(course_id)
    if not project:
        return jsonify({"error": "No project data for this course"}), 404
    return jsonify(project)


@app.route("/api/project/<course_id>/milestone/<milestone_id>/toggle", methods=["PATCH"])
def toggle_milestone(course_id, milestone_id):
    project = COURSE_PROJECTS.get(course_id)
    if not project:
        return jsonify({"error": "Not found"}), 404
    milestone = next((m for m in project["milestones"] if m["id"] == milestone_id), None)
    if not milestone:
        return jsonify({"error": "Milestone not found"}), 404
    milestone["done"] = not milestone["done"]
    return jsonify(milestone)


# ─── Material Routes ───


@app.route("/api/materials", methods=["POST"])
def add_material():
    file = request.files.get("file")
    mat_id = str(uuid.uuid4())
    course_id = request.form.get("course_id")
    title = request.form.get("title", "")
    mat_type = request.form.get("type", "other")

    material = Material(
        id=mat_id, course_id=course_id,
        week=int(request.form.get("week", 0)),
        title=title, type=mat_type,
        xp=XP_VALUES.get(mat_type, 10),
        created_at=datetime.now().isoformat(),
    )

    if file:
        safe_name = f"{mat_id}_{file.filename}"
        save_path = MATERIALS_DIR / course_id / safe_name
        file.save(str(save_path))
        material.file_path = str(save_path)
        material.file_name = file.filename
        if not title:
            material.title = file.filename
    else:
        material.url = request.form.get("url", "")

    db.session.add(material)
    db.session.commit()
    return jsonify(material.to_dict()), 201


@app.route("/api/materials/<material_id>", methods=["DELETE"])
def delete_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Not found"}), 404
    if material.file_path and os.path.exists(material.file_path):
        os.remove(material.file_path)
    if material.completed:
        xp = get_xp()
        set_xp(max(0, xp - material.xp))
    db.session.delete(material)
    db.session.commit()
    return jsonify({"ok": True})


@app.route("/api/materials/<material_id>/complete", methods=["PATCH"])
def toggle_material_complete(material_id):
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Not found"}), 404

    xp = get_xp()
    if material.completed:
        material.completed = False
        xp -= material.xp
    else:
        material.completed = True
        xp += material.xp
        week_mats = Material.query.filter_by(
            course_id=material.course_id, week=material.week
        ).all()
        if all(m.completed or m.id == material_id for m in week_mats) and len(week_mats) > 0:
            xp += XP_VALUES["week_complete_bonus"]

    set_xp(max(0, xp))
    db.session.commit()
    return jsonify({
        "completed": material.completed, "xp": get_xp(), "level": get_level(get_xp()),
    })


@app.route("/api/materials/file/<path:filepath>", methods=["GET"])
def serve_material(filepath):
    full_path = MATERIALS_DIR / filepath
    if not full_path.exists():
        return jsonify({"error": "File not found"}), 404
    return send_from_directory(full_path.parent, full_path.name)


@app.route("/api/materials/scan", methods=["POST"])
def scan_materials():
    """Scan materials folders for untracked files and auto-import them."""
    existing_paths = {m.file_path for m in Material.query.all() if m.file_path}
    existing_names = {m.file_name for m in Material.query.all() if m.file_name}

    new_count = 0
    ext_to_type = {
        ".pdf": "lecture_slides", ".pptx": "lecture_slides", ".ppt": "lecture_slides",
        ".docx": "note", ".doc": "note", ".txt": "note",
        ".py": "lab_exercise", ".ipynb": "lab_exercise", ".zip": "lab_exercise",
        ".mp4": "video", ".mp3": "video",
    }

    for course_dir in MATERIALS_DIR.iterdir():
        if not course_dir.is_dir() or course_dir.name.startswith("."):
            continue
        course_id = course_dir.name
        if not Course.query.get(course_id):
            continue

        for file_path in sorted(course_dir.rglob("*")):
            if not file_path.is_file() or file_path.name.startswith("."):
                continue
            str_path = str(file_path)
            if str_path in existing_paths or file_path.name in existing_names:
                continue

            ext = file_path.suffix.lower()
            mat_type = ext_to_type.get(ext, "other")

            material = Material(
                id=str(uuid.uuid4()), course_id=course_id, week=0,
                title=file_path.stem, type=mat_type,
                xp=XP_VALUES.get(mat_type, 10),
                file_path=str_path, file_name=file_path.name,
                created_at=datetime.now().isoformat(),
            )
            db.session.add(material)
            new_count += 1

    db.session.commit()
    return jsonify({"new_materials": new_count})


@app.route("/api/materials/<material_id>/week", methods=["PATCH"])
def assign_material_week(material_id):
    """Assign a material to a specific week."""
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Not found"}), 404
    body = request.json
    material.week = body.get("week", 0)
    db.session.commit()
    return jsonify(material.to_dict())


@app.route("/api/materials/auto-map", methods=["POST"])
def auto_map_materials():
    """Auto-assign materials to weeks based on filename patterns."""
    import re as re_mod

    NLP_MAP = [
        (r"about.this.course|course.info", 1),
        (r"lecture\s*1|introduction", 1),
        (r"lecture\s*2|text.preprocess", 2),
        (r"lecture\s*3|slm|statistical.lang", 3),
        (r"lecture\s*4|syntactic", 4),
        (r"lab\s*1|lab1", 5),
        (r"lecture\s*5|embedding", 6),
        (r"lecture\s*6|dl|deep.learn|neural.network", 7),
        (r"lab\s*2|lab2", 9),
        (r"lab\s*3|lab3|corpus", 11),
        (r"group.project|project.desc", 13),
    ]

    CVPR_MAP = [
        (r"chapter\s*1|ch1", 1),
        (r"chapter\s*2.*part\s*1|ch2.*p1", 2),
        (r"chapter\s*2.*part\s*2|ch2.*p2", 3),
        (r"chapter\s*2.*part\s*3|ch2.*p3", 4),
        (r"chapter\s*3|ch3|project.brief", 5),
        (r"quiz\s*1|quiz1", 5),
        (r"lab\s*1|lab1", 2),
        (r"lab\s*2|lab2", 3),
        (r"lab\s*3|lab3", 4),
        (r"lab\s*4|lab4", 7),
        (r"lab\s*5|lab5", 8),
        (r"lab\s*6|lab6", 9),
        (r"lab\s*7|lab7", 10),
    ]

    COURSE_MAPS = {"nlp": NLP_MAP, "cvpr": CVPR_MAP}
    mapped = 0

    for course_id, rules in COURSE_MAPS.items():
        materials = Material.query.filter_by(course_id=course_id).all()
        for mat in materials:
            if mat.week and mat.week > 0:
                continue
            fname = (mat.file_name or mat.title or "").lower()
            for pattern, week_num in rules:
                if re_mod.search(pattern, fname):
                    mat.week = week_num
                    mapped += 1
                    break

    db.session.commit()
    return jsonify({"mapped": mapped})


# ─── Deadline Routes ───


@app.route("/api/deadlines", methods=["GET"])
def get_deadlines():
    deadlines = Deadline.query.order_by(Deadline.date).all()
    today_str = date.today().isoformat()
    result = []
    for d in deadlines:
        dd = d.to_dict()
        if d.date < today_str and not d.done:
            dd["urgency"] = "overdue"
        elif d.date == today_str:
            dd["urgency"] = "today"
        else:
            days_away = (date.fromisoformat(d.date) - date.today()).days
            if days_away <= 7:
                dd["urgency"] = "this_week"
            elif days_away <= 14:
                dd["urgency"] = "next_week"
            else:
                dd["urgency"] = "future"
        result.append(dd)
    return jsonify(result)


@app.route("/api/deadlines/<deadline_id>/toggle", methods=["PATCH"])
def toggle_deadline(deadline_id):
    d = Deadline.query.get(deadline_id)
    if not d:
        return jsonify({"error": "Not found"}), 404
    d.done = not d.done
    db.session.commit()
    return jsonify(d.to_dict())


# ─── Stats ───


@app.route("/api/stats", methods=["GET"])
def get_stats():
    xp = get_xp()
    all_mats = Material.query.all()
    completed_mats = [m for m in all_mats if m.completed]
    all_deadlines = Deadline.query.all()
    done_deadlines = [d for d in all_deadlines if d.done]

    per_course = {}
    for course in Course.query.all():
        cm = [m for m in all_mats if m.course_id == course.id]
        cc = [m for m in cm if m.completed]
        per_course[course.id] = {
            "name": course.name, "total": len(cm), "completed": len(cc),
            "progress": round(len(cc) / len(cm) * 100) if cm else 0,
        }

    return jsonify({
        "xp": xp, "level": get_level(xp),
        "total_materials": len(all_mats),
        "completed_materials": len(completed_mats),
        "material_progress": round(len(completed_mats) / len(all_mats) * 100) if all_mats else 0,
        "total_deadlines": len(all_deadlines),
        "completed_deadlines": len(done_deadlines),
        "per_course": per_course,
        "xp_values": XP_VALUES, "levels": LEVELS,
    })


# ─── Study Tasks ───


@app.route("/api/study-tasks", methods=["GET"])
def get_study_tasks():
    tasks = StudyTask.query.order_by(StudyTask.date).all()
    return jsonify({"tasks": [t.to_dict() for t in tasks], "categories": TASK_CATEGORIES})


@app.route("/api/study-tasks/<task_id>/toggle", methods=["PATCH"])
def toggle_study_task(task_id):
    task = StudyTask.query.get(task_id)
    if not task:
        return jsonify({"error": "Not found"}), 404
    task.done = not task.done
    db.session.commit()
    return jsonify(task.to_dict())


@app.route("/api/study-tasks", methods=["POST"])
def add_study_task():
    body = request.json
    task = StudyTask(
        id=str(uuid.uuid4()), date=body.get("date"),
        course_id=body.get("course_id", ""),
        title=body.get("title", ""),
        hours=body.get("hours", 1),
        category=body.get("category", "review"),
        done=False,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.route("/api/study-tasks/<task_id>", methods=["DELETE"])
def delete_study_task(task_id):
    task = StudyTask.query.get(task_id)
    if not task:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(task)
    db.session.commit()
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
        "messages": messages, "temperature": temperature,
        "max_tokens": max_tokens, "top_p": 1, "stream": False,
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

    course = Course.query.get(course_context)
    course_info = ""
    if course:
        topics = ", ".join(w.topic for w in course.weeks)
        course_info = f"Course: {course.name}. Topics covered: {topics}."

    system_prompt = (
        "You are StudyDash AI, a helpful study assistant for a university student in Hong Kong. "
        "You help with course material understanding, exam preparation, and study strategies. "
        f"{course_info} "
        "Be concise, clear, and educational. Use examples when helpful."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    reply = call_ai(messages)
    entry = ChatHistory(
        id=str(uuid.uuid4()), course_id=course_context,
        user_message=user_message, ai_reply=reply,
        timestamp=datetime.now().isoformat(),
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict())


@app.route("/api/ai/quiz", methods=["POST"])
def ai_generate_quiz():
    import json as json_mod
    body = request.json
    course_id = body.get("course_id", "")
    week = body.get("week", None)
    topic = body.get("topic", "")

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    if week:
        w = Week.query.filter_by(course_id=course_id, week_num=week).first()
        if w:
            topic = f"{w.topic}: {w.details}"

    system_prompt = (
        "You are a quiz generator for university courses. Generate a quiz with 5 multiple-choice questions. "
        "Format your response as JSON with this structure: "
        '{"questions": [{"question": "...", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "correct": "A", "explanation": "..."}]}'
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate a quiz about: {topic} for the course {course.name}."},
    ]

    reply = call_ai(messages, temperature=0.5, max_tokens=2000)
    try:
        clean = reply.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
        quiz_data = json_mod.loads(clean)
    except (json_mod.JSONDecodeError, IndexError):
        quiz_data = {"raw": reply}

    return jsonify(quiz_data)


@app.route("/api/ai/summarize", methods=["POST"])
def ai_summarize():
    body = request.json
    material_id = body.get("material_id", "")
    material = Material.query.get(material_id)
    if not material or not material.file_path:
        return jsonify({"error": "Material not found or no file"}), 404

    try:
        reader = PdfReader(material.file_path)
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
    body = request.json
    topic = body.get("topic", "")
    course_id = body.get("course_id", "")
    course = Course.query.get(course_id)
    course_name = course.name if course else "your course"

    messages = [
        {"role": "system", "content": f"You are a university tutor for {course_name}. Explain topics clearly with examples, analogies, and key takeaways. Structure your explanation with headers and bullet points."},
        {"role": "user", "content": f"Explain this topic in detail: {topic}"},
    ]
    explanation = call_ai(messages, max_tokens=2000)
    return jsonify({"explanation": explanation, "topic": topic})


@app.route("/api/ai/study-plan", methods=["POST"])
def ai_study_plan():
    today_str = date.today().isoformat()
    courses = Course.query.all()
    progress_summary = []
    for course in courses:
        mats = Material.query.filter_by(course_id=course.id).all()
        completed = [m for m in mats if m.completed]
        upcoming = Deadline.query.filter(
            Deadline.course_id == course.id, Deadline.done == False, Deadline.date >= today_str
        ).order_by(Deadline.date).limit(3).all()
        progress_summary.append(
            f"{course.name}: {len(completed)}/{len(mats)} materials completed. "
            f"Upcoming deadlines: {', '.join(d.title + ' (' + d.date + ')' for d in upcoming)}"
        )

    messages = [
        {"role": "system", "content": "You are a study planner. Based on the student's current progress and upcoming deadlines, create a focused, actionable study plan for the next 7 days. Be specific about what to study each day and for how long."},
        {"role": "user", "content": f"Today is {today_str}. Here's my progress:\n" + "\n".join(progress_summary)},
    ]
    plan = call_ai(messages, max_tokens=1500)
    return jsonify({"plan": plan, "generated_at": today_str})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
