import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

def update_slide8():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(pptx_path)
    s8 = prs.slides[7]
    
    # 1. Title Visibility: "The AI Models We Tested" -> Crisp White
    title_shp = s8.shapes[1]
    title_shp.left = Inches(3.00)
    title_shp.top = Inches(1.10)
    title_shp.width = Inches(14.00)
    title_shp.height = Inches(0.85)
    
    tf_title = title_shp.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = "The AI Models We Tested"
    p_title.alignment = PP_ALIGN.CENTER
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255) # Pure White
    
    # 2. Hide old 3-column card background shapes (3, 4, 5) and old text boxes (2, 6, 7, 8)
    for idx in [2, 3, 4, 5, 6, 7, 8]:
        s8.shapes[idx].left = Inches(-20)
        
    # Existing pictures: Shape 9 (Bar Chart), Shape 10 (Target), Shape 11 (Gear)
    # 3. Create 2x2 Grid Cards
    # Dimensions: 8.20" wide x 3.60" tall
    cards_config = [
        # Card 1 (Top-Left): Naive Bayes
        {
            "card_left": Inches(1.40), "card_top": Inches(2.35),
            "title": "Naive Bayes (Simple Guesser)",
            "desc": "Uses simple probability based on word frequencies. Fast (0.5 ms), but makes simple mistakes because it assumes all words are independent.",
            "best_for": "A quick, lightweight baseline.",
            "pic_shape": s8.shapes[9], # Bar Chart
            "is_winner": False
        },
        # Card 2 (Top-Right): Linear SVM (Our Winner)
        {
            "card_left": Inches(10.40), "card_top": Inches(2.35),
            "title": "Linear SVM (Our Winner ⭐)",
            "desc": "Draws a straight dividing line between topics in 10,000-word feature space. 96.4% accurate and super fast (1.2 ms).",
            "best_for": "Real-world news websites that need speed and high accuracy.",
            "pic_shape": s8.shapes[10], # Target
            "is_winner": True
        },
        # Card 3 (Bottom-Left): Neural MLP
        {
            "card_left": Inches(1.40), "card_top": Inches(6.25),
            "title": "Neural MLP (The Mini-Brain)",
            "desc": "A simple neural network with hidden layers. It learns complex non-linear patterns. 95.1% accurate and very fast (3.2 ms).",
            "best_for": "Capturing complex relationships between words.",
            "pic_shape": None, # Will add brain_network_icon.png
            "is_winner": False
        },
        # Card 4 (Bottom-Right): DistilBERT
        {
            "card_left": Inches(10.40), "card_top": Inches(6.25),
            "title": "DistilBERT (The Bookworm)",
            "desc": "Deep learning transformer that reads full sentences forward and backward to understand context (97.8% accurate, 12.4 ms).",
            "best_for": "Offline research where speed doesn't matter.",
            "pic_shape": s8.shapes[11], # Gear
            "is_winner": False
        }
    ]
    
    card_w = Inches(8.20)
    card_h = Inches(3.60)
    
    brain_icon_path = "docs/brain_network_icon.png"
    if not os.path.exists(brain_icon_path):
        brain_icon_path = "public/brain_network_icon.png"
        
    for cfg in cards_config:
        cl = cfg["card_left"]
        ct = cfg["card_top"]
        
        # A) Add rounded card background
        card_bg = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cl, ct, card_w, card_h)
        card_bg.fill.solid()
        if cfg["is_winner"]:
            card_bg.fill.fore_color.rgb = RGBColor(248, 250, 255) # Subtle indigo tint
            card_bg.line.color.rgb = RGBColor(99, 102, 241)       # Electric indigo border (#6366F1)
            card_bg.line.width = Pt(2.0)
        else:
            card_bg.fill.fore_color.rgb = RGBColor(255, 255, 255) # Pure white
            card_bg.line.color.rgb = RGBColor(203, 213, 225)       # Soft slate-300 border
            card_bg.line.width = Pt(1.5)
            
        # B) Position Icon (Top-Left aligned inside card)
        icon_left = cl + Inches(0.40)
        icon_top = ct + Inches(0.35)
        icon_size = Inches(0.95)
        
        if cfg["pic_shape"] is not None:
            pic = cfg["pic_shape"]
            pic.left = icon_left
            pic.top = icon_top
            pic.width = icon_size
            pic.height = icon_size
        else:
            # Neural MLP: add brain icon
            s8.shapes.add_picture(brain_icon_path, icon_left, icon_top, icon_size, icon_size)
            
        # C) Title Box (next to icon)
        title_box = s8.shapes.add_textbox(cl + Inches(1.50), ct + Inches(0.42), card_w - Inches(1.80), Inches(0.70))
        pt = title_box.text_frame.paragraphs[0]
        pt.text = cfg["title"]
        pt.alignment = PP_ALIGN.LEFT
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(20)
        pt.font.bold = True
        pt.font.color.rgb = RGBColor(67, 56, 202) if cfg["is_winner"] else RGBColor(15, 23, 42)
        
        # D) Body Text Box (aligned left with icon)
        desc_box = s8.shapes.add_textbox(cl + Inches(0.40), ct + Inches(1.45), card_w - Inches(0.80), Inches(1.95))
        tf_desc = desc_box.text_frame
        tf_desc.word_wrap = True
        tf_desc.margin_left = Inches(0)
        tf_desc.margin_right = Inches(0)
        tf_desc.margin_top = Inches(0)
        tf_desc.margin_bottom = Inches(0)
        
        # Paragraph 1: Description
        pd0 = tf_desc.paragraphs[0]
        pd0.text = cfg["desc"]
        pd0.alignment = PP_ALIGN.LEFT
        pd0.font.name = "Segoe UI"
        pd0.font.size = Pt(15.5)
        pd0.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
        pd0.space_after = Pt(8)
        pd0.line_spacing = 1.2
        
        # Paragraph 2: Best for
        pd1 = tf_desc.add_paragraph()
        pd1.alignment = PP_ALIGN.LEFT
        
        r_bf = pd1.add_run()
        r_bf.text = "Best for: "
        r_bf.font.name = "Segoe UI"
        r_bf.font.size = Pt(15.5)
        r_bf.font.bold = True
        r_bf.font.color.rgb = RGBColor(15, 23, 42)
        
        r_val = pd1.add_run()
        r_val.text = cfg["best_for"]
        r_val.font.name = "Segoe UI"
        r_val.font.size = Pt(15.5)
        r_val.font.bold = False
        r_val.font.color.rgb = RGBColor(71, 85, 105)
        
    prs.save(pptx_path)
    prs.save(alt_path)
    print("Slide 8 updated successfully to 2x2 grid in both files!")

if __name__ == "__main__":
    update_slide8()

