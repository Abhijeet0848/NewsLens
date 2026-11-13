import os
import shutil
import cv2
import qrcode
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def apply_fixes():
    prs_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    prs = Presentation(prs_path)
    
    # Common Palette
    c_navy = RGBColor(15, 23, 42)          # Slate 900 (#0F172A)
    c_slate = RGBColor(51, 65, 85)         # Slate 700 (#334155)
    c_slate_light = RGBColor(100, 116, 139)# Slate 500 (#64748B)
    c_card_bg = RGBColor(248, 250, 252)    # Slate 50 (#F8FAFC)
    c_white = RGBColor(255, 255, 255)      # White
    c_border = RGBColor(203, 213, 225)     # Slate 300 (#CBD5E1)
    c_indigo = RGBColor(79, 70, 229)       # Indigo 600 (#4F46E5)
    c_indigo_bg = RGBColor(238, 242, 255)  # Indigo 50 (#EEF2FF)
    c_indigo_bdr = RGBColor(99, 102, 241)  # Indigo 500 (#6366F1)
    c_emerald = RGBColor(5, 150, 105)      # Emerald 600 (#059669)
    
    print("==================================================")
    print("APPLYING 4 CRITICAL FIXES")
    print("==================================================")

    # ------------------------------------------------------------------
    # FIX 1: SLIDE 4 - NUMBERING TYPO ("Problem 1", "Problem 2", "Problem 3")
    # ------------------------------------------------------------------
    print("\n[Fix 1] Slide 4: Updating problem numbering to clean 'Problem 1', 'Problem 2', 'Problem 3'...")
    s4 = prs.slides[3]
    
    # Find TextBox 21, TextBox 24, TextBox 27 inside groups
    # Group 19 -> TextBox 21 ("Problem 1")
    # Group 22 -> TextBox 24 ("Problem 2")
    # Group 25 -> TextBox 27 ("Problem 3")
    problem_map = {
        "TextBox 21": "Problem 1",
        "TextBox 24": "Problem 2",
        "TextBox 27": "Problem 3"
    }
    
    for shp in s4.shapes:
        if shp.shape_type == 6: # Group
            for sub in shp.shapes:
                if sub.name in problem_map:
                    target_text = problem_map[sub.name]
                    tf = sub.text_frame
                    tf.word_wrap = False
                    for p in tf.paragraphs:
                        p.alignment = PP_ALIGN.CENTER
                        p.text = target_text
                        for r in p.runs:
                            r.font.name = "Segoe UI"
                            r.font.size = Pt(22)
                            r.font.bold = True
                            r.font.color.rgb = c_white
                    print(f"  Updated {sub.name} in {shp.name} -> '{target_text}' (Segoe UI Bold 22pt White)")

    # ------------------------------------------------------------------
    # FIX 2: SLIDE 6 - BROKEN TITLE ("How NewsScope is Built (4 Simple Parts)")
    # ------------------------------------------------------------------
    print("\n[Fix 2] Slide 6: Expanding title width to 17.50\" for single-line display...")
    s6 = prs.slides[5]
    
    # 1. Update TextBox 6
    tb6 = None
    for shp in s6.shapes:
        if shp.name == "TextBox 6":
            tb6 = shp
            break
            
    if tb6:
        tb6.left = Inches(1.39)
        tb6.top = Inches(0.95)
        tb6.width = Inches(17.50)
        tb6.height = Inches(1.10)
        tf6 = tb6.text_frame
        tf6.word_wrap = False
        for p in tf6.paragraphs:
            p.alignment = PP_ALIGN.LEFT
            p.text = "How NewsScope is Built (4 Simple Parts)"
            for r in p.runs:
                r.font.name = "Segoe UI"
                r.font.size = Pt(34)
                r.font.bold = True
                r.font.color.rgb = c_navy
        print("  TextBox 6 set to width=17.50\" on single line: 'How NewsScope is Built (4 Simple Parts)'")

    # 2. Update TextBox 7 (Subtitle)
    for shp in s6.shapes:
        if shp.name == "TextBox 7":
            shp.left = Inches(1.39)
            shp.top = Inches(2.20)
            shp.width = Inches(17.50)
            shp.height = Inches(0.85)
            tf7 = shp.text_frame
            for p in tf7.paragraphs:
                for r in p.runs:
                    r.font.name = "Segoe UI"
                    r.font.size = Pt(18)
                    r.font.color.rgb = c_slate_light
            print("  TextBox 7 (Subtitle) aligned cleanly at top=2.20\"")

    # 3. Clean up off-screen Latin placeholder shapes (TextBox 16, 17, 18)
    shapes_to_remove = []
    for shp in s6.shapes:
        if shp.name in ["TextBox 16", "TextBox 17", "TextBox 18"] or shp.left < 0:
            shapes_to_remove.append(shp)
            
    for shp in shapes_to_remove:
        sp = shp._element
        sp.getparent().remove(sp)
        print(f"  Permanently removed off-screen shape from XML: {shp.name}")

    # ------------------------------------------------------------------
    # FIX 3: SLIDE 10 - REWRITE MATH ENGINE (Clean 2-Card Layout, Eradicate AI Glitch)
    # ------------------------------------------------------------------
    print("\n[Fix 3] Slide 10: Eradicating legacy hallucination and rebuilding clean 2-card layout...")
    s10 = prs.slides[9]
    
    # Permanently remove ALL existing shapes on Slide 10 to ensure zero leftover text
    for shp in list(s10.shapes):
        sp = shp._element
        sp.getparent().remove(sp)
    print("  Emptied Slide 10 shape tree of all legacy shapes.")

    # 1. Slide Title Header
    tb_title = s10.shapes.add_textbox(Inches(1.30), Inches(0.70), Inches(17.40), Inches(1.50))
    tb_title.name = "Slide10_Title"
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    
    p_t1 = tf_title.paragraphs[0]
    p_t1.text = "The Live Example: Step-by-Step"
    p_t1.font.name = "Segoe UI"
    p_t1.font.size = Pt(34)
    p_t1.font.bold = True
    p_t1.font.color.rgb = c_navy
    p_t1.space_after = Pt(4)
    
    p_t2 = tf_title.add_paragraph()
    p_t2.text = "Steps 2 & 3: Feature Extraction (TF-IDF) & Multi-Model Inference (Linear SVM)"
    p_t2.font.name = "Segoe UI"
    p_t2.font.size = Pt(17)
    p_t2.font.bold = False
    p_t2.font.color.rgb = c_slate_light

    # 2. Card 1 (Left): Box 1 - Step 2: TF-IDF Vectorization
    card1_left = Inches(1.30)
    card1_top = Inches(2.45)
    card1_w = Inches(8.10)
    card1_h = Inches(8.10)
    
    c1_rect = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card1_left, card1_top, card1_w, card1_h)
    c1_rect.name = "Card1_Background"
    c1_rect.fill.solid()
    c1_rect.fill.fore_color.rgb = c_card_bg
    c1_rect.line.color.rgb = c_border
    c1_rect.line.width = Pt(1.5)
    
    c1_tb = s10.shapes.add_textbox(card1_left + Inches(0.45), card1_top + Inches(0.40), card1_w - Inches(0.90), card1_h - Inches(0.80))
    c1_tb.name = "Card1_Content"
    tf1 = c1_tb.text_frame
    tf1.word_wrap = True
    
    # Step badge
    p1 = tf1.paragraphs[0]
    p1.text = "STEP 02  •  FEATURE EXTRACTION"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = c_indigo
    p1.space_after = Pt(6)
    
    # Card Title
    p2 = tf1.add_paragraph()
    p2.text = "Step 2: TF-IDF Vectorization"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(23)
    p2.font.bold = True
    p2.font.color.rgb = c_navy
    p2.space_after = Pt(14)
    
    # Explanation
    p3 = tf1.add_paragraph()
    p3.text = "The Math: The model converts these cleaned words into a 10,000-dimensional mathematical feature vector."
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(14.5)
    p3.font.color.rgb = c_slate
    p3.space_after = Pt(12)
    
    # TF Bullet
    p4 = tf1.add_paragraph()
    p4.text = 'TF (Term Frequency): The word "apple" appears 1 time in the article.'
    p4.font.name = "Segoe UI"
    p4.font.size = Pt(14.5)
    p4.font.color.rgb = c_slate
    p4.space_after = Pt(12)
    
    # IDF Bullet
    p5 = tf1.add_paragraph()
    p5.text = 'IDF (Inverse Document Frequency): The word "apple" is rare in general news, but highly common in Tech news. Therefore, it gets a massive mathematical weight.'
    p5.font.name = "Segoe UI"
    p5.font.size = Pt(14.5)
    p5.font.color.rgb = c_slate
    p5.space_after = Pt(14)
    
    # Subhead Saliency
    p6 = tf1.add_paragraph()
    p6.text = "Top Saliency Word Weights Extracted:"
    p6.font.name = "Segoe UI"
    p6.font.size = Pt(14.5)
    p6.font.bold = True
    p6.font.color.rgb = c_navy
    p6.space_after = Pt(6)
    
    # Tokens with weights
    tokens = [
        ('• "processor"', "+0.35  (High tech discriminator)"),
        ('• "macbook"', "+0.32  (Domain specific hardware)"),
        ('• "apple"', "+0.28  (Brand anchor entity)"),
        ('• "battery"', "+0.18  (Specification feature)")
    ]
    for tok, desc in tokens:
        pt = tf1.add_paragraph()
        pt.text = f"{tok.ljust(16)} ➔  {desc}"
        pt.font.name = "Consolas"
        pt.font.size = Pt(13)
        pt.font.color.rgb = c_indigo
        pt.space_after = Pt(3)

    # 3. Connecting Arrow in between
    arrow_left = Inches(9.55)
    arrow_top = Inches(6.00)
    arrow_w = Inches(0.90)
    arrow_h = Inches(0.50)
    arr = s10.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, arrow_left, arrow_top, arrow_w, arrow_h)
    arr.name = "Center_Connector_Arrow"
    arr.fill.solid()
    arr.fill.fore_color.rgb = c_indigo
    arr.line.color.rgb = c_indigo
    arr.line.width = Pt(1.0)

    # 4. Card 2 (Right): Box 2 - Step 3: Linear SVM Classification
    card2_left = Inches(10.60)
    card2_top = Inches(2.45)
    card2_w = Inches(8.10)
    card2_h = Inches(8.10)
    
    c2_rect = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card2_left, card2_top, card2_w, card2_h)
    c2_rect.name = "Card2_Background"
    c2_rect.fill.solid()
    c2_rect.fill.fore_color.rgb = c_indigo_bg
    c2_rect.line.color.rgb = c_indigo_bdr
    c2_rect.line.width = Pt(2.0)
    
    c2_tb = s10.shapes.add_textbox(card2_left + Inches(0.45), card2_top + Inches(0.40), card2_w - Inches(0.90), card2_h - Inches(0.80))
    c2_tb.name = "Card2_Content"
    tf2 = c2_tb.text_frame
    tf2.word_wrap = True
    
    # Step badge
    p2_1 = tf2.paragraphs[0]
    p2_1.text = "STEP 03  •  CHAMPION MODEL INFERENCE"
    p2_1.font.name = "Segoe UI"
    p2_1.font.size = Pt(12)
    p2_1.font.bold = True
    p2_1.font.color.rgb = c_emerald
    p2_1.space_after = Pt(6)
    
    # Card Title
    p2_2 = tf2.add_paragraph()
    p2_2.text = "Step 3: Linear SVM Classification"
    p2_2.font.name = "Segoe UI"
    p2_2.font.size = Pt(23)
    p2_2.font.bold = True
    p2_2.font.color.rgb = c_navy
    p2_2.space_after = Pt(14)
    
    # Math Explanation
    p2_3 = tf2.add_paragraph()
    p2_3.text = "The Math: The SVM calculates the dot product:"
    p2_3.font.name = "Segoe UI"
    p2_3.font.size = Pt(14.5)
    p2_3.font.color.rgb = c_slate
    p2_3.space_after = Pt(2)
    
    p2_math = tf2.add_paragraph()
    p2_math.text = "Score(k) = (Word Weight) × (SVM Category Hyperplane Weight)"
    p2_math.font.name = "Consolas"
    p2_math.font.size = Pt(13.5)
    p2_math.font.bold = True
    p2_math.font.color.rgb = c_indigo
    p2_math.space_after = Pt(12)
    
    p2_4 = tf2.add_paragraph()
    p2_4.text = 'It sees strong Tech words like "m3", "macbook", and "processor" driving the score heavily into the Technology decision region.'
    p2_4.font.name = "Segoe UI"
    p2_4.font.size = Pt(14.5)
    p2_4.font.color.rgb = c_slate
    p2_4.space_after = Pt(14)
    
    p2_5 = tf2.add_paragraph()
    p2_5.text = "Calibrated Probability Distribution:"
    p2_5.font.name = "Segoe UI"
    p2_5.font.size = Pt(14.5)
    p2_5.font.bold = True
    p2_5.font.color.rgb = c_navy
    p2_5.space_after = Pt(6)
    
    probs = [
        ("⭐ Technology:", "97.7%  [DEFINITIVE WINNER]"),
        ("•  Business:", "0.4%"),
        ("•  Sport:", "0.2%"),
        ("•  Politics:", "0.1%"),
        ("•  Entertainment:", "0.1%")
    ]
    for cat, val in probs:
        pp = tf2.add_paragraph()
        pp.text = f"{cat.ljust(18)} {val}"
        pp.font.name = "Consolas"
        pp.font.size = Pt(13)
        if "⭐" in cat:
            pp.font.bold = True
            pp.font.color.rgb = c_emerald
        else:
            pp.font.color.rgb = c_slate
        pp.space_after = Pt(2)
        
    p2_cons = tf2.add_paragraph()
    p2_cons.text = "✔ 100% Architecture Consensus (DistilBERT 97.8%, MLP 95.1%, NB 92.1%)"
    p2_cons.font.name = "Segoe UI"
    p2_cons.font.size = Pt(13.5)
    p2_cons.font.bold = True
    p2_cons.font.color.rgb = c_indigo
    p2_cons.space_before = Pt(10)
    
    print("  Slide 10 rebuilt with clean 2-card layout connecting Step 1 (Slide 9) to Step 4 (Slide 11).")

    # ------------------------------------------------------------------
    # FIX 4: SLIDE 15 - GITHUB REPO URL & FLAT QR CODE
    # ------------------------------------------------------------------
    print("\n[Fix 4] Slide 15: Updating GitHub repo URL to NewsScope and inserting flat QR code...")
    s15 = prs.slides[14]
    
    # 1. Update TextBox 25 text
    for shp in s15.shapes:
        if shp.name == "TextBox 25":
            tf = shp.text_frame
            tf.word_wrap = True
            while len(tf.paragraphs) > 0:
                p_rem = tf.paragraphs[-1]._p
                p_rem.getparent().remove(p_rem)
                
            p0 = tf.add_paragraph()
            p0.text = "Scan the QR code above or visit the project repository:"
            p0.font.name = "Segoe UI"
            p0.font.size = Pt(18)
            p0.font.color.rgb = c_slate
            p0.alignment = PP_ALIGN.CENTER
            p0.space_after = Pt(8)
            
            p1 = tf.add_paragraph()
            p1.text = "https://github.com/Abhijeet0848/NewsScope"
            p1.font.name = "Consolas"
            p1.font.size = Pt(26)
            p1.font.bold = True
            p1.font.color.rgb = c_indigo
            p1.alignment = PP_ALIGN.CENTER
            p1.space_after = Pt(8)
            
            p2 = tf.add_paragraph()
            p2.text = "Full Source Code   •   Pretrained Joblib Models   •   Complete Academic Report"
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(15)
            p2.font.color.rgb = c_slate_light
            p2.alignment = PP_ALIGN.CENTER
            print("  Updated TextBox 25 with https://github.com/Abhijeet0848/NewsScope (26pt Consolas Bold Indigo)")

    # 2. Remove old 3D/shadow QR picture (Picture 27) and any old QR shape
    s15_remove = []
    for shp in s15.shapes:
        if shp.name in ["Picture 27", "Slide15_FlatQR", "QR_Card_Background"] or (shp.shape_type == 13 and shp.left < Inches(0)):
            s15_remove.append(shp)
            
    for shp in s15_remove:
        sp = shp._element
        sp.getparent().remove(sp)
        print(f"  Removed old QR shape: {shp.name}")

    # 3. Add clean flat QR card container + image
    qr_card_w = Inches(4.30)
    qr_card_h = Inches(4.30)
    qr_card_left = (prs.slide_width - qr_card_w) / 2
    qr_card_top = Inches(3.40)
    
    qr_bg = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qr_card_left, qr_card_top, qr_card_w, qr_card_h)
    qr_bg.name = "QR_Card_Background"
    qr_bg.fill.solid()
    qr_bg.fill.fore_color.rgb = c_white
    qr_bg.line.color.rgb = c_border
    qr_bg.line.width = Pt(1.5)
    
    qr_img_w = Inches(3.90)
    qr_img_h = Inches(3.90)
    qr_img_left = (prs.slide_width - qr_img_w) / 2
    qr_img_top = qr_card_top + Inches(0.20)
    
    qr_pic = s15.shapes.add_picture("docs/github_qr_flat.png", qr_img_left, qr_img_top, qr_img_w, qr_img_h)
    qr_pic.name = "Slide15_FlatQR"
    print(f"  Inserted flat, zero-shadow QR code centered at left={qr_img_left/914400:.2f}\", top={qr_img_top/914400:.2f}\"")

    # Position TextBox 25 cleanly below the QR card
    for shp in s15.shapes:
        if shp.name == "TextBox 25":
            shp.left = Inches(2.00)
            shp.top = Inches(7.95)
            shp.width = Inches(16.00)
            shp.height = Inches(2.30)

    # Save presentation
    prs.save(prs_path)
    print(f"\n[Saved] All 4 fixes saved to {prs_path}")

    # Synchronize to docs/NewsScope_Presentation.pptx
    target_path = "docs/NewsScope_Presentation.pptx"
    try:
        shutil.copy2(prs_path, target_path)
        print(f"[Synchronized] Successfully copied to {target_path}")
    except PermissionError:
        print(f"[Warning] Could not copy to {target_path} because PowerPoint has it open. Close PowerPoint and run sync.")
    except Exception as e:
        print(f"[Error] Failed to copy to {target_path}: {e}")

if __name__ == "__main__":
    apply_fixes()
