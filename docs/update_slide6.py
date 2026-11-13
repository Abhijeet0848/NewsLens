import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide6():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(pptx_path)
    s6 = prs.slides[5]
    
    # 1. Title Visibility: Change "How NewsScope is Built (4 Simple Parts)" to White
    title_shp = s6.shapes[0]
    tf_title = title_shp.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = "How NewsScope is Built (4 Simple Parts)"
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(34)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255) # Pure White
    
    # Also adjust subtitle (shape 1) to soft light grey for perfect contrast
    sub_shp = s6.shapes[1]
    p_sub = sub_shp.text_frame.paragraphs[0]
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(226, 232, 240) # Light Slate 200
    
    # 2. Delete broken overlapping text (Shape 7 - 'dolor sit amet...') and empty boxes (Shapes 6, 8)
    for idx in [6, 7, 8]:
        s6.shapes[idx].left = Inches(-20)
        
    # Also remove connective connector shapes 14, 15, 16 if needed or keep them clean
    # Shape 17, 18, 19, 20 are the text frames for the 4 cards
    cards_data = [
        {
            "shape_idx": 17,
            "title": "Frontend (Next.js 14)",
            "text": "The screen you see. A fast, modern web page where typing never freezes or lags.",
            "left": Inches(0.70),
        },
        {
            "shape_idx": 18,
            "title": "API Gateway (FastAPI)",
            "text": "The waiter. Takes your article text, checks it safely, and sends it to the kitchen in 1 millisecond.",
            "left": Inches(5.70),
        },
        {
            "shape_idx": 19,
            "title": "ML Engine (Scikit-Learn)",
            "text": "The kitchen. Cleans the text, turns words into numbers (TF-IDF), and calculates the category scores.",
            "left": Inches(10.50),
        },
        {
            "shape_idx": 20,
            "title": "Saved Models (Joblib)",
            "text": "The recipe book. Saved pre-trained models ready to give answers instantly without retraining.",
            "left": Inches(15.75),
        }
    ]
    
    common_top = Inches(5.95)
    common_width = Inches(3.25)
    common_height = Inches(3.20)
    
    for c in cards_data:
        shp = s6.shapes[c["shape_idx"]]
        shp.left = c["left"]
        shp.top = common_top
        shp.width = common_width
        shp.height = common_height
        
        tf = shp.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.10)
        tf.margin_right = Inches(0.10)
        tf.margin_top = Inches(0.10)
        tf.margin_bottom = Inches(0.10)
        
        # Clear existing paragraphs and create structured content
        # P0: Title
        p0 = tf.paragraphs[0]
        p0.text = c["title"]
        p0.alignment = PP_ALIGN.LEFT
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(21)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy
        p0.space_after = Pt(10)
        
        # Remove extra paragraphs if any
        while len(tf.paragraphs) > 1:
            p_rem = tf.paragraphs[-1]._p
            p_rem.getparent().remove(p_rem)
            
        # P1: Description text
        p1 = tf.add_paragraph()
        p1.text = c["text"]
        p1.alignment = PP_ALIGN.LEFT
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(16)
        p1.font.bold = False
        p1.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
        p1.line_spacing = 1.25
        
    prs.save(pptx_path)
    prs.save(alt_path)
    print("Slide 6 updated successfully in both files!")

if __name__ == "__main__":
    update_slide6()
