"""
Pre-populated daily study tasks from Feb 21 to end of semester.
Each task has a date, course context, description, estimated hours, and category.
"""

INITIAL_STUDY_TASKS = [
    # ── PHASE 0: EMERGENCY WEEKEND (Feb 21-22) ──
    {"id": "s001", "date": "2026-02-21", "course_id": "nlp", "title": "Crash study NLP Week 1: Intro to NLP, NLU vs NLG, ambiguity types", "hours": 3, "category": "catch-up", "done": False},
    {"id": "s002", "date": "2026-02-21", "course_id": "nlp", "title": "Crash study NLP Week 2: Tokenization, stemming, lemmatization, regex", "hours": 3, "category": "catch-up", "done": False},
    {"id": "s003", "date": "2026-02-21", "course_id": "cvpr", "title": "Email Prof. GUO about missed Quiz 1 & late labs", "hours": 0.5, "category": "admin", "done": False},
    {"id": "s004", "date": "2026-02-22", "course_id": "nlp", "title": "Crash study NLP Week 3: N-grams, probability estimation, smoothing, perplexity", "hours": 3, "category": "catch-up", "done": False},
    {"id": "s005", "date": "2026-02-22", "course_id": "nlp", "title": "Crash study NLP Week 4: POS tagging, CFG, CKY parsing, dependency parsing", "hours": 3, "category": "catch-up", "done": False},
    {"id": "s006", "date": "2026-02-22", "course_id": "nlp", "title": "Practice N-gram probability calculations for quiz", "hours": 1, "category": "quiz-prep", "done": False},

    # ── PHASE 1: FIRST CATCH-UP SPRINT (Feb 23 - Mar 1) ──
    {"id": "s007", "date": "2026-02-23", "course_id": "nlp", "title": "Attend NLP Week 6: Quiz + Word Embedding lecture (18:30)", "hours": 3, "category": "attend", "done": False},
    {"id": "s008", "date": "2026-02-23", "course_id": "nlp", "title": "Review quiz results and note weak areas", "hours": 1, "category": "review", "done": False},

    {"id": "s009", "date": "2026-02-24", "course_id": "cvpr", "title": "Study CVPR Week 1: Image acquisition, color models, sampling, quantization", "hours": 2, "category": "catch-up", "done": False},
    {"id": "s010", "date": "2026-02-24", "course_id": "cvpr", "title": "Study CVPR Week 2: Image enhancement techniques", "hours": 2, "category": "catch-up", "done": False},
    {"id": "s011", "date": "2026-02-24", "course_id": "cvpr", "title": "Work on CVPR Lab 1 (submit ASAP)", "hours": 2, "category": "lab", "done": False},

    {"id": "s012", "date": "2026-02-25", "course_id": "cvpr", "title": "Study CVPR Week 3: Feature extraction methods", "hours": 2, "category": "catch-up", "done": False},
    {"id": "s013", "date": "2026-02-25", "course_id": "cvpr", "title": "Complete & submit CVPR Labs 2 and 3", "hours": 3, "category": "lab", "done": False},

    {"id": "s014", "date": "2026-02-26", "course_id": "cvpr", "title": "Attend CVPR Week 7: Segmentation + Lab 4 (18:30)", "hours": 3, "category": "attend", "done": False},
    {"id": "s015", "date": "2026-02-26", "course_id": "nlp", "title": "Review NLP Word Embedding notes (Word2Vec, GloVe)", "hours": 1.5, "category": "review", "done": False},

    {"id": "s016", "date": "2026-02-27", "course_id": "cvpr", "title": "Study CVPR Week 4: Image classification & segmentation", "hours": 2, "category": "catch-up", "done": False},
    {"id": "s017", "date": "2026-02-27", "course_id": "cvpr", "title": "Study CVPR Week 5: Deep learning for CVPR", "hours": 2, "category": "catch-up", "done": False},
    {"id": "s018", "date": "2026-02-27", "course_id": "cvpr", "title": "Submit CVPR Lab 4 (48h deadline)", "hours": 1, "category": "lab", "done": False},

    {"id": "s019", "date": "2026-02-28", "course_id": "it-forum", "title": "Attend IT Forum: Keith Li - Generative AI & Business (9:30)", "hours": 2, "category": "attend", "done": False},
    {"id": "s020", "date": "2026-02-28", "course_id": "it-forum", "title": "Write & submit IT Forum report", "hours": 1.5, "category": "assignment", "done": False},
    {"id": "s021", "date": "2026-02-28", "course_id": "cvpr", "title": "Contact classmates to form CVPR project group", "hours": 0.5, "category": "admin", "done": False},

    {"id": "s022", "date": "2026-03-01", "course_id": "nlp", "title": "Deep review NLP Weeks 1-6 material, fill knowledge gaps", "hours": 3, "category": "review", "done": False},
    {"id": "s023", "date": "2026-03-01", "course_id": "nlp", "title": "Read Jurafsky Ch.6: Word Embeddings (Word2Vec, GloVe)", "hours": 1.5, "category": "reading", "done": False},

    # ── PHASE 2: STEADY CATCH-UP (Mar 2 - Mar 15) ──
    {"id": "s024", "date": "2026-03-02", "course_id": "nlp", "title": "Attend NLP Week 7: DNN, Attention, Transformer (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s025", "date": "2026-03-03", "course_id": "nlp", "title": "Review Transformer architecture & self-attention in depth", "hours": 2.5, "category": "review", "done": False},
    {"id": "s026", "date": "2026-03-03", "course_id": "cvpr", "title": "Study CVPR segmentation methods (catch up Week 7)", "hours": 2, "category": "review", "done": False},

    {"id": "s027", "date": "2026-03-04", "course_id": "nlp", "title": "Read Jurafsky Ch.9-10: RNN, Attention, Transformers", "hours": 2, "category": "reading", "done": False},
    {"id": "s028", "date": "2026-03-04", "course_id": "cvpr", "title": "Pre-read Object Detection concepts for Thursday", "hours": 2, "category": "reading", "done": False},

    {"id": "s029", "date": "2026-03-05", "course_id": "cvpr", "title": "Attend CVPR Week 8: Object Detection + Lab 5 (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s030", "date": "2026-03-06", "course_id": "cvpr", "title": "Submit CVPR Lab 5 (48h deadline)", "hours": 1.5, "category": "lab", "done": False},
    {"id": "s031", "date": "2026-03-06", "course_id": "cvpr", "title": "Review Object Detection notes (YOLO, R-CNN, SSD)", "hours": 2, "category": "review", "done": False},

    {"id": "s032", "date": "2026-03-07", "course_id": "nlp", "title": "NLP comprehensive review: Weeks 5-7 concepts", "hours": 3, "category": "review", "done": False},
    {"id": "s033", "date": "2026-03-07", "course_id": "cvpr", "title": "Brainstorm CVPR project topic ideas with group", "hours": 1, "category": "project", "done": False},

    {"id": "s034", "date": "2026-03-08", "course_id": "cvpr", "title": "CVPR cumulative review: Weeks 1-8 key concepts", "hours": 3, "category": "review", "done": False},
    {"id": "s035", "date": "2026-03-08", "course_id": "nlp", "title": "Practice Transformer concepts with examples", "hours": 1.5, "category": "review", "done": False},

    {"id": "s036", "date": "2026-03-09", "course_id": "nlp", "title": "Attend NLP Week 8: Neural Language Models (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s037", "date": "2026-03-10", "course_id": "nlp", "title": "Review Neural LM notes: pre-training, fine-tuning", "hours": 2, "category": "review", "done": False},
    {"id": "s038", "date": "2026-03-10", "course_id": "cvpr", "title": "CVPR project: research related papers and approaches", "hours": 2, "category": "project", "done": False},

    {"id": "s039", "date": "2026-03-11", "course_id": "cvpr", "title": "CVPR project: draft proposal outline with group", "hours": 2, "category": "project", "done": False},
    {"id": "s040", "date": "2026-03-11", "course_id": "cvpr", "title": "Pre-read Temporal Processing concepts for Thursday", "hours": 1.5, "category": "reading", "done": False},

    {"id": "s041", "date": "2026-03-12", "course_id": "cvpr", "title": "Attend CVPR Week 9: Temporal Processing + Lab 6 (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s042", "date": "2026-03-13", "course_id": "cvpr", "title": "Submit CVPR Lab 6 (48h deadline)", "hours": 1.5, "category": "lab", "done": False},
    {"id": "s043", "date": "2026-03-13", "course_id": "cvpr", "title": "CVPR project: write proposal preliminary studies section", "hours": 2, "category": "project", "done": False},

    {"id": "s044", "date": "2026-03-14", "course_id": "cvpr", "title": "CVPR project: write methodology & design sections", "hours": 3, "category": "project", "done": False},
    {"id": "s045", "date": "2026-03-14", "course_id": "nlp", "title": "NLP review: Weeks 7-8 (Transformer, Neural LMs)", "hours": 2, "category": "review", "done": False},

    {"id": "s046", "date": "2026-03-15", "course_id": "nlp", "title": "Read about BERT, GPT architecture and pre-training", "hours": 2, "category": "reading", "done": False},
    {"id": "s047", "date": "2026-03-15", "course_id": "cvpr", "title": "CVPR project: polish proposal draft", "hours": 2, "category": "project", "done": False},

    # ── PHASE 3: PROJECT RAMP-UP + QUIZ 2 PREP (Mar 16 - Mar 30) ──
    {"id": "s048", "date": "2026-03-16", "course_id": "nlp", "title": "Attend NLP Week 9: Lab 2 - Text Classification, BERT (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s049", "date": "2026-03-17", "course_id": "cvpr", "title": "CVPR project: refine proposal based on feedback", "hours": 2.5, "category": "project", "done": False},
    {"id": "s050", "date": "2026-03-17", "course_id": "nlp", "title": "Review NLP Lab 2: BERT model training", "hours": 2, "category": "review", "done": False},

    {"id": "s051", "date": "2026-03-18", "course_id": "cvpr", "title": "Finalize CVPR project proposal for submission", "hours": 2.5, "category": "project", "done": False},
    {"id": "s052", "date": "2026-03-18", "course_id": "cvpr", "title": "Pre-read Data Generation concepts for Thursday", "hours": 1.5, "category": "reading", "done": False},

    {"id": "s053", "date": "2026-03-19", "course_id": "cvpr", "title": "Attend CVPR Week 10: Data Generation + Lab 7 (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s054", "date": "2026-03-20", "course_id": "cvpr", "title": "SUBMIT: CVPR Project Proposal via Moodle (DEADLINE)", "hours": 1, "category": "deadline", "done": False},
    {"id": "s055", "date": "2026-03-20", "course_id": "cvpr", "title": "Submit CVPR Lab 7 (48h deadline)", "hours": 1.5, "category": "lab", "done": False},

    {"id": "s056", "date": "2026-03-21", "course_id": "it-forum", "title": "Attend IT Forum: Albert LAM - Robotics & AI (9:30)", "hours": 2, "category": "attend", "done": False},
    {"id": "s057", "date": "2026-03-21", "course_id": "it-forum", "title": "Write & submit IT Forum report", "hours": 1.5, "category": "assignment", "done": False},
    {"id": "s058", "date": "2026-03-21", "course_id": "cvpr", "title": "Begin CVPR Quiz 2 prep: review DL for CVPR concepts", "hours": 2, "category": "quiz-prep", "done": False},

    {"id": "s059", "date": "2026-03-22", "course_id": "cvpr", "title": "CVPR Quiz 2 prep: Segmentation methods & architectures", "hours": 3, "category": "quiz-prep", "done": False},
    {"id": "s060", "date": "2026-03-22", "course_id": "nlp", "title": "Read about Large Language Models (prep for Monday)", "hours": 1.5, "category": "reading", "done": False},

    {"id": "s061", "date": "2026-03-23", "course_id": "nlp", "title": "Attend NLP Week 10: Large Language Model (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s062", "date": "2026-03-24", "course_id": "cvpr", "title": "CVPR Quiz 2 prep: Object Detection (YOLO, R-CNN, SSD)", "hours": 3, "category": "quiz-prep", "done": False},

    {"id": "s063", "date": "2026-03-25", "course_id": "cvpr", "title": "CVPR Quiz 2 prep: Temporal Processing & Data Generation", "hours": 2.5, "category": "quiz-prep", "done": False},
    {"id": "s064", "date": "2026-03-25", "course_id": "cvpr", "title": "Prepare A4 cheat sheet for CVPR Quiz 2", "hours": 1.5, "category": "quiz-prep", "done": False},

    {"id": "s065", "date": "2026-03-26", "course_id": "cvpr", "title": "CVPR Quiz 2 + Review lecture (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s066", "date": "2026-03-27", "course_id": "nlp", "title": "NLP Quiz 2 prep: Word Embedding (Word2Vec, GloVe, ELMo)", "hours": 3, "category": "quiz-prep", "done": False},

    {"id": "s067", "date": "2026-03-28", "course_id": "nlp", "title": "NLP Quiz 2 prep: Attention, Transformer, Neural LMs", "hours": 3, "category": "quiz-prep", "done": False},

    {"id": "s068", "date": "2026-03-29", "course_id": "nlp", "title": "NLP Quiz 2 prep: LLMs, full review of all topics", "hours": 3, "category": "quiz-prep", "done": False},

    {"id": "s069", "date": "2026-03-30", "course_id": "nlp", "title": "Attend NLP Week 11: Quiz 2 + Lab 3 (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s070", "date": "2026-03-31", "course_id": "cvpr", "title": "CVPR project: begin implementation / coding", "hours": 3, "category": "project", "done": False},
    {"id": "s071", "date": "2026-03-31", "course_id": "nlp", "title": "NLP mini-project: select topic & start literature review", "hours": 2, "category": "project", "done": False},

    # ── PHASE 4: EASTER BREAK PROJECT SPRINT (Apr 1 - Apr 12) ──
    {"id": "s072", "date": "2026-04-01", "course_id": "cvpr", "title": "CVPR project: core implementation (4h focused session)", "hours": 4, "category": "project", "done": False},

    {"id": "s073", "date": "2026-04-02", "course_id": "cvpr", "title": "CVPR project: implementation continued (Easter holiday)", "hours": 4, "category": "project", "done": False},

    {"id": "s074", "date": "2026-04-03", "course_id": "nlp", "title": "NLP mini-project: literature review & design approach", "hours": 3, "category": "project", "done": False},
    {"id": "s075", "date": "2026-04-03", "course_id": "cvpr", "title": "CVPR project: run experiments & collect results", "hours": 2, "category": "project", "done": False},

    {"id": "s076", "date": "2026-04-04", "course_id": "cvpr", "title": "CVPR project: experiments & result analysis", "hours": 4, "category": "project", "done": False},

    {"id": "s077", "date": "2026-04-05", "course_id": "nlp", "title": "NLP mini-project: start implementation / coding", "hours": 3, "category": "project", "done": False},
    {"id": "s078", "date": "2026-04-05", "course_id": "cvpr", "title": "CVPR project: additional experiments", "hours": 2, "category": "project", "done": False},

    {"id": "s079", "date": "2026-04-06", "course_id": "nlp", "title": "NLP mini-project: implementation continued (holiday)", "hours": 4, "category": "project", "done": False},

    {"id": "s080", "date": "2026-04-07", "course_id": "cvpr", "title": "CVPR project: finalize results & start slide deck", "hours": 3, "category": "project", "done": False},
    {"id": "s081", "date": "2026-04-07", "course_id": "nlp", "title": "NLP mini-project: run experiments", "hours": 2, "category": "project", "done": False},

    {"id": "s082", "date": "2026-04-08", "course_id": "cvpr", "title": "CVPR project: create presentation slides", "hours": 3, "category": "project", "done": False},
    {"id": "s083", "date": "2026-04-08", "course_id": "nlp", "title": "NLP mini-project: result analysis & write-up", "hours": 2, "category": "project", "done": False},

    {"id": "s084", "date": "2026-04-09", "course_id": "cvpr", "title": "CVPR project: rehearse presentation with group", "hours": 2, "category": "project", "done": False},

    {"id": "s085", "date": "2026-04-10", "course_id": "nlp", "title": "NLP mini-project: finalize implementation & results", "hours": 3, "category": "project", "done": False},

    {"id": "s086", "date": "2026-04-11", "course_id": "nlp", "title": "NLP mini-project: draft report", "hours": 3, "category": "project", "done": False},
    {"id": "s087", "date": "2026-04-11", "course_id": "cvpr", "title": "CVPR project: final presentation polish", "hours": 2, "category": "project", "done": False},

    {"id": "s088", "date": "2026-04-12", "course_id": "nlp", "title": "NLP mini-project: prepare presentation slides", "hours": 2, "category": "project", "done": False},
    {"id": "s089", "date": "2026-04-12", "course_id": "cvpr", "title": "CVPR project: dry-run presentation", "hours": 1, "category": "project", "done": False},

    # ── PHASE 5: PRESENTATIONS & FINALS (Apr 13 - Apr 30) ──
    {"id": "s090", "date": "2026-04-13", "course_id": "nlp", "title": "Attend NLP Week 12: Applications + Course Review (18:30)", "hours": 3, "category": "attend", "done": False},
    {"id": "s091", "date": "2026-04-13", "course_id": "nlp", "title": "NLP mini-project: finalize report", "hours": 2, "category": "project", "done": False},

    {"id": "s092", "date": "2026-04-14", "course_id": "cvpr", "title": "CVPR project: final presentation rehearsal", "hours": 2, "category": "project", "done": False},
    {"id": "s093", "date": "2026-04-14", "course_id": "nlp", "title": "Start NLP exam revision notes", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "s094", "date": "2026-04-15", "course_id": "cvpr", "title": "CVPR: last-minute presentation fixes", "hours": 1.5, "category": "project", "done": False},
    {"id": "s095", "date": "2026-04-15", "course_id": "nlp", "title": "NLP mini-project: polish presentation slides", "hours": 2, "category": "project", "done": False},

    {"id": "s096", "date": "2026-04-16", "course_id": "cvpr", "title": "CVPR Project Presentation (18:30) - present & demo", "hours": 3, "category": "attend", "done": False},

    {"id": "s097", "date": "2026-04-17", "course_id": "nlp", "title": "NLP mini-project: finalize everything for Monday", "hours": 3, "category": "project", "done": False},

    {"id": "s098", "date": "2026-04-18", "course_id": "nlp", "title": "NLP: rehearse presentation", "hours": 1.5, "category": "project", "done": False},
    {"id": "s099", "date": "2026-04-18", "course_id": "cvpr", "title": "Start CVPR final report writing", "hours": 2, "category": "project", "done": False},

    {"id": "s100", "date": "2026-04-19", "course_id": "nlp", "title": "NLP: final presentation dry run", "hours": 1, "category": "project", "done": False},
    {"id": "s101", "date": "2026-04-19", "course_id": "cvpr", "title": "CVPR final report: methodology & results sections", "hours": 3, "category": "project", "done": False},

    {"id": "s102", "date": "2026-04-20", "course_id": "nlp", "title": "NLP Mini-Project Presentation (18:30) + Submit Report", "hours": 3, "category": "attend", "done": False},

    {"id": "s103", "date": "2026-04-21", "course_id": "cvpr", "title": "CVPR final report: introduction & conclusion", "hours": 3, "category": "project", "done": False},

    {"id": "s104", "date": "2026-04-22", "course_id": "cvpr", "title": "CVPR final report: polish & proofread", "hours": 2, "category": "project", "done": False},
    {"id": "s105", "date": "2026-04-22", "course_id": "nlp", "title": "NLP exam prep: Weeks 1-4 review", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "s106", "date": "2026-04-23", "course_id": "cvpr", "title": "CVPR Presentation continued if needed (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "s107", "date": "2026-04-24", "course_id": "cvpr", "title": "CVPR: clean up code for submission", "hours": 2, "category": "project", "done": False},
    {"id": "s108", "date": "2026-04-24", "course_id": "nlp", "title": "NLP exam prep: Weeks 5-8 review", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "s109", "date": "2026-04-25", "course_id": "cvpr", "title": "CVPR: finalize report + PPT + code package", "hours": 3, "category": "project", "done": False},

    {"id": "s110", "date": "2026-04-26", "course_id": "nlp", "title": "NLP exam prep: Weeks 9-12 review (LLM focus)", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "s111", "date": "2026-04-26", "course_id": "cvpr", "title": "CVPR: final report review with group", "hours": 1.5, "category": "project", "done": False},

    {"id": "s112", "date": "2026-04-27", "course_id": "cvpr", "title": "CVPR exam prep: Weeks 1-5 (Conventional CVPR)", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "s113", "date": "2026-04-27", "course_id": "nlp", "title": "NLP exam prep: practice problems", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "s114", "date": "2026-04-28", "course_id": "cvpr", "title": "CVPR: absolute final report touches", "hours": 1.5, "category": "project", "done": False},
    {"id": "s115", "date": "2026-04-28", "course_id": "cvpr", "title": "CVPR exam prep: Weeks 7-11 (DL-based CVPR)", "hours": 2.5, "category": "exam-prep", "done": False},

    {"id": "s116", "date": "2026-04-29", "course_id": "cvpr", "title": "CVPR: prepare final submission package on Moodle", "hours": 1, "category": "deadline", "done": False},
    {"id": "s117", "date": "2026-04-29", "course_id": "nlp", "title": "NLP exam prep: comprehensive review", "hours": 3, "category": "exam-prep", "done": False},

    {"id": "s118", "date": "2026-04-30", "course_id": "cvpr", "title": "SUBMIT: CVPR Final Report + Code via Moodle (DEADLINE)", "hours": 1, "category": "deadline", "done": False},
    {"id": "s119", "date": "2026-04-30", "course_id": "cvpr", "title": "CVPR exam prep: full review session", "hours": 3, "category": "exam-prep", "done": False},

    # ── PHASE 6: FINAL EXAM PREP (May) ──
    {"id": "s120", "date": "2026-05-01", "course_id": "nlp", "title": "NLP exam prep: text preprocessing & language models", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "s121", "date": "2026-05-01", "course_id": "cvpr", "title": "CVPR exam prep: image processing fundamentals", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "s122", "date": "2026-05-02", "course_id": "nlp", "title": "NLP exam prep: syntactic analysis & word embeddings", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "s123", "date": "2026-05-02", "course_id": "cvpr", "title": "CVPR exam prep: feature extraction & classification", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "s124", "date": "2026-05-03", "course_id": "nlp", "title": "NLP exam prep: Transformer, BERT, Neural LMs", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "s125", "date": "2026-05-03", "course_id": "cvpr", "title": "CVPR exam prep: DL, segmentation, detection", "hours": 3, "category": "exam-prep", "done": False},

    {"id": "s126", "date": "2026-05-04", "course_id": "nlp", "title": "NLP exam prep: LLMs & applications, mock exam", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "s127", "date": "2026-05-04", "course_id": "cvpr", "title": "CVPR exam prep: temporal, generation, full mock exam", "hours": 3, "category": "exam-prep", "done": False},
]

TASK_CATEGORIES = {
    "attend": {"label": "Attend Class", "color": "#6366f1"},
    "catch-up": {"label": "Catch Up", "color": "#f43f5e"},
    "review": {"label": "Review", "color": "#38bdf8"},
    "reading": {"label": "Reading", "color": "#a855f7"},
    "lab": {"label": "Lab Work", "color": "#10b981"},
    "quiz-prep": {"label": "Quiz Prep", "color": "#f59e0b"},
    "exam-prep": {"label": "Exam Prep", "color": "#ef4444"},
    "project": {"label": "Project", "color": "#8b5cf6"},
    "assignment": {"label": "Assignment", "color": "#14b8a6"},
    "admin": {"label": "Admin", "color": "#6b7280"},
    "deadline": {"label": "Deadline", "color": "#f43f5e"},
}
