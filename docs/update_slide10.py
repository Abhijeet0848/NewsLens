import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide10():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(alt_path)
    s10 = prs.slides[9]
    
    # Colors
    c_card_bg = RGBColor(248, 250, 252)     # Slate 50 (#F8FAFC)
    c_border = RGBColor(203, 213, 225)      # Slate 300 (#CBD5E1)
    c_winner_bg = RGBColor(238, 242, 255)   # Indigo 50 (#EEF2FF)
    c_winner_bdr = RGBColor(99, 102, 241)   # Indigo 500 (#6366F1)
    c_navy = RGBColor(15, 23, 42)           # Slate 900
    c_slate = RGBColor(51, 65, 85)          # Slate 700
    c_indigo = RGBColor(79, 70, 229)        # Electric Indigo (#4F46E5)
    c_emerald = RGBColor(5, 150, 105)       # Emerald 600 (#059669)
    
    # 1. Clean up unused / floating leftover text boxes (shapes 0 through 7)
    for idx in range(8):
        s10.shapes[idx].left = Inches(-20)
        
    # Hide temporary slide title if present so boxes have full vertical breathing space
    for shp in s10.shapes:
        if shp.name == "Slide10_Title":
            shp.left = Inches(-20)
            
    # 2. Position the 4 cards in the exact Crux template layout
    # Box 1 (Top-Left): Shape 10 (Rectangle 38)
    # Box 2 (Top-Right): Shape 11 (Rectangle 39)
    # Box 3 (Bottom-Left): Shape 12 (Rectangle 40)
    # Box 4 (Bottom-Right): Shape 13 (Rectangle 42)
    
    box1_left = Inches(1.29)
    box1_top = Inches(0.37)
    box1_w = Inches(6.75)
    box1_h = Inches(4.95)
    
    box2_left = Inches(11.12)
    box2_top = Inches(0.37)
    box2_w = Inches(6.48)
    box2_h = Inches(4.95)
    
    box3_left = Inches(1.24)
    box3_top = Inches(5.72)
    box3_w = Inches(7.10)
    box3_h = Inches(5.33)
    
    box4_left = Inches(11.12)
    box4_top = Inches(5.58)
    box4_w = Inches(6.48)
    box4_h = Inches(5.29)
    
    # Setup Box 1 Shape
    b1 = s10.shapes[10]
    b1.left = box1_left
    b1.top = box1_top
    b1.width = box1_w
    b1.height = box1_h
    b1.fill.solid()
    b1.fill.fore_color.rgb = c_card_bg
    b1.line.color.rgb = c_border
    b1.line.width = Pt(1.5)
    
    # Setup Box 2 Shape
    b2 = s10.shapes[11]
    b2.left = box2_left
    b2.top = box2_top
    b2.width = box2_w
    b2.height = box2_h
    b2.fill.solid()
    b2.fill.fore_color.rgb = c_card_bg
    b2.line.color.rgb = c_border
    b2.line.width = Pt(1.5)
    
    # Setup Box 3 Shape
    b3 = s10.shapes[12]
    b3.left = box3_left
    b3.top = box3_top
    b3.width = box3_w
    b3.height = box3_h
    b3.fill.solid()
    b3.fill.fore_color.rgb = c_card_bg
    b3.line.color.rgb = c_border
    b3.line.width = Pt(1.5)
    
    # Setup Box 4 Shape (Highlighted Result Card)
    b4 = s10.shapes[13]
    b4.left = box4_left
    b4.top = box4_top
    b4.width = box4_w
    b4.height = box4_h
    b4.fill.solid()
    b4.fill.fore_color.rgb = c_winner_bg
    b4.line.color.rgb = c_winner_bdr
    b4.line.width = Pt(2.0)
    
    # 3. Restore and align the 3 Connecting Arrows
    # Connector 17: Elbow 56 (Box 1 -> Box 2)
    c17 = s10.shapes[17]
    c17.left = Inches(8.04)
    c17.top = Inches(2.12)
    c17.width = Inches(2.96)
    c17.height = Inches(0.92)
    
    # Connector 16: Elbow 53 (Box 2 -> Box 3)
    c16 = s10.shapes[16]
    c16.left = Inches(8.44)
    c16.top = Inches(4.62)
    c16.width = Inches(2.68)
    c16.height = Inches(2.05)
    
    # Connector 18: Elbow 57 (Box 3 -> Box 4)
    c18 = s10.shapes[18]
    c18.left = Inches(8.39)
    c18.top = Inches(7.85)
    c18.width = Inches(2.68)
    c18.height = Inches(0.78)
    
    # 4. Text for Box 1 (Top-Left): Step 1: Input & Preprocessing
    tb1 = s10.shapes[14]
    tb1.left = box1_left + Inches(0.35)
    tb1.top = box1_top + Inches(0.35)
    tb1.width = box1_w - Inches(0.70)
    tb1.height = box1_h - Inches(0.70)
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    while len(tf1.paragraphs) > 0:
        p_rem = tf1.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p1_0 = tf1.add_paragraph()
    p1_0.text = "Step 1: Input & Preprocessing"
    p1_0.font.name = "Segoe UI"
    p1_0.font.size = Pt(21)
    p1_0.font.bold = True
    p1_0.font.color.rgb = c_navy
    p1_0.space_after = Pt(10)
    
    p1_1 = tf1.add_paragraph()
    p1_1.text = "Original Text:"
    p1_1.font.name = "Segoe UI"
    p1_1.font.size = Pt(15)
    p1_1.font.bold = True
    p1_1.font.color.rgb = c_navy
    p1_1.space_after = Pt(3)
    
    p1_2 = tf1.add_paragraph()
    p1_2.text = '"Apple unveils new M3 MacBook with ultra-fast processor. The laptop delivers 22-hour battery life."'
    p1_2.font.name = "Segoe UI"
    p1_2.font.size = Pt(14)
    p1_2.font.italic = True
    p1_2.font.color.rgb = c_slate
    p1_2.space_after = Pt(14)
    
    p1_3 = tf1.add_paragraph()
    p1_3.text = "After Cleaning (Tokenized & Lemmatized):"
    p1_3.font.name = "Segoe UI"
    p1_3.font.size = Pt(15)
    p1_3.font.bold = True
    p1_3.font.color.rgb = c_navy
    p1_3.space_after = Pt(4)
    
    p1_4 = tf1.add_paragraph()
    p1_4.text = '["apple", "unveil", "new", "m3", "macbook", "ultra-fast", "processor", "laptop", "deliver", "battery", "life"]'
    p1_4.font.name = "Consolas"
    p1_4.font.size = Pt(13)
    p1_4.font.bold = True
    p1_4.font.color.rgb = c_indigo
    
    # 5. Text for Box 2 (Top-Right): Step 2: TF-IDF Vectorization
    tb2 = None
    for shp in s10.shapes:
        if shp.name == "Card2_Text":
            tb2 = shp
            break
    if not tb2:
        tb2 = s10.shapes.add_textbox(box2_left + Inches(0.35), box2_top + Inches(0.35), box2_w - Inches(0.70), box2_h - Inches(0.70))
        tb2.name = "Card2_Text"
    else:
        tb2.left = box2_left + Inches(0.35)
        tb2.top = box2_top + Inches(0.35)
        tb2.width = box2_w - Inches(0.70)
        tb2.height = box2_h - Inches(0.70)
        
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    while len(tf2.paragraphs) > 0:
        p_rem = tf2.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p2_0 = tf2.add_paragraph()
    p2_0.text = "Step 2: TF-IDF Vectorization"
    p2_0.font.name = "Segoe UI"
    p2_0.font.size = Pt(21)
    p2_0.font.bold = True
    p2_0.font.color.rgb = c_navy
    p2_0.space_after = Pt(10)
    
    p2_1 = tf2.add_paragraph()
    p2_1.text = "The Math: The model converts these words into a 10,000-dimensional math vector."
    p2_1.font.name = "Segoe UI"
    p2_1.font.size = Pt(14)
    p2_1.font.color.rgb = c_slate
    p2_1.space_after = Pt(10)
    
    p2_2 = tf2.add_paragraph()
    p2_2.text = 'TF (Term Frequency): The word "apple" appears 1 time.'
    p2_2.font.name = "Segoe UI"
    p2_2.font.size = Pt(14)
    p2_2.font.color.rgb = c_slate
    p2_2.space_after = Pt(10)
    
    p2_3 = tf2.add_paragraph()
    p2_3.text = 'IDF (Inverse Document Frequency): The word "apple" is rare in general news, but highly common in Tech news. Therefore, it gets a massive math weight.'
    p2_3.font.name = "Segoe UI"
    p2_3.font.size = Pt(14)
    p2_3.font.color.rgb = c_slate
    
    # 6. Text for Box 3 (Bottom-Left): Step 3: Linear SVM Classification
    tb3 = None
    for shp in s10.shapes:
        if shp.name == "Card3_Text":
            tb3 = shp
            break
    if not tb3:
        tb3 = s10.shapes.add_textbox(box3_left + Inches(0.35), box3_top + Inches(0.35), box3_w - Inches(0.70), box3_h - Inches(0.70))
        tb3.name = "Card3_Text"
    else:
        tb3.left = box3_left + Inches(0.35)
        tb3.top = box3_top + Inches(0.35)
        tb3.width = box3_w - Inches(0.70)
        tb3.height = box3_h - Inches(0.70)
        
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    while len(tf3.paragraphs) > 0:
        p_rem = tf3.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p3_0 = tf3.add_paragraph()
    p3_0.text = "Step 3: Linear SVM Classification"
    p3_0.font.name = "Segoe UI"
    p3_0.font.size = Pt(21)
    p3_0.font.bold = True
    p3_0.font.color.rgb = c_navy
    p3_0.space_after = Pt(10)
    
    p3_1 = tf3.add_paragraph()
    p3_1.text = "The Math: The SVM calculates: (Word Weight) × (SVM Category Score)."
    p3_1.font.name = "Consolas"
    p3_1.font.size = Pt(13.5)
    p3_1.font.bold = True
    p3_1.font.color.rgb = c_indigo
    p3_1.space_after = Pt(10)
    
    p3_2 = tf3.add_paragraph()
    p3_2.text = 'It sees strong Tech words like "m3", "macbook", and "processor".'
    p3_2.font.name = "Segoe UI"
    p3_2.font.size = Pt(14)
    p3_2.font.color.rgb = c_slate
    p3_2.space_after = Pt(10)
    
    p3_3 = tf3.add_paragraph()
    p3_3.text = "It calculates a probability distribution:"
    p3_3.font.name = "Segoe UI"
    p3_3.font.size = Pt(14)
    p3_3.font.bold = True
    p3_3.font.color.rgb = c_navy
    p3_3.space_after = Pt(4)
    
    p3_4 = tf3.add_paragraph()
    p3_4.text = "Tech (97.7%) vs. Business (0.4%) vs. Sport (0.2%)."
    p3_4.font.name = "Consolas"
    p3_4.font.size = Pt(15)
    p3_4.font.bold = True
    p3_4.font.color.rgb = c_emerald
    
    # 7. Text for Box 4 (Bottom-Right): Step 4: Live Model Prediction
    tb4 = s10.shapes[15]
    tb4.left = box4_left + Inches(0.35)
    tb4.top = box4_top + Inches(0.35)
    tb4.width = box4_w - Inches(0.70)
    tb4.height = box4_h - Inches(0.70)
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    while len(tf4.paragraphs) > 0:
        p_rem = tf4.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p4_0 = tf4.add_paragraph()
    p4_0.text = "Step 4: Live Model Prediction"
    p4_0.font.name = "Segoe UI"
    p4_0.font.size = Pt(21)
    p4_0.font.bold = True
    p4_0.font.color.rgb = c_navy
    p4_0.space_after = Pt(8)
    
    p4_1 = tf4.add_paragraph()
    p4_1.text = "All 4 models evaluate the text simultaneously:"
    p4_1.font.name = "Segoe UI"
    p4_1.font.size = Pt(14)
    p4_1.font.bold = True
    p4_1.font.color.rgb = c_slate
    p4_1.space_after = Pt(6)
    
    p4_m1 = tf4.add_paragraph()
    p4_m1.text = "⭐ Linear SVM: Tech (97.7%) [Champion]"
    p4_m1.font.name = "Segoe UI"
    p4_m1.font.size = Pt(15)
    p4_m1.font.bold = True
    p4_m1.font.color.rgb = c_emerald
    p4_m1.space_after = Pt(3)
    
    p4_m2 = tf4.add_paragraph()
    p4_m2.text = "• DistilBERT: Tech (97.8%)"
    p4_m2.font.name = "Segoe UI"
    p4_m2.font.size = Pt(14)
    p4_m2.font.color.rgb = c_slate
    p4_m2.space_after = Pt(3)
    
    p4_m3 = tf4.add_paragraph()
    p4_m3.text = "• Neural MLP: Tech (95.1%)"
    p4_m3.font.name = "Segoe UI"
    p4_m3.font.size = Pt(14)
    p4_m3.font.color.rgb = c_slate
    p4_m3.space_after = Pt(3)
    
    p4_m4 = tf4.add_paragraph()
    p4_m4.text = "• Naive Bayes: Tech (92.1%)"
    p4_m4.font.name = "Segoe UI"
    p4_m4.font.size = Pt(14)
    p4_m4.font.color.rgb = c_slate
    p4_m4.space_after = Pt(10)
    
    p4_res = tf4.add_paragraph()
    p4_res.text = "✔ Result: 100% consensus across all architectures."
    p4_res.font.name = "Segoe UI"
    p4_res.font.size = Pt(14)
    p4_res.font.bold = True
    p4_res.font.color.rgb = c_indigo
    
    # 8. Speaker Notes
    try:
        notes_slide = s10.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = (
            "Here is the mathematical progression across our 4-stage pipeline. "
            "In Step 1, we take the raw Apple M3 MacBook text, strip noise, and lemmatize words like 'delivers' into 'deliver'. "
            "In Step 2, TF-IDF vectorization assigns weights—because 'apple' is rare across general news but frequent in tech, it receives a high discriminative weight. "
            "In Step 3, our Linear SVM takes these word weights and multiplies them against the hyperplane category scores, finding an overwhelming 97.7% probability for Technology. "
            "Finally, in Step 4, all 4 of our tested models evaluate the text simultaneously and reach 100% consensus that this is Technology news."
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
