import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide4():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    prs = Presentation(pptx_path)
    s4 = prs.slides[3]
    
    # 1. Title: Change "Problems" to "Problem Statement"
    title_shp = s4.shapes[0]
    p_title = title_shp.text_frame.paragraphs[0]
    p_title.text = "Problem Statement"
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy
    
    # 2. Punctuation & Keyword Highlighting in Shape 2
    intro_shp = s4.shapes[2]
    tf_intro = intro_shp.text_frame
    
    # Clear existing runs in P0 and P2
    p0 = tf_intro.paragraphs[0]
    p0.text = ""
    
    # P0 - Run 1: Bold keywords
    r0_bold = p0.add_run()
    r0_bold.text = "Over 500 million news articles"
    r0_bold.font.name = "Segoe UI"
    r0_bold.font.size = Pt(20)
    r0_bold.font.bold = True
    r0_bold.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy
    
    # P0 - Run 2: Normal text with em-dash without space
    r0_norm = p0.add_run()
    r0_norm.text = " appear online every day. Sorting them by hand is too slow, expensive, and tiring for human editors. Regular AI models are 'black boxes'—they give a category without explaining why."
    r0_norm.font.name = "Segoe UI"
    r0_norm.font.size = Pt(20)
    r0_norm.font.bold = False
    r0_norm.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
    
    p2 = tf_intro.paragraphs[2]
    p2.text = ""
    
    # P2 - Run 1: Normal intro
    r2_norm = p2.add_run()
    r2_norm.text = "News editors and readers "
    r2_norm.font.name = "Segoe UI"
    r2_norm.font.size = Pt(20)
    r2_norm.font.bold = False
    r2_norm.font.color.rgb = RGBColor(51, 65, 85) # Slate 700
    
    # P2 - Run 2: Bold key phrase
    r2_bold = p2.add_run()
    r2_bold.text = "need an AI tool that is super fast, fair, and clearly explains its work."
    r2_bold.font.name = "Segoe UI"
    r2_bold.font.size = Pt(20)
    r2_bold.font.bold = True
    r2_bold.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy
    
    # 3. Color Clash: Replace neon cyan (00B0F0) with soft light blue (EEF2FF) in Shape 4
    shape4 = s4.shapes[4]
    xml_str = shape4._element.xml
    if "00B0F0" in xml_str:
        # Replace 00B0F0 with EEF2FF in the XML element
        from xml.etree import ElementTree as ET
        from pptx.oxml import parse_xml
        new_xml = xml_str.replace("00B0F0", "EEF2FF")
        new_elem = parse_xml(new_xml.encode("utf-8"))
        parent = shape4._element.getparent()
        parent.replace(shape4._element, new_elem)
        print("Updated Shape 4 fill from 00B0F0 to EEF2FF")
        
    # Re-fetch slide shapes after XML replacement
    s4 = prs.slides[3]
    
    # 4. Text Padding & Dark Navy Text in the 3 Problem Boxes (Shape 8, 9, 10)
    box_indices = [8, 9, 10]
    box_titles = ["Information Overload", "The Black-Box Gap", "Slow & Expensive AI"]
    box_descs = [
        "Millions of articles are published daily. Editors cannot tag thousands of stories by hand fast enough.",
        "Most AI tools just give an answer. They don't show which words caused the decision, making them hard to trust.",
        "Large AI models need expensive supercomputers. They are too slow and costly for instant news updates."
    ]
    
    for i, idx in enumerate(box_indices):
        shp = s4.shapes[idx]
        tf = shp.text_frame
        
        # Add Inner Margins / Padding
        tf.margin_left = Inches(0.28)
        tf.margin_right = Inches(0.28)
        tf.margin_top = Inches(0.22)
        tf.margin_bottom = Inches(0.22)
        tf.word_wrap = True
        
        # Clean text & format
        p0 = tf.paragraphs[0]
        p0.text = box_titles[i]
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(19)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy
        
        # Paragraph 1 (blank gap)
        if len(tf.paragraphs) > 1:
            tf.paragraphs[1].text = ""
            
        # Paragraph 2 (body)
        if len(tf.paragraphs) > 2:
            p2 = tf.paragraphs[2]
            p2.text = box_descs[i]
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(16)
            p2.font.bold = False
            p2.font.color.rgb = RGBColor(30, 41, 59) # Slate 800 Dark Navy
            
    prs.save(pptx_path)
    prs.save(alt_path)
    print("Slide 4 updated successfully in both files!")

if __name__ == "__main__":
    update_slide4()
