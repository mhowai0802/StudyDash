"""Pre-populated course data for all 3 courses."""

INITIAL_COURSES = [
    {
        "id": "nlp",
        "name": "COMP7045 NLP & Large Language Model",
        "code": "COMP7045",
        "instructor": "Dr. Jing MA",
        "ta": "Fu Rao (csraofu@comp.hkbu.edu.hk)",
        "schedule": "Mon 18:30-21:20",
        "venue": "SCT502 (HSH Campus)",
        "color": "#6366f1",
        "assessment": {
            "continuous": {"weight": 50, "components": [
                {"name": "Assignments & Quizzes", "weight": "TBD (part of 50%)"},
                {"name": "Mini-Project (Presentation + Report)", "weight": "TBD (part of 50%)"}
            ]},
            "exam": {"weight": 50, "note": "Must score at least 30% to pass"}
        },
        "weeks": [
            {
                "week": 1, "date": "2026-01-12", "topic": "Course Information & Introduction to NLP",
                "details": "What is NLP, NLU vs NLG, why NLP is hard, ambiguity types, history of NLP",
                "has_lab": False, "has_quiz": False, "status": "missed"
            },
            {
                "week": 2, "date": "2026-01-19", "topic": "Text Preprocessing",
                "details": "Tokenization, stemming, lemmatization, stopword removal, regular expressions",
                "has_lab": False, "has_quiz": False, "status": "missed"
            },
            {
                "week": 3, "date": "2026-01-26", "topic": "Statistical Language Models",
                "details": "N-grams, probability estimation, smoothing techniques, perplexity",
                "has_lab": False, "has_quiz": False, "status": "missed"
            },
            {
                "week": 4, "date": "2026-02-02", "topic": "Syntactic Analysis",
                "details": "POS tagging, parsing (CFG, CKY algorithm), dependency parsing",
                "has_lab": False, "has_quiz": False, "status": "missed"
            },
            {
                "week": 5, "date": "2026-02-09", "topic": "Lab 1: Hugging Face & Colab",
                "details": "Text Preprocessing, Train a Language Model for Text Generation",
                "has_lab": True, "has_quiz": False, "status": "missed"
            },
            {
                "week": 6, "date": "2026-02-23", "topic": "Quiz + Word Embedding",
                "details": "Quiz/In-class Exercise, Word2Vec, GloVe, ELMo",
                "has_lab": False, "has_quiz": True, "status": "upcoming"
            },
            {
                "week": 7, "date": "2026-03-02", "topic": "Deep Neural Networks, Attention & Transformer",
                "details": "RNN, CNN, Attention mechanism, Transformer architecture",
                "has_lab": False, "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 8, "date": "2026-03-09", "topic": "Neural Language Models",
                "details": "Neural language models, pre-training, fine-tuning",
                "has_lab": False, "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 9, "date": "2026-03-16", "topic": "Lab 2: Text Classification & BERT",
                "details": "Train Text Classification Model, Word Embedding Visualization, BERT Model",
                "has_lab": True, "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 10, "date": "2026-03-23", "topic": "Large Language Model",
                "details": "LLM architecture, training, capabilities, limitations",
                "has_lab": False, "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 11, "date": "2026-03-30", "topic": "Quiz + Lab 3: Prompt Engineering & Toy LLM",
                "details": "Quiz 2, Prompt Engineering techniques, Train a toy LLM",
                "has_lab": True, "has_quiz": True, "status": "upcoming"
            },
            {
                "week": 12, "date": "2026-04-13", "topic": "NLP Applications & Course Review",
                "details": "Real-world NLP applications, course summary and review",
                "has_lab": False, "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 13, "date": "2026-04-20", "topic": "Mini-Project Presentation",
                "details": "~10 min presentation, graded by instructor, TA, and students",
                "has_lab": False, "has_quiz": False, "status": "upcoming"
            }
        ]
    },
    {
        "id": "cvpr",
        "name": "Computer Vision & Pattern Recognition",
        "code": "CVPR",
        "instructor": "Prof. Xiaoqing GUO",
        "ta": "Zhenshun LIU (cszsliu@comp.hkbu.edu.hk)",
        "schedule": "Thu 18:30-21:20 (Lecture 18:30-20:20, Lab 20:30-21:20)",
        "venue": "FSC801C, FSC801D",
        "color": "#f59e0b",
        "assessment": {
            "continuous": {"weight": 50, "components": [
                {"name": "2 In-class Quizzes", "weight": 5},
                {"name": "7 Lab Exercises", "weight": 10},
                {"name": "Group Project (Proposal 20% + Presentation 40% + Report 40%)", "weight": 35}
            ]},
            "exam": {"weight": 50, "note": "Must score at least 30% on exam AND 35% total to pass"}
        },
        "weeks": [
            {
                "week": 1, "date": "2026-01-15", "topic": "Introduction + Image Acquisition",
                "details": "CV applications, image acquisition, color models/spaces, sampling, quantization",
                "has_lab": False, "has_quiz": False, "status": "missed"
            },
            {
                "week": 2, "date": "2026-01-22", "topic": "Image Enhancement",
                "details": "Image enhancement techniques",
                "has_lab": True, "lab_name": "Lab 1", "has_quiz": False, "status": "missed"
            },
            {
                "week": 3, "date": "2026-01-29", "topic": "Feature Extractor",
                "details": "Feature extraction methods",
                "has_lab": True, "lab_name": "Lab 2", "has_quiz": False, "status": "missed"
            },
            {
                "week": 4, "date": "2026-02-05", "topic": "Image Classification & Segmentation",
                "details": "Classification and segmentation techniques",
                "has_lab": True, "lab_name": "Lab 3", "has_quiz": False, "status": "missed"
            },
            {
                "week": 5, "date": "2026-02-12", "topic": "Deep Learning for CVPR + Project Briefing",
                "details": "Deep learning approaches for CV, course project introduction. Quiz on Conventional CVPR.",
                "has_lab": False, "has_quiz": True, "quiz_name": "Quiz 1 (Conventional CVPR)", "status": "missed"
            },
            {
                "week": 6, "date": "2026-02-19", "topic": "Holiday (Chinese New Year)",
                "details": "No class", "has_lab": False, "has_quiz": False, "status": "holiday"
            },
            {
                "week": 7, "date": "2026-02-26", "topic": "Segmentation",
                "details": "Advanced segmentation methods with deep learning",
                "has_lab": True, "lab_name": "Lab 4", "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 8, "date": "2026-03-05", "topic": "Object Detection",
                "details": "Object detection algorithms and frameworks",
                "has_lab": True, "lab_name": "Lab 5", "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 9, "date": "2026-03-12", "topic": "Temporal Processing",
                "details": "Video and temporal data processing",
                "has_lab": True, "lab_name": "Lab 6", "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 10, "date": "2026-03-19", "topic": "Data Generation",
                "details": "Data augmentation and generation techniques",
                "has_lab": True, "lab_name": "Lab 7", "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 11, "date": "2026-03-26", "topic": "CVPR Review + Quiz 2",
                "details": "Course review, Quiz on DL-based CVPR. Optional project consultation.",
                "has_lab": False, "has_quiz": True, "quiz_name": "Quiz 2 (DL-based CVPR)", "status": "upcoming"
            },
            {
                "week": 12, "date": "2026-04-02", "topic": "Holiday (Easter)",
                "details": "No class", "has_lab": False, "has_quiz": False, "status": "holiday"
            },
            {
                "week": 13, "date": "2026-04-09", "topic": "Holiday (Easter)",
                "details": "No class", "has_lab": False, "has_quiz": False, "status": "holiday"
            },
            {
                "week": 14, "date": "2026-04-16", "topic": "Group Project Presentation",
                "details": "10 min/person + 5 min Q&A per group",
                "has_lab": False, "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 15, "date": "2026-04-23", "topic": "Group Project Presentation",
                "details": "10 min/person + 5 min Q&A per group",
                "has_lab": False, "has_quiz": False, "status": "upcoming"
            }
        ]
    },
    {
        "id": "it-forum",
        "name": "IT Forum",
        "code": "IT Forum",
        "instructor": "Various Speakers",
        "ta": "",
        "schedule": "Sat 9:30-11:30 (selected dates)",
        "venue": "SCT503, HKBU",
        "color": "#10b981",
        "assessment": {
            "continuous": {"weight": 100, "components": [
                {"name": "Attendance + Report Submission", "weight": 100}
            ]},
            "exam": {"weight": 0, "note": "No exam"}
        },
        "weeks": [
            {
                "week": 1, "date": "2026-01-17", "topic": "AI Agents in Action: Your Path to Cloud Innovation",
                "details": "Speakers: Diane Long & Lok Yeung (AWS). AWS Intro, GenAI in AWS, AgentCore, AI Use Cases, Kiro, AWS Certificates.",
                "has_lab": False, "has_quiz": False, "status": "past"
            },
            {
                "week": 2, "date": "2026-01-24", "topic": "IT Professional's Career Development in the AI Era",
                "details": "Speaker: Raymond Tsang (Alibaba Cloud Global Training Advisor in AI).",
                "has_lab": False, "has_quiz": False, "status": "past"
            },
            {
                "week": 3, "date": "2026-02-07", "topic": "Cyber Security Operations Trend in 2026",
                "details": "Speakers: Wilfred CW Leung & Yoga Yujia Tian (HKT). MDR, Next-Gen SOC.",
                "has_lab": False, "has_quiz": False, "status": "past"
            },
            {
                "week": 4, "date": "2026-02-28", "topic": "Generative AI and Business (Title TBD)",
                "details": "Speaker: Keith Li (Chairman, WTIA - HK Wireless Technology Industry Association).",
                "has_lab": False, "has_quiz": False, "status": "upcoming"
            },
            {
                "week": 5, "date": "2026-03-21", "topic": "Robotics and AI (Title TBD)",
                "details": "Speaker: Albert LAM (Co-Founder, Novelte Robotics).",
                "has_lab": False, "has_quiz": False, "status": "upcoming"
            }
        ]
    }
]

