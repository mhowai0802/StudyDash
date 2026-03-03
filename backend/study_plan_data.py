"""
Pre-populated daily study tasks from Mar 1 to end of semester.
Replanned on March 1, 2026 — assuming ZERO revision done on any past lectures.

Current situation:
  - NLP: Weeks 1-6 unreviewed, Quiz 1 is TOMORROW (Mar 2)
  - CVPR: Weeks 1-5 unreviewed, Lab 4 overdue, Week 7 class missed
  - IT Forum: Keith Li talk missed (Feb 28)
  - No catch-up or revision has been done at all
"""

INITIAL_STUDY_TASKS = [
    # ═══════════════════════════════════════════════════════════════════
    #  PHASE 0: EMERGENCY — NLP QUIZ 1 CRAM (Mar 1)
    #  Quiz is TOMORROW. Zero prep done. Focus on high-impact topics.
    # ═══════════════════════════════════════════════════════════════════
    {"id": "r001", "date": "2026-03-01", "course_id": "nlp", "title": "CRAM NLP Weeks 1-2: NLP intro, ambiguity, tokenization, stemming, regex", "hours": 2, "category": "quiz-prep", "done": False},
    {"id": "r002", "date": "2026-03-01", "course_id": "nlp", "title": "CRAM NLP Week 3: N-grams, probability, smoothing, perplexity (most quiz-able!)", "hours": 2, "category": "quiz-prep", "done": False},
    {"id": "r003", "date": "2026-03-01", "course_id": "nlp", "title": "CRAM NLP Week 4: POS tagging, CFG, CKY parsing basics", "hours": 1.5, "category": "quiz-prep", "done": False},
    {"id": "r004", "date": "2026-03-01", "course_id": "nlp", "title": "CRAM NLP Week 6: Word2Vec, GloVe key concepts (if time permits)", "hours": 1, "category": "quiz-prep", "done": False},

    # ═══════════════════════════════════════════════════════════════════
    #  PHASE 1: CVPR CATCH-UP SPRINT (Mar 2 - Mar 8)
    #  Must catch up CVPR Weeks 1-5 before Thursday Mar 5 class
    #  Submit overdue CVPR Lab 4 ASAP
    #  Also email professors about missed work
    # ═══════════════════════════════════════════════════════════════════
    {"id": "r005", "date": "2026-03-02", "course_id": "nlp", "title": "NLP Quiz 1 (in class!) + Attend NLP Week 7: DNN, Attention, Transformer (18:30)", "hours": 3, "category": "attend", "done": False},
    {"id": "r006", "date": "2026-03-02", "course_id": "cvpr", "title": "Email Prof. GUO about missed Quiz 1, late labs & Week 7", "hours": 0.5, "category": "admin", "done": False},

    {"id": "r007", "date": "2026-03-03", "course_id": "cvpr", "title": "Catch-up CVPR Week 1: Image acquisition, color models, sampling", "hours": 2, "category": "catch-up", "done": False},
    {"id": "r008", "date": "2026-03-03", "course_id": "cvpr", "title": "Catch-up CVPR Week 2: Image enhancement techniques", "hours": 2, "category": "catch-up", "done": False},
    {"id": "r009", "date": "2026-03-03", "course_id": "nlp", "title": "Review NLP Week 7: Transformer architecture & self-attention", "hours": 1.5, "category": "review", "done": False},

    {"id": "r010", "date": "2026-03-04", "course_id": "cvpr", "title": "Catch-up CVPR Week 3: Feature extraction methods", "hours": 2, "category": "catch-up", "done": False},
    {"id": "r011", "date": "2026-03-04", "course_id": "cvpr", "title": "Catch-up CVPR Week 4: Image classification & segmentation", "hours": 2, "category": "catch-up", "done": False},
    {"id": "r012", "date": "2026-03-04", "course_id": "cvpr", "title": "Submit CVPR Lab 4 (overdue — submit ASAP)", "hours": 1.5, "category": "lab", "done": False},

    {"id": "r013", "date": "2026-03-05", "course_id": "cvpr", "title": "Catch-up CVPR Week 5: Deep learning for CVPR (morning)", "hours": 2, "category": "catch-up", "done": False},
    {"id": "r014", "date": "2026-03-05", "course_id": "cvpr", "title": "Attend CVPR Week 8: Object Detection + Lab 5 (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "r015", "date": "2026-03-06", "course_id": "cvpr", "title": "Catch-up CVPR Week 7: Segmentation (missed class — study slides)", "hours": 2, "category": "catch-up", "done": False},
    {"id": "r016", "date": "2026-03-06", "course_id": "cvpr", "title": "Complete & submit CVPR Lab 5", "hours": 1.5, "category": "lab", "done": False},

    {"id": "r017", "date": "2026-03-07", "course_id": "cvpr", "title": "Review CVPR Week 8: Object Detection (YOLO, R-CNN, SSD)", "hours": 2, "category": "review", "done": False},
    {"id": "r018", "date": "2026-03-07", "course_id": "cvpr", "title": "Contact classmates to form CVPR project group", "hours": 0.5, "category": "admin", "done": False},
    {"id": "r019", "date": "2026-03-07", "course_id": "nlp", "title": "Catch-up NLP Week 6: Word Embedding (Word2Vec, GloVe, ELMo)", "hours": 2, "category": "catch-up", "done": False},

    {"id": "r020", "date": "2026-03-08", "course_id": "nlp", "title": "NLP deep review: Weeks 1-4 (fill gaps from quiz cram)", "hours": 2.5, "category": "review", "done": False},
    {"id": "r021", "date": "2026-03-08", "course_id": "nlp", "title": "Read Jurafsky Ch.9-10: RNN, Attention, Transformers", "hours": 2, "category": "reading", "done": False},

    # ═══════════════════════════════════════════════════════════════════
    #  PHASE 2: STEADY STATE (Mar 9 - Mar 15)
    #  Keep up with new lectures + start CVPR project proposal
    # ═══════════════════════════════════════════════════════════════════
    {"id": "r022", "date": "2026-03-09", "course_id": "nlp", "title": "Attend NLP Week 8: Neural Language Models (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "r023", "date": "2026-03-10", "course_id": "nlp", "title": "Review Neural LM notes: pre-training & fine-tuning", "hours": 2, "category": "review", "done": False},
    {"id": "r024", "date": "2026-03-10", "course_id": "cvpr", "title": "CVPR project: research related papers & approaches", "hours": 2, "category": "project", "done": False},

    {"id": "r025", "date": "2026-03-11", "course_id": "cvpr", "title": "CVPR project: draft proposal outline with group", "hours": 2, "category": "project", "done": False},
    {"id": "r026", "date": "2026-03-11", "course_id": "cvpr", "title": "Pre-read Temporal Processing concepts for Thursday", "hours": 1.5, "category": "reading", "done": False},

    {"id": "r027", "date": "2026-03-12", "course_id": "cvpr", "title": "Attend CVPR Week 9: Temporal Processing + Lab 6 (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "r028", "date": "2026-03-13", "course_id": "cvpr", "title": "Complete & submit CVPR Lab 6", "hours": 1.5, "category": "lab", "done": False},
    {"id": "r029", "date": "2026-03-13", "course_id": "cvpr", "title": "CVPR project: write preliminary studies section", "hours": 2, "category": "project", "done": False},

    {"id": "r030", "date": "2026-03-14", "course_id": "cvpr", "title": "CVPR project: write methodology & design sections", "hours": 2.5, "category": "project", "done": False},
    {"id": "r031", "date": "2026-03-14", "course_id": "nlp", "title": "NLP review: Weeks 7-8 (Transformer, Neural LMs)", "hours": 2, "category": "review", "done": False},

    {"id": "r032", "date": "2026-03-15", "course_id": "nlp", "title": "Deep read on BERT, GPT architecture & pre-training", "hours": 2, "category": "reading", "done": False},
    {"id": "r033", "date": "2026-03-15", "course_id": "cvpr", "title": "CVPR project: polish proposal draft", "hours": 2, "category": "project", "done": False},

    # ═══════════════════════════════════════════════════════════════════
    #  PHASE 3: PROPOSAL + BOTH QUIZ 2s (Mar 16 - Mar 30)
    #  CVPR Proposal due Mar 20, Quiz 2 Mar 26, NLP Quiz 2 Mar 30
    # ═══════════════════════════════════════════════════════════════════
    {"id": "r034", "date": "2026-03-16", "course_id": "nlp", "title": "Attend NLP Week 9: Lab 2 — Text Classification & BERT (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "r035", "date": "2026-03-17", "course_id": "cvpr", "title": "CVPR project: refine proposal based on group feedback", "hours": 2.5, "category": "project", "done": False},
    {"id": "r036", "date": "2026-03-17", "course_id": "nlp", "title": "Review NLP Lab 2: BERT model training notes", "hours": 2, "category": "review", "done": False},

    {"id": "r037", "date": "2026-03-18", "course_id": "cvpr", "title": "Finalize CVPR project proposal for submission", "hours": 2.5, "category": "project", "done": False},
    {"id": "r038", "date": "2026-03-18", "course_id": "cvpr", "title": "Pre-read Data Generation concepts for Thursday", "hours": 1.5, "category": "reading", "done": False},

    {"id": "r039", "date": "2026-03-19", "course_id": "cvpr", "title": "Attend CVPR Week 10: Data Generation + Lab 7 (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "r040", "date": "2026-03-20", "course_id": "cvpr", "title": "SUBMIT: CVPR Project Proposal via Moodle (DEADLINE)", "hours": 1, "category": "deadline", "done": False},
    {"id": "r041", "date": "2026-03-20", "course_id": "cvpr", "title": "Complete & submit CVPR Lab 7", "hours": 1.5, "category": "lab", "done": False},

    {"id": "r042", "date": "2026-03-21", "course_id": "it-forum", "title": "Attend IT Forum: Albert LAM — Robotics & AI (9:30)", "hours": 2, "category": "attend", "done": False},
    {"id": "r043", "date": "2026-03-21", "course_id": "it-forum", "title": "Write & submit IT Forum report", "hours": 1.5, "category": "assignment", "done": False},
    {"id": "r044", "date": "2026-03-21", "course_id": "cvpr", "title": "CVPR Quiz 2 prep: review DL for CVPR + Segmentation", "hours": 2, "category": "quiz-prep", "done": False},

    {"id": "r045", "date": "2026-03-22", "course_id": "cvpr", "title": "CVPR Quiz 2 prep: Object Detection (YOLO, R-CNN, SSD)", "hours": 3, "category": "quiz-prep", "done": False},
    {"id": "r046", "date": "2026-03-22", "course_id": "nlp", "title": "Pre-read Large Language Models for Monday", "hours": 1.5, "category": "reading", "done": False},

    {"id": "r047", "date": "2026-03-23", "course_id": "nlp", "title": "Attend NLP Week 10: Large Language Model (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "r048", "date": "2026-03-24", "course_id": "cvpr", "title": "CVPR Quiz 2 prep: Temporal Processing & Data Generation", "hours": 3, "category": "quiz-prep", "done": False},

    {"id": "r049", "date": "2026-03-25", "course_id": "cvpr", "title": "CVPR Quiz 2 FINAL prep: full review + prepare cheat sheet", "hours": 3, "category": "quiz-prep", "done": False},
    {"id": "r050", "date": "2026-03-25", "course_id": "nlp", "title": "Review NLP Week 10: LLM architecture & capabilities", "hours": 1.5, "category": "review", "done": False},

    {"id": "r051", "date": "2026-03-26", "course_id": "cvpr", "title": "CVPR Quiz 2 + Review lecture (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "r052", "date": "2026-03-27", "course_id": "nlp", "title": "NLP Quiz 2 prep: Word Embedding (Word2Vec, GloVe, ELMo)", "hours": 3, "category": "quiz-prep", "done": False},

    {"id": "r053", "date": "2026-03-28", "course_id": "nlp", "title": "NLP Quiz 2 prep: Attention, Transformer, Neural LMs", "hours": 3, "category": "quiz-prep", "done": False},

    {"id": "r054", "date": "2026-03-29", "course_id": "nlp", "title": "NLP Quiz 2 FINAL prep: LLMs + full topic review", "hours": 3, "category": "quiz-prep", "done": False},

    {"id": "r055", "date": "2026-03-30", "course_id": "nlp", "title": "NLP Quiz 2 + Attend NLP Week 11: Lab 3 (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "r056", "date": "2026-03-31", "course_id": "cvpr", "title": "CVPR project: begin implementation / coding", "hours": 3, "category": "project", "done": False},
    {"id": "r057", "date": "2026-03-31", "course_id": "nlp", "title": "NLP mini-project: select topic & start literature review", "hours": 2, "category": "project", "done": False},

    # ═══════════════════════════════════════════════════════════════════
    #  PHASE 4: EASTER BREAK PROJECT SPRINT (Apr 1 - Apr 12)
    #  No classes. Focus: CVPR + NLP project implementation.
    # ═══════════════════════════════════════════════════════════════════
    {"id": "r058", "date": "2026-04-01", "course_id": "cvpr", "title": "CVPR project: core implementation (4h focused session)", "hours": 4, "category": "project", "done": False},

    {"id": "r059", "date": "2026-04-02", "course_id": "cvpr", "title": "CVPR project: implementation continued (Easter holiday)", "hours": 4, "category": "project", "done": False},

    {"id": "r060", "date": "2026-04-03", "course_id": "nlp", "title": "NLP mini-project: literature review & design approach", "hours": 3, "category": "project", "done": False},
    {"id": "r061", "date": "2026-04-03", "course_id": "cvpr", "title": "CVPR project: run experiments & collect results", "hours": 2, "category": "project", "done": False},

    {"id": "r062", "date": "2026-04-04", "course_id": "cvpr", "title": "CVPR project: experiments & result analysis", "hours": 4, "category": "project", "done": False},

    {"id": "r063", "date": "2026-04-05", "course_id": "nlp", "title": "NLP mini-project: start implementation / coding", "hours": 3, "category": "project", "done": False},
    {"id": "r064", "date": "2026-04-05", "course_id": "cvpr", "title": "CVPR project: additional experiments", "hours": 2, "category": "project", "done": False},

    {"id": "r065", "date": "2026-04-06", "course_id": "nlp", "title": "NLP mini-project: implementation continued (holiday)", "hours": 4, "category": "project", "done": False},

    {"id": "r066", "date": "2026-04-07", "course_id": "cvpr", "title": "CVPR project: finalize results & start slide deck", "hours": 3, "category": "project", "done": False},
    {"id": "r067", "date": "2026-04-07", "course_id": "nlp", "title": "NLP mini-project: run experiments", "hours": 2, "category": "project", "done": False},

    {"id": "r068", "date": "2026-04-08", "course_id": "cvpr", "title": "CVPR project: create presentation slides", "hours": 3, "category": "project", "done": False},
    {"id": "r069", "date": "2026-04-08", "course_id": "nlp", "title": "NLP mini-project: result analysis & write-up", "hours": 2, "category": "project", "done": False},

    {"id": "r070", "date": "2026-04-09", "course_id": "cvpr", "title": "CVPR project: rehearse presentation with group", "hours": 2, "category": "project", "done": False},

    {"id": "r071", "date": "2026-04-10", "course_id": "nlp", "title": "NLP mini-project: finalize implementation & results", "hours": 3, "category": "project", "done": False},

    {"id": "r072", "date": "2026-04-11", "course_id": "nlp", "title": "NLP mini-project: draft report", "hours": 3, "category": "project", "done": False},
    {"id": "r073", "date": "2026-04-11", "course_id": "cvpr", "title": "CVPR project: final presentation polish", "hours": 2, "category": "project", "done": False},

    {"id": "r074", "date": "2026-04-12", "course_id": "nlp", "title": "NLP mini-project: prepare presentation slides", "hours": 2, "category": "project", "done": False},
    {"id": "r075", "date": "2026-04-12", "course_id": "cvpr", "title": "CVPR project: dry-run presentation", "hours": 1, "category": "project", "done": False},

    # ═══════════════════════════════════════════════════════════════════
    #  PHASE 5: PRESENTATIONS & REPORT WRITING (Apr 13 - Apr 30)
    # ═══════════════════════════════════════════════════════════════════
    {"id": "r076", "date": "2026-04-13", "course_id": "nlp", "title": "Attend NLP Week 12: Applications + Course Review (18:30)", "hours": 3, "category": "attend", "done": False},
    {"id": "r077", "date": "2026-04-13", "course_id": "nlp", "title": "NLP mini-project: finalize report", "hours": 2, "category": "project", "done": False},

    {"id": "r078", "date": "2026-04-14", "course_id": "cvpr", "title": "CVPR project: final presentation rehearsal", "hours": 2, "category": "project", "done": False},
    {"id": "r079", "date": "2026-04-14", "course_id": "nlp", "title": "Start NLP exam revision notes", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r080", "date": "2026-04-15", "course_id": "cvpr", "title": "CVPR: last-minute presentation fixes", "hours": 1.5, "category": "project", "done": False},
    {"id": "r081", "date": "2026-04-15", "course_id": "nlp", "title": "NLP mini-project: polish presentation slides", "hours": 2, "category": "project", "done": False},

    {"id": "r082", "date": "2026-04-16", "course_id": "cvpr", "title": "CVPR Project Presentation (18:30) — present & demo", "hours": 3, "category": "attend", "done": False},

    {"id": "r083", "date": "2026-04-17", "course_id": "nlp", "title": "NLP mini-project: finalize everything for Monday submission", "hours": 3, "category": "project", "done": False},

    {"id": "r084", "date": "2026-04-18", "course_id": "nlp", "title": "NLP: rehearse presentation", "hours": 1.5, "category": "project", "done": False},
    {"id": "r085", "date": "2026-04-18", "course_id": "cvpr", "title": "Start CVPR final report writing", "hours": 2, "category": "project", "done": False},

    {"id": "r086", "date": "2026-04-19", "course_id": "nlp", "title": "NLP: final presentation dry run", "hours": 1, "category": "project", "done": False},
    {"id": "r087", "date": "2026-04-19", "course_id": "cvpr", "title": "CVPR final report: methodology & results sections", "hours": 3, "category": "project", "done": False},

    {"id": "r088", "date": "2026-04-20", "course_id": "nlp", "title": "NLP Mini-Project Presentation (18:30) + Submit Report", "hours": 3, "category": "attend", "done": False},

    {"id": "r089", "date": "2026-04-21", "course_id": "cvpr", "title": "CVPR final report: introduction & conclusion", "hours": 3, "category": "project", "done": False},

    {"id": "r090", "date": "2026-04-22", "course_id": "cvpr", "title": "CVPR final report: polish & proofread", "hours": 2, "category": "project", "done": False},
    {"id": "r091", "date": "2026-04-22", "course_id": "nlp", "title": "NLP exam prep: Weeks 1-4 review (NLP basics, parsing)", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r092", "date": "2026-04-23", "course_id": "cvpr", "title": "CVPR Presentation continued if needed (18:30)", "hours": 3, "category": "attend", "done": False},

    {"id": "r093", "date": "2026-04-24", "course_id": "cvpr", "title": "CVPR: clean up code for submission", "hours": 2, "category": "project", "done": False},
    {"id": "r094", "date": "2026-04-24", "course_id": "nlp", "title": "NLP exam prep: Weeks 5-8 review (embeddings, transformers)", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r095", "date": "2026-04-25", "course_id": "cvpr", "title": "CVPR: finalize report + PPT + code package", "hours": 3, "category": "project", "done": False},

    {"id": "r096", "date": "2026-04-26", "course_id": "nlp", "title": "NLP exam prep: Weeks 9-12 review (LLM, applications)", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r097", "date": "2026-04-26", "course_id": "cvpr", "title": "CVPR: final report review with group", "hours": 1.5, "category": "project", "done": False},

    {"id": "r098", "date": "2026-04-27", "course_id": "cvpr", "title": "CVPR exam prep: Weeks 1-5 (Conventional CVPR)", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r099", "date": "2026-04-27", "course_id": "nlp", "title": "NLP exam prep: practice problems & self-test", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r100", "date": "2026-04-28", "course_id": "cvpr", "title": "CVPR: absolute final report touches", "hours": 1.5, "category": "project", "done": False},
    {"id": "r101", "date": "2026-04-28", "course_id": "cvpr", "title": "CVPR exam prep: Weeks 7-11 (DL-based CVPR)", "hours": 2.5, "category": "exam-prep", "done": False},

    {"id": "r102", "date": "2026-04-29", "course_id": "cvpr", "title": "CVPR: prepare final submission package on Moodle", "hours": 1, "category": "deadline", "done": False},
    {"id": "r103", "date": "2026-04-29", "course_id": "nlp", "title": "NLP exam prep: comprehensive review all topics", "hours": 3, "category": "exam-prep", "done": False},

    {"id": "r104", "date": "2026-04-30", "course_id": "cvpr", "title": "SUBMIT: CVPR Final Report + Code via Moodle (DEADLINE)", "hours": 1, "category": "deadline", "done": False},
    {"id": "r105", "date": "2026-04-30", "course_id": "cvpr", "title": "CVPR exam prep: full review session", "hours": 3, "category": "exam-prep", "done": False},

    # ═══════════════════════════════════════════════════════════════════
    #  PHASE 6: FINAL EXAM PREP (May 1 - May 14)
    #  Both exams on May 15 — alternate between subjects daily
    # ═══════════════════════════════════════════════════════════════════
    {"id": "r106", "date": "2026-05-01", "course_id": "nlp", "title": "NLP exam: text preprocessing & statistical language models", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r107", "date": "2026-05-01", "course_id": "cvpr", "title": "CVPR exam: image processing fundamentals", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r108", "date": "2026-05-02", "course_id": "nlp", "title": "NLP exam: syntactic analysis & word embeddings", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r109", "date": "2026-05-02", "course_id": "cvpr", "title": "CVPR exam: feature extraction & classification", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r110", "date": "2026-05-03", "course_id": "nlp", "title": "NLP exam: Transformer, BERT, Neural LMs", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r111", "date": "2026-05-03", "course_id": "cvpr", "title": "CVPR exam: DL, segmentation, detection", "hours": 3, "category": "exam-prep", "done": False},

    {"id": "r112", "date": "2026-05-04", "course_id": "nlp", "title": "NLP exam: LLMs & applications, mock exam", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r113", "date": "2026-05-04", "course_id": "cvpr", "title": "CVPR exam: temporal, generation, full mock exam", "hours": 3, "category": "exam-prep", "done": False},

    {"id": "r114", "date": "2026-05-05", "course_id": "nlp", "title": "NLP exam: weak areas review + past paper practice", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r115", "date": "2026-05-05", "course_id": "cvpr", "title": "CVPR exam: weak areas review + past paper practice", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r116", "date": "2026-05-06", "course_id": "nlp", "title": "NLP exam: timed mock exam + review mistakes", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r117", "date": "2026-05-06", "course_id": "cvpr", "title": "CVPR exam: timed mock exam + review mistakes", "hours": 3, "category": "exam-prep", "done": False},

    {"id": "r118", "date": "2026-05-07", "course_id": "nlp", "title": "NLP exam: consolidate notes, create summary sheets", "hours": 2.5, "category": "exam-prep", "done": False},
    {"id": "r119", "date": "2026-05-07", "course_id": "cvpr", "title": "CVPR exam: consolidate notes, create summary sheets", "hours": 2.5, "category": "exam-prep", "done": False},

    {"id": "r120", "date": "2026-05-08", "course_id": "nlp", "title": "NLP exam: full revision — Weeks 1-6", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r121", "date": "2026-05-08", "course_id": "cvpr", "title": "CVPR exam: full revision — Conventional CVPR", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r122", "date": "2026-05-09", "course_id": "nlp", "title": "NLP exam: full revision — Weeks 7-12", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r123", "date": "2026-05-09", "course_id": "cvpr", "title": "CVPR exam: full revision — DL-based CVPR", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r124", "date": "2026-05-10", "course_id": "nlp", "title": "NLP exam: final mock exam + gap analysis", "hours": 3, "category": "exam-prep", "done": False},
    {"id": "r125", "date": "2026-05-10", "course_id": "cvpr", "title": "CVPR exam: final mock exam + gap analysis", "hours": 3, "category": "exam-prep", "done": False},

    {"id": "r126", "date": "2026-05-11", "course_id": "nlp", "title": "NLP exam: targeted review on weak topics", "hours": 2.5, "category": "exam-prep", "done": False},
    {"id": "r127", "date": "2026-05-11", "course_id": "cvpr", "title": "CVPR exam: targeted review on weak topics", "hours": 2.5, "category": "exam-prep", "done": False},

    {"id": "r128", "date": "2026-05-12", "course_id": "nlp", "title": "NLP exam: formula sheet & key concept cards", "hours": 2, "category": "exam-prep", "done": False},
    {"id": "r129", "date": "2026-05-12", "course_id": "cvpr", "title": "CVPR exam: formula sheet & key concept cards", "hours": 2, "category": "exam-prep", "done": False},

    {"id": "r130", "date": "2026-05-13", "course_id": "nlp", "title": "NLP exam: light review + rest (don't cram)", "hours": 1.5, "category": "exam-prep", "done": False},
    {"id": "r131", "date": "2026-05-13", "course_id": "cvpr", "title": "CVPR exam: light review + rest (don't cram)", "hours": 1.5, "category": "exam-prep", "done": False},

    {"id": "r132", "date": "2026-05-14", "course_id": "nlp", "title": "NLP exam: final glance at summary sheets, relax", "hours": 1, "category": "exam-prep", "done": False},
    {"id": "r133", "date": "2026-05-14", "course_id": "cvpr", "title": "CVPR exam: final glance at summary sheets, relax", "hours": 1, "category": "exam-prep", "done": False},
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
