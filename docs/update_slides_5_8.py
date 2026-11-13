import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def update_slides():
    prs_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    prs = Presentation(prs_path)
    
    # -------------------------------------------------------------
    # COLOR PALETTE
    # -------------------------------------------------------------
    c_white = RGBColor(255, 255, 255)
    c_navy = RGBColor(15, 23, 42)          # Slate 900 (#0F172A)
    c_slate_dark = RGBColor(51, 65, 85)    # Slate 700 (#334155)
    c_slate_mid = RGBColor(100, 116, 139)  # Slate 500 (#64748B)
    c_slate_light = RGBColor(203, 213, 225)# Slate 300 (#CBD5E1)
    c_slate_sub = RGBColor(226, 232, 240)  # Slate 200 (#E2E8F0)
    c_card_bg = RGBColor(248, 250, 252)    # Slate 50 (#F8FAFC)
    c_border = RGBColor(203, 213, 225)     # Slate 300 (#CBD5E1)
    
    # Accent Colors
    c_indigo = RGBColor(79, 70, 229)       # Indigo 600 (#4F46E5)
    c_indigo_light = RGBColor(238, 242, 255)# Indigo 50 (#EEF2FF)
    c_indigo_bdr = RGBColor(99, 102, 241)  # Indigo 500 (#6366F1)
    c_cyan = RGBColor(56, 189, 248)        # Sky 400 (#38BDF8)
    c_emerald = RGBColor(5, 150, 105)      # Emerald 600 (#059669)
    c_emerald_dark = RGBColor(6, 78, 59)   # Emerald 900 (#064E3B)
    c_emerald_bg = RGBColor(240, 253, 244) # Emerald 50 (#F0FDF4)
    c_amber = RGBColor(217, 119, 6)        # Amber 600 (#D97706)
    
    # Gradient Colors for Slide 7
    c_grad1_bg = RGBColor(240, 249, 255)   # Sky 50 (#F0F9FF)
    c_grad1_bdr = RGBColor(56, 189, 248)   # Sky 400 (#38BDF8)
    c_grad2_bg = RGBColor(224, 242, 254)   # Sky 100 (#E0F2FE)
    c_grad2_bdr = RGBColor(2, 132, 199)    # Sky 600 (#0284C7)
    c_grad3_bg = RGBColor(219, 234, 254)   # Blue 100 (#DBEAFE)
    c_grad3_bdr = RGBColor(37, 99, 235)    # Blue 600 (#2563EB)
    c_grad4_bg = RGBColor(238, 242, 255)   # Indigo 50 (#EEF2FF)
    c_grad4_bdr = RGBColor(79, 70, 229)    # Indigo 600 (#4F46E5)
    
    # -------------------------------------------------------------------------
    # SLIDE 5: The NewsScope Solution (Dashboard: 3 Left Cards + App Screenshot)
    # -------------------------------------------------------------------------
    print("\n[Slide 5] Redesigning to Dashboard layout: 3 Stacked Horizontal Cards + Live App Screenshot...")
    s5 = prs.slides[4]
    
    # Clear previous shapes
    for shp in list(s5.shapes):
        sp = shp._element
        sp.getparent().remove(sp)
        
    # Title Header
    tb_s5 = s5.shapes.add_textbox(Inches(1.20), Inches(0.65), Inches(17.60), Inches(1.30))
    tb_s5.name = "Slide5_Header"
    tf_s5 = tb_s5.text_frame
    tf_s5.word_wrap = True
    
    p5_0 = tf_s5.paragraphs[0]
    p5_0.text = "The NewsScope Solution"
    p5_0.font.name = "Segoe UI"
    p5_0.font.size = Pt(34)
    p5_0.font.bold = True
    p5_0.font.color.rgb = c_white
    p5_0.space_after = Pt(4)
    
    p5_sub = tf_s5.add_paragraph()
    p5_sub.text = "A production-grade NLP classifier delivering transparency, high accuracy, and 1.2 ms inference."
    p5_sub.font.name = "Segoe UI"
    p5_sub.font.size = Pt(18)
    p5_sub.font.color.rgb = c_slate_sub
    
    # Left Side: 3 Horizontal Cards (Squat rectangles)
    s5_card_left = Inches(1.20)
    s5_card_w = Inches(8.50)
    s5_card_h = Inches(2.50)
    s5_tops = [Inches(2.20), Inches(5.05), Inches(7.90)]
    
    cards_data_s5 = [
        {
            "icon": "🔍",
            "badge": "TRANSPARENCY",
            "title": "Explainable AI (Zero Black Boxes)",
            "body": "Saliency keyword weights reveal the exact words driving each decision. Editors see why, not just what."
        },
        {
            "icon": "🎯",
            "badge": "BENCHMARK PERFORMANCE",
            "title": "High Accuracy (96.4%)",
            "body": "Linear SVM achieves near-deep-learning accuracy on the 5 BBC news domains with calibrated probability margins."
        },
        {
            "icon": "⚡",
            "badge": "PRODUCTION SPEED",
            "title": "Ultra-Fast Speed (1.2 ms)",
            "body": "Processes articles in 1.2 milliseconds on standard CPU hardware with zero GPU dependency or latency delay."
        }
    ]
    
    for i, cdata in enumerate(cards_data_s5):
        top_pos = s5_tops[i]
        
        # Card Background
        rect = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s5_card_left, top_pos, s5_card_w, s5_card_h)
        rect.name = f"Slide5_Card_{i+1}"
        rect.fill.solid()
        rect.fill.fore_color.rgb = c_white
        rect.line.color.rgb = c_border
        rect.line.width = Pt(1.5)
        
        # Left Icon Badge (Centered vertically on card left)
        icon_box = s5.shapes.add_textbox(s5_card_left + Inches(0.35), top_pos + Inches(0.40), Inches(1.50), Inches(1.70))
        icon_box.name = f"Slide5_CardIcon_{i+1}"
        itf = icon_box.text_frame
        itf.word_wrap = False
        ip = itf.paragraphs[0]
        ip.alignment = PP_ALIGN.CENTER
        ip.text = cdata["icon"]
        ip.font.size = Pt(44)
        
        # Right Text Area (Centered vertically)
        txt_box = s5.shapes.add_textbox(s5_card_left + Inches(2.00), top_pos + Inches(0.25), s5_card_w - Inches(2.25), s5_card_h - Inches(0.50))
        txt_box.name = f"Slide5_CardText_{i+1}"
        ttf = txt_box.text_frame
        ttf.word_wrap = True
        
        # Badge
        bp = ttf.paragraphs[0]
        bp.alignment = PP_ALIGN.LEFT
        bp.text = cdata["badge"]
        bp.font.name = "Segoe UI"
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = c_indigo
        bp.space_after = Pt(2)
        
        # Title
        tp = ttf.add_paragraph()
        tp.alignment = PP_ALIGN.LEFT
        tp.text = cdata["title"]
        tp.font.name = "Segoe UI"
        tp.font.size = Pt(22)
        tp.font.bold = True
        tp.font.color.rgb = c_navy
        tp.space_after = Pt(4)
        
        # Body
        body_p = ttf.add_paragraph()
        body_p.alignment = PP_ALIGN.LEFT
        body_p.text = cdata["body"]
        body_p.font.name = "Segoe UI"
        body_p.font.size = Pt(17)
        body_p.font.color.rgb = c_slate_dark
        
    # Right Side: Live App Screenshot Dashboard Mockup
    mock_left = Inches(10.10)
    mock_top = Inches(2.20)
    mock_w = Inches(8.70)
    mock_h = Inches(8.20)
    
    mock_bg = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mock_left, mock_top, mock_w, mock_h)
    mock_bg.name = "Slide5_Mockup_Frame"
    mock_bg.fill.solid()
    mock_bg.fill.fore_color.rgb = c_navy
    mock_bg.line.color.rgb = c_indigo_bdr
    mock_bg.line.width = Pt(2.0)
    
    # Mockup Header Bar
    mock_hdr = s5.shapes.add_textbox(mock_left + Inches(0.35), mock_top + Inches(0.18), mock_w - Inches(0.70), Inches(0.55))
    mock_hdr.name = "Slide5_Mockup_Header"
    htf = mock_hdr.text_frame
    htf.word_wrap = False
    hp = htf.paragraphs[0]
    hp.alignment = PP_ALIGN.LEFT
    hp.text = "🔴 🟡 🟢   NewsScope Classifier  •  Live Inference Dashboard"
    hp.font.name = "Consolas"
    hp.font.size = Pt(13)
    hp.font.bold = True
    hp.font.color.rgb = c_white
    
    # App Screenshot Image
    img_left = mock_left + Inches(0.20)
    img_top = mock_top + Inches(0.75)
    img_w = mock_w - Inches(0.40)
    img_h = mock_h - Inches(0.95)
    
    pic5 = s5.shapes.add_picture("docs/slide11_ui_screenshot.png", img_left, img_top, img_w, img_h)
    pic5.name = "Slide5_App_Screenshot"
    print("  Slide 5 rebuilt with horizontal cards on left and live app UI screenshot on right.")

    # -------------------------------------------------------------------------
    # SLIDE 6: How NewsScope is Built (Flowchart: 4 Boxes Connected by Bold Arrows)
    # -------------------------------------------------------------------------
    print("\n[Slide 6] Redesigning to Flowchart layout: 4 centered boxes connected by bold arrows...")
    s6 = prs.slides[5]
    
    # Clear previous shapes
    for shp in list(s6.shapes):
        sp = shp._element
        sp.getparent().remove(sp)
        
    # Title Header
    tb_s6 = s6.shapes.add_textbox(Inches(1.20), Inches(0.70), Inches(17.60), Inches(1.30))
    tb_s6.name = "Slide6_Header"
    tf_s6 = tb_s6.text_frame
    tf_s6.word_wrap = True
    
    p6_0 = tf_s6.paragraphs[0]
    p6_0.alignment = PP_ALIGN.CENTER
    p6_0.text = "How NewsScope is Built (4 Simple Parts)"
    p6_0.font.name = "Segoe UI"
    p6_0.font.size = Pt(34)
    p6_0.font.bold = True
    p6_0.font.color.rgb = c_white
    p6_0.space_after = Pt(4)
    
    p6_sub = tf_s6.add_paragraph()
    p6_sub.alignment = PP_ALIGN.CENTER
    p6_sub.text = "An end-to-end data pipeline from user keystrokes to sub-millisecond classification."
    p6_sub.font.name = "Segoe UI"
    p6_sub.font.size = Pt(18)
    p6_sub.font.color.rgb = c_slate_sub
    
    # 4 Flowchart Boxes (Squat rectangles + Bold connecting arrows)
    box_w = Inches(3.85)
    box_h = Inches(6.80)
    card_top_s6 = Inches(3.20)
    
    boxes_s6 = [
        {
            "left": Inches(1.10),
            "step": "STEP 1  •  SCREEN",
            "icon": "💻",
            "title": "Frontend\n(Next.js 14)",
            "body": "The screen you see.\nA reactive web interface where typing never freezes or lags.",
            "tech": "React 18  •  Tailwind CSS"
        },
        {
            "left": Inches(5.75),
            "step": "STEP 2  •  WAITER",
            "icon": "⚡",
            "title": "API Gateway\n(FastAPI)",
            "body": "The waiter.\nInspects article text, runs HTTP 422 checks, and delivers payload in 1 ms.",
            "tech": "Pydantic  •  Uvicorn"
        },
        {
            "left": Inches(10.40),
            "step": "STEP 3  •  KITCHEN",
            "icon": "⚙️",
            "title": "ML Engine\n(Scikit-Learn)",
            "body": "The kitchen.\nCleans raw text, computes 10,000-D TF-IDF, and runs hyperplane dot products.",
            "tech": "NLTK  •  Linear SVM"
        },
        {
            "left": Inches(15.05),
            "step": "STEP 4  •  RECIPE BOOK",
            "icon": "💾",
            "title": "Saved Models\n(Joblib)",
            "body": "The recipe book.\nPre-trained models loaded in RAM for instant prediction without retraining.",
            "tech": "Pickle / Joblib Storage"
        }
    ]
    
    # Bold Connecting Arrows between boxes
    arrow_tops = card_top_s6 + Inches(3.10)
    arrow_w = Inches(0.70)
    arrow_h = Inches(0.60)
    arrow_lefts = [Inches(5.00), Inches(9.65), Inches(14.30)]
    
    for al in arrow_lefts:
        arr = s6.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, al, arrow_tops, arrow_w, arrow_h)
        arr.name = f"Slide6_Arrow_{al}"
        arr.fill.solid()
        arr.fill.fore_color.rgb = c_cyan
        arr.line.color.rgb = c_cyan
        arr.line.width = Pt(1.5)
        
    for i, bdata in enumerate(boxes_s6):
        bx = bdata["left"]
        
        # Card Background
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, card_top_s6, box_w, box_h)
        card.name = f"Slide6_Box_{i+1}"
        card.fill.solid()
        card.fill.fore_color.rgb = c_white
        card.line.color.rgb = c_border
        card.line.width = Pt(2.0)
        
        # Content Text Box
        ctb = s6.shapes.add_textbox(bx + Inches(0.20), card_top_s6 + Inches(0.35), box_w - Inches(0.40), box_h - Inches(0.60))
        ctb.name = f"Slide6_BoxContent_{i+1}"
        ctf = ctb.text_frame
        ctf.word_wrap = True
        
        # Step Badge
        p_step = ctf.paragraphs[0]
        p_step.alignment = PP_ALIGN.CENTER
        p_step.text = bdata["step"]
        p_step.font.name = "Segoe UI"
        p_step.font.size = Pt(12)
        p_step.font.bold = True
        p_step.font.color.rgb = c_indigo
        p_step.space_after = Pt(6)
        
        # Icon
        p_icon = ctf.add_paragraph()
        p_icon.alignment = PP_ALIGN.CENTER
        p_icon.text = bdata["icon"]
        p_icon.font.size = Pt(40)
        p_icon.space_after = Pt(6)
        
        # Title (24pt Bold, CENTERED)
        p_title = ctf.add_paragraph()
        p_title.alignment = PP_ALIGN.CENTER
        p_title.text = bdata["title"]
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(23)
        p_title.font.bold = True
        p_title.font.color.rgb = c_navy
        p_title.space_after = Pt(12)
        
        # Body (18pt, CENTERED)
        p_body = ctf.add_paragraph()
        p_body.alignment = PP_ALIGN.CENTER
        p_body.text = bdata["body"]
        p_body.font.name = "Segoe UI"
        p_body.font.size = Pt(18)
        p_body.font.color.rgb = c_slate_dark
        p_body.space_after = Pt(14)
        
        # Tech Pill (14pt Consolas Bold)
        p_tech = ctf.add_paragraph()
        p_tech.alignment = PP_ALIGN.CENTER
        p_tech.text = f"[ {bdata['tech']} ]"
        p_tech.font.name = "Consolas"
        p_tech.font.size = Pt(14)
        p_tech.font.bold = True
        p_tech.font.color.rgb = c_indigo
        
    print("  Slide 6 rebuilt with flowchart layout, 4 centered boxes, bold connecting arrows, and 18pt/24pt fonts.")

    # -------------------------------------------------------------------------
    # SLIDE 7: The NLP Pipeline (Factory Assembly Line: Color Gradient & Bullets)
    # -------------------------------------------------------------------------
    print("\n[Slide 7] Redesigning to Factory Assembly Line layout: Color gradient, bold arrows, short bullets & examples...")
    s7 = prs.slides[6]
    
    # Clear previous shapes
    for shp in list(s7.shapes):
        sp = shp._element
        sp.getparent().remove(sp)
        
    # Title Header
    tb_s7 = s7.shapes.add_textbox(Inches(1.20), Inches(0.70), Inches(17.60), Inches(1.30))
    tb_s7.name = "Slide7_Header"
    tf_s7 = tb_s7.text_frame
    tf_s7.word_wrap = True
    
    p7_0 = tf_s7.paragraphs[0]
    p7_0.alignment = PP_ALIGN.CENTER
    p7_0.text = "The NLP Preprocessing Pipeline"
    p7_0.font.name = "Segoe UI"
    p7_0.font.size = Pt(34)
    p7_0.font.bold = True
    p7_0.font.color.rgb = c_white
    p7_0.space_after = Pt(4)
    
    p7_sub = tf_s7.add_paragraph()
    p7_sub.alignment = PP_ALIGN.CENTER
    p7_sub.text = "A 4-stage assembly line converting raw, noisy news text into calibrated mathematical features."
    p7_sub.font.name = "Segoe UI"
    p7_sub.font.size = Pt(18)
    p7_sub.font.color.rgb = c_slate_sub
    
    # 4 Factory Assembly Line Boxes (Progressive Color Gradient)
    box_w_s7 = Inches(3.85)
    box_h_s7 = Inches(6.80)
    card_top_s7 = Inches(3.20)
    
    stages_s7 = [
        {
            "left": Inches(1.10),
            "bg": c_grad1_bg,
            "bdr": c_grad1_bdr,
            "badge": "STAGE 01  •  CLEAN",
            "badge_col": RGBColor(3, 105, 161),
            "icon": "🧹",
            "title": "Text Cleaning",
            "example": '"Apple\'s $999!"  ➔  "apples 999"',
            "bullets": [
                "• Lowercases all characters",
                "• Strips punctuation & symbols",
                "• Eliminates HTML & URLs"
            ]
        },
        {
            "left": Inches(5.75),
            "bg": c_grad2_bg,
            "bdr": c_grad2_bdr,
            "badge": "STAGE 02  •  FILTER",
            "badge_col": RGBColor(2, 132, 199),
            "icon": "🛑",
            "title": "Stop-Words",
            "example": '["the", "laptop"]  ➔  ["laptop"]',
            "bullets": [
                "• Drops filler grammar words",
                "• Discards: 'the', 'is', 'with'",
                "• Retains high-signal tokens"
            ]
        },
        {
            "left": Inches(10.40),
            "bg": c_grad3_bg,
            "bdr": c_grad3_bdr,
            "badge": "STAGE 03  •  NORMALIZE",
            "badge_col": RGBColor(37, 99, 235),
            "icon": "🌱",
            "title": "Lemmatization",
            "example": '"running"  ➔  "run"\n"unveils"  ➔  "unveil"',
            "bullets": [
                "• WordNet morphological root",
                "• Normalizes plural forms",
                "• Unifies vocabulary space"
            ]
        },
        {
            "left": Inches(15.05),
            "bg": c_grad4_bg,
            "bdr": c_grad4_bdr,
            "badge": "STAGE 04  •  VECTORIZE",
            "badge_col": RGBColor(79, 70, 229),
            "icon": "🔢",
            "title": "TF-IDF Vector",
            "example": '"processor"  ➔  [0.35, 0, ...]',
            "bullets": [
                "• 10,000-D sparse vector",
                "• Downweights common words",
                "• Optimized for Linear SVM"
            ]
        }
    ]
    
    # Extra-Bold Factory Assembly Line Connecting Arrows
    arr7_tops = card_top_s7 + Inches(3.05)
    arr7_w = Inches(0.70)
    arr7_h = Inches(0.70)
    arr7_lefts = [Inches(5.00), Inches(9.65), Inches(14.30)]
    
    for al in arr7_lefts:
        arr7 = s7.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, al, arr7_tops, arr7_w, arr7_h)
        arr7.name = f"Slide7_AssemblyArrow_{al}"
        arr7.fill.solid()
        arr7.fill.fore_color.rgb = c_cyan
        arr7.line.color.rgb = c_cyan
        arr7.line.width = Pt(1.5)
        
    for i, sdata in enumerate(stages_s7):
        bx = sdata["left"]
        
        # Card Background with Progressive Color Gradient
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, card_top_s7, box_w_s7, box_h_s7)
        card.name = f"Slide7_StageBox_{i+1}"
        card.fill.solid()
        card.fill.fore_color.rgb = sdata["bg"]
        card.line.color.rgb = sdata["bdr"]
        card.line.width = Pt(2.5)
        
        # Content Text Box
        stb = s7.shapes.add_textbox(bx + Inches(0.20), card_top_s7 + Inches(0.35), box_w_s7 - Inches(0.40), box_h_s7 - Inches(0.60))
        stb.name = f"Slide7_StageContent_{i+1}"
        stf = stb.text_frame
        stf.word_wrap = True
        
        # Stage Badge
        p_badge = stf.paragraphs[0]
        p_badge.alignment = PP_ALIGN.CENTER
        p_badge.text = sdata["badge"]
        p_badge.font.name = "Segoe UI"
        p_badge.font.size = Pt(12)
        p_badge.font.bold = True
        p_badge.font.color.rgb = sdata["badge_col"]
        p_badge.space_after = Pt(6)
        
        # Icon
        p_icon = stf.add_paragraph()
        p_icon.alignment = PP_ALIGN.CENTER
        p_icon.text = sdata["icon"]
        p_icon.font.size = Pt(38)
        p_icon.space_after = Pt(6)
        
        # Title (24pt Bold, CENTERED)
        p_title = stf.add_paragraph()
        p_title.alignment = PP_ALIGN.CENTER
        p_title.text = sdata["title"]
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = c_navy
        p_title.space_after = Pt(10)
        
        # Example Box / Pill (18pt Bold Consolas, CENTERED)
        p_ex = stf.add_paragraph()
        p_ex.alignment = PP_ALIGN.CENTER
        p_ex.text = sdata["example"]
        p_ex.font.name = "Consolas"
        p_ex.font.size = Pt(16.5)
        p_ex.font.bold = True
        p_ex.font.color.rgb = c_indigo
        p_ex.space_after = Pt(14)
        
        # Bullets (18pt Segoe UI, CENTERED)
        for btext in sdata["bullets"]:
            pb = stf.add_paragraph()
            pb.alignment = PP_ALIGN.CENTER
            pb.text = btext
            pb.font.name = "Segoe UI"
            pb.font.size = Pt(18)
            pb.font.color.rgb = c_slate_dark
            pb.space_after = Pt(4)
            
    print("  Slide 7 rebuilt with factory assembly line, progressive color gradient, bold arrows, and concise examples/bullets.")

    # -------------------------------------------------------------------------
    # SLIDE 8: The AI Models We Tested (2x2 Grid Layout & Winner Highlight)
    # -------------------------------------------------------------------------
    print("\n[Slide 8] Redesigning to 2x2 Grid layout: Winner highlight, cut text, centered alignment, and 24pt/20pt fonts...")
    s8 = prs.slides[7]
    
    # Clear previous shapes
    for shp in list(s8.shapes):
        sp = shp._element
        sp.getparent().remove(sp)
        
    # Title Header
    tb_s8 = s8.shapes.add_textbox(Inches(1.20), Inches(0.70), Inches(17.60), Inches(1.30))
    tb_s8.name = "Slide8_Header"
    tf_s8 = tb_s8.text_frame
    tf_s8.word_wrap = True
    
    p8_0 = tf_s8.paragraphs[0]
    p8_0.alignment = PP_ALIGN.CENTER
    p8_0.text = "The AI Models We Tested"
    p8_0.font.name = "Segoe UI"
    p8_0.font.size = Pt(34)
    p8_0.font.bold = True
    p8_0.font.color.rgb = c_white
    p8_0.space_after = Pt(4)
    
    p8_sub = tf_s8.add_paragraph()
    p8_sub.alignment = PP_ALIGN.CENTER
    p8_sub.text = "Benchmarking 4 architectures on the identical 2,225 BBC news dataset (80% train, 20% test)."
    p8_sub.font.name = "Segoe UI"
    p8_sub.font.size = Pt(18)
    p8_sub.font.color.rgb = c_slate_sub
    
    # 2x2 Grid Coordinates (Squat, spacious rectangles!)
    card_w_s8 = Inches(8.40)
    card_h_s8 = Inches(3.75)
    row1_top = Inches(2.40)
    row2_top = Inches(6.60)
    col1_left = Inches(1.20)
    col2_left = Inches(10.40)
    
    models_s8 = [
        # Top-Left: Naive Bayes
        {
            "left": col1_left,
            "top": row1_top,
            "is_winner": False,
            "badge": "FAST PROBABILISTIC BASELINE",
            "title": "Naive Bayes",
            "stats": "⚡ 0.5 ms Latency   •   92.1% Accuracy",
            "subtitle": "Word Frequency Multi-Class Baseline",
            "body": "Calculates category probabilities based on word frequencies.\nAssumes word independence. Fast, lightweight reference model."
        },
        # Top-Right: Linear SVM (OUR WINNER / CHAMPION)
        {
            "left": col2_left,
            "top": row1_top,
            "is_winner": True,
            "badge": "⭐ PROJECT CHAMPION  •  OPTIMAL TRADE-OFF",
            "title": "Linear SVM (Champion ⭐)",
            "stats": "⚡ 1.2 ms Latency   •   96.4% Accuracy (0.963 F1)",
            "subtitle": "Max-Margin Hyperplane in 10,000-D Space",
            "body": "Draws optimal dividing hyperplanes between news topics.\nMatches deep learning accuracy with 10× faster CPU inference."
        },
        # Bottom-Left: Neural MLP
        {
            "left": col1_left,
            "top": row2_top,
            "is_winner": False,
            "badge": "NEURAL NETWORK BASELINE",
            "title": "Neural MLP (The Mini-Brain)",
            "stats": "⚡ 3.2 ms Latency   •   95.1% Accuracy",
            "subtitle": "Feedforward Network with ReLU Activation",
            "body": "Dense hidden layers learning non-linear word associations.\nFast CPU execution without requiring GPU acceleration."
        },
        # Bottom-Right: DistilBERT
        {
            "left": col2_left,
            "top": row2_top,
            "is_winner": False,
            "badge": "HEAVYWEIGHT DEEP LEARNING",
            "title": "DistilBERT (Transformer)",
            "stats": "⚡ 12.4 ms Latency   •   97.8% Accuracy",
            "subtitle": "Bidirectional Self-Attention Transformer",
            "body": "Reads full bidirectional sentence context for highest accuracy.\n10× slower latency and 20× higher memory footprint."
        }
    ]
    
    for i, mdata in enumerate(models_s8):
        bx = mdata["left"]
        by = mdata["top"]
        is_win = mdata["is_winner"]
        
        # Card Background
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, card_w_s8, card_h_s8)
        card.name = f"Slide8_ModelCard_{i+1}"
        card.fill.solid()
        
        if is_win:
            card.fill.fore_color.rgb = c_emerald_bg
            card.line.color.rgb = c_emerald
            card.line.width = Pt(3.5)
        else:
            card.fill.fore_color.rgb = c_white
            card.line.color.rgb = c_border
            card.line.width = Pt(2.0)
            
        # Text Frame Box
        tb = s8.shapes.add_textbox(bx + Inches(0.40), by + Inches(0.25), card_w_s8 - Inches(0.80), card_h_s8 - Inches(0.50))
        tb.name = f"Slide8_ModelText_{i+1}"
        tf = tb.text_frame
        tf.word_wrap = True
        
        # Badge
        p_badge = tf.paragraphs[0]
        p_badge.alignment = PP_ALIGN.CENTER
        p_badge.text = mdata["badge"]
        p_badge.font.name = "Segoe UI"
        p_badge.font.size = Pt(12)
        p_badge.font.bold = True
        p_badge.font.color.rgb = c_emerald if is_win else c_indigo
        p_badge.space_after = Pt(4)
        
        # Title (25pt Bold, CENTERED)
        p_title = tf.add_paragraph()
        p_title.alignment = PP_ALIGN.CENTER
        p_title.text = mdata["title"]
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(25)
        p_title.font.bold = True
        p_title.font.color.rgb = c_emerald_dark if is_win else c_navy
        p_title.space_after = Pt(4)
        
        # Stat Pill (17pt Bold Consolas, CENTERED)
        p_stat = tf.add_paragraph()
        p_stat.alignment = PP_ALIGN.CENTER
        p_stat.text = mdata["stats"]
        p_stat.font.name = "Consolas"
        p_stat.font.size = Pt(17)
        p_stat.font.bold = True
        p_stat.font.color.rgb = c_emerald if is_win else c_indigo
        p_stat.space_after = Pt(6)
        
        # Subtitle / Tag (15pt Bold Slate-500)
        p_sub = tf.add_paragraph()
        p_sub.alignment = PP_ALIGN.CENTER
        p_sub.text = mdata["subtitle"]
        p_sub.font.name = "Segoe UI"
        p_sub.font.size = Pt(15)
        p_sub.font.bold = True
        p_sub.font.color.rgb = c_emerald_dark if is_win else c_slate_mid
        p_sub.space_after = Pt(6)
        
        # Body (19pt, CENTERED)
        p_body = tf.add_paragraph()
        p_body.alignment = PP_ALIGN.CENTER
        p_body.text = mdata["body"]
        p_body.font.name = "Segoe UI"
        p_body.font.size = Pt(19)
        p_body.font.color.rgb = c_emerald_dark if is_win else c_slate_dark
        
    print("  Slide 8 rebuilt with 2x2 grid layout, Emerald winner highlight on Linear SVM, concise cut text, and 25pt/19pt centered fonts.")

    # Save to CruxTemplate presentation
    prs.save(prs_path)
    print(f"\n[Saved] Slides 5, 6, 7, and 8 successfully updated in {prs_path}!")

    # Attempt copy to NewsScope_Presentation.pptx
    target = "docs/NewsScope_Presentation.pptx"
    try:
        shutil.copy2(prs_path, target)
        print(f"[Synchronized] Successfully updated {target}!")
    except PermissionError:
        print(f"[Notice] {target} is locked by PowerPoint. Close PowerPoint and run docs/sync_when_unlocked.py.")
    except Exception as e:
        print(f"[Error] Failed to copy to {target}: {e}")

if __name__ == "__main__":
    update_slides()
