import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="docs/NewsScope_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # LIGHT THEME PALETTE
    # ==========================================
    BG_LIGHT = RGBColor(248, 250, 252)      # Soft Slate Light Gray (#f8fafc)
    CARD_BG = RGBColor(255, 255, 255)       # Pure White (#ffffff)
    CARD_BG_ALT = RGBColor(241, 245, 249)   # Light Card Tint (#f1f5f9)
    BORDER_COLOR = RGBColor(226, 232, 240)  # Border Gray (#e2e8f0)
    BORDER_ACCENT = RGBColor(199, 210, 254) # Light Indigo Border (#c7d2fe)

    NAVY_DARK = RGBColor(15, 23, 42)        # Deep Charcoal/Navy (#0f172a)
    TEXT_BODY = RGBColor(51, 65, 85)        # Slate Body Text (#334155)
    TEXT_MUTED = RGBColor(100, 116, 139)    # Muted Slate (#64748b)

    INDIGO_PRIMARY = RGBColor(79, 70, 229)  # Indigo 600 (#4f46e5)
    INDIGO_LIGHT = RGBColor(238, 242, 255)  # Indigo 50 (#eef2ff)
    EMERALD_GREEN = RGBColor(5, 150, 105)   # Emerald 600 (#059669)
    EMERALD_LIGHT = RGBColor(236, 253, 245) # Emerald 50 (#ecfdf5)
    ROSE_RED = RGBColor(225, 29, 72)        # Rose 600 (#e11d48)
    ROSE_LIGHT = RGBColor(255, 241, 242)    # Rose 50 (#fff1f2)

    def set_slide_background(slide, color=BG_LIGHT):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, section_tag, title_text):
        # Section Tag Badge
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.7), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.name = "Calibri"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = INDIGO_PRIMARY

        # Title Text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.75))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(25)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY_DARK

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (LIGHT THEME HERO)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, BG_LIGHT)

    # Hero Card Container
    hero_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(11.733), Inches(5.7))
    hero_card.fill.solid()
    hero_card.fill.fore_color.rgb = CARD_BG
    hero_card.line.color.rgb = BORDER_ACCENT
    hero_card.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.3), Inches(1.3), Inches(10.7), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p_badge = tf.paragraphs[0]
    p_badge.text = "FINAL YEAR PROJECT DEFENSE • MACHINE LEARNING & NLP"
    p_badge.font.name = "Calibri"
    p_badge.font.size = Pt(12)
    p_badge.font.bold = True
    p_badge.font.color.rgb = INDIGO_PRIMARY
    p_badge.space_after = Pt(14)

    p_main = tf.add_paragraph()
    p_main.text = "NewsScope: Smart News Article Classifier"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(38)
    p_main.font.bold = True
    p_main.font.color.rgb = NAVY_DARK
    p_main.space_after = Pt(14)

    p_sub = tf.add_paragraph()
    p_sub.text = "An Interpretable, High-Throughput Classification System Benchmarking 4 AI Architectures"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_after = Pt(28)

    p_metrics = tf.add_paragraph()
    p_metrics.text = "⭐ Production Champion: Linear SVM  |  Accuracy: 96.4%  |  Inference Latency: 1.2 ms"
    p_metrics.font.name = "Calibri"
    p_metrics.font.size = Pt(14)
    p_metrics.font.bold = True
    p_metrics.font.color.rgb = EMERALD_GREEN
    p_metrics.space_after = Pt(24)

    p_meta = tf.add_paragraph()
    p_meta.text = "Presenter: Abhijeet   •   Dataset: BBC News (5 Categories, 2,225 Articles)   •   Stack: FastAPI + Next.js 14 + Scikit-Learn"
    p_meta.font.name = "Calibri"
    p_meta.font.size = Pt(12)
    p_meta.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 2: AGENDA (7 CORE SECTIONS)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, BG_LIGHT)
    add_header(s2, "Presentation Structure", "Agenda & Key Topics")

    sections = [
        ("01", "Introduction & Objectives", "Why news classification matters, industry motivation, and core engineering goals."),
        ("02", "System Architecture & NLP Pipeline", "Decoupled Next.js & FastAPI stack, and the 5-stage text transformation pipeline."),
        ("03", "Machine Learning Models", "Plain English explanation of Naive Bayes, Linear SVM, Neural MLP, & DistilBERT."),
        ("04", "Dataset & Experimental Results", "BBC 2,225 corpus analysis, 4-model leaderboard, and per-domain accuracy breakdown."),
        ("05", "Error Analysis & Explainability", "Confusion matrix diagnostics, boundary overlap, Platt scaling, and word saliency."),
        ("06", "Application Features (Live Demo)", "Real-time example walkthrough, consensus modal, batch CSV, and analytics."),
        ("07", "Conclusion & Future Scope", "Key takeaways, project limitations, future roadmap, and Viva defense backup.")
    ]

    for idx, (num, title, desc) in enumerate(sections):
        col = idx // 4
        row = idx % 4
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.6 + row * 1.35)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(1.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        ctb = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.12), Inches(5.2), Inches(0.95))
        ctf = ctb.text_frame
        ctf.word_wrap = True

        p1 = ctf.paragraphs[0]
        p1.text = f"{num}. {title}"
        p1.font.name = "Calibri"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO_PRIMARY

        p2 = ctf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SECTION 1: INTRODUCTION & OBJECTIVES
    # =========================================================================

    # SLIDE 3: PROBLEM STATEMENT & MOTIVATION
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, BG_LIGHT)
    add_header(s3, "Section 1 • Introduction & Objectives", "Why Automated News Classification Matters")

    # Left Box: Problem
    left_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = BORDER_COLOR

    ltb = s3.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.1), Inches(4.8))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "The Real-World Industry Problem"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(14)

    bullets_l = [
        "Massive Information Flow: Over 500 million news articles and blogs are posted online every day.",
        "Manual Tagging is Impossible: Newsrooms cannot afford human staff to read and categorize every story.",
        "Strict Latency Demands: Real-time news aggregators require classification in under 20 milliseconds.",
        "Inconsistent Tagging: Different human editors often label the same news article under different categories."
    ]
    for b in bullets_l:
        p = ltf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Right Box: Gap & Solution
    right_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = CARD_BG
    right_card.line.color.rgb = BORDER_COLOR

    rtb = s3.shapes.add_textbox(Inches(7.05), Inches(1.8), Inches(5.2), Inches(4.8))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "The 'Black-Box' Problem & NewsScope"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = INDIGO_PRIMARY
    p.space_after = Pt(14)

    bullets_r = [
        "Black-Box Predictions: Most automated classifiers give a category label without explaining why.",
        "Trust & Auditability: Journalists and editors need to see the exact keywords that triggered a decision.",
        "Data Leakage Risk: Many academic projects clean text across train and test sets together, producing inflated fake metrics.",
        "The NewsScope Solution: A zero-leakage, transparent system delivering 96.4% accuracy in 1.2 ms with clear word explanations."
    ]
    for b in bullets_r:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # SLIDE 4: CORE PROJECT OBJECTIVES
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, BG_LIGHT)
    add_header(s4, "Section 1 • Introduction & Objectives", "Core Engineering Objectives")

    pillars = [
        ("1. Zero Data Leakage Pipeline", "Strict scientific separation between training and testing data. The vocabulary is built exclusively from training articles; test sets are treated strictly as unseen incoming articles."),
        ("2. Multi-Model Architecture Benchmark", "Systematically compare 4 distinct machine learning paradigms on the identical test split: Naive Bayes (probability), Linear SVM (geometry), MLP (neural network), and DistilBERT (transformer)."),
        ("3. Model Interpretability & Explainability", "Demystify black-box predictions. Extract top contributing words using hyperplane feature coefficients and display calibrated confidence percentages."),
        ("4. Production-Ready Full-Stack Web Platform", "Build a high-performance web application with sub-second single inference, 4-model parallel comparison, and bulk CSV batch processing.")
    ]

    for idx, (title, desc) in enumerate(pillars):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.6 + (idx // 2) * 2.65)

        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.4))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s4.shapes.add_textbox(left + Inches(0.3), top + Inches(0.22), Inches(5.0), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO_PRIMARY
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SECTION 2: SYSTEM ARCHITECTURE & NLP PIPELINE
    # =========================================================================

    # SLIDE 5: SYSTEM ARCHITECTURE
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, BG_LIGHT)
    add_header(s5, "Section 2 • System Architecture & NLP Pipeline", "Decoupled Full-Stack Architecture")

    layers = [
        ("1. Client Application (Next.js 14 App Router)", "• Built with Next.js 14, React 18, and Tailwind CSS for modern responsive design.\n• Uses Zustand centralized store with atomic selectors so typing does not freeze the UI.\n• Visualizes data using Recharts (per-domain accuracy bars and confusion matrix heatmaps)."),
        ("2. API Gateway (FastAPI 0.115 Async REST)", "• High-speed Python REST API handling requests in under 1 millisecond.\n• Pydantic v2 schemas for strict input sanitization, runtime validation, and CORS security.\n• Endpoints: POST /api/classify (single article), GET /api/dataset (corpus metrics)."),
        ("3. Machine Learning Engine (Scikit-Learn & PyTorch)", "• Serialized pipelines loaded instantly into memory via Joblib.\n• Linear SVM (Production Champion) with Platt scaling for honest calibrated probabilities.\n• Supports live parallel inference for Naive Bayes, Neural MLP, and DistilBERT.")
    ]

    for idx, (title, desc) in enumerate(layers):
        top = Inches(1.6 + idx * 1.75)
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.55))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s5.shapes.add_textbox(Inches(1.1), top + Inches(0.16), Inches(11.1), Inches(1.25))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO_PRIMARY
        p1.space_after = Pt(4)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(11.5)
            p.font.color.rgb = TEXT_BODY

    # SLIDE 6: 5-STAGE NLP PIPELINE
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, BG_LIGHT)
    add_header(s6, "Section 2 • System Architecture & NLP Pipeline", "5-Stage Zero-Leakage Text Pipeline")

    stages = [
        ("Step 1: Lowercase & Clean", "Converts text to lowercase and strips HTML tags, punctuation, and URLs.", "Input: 'Apple's NEW iPhone @ $999!' -> 'apples new iphone 999'"),
        ("Step 2: Split Words (Tokenize)", "Breaks the continuous sentence into individual word units.", "Output: ['apples', 'new', 'iphone', '999']"),
        ("Step 3: Remove Stopwords", "Filters out 179 useless filler words (like 'the', 'is', 'at', 'and').", "Filtered: ['apples', 'iphone', '999']"),
        ("Step 4: Lemmatization", "Reduces words to their dictionary root form (e.g. 'apples' -> 'apple').", "Lemmas: ['apple', 'iphone', '999']"),
        ("Step 5: Sublinear TF-IDF", "Converts words to numerical weights (10,000 features, unigram + bigram).", "Vector: [0.42, 0.61, 0.28, ...] (numbers ready for the ML model)")
    ]

    for idx, (title, desc, example) in enumerate(stages):
        top = Inches(1.6 + idx * 1.05)
        c = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(0.95))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s6.shapes.add_textbox(Inches(1.0), top + Inches(0.1), Inches(11.3), Inches(0.78))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{title}:  {desc}"
        p1.font.name = "Calibri"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK

        p2 = tf.add_paragraph()
        p2.text = example
        p2.font.name = "Consolas"
        p2.font.size = Pt(11)
        p2.font.color.rgb = INDIGO_PRIMARY

    # =========================================================================
    # SECTION 3: MACHINE LEARNING MODELS
    # =========================================================================

    # SLIDE 7: MACHINE LEARNING MODELS (PLAIN ENGLISH)
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, BG_LIGHT)
    add_header(s7, "Section 3 • Machine Learning Models", "The 4 Machine Learning Models Explained")

    models_info = [
        ("1. Multinomial Naive Bayes", "Probability Baseline: P(Category | Words) via Bayes' Theorem", "How it works: Multiplies word probabilities assuming words are independent. It is ultra-fast (0.5 ms) and provides a clean statistical baseline."),
        ("2. Linear SVM (Our Production Champion)", "Maximum-Margin Line: Finds the widest gap between categories", "How it works: High-dimensional text (10,000 words) is linearly separable by Cover's Theorem. Draws the optimal decision boundary. 96.4% accuracy in 1.2 ms."),
        ("3. Neural MLP (Multi-Layer Perceptron)", "Neural Network: 2 layers (128 hidden neurons, ReLU, Adam)", "How it works: Learns non-linear combinations of words. Highly capable, achieving 95.1% accuracy in 3.2 ms."),
        ("4. DistilBERT Transformer", "Self-Attention Mechanism: 6 transformer layers (66M parameters)", "How it works: Reads sentences bidirectionally to understand deep grammar context (e.g. 'Apple' company vs fruit). 97.8% accuracy in 12.4 ms.")
    ]

    for idx, (title, formula, note) in enumerate(models_info):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.6 + (idx // 2) * 2.65)

        c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.4))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s7.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), Inches(5.1), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_DARK
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = formula
        p2.font.name = "Consolas"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = INDIGO_PRIMARY
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = note
        p3.font.name = "Calibri"
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SECTION 4: DATASET & EXPERIMENTAL RESULTS
    # =========================================================================

    # SLIDE 8: BBC DATASET & DISTRIBUTION
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, BG_LIGHT)
    add_header(s8, "Section 4 • Dataset & Experimental Results", "BBC News Dataset & Class Distribution")

    table_shape = s8.shapes.add_table(6, 4, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.1))
    table = table_shape.table

    headers = ["Category", "Total", "Percent", "Test Split (20%)"]
    data = [
        ["Sport", "511", "23.0%", "102"],
        ["Business", "510", "22.9%", "102"],
        ["Politics", "417", "18.7%", "84"],
        ["Tech", "401", "18.0%", "80"],
        ["Entertainment", "386", "17.3%", "77"],
    ]

    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = INDIGO_PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.name = "Calibri"
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    for i, row_data in enumerate(data):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else CARD_BG_ALT
            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(11.5)
                p.font.color.rgb = NAVY_DARK

    # Right Card: Dataset Notes
    rc = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.6), Inches(5.5), Inches(5.1))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = BORDER_COLOR

    rtb = s8.shapes.add_textbox(Inches(7.25), Inches(1.85), Inches(5.0), Inches(4.6))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Dataset Characteristics"
    p.font.name = "Calibri"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(12)

    bullets = [
        "Benchmark Corpus: Compiled by Greene & Cunningham (2006) from BBC news archive.",
        "Total Sample Size: 2,225 genuine news articles across 5 distinct news domains.",
        "Stratified 80/20 Split: 1,780 articles for training / 445 articles held out for testing.",
        "Balanced Classes: Each category holds between 386 and 511 articles; no severe class imbalance.",
        "Average Article Length: ~2,200 characters (~380 words) per article.",
        "Zero Leakage Guarantee: Vectorizer fitted strictly on train split; test transformed using fitted vocabulary."
    ]
    for b in bullets:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(8)

    # SLIDE 9: 4-MODEL LEADERBOARD & RESULTS
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, BG_LIGHT)
    add_header(s9, "Section 4 • Dataset & Experimental Results", "4-Model Performance Benchmark")

    table_shape = s9.shapes.add_table(5, 5, Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.3))
    table = table_shape.table

    m_headers = ["Model Name", "Paradigm / Technique", "Test Accuracy", "Macro F1", "Speed (Latency)"]
    m_data = [
        ["DistilBERT", "Transformer Attention (66M weights)", "97.8%", "0.976", "12.4 ms"],
        ["Linear SVM (Winner)", "Maximum-Margin Line", "96.4%", "0.963", "1.2 ms"],
        ["Neural MLP", "Neural Network (128 neurons)", "95.1%", "0.948", "3.2 ms"],
        ["Multinomial Naive Bayes", "Generative Probabilistic", "92.1%", "0.920", "0.5 ms"]
    ]

    for j, h in enumerate(m_headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = INDIGO_PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.name = "Calibri"
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    for i, row_data in enumerate(m_data):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            if i == 1:
                cell.fill.fore_color.rgb = EMERALD_LIGHT
            else:
                cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else CARD_BG_ALT
            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(12)
                p.font.bold = (i == 1)
                p.font.color.rgb = EMERALD_GREEN if (i == 1 and j in [0, 2]) else NAVY_DARK

    # Callout Banner below table
    banner = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.6))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = BORDER_COLOR

    btb = s9.shapes.add_textbox(Inches(1.1), Inches(5.35), Inches(11.1), Inches(1.3))
    btf = btb.text_frame
    btf.word_wrap = True

    p = btf.paragraphs[0]
    p.text = "Key Empirical Finding: Why Linear SVM is the Production Winner"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = INDIGO_PRIMARY

    p2 = btf.add_paragraph()
    p2.text = "• DistilBERT achieved the highest raw accuracy (97.8%), but Linear SVM achieved 96.4% while running 10x faster (1.2 ms vs 12.4 ms) and requiring 20x less memory (< 15 MB vs 260 MB). In production newsrooms, Linear SVM delivers the ideal balance of accuracy, cost, and latency."
    p2.font.name = "Calibri"
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = TEXT_BODY

    # SLIDE 10: PER-DOMAIN ACCURACY BREAKDOWN
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, BG_LIGHT)
    add_header(s10, "Section 4 • Dataset & Experimental Results", "Per-Domain Accuracy Breakdown (Linear SVM)")

    domains = [
        ("Sport", "99.0%", "101 / 102 correct", "Distinct athletic vocabulary (goal, cup, match, injury, coach)"),
        ("Tech", "96.3%", "77 / 80 correct", "Software, mobile, hardware, broadband, computer"),
        ("Entertainment", "96.1%", "74 / 77 correct", "Film, festival, awards, music, box office, actor"),
        ("Business", "96.1%", "98 / 102 correct", "Market, shares, profit, inflation, bank, economy"),
        ("Politics", "94.0%", "79 / 84 correct", "Government, ministers, parliament, election, tax policy")
    ]

    for idx, (dom, acc, ratio, notes) in enumerate(domains):
        left = Inches(0.8 + idx * 2.38)
        c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.6), Inches(2.25), Inches(3.5))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s10.shapes.add_textbox(left + Inches(0.15), Inches(1.75), Inches(1.95), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = dom
        p.font.name = "Calibri"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = NAVY_DARK

        p_acc = tf.add_paragraph()
        p_acc.text = acc
        p_acc.font.name = "Calibri"
        p_acc.font.size = Pt(30)
        p_acc.font.bold = True
        p_acc.font.color.rgb = EMERALD_GREEN if dom in ["Sport", "Tech"] else INDIGO_PRIMARY
        p_acc.space_after = Pt(4)

        p_r = tf.add_paragraph()
        p_r.text = ratio
        p_r.font.name = "Calibri"
        p_r.font.size = Pt(11)
        p_r.font.color.rgb = TEXT_MUTED
        p_r.space_after = Pt(8)

        p_n = tf.add_paragraph()
        p_n.text = notes
        p_n.font.name = "Calibri"
        p_n.font.size = Pt(11)
        p_n.font.color.rgb = TEXT_BODY

    # Bottom Summary
    bs = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.5))
    bs.fill.solid()
    bs.fill.fore_color.rgb = CARD_BG
    bs.line.color.rgb = BORDER_COLOR

    btb = s10.shapes.add_textbox(Inches(1.1), Inches(5.42), Inches(11.1), Inches(1.2))
    btf = btb.text_frame
    btf.word_wrap = True
    p = btf.paragraphs[0]
    p.text = "Overall Weighted Test Accuracy: 429 / 445 = 96.4%"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK

    p2 = btf.add_paragraph()
    p2.text = "• Sport is the easiest to classify (99.0%) due to unique athletic terms. Politics has the lowest score (94.0%) because politicians frequently debate macroeconomic topics (tax, budgets, inflation), which overlap with Business."
    p2.font.name = "Calibri"
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SECTION 5: ERROR ANALYSIS & EXPLAINABILITY
    # =========================================================================

    # SLIDE 11: ERROR ANALYSIS & CONFUSION MATRIX
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, BG_LIGHT)
    add_header(s11, "Section 5 • Error Analysis & Explainability", "Error Analysis & Confusion Matrix Dynamics")

    cm_shape = s11.shapes.add_table(6, 6, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.1))
    cm_table = cm_shape.table

    cm_headers = ["Actual \\ Pred", "Business", "Entertain", "Politics", "Sport", "Tech"]
    cm_data = [
        ["Business", "98", "1", "2", "0", "1"],
        ["Entertainment", "1", "74", "1", "0", "1"],
        ["Politics", "2", "1", "79", "1", "1"],
        ["Sport", "0", "0", "1", "101", "0"],
        ["Tech", "1", "0", "1", "1", "77"]
    ]

    for j, h in enumerate(cm_headers):
        cell = cm_table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = INDIGO_PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.name = "Calibri"
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(cm_data):
        for j, val in enumerate(row):
            cell = cm_table.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            if j == 0:
                cell.fill.fore_color.rgb = CARD_BG_ALT
            elif (i + 1) == j:
                cell.fill.fore_color.rgb = EMERALD_LIGHT
            elif int(val) > 0:
                cell.fill.fore_color.rgb = ROSE_LIGHT
            else:
                cell.fill.fore_color.rgb = CARD_BG

            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(11)
                p.font.bold = (j > 0 and (i + 1) == j)
                p.font.color.rgb = NAVY_DARK

    # Right: Diagnostic Notes
    rc = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.6), Inches(5.4), Inches(5.1))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = BORDER_COLOR

    rtb = s11.shapes.add_textbox(Inches(7.35), Inches(1.85), Inches(4.9), Inches(4.6))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Key Qualitative Diagnostics"
    p.font.name = "Calibri"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY_DARK
    p.space_after = Pt(12)

    diag_bullets = [
        "Only 16 Total Errors: Out of 445 unseen test articles, only 16 were misclassified across the entire corpus.",
        "Primary Confusion Vector: Politics <-> Business. 2 Business articles were misclassified as Politics; 2 Politics misclassified as Business.",
        "Root Cause: Shared vocabulary in fiscal policy (treasury, tax legislation, chancellor, budget deficit).",
        "Remediation Applied: Unigram + Bigram feature extraction ('corporate tax' vs 'tax policy') resolved 80% of borderline ambiguities.",
        "Sport Isolation: 99.0% recall. Only 1 article misclassified ('Olympic committee governance election' -> Politics)."
    ]
    for b in diag_bullets:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(8)

    # SLIDE 12: MODEL EXPLAINABILITY
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, BG_LIGHT)
    add_header(s12, "Section 5 • Error Analysis & Explainability", "Opening the Black Box: Model Explainability")

    methods = [
        ("1. Feature Coefficient Extraction (Linear SVM)", "Linear SVM decisions follow f(x) = w^T * x + b. By multiplying feature values by their hyperplane weights (w_i * x_i), NewsScope reveals the exact words driving the outcome.", "Example: 'processor' (+0.35) and 'macbook' (+0.28) strongly pull the prediction toward Technology."),
        ("2. Calibrated Confidence Percentages (Platt Scaling)", "Standard SVMs output raw distance values. Platt Scaling trains a logistic regression sigmoid on top of margins, converting distances into statistically honest probabilities.", "Example: Margin +2.45 -> 96.4% calibrated confidence percentage."),
        ("3. Color-Coded Word Saliency Highlights", "In our Next.js frontend, influential words light up with vibrant badges, giving editorial staff instant visual confirmation of the classifier's reasoning.", "User Experience: Dynamic token badges showing top keyword weights.")
    ]

    for idx, (title, desc, ex) in enumerate(methods):
        top = Inches(1.6 + idx * 1.75)
        c = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.55))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s12.shapes.add_textbox(Inches(1.1), top + Inches(0.16), Inches(11.1), Inches(1.25))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO_PRIMARY
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = NAVY_DARK
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = ex
        p3.font.name = "Consolas"
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SECTION 6: APPLICATION FEATURES (LIVE DEMO)
    # =========================================================================

    # SLIDE 13: APPLICATION FEATURES OVERVIEW
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, BG_LIGHT)
    add_header(s13, "Section 6 • Application Features (Live Demo)", "NewsScope Web Platform Capabilities")

    features = [
        ("1. Real-Time Classifier", "• Type or paste any news text and get instant results in under 1 second.\n• Shows predicted category, confidence percentage, and word count.\n• Optimistic UI: typing is smooth with atomic Zustand selectors."),
        ("2. 4-Model Consensus Modal", "• Click 'Compare All Models' to test all 4 models simultaneously.\n• Shows execution speed, individual confidence, and agreement side-by-side.\n• Validates how classical and deep learning models behave live."),
        ("3. High-Throughput Batch CSV Processing", "• Drag and drop a CSV file with hundreds of news articles.\n• Live progress bar shows processing speed and completion count.\n• Instant CSV export with predicted category and confidence scores."),
        ("4. Interactive Analytics Dashboard", "• Live bar chart showing Per-Domain Accuracy Breakdown.\n• Interactive Confusion Matrix heatmap showing where errors occur.\n• Full system metrics: Accuracy, Precision, Recall, and Macro F1.")
    ]

    for idx, (title, desc) in enumerate(features):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.6 + (idx // 2) * 2.65)

        c = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.4))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s13.shapes.add_textbox(left + Inches(0.3), top + Inches(0.2), Inches(5.0), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO_PRIMARY
        p1.space_after = Pt(6)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(11.5)
            p.font.color.rgb = TEXT_BODY

    # SLIDE 14: LIVE DEMO REAL-TIME WALKTHROUGH EXAMPLE
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, BG_LIGHT)
    add_header(s14, "Section 6 • Application Features (Live Demo)", "Real-Time Demonstration: Step-by-Step Example")

    # Left: Input & Pipeline Steps
    left_card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.2))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = BORDER_COLOR

    ltb = s14.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.4), Inches(4.8))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "1. Input Article & Text Transformation"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = INDIGO_PRIMARY
    p.space_after = Pt(8)

    p_in_lbl = ltf.add_paragraph()
    p_in_lbl.text = "Live Article Entered in Classifier:"
    p_in_lbl.font.name = "Calibri"
    p_in_lbl.font.size = Pt(12)
    p_in_lbl.font.bold = True
    p_in_lbl.font.color.rgb = NAVY_DARK

    p_in = ltf.add_paragraph()
    p_in.text = "\"Apple unveils new M3 MacBook laptop with ultra-fast processor, 22-hour battery life, and high performance graphics for developers.\""
    p_in.font.name = "Consolas"
    p_in.font.size = Pt(11)
    p_in.font.color.rgb = NAVY_DARK
    p_in.space_after = Pt(10)

    pipeline_steps = [
        "1. Cleansed: 'apple unveils new m3 macbook laptop ultrafast processor 22hour battery life high performance graphics developers'",
        "2. Stopwords Dropped: filtered 'with', 'and', 'for'",
        "3. Lemmatized: 'features' -> 'feature', 'unveils' -> 'unveil'",
        "4. Converted to 10,000-dimensional TF-IDF sparse vector"
    ]
    for step in pipeline_steps:
        p = ltf.add_paragraph()
        p.text = "• " + step
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(4)

    # Right: Prediction, Keywords, Consensus
    right_card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = CARD_BG
    right_card.line.color.rgb = BORDER_COLOR

    rtb = s14.shapes.add_textbox(Inches(7.1), Inches(1.75), Inches(5.2), Inches(4.8))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "2. Prediction & Model Consensus"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(8)

    p_res = rtf.add_paragraph()
    p_res.text = "Predicted Category: TECHNOLOGY (98.4%)"
    p_res.font.name = "Calibri"
    p_res.font.size = Pt(15)
    p_res.font.bold = True
    p_res.font.color.rgb = NAVY_DARK
    p_res.space_after = Pt(8)

    p_kw = rtf.add_paragraph()
    p_kw.text = "Top Explanatory Keywords:"
    p_kw.font.name = "Calibri"
    p_kw.font.size = Pt(12)
    p_kw.font.bold = True
    p_kw.font.color.rgb = INDIGO_PRIMARY

    keywords = ["processor (+0.35)", "apple (+0.28)", "laptop (+0.24)", "developer (+0.18)"]
    p_chips = rtf.add_paragraph()
    p_chips.text = "  |  ".join(keywords)
    p_chips.font.name = "Consolas"
    p_chips.font.size = Pt(11)
    p_chips.font.color.rgb = NAVY_DARK
    p_chips.space_after = Pt(12)

    p_con_lbl = rtf.add_paragraph()
    p_con_lbl.text = "4-Model Consensus Modal:"
    p_con_lbl.font.name = "Calibri"
    p_con_lbl.font.size = Pt(12)
    p_con_lbl.font.bold = True
    p_con_lbl.font.color.rgb = NAVY_DARK

    models_consensus = [
        "Linear SVM: Technology (98.4% | 1.2 ms)",
        "DistilBERT: Technology (99.1% | 12.4 ms)",
        "Neural MLP: Technology (97.0% | 3.2 ms)",
        "Naive Bayes: Technology (93.5% | 0.5 ms)"
    ]
    for mc in models_consensus:
        p = rtf.add_paragraph()
        p.text = "✔ " + mc
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(3)

    p_verdict = rtf.add_paragraph()
    p_verdict.text = "Result: 100% agreement across all 4 architectures!"
    p_verdict.font.name = "Calibri"
    p_verdict.font.size = Pt(12)
    p_verdict.font.bold = True
    p_verdict.font.color.rgb = EMERALD_GREEN

    # =========================================================================
    # SECTION 7: CONCLUSION & FUTURE SCOPE
    # =========================================================================

    # SLIDE 15: LIMITATIONS & FUTURE SCOPE
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, BG_LIGHT)
    add_header(s15, "Section 7 • Conclusion & Future Scope", "Current Limitations & Future Roadmap")

    # Left: Limitations
    lc = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    lc.fill.solid()
    lc.fill.fore_color.rgb = CARD_BG
    lc.line.color.rgb = BORDER_COLOR

    ltb = s15.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.1), Inches(4.7))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "Current Limitations"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ROSE_RED
    p.space_after = Pt(12)

    lims = [
        "Historical Dataset: The BBC 2005 corpus lacks modern vocabulary (smartphones, LLMs, crypto, streaming).",
        "Single-Label Constraint: Real-world articles can span multiple domains (e.g. tech antitrust policy) but receive only one category.",
        "Monolingual: Evaluated strictly on English news articles.",
        "Static Training: No automated concept drift detection or online model retraining."
    ]
    for b in lims:
        p = ltf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # Right: Future Scope
    rc = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = BORDER_COLOR

    rtb = s15.shapes.add_textbox(Inches(7.05), Inches(1.8), Inches(5.2), Inches(4.7))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Future Roadmap"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(12)

    roadmap = [
        "Multi-Label Classification: Binary relevance / sigmoid thresholding for multi-topic stories.",
        "Multilingual Embeddings: Fine-tuning XLM-RoBERTa for cross-lingual news classification across 50+ languages.",
        "Active Learning: Routing low-confidence predictions (< 50%) to human editors for iterative active learning.",
        "Model Quantization: 8-bit ONNX runtime deployment to achieve sub-millisecond transformer inference."
    ]
    for b in roadmap:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(10)

    # SLIDE 16: CONCLUSION (LIGHT THEME)
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, BG_LIGHT)

    conc_card = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(11.733), Inches(5.7))
    conc_card.fill.solid()
    conc_card.fill.fore_color.rgb = CARD_BG
    conc_card.line.color.rgb = BORDER_ACCENT
    conc_card.line.width = Pt(1.5)

    tb = s16.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(5.1))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SECTION 7 • CONCLUSION & TAKEAWAYS"
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = INDIGO_PRIMARY
    p.space_after = Pt(10)

    p_t = tf.add_paragraph()
    p_t.text = "Project Summary & Key Conclusions"
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(32)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY_DARK
    p_t.space_after = Pt(18)

    concl_points = [
        "High Performance: Linear SVM achieved 96.4% accuracy at 1.2 ms latency, showing simple math beats heavy neural nets in real-world efficiency.",
        "Methodological Rigor: Zero data leakage enforced through strict pipeline encapsulation and sublinear TF-IDF feature extraction.",
        "Transparency & Trust: Solved the black-box dilemma using hyperplane feature coefficients and Platt-scaled calibrated probabilities.",
        "Production Delivery: Completed fully functional full-stack system with Next.js 14, FastAPI, batch CSV processing, and live analytics."
    ]
    for cp in concl_points:
        p = tf.add_paragraph()
        p.text = "✔  " + cp
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = NAVY_DARK
        p.space_after = Pt(10)

    # =========================================================================
    # BACKUP SLIDE: VIVA VOCE DEFENSE CHEAT SHEET
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17, BG_LIGHT)
    add_header(s17, "Backup Reference", "Viva Voce Defense Cheat Sheet (Simple Answers)")

    qa_list = [
        ("Q1: Why TF-IDF over simple CountVectorizer?", "Answer: CountVectorizer lets common filler words dominate. TF-IDF uses Inverse Document Frequency to downweight ubiquitous words and highlight discriminative topic terms like 'striker' or 'inflation'."),
        ("Q2: Why does Linear SVM perform so well on text?", "Answer: Cover's Theorem states that high-dimensional sparse representations (10,000 features) are linearly separable with high probability. Linear SVM finds the maximum-margin hyperplane without overfitting."),
        ("Q3: How did you strictly guarantee Zero Data Leakage?", "Answer: TfidfVectorizer.fit() was called exclusively on the 1,780 training articles. The 445 test articles were only transformed using the pre-fit vocabulary. Test words are completely ignored during fitting."),
        ("Q4: Why choose DistilBERT over standard BERT?", "Answer: DistilBERT retains 97% of BERT's language comprehension capabilities via knowledge distillation, while using 40% fewer parameters and running 60% faster.")
    ]

    for idx, (q, a) in enumerate(qa_list):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.6 + (idx // 2) * 2.65)

        c = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.4))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s17.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), Inches(5.1), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = q
        p1.font.name = "Calibri"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO_PRIMARY
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = a
        p2.font.name = "Calibri"
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = TEXT_BODY

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        prs.save(output_path)
        print(f"Presentation saved successfully to {output_path}")
    except PermissionError:
        alt_path = output_path.replace(".pptx", "_v2.pptx")
        prs.save(alt_path)
        print(f"Notice: {output_path} is locked. Saved to {alt_path}")

if __name__ == "__main__":
    create_deck()
