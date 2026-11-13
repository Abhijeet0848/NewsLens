import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide11():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    screenshot_path = "docs/slide11_ui_screenshot.png"
    
    # Verify screenshot exists
    if not os.path.exists(screenshot_path):
        import generate_ui_screenshot
        generate_ui_screenshot.generate_ui_screenshot()

    # Apply to both presentations
    for target_path in [alt_path, pptx_path]:
        try:
            prs = Presentation(target_path)
        except Exception as e:
            print(f"Cannot open {target_path}: {e}")
            continue
            
        s11 = prs.slides[10]
        
        # Colors
        c_navy = RGBColor(15, 23, 42)          # Slate 900 (#0F172A)
        c_slate = RGBColor(100, 116, 139)      # Slate 500 (#64748B)
        c_tech_green = RGBColor(5, 150, 105)   # Emerald 600 (#059669) - Vibrant Green for TECHNOLOGY
        c_indigo = RGBColor(79, 70, 229)       # Electric Indigo (#4F46E5)
        c_border = RGBColor(203, 213, 225)     # Slate 300
        
        # 1. Clean up unused leftover floating text boxes (shapes 0 through 7)
        for idx in range(8):
            if idx < len(s11.shapes):
                s11.shapes[idx].left = Inches(-20)
                
        # Also clean up old shape 12 (TextBox 7) if it had the old small text
        if len(s11.shapes) > 12 and s11.shapes[12].name != "Slide11_UIScreenshot":
            s11.shapes[12].left = Inches(-20)
            
        # 2. Main Title & Massive TECHNOLOGY Headline: Shape 10 (TextBox 2)
        title_shp = s11.shapes[10]
        title_shp.left = Inches(1.80)
        title_shp.top = Inches(0.40)
        title_shp.width = Inches(16.40)
        title_shp.height = Inches(1.70)
        
        tf_title = title_shp.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = Inches(0.10)
        tf_title.margin_top = Inches(0.05)
        tf_title.margin_right = Inches(0.10)
        tf_title.margin_bottom = Inches(0.05)
        
        while len(tf_title.paragraphs) > 0:
            p_rem = tf_title.paragraphs[-1]._p
            p_rem.getparent().remove(p_rem)
            
        # Paragraph 0: Subtitle / Stage indicator
        p0 = tf_title.add_paragraph()
        p0.text = "THE LIVE EXAMPLE: STEP 4 — FINAL CLASSIFICATION RESULT"
        p0.alignment = PP_ALIGN.LEFT
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = c_indigo
        p0.space_after = Pt(2)
        
        # Paragraph 1: Massive "TECHNOLOGY (97.7% Calibrated Confidence)"
        p1 = tf_title.add_paragraph()
        p1.alignment = PP_ALIGN.LEFT
        p1.space_after = Pt(2)
        
        run_label = p1.add_run()
        run_label.text = "Predicted Category: "
        run_label.font.name = "Segoe UI"
        run_label.font.size = Pt(26)
        run_label.font.bold = True
        run_label.font.color.rgb = c_navy
        
        run_tech = p1.add_run()
        run_tech.text = "TECHNOLOGY"
        run_tech.font.name = "Segoe UI"
        run_tech.font.size = Pt(36)
        run_tech.font.bold = True
        run_tech.font.color.rgb = c_tech_green # Vibrant Emerald Green!
        
        run_conf = p1.add_run()
        run_conf.text = "  (97.7% Calibrated Confidence)"
        run_conf.font.name = "Segoe UI"
        run_conf.font.size = Pt(24)
        run_conf.font.bold = True
        run_conf.font.color.rgb = c_navy
        
        # Paragraph 2: Sub-badges line
        p2 = tf_title.add_paragraph()
        p2.text = "⚡ Latency: 1.20 ms   |   ✔ Verified Confidence (>80%)   |   Zero Data Leakage Pipeline"
        p2.alignment = PP_ALIGN.LEFT
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(13.5)
        p2.font.bold = True
        p2.font.color.rgb = c_slate
        
        # 3. Outer Frame Box: Shape 11 (Rectangle: Rounded Corners 3)
        box_shp = s11.shapes[11]
        box_shp.left = Inches(1.80)
        box_shp.top = Inches(2.25)
        box_shp.width = Inches(16.40)
        box_shp.height = Inches(8.55)
        box_shp.fill.solid()
        box_shp.fill.fore_color.rgb = RGBColor(255, 255, 255) # Clean White
        box_shp.line.color.rgb = c_border
        box_shp.line.width = Pt(1.5)
        
        # 4. Add UI Screenshot inside the Box
        # Hide any previous picture instances
        for shp in s11.shapes:
            if shp.name == "Slide11_UIScreenshot":
                shp.left = Inches(-20)
                
        # Insert new picture with perfect margin inside the rounded box
        pic_left = Inches(1.95)
        pic_top = Inches(2.40)
        pic_w = Inches(16.10)
        pic_h = Inches(8.25)
        
        pic_shp = s11.shapes.add_picture(screenshot_path, pic_left, pic_top, pic_w, pic_h)
        pic_shp.name = "Slide11_UIScreenshot"
        
        # 5. Speaker Notes
        try:
            notes_slide = s11.notes_slide
            tf_notes = notes_slide.notes_text_frame
            tf_notes.text = (
                "And here is the live culmination of the entire pipeline—our production NewsScope application interface. "
                "Notice the massive result at the top: our Linear SVM classified this article into Technology with 97.7% calibrated confidence in only 1.20 milliseconds! "
                "Because our confidence exceeds the strict 80% threshold, the system displays the green 'Verified' badge and automatically routes the story to the Technology desk without human bottleneck. "
                "Furthermore, look at the explainability cards below: 'processor' and 'macbook' contributed over 65% of the decision weight, providing full auditability for news editors."
            )
            print(f"Speaker notes added to Slide 11 in {target_path}")
        except Exception as e:
            print(f"Notes warning in {target_path}: {e}")
            
        try:
            prs.save(target_path)
            print(f"Slide 11 successfully saved to {target_path}!")
        except Exception as e:
            print(f"Error saving to {target_path}: {e}")

if __name__ == "__main__":
    update_slide11()
