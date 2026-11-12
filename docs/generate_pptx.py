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
    BG_COLOR = RGBColor(248, 249, 250)      # Light gray background
    NAVY = RGBColor(15, 23, 42)             # Deep Navy
    INDIGO = RGBColor(79, 70, 229)          # Indigo Primary
    EMERALD = RGBColor(5, 150, 105)         # Green Accent
    TEXT_MUTED = RGBColor(100, 116, 139)    # Muted Slate Gray
    CARD_BG = RGBColor(255, 255, 255)       # White Card
    BORDER_COLOR = RGBColor(226, 232, 240)  # Border Gray

    def set_slide_background(slide, color=BG_COLOR):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, category_tag, title_text):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_tag.upper()
        p_tag.font.name = "Calibri"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = INDIGO

        # Title Text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.75))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Calibri"
        p_title.font.size = Pt(25)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Navy Hero)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, NAVY)

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p_badge = tf.paragraphs[0]
    p_badge.text = "FINAL YEAR PROJECT DEFENSE • MACHINE LEARNING & NLP"
    p_badge.font.name = "Calibri"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(129, 140, 248)
    p_badge.space_after = Pt(14)

    p_main = tf.add_paragraph()
    p_main.text = "NewsScope: Smart News Article Classifier"
    p_main.font.name = "Calibri"
    p_main.font.size = Pt(40)
    p_main.font.bold = True
    p_main.font.color.rgb = RGBColor(255, 255, 255)
    p_main.space_after = Pt(16)

    p_sub = tf.add_paragraph()
    p_sub.text = "A Fast, Explainable Machine Learning System Benchmarking 4 AI Models"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_after = Pt(32)

    p_meta = tf.add_paragraph()
    p_meta.text = "Presenter: Abhijeet  |  Dataset: BBC News (5 Categories)  |  Stack: FastAPI + Next.js 14 + Scikit-Learn"
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
        ("01", "Why News Classification?", "The problem of manual news sorting and the black-box AI issue."),
        ("02", "Project Objectives", "Zero data leakage, comparing 4 models, and explaining predictions."),
        ("03", "System Architecture", "How the Next.js frontend and FastAPI backend work together."),
        ("04", "5-Step Text Pipeline", "How we clean raw text and turn it into numerical features."),
        ("05", "The 4 AI Models", "Plain English explanation of Naive Bayes, Linear SVM, MLP, & DistilBERT."),
        ("06", "Corpus & Results", "Benchmark numbers on 445 unseen test articles (Champion: 96.4%)."),
        ("07", "Real-Time Demonstration", "Step-by-step walkthrough of a real news article in action."),
        ("08", "Future Scope & Viva Q&A", "System limitations, planned roadmap, and common defense questions.")
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
    add_header(s3, "Background & Motivation", "Why Automated News Classification Matters")

    # Left Box: Problem
    left_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.1))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = BORDER_COLOR

    ltb = s3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.7))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "The Real-World Problem"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(14)

    bullets_l = [
        "Massive Content Volume: Over 500 million news articles are posted online every day.",
        "Manual Sorting is Slow: Editors cannot read and tag every story by hand.",
        "Strict Speed Requirements: News apps and portals require classification in under 20 milliseconds.",
        "High Inconsistency: Different human readers often tag the same news article under different topics."
    ]
    for b in bullets_l:
        p = ltf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    # Right Box: The Gap & NewsScope Solution
    right_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = CARD_BG
    right_card.line.color.rgb = BORDER_COLOR

    rtb = s3.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.7))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "The 'Black-Box' Problem & Our Fix"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = INDIGO
    p.space_after = Pt(14)

    bullets_r = [
        "Black-Box Predictions: Most AI tools output a label without explaining why they chose it.",
        "Trust & Verification: Editors need to see which keywords triggered the decision.",
        "Data Leakage Risk: Many student projects clean text across train and test sets together, giving fake high scores.",
        "The NewsScope Solution: A zero-leakage, transparent system that tells you the category in 1.2 ms and highlights the key words."
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
    add_header(s4, "Project Goals", "What We Set Out to Build")

    pillars = [
        ("1. Zero Data Leakage", "Strict separation between training and testing data. The text cleaner only learns words from training articles; test data remains 100% unseen."),
        ("2. Compare 4 Different AI Models", "Benchmark 4 different approaches: Naive Bayes (probability), Linear SVM (geometry), Neural MLP (neural network), and DistilBERT (transformer)."),
        ("3. Explain Every Prediction", "No mystery results. The system reveals the exact keywords and mathematical weights that drove the model's decision."),
        ("4. Real Working Web Application", "A complete website with real-time text analysis, side-by-side model comparison, and bulk CSV file processing.")
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
    add_header(s5, "System Design", "How NewsScope Works Behind the Scenes")

    layers = [
        ("1. Frontend User Interface (Next.js 14)", "• Built with Next.js 14 and Tailwind CSS for a modern, responsive interface.\n• Uses Zustand state management so typing into the text box doesn't lag or freeze the page.\n• Displays live charts and confidence bars using Recharts."),
        ("2. Backend API Gateway (FastAPI)", "• High-speed Python API using FastAPI.\n• Validates incoming news text and routes requests in under 1 millisecond.\n• Exposes REST endpoints: POST /api/classify and GET /api/dataset."),
        ("3. Machine Learning Engine (Scikit-Learn & PyTorch)", "• Loads pre-trained models instantly from disk.\n• Linear SVM (Production Champion) with calibrated confidence percentages.\n• Also runs Naive Bayes, Neural MLP, and DistilBERT for live comparison.")
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
    add_header(s6, "Data Processing", "5 Steps to Clean and Prepare News Text")

    stages = [
        ("Step 1: Lowercase & Clean", "Converts all letters to lowercase and removes punctuation and web links.", "Example: 'Apple's NEW iPhone @ $999!' -> 'apples new iphone 999'"),
        ("Step 2: Split Words (Tokenize)", "Cuts the sentence into individual words.", "Example: ['apples', 'new', 'iphone', '999']"),
        ("Step 3: Remove Stopwords", "Filters out 179 useless common words like 'the', 'is', 'at', and 'and'.", "Example: ['apples', 'iphone', '999']"),
        ("Step 4: Lemmatization", "Converts words back to their base dictionary form (e.g. 'apples' -> 'apple').", "Example: ['apple', 'iphone', '999']"),
        ("Step 5: TF-IDF Vectorization", "Turns words into importance numbers (unigrams + bigrams, top 10,000 words).", "Example: [0.42, 0.61, 0.28, ...] (numbers ready for the ML model)")
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
        p2.text = example
        p2.font.name = "Consolas"
        p2.font.size = Pt(11)
        p2.font.color.rgb = INDIGO

    # ==========================================
    # SLIDE 7: MATHEMATICAL FOUNDATIONS (SIMPLE)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Model Concepts", "How the 4 AI Models Make Decisions (In Plain English)")

    math_models = [
        ("1. TF-IDF Word Weighting", "TF-IDF = Term Frequency * Inverse Document Frequency", "Plain English: If a word appears often in one article but rarely across all news, it gets a high score (like 'quarterback' or 'inflation')."),
        ("2. Multinomial Naive Bayes", "Probability: P(Category | Words) based on Bayes Rule", "Plain English: Multiplies the chances of each word belonging to a category. It assumes words are independent. Very simple and super fast (0.5 ms)."),
        ("3. Linear SVM (Our Champion)", "Finds the widest boundary line: Margin = 2 / ||w||", "Plain English: Places articles as points in a 10,000-word space and draws the cleanest dividing line between topics. Highly accurate for text."),
        ("4. DistilBERT Transformer", "Self-Attention Mechanism: Attention(Q, K, V)", "Plain English: Reads the whole sentence in both directions. It understands how words relate to each other in context (e.g. 'Apple' company vs fruit).")
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
        p2.font.size = Pt(11)
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
    add_header(s8, "Dataset Overview", "BBC News Dataset (2,225 Real Articles)")

    # Table on Left
    table_shape = s8.shapes.add_table(6, 3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    table = table_shape.table

    headers = ["News Category", "Article Count", "Percentage"]
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
    p.text = "Dataset Details"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    bullets = [
        "Benchmark Source: Standard BBC News benchmark corpus (Greene & Cunningham, 2006).",
        "Total Articles: 2,225 genuine news stories across 5 popular topics.",
        "80 / 20 Train-Test Split: 1,780 articles for training and 445 articles held out for testing.",
        "Balanced Classes: Each topic has 380 to 510 articles, meaning the dataset is well-balanced.",
        "Average Length: ~2,200 characters (~380 words) per article.",
        "Zero Leakage: Test articles were kept completely hidden while building the word dictionary."
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
    add_header(s9, "Benchmark Results", "Which AI Model Performed Best?")

    table_shape = s9.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.2))
    table = table_shape.table

    m_headers = ["Model Name", "How It Works", "Test Accuracy", "Macro F1 Score", "Speed (Latency)"]
    m_data = [
        ["DistilBERT", "Transformer Attention (66M weights)", "97.8%", "0.976", "12.4 ms"],
        ["Linear SVM (Winner)", "Maximum-Margin Line", "96.4%", "0.963", "1.2 ms"],
        ["Neural MLP", "Neural Network (128 neurons)", "95.1%", "0.948", "3.2 ms"],
        ["Naive Bayes", "Probability (Bayes Rule)", "92.1%", "0.920", "0.5 ms"]
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
            if i == 1:
                cell.fill.fore_color.rgb = RGBColor(236, 253, 245) # Light green
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
    p.text = "Why Linear SVM is our Production Winner"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = INDIGO

    p2 = btf.add_paragraph()
    p2.text = "• DistilBERT got the highest score (97.8%), but Linear SVM reached 96.4% while running 10x faster (1.2 ms vs 12.4 ms) and taking 20x less memory (< 15 MB vs 260 MB). That makes Linear SVM the best choice for real-world news websites."
    p2.font.name = "Calibri"
    p2.font.size = Pt(12)
    p2.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 10: PER-DOMAIN ACCURACY BREAKDOWN
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Accuracy by Category", "How Accurate Was Linear SVM for Each Topic?")

    domains = [
        ("Sport", "99.0%", "101 / 102 correct", "Specialized sports terms (match, cup, player, coach, score)."),
        ("Tech", "96.3%", "77 / 80 correct", "Distinct technology words (software, broadband, laptop, virus)."),
        ("Entertainment", "96.1%", "74 / 77 correct", "Showbiz terms (film, oscar, music, festival, box office)."),
        ("Business", "96.1%", "98 / 102 correct", "Market terms (shares, economy, profit, bank, inflation)."),
        ("Politics", "94.0%", "79 / 84 correct", "Government terms (minister, election, parliament, tax).")
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
    p.text = "Overall Accuracy: 429 out of 445 correct (96.4%)"
    p.font.name = "Calibri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p2 = btf.add_paragraph()
    p2.text = "• Sport is the easiest to classify (99.0%) because sports words are unique. Politics is slightly harder (94.0%) because politicians often talk about the economy and taxes, which overlaps with Business."
    p2.font.name = "Calibri"
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(51, 65, 85)

    # ==========================================
    # SLIDE 11: ERROR ANALYSIS & CONFUSION MATRIX
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Error Diagnostics", "Where Did the Model Make Mistakes?")

    # Left: Confusion Matrix Table
    cm_shape = s11.shapes.add_table(6, 6, Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.8))
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
            elif (i + 1) == j: # Correct diagonal
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
    p.text = "Key Observations"
    p.font.name = "Calibri"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(12)

    diag_bullets = [
        "Only 16 Errors: Out of 445 unseen articles, only 16 were misclassified.",
        "Politics vs Business: 4 articles were confused between Politics and Business. Both topics share words like 'budget', 'taxation', and 'economy'.",
        "How We Improved It: We used 2-word combinations (bigrams) like 'corporate tax' vs 'tax bill' to help tell them apart.",
        "Sport was Almost Perfect: 101 out of 102 articles were correctly identified. Only 1 article about Olympic committee elections slipped into Politics."
    ]
    for b in diag_bullets:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 12: MODEL EXPLAINABILITY
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Explainable AI", "How NewsScope Explains Its Decisions")

    methods = [
        ("1. Word Importance Scores", "Linear SVM calculates a math weight for every word. Words with the highest positive weights for a category are shown to the user as key reasons.", "Example: 'processor' (+0.35) and 'macbook' (+0.28) clearly point to Technology."),
        ("2. Calibrated Confidence Percentages", "Instead of giving raw math numbers, Platt Scaling converts distances into clear, honest percentages (like 98.4% confident).", "Example: The system tells editors exactly how confident it is."),
        ("3. Color-Coded Word Highlights", "In our web app, the most important words light up automatically. Users can see at a glance why the AI made its prediction.", "User Experience: Clean visual badges showing top keyword weights.")
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

    # =========================================================
    # SLIDE 13: REAL-TIME DEMONSTRATION (THE CONCRETE EXAMPLE!)
    # =========================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Live Walkthrough", "Real-Time Demonstration: Step-by-Step Example")

    # Left: Input & Pipeline Steps
    left_card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.8), Inches(5.1))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = BORDER_COLOR

    ltb = s13.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(5.4), Inches(4.8))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "1. Input Text & Pipeline Transformation"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = INDIGO
    p.space_after = Pt(8)

    p_in_lbl = ltf.add_paragraph()
    p_in_lbl.text = "Article Typed into Classifier:"
    p_in_lbl.font.name = "Calibri"
    p_in_lbl.font.size = Pt(12)
    p_in_lbl.font.bold = True
    p_in_lbl.font.color.rgb = NAVY

    p_in = ltf.add_paragraph()
    p_in.text = "\"Apple unveils new M3 MacBook laptop with ultra-fast processor, 22-hour battery life, and AI neural engine features for developers.\""
    p_in.font.name = "Consolas"
    p_in.font.size = Pt(11)
    p_in.font.color.rgb = RGBColor(30, 41, 59)
    p_in.space_after = Pt(10)

    pipeline_steps = [
        "1. Cleansed: 'apple unveils new m3 macbook laptop ultrafast processor 22hour battery life ai neural engine features developers'",
        "2. Stopwords Dropped: removed 'with', 'and', 'for'",
        "3. Lemmatized: 'features' -> 'feature', 'unveils' -> 'unveil'",
        "4. Converted to 10,000-D TF-IDF numerical vector"
    ]
    for step in pipeline_steps:
        p = ltf.add_paragraph()
        p.text = "• " + step
        p.font.name = "Calibri"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(71, 85, 105)
        p.space_after = Pt(4)

    # Right: Output, Confidence, Keywords, Consensus
    right_card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.1))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = CARD_BG
    right_card.line.color.rgb = BORDER_COLOR

    rtb = s13.shapes.add_textbox(Inches(7.1), Inches(1.95), Inches(5.2), Inches(4.8))
    rtf = rtb.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "2. Prediction & Model Consensus"
    p.font.name = "Calibri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p.space_after = Pt(8)

    p_res = rtf.add_paragraph()
    p_res.text = "Predicted Category: TECHNOLOGY (98.4%)"
    p_res.font.name = "Calibri"
    p_res.font.size = Pt(15)
    p_res.font.bold = True
    p_res.font.color.rgb = NAVY
    p_res.space_after = Pt(8)

    p_kw = rtf.add_paragraph()
    p_kw.text = "Top Explanatory Keywords:"
    p_kw.font.name = "Calibri"
    p_kw.font.size = Pt(12)
    p_kw.font.bold = True
    p_kw.font.color.rgb = INDIGO

    keywords = [
        "processor (+0.35)", "apple (+0.28)", "laptop (+0.24)", "developer (+0.18)"
    ]
    p_chips = rtf.add_paragraph()
    p_chips.text = "  |  ".join(keywords)
    p_chips.font.name = "Consolas"
    p_chips.font.size = Pt(11)
    p_chips.font.color.rgb = RGBColor(15, 23, 42)
    p_chips.space_after = Pt(12)

    p_con_lbl = rtf.add_paragraph()
    p_con_lbl.text = "4-Model Consensus Modal:"
    p_con_lbl.font.name = "Calibri"
    p_con_lbl.font.size = Pt(12)
    p_con_lbl.font.bold = True
    p_con_lbl.font.color.rgb = NAVY

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
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(3)

    p_verdict = rtf.add_paragraph()
    p_verdict.text = "Result: 100% agreement across all 4 architectures!"
    p_verdict.font.name = "Calibri"
    p_verdict.font.size = Pt(12)
    p_verdict.font.bold = True
    p_verdict.font.color.rgb = EMERALD

    # ==========================================
    # SLIDE 14: WEB APPLICATION FEATURES
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Web Application", "NewsScope Web Platform Features")

    features = [
        ("1. Instant Single Classifier", "• Type or paste any news text and get instant results in under 1 second.\n• Shows predicted category, confidence percentage, and word count.\n• Optimistic UI: instant response with no typing lag."),
        ("2. 4-Model Comparison Modal", "• Click 'Compare All Models' to test all 4 models simultaneously.\n• Shows execution time, confidence, and agreement side-by-side.\n• Proves that Linear SVM gives transformer accuracy in 1/10th the time."),
        ("3. Bulk CSV Batch Processing", "• Drag and drop a CSV file with hundreds of news articles.\n• Live progress bar shows processing speed.\n• Export the categorized results back to CSV with one click."),
        ("4. Live Analytics Dashboard", "• Interactive bar chart showing accuracy for all 5 domains.\n• Visual confusion matrix heatmap showing where errors occur.\n• Complete metrics: Accuracy, Precision, Recall, and Macro F1.")
    ]

    for idx, (title, desc) in enumerate(features):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.8 + (idx // 2) * 2.6)

        c = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.35))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s14.shapes.add_textbox(left + Inches(0.3), top + Inches(0.2), Inches(5.0), Inches(1.9))
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
    # SLIDE 15: LIMITATIONS & FUTURE SCOPE
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Evaluation & Scope", "Current Limitations & Future Roadmap")

    # Left: Limitations
    lc = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    lc.fill.solid()
    lc.fill.fore_color.rgb = CARD_BG
    lc.line.color.rgb = BORDER_COLOR

    ltb = s15.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.6))
    ltf = ltb.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "Current Limitations"
    p.font.name = "Calibri"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(225, 29, 72)
    p.space_after = Pt(12)

    lims = [
        "Older Dataset: The BBC 2005 dataset lacks modern words like 'cryptocurrency', 'ChatGPT', or 'streaming apps'.",
        "Single-Label Only: The system assigns one category per article, even if a story touches both Tech and Business.",
        "English Language Only: Only cleans and processes English news articles.",
        "Static Training: Models do not automatically retrain when new news trends emerge."
    ]
    for b in lims:
        p = ltf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    # Right: Future Scope
    rc = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    rc.fill.solid()
    rc.fill.fore_color.rgb = CARD_BG
    rc.line.color.rgb = BORDER_COLOR

    rtb = s15.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.6))
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
        "Multi-Label Classification: Allow articles to belong to two topics at once (e.g. 70% Tech, 30% Business).",
        "Multilingual Support: Use multilingual models (like XLM-RoBERTa) to classify news in Hindi, Spanish, and French.",
        "Live RSS Ingestion: Connect directly to live news wires for automatic real-time feed sorting.",
        "Model Quantization: Use 8-bit ONNX runtime so transformers can run at sub-millisecond speeds."
    ]
    for b in roadmap:
        p = rtf.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 65, 85)
        p.space_after = Pt(10)

    # ==========================================
    # SLIDE 16: CONCLUSION
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, NAVY)

    tb = s16.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(5.5))
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
        "High Performance: Linear SVM achieved 96.4% accuracy at 1.2 ms latency, showing simple math beats heavy neural nets in speed.",
        "Zero Data Leakage: We kept test data completely separate during all 5 preprocessing stages.",
        "Explainable Results: Predictions are not black boxes; users see the exact words that influenced the score.",
        "Complete Web Application: Delivered a fully functional, responsive system with live demo and batch CSV processing."
    ]
    for cp in concl_points:
        p = tf.add_paragraph()
        p.text = "✔  " + cp
        p.font.name = "Calibri"
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(12)

    # ==========================================
    # SLIDE 17: VIVA Q&A DEFENSE BACKUP SLIDE
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, "Examiner Questions", "Viva Voce Defense Cheat Sheet (Simple Answers)")

    qa_list = [
        ("Q1: Why use TF-IDF instead of simple word counts?", "Answer: Simple counting lets common words like 'the' or 'said' dominate. TF-IDF lowers the weight of common words and highlights unique topic words like 'striker' or 'inflation'."),
        ("Q2: Why does Linear SVM work so well on text?", "Answer: When text is converted into 10,000 words, it becomes a very wide, sparse space. In high dimensions, categories can easily be separated by a straight dividing line without overfitting."),
        ("Q3: How did you strictly prevent Data Leakage?", "Answer: We built our word dictionary using ONLY the 1,780 training articles. The 445 test articles were kept hidden until evaluation time, just like real-world news."),
        ("Q4: Why choose DistilBERT over standard BERT?", "Answer: DistilBERT is 40% smaller and 60% faster than BERT, while keeping 97% of BERT's accuracy. It is much easier to run on a regular laptop.")
    ]

    for idx, (q, a) in enumerate(qa_list):
        left = Inches(0.8 + (idx % 2) * 5.9)
        top = Inches(1.8 + (idx // 2) * 2.6)

        c = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(2.35))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = BORDER_COLOR

        tb = s17.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.1), Inches(1.9))
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
    try:
        prs.save(output_path)
        print(f"Presentation saved successfully to {output_path}")
    except PermissionError:
        alt_path = output_path.replace(".pptx", "_v2.pptx")
        prs.save(alt_path)
        print(f"Notice: {output_path} is locked (open in PowerPoint). Saved to {alt_path}")

if __name__ == "__main__":
    create_deck()
