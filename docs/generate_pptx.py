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

    # Theme Palette
    BG_COLOR = RGBColor(248, 249, 250)      # #f8f9fa
    NAVY = RGBColor(15, 23, 42)             # #0f172a
    INDIGO = RGBColor(79, 70, 229)          # #4f46e5
    EMERALD = RGBColor(5, 150, 105)         # #059669
    TEXT_MUTED = RGBColor(100, 116, 139)    # #64748b
    CARD_BG = RGBColor(255, 255, 255)       # #ffffff
    BORDER_COLOR = RGBColor(226, 232, 240)  # #e2e8f0

    def set_slide_background(slide, color=BG_COLOR):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, category_tag, title_text):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_tag.upper()
        p_tag.font.name = "Calibri"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = INDIGO

        # Title Text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Hero)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, NAVY)

    # Title box
    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p_badge = tf.paragraphs[0]
    p_badge.text = "FINAL YEAR PROJECT DEFENSE • MACHINE LEARNING & NLP"
    p_badge.font.name = "Calibri"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(129, 140, 248) # Indigo 400
    p_badge.space_after = Pt(14)

    p_main = tf.add_paragraph()
    p_main.text = "NewsScope: Multi-Architecture\nNews Article Category Classifier"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(40)
    p_main.font.bold = True
    p_main.font.color.rgb = RGBColor(255, 255, 255)
    p_main.space_after = Pt(18)

    p_sub = tf.add_paragraph()
    p_sub.text = "An Interpretable, High-Throughput Classification System Benchmarking 4 Statistical & Deep Learning Architectures"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(36)

    p_meta = tf.add_paragraph()
    p_meta.text = "Presenter: Abhijeet  |  Domain: BBC 5-Class News Corpus  |  Stack: FastAPI + Next.js 14 + Scikit-Learn"
    p_meta.font.name = "Calibri"
    p_meta.font.size = Pt(13)
    p_meta.font.color.rgb = RGBColor(148, 163, 184)

    # ==========================================
    # SLIDE 2: AGENDA
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Presentation Structure", "Agenda & Key Topics")

    agenda_items = [
        ("01", "Problem Statement & Motivation", "The news categorization challenge and the 'black-box' transparency gap."),
        ("02", "Project Objectives", "Zero data leakage, 4-model benchmark, and real-time interpretability."),
        ("03", "System Architecture", "Decoupled full-stack design with FastAPI backend and Next.js 14 frontend."),
        ("04", "5-Stage NLP Pipeline", "Rigorous text preprocessing from raw strings to sublinear TF-IDF vectors."),
        ("05", "Mathematical Foundations", "Formulations of Naive Bayes, Linear SVM, Neural MLP, and Attention."),
        ("06", "Experimental Benchmark", "Evaluation results on 445 held-out articles across all 4 architectures."),
        ("07", "Error Analysis & Saliency", "Confusion matrix dynamics and feature-weight explainability."),
        ("08", "Conclusion & Future Scope", "Key engineering takeaways, real-world constraints, and roadmap.")
    ]

    for idx, (num, title, desc) in enumerate(agenda_items):
        col = idx // 4
        row = idx % 4
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.8 + row * 1.3)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(1.15))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        ctb = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.12), Inches(5.2), Inches(0.9))
        ctf = ctb.text_frame
        ctf.word_wrap = True

        p1 = ctf.paragraphs[0]
        p1.text = f"{num}. {title}"
        p1.font.name = "Calibri"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = ctf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 3: PROBLEM STATEMENT & MOTIVATION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Background & Need", "Problem Statement & Industry Motivation")

    # Left Box: Problem
    left_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = BORDER_COLOR

    ltb = s3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.7))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "The Information Overload Challenge"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(14)

    bullets_l = [
        "500M+ digital articles are published worldwide daily across news wires, blogs, and portals.",
        "Manual classification is unscalable, slow, inconsistent, and expensive for news desks.",
        "High dimensionality & vocabulary sparsity create major computational hurdles for raw text.",
        "Latency constraints (< 20 ms) demand fast, lightweight architectures for real-time editorial ingestion."
    ]
    for b in bullets_l:
        p = ltf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    # Right Box: Gap & Solution
    right_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = CARD_BG
    right_card.line.color.rgb = BORDER_COLOR

    rtb = s3.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "The 'Black-Box' Transparency Gap"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = INDIGO
    p.space_after = Pt(14)

    bullets_r = [
        "Standard classifiers output categorical probabilities without justifying why a prediction was made.",
        "Editors and journalists require explainability (which keywords or phrases triggered the decision?).",
        "Many academic projects suffer from data leakage (fitting vectorizers across both train and test sets).",
        "NewsScope delivers 100% pipeline transparency, zero leakage, and real-time word-level saliency."
    ]
    for b in bullets_r:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 4: OBJECTIVES & SCOPE
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Engineering Scope", "Core Project Objectives")

    pillars = [
        ("1. Zero Data Leakage Pipeline", "Strict statistical separation between training vocabulary and unseen test data. Vectorizer is fitted exclusively on train folds."),
        ("2. Multi-Model Architecture Benchmark", "Systematic evaluation of 4 distinct paradigms (Naive Bayes, Linear SVM, Neural MLP, DistilBERT) on the identical held-out test split."),
        ("3. Model Interpretability & Explainability", "Real-time extraction of top salient keywords using hyperplane feature coefficients and token-level attention heatmaps."),
        ("4. Production-Ready Full-Stack System", "FastAPI backend for low-latency inference (< 2ms) and responsive Next.js 14 web interface featuring batch CSV processing and analytics.")
    ]

    for idx, (title, desc) in enumerate(pillars):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.8 + (idx // 2) * 2.6)

        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.3))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s4.shapes.add_textbox(left + Inches(0.3), top + Inches(0.25), Inches(5.0), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(10)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(13)
        p2.font.color.rgb = RGBColor(51, 65, 85)

    # ==========================================
    # SLIDE 5: SYSTEM ARCHITECTURE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "System Design", "Decoupled Full-Stack Architecture")

    layers = [
        ("Client Tier (Next.js 14)", "• Next.js App Router (React Server + Client Components)\n• Tailwind CSS for responsive styling\n• Framer Motion & Recharts for interactive dashboards\n• Zustand state management with atomic selectors"),
        ("API Gateway (FastAPI 0.115)", "• Asynchronous REST endpoints (POST /api/classify, GET /api/dataset)\n• Pydantic validation & strict typing\n• CORS middleware for secure cross-origin requests\n• Sub-millisecond routing overhead"),
        ("Machine Learning Engine", "• Scikit-Learn pipeline serialization via Joblib\n• LinearSVC with Platt scaling for calibrated probabilities\n• MultinomialNB (Laplace smoothing α=0.1)\n• MLPClassifier (128 units, Adam, ReLU)\n• DistilBERT-base-uncased sequence classification")
    ]

    for idx, (title, desc) in enumerate(layers):
        top = Inches(1.8 + idx * 1.75)
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.55))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s5.shapes.add_textbox(Inches(1.1), top + Inches(0.18), Inches(11.1), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(4)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(12)
            p.font.color.rgb = RGBColor(51, 65, 85)

    # ==========================================
    # SLIDE 6: 5-STAGE NLP PIPELINE
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Data Preprocessing", "The 5-Stage Zero-Leakage NLP Pipeline")

    stages = [
        ("Stage 1: Normalization", "Case folding (lowercasing), regex stripping of URLs, HTML tags, and punctuation.", "Input: 'Apple's NEW iPhone @ $999!' -> 'apples new iphone 999'"),
        ("Stage 2: Tokenization", "Splitting continuous text into discrete linguistic word units.", "Output: ['apples', 'new', 'iphone', '999']"),
        ("Stage 3: Stopword Pruning", "Removal of 179 high-frequency uninformative words using NLTK corpus.", "Filtered: ['apples', 'iphone', '999']"),
        ("Stage 4: Lemmatization", "WordNet morphological analysis reducing inflected words to dictionary lemmas.", "Lemmas: ['apple', 'iphone', '999']"),
        ("Stage 5: Sublinear TF-IDF", "10,000 features, unigram + bigram (1,2), min_df=2, sublinear scaling (1+log(TF)).", "Result: [0.42, 0.61, 0.28, ...] sparse vector")
    ]

    for idx, (title, desc, example) in enumerate(stages):
        top = Inches(1.7 + idx * 1.05)
        c = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(0.95))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s6.shapes.add_textbox(Inches(1.0), top + Inches(0.1), Inches(11.3), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{title}:  {desc}"
        p1.font.name = "Calibri"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = f"Example: {example}"
        p2.font.name = "Consolas"
        p2.font.size = Pt(11)
        p2.font.color.rgb = INDIGO

    # ==========================================
    # SLIDE 7: MATHEMATICAL FORMULATIONS
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Mathematical Modeling", "Theoretical Foundations of the Classifiers")

    math_models = [
        ("Sublinear TF-IDF Weighting", "TF-IDF(t, d, D) = (1 + ln TF(t, d)) * (ln((1 + |D|) / (1 + df(t))) + 1)", "Dampens extreme term frequencies while prioritizing discriminative rare domain keywords."),
        ("Multinomial Naive Bayes", "P(c_k | x) ∝ P(c_k) * ∏ P(x_i | c_k)^{f_i}   (Laplace smoothing α = 0.1)", "Assumes conditional feature independence given class label. Ultra-fast baseline (0.5 ms)."),
        ("Linear SVM (Maximum-Margin)", "min 1/2 ||w||^2 + C ∑ ξ_i   s.t.   y_i(w^T x_i + b) >= 1 - ξ_i", "Finds optimal separating hyperplane in 10,000-D sparse space. Calibrated via Platt Scaling."),
        ("DistilBERT Self-Attention", "Attention(Q, K, V) = softmax((Q * K^T) / sqrt(d_k)) * V", "Captures bidirectional token dependencies across 6 transformer layers (66M parameters).")
    ]

    for idx, (title, formula, note) in enumerate(math_models):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.8 + (idx // 2) * 2.6)

        c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.35))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s7.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.1), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = formula
        p2.font.name = "Consolas"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = INDIGO
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = note
        p3.font.name = "Calibri"
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 8: DATASET & DISTRIBUTION
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Corpus Analysis", "BBC News Dataset & Class Distribution")

    # Table on Left
    rows = 6
    cols = 3
    left = Inches(0.8)
    top = Inches(1.8)
    width = Inches(5.6)
    height = Inches(4.8)

    table_shape = s8.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    headers = ["Domain / Category", "Articles", "Percentage"]
    data = [
        ["Sport", "511", "23.0%"],
        ["Business", "510", "22.9%"],
        ["Politics", "417", "18.7%"],
        ["Tech", "401", "18.0%"],
        ["Entertainment", "386", "17.3%"],
    ]

    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = INDIGO
        for p in cell.text_frame.paragraphs:
            p.font.name = "Calibri"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    for i, row_data in enumerate(data):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(12)
                p.font.color.rgb = NAVY

    # Right Card: Details
    rc = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = BORDER_COLOR

    rtb = s8.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.1), Inches(4.2))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Dataset Characteristics"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    bullets = [
        "Origin: Benchmark corpus compiled by Greene & Cunningham (2006).",
        "Total Sample Size: 2,225 genuine news articles from 2004–2005.",
        "Stratified Split: 80% Training (1,780 articles) / 20% Held-Out Testing (445 articles).",
        "Class Balance: Balanced distribution; no severe class imbalance remediation required.",
        "Average Article Length: ~2,200 characters per article.",
        "Zero Leakage Guarantee: Vectorizer fitted strictly on train split; test transformed using fitted vocabulary."
    ]
    for b in bullets:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 9: EXPERIMENTAL RESULTS (LEADERBOARD)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Performance Benchmark", "4-Model Architecture Comparison")

    table_shape = s9.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.2))
    table = table_shape.table

    m_headers = ["Model Architecture", "Paradigm", "Test Accuracy", "Macro F1", "Inference Latency"]
    m_data = [
        ["DistilBERT", "Transformer Attention (66M params)", "97.8%", "0.976", "12.4 ms"],
        ["Linear SVM (Champion)", "Maximum-Margin (Platt Calibrated)", "96.4%", "0.963", "1.2 ms"],
        ["Neural MLP", "Multi-Layer Perceptron (128 units)", "95.1%", "0.948", "3.2 ms"],
        ["Multinomial Naive Bayes", "Generative Probabilistic", "92.1%", "0.920", "0.5 ms"]
    ]

    for j, h in enumerate(m_headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = INDIGO
        for p in cell.text_frame.paragraphs:
            p.font.name = "Calibri"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    for i, row_data in enumerate(m_data):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            if i == 1: # Highlight Linear SVM
                cell.fill.fore_color.rgb = RGBColor(236, 253, 245) # Mint green
            else:
                cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(12)
                p.font.bold = (i == 1)
                p.font.color.rgb = EMERALD if (i == 1 and j in [0, 2]) else NAVY

    # Callout Banner below table
    banner = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.4))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = BORDER_COLOR

    btb = s9.shapes.add_textbox(Inches(1.1), Inches(5.45), Inches(11.1), Inches(1.1))
    btf = btb.text_frame
    btf.word_wrap = True

    p = btf.paragraphs[0]
    p.text = "Key Empirical Takeaway: The Speed vs Accuracy Trade-off"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = INDIGO

    p2 = btf.add_paragraph()
    p2.text = "• DistilBERT achieves the highest raw accuracy (97.8%), but Linear SVM reaches 96.4% while running 10x faster (1.2 ms vs 12.4 ms) with 20x smaller memory footprint (<15 MB vs >260 MB). Linear SVM is crowned the Production Champion."
    p2.font.name = "Calibri"
    p2.font.size = Pt(12)
    p2.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 10: PER-DOMAIN ACCURACY BREAKDOWN
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Domain Evaluation", "Per-Domain Accuracy Breakdown (Linear SVM)")

    # 5 Metric Cards for Domains
    domains = [
        ("Sport", "99.0%", "101 / 102 correct", "Distinct athletic vocabulary (goal, cup, match, injury)"),
        ("Tech", "96.3%", "77 / 80 correct", "Software, mobile, hardware, broadband, internet"),
        ("Entertainment", "96.1%", "74 / 77 correct", "Film, festival, awards, music, box office"),
        ("Business", "96.1%", "98 / 102 correct", "Market, shares, profit, inflation, economy"),
        ("Politics", "94.0%", "79 / 84 correct", "Government, ministers, parliament, election, tax")
    ]

    for idx, (dom, acc, ratio, notes) in enumerate(domains):
        left = Inches(0.8 + idx * 2.38)
        c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(2.25), Inches(3.4))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s10.shapes.add_textbox(left + Inches(0.15), Inches(1.95), Inches(1.95), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = dom
        p.font.name = "Calibri"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p_acc = tf.add_paragraph()
        p_acc.text = acc
        p_acc.font.name = "Calibri"
        p_acc.font.size = Pt(30)
        p_acc.font.bold = True
        p_acc.font.color.rgb = EMERALD if dom in ["Sport", "Tech"] else INDIGO
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
        p_n.font.color.rgb = RGBColor(51, 65, 85)

    # Bottom Summary
    bs = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.3))
    bs.fill.solid()
    bs.fill.fore_color.rgb = CARD_BG
    bs.line.color.rgb = BORDER_COLOR

    btb = s10.shapes.add_textbox(Inches(1.1), Inches(5.5), Inches(11.1), Inches(1.1))
    btf = btb.text_frame
    btf.word_wrap = True
    p = btf.paragraphs[0]
    p.text = "Overall Weighted Test Accuracy: 429 / 445 = 96.4%"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p2 = btf.add_paragraph()
    p2.text = "• Sport achieves the highest accuracy (99.0%) due to specialized sports lexicons. Politics has the lowest (94.0%) due to overlap with macroeconomic terms in Business articles."
    p2.font.name = "Calibri"
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(51, 65, 85)

    # ==========================================
    # SLIDE 11: ERROR ANALYSIS & CONFUSION MATRIX
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Qualitative Diagnostics", "Error Analysis & Confusion Matrix Insights")

    # Left: Confusion Matrix Table
    c_rows = 6
    c_cols = 6
    cm_shape = s11.shapes.add_table(c_rows, c_cols, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.8))
    cm_table = cm_shape.table

    cm_headers = ["Actual \\ Pred", "Bus", "Ent", "Pol", "Spo", "Tec"]
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
        cell.fill.fore_color.rgb = INDIGO
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
                cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
            elif (i + 1) == j: # Diagonal
                cell.fill.fore_color.rgb = RGBColor(220, 252, 231) # Green
            elif int(val) > 0:
                cell.fill.fore_color.rgb = RGBColor(254, 226, 226) # Red error
            else:
                cell.fill.fore_color.rgb = CARD_BG

            for p in cell.text_frame.paragraphs:
                p.font.name = "Calibri"
                p.font.size = Pt(11)
                p.font.bold = (j > 0 and (i + 1) == j)
                p.font.color.rgb = NAVY

    # Right: Diagnostic Notes
    rc = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = BORDER_COLOR

    rtb = s11.shapes.add_textbox(Inches(7.45), Inches(2.05), Inches(4.8), Inches(4.3))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Key Misclassification Findings"
    p.font.name = "Calibri"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    diag_bullets = [
        "Primary Confusion Vector: Politics <-> Business. 2 Business articles misclassified as Politics; 2 Politics misclassified as Business.",
        "Root Cause: Shared vocabulary in economic legislation (chancellor, tax policy, treasury, budget deficit).",
        "Remediation: Bigrams (ngram_range=(1,2)) helped bind context ('tax policy' vs 'corporate tax').",
        "Sport Isolation: 99.0% recall, 98.1% precision. Only 1 article misclassified into politics ('Olympic committee election').",
        "Total errors: Only 16 articles out of 445 misclassified across the entire corpus."
    ]
    for b in diag_bullets:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(8)

    # ==========================================
    # SLIDE 12: MODEL EXPLAINABILITY
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Interpretability", "Peeking Inside the Black Box: Explainability")

    methods = [
        ("Feature Coefficient Extraction (Linear SVM)", "Linear SVM decisions are calculated via w^T * x + b. By extracting the top dot-product weights w_i * x_i for the predicted class, NewsScope highlights the exact words driving the outcome.", "Example: 'Apple unveils M3 processor' -> 'processor' (0.34), 'apple' (0.28), 'm3' (0.24)"),
        ("Platt Scaling Probability Calibration", "Standard SVMs output uncalibrated geometric margins. Platt Scaling fits a logistic regression sigmoid on top of margins, converting distances into trustworthy probabilities P(y | x).", "Example: Margin +2.45 -> 96.4% Calibrated Confidence"),
        ("Token Attention Heatmap Visualizer", "Every word in the input article is evaluated and color-coded dynamically in the frontend UI. Important tokens glow with higher saturation, giving users immediate visual validation.", "Visual UI: Interactive word highlight badges & percentage impact")
    ]

    for idx, (title, desc, ex) in enumerate(methods):
        top = Inches(1.8 + idx * 1.7)
        c = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.5))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s12.shapes.add_textbox(Inches(1.1), top + Inches(0.15), Inches(11.1), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.color.rgb = NAVY
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = ex
        p3.font.name = "Consolas"
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 13: WEB APPLICATION & LIVE DEMO
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Live Demonstration", "NewsScope Interactive Web Platform")

    features = [
        ("1. Real-Time Classifier", "• Paste raw text or enter news URLs\n• Instant classification with probability distribution\n• Saliency keywords & decision factor explanations\n• Optimistic UI with sub-second feedback"),
        ("2. 4-Model Architecture Consensus", "• Simultaneous parallel benchmark modal\n• Compares SVM, DistilBERT, MLP, and Naive Bayes live\n• Shows latency differences and cross-model agreement\n• Clean mobile-responsive portal layout"),
        ("3. High-Throughput Batch Processing", "• Drag-and-drop CSV files with hundreds of articles\n• Streaming progress bar with live status indicators\n• Instant batch export to CSV with category & confidence\n• Client-side validation & error recovery"),
        ("4. Performance Analytics Dashboard", "• Live Confusion Matrix heatmap\n• Dynamic Per-Domain Accuracy Breakdown bar chart\n• Metric cards (Accuracy, Macro F1, Precision, Recall)\n• Complete benchmark leaderboard")
    ]

    for idx, (title, desc) in enumerate(features):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.8 + (idx // 2) * 2.6)

        c = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.35))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s13.shapes.add_textbox(left + Inches(0.3), top + Inches(0.2), Inches(5.0), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(6)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Calibri"
            p.font.size = Pt(12)
            p.font.color.rgb = RGBColor(51, 65, 85)

    # ==========================================
    # SLIDE 14: LIMITATIONS & FUTURE SCOPE
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Critical Evaluation", "Limitations & Future Roadmap")

    # Left: Limitations
    lc = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    lc.fill.solid()
    lc.fill.fore_color.rgb = CARD_BG
    lc.line.color.rgb = BORDER_COLOR

    ltb = s14.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.6))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "Current Limitations"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(225, 29, 72) # Rose red
    p.space_after = Pt(12)

    lims = [
        "Historical Corpus: BBC 2004–2005 corpus lacks modern vocabulary (smartphones, LLMs, crypto, streaming).",
        "Single-Label Constraint: News articles touching multiple topics (e.g. Big Tech Antitrust) are forced into one label.",
        "Monolingual: Evaluated strictly on English language articles.",
        "Static Training: No automated concept drift detection or continuous online model retraining."
    ]
    for b in lims:
        p = ltf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    # Right: Future Scope
    rc = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = BORDER_COLOR

    rtb = s14.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.6))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Future Roadmap"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p.space_after = Pt(12)

    roadmap = [
        "Multi-Label Classification: Binary relevance / sigmoid thresholding for multi-topic stories.",
        "Multilingual Embeddings: Fine-tuning XLM-RoBERTa for cross-lingual news classification across 50+ languages.",
        "Active Learning: Routing low-confidence predictions (< 40%) to human editors for iterative active learning.",
        "Model Quantization: 8-bit ONNX runtime deployment to achieve sub-millisecond transformer inference."
    ]
    for b in roadmap:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 15: CONCLUSION
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, NAVY)

    tb = s15.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(5.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "PROJECT SUMMARY & TAKEAWAYS"
    p.font.name = "Calibri"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(129, 140, 248)
    p.space_after = Pt(12)

    p_t = tf.add_paragraph()
    p_t.text = "Conclusion"
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = RGBColor(255, 255, 255)
    p_t.space_after = Pt(20)

    concl_points = [
        "Empirical Validation: Linear SVM achieved 96.4% accuracy with 1.2ms latency, proving classical statistical methods remain superior for latency-critical production NLP.",
        "Methodological Rigor: Zero data leakage enforced through strict pipeline encapsulation and sublinear TF-IDF feature extraction.",
        "Transparency & Trust: Combined Platt probability scaling with dot-product keyword saliency to demystify black-box predictions.",
        "Production Delivery: Completed fully functional full-stack system with Next.js 14, FastAPI, batch CSV processing, and live analytics."
    ]
    for cp in concl_points:
        p = tf.add_paragraph()
        p.text = "✔  " + cp
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(12)

    # ==========================================
    # SLIDE 16: VIVA Q&A BACKUP SLIDE
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "Examiner Reference", "Viva Q&A Defense Cheat Sheet")

    qa_list = [
        ("Q1: Why TF-IDF over simple CountVectorizer?", "A: CountVectorizer lets frequent non-discriminative words dominate. TF-IDF uses Inverse Document Frequency to downweight common terms and emphasize informative domain keywords."),
        ("Q2: Why does Linear SVM perform so well on text?", "A: Cover's Theorem states high-dimensional sparse representations (10,000 features) are almost always linearly separable. Linear SVM finds the maximum-margin hyperplane without overfitting."),
        ("Q3: How is Zero Data Leakage strictly guaranteed?", "A: Vectorizer.fit() was called solely on the 1,780 training articles. The 445 test articles were only transformed using the pre-fit vocabulary. Out-of-vocabulary test terms are ignored."),
        ("Q4: Why choose DistilBERT over standard BERT?", "A: DistilBERT has 40% fewer parameters, runs 60% faster, and retains 97% of BERT's language comprehension capabilities via knowledge distillation.")
    ]

    for idx, (q, a) in enumerate(qa_list):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.8 + (idx // 2) * 2.6)

        c = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.35))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s16.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.1), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = q
        p1.font.name = "Calibri"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = a
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(51, 65, 85)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_deck()
