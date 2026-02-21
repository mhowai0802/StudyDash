"""SQLite database models and initialization for StudyDash."""

import json
from datetime import datetime
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    instructor = db.Column(db.String(200))
    ta = db.Column(db.String(200))
    schedule = db.Column(db.String(200))
    venue = db.Column(db.String(200))
    color = db.Column(db.String(20))
    assessment_json = db.Column(db.Text)

    weeks = db.relationship("Week", backref="course", cascade="all, delete-orphan")

    @property
    def assessment(self):
        return json.loads(self.assessment_json) if self.assessment_json else {}

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "code": self.code,
            "instructor": self.instructor, "ta": self.ta,
            "schedule": self.schedule, "venue": self.venue,
            "color": self.color, "assessment": self.assessment,
            "weeks": [w.to_dict() for w in sorted(self.weeks, key=lambda w: w.week_num)],
        }


class Week(db.Model):
    __tablename__ = "weeks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.String(50), db.ForeignKey("courses.id"), nullable=False)
    week_num = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20))
    topic = db.Column(db.String(300))
    details = db.Column(db.Text)
    has_lab = db.Column(db.Boolean, default=False)
    lab_name = db.Column(db.String(100))
    has_quiz = db.Column(db.Boolean, default=False)
    quiz_name = db.Column(db.String(100))
    status = db.Column(db.String(20))

    def to_dict(self):
        d = {
            "week": self.week_num, "date": self.date, "topic": self.topic,
            "details": self.details, "has_lab": self.has_lab, "has_quiz": self.has_quiz,
            "status": self.status,
        }
        if self.lab_name:
            d["lab_name"] = self.lab_name
        if self.quiz_name:
            d["quiz_name"] = self.quiz_name
        return d


class Deadline(db.Model):
    __tablename__ = "deadlines"
    id = db.Column(db.String(100), primary_key=True)
    course_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.String(100))
    type = db.Column(db.String(50))
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id, "course_id": self.course_id, "title": self.title,
            "date": self.date, "weight": self.weight, "type": self.type, "done": self.done,
        }


class StudyTask(db.Model):
    __tablename__ = "study_tasks"
    id = db.Column(db.String(100), primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    course_id = db.Column(db.String(50))
    title = db.Column(db.String(500), nullable=False)
    hours = db.Column(db.Float, default=1)
    category = db.Column(db.String(50))
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id, "date": self.date, "course_id": self.course_id,
            "title": self.title, "hours": self.hours, "category": self.category,
            "done": self.done,
        }


class Material(db.Model):
    __tablename__ = "materials"
    id = db.Column(db.String(100), primary_key=True)
    course_id = db.Column(db.String(50), nullable=False)
    week = db.Column(db.Integer, default=0)
    title = db.Column(db.String(300))
    type = db.Column(db.String(50))
    xp = db.Column(db.Integer, default=10)
    file_path = db.Column(db.String(500))
    file_name = db.Column(db.String(300))
    url = db.Column(db.String(500))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id, "course_id": self.course_id, "week": self.week,
            "title": self.title, "type": self.type, "xp": self.xp,
            "file_path": self.file_path, "file_name": self.file_name,
            "url": self.url, "completed": self.completed, "created_at": self.created_at,
        }


class ChatHistory(db.Model):
    __tablename__ = "chat_history"
    id = db.Column(db.String(100), primary_key=True)
    course_id = db.Column(db.String(50))
    user_message = db.Column(db.Text)
    ai_reply = db.Column(db.Text)
    timestamp = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id, "course_id": self.course_id,
            "user_message": self.user_message, "ai_reply": self.ai_reply,
            "timestamp": self.timestamp,
        }


class UserStats(db.Model):
    __tablename__ = "user_stats"
    id = db.Column(db.Integer, primary_key=True, default=1)
    xp = db.Column(db.Integer, default=0)


def seed_from_initial_data(app):
    """Populate the database with initial course data if tables are empty."""
    from course_data import INITIAL_COURSES, INITIAL_DEADLINES
    from study_plan_data import INITIAL_STUDY_TASKS

    with app.app_context():
        if Course.query.first():
            return

        for c_data in INITIAL_COURSES:
            weeks_data = c_data.pop("weeks", [])
            assessment = c_data.pop("assessment", {})
            course = Course(**c_data, assessment_json=json.dumps(assessment))
            db.session.add(course)

            for w in weeks_data:
                week = Week(
                    course_id=c_data["id"], week_num=w["week"], date=w.get("date"),
                    topic=w.get("topic"), details=w.get("details"),
                    has_lab=w.get("has_lab", False), lab_name=w.get("lab_name"),
                    has_quiz=w.get("has_quiz", False), quiz_name=w.get("quiz_name"),
                    status=w.get("status"),
                )
                db.session.add(week)

        for d_data in INITIAL_DEADLINES:
            db.session.add(Deadline(**d_data))

        for t_data in INITIAL_STUDY_TASKS:
            db.session.add(StudyTask(**t_data))

        db.session.add(UserStats(id=1, xp=0))
        db.session.commit()


def migrate_from_json(app, json_path: Path):
    """Migrate existing progress.json data into SQLite."""
    if not json_path.exists():
        return

    with app.app_context():
        if Course.query.first():
            return

        with open(json_path) as f:
            data = json.load(f)

        for c_data in data.get("courses", []):
            weeks_data = c_data.pop("weeks", [])
            assessment = c_data.pop("assessment", {})
            for key in ["total_materials", "completed_materials", "total_weeks"]:
                c_data.pop(key, None)
            course = Course(**c_data, assessment_json=json.dumps(assessment))
            db.session.add(course)

            for w in weeks_data:
                week = Week(
                    course_id=c_data["id"], week_num=w["week"], date=w.get("date"),
                    topic=w.get("topic"), details=w.get("details"),
                    has_lab=w.get("has_lab", False), lab_name=w.get("lab_name"),
                    has_quiz=w.get("has_quiz", False), quiz_name=w.get("quiz_name"),
                    status=w.get("status"),
                )
                db.session.add(week)

        for d_data in data.get("deadlines", []):
            d_data.pop("urgency", None)
            db.session.add(Deadline(**d_data))

        for t_data in data.get("study_tasks", []):
            db.session.add(StudyTask(**t_data))

        completed_ids = set(data.get("completed_materials", []))
        for m_data in data.get("materials", []):
            m = Material(
                id=m_data["id"], course_id=m_data["course_id"],
                week=m_data.get("week", 0), title=m_data.get("title"),
                type=m_data.get("type"), xp=m_data.get("xp", 10),
                file_path=m_data.get("file_path"), file_name=m_data.get("file_name"),
                url=m_data.get("url"), completed=m_data["id"] in completed_ids,
                created_at=m_data.get("created_at"),
            )
            db.session.add(m)

        for ch in data.get("chat_history", []):
            db.session.add(ChatHistory(**ch))

        db.session.add(UserStats(id=1, xp=data.get("xp", 0)))
        db.session.commit()

        backup = json_path.with_suffix(".json.bak")
        json_path.rename(backup)
