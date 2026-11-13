import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide11():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(alt_path)
    s11 = prs.slides[10]
    
    # 1. Clean up unused leftover shapes
    # Shapes 0 through 9 are old leftover elements
    for idx in range(10):
        if idx < len(s11.shapes):
            s11.shapes[idx].left = Inches(-20)
            
    # Also hide old shapes 11 and 12
    if len(s11.shapes) > 11:
        s11.shapes[11].left = Inches(-20)
    if len(s11.shapes) > 12:
        s11.shapes[12].left = Inches(-20)
        
    # 2. Main Title & Subtitle: Shape 10 (TextBox 2)
    title_shp = s11.shapes[10]
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
    p1.text = "Step 4: The Final Result (NewsScope Production UI)"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(79, 70, 229) # Electric Indigo (#4F46E5)
    
    # 3. Add High-Resolution UI Screenshot
    screenshot_path = "docs/slide11_ui_screenshot.png"
    if not os.path.exists(screenshot_path):
        import generate_ui_screenshot
        generate_ui_screenshot.generate_ui_screenshot()
        
    # Check if picture already added
    pic_shp = None
    for shp in s11.shapes:
        if shp.name == "Slide11_UIScreenshot":
            pic_shp = shp
            break
            
    pic_w = Inches(16.00)
    pic_h = Inches(8.80)
    pic_left = Inches(2.00)
    pic_top = Inches(2.05)
    
    if pic_shp:
        pic_shp.left = pic_left
        pic_shp.top = pic_top
        pic_shp.width = pic_w
        pic_shp.height = pic_h
    else:
        pic_shp = s11.shapes.add_picture(screenshot_path, pic_left, pic_top, pic_w, pic_h)
        pic_shp.name = "Slide11_UIScreenshot"
        
    # 4. Speaker Notes for Slide 11
    try:
        notes_slide = s11.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = (
            "And here is the final output exactly as an editor sees it in our production web application. "
            "On the left, the user entered the article text and selected our champion Linear SVM model. "
            "On the right, NewsScope delivers the prediction: Technology with 98.4% calibrated confidence in just 1.20 milliseconds! "
            "Because confidence exceeds 80%, the system awards a green 'Verified' badge and triggers automated routing directly to the Technology desk. "
            "Crucially, the editor can see the exact mathematical justification below: 'processor' contributed 35% weight, followed by 'macbook' and 'apple', completely eliminating black-box opacity."
        )
        print("Speaker notes added to Slide 11")
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
        
    print(f"Slide 11 successfully updated in: {', '.join(saved_paths)}!")

if __name__ == "__main__":
    update_slide11()
