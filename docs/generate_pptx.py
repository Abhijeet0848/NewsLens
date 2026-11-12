import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path="docs/NewsScope_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean Light Theme Palette
    BG_OFFWHITE = RGBColor(248, 250, 252)     # #f8fafc
    CARD_BG = RGBColor(255, 255, 255)         # #ffffff
    BORDER_GRAY = RGBColor(226, 232, 240)     # #e2e8f0
    
    # Text
    TITLE_COLOR = RGBColor(15, 23, 42)        # #0f172a
    BODY_COLOR = RGBColor(51, 65, 85)         # #334155
    MUTED_COLOR = RGBColor(100, 116, 139)     # #64748b

    # Accents
    INDIGO = RGBColor(79, 70, 229)            # #4f46e5
    INDIGO_BG = RGBColor(238, 242, 255)       # #eef2ff
    EMERALD = RGBColor(5, 150, 105)           # #059669
    EMERALD_BG = RGBColor(236, 253, 245)      # #ecfdf5
    AMBER = RGBColor(217, 119, 6)             # #d97706
    AMBER_BG = RGBColor(254, 243, 199)        # #fef3c7

    def set_bg(slide):
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = BG_OFFWHITE

    def add_notes(slide, explanation, example):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = f"SIMPLE EXPLANATION:\n{explanation}\n\nREAL-WORLD ANALOGY:\n{example}"

    def add_header(slide, slide_num, title_text):
        # Slide Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.2), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = INDIGO_BG
        badge.line.color.rgb = RGBColor(199, 210, 254)
        badge.line.width = Pt(1)
        p = badge.text_frame.paragraphs[0]
        p.text = f"SLIDE {slide_num:02d} / 13"
        p.font.name = "Segoe UI"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = INDIGO
        p.alignment = PP_ALIGN.CENTER

        # Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
        tf = tb.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TITLE_COLOR

    def add_dual_callouts(slide, explanation, example):
        # Left Callout: Simple Explanation
        c_left = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.1), Inches(5.7), Inches(1.85))
        c_left.fill.solid()
        c_left.fill.fore_color.rgb = INDIGO_BG
        c_left.line.color.rgb = RGBColor(199, 210, 254)
        c_left.line.width = Pt(1)

        tb_l = slide.shapes.add_textbox(Inches(1.0), Inches(5.18), Inches(5.3), Inches(1.68))
        tf_l = tb_l.text_frame
        tf_l.word_wrap = True
        p_l1 = tf_l.paragraphs[0]
        p_l1.text = "💡 Simple Explanation"
        p_l1.font.name = "Segoe UI"
        p_l1.font.size = Pt(12)
        p_l1.font.bold = True
        p_l1.font.color.rgb = INDIGO
        p_l1.space_after = Pt(3)

        p_l2 = tf_l.add_paragraph()
        p_l2.text = explanation
        p_l2.font.name = "Segoe UI"
        p_l2.font.size = Pt(10.5)
        p_l2.font.color.rgb = BODY_COLOR

        # Right Callout: Real-World Example
        c_right = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(5.1), Inches(5.7), Inches(1.85))
        c_right.fill.solid()
        c_right.fill.fore_color.rgb = EMERALD_BG
        c_right.line.color.rgb = RGBColor(167, 243, 208)
        c_right.line.width = Pt(1)

        tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(5.18), Inches(5.3), Inches(1.68))
        tf_r = tb_r.text_frame
        tf_r.word_wrap = True
        p_r1 = tf_r.paragraphs[0]
        p_r1.text = "🌍 Real-World Analogy"
        p_r1.font.name = "Segoe UI"
        p_r1.font.size = Pt(12)
        p_r1.font.bold = True
        p_r1.font.color.rgb = EMERALD
        p_r1.space_after = Pt(3)

        p_r2 = tf_r.add_paragraph()
        p_r2.text = example
        p_r2.font.name = "Segoe UI"
        p_r2.font.size = Pt(10.5)
        p_r2.font.color.rgb = BODY_COLOR

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Hero Card
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(4.0))
    hero.fill.solid()
    hero.fill.fore_color.rgb = CARD_BG
    hero.line.color.rgb = BORDER_GRAY

    # Top accent line
    strip = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.08))
    strip.fill.solid()
    strip.fill.fore_color.rgb = INDIGO
    strip.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.15), Inches(10.9), Inches(3.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "FINAL YEAR PROJECT DEFENSE • MCA"
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INDIGO
    p.space_after = Pt(10)

    p_t = tf.add_paragraph()
    p_t.text = "NewsScope: News Article Category Classifier"
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = TITLE_COLOR
    p_t.space_after = Pt(14)

    p_n = tf.add_paragraph()
    p_n.text = "Name: Abhijeet Kumar (MCA)"
    p_n.font.name = "Segoe UI"
    p_n.font.size = Pt(18)
    p_n.font.bold = True
    p_n.font.color.rgb = EMERALD
    p_n.space_after = Pt(10)

    p_s = tf.add_paragraph()
    p_s.text = "Tech Stack: Next.js 14  •  FastAPI  •  Scikit-Learn  •  PyTorch"
    p_s.font.name = "Segoe UI"
    p_s.font.size = Pt(13)
    p_s.font.color.rgb = MUTED_COLOR

    expl_1 = "This is the cover page. It tells the examiner what the project is called, who built it, and what technologies were used."
    exam_1 = "Think of this like the cover of a movie poster. It gives the title, the director (you), and the main actors (your tech stack)."
    add_dual_callouts(s1, expl_1, exam_1)
    add_notes(s1, expl_1, exam_1)

    # =========================================================================
    # SLIDE 2: THE PROBLEM
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, 2, "The Problem: News Overload & Black-Box AI")

    # Content Card
    c = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(3.35))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = BORDER_GRAY

    tb = s2.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(2.9))
    tf = tb.text_frame
    tf.word_wrap = True

    pts_2 = [
        ("Massive Content Volume", "Millions of news articles are published daily across news portals and feeds."),
        ("Manual Tagging is Impossible", "Human editors cannot read, tag, and organize thousands of stories by hand fast enough."),
        ("Black-Box AI Models", "Standard AI models are black boxes: they output a label without explaining why they chose it.")
    ]
    for i, (head, body) in enumerate(pts_2):
        p1 = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p1.text = f"•  {head}:  {body}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(14)
        p1.font.color.rgb = BODY_COLOR
        p1.space_after = Pt(16)

    expl_2 = "There is too much news to sort by hand. We use AI, but normal AI just gives an answer without explaining how it got it."
    exam_2 = "Imagine a librarian who gets 10,000 books a day. They can't read and sort them all. If they use a robot to help, the robot just puts the book on a shelf and says, 'Trust me, it belongs here,' without explaining why."
    add_dual_callouts(s2, expl_2, exam_2)
    add_notes(s2, expl_2, exam_2)

    # =========================================================================
    # SLIDE 3: PROJECT OBJECTIVES
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, 3, "Project Objectives")

    c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(3.35))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = BORDER_GRAY

    tb = s3.shapes.add_textbox(Inches(1.2), Inches(1.75), Inches(10.9), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True

    pts_3 = [
        ("1. Zero Data Leakage", "Strict separation between training and test sets so the AI never cheats during testing."),
        ("2. Compare 4 Different AI Models", "Benchmark 4 distinct algorithms head-to-head on the exact same data."),
        ("3. Explainable AI", "Show the exact top keywords and weights that caused the AI to pick a category."),
        ("4. Build a Complete Web App", "Wrap the models into a real, responsive website with live inference and CSV uploading.")
    ]
    for i, (head, body) in enumerate(pts_3):
        p1 = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p1.text = f"✔  {head}:  {body}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13.5)
        p1.font.color.rgb = BODY_COLOR
        p1.space_after = Pt(12)

    expl_3 = "Our goals were to train the AI fairly, test different algorithms, make sure the AI shows its work, and wrap it all in a nice website."
    exam_3 = "Like building a new car. You want it to be safe (no cheating), test different engines (4 models), make sure the dashboard shows the speed (explainable), and actually put it on the road for people to drive (web app)."
    add_dual_callouts(s3, expl_3, exam_3)
    add_notes(s3, expl_3, exam_3)

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, 4, "System Architecture")

    # 3 Horizontal Cards
    arch_tiers = [
        ("Frontend: Next.js 14", "What the user sees. Modern, responsive React UI that takes user text and displays live charts without lag.", INDIGO),
        ("Backend: FastAPI", "The brain. High-speed Python REST API that runs validation and handles requests in under 1 millisecond.", EMERALD),
        ("ML Engine: Scikit-Learn & PyTorch", "The recipes. Pre-trained machine learning models ready to classify text and extract keyword weights instantly.", AMBER)
    ]
    for i, (title, desc, color) in enumerate(arch_tiers):
        left = Inches(0.8 + i * 3.98)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.55), Inches(3.77), Inches(3.35))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_GRAY

        # Top Accent Strip
        top_bar = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.55), Inches(3.77), Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = color
        top_bar.line.fill.background()

        tb = s4.shapes.add_textbox(left + Inches(0.25), Inches(1.85), Inches(3.27), Inches(2.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = TITLE_COLOR
        p1.space_after = Pt(10)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(11)
        p2.font.color.rgb = BODY_COLOR

    expl_4 = "We split the app into two parts. The frontend takes the user's text and sends it to the backend. The backend runs the math and sends the answer back."
    exam_4 = "Think of a restaurant. The Frontend is the waiter taking your order. The Backend is the kitchen cooking the food. The ML Model is the recipe they follow."
    add_dual_callouts(s4, expl_4, exam_4)
    add_notes(s4, expl_4, exam_4)

    # =========================================================================
    # SLIDE 5: NLP PREPROCESSING PIPELINE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, 5, "NLP Preprocessing Pipeline (5 Steps)")

    pipeline_steps = [
        ("1. Clean", "Converts text to lowercase and removes punctuation and web links.", "apples new iphone 999"),
        ("2. Tokenize", "Splits the continuous sentence into individual words.", "['apples', 'new', 'iphone', '999']"),
        ("3. Stopwords", "Removes 179 common filler words like 'the', 'is', 'at', and 'and'.", "['apples', 'iphone', '999']"),
        ("4. Lemmatize", "Turns words back to root dictionary words (running -> run).", "['apple', 'iphone', '999']"),
        ("5. Vectorize", "Turns words into importance numbers (TF-IDF vector).", "[0.42, 0.61, 0.28, ...]")
    ]

    for i, (step, desc, ex) in enumerate(pipeline_steps):
        left = Inches(0.8 + i * 2.38)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.55), Inches(2.25), Inches(3.35))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_GRAY

        tb = s5.shapes.add_textbox(left + Inches(0.15), Inches(1.7), Inches(1.95), Inches(3.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = step
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = INDIGO
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = BODY_COLOR
        p2.space_after = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = "Example:"
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(9)
        p3.font.bold = True
        p3.font.color.rgb = MUTED_COLOR

        p4 = tf.add_paragraph()
        p4.text = ex
        p4.font.name = "Consolas"
        p4.font.size = Pt(8.5)
        p4.font.color.rgb = TITLE_COLOR

    expl_5 = "Computers can't read English. We have to clean the text, chop it into words, remove useless filler words, and turn the words into numbers."
    exam_5 = "Like preparing vegetables to cook. You wash them (clean), chop them (tokenize), throw away the stems (stopwords), and measure them (vectorize) before putting them in the pan."
    add_dual_callouts(s5, expl_5, exam_5)
    add_notes(s5, expl_5, exam_5)

    # =========================================================================
    # SLIDE 6: THE 4 AI MODELS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, 6, "The 4 AI Models Tested")

    models_data = [
        ("1. Naive Bayes", "Simple Guesser", "Uses basic probability. Multiplies chances of each word belonging to a topic. Fast (0.5 ms).", INDIGO),
        ("2. Linear SVM", "Finds Boundaries (Champion)", "Draws a straight dividing line in 10,000-word space. 96.4% accurate and super fast (1.2 ms).", EMERALD),
        ("3. Neural MLP", "Mini Brain", "Artificial neural network with 128 neurons. Learns non-linear word patterns (95.1% acc).", AMBER),
        ("4. DistilBERT", "Supercomputer", "Deep learning transformer (66M weights). Reads sentences bidirectionally to understand context.", RGBColor(2, 132, 199))
    ]

    for i, (name, role, desc, color) in enumerate(models_data):
        left = Inches(0.8 + (i % 2) * 5.95)
        top = Inches(1.55 + (i // 2) * 1.7)

        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(1.55))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_GRAY

        bar = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(0.12), Inches(1.55))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb = s6.shapes.add_textbox(left + Inches(0.25), top + Inches(0.12), Inches(5.2), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"{name}  —  {role}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = TITLE_COLOR
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = BODY_COLOR

    expl_6 = "We tested four different ways for the AI to learn."
    exam_6 = "Imagine four students taking a test:\n• Naive Bayes just guesses based on what it remembers.\n• SVM draws a straight line in the sand to separate answers.\n• MLP uses a complex brain to figure it out.\n• BERT reads the entire textbook and remembers every detail."
    add_dual_callouts(s6, expl_6, exam_6)
    add_notes(s6, expl_6, exam_6)

    # =========================================================================
    # SLIDE 7: DATASET & EVALUATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, 7, "Dataset & Evaluation")

    c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(3.35))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = BORDER_GRAY

    tb = s7.shapes.add_textbox(Inches(1.2), Inches(1.75), Inches(10.9), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True

    pts_7 = [
        ("BBC News Corpus", "2,225 genuine news articles from 2004–2005 (compiled by Greene & Cunningham)."),
        ("5 Balanced Categories", "Sport (511), Business (510), Politics (417), Tech (401), Entertainment (386)."),
        ("80 / 20 Train-Test Split", "80% (1,780 articles) for training the models; 20% (445 articles) held out for testing."),
        ("Zero Data Leakage Guarantee", "The test articles were kept 100% unseen until final grading to ensure honest metrics.")
    ]
    for i, (head, body) in enumerate(pts_7):
        p1 = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p1.text = f"•  {head}:  {body}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13.5)
        p1.font.color.rgb = BODY_COLOR
        p1.space_after = Pt(12)

    expl_7 = "We used a real dataset of 2,225 BBC articles. We taught the AI using 80% of them, and saved 20% to test if it actually learned."
    exam_7 = "Like a teacher giving you practice questions (80%) to study, and then giving you a final exam (20%) with new questions to see if you really understand the topic."
    add_dual_callouts(s7, expl_7, exam_7)
    add_notes(s7, expl_7, exam_7)

    # =========================================================================
    # SLIDE 8: THE LEADERBOARD (RESULTS)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, 8, "The Leaderboard (Results on 445 Test Articles)")

    # Leaderboard Table
    t_shape = s8.shapes.add_table(5, 4, Inches(0.8), Inches(1.55), Inches(11.7), Inches(3.35))
    table = t_shape.table

    l_headers = ["Model", "Accuracy", "Speed (Latency)", "Role / Verdict"]
    l_rows = [
        ["DistilBERT", "97.8%", "12.4 ms", "Most accurate, but slowest & heavy (260 MB)"],
        ["Linear SVM ⭐", "96.4%", "1.2 ms", "Production Champion! 10x faster & lightweight (<15 MB)"],
        ["Neural MLP", "95.1%", "3.2 ms", "Balanced neural network approach"],
        ["Naive Bayes", "92.1%", "0.5 ms", "Fastest baseline, but lower accuracy"]
    ]

    for j, h in enumerate(l_headers):
        cell = table.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = INDIGO
        for p in cell.text_frame.paragraphs:
            p.font.name = "Segoe UI"
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(l_rows):
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
                p.font.color.rgb = EMERALD if (i == 1 and j < 2) else TITLE_COLOR

    expl_8 = "BERT was the most accurate, but it was slow. SVM was almost as accurate, but 10 times faster. So we chose SVM for the final app."
    exam_8 = "A sports car (BERT) goes 1 mile per hour faster than a bullet train (SVM). But the train carries everyone in half the time. For a web app, speed matters, so we chose the train."
    add_dual_callouts(s8, expl_8, exam_8)
    add_notes(s8, expl_8, exam_8)

    # =========================================================================
    # SLIDE 9: ERROR ANALYSIS (CONFUSION MATRIX)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, 9, "Error Analysis (Confusion Matrix)")

    c = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(3.35))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = BORDER_GRAY

    tb = s9.shapes.add_textbox(Inches(1.2), Inches(1.75), Inches(10.9), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True

    pts_9 = [
        ("Best Categories", "Sport (99.0% - 101/102 correct) and Entertainment (96.1% - 74/77 correct)."),
        ("Hardest Boundary", "Politics vs. Business (4 articles confused due to shared words like 'tax', 'budget', 'economy')."),
        ("The Solution (Bigrams)", "We trained the AI on two-word phrases (like 'corporate tax' vs 'tax policy') to tell them apart."),
        ("Total Errors", "Only 16 articles out of 445 were misclassified across the entire test set.")
    ]
    for i, (head, body) in enumerate(pts_9):
        p1 = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p1.text = f"•  {head}:  {body}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13.5)
        p1.font.color.rgb = BODY_COLOR
        p1.space_after = Pt(12)

    expl_9 = "The AI was great at sports. But it got confused between Politics and Business because they use similar words. We fixed this by teaching it phrases instead of just single words."
    exam_9 = "If an article says 'The Chancellor announced the new tax budget.' Is it Politics or Business? Even a human gets confused. By looking at the phrase 'tax budget' together, the AI understands it better."
    add_dual_callouts(s9, expl_9, exam_9)
    add_notes(s9, expl_9, exam_9)

    # =========================================================================
    # SLIDE 10: EXPLAINABLE AI
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, 10, "Explainable AI (No More Black Boxes)")

    c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(3.35))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = BORDER_GRAY

    tb = s10.shapes.add_textbox(Inches(1.2), Inches(1.75), Inches(10.9), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True

    pts_10 = [
        ("Top Keywords Saliency", "Shows the exact words that caused the prediction (e.g. 'wembley' = 28%, 'processor' = 35%)."),
        ("Platt Scaling (Confidence Scores)", "Converts raw mathematical margin distances into honest percentage probabilities (e.g. 98.4%)."),
        ("'Low Confidence' Warnings", "If the highest category probability is under 45%, the system warns the editor that the article is ambiguous.")
    ]
    for i, (head, body) in enumerate(pts_10):
        p1 = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p1.text = f"✔  {head}:  {body}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(14)
        p1.font.color.rgb = BODY_COLOR
        p1.space_after = Pt(16)

    expl_10 = "The AI doesn't just give an answer; it shows exactly which words it used to make the decision. If it's confused, it warns the user."
    exam_10 = "A doctor shouldn't just say, 'You are sick.' They should say, 'You are sick because your temperature is 102.' Our AI acts like the good doctor—it shows its evidence."
    add_dual_callouts(s10, expl_10, exam_10)
    add_notes(s10, expl_10, exam_10)

    # =========================================================================
    # SLIDE 11: APPLICATION FEATURES
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, 11, "Application Features (Live Web Platform)")

    features = [
        ("Single Text Classifier", "Paste any news article or enter a URL. Instant classification in under 1 second with keyword badges."),
        ("Batch CSV Processing", "Drag and drop a CSV file with 1,000+ articles. Live progress bar and one-click export with predictions."),
        ("Compare 4 Models Live", "Consensus modal runs SVM, DistilBERT, MLP, and Naive Bayes simultaneously on the input text."),
        ("Analytics Dashboard", "Interactive bar charts (per-domain accuracy) and live Confusion Matrix heatmap.")
    ]
    for i, (title, desc) in enumerate(features):
        left = Inches(0.8 + (i % 2) * 5.95)
        top = Inches(1.55 + (i // 2) * 1.7)

        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.65), Inches(1.55))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_GRAY

        bar = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(0.12), Inches(1.55))
        bar.fill.solid()
        bar.fill.fore_color.rgb = INDIGO
        bar.line.fill.background()

        tb = s11.shapes.add_textbox(left + Inches(0.25), top + Inches(0.12), Inches(5.2), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = TITLE_COLOR
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = BODY_COLOR

    expl_11 = "This is what the user can actually do on the website."
    exam_11 = "It's like a Swiss Army Knife. You can classify one article, classify 1,000 articles at once (CSV), compare all 4 AIs, and look at charts."
    add_dual_callouts(s11, expl_11, exam_11)
    add_notes(s11, expl_11, exam_11)

    # =========================================================================
    # SLIDE 12: LIMITATIONS & FUTURE SCOPE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_header(s12, 12, "Limitations & Future Scope")

    c = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(3.35))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = BORDER_GRAY

    tb = s12.shapes.add_textbox(Inches(1.2), Inches(1.75), Inches(10.9), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True

    pts_12 = [
        ("Current Limitations", "Historical BBC dataset (2005) lacks modern words like 'cryptocurrency' or 'LLMs'; English-only; single-label only."),
        ("Future Roadmap", "Multi-label classification (articles spanning multiple topics), multilingual models (XLM-RoBERTa), and active learning loops.")
    ]
    for i, (head, body) in enumerate(pts_12):
        p1 = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p1.text = f"•  {head}:  {body}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13.5)
        p1.font.color.rgb = BODY_COLOR
        p1.space_after = Pt(14)

    expl_12 = "What the app can't do today, and how we can make it better tomorrow."
    exam_12 = "Right now, our car only drives on old roads (2005 data) and only carries one passenger (single label). In the future, we want a flying car that can go anywhere in the world (multilingual)."
    add_dual_callouts(s12, expl_12, exam_12)
    add_notes(s12, expl_12, exam_12)

    # =========================================================================
    # SLIDE 13: CONCLUSION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13)
    add_header(s13, 13, "Conclusion & Key Takeaways")

    c = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(3.35))
    c.fill.solid()
    c.fill.fore_color.rgb = CARD_BG
    c.line.color.rgb = BORDER_GRAY

    tb = s13.shapes.add_textbox(Inches(1.2), Inches(1.85), Inches(10.9), Inches(2.9))
    tf = tb.text_frame
    tf.word_wrap = True

    pts_13 = [
        ("Classical ML (SVM) Matches Deep Learning", "Linear SVM achieved 96.4% accuracy (within 1.4% of DistilBERT) while running 10x faster (1.2 ms vs 12.4 ms)."),
        ("Complete Full-Stack Delivery", "Delivered a production-ready, beautiful web application with Next.js 14 and FastAPI.")
    ]
    for i, (head, body) in enumerate(pts_13):
        p1 = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p1.text = f"✔  {head}:  {body}"
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(14)
        p1.font.color.rgb = BODY_COLOR
        p1.space_after = Pt(18)

    expl_13 = "To wrap up, we proved that you don't always need massive, expensive AI to do a great job. We built a fast, accurate, and beautiful app."
    exam_13 = "We didn't need a supercomputer to build a great tool. Just a smart, well-tuned engine."
    add_dual_callouts(s13, expl_13, exam_13)
    add_notes(s13, expl_13, exam_13)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        prs.save(output_path)
        print(f"Presentation saved successfully to {output_path}")
    except PermissionError:
        alt_path = output_path.replace(".pptx", "_13Slides.pptx")
        prs.save(alt_path)
        print(f"Notice: {output_path} is currently open in PowerPoint. Saved to {alt_path}")

if __name__ == "__main__":
    build_presentation()
