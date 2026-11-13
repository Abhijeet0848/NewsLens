import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_presentation():
    pptx_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    output_path = "docs/NewsScope_Presentation.pptx"
    
    prs = Presentation(pptx_path)
    s1 = prs.slides[0]
    
    # 1. Inspect existing shapes on slide 1
    # Move old picture (shape 4) off slide
    for shape in s1.shapes:
        if shape.shape_type == 13: # Picture
            shape.left = Inches(-20)
            
    # Position NEWSCOPE shape
    title_shape = None
    for shape in s1.shapes:
        if shape.has_text_frame and "NEWSCOPE" in shape.text_frame.text:
            title_shape = shape
            break
            
    # Set Logo Icon next to title
    # We will use the simple newspaper icon or the brand squircle icon
    icon_path = "docs/newspaper_simple_icon.png"
    if not os.path.exists(icon_path):
        icon_path = "public/logo-icon.png"
        
    # Place Icon at left=7.30", top=2.40", w=1.15", h=1.15"
    logo_img = s1.shapes.add_picture(
        icon_path,
        left=Inches(7.30),
        top=Inches(2.40),
        width=Inches(1.15),
        height=Inches(1.15)
    )
    
    if title_shape:
        title_shape.left = Inches(8.60)
        title_shape.top = Inches(2.62)
        title_shape.width = Inches(4.30)
        title_shape.height = Inches(0.75)
        # Ensure left-aligned with icon
        p = title_shape.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        p.font.bold = True
        
    # 2. Add the 3 Tech Badges at the bottom
    badges_data = [
        ("Next.js", Inches(5.90), RGBColor(241, 245, 249), RGBColor(148, 163, 184), RGBColor(15, 23, 42)),
        ("FastAPI", Inches(8.70), RGBColor(236, 253, 245), RGBColor(52, 211, 153), RGBColor(5, 150, 105)),
        ("Scikit-Learn", Inches(11.50), RGBColor(238, 242, 255), RGBColor(129, 140, 248), RGBColor(67, 56, 202))
    ]
    
    badge_top = Inches(8.35)
    badge_height = Inches(0.62)
    
    for label, b_left, bg_col, border_col, text_col in badges_data:
        b_width = Inches(2.80) if "Scikit" in label else Inches(2.40)
        badge = s1.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            b_left, badge_top, b_width, badge_height
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = bg_col
        badge.line.color.rgb = border_col
        badge.line.width = Pt(1.5)
        
        tf = badge.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = f"[{label}]"
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Segoe UI"
        p.font.size = Pt(17)
        p.font.bold = True
        p.font.color.rgb = text_col
        
    # Also save to both files
    try:
        prs.save(output_path)
        print(f"Saved successfully to {output_path}")
    except PermissionError:
        print(f"Could not write {output_path} (locked by PowerPoint)")
        
    prs.save(pptx_path)
    print(f"Saved successfully to {pptx_path}")

if __name__ == "__main__":
    update_presentation()
