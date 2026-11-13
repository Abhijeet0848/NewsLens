import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide12():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    # Colors
    c_navy = RGBColor(15, 23, 42)          # Slate 900 (#0F172A)
    c_slate = RGBColor(51, 65, 85)         # Slate 700 (#334155)
    c_indigo = RGBColor(79, 70, 229)       # Electric Indigo (#4F46E5)
    c_card_bg = RGBColor(248, 250, 252)    # Slate 50 (#F8FAFC)
    c_border = RGBColor(203, 213, 225)     # Slate 300 (#CBD5E1)

    for target_path in [alt_path, pptx_path]:
        try:
            prs = Presentation(target_path)
        except Exception as e:
            print(f"Cannot open {target_path}: {e}")
            continue
            
        s12 = prs.slides[11]
        
        # Slide 12 has Group 38 as Shape 0
        grp = s12.shapes[0]
        
        # 1. Update Title in TextBox 5: Make it much larger, bold, and centered
        for sub in grp.shapes:
            if sub.name == "TextBox 5":
                sub.left = Inches(3.00)
                sub.top = Inches(0.80)
                sub.width = Inches(14.00)
                sub.height = Inches(1.50)
                
                tf = sub.text_frame
                tf.word_wrap = True
                while len(tf.paragraphs) > 0:
                    p_rem = tf.paragraphs[-1]._p
                    p_rem.getparent().remove(p_rem)
                    
                p0 = tf.add_paragraph()
                p0.text = "Handling Difficult Cases"
                p0.alignment = PP_ALIGN.CENTER
                p0.font.name = "Segoe UI"
                p0.font.size = Pt(36)
                p0.font.bold = True
                p0.font.color.rgb = c_navy
                p0.space_after = Pt(4)
                
                p1 = tf.add_paragraph()
                p1.text = "Domain Ambiguity Resolution, Robust API Validation & Scalable Batch Ingestion"
                p1.alignment = PP_ALIGN.CENTER
                p1.font.name = "Segoe UI"
                p1.font.size = Pt(17)
                p1.font.bold = True
                p1.font.color.rgb = c_indigo
                break

        # 2. Geometry for the 3 Cards:
        # Shorter height (4.70" instead of 5.69") and balanced layout
        card_w = Inches(4.80)
        card_h = Inches(4.70)
        card_top = Inches(3.20)
        
        c1_left = Inches(1.60)
        c2_left = Inches(7.60)
        c3_left = Inches(13.60)
        
        c1_center = int(c1_left + card_w / 2)
        c2_center = int(c2_left + card_w / 2)
        c3_center = int(c3_left + card_w / 2)
        
        icon_w = Inches(1.00)
        icon_h = Inches(1.00)
        icon_top = Inches(3.55)
        
        tb_w = Inches(4.20)
        title_top = Inches(4.75)
        title_h = Inches(0.55)
        body_top = Inches(5.45)
        body_h = Inches(2.20)
        
        # Update Card 1 Background (Rectangle: Rounded Corners 1)
        for sub in grp.shapes:
            if sub.name == "Rectangle: Rounded Corners 1":
                sub.left = c1_left
                sub.top = card_top
                sub.width = card_w
                sub.height = card_h
                sub.fill.solid()
                sub.fill.fore_color.rgb = c_card_bg
                sub.line.color.rgb = c_border
                sub.line.width = Pt(1.5)
            elif sub.name == "Rectangle: Rounded Corners 2":
                sub.left = c2_left
                sub.top = card_top
                sub.width = card_w
                sub.height = card_h
                sub.fill.solid()
                sub.fill.fore_color.rgb = c_card_bg
                sub.line.color.rgb = c_border
                sub.line.width = Pt(1.5)
            elif sub.name == "Rectangle: Rounded Corners 3":
                sub.left = c3_left
                sub.top = card_top
                sub.width = card_w
                sub.height = card_h
                sub.fill.solid()
                sub.fill.fore_color.rgb = c_card_bg
                sub.line.color.rgb = c_border
                sub.line.width = Pt(1.5)
                
            # Icons
            elif sub.name == "Graphic 8":
                sub.left = int(c1_center - icon_w / 2)
                sub.top = icon_top
                sub.width = icon_w
                sub.height = icon_h
            elif sub.name == "Graphic 27":
                sub.left = int(c2_center - icon_w / 2)
                sub.top = icon_top
                sub.width = icon_w
                sub.height = icon_h
            elif sub.name == "Graphic 35":
                sub.left = int(c3_center - icon_w / 2)
                sub.top = icon_top
                sub.width = icon_w
                sub.height = icon_h
                
            # Card 1 Title & Body
            elif sub.name == "TextBox 15":
                sub.left = int(c1_center - tb_w / 2)
                sub.top = title_top
                sub.width = tb_w
                sub.height = title_h
                tf = sub.text_frame
                p = tf.paragraphs[0]
                p.text = "Two-Word Clues (Bigrams)"
                p.alignment = PP_ALIGN.CENTER
                p.font.name = "Segoe UI"
                p.font.size = Pt(20)
                p.font.bold = True
                p.font.color.rgb = c_navy
            elif sub.name == "TextBox 16":
                sub.left = int(c1_center - tb_w / 2)
                sub.top = body_top
                sub.width = tb_w
                sub.height = body_h
                tf = sub.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.text = "Politics and Business share words like 'tax'. Teaching the AI phrases like 'tax budget' vs 'corporate tax' fixed the confusion."
                p.alignment = PP_ALIGN.CENTER
                p.font.name = "Segoe UI"
                p.font.size = Pt(15)
                p.font.color.rgb = c_slate
                p.line_spacing = 1.3
                
            # Card 2 Title & Body (with HTTP 422 validation)
            elif sub.name == "TextBox 28":
                sub.left = int(c2_center - tb_w / 2)
                sub.top = title_top
                sub.width = tb_w
                sub.height = title_h
                tf = sub.text_frame
                p = tf.paragraphs[0]
                p.text = "Safe & Protected API"
                p.alignment = PP_ALIGN.CENTER
                p.font.name = "Segoe UI"
                p.font.size = Pt(20)
                p.font.bold = True
                p.font.color.rgb = c_navy
            elif sub.name == "TextBox 33":
                sub.left = int(c2_center - tb_w / 2)
                sub.top = body_top
                sub.width = tb_w
                sub.height = body_h
                tf = sub.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.text = "FastAPI checks all input text immediately (HTTP 422 validation) to make sure nothing crashes or attacks the server."
                p.alignment = PP_ALIGN.CENTER
                p.font.name = "Segoe UI"
                p.font.size = Pt(15)
                p.font.color.rgb = c_slate
                p.line_spacing = 1.3
                
            # Card 3 Title & Body (with 1,000 articles)
            elif sub.name == "TextBox 36":
                sub.left = int(c3_center - tb_w / 2)
                sub.top = title_top
                sub.width = tb_w
                sub.height = title_h
                tf = sub.text_frame
                p = tf.paragraphs[0]
                p.text = "Safe File Uploads"
                p.alignment = PP_ALIGN.CENTER
                p.font.name = "Segoe UI"
                p.font.size = Pt(20)
                p.font.bold = True
                p.font.color.rgb = c_navy
            elif sub.name == "TextBox 37":
                sub.left = int(c3_center - tb_w / 2)
                sub.top = body_top
                sub.width = tb_w
                sub.height = body_h
                tf = sub.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.text = "Users can upload spreadsheets (CSV) with 1,000 articles. The app reads them safely and skips broken rows."
                p.alignment = PP_ALIGN.CENTER
                p.font.name = "Segoe UI"
                p.font.size = Pt(15)
                p.font.color.rgb = c_slate
                p.line_spacing = 1.3

        # 3. Add Speaker Notes to Slide 12
        try:
            notes_slide = s12.notes_slide
            tf_notes = notes_slide.notes_text_frame
            tf_notes.text = (
                "In real-world deployment, machine learning systems face messy data and ambiguous edge cases. Here is how NewsScope handles them: "
                "First, for vocabulary ambiguity—topics like Politics and Business frequently overlap on words like 'tax'. By expanding our TF-IDF pipeline to unigrams plus bigrams, phrases like 'tax budget' and 'corporate tax' eliminate false classifications. "
                "Second, for system resilience—FastAPI provides strict HTTP 422 schema validation, catching empty strings, excessively long payloads, or malicious scripts before they ever touch the model. "
                "Finally, for batch scalability—our batch endpoint processes CSV files with up to 1,000 articles at once, streaming predictions safely while gracefully logging and skipping corrupted rows."
            )
            print(f"Speaker notes added to Slide 12 in {target_path}")
        except Exception as e:
            print(f"Notes warning in {target_path}: {e}")
            
        try:
            prs.save(target_path)
            print(f"Slide 12 successfully updated in {target_path}!")
        except Exception as e:
            print(f"Error saving {target_path}: {e}")

if __name__ == "__main__":
    update_slide12()
