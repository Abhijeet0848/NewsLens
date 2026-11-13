import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide9():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(pptx_path)
    s9 = prs.slides[8]
    
    # 1. Clean up unused leftover shapes 1 through 7
    for idx in range(1, 8):
        s9.shapes[idx].left = Inches(-20)
        
    # 2. Main Title & Subtitle: "The Live Example: Step-by-Step" + "Step 1: The Raw Input"
    title_shp = s9.shapes[0]
    title_shp.left = Inches(3.00)
    title_shp.top = Inches(0.80)
    title_shp.width = Inches(14.00)
    title_shp.height = Inches(1.40)
    
    tf_title = title_shp.text_frame
    tf_title.word_wrap = True
    
    # Paragraph 0: Main Title
    p0 = tf_title.paragraphs[0]
    p0.text = "The Live Example: Step-by-Step"
    p0.alignment = PP_ALIGN.CENTER
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(38)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    p0.space_after = Pt(6)
    
    # Paragraph 1: Subtitle
    while len(tf_title.paragraphs) > 1:
        p_rem = tf_title.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    p1 = tf_title.add_paragraph()
    p1.text = "Step 1: The Raw Input"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(21)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(79, 70, 229) # Electric Indigo (#4F46E5)
    
    # 3. Card Container (Shape 10)
    card_shp = s9.shapes[10]
    card_shp.left = Inches(5.00)
    card_shp.top = Inches(2.65)
    card_shp.width = Inches(10.00)
    card_shp.height = Inches(6.50)
    card_shp.fill.solid()
    card_shp.fill.fore_color.rgb = RGBColor(248, 250, 252) # Soft Slate 50 (#F8FAFC)
    card_shp.line.color.rgb = RGBColor(203, 213, 225)      # Subtle Slate 300 border
    card_shp.line.width = Pt(1.5)
    
    # 4. Heading with 📄 Icon (Shape 11)
    heading_shp = s9.shapes[11]
    heading_shp.left = Inches(5.40)
    heading_shp.top = Inches(3.15)
    heading_shp.width = Inches(9.20)
    heading_shp.height = Inches(0.75)
    
    tf_h = heading_shp.text_frame
    p_h = tf_h.paragraphs[0]
    p_h.text = "📄  Original Text"
    p_h.alignment = PP_ALIGN.CENTER
    p_h.font.name = "Segoe UI Emoji"
    p_h.font.size = Pt(24)
    p_h.font.bold = True
    p_h.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy
    
    # 5. Clean Single Paragraph Text without Quotation Marks (Shape 12)
    body_shp = s9.shapes[12]
    body_shp.left = Inches(5.60)
    body_shp.top = Inches(4.30)
    body_shp.width = Inches(8.80)
    body_shp.height = Inches(4.00)
    
    tf_b = body_shp.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = Inches(0.30)
    tf_b.margin_right = Inches(0.30)
    tf_b.margin_top = Inches(0.20)
    tf_b.margin_bottom = Inches(0.20)
    
    # Clear all paragraphs and set single clean paragraph
    while len(tf_b.paragraphs) > 1:
        p_rem = tf_b.paragraphs[-1]._p
        p_rem.getparent().remove(p_rem)
        
    pb = tf_b.paragraphs[0]
    pb.text = "Apple unveils new M3 MacBook laptop with ultra-fast processor. The laptop delivers 22-hour battery life and high performance graphics. Developers can build machine learning applications seamlessly."
    pb.alignment = PP_ALIGN.LEFT
    pb.font.name = "Segoe UI"
    pb.font.size = Pt(21)
    pb.font.bold = False
    pb.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
    pb.line_spacing = 1.45
    
    # 6. Speaker Notes (Presenter Script)
    try:
        notes_slide = s9.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = (
            "To show you exactly how the AI works, let's walk through a real example step-by-step. "
            "Imagine a user pastes this short article about the new Apple M3 MacBook. "
            "We can clearly see it's about Technology. But to the computer, this is just a long string of characters. "
            "So, how does it figure it out? Let's move to the next step."
        )
        print("Speaker notes added to Slide 9")
    except Exception as e:
        print(f"Notes note added: {e}")
        
    # Save with fallback if PowerPoint locks NewsScope_Presentation.pptx
    saved_paths = []
    try:
        prs.save(pptx_path)
        saved_paths.append(pptx_path)
    except PermissionError:
        print(f"Notice: {pptx_path} is currently open in PowerPoint (locked).")
        
    try:
        prs.save(alt_path)
        saved_paths.append(alt_path)
    except PermissionError:
        print(f"Notice: {alt_path} is currently open in PowerPoint (locked).")
        
    if not saved_paths:
        fallback = "docs/NewsScope_Presentation_Latest.pptx"
        prs.save(fallback)
        saved_paths.append(fallback)
        
    print(f"Slide 9 updated successfully in: {', '.join(saved_paths)}!")

if __name__ == "__main__":
    update_slide9()
