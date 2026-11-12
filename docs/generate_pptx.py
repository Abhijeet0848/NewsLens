import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path="docs/NewsScope_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Premium Modern Light Palette
    BG_WHITE = RGBColor(255, 255, 255)
    BG_OFFWHITE = RGBColor(248, 250, 252)     # #f8fafc
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)     # #e2e8f0
    CARD_HOVER_BORDER = RGBColor(203, 213, 225) # #cbd5e1

    # Text Colors
    COLOR_TITLE = RGBColor(15, 23, 42)        # Deep Charcoal/Navy #0f172a
    COLOR_BODY = RGBColor(51, 65, 85)         # Slate 700 #334155
    COLOR_MUTED = RGBColor(100, 116, 139)     # Slate 500 #64748b
    COLOR_LIGHT = RGBColor(148, 163, 184)     # Slate 400 #94a3b8

    # Accent Colors
    INDIGO = RGBColor(79, 70, 229)            # Indigo 600 #4f46e5
    INDIGO_BG = RGBColor(238, 242, 255)       # Indigo 50 #eef2ff
    EMERALD = RGBColor(5, 150, 105)           # Emerald 600 #059669
    EMERALD_BG = RGBColor(236, 253, 245)      # Emerald 50 #ecfdf5
    AMBER = RGBColor(217, 119, 6)             # Amber 600 #d97706
    AMBER_BG = RGBColor(254, 243, 199)        # Amber 50 #fef3c7
    ROSE = RGBColor(225, 29, 72)              # Rose 600 #e11d48
    ROSE_BG = RGBColor(255, 241, 242)         # Rose 50 #fff1f2
    BLUE = RGBColor(2, 132, 199)              # Sky 600 #0284c7
    BLUE_BG = RGBColor(240, 249, 255)         # Sky 50 #f0f9ff

    def set_slide_bg(slide, color=BG_OFFWHITE):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_slide_header(slide, section_num, section_name, title_text, subtitle_text=""):
        # Section Pill Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.45), Inches(3.2), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = INDIGO_BG
        badge.line.color.rgb = RGBColor(199, 210, 254)
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = False
        p_b = tf_b.paragraphs[0]
        p_b.text = f"{section_num.upper()}  •  {section_name.upper()}"
        p_b.font.name = "Segoe UI"
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = INDIGO

        # Main Title Box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.82), Inches(11.7), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p_title = tf.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TITLE

        if subtitle_text:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.name = "Segoe UI"
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 1: TITLE HERO (Modern Executive Light)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, BG_WHITE)

    # Top Accent Strip
    accent_strip = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.06))
    accent_strip.fill.solid()
    accent_strip.fill.fore_color.rgb = INDIGO
    accent_strip.line.fill.background()

    # Hero Badge
    hero_badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.1), Inches(4.5), Inches(0.35))
    hero_badge.fill.solid()
    hero_badge.fill.fore_color.rgb = INDIGO_BG
    hero_badge.line.color.rgb = RGBColor(199, 210, 254)
    p = hero_badge.text_frame.paragraphs[0]
    p.text = "ACADEMIC DEFENSE  •  MACHINE LEARNING & NLP"
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INDIGO

    # Main Title
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.7), Inches(2.2))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True

    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "NewsScope: Smart News Article Classifier"
    p_t1.font.name = "Segoe UI"
    p_t1.font.size = Pt(36)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_TITLE
    p_t1.space_after = Pt(8)

    p_t2 = tf_t.add_paragraph()
    p_t2.text = "An Interpretable, High-Throughput Classification System Benchmarking 4 AI Architectures"
    p_t2.font.name = "Segoe UI"
    p_t2.font.size = Pt(16)
    p_t2.font.color.rgb = COLOR_MUTED

    # 3 Stat Cards Side-by-Side
    stats = [
        ("96.4%", "Linear SVM Accuracy", "Tested on 445 unseen articles", EMERALD, EMERALD_BG),
        ("1.2 ms", "Inference Latency", "10x faster than transformers", INDIGO, INDIGO_BG),
        ("4 Models", "Benchmarked Head-to-Head", "SVM, DistilBERT, MLP, Naive Bayes", BLUE, BLUE_BG)
    ]
    for i, (big_num, lbl, sub, color, bg_col) in enumerate(stats):
        left = Inches(0.8 + i * 3.98)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(3.9), Inches(3.77), Inches(1.6))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s1.shapes.add_textbox(left + Inches(0.25), Inches(4.05), Inches(3.27), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = big_num
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TITLE

        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_MUTED

    # Bottom Presenter Footer
    foot = s1.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(11.7), Inches(0.5))
    p_f = foot.text_frame.paragraphs[0]
    p_f.text = "Presenter: Abhijeet   |   Dataset: BBC News (2,225 Articles, 5 Categories)   |   Stack: FastAPI + Next.js 14 + Scikit-Learn"
    p_f.font.name = "Segoe UI"
    p_f.font.size = Pt(11)
    p_f.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 2: AGENDA (7 Core Sections - Clean List Layout)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_slide_header(s2, "Overview", "Agenda", "Presentation Roadmap & Key Topics")

    agenda_items = [
        ("01", "Introduction & Objectives", "Why automated news classification matters, industry pain points, and zero data leakage."),
        ("02", "System Architecture & NLP Pipeline", "Decoupled Next.js 14 & FastAPI full-stack design, plus the 5-stage text processing flow."),
        ("03", "Machine Learning Models", "Plain English explanation of Naive Bayes, Linear SVM, Neural MLP, & DistilBERT."),
        ("04", "Dataset & Experimental Results", "BBC 2,225 corpus analysis, 4-model performance leaderboard, and per-domain accuracy."),
        ("05", "Error Analysis & Explainability", "Confusion matrix dynamics, shared vocabulary overlap, Platt scaling, and word saliency."),
        ("06", "Application Features (Live Demo)", "Real-time example walkthrough, 4-model consensus modal, batch CSV, and analytics."),
        ("07", "Conclusion & Future Scope", "Key takeaways, project limitations, future roadmap, and Viva defense backup.")
    ]

    for i, (num, title, desc) in enumerate(agenda_items):
        col = i // 4
        row = i % 4
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.8 + row * 1.25)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(1.12))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Number circle badge
        num_badge = s2.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.2), top + Inches(0.22), Inches(0.68), Inches(0.68))
        num_badge.fill.solid()
        num_badge.fill.fore_color.rgb = INDIGO_BG
        num_badge.line.fill.background()
        p_n = num_badge.text_frame.paragraphs[0]
        p_n.text = num
        p_n.font.name = "Segoe UI"
        p_n.font.size = Pt(12)
        p_n.font.bold = True
        p_n.font.color.rgb = INDIGO
        p_n.alignment = PP_ALIGN.CENTER

        tb = s2.shapes.add_textbox(left + Inches(1.05), top + Inches(0.12), Inches(4.45), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TITLE

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SECTION 1: INTRODUCTION & OBJECTIVES
    # =========================================================================

    # SLIDE 3: PROBLEM STATEMENT & MOTIVATION
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_slide_header(s3, "Section 01", "Introduction & Objectives", "Why Automated News Classification Matters", "The Information Overload Challenge & The AI Black-Box Gap")

    # Left: The Real-World Problem
    c_left = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.65), Inches(4.9))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CARD_BORDER

    tb_l = s3.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(5.05), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "The Real-World Industry Challenge"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITLE
    p.space_after = Pt(12)

    prob_bullets = [
        ("Massive Content Volume", "Over 500 million news articles and blog posts are published online every day across the globe."),
        ("Manual Tagging is Impossible", "Newsrooms cannot hire enough editors to read and categorize thousands of incoming wire stories."),
        ("Strict Speed Demands", "Editorial portals and news feeds require real-time classification in under 20 milliseconds."),
        ("Human Inconsistency", "Different editors frequently assign different tags to the exact same article.")
    ]
    for title, desc in prob_bullets:
        p1 = tf_l.add_paragraph()
        p1.text = f"•  {title}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(1)

        p2 = tf_l.add_paragraph()
        p2.text = f"    {desc}"
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_BODY
        p2.space_after = Pt(8)

    # Right: The Black-Box Gap & NewsScope Fix
    c_right = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.85), Inches(5.7), Inches(4.9))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = CARD_BG
    c_right.line.color.rgb = CARD_BORDER

    tb_r = s3.shapes.add_textbox(Inches(7.1), Inches(2.05), Inches(5.1), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "The 'Black-Box' Gap & Our Fix"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p.space_after = Pt(12)

    sol_bullets = [
        ("Black-Box Predictions", "Most AI models output a category without explaining why, making validation difficult."),
        ("Editorial Trust & Auditability", "Journalists require clear keyword justifications before publishing automated tags."),
        ("Data Leakage in Research", "Many ML projects clean train and test text together, creating fake inflated metrics."),
        ("The NewsScope Solution", "A zero-leakage, transparent system delivering 96.4% accuracy in 1.2 ms with word saliency.")
    ]
    for title, desc in sol_bullets:
        p1 = tf_r.add_paragraph()
        p1.text = f"✔  {title}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = EMERALD
        p1.space_after = Pt(1)

        p2 = tf_r.add_paragraph()
        p2.text = f"    {desc}"
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_BODY
        p2.space_after = Pt(8)

    # SLIDE 4: CORE PROJECT OBJECTIVES
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_slide_header(s4, "Section 01", "Introduction & Objectives", "Core Engineering Objectives", "Four foundational pillars guiding system design and scientific evaluation")

    obj_cards = [
        ("1. Zero Data Leakage Pipeline", "Strict scientific separation between training and test sets. Vocabulary and TF-IDF weights are learned strictly from training data; test data remains 100% unseen.", INDIGO),
        ("2. 4-Model Architecture Benchmark", "Systematic evaluation of 4 distinct ML paradigms on the identical test split: Naive Bayes (probability), Linear SVM (geometry), MLP (neural net), and DistilBERT (transformer).", BLUE),
        ("3. Model Interpretability & Saliency", "Eliminate black-box ambiguity. Extract top keyword weights via hyperplane feature coefficients and display calibrated confidence percentages (Platt scaling).", EMERALD),
        ("4. Production Full-Stack Web Platform", "Deliver a complete, responsive web application with sub-second single inference, live 4-model consensus dialog, and high-throughput CSV batch uploading.", AMBER)
    ]

    for i, (title, desc, color) in enumerate(obj_cards):
        left = Inches(0.8 + (i % 2) * 5.95)
        top = Inches(1.85 + (i // 2) * 2.5)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(2.25))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        # Color Accent Top Strip
        top_strip = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(0.08))
        top_strip.fill.solid()
        top_strip.fill.fore_color.rgb = color
        top_strip.line.fill.background()

        tb = s4.shapes.add_textbox(left + Inches(0.3), top + Inches(0.2), Inches(5.05), Inches(1.85))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TITLE
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_BODY

    # =========================================================================
    # SECTION 2: SYSTEM ARCHITECTURE & NLP PIPELINE
    # =========================================================================

    # SLIDE 5: SYSTEM ARCHITECTURE
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_slide_header(s5, "Section 02", "System Architecture & NLP Pipeline", "Decoupled Full-Stack Architecture", "High-performance separation of concerns between client, gateway, and ML engine")

    tiers = [
        ("Tier 1: Client Application (Next.js 14 App Router)",
         "• Built with Next.js 14, React 18, and Tailwind CSS for modern responsive aesthetics.\n• Uses Zustand state management with atomic selectors so typing does not re-render heavy components.\n• Interactive Recharts dashboards (per-domain accuracy breakdown and confusion matrix heatmaps).",
         BLUE, BLUE_BG),
        ("Tier 2: API Gateway (FastAPI 0.115 Async REST)",
         "• Ultra-fast asynchronous Python REST service delivering sub-millisecond routing overhead.\n• Pydantic v2 schemas for strict input sanitization, runtime validation, and CORS security.\n• Endpoints: POST /api/classify (single inference), GET /api/dataset (corpus metrics).",
         INDIGO, INDIGO_BG),
        ("Tier 3: Machine Learning Engine (Scikit-Learn & PyTorch)",
         "• Serialized pipelines loaded instantly into memory via Joblib.\n• Linear SVM (Production Champion) with Platt scaling for honest calibrated probabilities.\n• Supports live parallel consensus inference across Naive Bayes, Neural MLP, and DistilBERT.",
         EMERALD, EMERALD_BG)
    ]

    for i, (title, desc, color, bg_col) in enumerate(tiers):
        top = Inches(1.85 + i * 1.65)
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.48))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        # Left Accent Bar
        bar = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(0.12), Inches(1.48))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb = s5.shapes.add_textbox(Inches(1.15), top + Inches(0.12), Inches(11.1), Inches(1.22))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TITLE
        p1.space_after = Pt(4)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_BODY

    # SLIDE 6: 5-STAGE NLP PIPELINE
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_slide_header(s6, "Section 02", "System Architecture & NLP Pipeline", "5-Stage Zero-Leakage Text Pipeline", "Systematic transformation from raw natural language strings to numerical sparse feature vectors")

    steps = [
        ("Step 1", "Clean & Normalise", "Lowercased and stripped punctuation, URLs, and HTML tags.", "'Apple's NEW iPhone @ $999!' -> 'apples new iphone 999'"),
        ("Step 2", "Word Tokenization", "Splits the string into individual linguistic word units.", "['apples', 'new', 'iphone', '999']"),
        ("Step 3", "Stopword Pruning", "Filters out 179 high-frequency, uninformative English words.", "['apples', 'iphone', '999']"),
        ("Step 4", "Lemmatization", "WordNet morphologically reduces words to dictionary lemmas.", "['apple', 'iphone', '999']"),
        ("Step 5", "Sublinear TF-IDF", "Converts words to 10,000-D sparse vector (unigram + bigram).", "[0.42, 0.61, 0.28, ...]")
    ]

    for i, (step_num, title, desc, ex) in enumerate(steps):
        left = Inches(0.8 + i * 2.38)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.85), Inches(2.25), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        # Number Badge
        nb = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), Inches(2.05), Inches(1.85), Inches(0.35))
        nb.fill.solid()
        nb.fill.fore_color.rgb = INDIGO_BG
        nb.line.fill.background()
        p = nb.text_frame.paragraphs[0]
        p.text = step_num.upper()
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = INDIGO
        p.alignment = PP_ALIGN.CENTER

        tb = s6.shapes.add_textbox(left + Inches(0.15), Inches(2.5), Inches(1.95), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TITLE
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_BODY
        p2.space_after = Pt(14)

        p3 = tf.add_paragraph()
        p3.text = "Example Transformation:"
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(9.5)
        p3.font.bold = True
        p3.font.color.rgb = INDIGO

        p4 = tf.add_paragraph()
        p4.text = ex
        p4.font.name = "Consolas"
        p4.font.size = Pt(9)
        p4.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SECTION 3: MACHINE LEARNING MODELS
    # =========================================================================

    # SLIDE 7: MACHINE LEARNING MODELS (PLAIN ENGLISH)
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_slide_header(s7, "Section 03", "Machine Learning Models", "The 4 Machine Learning Models Explained", "Benchmarking probabilistic, geometric, neural, and attention-based architectures")

    models = [
        ("1. Multinomial Naive Bayes", "Generative Probabilistic Baseline", "0.5 ms Latency  |  92.1% Accuracy",
         "• Multiplies word likelihoods assuming conditional feature independence given class label.\n• Laplace smoothing (alpha=0.1) prevents zero-probability traps for unseen words.\n• Ultra-lightweight memory footprint (< 5 MB); ideal baseline.", BLUE, BLUE_BG),
        ("2. Linear SVM (Our Production Champion)", "Maximum-Margin Geometric Classifier", "1.2 ms Latency  |  96.4% Accuracy",
         "• Cover's Theorem: High-dimensional sparse text (10,000 features) is linearly separable.\n• Identifies the maximum-margin hyperplane separating topics without overfitting.\n• 10x faster than DistilBERT; fitted with Platt scaling for honest calibrated probabilities.", EMERALD, EMERALD_BG),
        ("3. Neural MLP (Multi-Layer Perceptron)", "Discriminative Artificial Neural Network", "3.2 ms Latency  |  95.1% Accuracy",
         "• Two dense layers with 128 hidden neurons, ReLU activations, and Adam optimizer.\n• Learns non-linear interactions between word combinations across domains.\n• Balanced performance between statistical and deep learning approaches.", AMBER, AMBER_BG),
        ("4. DistilBERT Transformer", "Self-Attention Deep Learning Architecture", "12.4 ms Latency  |  97.8% Accuracy",
         "• 6 transformer layers, 66M parameters, bidirectional contextual understanding.\n• Knowledge-distilled from BERT-base; retains 97% of language comprehension.\n• Highest raw accuracy, but requires GPU/heavy CPU and 260 MB memory.", INDIGO, INDIGO_BG)
    ]

    for i, (title, sub, badge, desc, color, bg_col) in enumerate(models):
        left = Inches(0.8 + (i % 2) * 5.95)
        top = Inches(1.85 + (i // 2) * 2.5)

        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        # Top Bar
        bar = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb = s7.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), Inches(5.15), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TITLE

        p_sub = tf.add_paragraph()
        p_sub.text = f"{sub}   •   {badge}"
        p_sub.font.name = "Segoe UI"
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = color
        p_sub.space_after = Pt(6)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Segoe UI"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_BODY

    # =========================================================================
    # SECTION 4: DATASET & EXPERIMENTAL RESULTS
    # =========================================================================

    # SLIDE 8: BBC NEWS CORPUS
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_slide_header(s8, "Section 04", "Dataset & Experimental Results", "BBC News Dataset & Class Distribution", "2,225 genuine news articles evaluated under a strict stratified 80/20 train/test split")

    table_shape = s8.shapes.add_table(6, 4, Inches(0.8), Inches(1.85), Inches(5.8), Inches(4.9))
    table = table_shape.table

    headers = ["News Category", "Articles", "Share (%)", "Held-Out Test (20%)"]
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
        cell.fill.fore_color.rgb = INDIGO
        for p in cell.text_frame.paragraphs:
            p.font.name = "Segoe UI"
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else BG_OFFWHITE
            for p in cell.text_frame.paragraphs:
                p.font.name = "Segoe UI"
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_TITLE

    # Right: Dataset Details
    rc = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.85), Inches(5.5), Inches(4.9))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = CARD_BORDER

    tb_r = s8.shapes.add_textbox(Inches(7.25), Inches(2.05), Inches(5.0), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "Dataset Characteristics & Integrity"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITLE
    p.space_after = Pt(12)

    bullets = [
        ("Benchmark Corpus", "Standard academic dataset compiled by Greene & Cunningham (2006)."),
        ("Natural Balance", "Balanced across 5 domains (386 to 511 articles); no artificial SMOTE required."),
        ("Stratified Split", "80% Training (1,780 articles) / 20% Unseen Testing (445 articles)."),
        ("Article Length", "Average length of ~2,200 characters (~380 words) per article."),
        ("Zero Leakage Guarantee", "TF-IDF vocabulary built exclusively on train split. Test set treated strictly as unseen incoming stream.")
    ]
    for title, desc in bullets:
        p1 = tf_r.add_paragraph()
        p1.text = f"•  {title}:"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(1)

        p2 = tf_r.add_paragraph()
        p2.text = f"    {desc}"
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_BODY
        p2.space_after = Pt(6)

    # SLIDE 9: 4-MODEL LEADERBOARD & RESULTS
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_slide_header(s9, "Section 04", "Dataset & Experimental Results", "4-Model Performance Benchmark", "Empirical evaluation across 445 unseen held-out test articles")

    table_shape = s9.shapes.add_table(5, 5, Inches(0.8), Inches(1.85), Inches(11.7), Inches(3.2))
    table = table_shape.table

    m_headers = ["Model Name", "Paradigm / Technique", "Test Accuracy", "Macro F1 Score", "Speed (Latency)"]
    m_data = [
        ["DistilBERT", "Transformer Attention (66M params)", "97.8%", "0.976", "12.4 ms"],
        ["Linear SVM (Winner)", "Maximum-Margin Line (Platt Scaled)", "96.4%", "0.963", "1.2 ms"],
        ["Neural MLP", "Neural Network (128 units, ReLU)", "95.1%", "0.948", "3.2 ms"],
        ["Multinomial Naive Bayes", "Generative Probabilistic", "92.1%", "0.920", "0.5 ms"]
    ]

    for j, h in enumerate(m_headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = INDIGO
        for p in cell.text_frame.paragraphs:
            p.font.name = "Segoe UI"
            p.font.size = Pt(11.5)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(m_data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            if i == 1:
                cell.fill.fore_color.rgb = EMERALD_BG
            else:
                cell.fill.fore_color.rgb = CARD_BG if i % 2 == 0 else BG_OFFWHITE
            for p in cell.text_frame.paragraphs:
                p.font.name = "Segoe UI"
                p.font.size = Pt(11.5)
                p.font.bold = (i == 1)
                p.font.color.rgb = EMERALD if (i == 1 and j in [0, 2]) else COLOR_TITLE

    # Callout Banner below table
    banner = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.35), Inches(11.7), Inches(1.5))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = CARD_BORDER

    btb = s9.shapes.add_textbox(Inches(1.1), Inches(5.5), Inches(11.1), Inches(1.2))
    btf = btb.text_frame
    btf.word_wrap = True

    p = btf.paragraphs[0]
    p.text = "Empirical Finding: The Accuracy vs Speed Trade-off in Production"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = INDIGO

    p2 = btf.add_paragraph()
    p2.text = "• DistilBERT achieves the highest accuracy (97.8%), but Linear SVM reaches 96.4% while running 10x faster (1.2 ms vs 12.4 ms) with 20x smaller memory footprint (< 15 MB vs > 260 MB). Linear SVM is crowned the Production Champion."
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_BODY

    # SLIDE 10: PER-DOMAIN ACCURACY BREAKDOWN
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_slide_header(s10, "Section 04", "Dataset & Experimental Results", "Per-Domain Accuracy Breakdown (Linear SVM)", "Overall Test Accuracy: 429 / 445 = 96.4% across 5 domains")

    domains = [
        ("Sport", "99.0%", "101 / 102 correct", "Distinct sports lexicon (match, cup, goal, injury, coach)"),
        ("Tech", "96.3%", "77 / 80 correct", "Software, mobile, hardware, broadband, computer"),
        ("Entertainment", "96.1%", "74 / 77 correct", "Film, festival, awards, music, box office, actress"),
        ("Business", "96.1%", "98 / 102 correct", "Market, shares, profit, inflation, bank, economy"),
        ("Politics", "94.0%", "79 / 84 correct", "Government, minister, parliament, election, tax policy")
    ]

    for i, (dom, acc, ratio, notes) in enumerate(domains):
        left = Inches(0.8 + i * 2.38)
        c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.85), Inches(2.25), Inches(3.4))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s10.shapes.add_textbox(left + Inches(0.15), Inches(2.0), Inches(1.95), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = dom
        p.font.name = "Segoe UI"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_TITLE

        p_acc = tf.add_paragraph()
        p_acc.text = acc
        p_acc.font.name = "Segoe UI"
        p_acc.font.size = Pt(28)
        p_acc.font.bold = True
        p_acc.font.color.rgb = EMERALD if dom in ["Sport", "Tech"] else INDIGO
        p_acc.space_after = Pt(2)

        p_r = tf.add_paragraph()
        p_r.text = ratio
        p_r.font.name = "Segoe UI"
        p_r.font.size = Pt(10.5)
        p_r.font.color.rgb = COLOR_MUTED
        p_r.space_after = Pt(8)

        p_n = tf.add_paragraph()
        p_n.text = notes
        p_n.font.name = "Segoe UI"
        p_n.font.size = Pt(10)
        p_n.font.color.rgb = COLOR_BODY

    # Bottom Summary
    bs = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.45), Inches(11.7), Inches(1.4))
    bs.fill.solid()
    bs.fill.fore_color.rgb = CARD_BG
    bs.line.color.rgb = CARD_BORDER

    btb = s10.shapes.add_textbox(Inches(1.1), Inches(5.55), Inches(11.1), Inches(1.15))
    btf = btb.text_frame
    btf.word_wrap = True
    p = btf.paragraphs[0]
    p.text = "Key Qualitative Takeaway on Category Separation:"
    p.font.name = "Segoe UI"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITLE

    p2 = btf.add_paragraph()
    p2.text = "• Sport achieved the highest score (99.0%) due to specialized sports lexicons. Politics has the lowest score (94.0%) because politicians frequently debate macroeconomic topics (taxation, national budgets, inflation), which naturally overlaps with Business."
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_BODY

    # =========================================================================
    # SECTION 5: ERROR ANALYSIS & EXPLAINABILITY
    # =========================================================================

    # SLIDE 11: ERROR ANALYSIS & CONFUSION MATRIX
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_slide_header(s11, "Section 05", "Error Analysis & Explainability", "Error Analysis & Confusion Matrix Dynamics", "Only 16 misclassifications out of 445 held-out articles across the entire corpus")

    cm_shape = s11.shapes.add_table(6, 6, Inches(0.8), Inches(1.85), Inches(5.8), Inches(4.9))
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
        cell.fill.fore_color.rgb = INDIGO
        for p in cell.text_frame.paragraphs:
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(cm_data):
        for j, val in enumerate(row):
            cell = cm_table.cell(i + 1, j)
            cell.text = val
            cell.fill.solid()
            if j == 0:
                cell.fill.fore_color.rgb = BG_OFFWHITE
            elif (i + 1) == j:
                cell.fill.fore_color.rgb = EMERALD_BG
            elif int(val) > 0:
                cell.fill.fore_color.rgb = ROSE_BG
            else:
                cell.fill.fore_color.rgb = CARD_BG

            for p in cell.text_frame.paragraphs:
                p.font.name = "Segoe UI"
                p.font.size = Pt(11)
                p.font.bold = (j > 0 and (i + 1) == j)
                p.font.color.rgb = COLOR_TITLE

    # Right: Diagnostic Notes
    rc = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.85), Inches(5.5), Inches(4.9))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = CARD_BORDER

    rtb = s11.shapes.add_textbox(Inches(7.25), Inches(2.05), Inches(5.0), Inches(4.5))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Key Qualitative Diagnostics"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITLE
    p.space_after = Pt(12)

    diag_bullets = [
        ("Only 16 Mistakes", "Out of 445 unseen test articles, 429 were classified correctly (96.4%)."),
        ("Politics <-> Business Confusion", "Primary error vector: 2 Business articles misclassified as Politics; 2 Politics misclassified as Business."),
        ("Lexical Overlap", "Caused by overlapping financial and government vocabulary ('budget deficit', 'chancellor', 'taxation')."),
        ("Bigram Resolution", "Unigrams + Bigrams ('corporate tax' vs 'tax policy') resolved 80% of borderline ambiguities."),
        ("Sport Isolation", "99.0% recall. Only 1 article misclassified ('Olympic committee governance election' -> Politics).")
    ]
    for title, desc in diag_bullets:
        p1 = rtf.add_paragraph()
        p1.text = f"•  {title}:"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(1)

        p2 = rtf.add_paragraph()
        p2.text = f"    {desc}"
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_BODY
        p2.space_after = Pt(6)

    # SLIDE 12: MODEL EXPLAINABILITY
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_slide_header(s12, "Section 05", "Error Analysis & Explainability", "Opening the Black Box: Model Explainability", "Transforming opaque machine learning predictions into auditable keyword saliency")

    methods = [
        ("1. Feature Coefficient Extraction (Linear SVM)", "Linear SVM decisions follow f(x) = w^T * x + b. By multiplying feature values by their hyperplane weights (w_i * x_i), NewsScope reveals the exact words driving the outcome.", "Example: 'processor' (+0.35) and 'macbook' (+0.28) strongly pull the prediction toward Technology."),
        ("2. Calibrated Confidence Percentages (Platt Scaling)", "Standard SVMs output raw distance values. Platt Scaling trains a logistic regression sigmoid on top of margins, converting distances into statistically honest probabilities.", "Example: Margin +2.45 -> 96.4% calibrated confidence percentage."),
        ("3. Color-Coded Word Saliency Highlights", "In our Next.js frontend, influential words light up with vibrant badges, giving editorial staff instant visual confirmation of the classifier's reasoning.", "User Experience: Dynamic token badges showing top keyword weights.")
    ]

    for i, (title, desc, ex) in enumerate(methods):
        top = Inches(1.85 + i * 1.65)
        c = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.48))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        bar = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(0.12), Inches(1.48))
        bar.fill.solid()
        bar.fill.fore_color.rgb = INDIGO
        bar.line.fill.background()

        tb = s12.shapes.add_textbox(Inches(1.15), top + Inches(0.12), Inches(11.1), Inches(1.22))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TITLE
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_BODY
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = ex
        p3.font.name = "Consolas"
        p3.font.size = Pt(10)
        p3.font.color.rgb = INDIGO

    # =========================================================================
    # SECTION 6: APPLICATION FEATURES (LIVE DEMO)
    # =========================================================================

    # SLIDE 13: APPLICATION FEATURES OVERVIEW
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_slide_header(s13, "Section 06", "Application Features (Live Demo)", "NewsScope Web Platform Capabilities", "Interactive software features built with Next.js 14 and FastAPI")

    features = [
        ("1. Real-Time Classifier Portal", "• Instant single article classification in under 1 second.\n• Real-time confidence percentage bar across all 5 domains.\n• Optimistic UI: typing is responsive with zero keystroke lag.", BLUE),
        ("2. 4-Model Consensus Modal", "• Click 'Compare All Models' to benchmark all 4 architectures live.\n• Displays execution latency, individual confidence, and agreement.\n• Demonstrates the speed difference between SVM and DistilBERT.", INDIGO),
        ("3. High-Throughput Batch CSV Processor", "• Drag and drop CSV files with hundreds of news articles.\n• Client-side streaming progress bar with error recovery.\n• Instant CSV export with predicted category and confidence scores.", EMERALD),
        ("4. Performance Analytics Dashboard", "• Live bar chart showing Per-Domain Accuracy Breakdown.\n• Interactive Confusion Matrix heatmap showing where errors occur.\n• Full system metrics: Accuracy, Precision, Recall, and Macro F1.", AMBER)
    ]

    for i, (title, desc, color) in enumerate(features):
        left = Inches(0.8 + (i % 2) * 5.95)
        top = Inches(1.85 + (i // 2) * 2.5)

        card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(2.25))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        bar = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb = s13.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), Inches(5.15), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TITLE
        p1.space_after = Pt(6)

        for line in desc.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Segoe UI"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_BODY

    # SLIDE 14: LIVE DEMO REAL-TIME WALKTHROUGH EXAMPLE (UI MOCKUP CARD)
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)
    add_slide_header(s14, "Section 06", "Application Features (Live Demo)", "Real-Time Demonstration: Step-by-Step Example", "Tracing a genuine news headline through cleaning, inference, explainability, and consensus")

    # Left: Input & Pipeline Transformation
    c_left = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.65), Inches(4.9))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CARD_BORDER

    tb_l = s14.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.15), Inches(4.5))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "1. Input Article & Pipeline Transformation"
    p.font.name = "Segoe UI"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = INDIGO
    p.space_after = Pt(8)

    p_in_lbl = tf_l.add_paragraph()
    p_in_lbl.text = "Live Article Entered in Classifier:"
    p_in_lbl.font.name = "Segoe UI"
    p_in_lbl.font.size = Pt(11)
    p_in_lbl.font.bold = True
    p_in_lbl.font.color.rgb = COLOR_TITLE

    p_in = tf_l.add_paragraph()
    p_in.text = "\"Apple unveils new M3 MacBook laptop with ultra-fast processor, 22-hour battery life, and high performance graphics for developers.\""
    p_in.font.name = "Consolas"
    p_in.font.size = Pt(10)
    p_in.font.color.rgb = COLOR_TITLE
    p_in.space_after = Pt(10)

    pipeline_steps = [
        "1. Cleansed: 'apple unveils new m3 macbook laptop ultrafast processor 22hour battery life high performance graphics developers'",
        "2. Stopwords Dropped: filtered 'with', 'and', 'for'",
        "3. Lemmatized: 'features' -> 'feature', 'unveils' -> 'unveil'",
        "4. Converted: 10,000-dimensional TF-IDF sparse vector"
    ]
    for step in pipeline_steps:
        p = tf_l.add_paragraph()
        p.text = "• " + step
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_BODY
        p.space_after = Pt(4)

    # Right: Prediction, Keywords, Consensus
    c_right = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.85), Inches(5.7), Inches(4.9))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = CARD_BG
    c_right.line.color.rgb = CARD_BORDER

    tb_r = s14.shapes.add_textbox(Inches(7.05), Inches(2.05), Inches(5.2), Inches(4.5))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "2. Prediction & Model Consensus"
    p.font.name = "Segoe UI"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p.space_after = Pt(8)

    p_res = tf_r.add_paragraph()
    p_res.text = "Predicted Category: TECHNOLOGY  (98.4% Confidence)"
    p_res.font.name = "Segoe UI"
    p_res.font.size = Pt(14)
    p_res.font.bold = True
    p_res.font.color.rgb = COLOR_TITLE
    p_res.space_after = Pt(6)

    p_kw = tf_r.add_paragraph()
    p_kw.text = "Top Explanatory Keywords:"
    p_kw.font.name = "Segoe UI"
    p_kw.font.size = Pt(11)
    p_kw.font.bold = True
    p_kw.font.color.rgb = INDIGO

    keywords = ["processor (+0.35)", "apple (+0.28)", "laptop (+0.24)", "developer (+0.18)"]
    p_chips = tf_r.add_paragraph()
    p_chips.text = "  |  ".join(keywords)
    p_chips.font.name = "Consolas"
    p_chips.font.size = Pt(10)
    p_chips.font.color.rgb = COLOR_TITLE
    p_chips.space_after = Pt(10)

    p_con_lbl = tf_r.add_paragraph()
    p_con_lbl.text = "4-Model Consensus Modal:"
    p_con_lbl.font.name = "Segoe UI"
    p_con_lbl.font.size = Pt(11)
    p_con_lbl.font.bold = True
    p_con_lbl.font.color.rgb = COLOR_TITLE

    models_consensus = [
        "Linear SVM: Technology (98.4% | 1.2 ms)",
        "DistilBERT: Technology (99.1% | 12.4 ms)",
        "Neural MLP: Technology (97.0% | 3.2 ms)",
        "Naive Bayes: Technology (93.5% | 0.5 ms)"
    ]
    for mc in models_consensus:
        p = tf_r.add_paragraph()
        p.text = "✔ " + mc
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_BODY
        p.space_after = Pt(2)

    p_verdict = tf_r.add_paragraph()
    p_verdict.text = "Result: 100% agreement across all 4 architectures!"
    p_verdict.font.name = "Segoe UI"
    p_verdict.font.size = Pt(11.5)
    p_verdict.font.bold = True
    p_verdict.font.color.rgb = EMERALD

    # =========================================================================
    # SECTION 7: CONCLUSION & FUTURE SCOPE
    # =========================================================================

    # SLIDE 15: LIMITATIONS & FUTURE SCOPE
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15)
    add_slide_header(s15, "Section 07", "Conclusion & Future Scope", "Current Limitations & Future Roadmap", "Honest critical evaluation of system constraints and engineering roadmap")

    # Left: Limitations
    lc = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.65), Inches(4.9))
    lc.fill.solid()
    lc.fill.fore_color.rgb = CARD_BG
    lc.line.color.rgb = CARD_BORDER

    ltb = s15.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.15), Inches(4.5))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "Current Limitations"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ROSE
    p.space_after = Pt(12)

    lims = [
        ("Historical Dataset", "BBC 2005 corpus lacks modern vocabulary (smartphones, LLMs, crypto, streaming)."),
        ("Single-Label Constraint", "Real-world stories can span multiple domains (e.g. Big Tech antitrust) but receive one label."),
        ("Monolingual Processing", "Evaluated strictly on English news articles."),
        ("Static Training", "No automated concept drift detection or continuous online retraining.")
    ]
    for title, desc in lims:
        p1 = ltf.add_paragraph()
        p1.text = f"•  {title}:"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = ROSE
        p1.space_after = Pt(1)

        p2 = ltf.add_paragraph()
        p2.text = f"    {desc}"
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_BODY
        p2.space_after = Pt(6)

    # Right: Future Scope
    rc = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.85), Inches(5.7), Inches(4.9))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = CARD_BORDER

    rtb = s15.shapes.add_textbox(Inches(7.05), Inches(2.05), Inches(5.2), Inches(4.5))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Future Roadmap"
    p.font.name = "Segoe UI"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p.space_after = Pt(12)

    roadmap = [
        ("Multi-Label Tagging", "Binary relevance / sigmoid thresholding for multi-topic stories."),
        ("Multilingual Embeddings", "Fine-tuning XLM-RoBERTa for cross-lingual news classification across 50+ languages."),
        ("Active Learning Loop", "Routing low-confidence predictions (< 50%) to editors for iterative active learning."),
        ("Model Quantization", "8-bit ONNX runtime deployment to achieve sub-millisecond transformer inference.")
    ]
    for title, desc in roadmap:
        p1 = rtf.add_paragraph()
        p1.text = f"✔  {title}:"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = EMERALD
        p1.space_after = Pt(1)

        p2 = rtf.add_paragraph()
        p2.text = f"    {desc}"
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_BODY
        p2.space_after = Pt(6)

    # SLIDE 16: CONCLUSION (LIGHT THEME HERO)
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s16, BG_WHITE)

    # Top Accent Strip
    strip = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.06))
    strip.fill.solid()
    strip.fill.fore_color.rgb = EMERALD
    strip.line.fill.background()

    tb = s16.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(5.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p_badge = tf.paragraphs[0]
    p_badge.text = "SECTION 07  •  CONCLUSION & KEY TAKEAWAYS"
    p_badge.font.name = "Segoe UI"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = INDIGO
    p_badge.space_after = Pt(8)

    p_t = tf.add_paragraph()
    p_t.text = "Project Summary & Engineering Conclusion"
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(32)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_TITLE
    p_t.space_after = Pt(20)

    concl_points = [
        ("High Performance", "Linear SVM achieved 96.4% accuracy at 1.2 ms latency, showing simple math beats heavy neural nets in real-world efficiency."),
        ("Methodological Rigor", "Zero data leakage enforced through strict pipeline encapsulation and sublinear TF-IDF feature extraction."),
        ("Transparency & Trust", "Solved the black-box dilemma using hyperplane feature coefficients and Platt-scaled calibrated probabilities."),
        ("Production Delivery", "Completed fully functional full-stack system with Next.js 14, FastAPI, batch CSV processing, and live analytics.")
    ]
    for title, desc in concl_points:
        p1 = tf.add_paragraph()
        p1.text = f"✔  {title}:  {desc}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.color.rgb = COLOR_BODY
        p1.space_after = Pt(12)

    # SLIDE 17: VIVA VOCE DEFENSE CHEAT SHEET
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s17)
    add_slide_header(s17, "Backup", "Viva Voce Defense Cheat Sheet", "Common Examiner Questions & Concise Answers", "Rapid reference for theoretical and methodological evaluation")

    qa_list = [
        ("Q1: Why TF-IDF over simple CountVectorizer?", "Answer: CountVectorizer lets common filler words dominate. TF-IDF uses Inverse Document Frequency to downweight ubiquitous words and highlight discriminative topic terms like 'striker' or 'inflation'."),
        ("Q2: Why does Linear SVM perform so well on text?", "Answer: Cover's Theorem states that high-dimensional sparse representations (10,000 features) are linearly separable with high probability. Linear SVM finds the maximum-margin hyperplane without overfitting."),
        ("Q3: How did you strictly guarantee Zero Data Leakage?", "Answer: TfidfVectorizer.fit() was called exclusively on the 1,780 training articles. The 445 test articles were only transformed using the pre-fit vocabulary. Test words are completely ignored during fitting."),
        ("Q4: Why choose DistilBERT over standard BERT?", "Answer: DistilBERT retains 97% of BERT's language comprehension capabilities via knowledge distillation, while using 40% fewer parameters and running 60% faster.")
    ]

    for i, (q, a) in enumerate(qa_list):
        left = Inches(0.8 + (i % 2) * 5.95)
        top = Inches(1.85 + (i // 2) * 2.5)

        card = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(2.25))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        bar = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = INDIGO
        bar.line.fill.background()

        tb = s17.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), Inches(5.15), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = q
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = a
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_BODY

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    build_presentation()
