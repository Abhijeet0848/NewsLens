import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide5():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(pptx_path)
    s5 = prs.slides[4]
    
    # 1. Subtitle Visibility: "The NewsScope Solution" at the top -> White text on dark blue
    header_shp = s5.shapes[8]
    tf_hdr = header_shp.text_frame
    p_hdr = tf_hdr.paragraphs[0]
    p_hdr.text = "The NewsScope Solution"
    p_hdr.alignment = PP_ALIGN.CENTER
    p_hdr.font.name = "Segoe UI"
    p_hdr.font.size = Pt(36)
    p_hdr.font.bold = True
    p_hdr.font.color.rgb = RGBColor(255, 255, 255) # Pure White
    
    # 2. Card 1 (Document Icon - Shape 17)
    # Title (Shape 11): Shows Its Work (Explainability)
    # Desc  (Shape 14): Extracts the exact words that caused the decision (e.g., 'Wembley' = 28%). It provides an honest confidence score so editors can trust the AI.
    t1_shp = s5.shapes[11]
    t1_shp.left = Inches(1.35)
    t1_shp.top = Inches(6.30)
    t1_shp.width = Inches(4.20)
    t1_shp.height = Inches(0.85)
    p1 = t1_shp.text_frame.paragraphs[0]
    p1.text = "Shows Its Work (Explainability)"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy
    
    d1_shp = s5.shapes[14]
    d1_shp.left = Inches(0.80)
    d1_shp.top = Inches(7.20)
    d1_shp.width = Inches(5.30)
    d1_shp.height = Inches(1.20)
    d1_shp.text_frame.word_wrap = True
    pd1 = d1_shp.text_frame.paragraphs[0]
    pd1.text = "Extracts the exact words that caused the decision (e.g., 'Wembley' = 28%). It provides an honest confidence score so editors can trust the AI."
    pd1.alignment = PP_ALIGN.CENTER
    pd1.font.name = "Segoe UI"
    pd1.font.size = Pt(16)
    pd1.font.bold = False
    pd1.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
    
    # 3. Card 2 (Checkmark Icon - Shape 19)
    # Title (Shape 12): High Accuracy (96.4%)
    # Desc  (Shape 9): Draws a clear mathematical dividing line between news topics. It reaches 96.4% accuracy without needing big, expensive supercomputers.
    t2_shp = s5.shapes[12]
    t2_shp.left = Inches(7.90)
    t2_shp.top = Inches(6.30)
    t2_shp.width = Inches(4.20)
    t2_shp.height = Inches(0.85)
    p2 = t2_shp.text_frame.paragraphs[0]
    p2.text = "High Accuracy (96.4%)"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy
    
    d2_shp = s5.shapes[9]
    d2_shp.left = Inches(7.35)
    d2_shp.top = Inches(7.20)
    d2_shp.width = Inches(5.30)
    d2_shp.height = Inches(1.20)
    d2_shp.text_frame.word_wrap = True
    pd2 = d2_shp.text_frame.paragraphs[0]
    pd2.text = "Draws a clear mathematical dividing line between news topics. It reaches 96.4% accuracy without needing big, expensive supercomputers."
    pd2.alignment = PP_ALIGN.CENTER
    pd2.font.name = "Segoe UI"
    pd2.font.size = Pt(16)
    pd2.font.bold = False
    pd2.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
    
    # 4. Card 3 (Lightning Icon - Shape 18)
    # Title (Shape 13): Ultra-Fast Speed (1.2 ms)
    # Desc  (Shape 10): Uses a strict zero data leakage pipeline. It sorts articles in just 1.2 milliseconds, allowing instant news updates on a normal laptop.
    t3_shp = s5.shapes[13]
    t3_shp.left = Inches(14.45)
    t3_shp.top = Inches(6.30)
    t3_shp.width = Inches(4.20)
    t3_shp.height = Inches(0.85)
    p3 = t3_shp.text_frame.paragraphs[0]
    p3.text = "Ultra-Fast Speed (1.2 ms)"
    p3.alignment = PP_ALIGN.CENTER
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(20)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy
    
    d3_shp = s5.shapes[10]
    d3_shp.left = Inches(13.90)
    d3_shp.top = Inches(7.20)
    d3_shp.width = Inches(5.30)
    d3_shp.height = Inches(1.20)
    d3_shp.text_frame.word_wrap = True
    pd3 = d3_shp.text_frame.paragraphs[0]
    pd3.text = "Uses a strict zero data leakage pipeline. It sorts articles in just 1.2 milliseconds, allowing instant news updates on a normal laptop."
    pd3.alignment = PP_ALIGN.CENTER
    pd3.font.name = "Segoe UI"
    pd3.font.size = Pt(16)
    pd3.font.bold = False
    pd3.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
    
    prs.save(pptx_path)
    prs.save(alt_path)
    print("Slide 5 updated successfully in both files!")

if __name__ == "__main__":
    update_slide5()

