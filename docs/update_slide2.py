import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide2():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(pptx_path)
    s2 = prs.slides[1]
    
    items = [
        (2, 3, 4, "The Problem"),
        (5, 6, 7, "Proposed Solution"),
        (8, 9, 10, "How It Is Built (Architecture)"),
        (11, 12, 13, "5-Step Text Preprocessing"),
        (14, 15, 16, "The 4 AI Models Tested"),
        (17, 18, 19, "Step-by-Step Live Example"),
        (20, 21, 22, "Test Results & Accuracy"),
        (23, 24, 25, "Future Plans & Conclusion")
    ]
    
    bullet_left = Inches(7.10)
    bullet_size = Inches(0.18)
    text_left = Inches(7.45)
    text_width = Inches(4.75)
    num_left = Inches(12.30)
    num_width = Inches(0.65)
    
    bullet_color = RGBColor(99, 102, 241) # Modern electric indigo (#6366F1)
    
    for arrow_idx, text_idx, num_idx, new_text in items:
        # 1. Update Text
        t_shp = s2.shapes[text_idx]
        t_shp.text_frame.paragraphs[0].text = new_text
        t_shp.left = text_left
        t_shp.width = text_width
        
        # 2. Update Number Position (bring closer to text)
        n_shp = s2.shapes[num_idx]
        n_shp.left = num_left
        n_shp.width = num_width
        
        # 3. Replace large distracting blue arrow with clean small bullet dot
        a_shp = s2.shapes[arrow_idx]
        # Move old arrow off-slide
        a_shp.left = Inches(-20)
        
        # Add a sleek, perfectly aligned small bullet circle
        b_top = t_shp.top + (t_shp.height - bullet_size) / 2
        bullet = s2.shapes.add_shape(
            MSO_SHAPE.OVAL,
            bullet_left, b_top, bullet_size, bullet_size
        )
        bullet.fill.solid()
        bullet.fill.fore_color.rgb = bullet_color
        bullet.line.fill.background() # No border line
        
    prs.save(pptx_path)
    prs.save(alt_path)
    print("Slide 2 updated successfully in both files!")

if __name__ == "__main__":
    update_slide2()
