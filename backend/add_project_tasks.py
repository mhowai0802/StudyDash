"""One-time script to add detailed project planning tasks to the calendar."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app import app, db
from database import StudyTask

NEW_TASKS = [
    # ── NLP Mini-Project: Early Planning ──
    {"id": "sp-nlp-01", "date": "2026-03-09", "course_id": "nlp", "title": "NLP project: brainstorm topic ideas, review project description", "hours": 1.5, "category": "project"},
    {"id": "sp-nlp-02", "date": "2026-03-14", "course_id": "nlp", "title": "NLP project: decide on topic, identify 3-5 key papers", "hours": 2, "category": "project"},
    {"id": "sp-nlp-03", "date": "2026-03-20", "course_id": "nlp", "title": "NLP project: read related papers, take notes on approaches", "hours": 2.5, "category": "project"},
    {"id": "sp-nlp-04", "date": "2026-03-22", "course_id": "nlp", "title": "NLP project: design methodology & plan experiments", "hours": 2, "category": "project"},
    {"id": "sp-nlp-05", "date": "2026-03-28", "course_id": "nlp", "title": "NLP project: set up code repo, install dependencies, get dataset", "hours": 2, "category": "project"},

    # ── CVPR Group Project: Detailed Early Planning ──
    {"id": "sp-cvpr-01", "date": "2026-02-23", "course_id": "cvpr", "title": "CVPR project: message classmates to form group", "hours": 0.5, "category": "project"},
    {"id": "sp-cvpr-02", "date": "2026-02-26", "course_id": "cvpr", "title": "CVPR project: confirm group members, submit member list", "hours": 0.5, "category": "project"},
    {"id": "sp-cvpr-03", "date": "2026-03-01", "course_id": "cvpr", "title": "CVPR project: discuss task options with group (segmentation/detection/classification)", "hours": 1, "category": "project"},
    {"id": "sp-cvpr-04", "date": "2026-03-03", "course_id": "cvpr", "title": "CVPR project: decide task & find 2-3 candidate datasets", "hours": 1.5, "category": "project"},
    {"id": "sp-cvpr-05", "date": "2026-03-08", "course_id": "cvpr", "title": "CVPR project: read 3-5 related papers on chosen task", "hours": 2.5, "category": "project"},
    {"id": "sp-cvpr-06", "date": "2026-03-09", "course_id": "cvpr", "title": "CVPR project: outline proposal structure, assign writing sections", "hours": 1, "category": "project"},
    {"id": "sp-cvpr-07", "date": "2026-03-12", "course_id": "cvpr", "title": "CVPR project: write preliminary studies section of proposal", "hours": 2, "category": "project"},
    {"id": "sp-cvpr-08", "date": "2026-03-14", "course_id": "cvpr", "title": "CVPR project: write methodology section of proposal", "hours": 2, "category": "project"},
    {"id": "sp-cvpr-09", "date": "2026-03-16", "course_id": "cvpr", "title": "CVPR project: write initial design & timeline in proposal", "hours": 1.5, "category": "project"},
    {"id": "sp-cvpr-10", "date": "2026-03-19", "course_id": "cvpr", "title": "CVPR project: group review proposal draft, polish & proofread", "hours": 1.5, "category": "project"},
    {"id": "sp-cvpr-11", "date": "2026-03-27", "course_id": "cvpr", "title": "CVPR project: set up PyTorch codebase & data loader", "hours": 2, "category": "project"},
    {"id": "sp-cvpr-12", "date": "2026-03-29", "course_id": "cvpr", "title": "CVPR project: implement baseline model (e.g. U-Net / YOLO)", "hours": 3, "category": "project"},
]

def main():
    with app.app_context():
        existing_ids = {t.id for t in StudyTask.query.all()}
        added = 0
        for t in NEW_TASKS:
            if t["id"] in existing_ids:
                continue
            task = StudyTask(id=t["id"], date=t["date"], course_id=t["course_id"],
                             title=t["title"], hours=t["hours"], category=t["category"], done=False)
            db.session.add(task)
            added += 1
        db.session.commit()
        print(f"Added {added} new project tasks to calendar")

if __name__ == "__main__":
    main()
