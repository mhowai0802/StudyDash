import os
import uuid
from datetime import date

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client

from study_plan_data import TASK_CATEGORIES
from project_data import COURSE_PROJECTS

load_dotenv()

app = Flask(__name__)
CORS(app)

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY"),
)


# ─── Course Routes ───


@app.route("/api/courses", methods=["GET"])
def get_courses():
    courses = supabase.table("courses").select("*").execute().data
    weeks = supabase.table("weeks").select("*").execute().data
    tasks = supabase.table("study_tasks").select("id,course_id,done").execute().data

    result = []
    for c in courses:
        c["assessment"] = __import__("json").loads(c["assessment_json"]) if c.get("assessment_json") else {}
        c_weeks = [w for w in weeks if w["course_id"] == c["id"]]
        c["weeks"] = sorted(c_weeks, key=lambda w: w["week_num"])
        c["total_weeks"] = len([w for w in c_weeks if w.get("status") != "holiday"])
        c_tasks = [t for t in tasks if t["course_id"] == c["id"]]
        c["total_tasks"] = len(c_tasks)
        c["completed_tasks"] = len([t for t in c_tasks if t["done"]])
        result.append(c)
    return jsonify(result)


@app.route("/api/course/<course_id>", methods=["GET"])
def get_course(course_id):
    rows = supabase.table("courses").select("*").eq("id", course_id).execute().data
    if not rows:
        return jsonify({"error": "Course not found"}), 404
    c = rows[0]
    c["assessment"] = __import__("json").loads(c["assessment_json"]) if c.get("assessment_json") else {}
    weeks = supabase.table("weeks").select("*").eq("course_id", course_id).order("week_num").execute().data
    c["weeks"] = weeks
    c["total_weeks"] = len([w for w in weeks if w.get("status") != "holiday"])
    return jsonify(c)


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


# ─── Deadline Routes ───


@app.route("/api/deadlines", methods=["GET"])
def get_deadlines():
    deadlines = supabase.table("deadlines").select("*").order("date").execute().data
    today_str = date.today().isoformat()
    result = []
    for d in deadlines:
        if d["date"] < today_str and not d["done"]:
            d["urgency"] = "overdue"
        elif d["date"] == today_str:
            d["urgency"] = "today"
        else:
            days_away = (date.fromisoformat(d["date"]) - date.today()).days
            if days_away <= 7:
                d["urgency"] = "this_week"
            elif days_away <= 14:
                d["urgency"] = "next_week"
            else:
                d["urgency"] = "future"
        result.append(d)
    return jsonify(result)


@app.route("/api/deadlines/<deadline_id>/toggle", methods=["PATCH"])
def toggle_deadline(deadline_id):
    rows = supabase.table("deadlines").select("*").eq("id", deadline_id).execute().data
    if not rows:
        return jsonify({"error": "Not found"}), 404
    new_done = not rows[0]["done"]
    supabase.table("deadlines").update({"done": new_done}).eq("id", deadline_id).execute()
    updated = supabase.table("deadlines").select("*").eq("id", deadline_id).execute().data[0]
    return jsonify(updated)


# ─── Study Tasks ───


@app.route("/api/study-tasks", methods=["GET"])
def get_study_tasks():
    tasks = supabase.table("study_tasks").select("*").order("date").execute().data
    return jsonify({"tasks": tasks, "categories": TASK_CATEGORIES})


@app.route("/api/study-tasks/<task_id>/toggle", methods=["PATCH"])
def toggle_study_task(task_id):
    rows = supabase.table("study_tasks").select("*").eq("id", task_id).execute().data
    if not rows:
        return jsonify({"error": "Not found"}), 404
    new_done = not rows[0]["done"]
    supabase.table("study_tasks").update({"done": new_done}).eq("id", task_id).execute()
    updated = supabase.table("study_tasks").select("*").eq("id", task_id).execute().data[0]
    return jsonify(updated)


@app.route("/api/study-tasks", methods=["POST"])
def add_study_task():
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
    result = supabase.table("study_tasks").insert(task).execute()
    return jsonify(result.data[0]), 201


@app.route("/api/study-tasks/<task_id>", methods=["PATCH"])
def update_study_task(task_id):
    rows = supabase.table("study_tasks").select("*").eq("id", task_id).execute().data
    if not rows:
        return jsonify({"error": "Not found"}), 404
    body = request.json
    updates = {}
    for field in ("date", "title", "hours", "category", "course_id"):
        if field in body:
            updates[field] = body[field]
    supabase.table("study_tasks").update(updates).eq("id", task_id).execute()
    updated = supabase.table("study_tasks").select("*").eq("id", task_id).execute().data[0]
    return jsonify(updated)


@app.route("/api/study-tasks/<task_id>", methods=["DELETE"])
def delete_study_task(task_id):
    supabase.table("study_tasks").delete().eq("id", task_id).execute()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
