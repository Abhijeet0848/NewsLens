import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide13():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    # Colors
    c_navy = RGBColor(15, 23, 42)          # Slate 900 (#0F172A)
    c_slate = RGBColor(51, 65, 85)         # Slate 700 (#334155)
    c_indigo = RGBColor(79, 70, 229)       # Electric Indigo (#4F46E5)
    c_emerald = RGBColor(5, 150, 105)      # Emerald 600 (#059669)
    c_card_bg = RGBColor(248, 250, 252)    # Slate 50 (#F8FAFC)
    c_border = RGBColor(203, 213, 225)     # Slate 300 (#CBD5E1)

    for target_path in [alt_path, pptx_path]:
        try:
            prs = Presentation(target_path)
        except Exception as e:
            print(f"Cannot open {target_path}: {e}")
            continue
            
        s13 = prs.slides[12]
        grp = s13.shapes[0]
        
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
                p0.alignment = PP_ALIGN.CENTER
                p0.space_after = Pt(4)
                r0 = p0.add_run()
                r0.text = "Test Results & Accuracy"
                r0.font.name = "Segoe UI"
                r0.font.size = Pt(36)
                r0.font.bold = True
                r0.font.color.rgb = c_navy
                
                p1 = tf.add_paragraph()
                p1.alignment = PP_ALIGN.CENTER
                r1 = p1.add_run()
                r1.text = "Held-Out Evaluation Benchmarks, Per-Domain Breakdown & Efficiency Metrics"
                r1.font.name = "Segoe UI"
                r1.font.size = Pt(17)
                r1.font.bold = True
                r1.font.color.rgb = c_indigo
                break

        # 2. Geometry for the 3 Cards
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
        
        # Update Card Backgrounds
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
                
            # Card 1 Title & Body
            elif sub.name == "TextBox 15":
                sub.left = int(c1_center - tb_w / 2)
                sub.top = title_top
                sub.width = tb_w
                sub.height = title_h
                tf = sub.text_frame
                while len(tf.paragraphs) > 0:
                    p_rem = tf.paragraphs[-1]._p
                    p_rem.getparent().remove(p_rem)
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run()
                r.text = "96.4% Overall Accuracy"
                r.font.name = "Segoe UI"
                r.font.size = Pt(20)
                r.font.bold = True
                r.font.color.rgb = c_navy
                
            elif sub.name == "TextBox 16":
                sub.left = int(c1_center - tb_w / 2)
                sub.top = body_top
                sub.width = tb_w
                sub.height = body_h
                tf = sub.text_frame
                tf.word_wrap = True
                while len(tf.paragraphs) > 0:
                    p_rem = tf.paragraphs[-1]._p
                    p_rem.getparent().remove(p_rem)
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.CENTER
                p.line_spacing = 1.3
                
                r1 = p.add_run()
                r1.text = "Tested on "
                r1.font.name = "Segoe UI"
                r1.font.size = Pt(15)
                r1.font.color.rgb = c_slate
                
                r2 = p.add_run()
                r2.text = "445"
                r2.font.name = "Segoe UI"
                r2.font.size = Pt(15)
                r2.font.bold = True
                r2.font.color.rgb = c_navy
                
                r3 = p.add_run()
                r3.text = " brand new, unseen BBC articles. It got "
                r3.font.name = "Segoe UI"
                r3.font.size = Pt(15)
                r3.font.color.rgb = c_slate
                
                r4 = p.add_run()
                r4.text = "429"
                r4.font.name = "Segoe UI"
                r4.font.size = Pt(15)
                r4.font.bold = True
                r4.font.color.rgb = c_emerald
                
                r5 = p.add_run()
                r5.text = " correct and made only "
                r5.font.name = "Segoe UI"
                r5.font.size = Pt(15)
                r5.font.color.rgb = c_slate
                
                r6 = p.add_run()
                r6.text = "16"
                r6.font.name = "Segoe UI"
                r6.font.size = Pt(15)
                r6.font.bold = True
                r6.font.color.rgb = c_navy
                
                r7 = p.add_run()
                r7.text = " small mistakes."
                r7.font.name = "Segoe UI"
                r7.font.size = Pt(15)
                r7.font.color.rgb = c_slate
                
            # Card 2 Title & Body (Bold stats: 99.0%, 96.1%, 94.0%)
            elif sub.name == "TextBox 28":
                sub.left = int(c2_center - tb_w / 2)
                sub.top = title_top
                sub.width = tb_w
                sub.height = title_h
                tf = sub.text_frame
                while len(tf.paragraphs) > 0:
                    p_rem = tf.paragraphs[-1]._p
                    p_rem.getparent().remove(p_rem)
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run()
                r.text = "Scores by Category"
                r.font.name = "Segoe UI"
                r.font.size = Pt(20)
                r.font.bold = True
                r.font.color.rgb = c_navy
                
            elif sub.name == "TextBox 33":
                sub.left = int(c2_center - tb_w / 2)
                sub.top = body_top
                sub.width = tb_w
                sub.height = body_h
                tf = sub.text_frame
                tf.word_wrap = True
                while len(tf.paragraphs) > 0:
                    p_rem = tf.paragraphs[-1]._p
                    p_rem.getparent().remove(p_rem)
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.CENTER
                p.line_spacing = 1.3
                
                r1 = p.add_run()
                r1.text = "Sport was easiest at "
                r1.font.name = "Segoe UI"
                r1.font.size = Pt(15)
                r1.font.color.rgb = c_slate
                
                r2 = p.add_run()
                r2.text = "99.0%"
                r2.font.name = "Segoe UI"
                r2.font.size = Pt(15)
                r2.font.bold = True
                r2.font.color.rgb = c_emerald
                
                r3 = p.add_run()
                r3.text = ". Entertainment was "
                r3.font.name = "Segoe UI"
                r3.font.size = Pt(15)
                r3.font.color.rgb = c_slate
                
                r4 = p.add_run()
                r4.text = "96.1%"
                r4.font.name = "Segoe UI"
                r4.font.size = Pt(15)
                r4.font.bold = True
                r4.font.color.rgb = c_indigo
                
                r5 = p.add_run()
                r5.text = ". Politics was "
                r5.font.name = "Segoe UI"
                r5.font.size = Pt(15)
                r5.font.color.rgb = c_slate
                
                r6 = p.add_run()
                r6.text = "94.0%"
                r6.font.name = "Segoe UI"
                r6.font.size = Pt(15)
                r6.font.bold = True
                r6.font.color.rgb = c_navy
                
                r7 = p.add_run()
                r7.text = " due to overlapping economic words."
                r7.font.name = "Segoe UI"
                r7.font.size = Pt(15)
                r7.font.color.rgb = c_slate
                
            # Card 3 Title & Body (Bold stats: 1.2 milliseconds, 10 times faster, 20 times less memory)
            elif sub.name == "TextBox 36":
                sub.left = int(c3_center - tb_w / 2)
                sub.top = title_top
                sub.width = tb_w
                sub.height = title_h
                tf = sub.text_frame
                while len(tf.paragraphs) > 0:
                    p_rem = tf.paragraphs[-1]._p
                    p_rem.getparent().remove(p_rem)
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.CENTER
                r = p.add_run()
                r.text = "10x Faster Speed"
                r.font.name = "Segoe UI"
                r.font.size = Pt(20)
                r.font.bold = True
                r.font.color.rgb = c_navy
                
            elif sub.name == "TextBox 37":
                sub.left = int(c3_center - tb_w / 2)
                sub.top = body_top
                sub.width = tb_w
                sub.height = body_h
                tf = sub.text_frame
                tf.word_wrap = True
                while len(tf.paragraphs) > 0:
                    p_rem = tf.paragraphs[-1]._p
                    p_rem.getparent().remove(p_rem)
                p = tf.add_paragraph()
                p.alignment = PP_ALIGN.CENTER
                p.line_spacing = 1.3
                
                r1 = p.add_run()
                r1.text = "Runs in "
                r1.font.name = "Segoe UI"
                r1.font.size = Pt(15)
                r1.font.color.rgb = c_slate
                
                r2 = p.add_run()
                r2.text = "1.2 milliseconds"
                r2.font.name = "Segoe UI"
                r2.font.size = Pt(15)
                r2.font.bold = True
                r2.font.color.rgb = c_emerald
                
                r3 = p.add_run()
                r3.text = ". It is "
                r3.font.name = "Segoe UI"
                r3.font.size = Pt(15)
                r3.font.color.rgb = c_slate
                
                r4 = p.add_run()
                r4.text = "10 times faster"
                r4.font.name = "Segoe UI"
                r4.font.size = Pt(15)
                r4.font.bold = True
                r4.font.color.rgb = c_indigo
                
                r5 = p.add_run()
                r5.text = " than deep learning models and takes "
                r5.font.name = "Segoe UI"
                r5.font.size = Pt(15)
                r5.font.color.rgb = c_slate
                
                r6 = p.add_run()
                r6.text = "20 times less memory"
                r6.font.name = "Segoe UI"
                r6.font.size = Pt(15)
                r6.font.bold = True
                r6.font.color.rgb = c_navy
                
                r7 = p.add_run()
                r7.text = "."
                r7.font.name = "Segoe UI"
                r7.font.size = Pt(15)
                r7.font.color.rgb = c_slate

        # 3. Center the 3 picture icons (Shapes 1, 2, 3 outside Group 38)
        for shp in s13.shapes:
            if shp.name == "Graphic 10":
                shp.left = int(c1_center - icon_w / 2)
                shp.top = icon_top
                shp.width = icon_w
                shp.height = icon_h
            elif shp.name == "Graphic 17":
                shp.left = int(c2_center - icon_w / 2)
                shp.top = icon_top
                shp.width = icon_w
                shp.height = icon_h
            elif shp.name == "Graphic 25":
                shp.left = int(c3_center - icon_w / 2)
                shp.top = icon_top
                shp.width = icon_w
                shp.height = icon_h

        # 4. Speaker Notes for Slide 13
        try:
            notes_slide = s13.notes_slide
            tf_notes = notes_slide.notes_text_frame
            tf_notes.text = (
                "Turning to empirical evaluation, here are our benchmark results on the BBC held-out test split: "
                "First, overall predictive accuracy—our Linear SVM achieved 96.4% accuracy across 445 unseen test articles, getting 429 exactly right with only 16 edge-case errors. "
                "Second, performance by domain—Sport proved easiest at 99.0% F1-score due to distinct athletic vocabulary. Entertainment reached 96.1%, while Politics scored 94.0% due to occasional semantic overlap with business and fiscal reporting. "
                "Third, computational efficiency—with an inference latency of just 1.2 milliseconds, our pipeline runs over 10 times faster than transformer models like DistilBERT and consumes 20 times less memory, making real-time CPU deployment seamless."
            )
            print(f"Speaker notes added to Slide 13 in {target_path}")
        except Exception as e:
            print(f"Notes warning in {target_path}: {e}")
            
        try:
            prs.save(target_path)
            print(f"Slide 13 successfully updated in {target_path}!")
        except Exception as e:
            print(f"Error saving {target_path}: {e}")

if __name__ == "__main__":
    update_slide13()
