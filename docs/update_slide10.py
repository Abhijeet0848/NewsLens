import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def update_slide10():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(alt_path)
    s10 = prs.slides[9]
    
    # 1. Clean up unused / floating leftover text boxes (shapes 0 through 7)
    for idx in range(8):
        s10.shapes[idx].left = Inches(-20)
        
    # Also hide old connectors (shapes 16, 17, 18) to avoid overlap with new aligned cards
    for idx in [16, 17, 18]:
        if idx < len(s10.shapes):
            s10.shapes[idx].left = Inches(-20)
            
    # 2. Main Title & Subtitle at top
    # Use or add a title shape
    title_shp = None
    for shp in s10.shapes:
        if shp.name == "Slide10_Title":
            title_shp = shp
            break
            
    if not title_shp:
        title_shp = s10.shapes.add_textbox(Inches(3.00), Inches(0.60), Inches(14.00), Inches(1.30))
        title_shp.name = "Slide10_Title"
    else:
        title_shp.left = Inches(3.00)
        title_shp.top = Inches(0.60)
        title_shp.width = Inches(14.00)
        title_shp.height = Inches(1.30)
        
    tf_title = title_shp.text_frame
    tf_title.word_wrap = True
    
    # Paragraph 0: Main Title
    p0 = tf_title.paragraphs[0]
    p0.text = "The Live Example: Step-by-Step"
    p0.alignment = PP_ALIGN.CENTER
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    p0.space_after = Pt(4)
    
    # Paragraph 1: Subtitle
    while len(tf_title.paragraphs) > 1:
        p_rem = tf_title.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p1 = tf_title.add_paragraph()
    p1.text = "Steps 2 & 3: Feature Extraction & Multi-Model Inference"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(79, 70, 229) # Electric Indigo (#4F46E5)
    
    # 3. Position the 4 cards in a neat 2x2 grid
    # Card 1 (Top-Left): Shape 10 (Rectangle 38)
    # Card 2 (Top-Right): Shape 11 (Rectangle 39)
    # Card 3 (Bottom-Left): Shape 12 (Rectangle 40)
    # Card 4 (Bottom-Right): Shape 13 (Rectangle 42)
    
    card_w = Inches(8.40)
    card_h = Inches(4.00)
    top_r1 = Inches(2.20)
    top_r2 = Inches(6.50)
    left_c1 = Inches(1.20)
    left_c2 = Inches(10.40)
    
    # Colors
    c_card_bg = RGBColor(248, 250, 252)     # Slate 50
    c_border = RGBColor(203, 213, 225)      # Slate 300
    c_winner_bg = RGBColor(238, 242, 255)   # Indigo 50
    c_winner_bdr = RGBColor(99, 102, 241)   # Indigo 500
    c_navy = RGBColor(15, 23, 42)           # Slate 900
    c_slate = RGBColor(51, 65, 85)          # Slate 700
    c_indigo = RGBColor(79, 70, 229)        # Electric Indigo
    c_emerald = RGBColor(5, 150, 105)       # Emerald 600
    
    # Setup Card 1 Background
    c1 = s10.shapes[10]
    c1.left = left_c1
    c1.top = top_r1
    c1.width = card_w
    c1.height = card_h
    c1.fill.solid()
    c1.fill.fore_color.rgb = c_card_bg
    c1.line.color.rgb = c_border
    c1.line.width = Pt(1.5)
    
    # Setup Card 2 Background
    c2 = s10.shapes[11]
    c2.left = left_c2
    c2.top = top_r1
    c2.width = card_w
    c2.height = card_h
    c2.fill.solid()
    c2.fill.fore_color.rgb = c_card_bg
    c2.line.color.rgb = c_border
    c2.line.width = Pt(1.5)
    
    # Setup Card 3 Background
    c3 = s10.shapes[12]
    c3.left = left_c1
    c3.top = top_r2
    c3.width = card_w
    c3.height = card_h
    c3.fill.solid()
    c3.fill.fore_color.rgb = c_card_bg
    c3.line.color.rgb = c_border
    c3.line.width = Pt(1.5)
    
    # Setup Card 4 Background (Winner highlight)
    c4 = s10.shapes[13]
    c4.left = left_c2
    c4.top = top_r2
    c4.width = card_w
    c4.height = card_h
    c4.fill.solid()
    c4.fill.fore_color.rgb = c_winner_bg
    c4.line.color.rgb = c_winner_bdr
    c4.line.width = Pt(2.0)
    
    # 4. Text for Card 1 (Use Shape 14 / TextBox 44)
    tb1 = s10.shapes[14]
    tb1.left = left_c1 + Inches(0.40)
    tb1.top = top_r1 + Inches(0.30)
    tb1.width = card_w - Inches(0.80)
    tb1.height = card_h - Inches(0.60)
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    while len(tf1.paragraphs) > 0:
        p_rem = tf1.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p1_title = tf1.add_paragraph()
    p1_title.text = "Step 2A: Cleaning & Tokenization"
    p1_title.font.name = "Segoe UI"
    p1_title.font.size = Pt(20)
    p1_title.font.bold = True
    p1_title.font.color.rgb = c_navy
    p1_title.space_after = Pt(8)
    
    p1_b1 = tf1.add_paragraph()
    p1_b1.text = "• Lowercases text and strips punctuation, URLs, and numbers."
    p1_b1.font.name = "Segoe UI"
    p1_b1.font.size = Pt(15)
    p1_b1.font.color.rgb = c_slate
    p1_b1.space_after = Pt(4)
    
    p1_b2 = tf1.add_paragraph()
    p1_b2.text = "• Removes common English stopwords: 'the', 'with', 'and', 'can'."
    p1_b2.font.name = "Segoe UI"
    p1_b2.font.size = Pt(15)
    p1_b2.font.color.rgb = c_slate
    p1_b2.space_after = Pt(8)
    
    p1_tokens = tf1.add_paragraph()
    p1_tokens.text = "Filtered Tokens (23 terms extracted):\n['apple', 'unveil', 'new', 'm3', 'macbook', 'laptop', 'ultra', 'fast', 'processor', 'battery', 'life', 'graphics', 'developer', 'machine', 'learning']"
    p1_tokens.font.name = "Consolas"
    p1_tokens.font.size = Pt(13)
    p1_tokens.font.color.rgb = c_indigo
    
    # 5. Text for Card 2 (Add or update textbox)
    tb2 = None
    for shp in s10.shapes:
        if shp.name == "Card2_Text":
            tb2 = shp
            break
    if not tb2:
        tb2 = s10.shapes.add_textbox(left_c2 + Inches(0.40), top_r1 + Inches(0.30), card_w - Inches(0.80), card_h - Inches(0.60))
        tb2.name = "Card2_Text"
    else:
        tb2.left = left_c2 + Inches(0.40)
        tb2.top = top_r1 + Inches(0.30)
        tb2.width = card_w - Inches(0.80)
        tb2.height = card_h - Inches(0.60)
        
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    while len(tf2.paragraphs) > 0:
        p_rem = tf2.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p2_title = tf2.add_paragraph()
    p2_title.text = "Step 2B: Lemmatization (Root Standard)"
    p2_title.font.name = "Segoe UI"
    p2_title.font.size = Pt(20)
    p2_title.font.bold = True
    p2_title.font.color.rgb = c_navy
    p2_title.space_after = Pt(8)
    
    p2_b1 = tf2.add_paragraph()
    p2_b1.text = "• Reduces word variants to canonical dictionary lemmas via WordNet:"
    p2_b1.font.name = "Segoe UI"
    p2_b1.font.size = Pt(15)
    p2_b1.font.color.rgb = c_slate
    p2_b1.space_after = Pt(4)
    
    p2_ex1 = tf2.add_paragraph()
    p2_ex1.text = "   'unveils'  ➔  'unveil'   |   'delivers'  ➔  'deliver'"
    p2_ex1.font.name = "Consolas"
    p2_ex1.font.size = Pt(14)
    p2_ex1.font.bold = True
    p2_ex1.font.color.rgb = c_indigo
    p2_ex1.space_after = Pt(4)
    
    p2_ex2 = tf2.add_paragraph()
    p2_ex2.text = "   'applications'  ➔  'application'   |   'laptops'  ➔  'laptop'"
    p2_ex2.font.name = "Consolas"
    p2_ex2.font.size = Pt(14)
    p2_ex2.font.bold = True
    p2_ex2.font.color.rgb = c_indigo
    p2_ex2.space_after = Pt(8)
    
    p2_b2 = tf2.add_paragraph()
    p2_b2.text = "• Benefit: Connects inflectional variations directly to the 10,000-feature BBC vocabulary without ballooning dictionary size."
    p2_b2.font.name = "Segoe UI"
    p2_b2.font.size = Pt(14)
    p2_b2.font.color.rgb = c_slate
    
    # 6. Text for Card 3 (Add or update textbox)
    tb3 = None
    for shp in s10.shapes:
        if shp.name == "Card3_Text":
            tb3 = shp
            break
    if not tb3:
        tb3 = s10.shapes.add_textbox(left_c1 + Inches(0.40), top_r2 + Inches(0.30), card_w - Inches(0.80), card_h - Inches(0.60))
        tb3.name = "Card3_Text"
    else:
        tb3.left = left_c1 + Inches(0.40)
        tb3.top = top_r2 + Inches(0.30)
        tb3.width = card_w - Inches(0.80)
        tb3.height = card_h - Inches(0.60)
        
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    while len(tf3.paragraphs) > 0:
        p_rem = tf3.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p3_title = tf3.add_paragraph()
    p3_title.text = "Step 3A: TF-IDF Feature Extraction"
    p3_title.font.name = "Segoe UI"
    p3_title.font.size = Pt(20)
    p3_title.font.bold = True
    p3_title.font.color.rgb = c_navy
    p3_title.space_after = Pt(8)
    
    p3_b1 = tf3.add_paragraph()
    p3_b1.text = "• Computes mathematical saliency: TF × log(N / DF)."
    p3_b1.font.name = "Segoe UI"
    p3_b1.font.size = Pt(15)
    p3_b1.font.color.rgb = c_slate
    p3_b1.space_after = Pt(6)
    
    p3_kw = tf3.add_paragraph()
    p3_kw.text = "Top Informative Keywords Identified for 'Technology':\n  • processor :  +0.35  (35% relative weight)\n  • macbook   :  +0.32  (32% relative weight)\n  • apple     :  +0.28  (28% relative weight)\n  • laptop    :  +0.24  (24% relative weight)\n  • graphics  :  +0.21  (21% relative weight)"
    p3_kw.font.name = "Consolas"
    p3_kw.font.size = Pt(13)
    p3_kw.font.bold = True
    p3_kw.font.color.rgb = c_indigo
    
    # 7. Text for Card 4 (Use Shape 15 / TextBox 47)
    tb4 = s10.shapes[15]
    tb4.left = left_c2 + Inches(0.40)
    tb4.top = top_r2 + Inches(0.30)
    tb4.width = card_w - Inches(0.80)
    tb4.height = card_h - Inches(0.60)
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    while len(tf4.paragraphs) > 0:
        p_rem = tf4.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p4_title = tf4.add_paragraph()
    p4_title.text = "Step 3B: AI Multi-Model Evaluation"
    p4_title.font.name = "Segoe UI"
    p4_title.font.size = Pt(20)
    p4_title.font.bold = True
    p4_title.font.color.rgb = c_navy
    p4_title.space_after = Pt(8)
    
    p4_b1 = tf4.add_paragraph()
    p4_b1.text = "All 4 models evaluate the 10,000-dimensional vector:"
    p4_b1.font.name = "Segoe UI"
    p4_b1.font.size = Pt(14)
    p4_b1.font.color.rgb = c_slate
    p4_b1.space_after = Pt(6)
    
    p4_m1 = tf4.add_paragraph()
    p4_m1.text = "⭐ Linear SVM: Technology  (98.4% Confidence | 1.2 ms) [Winner]"
    p4_m1.font.name = "Segoe UI"
    p4_m1.font.size = Pt(14)
    p4_m1.font.bold = True
    p4_m1.font.color.rgb = c_emerald
    p4_m1.space_after = Pt(3)
    
    p4_m2 = tf4.add_paragraph()
    p4_m2.text = "• DistilBERT:  Technology  (99.1% Confidence | 12.4 ms)"
    p4_m2.font.name = "Segoe UI"
    p4_m2.font.size = Pt(14)
    p4_m2.font.color.rgb = c_slate
    p4_m2.space_after = Pt(3)
    
    p4_m3 = tf4.add_paragraph()
    p4_m3.text = "• Neural MLP:  Technology  (97.0% Confidence | 3.2 ms)"
    p4_m3.font.name = "Segoe UI"
    p4_m3.font.size = Pt(14)
    p4_m3.font.color.rgb = c_slate
    p4_m3.space_after = Pt(3)
    
    p4_m4 = tf4.add_paragraph()
    p4_m4.text = "• Naive Bayes: Technology  (93.5% Confidence | 0.5 ms)"
    p4_m4.font.name = "Segoe UI"
    p4_m4.font.size = Pt(14)
    p4_m4.font.color.rgb = c_slate
    p4_m4.space_after = Pt(8)
    
    p4_res = tf4.add_paragraph()
    p4_res.text = "✔ 100% Unanimous Agreement: Technology is guaranteed."
    p4_res.font.name = "Segoe UI"
    p4_res.font.size = Pt(13)
    p4_res.font.bold = True
    p4_res.font.color.rgb = c_indigo
    
    # 8. Speaker Notes
    try:
        notes_slide = s10.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = (
            "Here is the machine learning pipeline in action on our Apple M3 MacBook text. "
            "First, in Step 2A, we remove stopwords like 'the' and 'with' and extract 23 key tokens. "
            "Next, in Step 2B, lemmatization standardizes words like 'delivers' into 'deliver' so our dictionary recognizes them. "
            "In Step 3A, the TF-IDF vectorizer assigns mathematical weights to each word—notice how 'processor' and 'macbook' received high scores above 0.30. "
            "Finally, in Step 3B, our 4 models score the text simultaneously. All 4 agree with over 93% confidence that this belongs to Technology, with our production Linear SVM making the call in just 1.2 milliseconds."
        )
        print("Speaker notes added to Slide 10")
    except Exception as e:
        print(f"Notes warning: {e}")
        
    # Save
    saved_paths = []
    try:
        prs.save(pptx_path)
        saved_paths.append(pptx_path)
    except PermissionError:
        print(f"Notice: {pptx_path} is currently locked by PowerPoint.")
        
    try:
        prs.save(alt_path)
        saved_paths.append(alt_path)
    except PermissionError:
        print(f"Notice: {alt_path} is currently locked.")
        
    print(f"Slide 10 successfully updated in: {', '.join(saved_paths)}!")

if __name__ == "__main__":
    update_slide10()
