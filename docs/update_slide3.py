import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide3():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(pptx_path)
    s3 = prs.slides[2]
    
    # 1. Move old beige group (shape 1) and old text box (shape 3) off slide
    # Keep Shape 0 (footer) and Shape 2 (title)
    if len(s3.shapes) > 1:
        s3.shapes[1].left = Inches(-20)
    if len(s3.shapes) > 3:
        s3.shapes[3].left = Inches(-20)
        
    # 2. Add modern off-white / light slate card container (perfectly centered)
    # Slide width = 20.0, card width = 14.40, left = 2.80 -> left & right margins are both 2.80"
    card_left = Inches(2.80)
    card_top = Inches(2.10)
    card_width = Inches(14.40)
    card_height = Inches(7.00)
    
    card = s3.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        card_left, card_top, card_width, card_height
    )
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(248, 250, 252) # Soft modern off-white / Slate 50 (#F8FAFC)
    card.line.color.rgb = RGBColor(203, 213, 225)      # Crisp subtle border (#CBD5E1)
    card.line.width = Pt(1.5)
    
    # 3. Slide Title: "Introduction" (Centered at the top of the card)
    title_box = s3.shapes.add_textbox(card_left, Inches(2.35), card_width, Inches(0.80))
    p_title = title_box.text_frame.paragraphs[0]
    p_title.text = "Introduction"
    p_title.alignment = PP_ALIGN.CENTER
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(34)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
    
    # Also move old title (shape 2) off slide to prevent duplicate
    for shape in s3.shapes:
        if shape.has_text_frame and shape.text_frame.text.strip() == "Introduction" and shape != title_box:
            shape.left = Inches(-20)
            
    # 4. The 3 Points with Icons, Bold Headings (NO UNDERLINES), and Equal Margins
    # Card is from X=2.80 to 17.20. Content will be from X=3.50 to 16.50 (equal 0.70" internal margins!)
    points = [
        {
            "icon": "📰",
            "title": "The Challenge:",
            "desc": "Too Much News. Millions of articles are published online daily. Humans cannot read and sort them all by hand.",
            "badge_bg": RGBColor(254, 242, 242),   # Soft red-50
            "badge_border": RGBColor(254, 202, 202) # Soft red-200
        },
        {
            "icon": "🤖",
            "title": "The Solution:",
            "desc": "NewsScope, a web app created to categorize content instantly.",
            "badge_bg": RGBColor(238, 242, 255),   # Soft indigo-50
            "badge_border": RGBColor(199, 210, 254) # Soft indigo-200
        },
        {
            "icon": "🎯",
            "title": "The Goal:",
            "desc": "Help news websites, editors, and readers organize news instantly and explain why each category was chosen.",
            "badge_bg": RGBColor(240, 253, 244),   # Soft emerald-50
            "badge_border": RGBColor(187, 247, 208) # Soft emerald-200
        }
    ]
    
    start_y = Inches(3.45)
    row_gap = Inches(1.20)
    
    for i, pt_data in enumerate(points):
        row_y = start_y + i * row_gap
        
        # A) Icon Badge Box (left = 3.50")
        badge = s3.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(3.50), row_y + Inches(0.05), Inches(0.85), Inches(0.85)
        )
        badge.fill.solid()
        badge.fill.fore_color.rgb = pt_data["badge_bg"]
        badge.line.color.rgb = pt_data["badge_border"]
        badge.line.width = Pt(1.5)
        
        p_badge = badge.text_frame.paragraphs[0]
        p_badge.text = pt_data["icon"]
        p_badge.alignment = PP_ALIGN.CENTER
        p_badge.font.name = "Segoe UI Emoji"
        p_badge.font.size = Pt(26)
        
        # B) Text Box (left = 4.65", width = 11.85", right edge = 16.50")
        # Internal right margin is (17.20 - 16.50) = 0.70", matching internal left margin (3.50 - 2.80 = 0.70")!
        t_box = s3.shapes.add_textbox(Inches(4.65), row_y, Inches(11.85), Inches(0.95))
        tf = t_box.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        
        # Run 1: Bold Title (NO UNDERLINE)
        r1 = p.add_run()
        r1.text = pt_data["title"] + " "
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(19)
        r1.font.bold = True
        r1.font.underline = False
        r1.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
        
        # Run 2: Description
        r2 = p.add_run()
        r2.text = pt_data["desc"]
        r2.font.name = "Segoe UI"
        r2.font.size = Pt(18)
        r2.font.bold = False
        r2.font.underline = False
        r2.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
        
    prs.save(pptx_path)
    prs.save(alt_path)
    print("Slide 3 updated successfully in both files!")

if __name__ == "__main__":
    update_slide3()