INITIAL_DEADLINES = [
    {"id": "nlp-quiz1", "course_id": "nlp", "title": "NLP Quiz 1", "date": "2026-02-23", "weight": "Part of 50% CA", "type": "quiz", "done": False},
    {"id": "cvpr-lab4", "course_id": "cvpr", "title": "CVPR Lab 4 Submission", "date": "2026-02-28", "weight": "~1.4%", "type": "lab", "done": False},
    {"id": "it-forum-4", "course_id": "it-forum", "title": "IT Forum: Keith Li Talk + Report", "date": "2026-02-28", "weight": "Attendance", "type": "talk", "done": False},
    {"id": "cvpr-labs-overdue", "course_id": "cvpr", "title": "CVPR Labs 1-3 (OVERDUE)", "date": "2026-02-21", "weight": "~4.3%", "type": "lab", "done": False},
    {"id": "cvpr-group", "course_id": "cvpr", "title": "CVPR Project Group Formation (OVERDUE)", "date": "2026-02-19", "weight": "Required", "type": "admin", "done": False},
    {"id": "cvpr-lab5", "course_id": "cvpr", "title": "CVPR Lab 5 Submission", "date": "2026-03-07", "weight": "~1.4%", "type": "lab", "done": False},
    {"id": "cvpr-lab6", "course_id": "cvpr", "title": "CVPR Lab 6 Submission", "date": "2026-03-14", "weight": "~1.4%", "type": "lab", "done": False},
    {"id": "cvpr-lab7", "course_id": "cvpr", "title": "CVPR Lab 7 Submission", "date": "2026-03-21", "weight": "~1.4%", "type": "lab", "done": False},
    {"id": "cvpr-proposal", "course_id": "cvpr", "title": "CVPR Project Proposal", "date": "2026-03-20", "weight": "7% (20% of 35%)", "type": "project", "done": False},
    {"id": "it-forum-5", "course_id": "it-forum", "title": "IT Forum: Albert LAM Talk + Report", "date": "2026-03-21", "weight": "Attendance", "type": "talk", "done": False},
    {"id": "cvpr-quiz2", "course_id": "cvpr", "title": "CVPR Quiz 2 (DL-based)", "date": "2026-03-26", "weight": "2.5%", "type": "quiz", "done": False},
    {"id": "nlp-quiz2", "course_id": "nlp", "title": "NLP Quiz 2", "date": "2026-03-30", "weight": "Part of 50% CA", "type": "quiz", "done": False},
    {"id": "nlp-report", "course_id": "nlp", "title": "NLP Mini-Project Report", "date": "2026-04-20", "weight": "Part of 50% CA", "type": "project", "done": False},
    {"id": "nlp-presentation", "course_id": "nlp", "title": "NLP Mini-Project Presentation", "date": "2026-04-20", "weight": "Part of 50% CA", "type": "project", "done": False},
    {"id": "cvpr-presentation", "course_id": "cvpr", "title": "CVPR Project Presentation", "date": "2026-04-16", "weight": "14% (40% of 35%)", "type": "project", "done": False},
    {"id": "cvpr-report", "course_id": "cvpr", "title": "CVPR Final Report + Code", "date": "2026-04-30", "weight": "14% (40% of 35%)", "type": "project", "done": False},
    {"id": "nlp-exam", "course_id": "nlp", "title": "NLP Final Exam", "date": "2026-05-15", "weight": "50%", "type": "exam", "done": False},
    {"id": "cvpr-exam", "course_id": "cvpr", "title": "CVPR Final Exam", "date": "2026-05-15", "weight": "50%", "type": "exam", "done": False},
]

XP_VALUES = {
    "lecture_slides": 10,
    "textbook_chapter": 20,
    "video": 15,
    "lab_exercise": 25,
    "quiz_prep": 20,
    "paper": 15,
    "note": 5,
    "other": 10,
    "week_complete_bonus": 10,
}

LEVELS = [
    {"level": 1, "name": "Beginner", "xp_required": 0},
    {"level": 2, "name": "Learner", "xp_required": 50},
    {"level": 3, "name": "Student", "xp_required": 150},
    {"level": 4, "name": "Scholar", "xp_required": 300},
    {"level": 5, "name": "Expert", "xp_required": 500},
    {"level": 6, "name": "Master", "xp_required": 750},
    {"level": 7, "name": "Grandmaster", "xp_required": 1000},
]
