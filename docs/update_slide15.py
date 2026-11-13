import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide15():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    qr_path = "docs/github_qr_flat.png"
    
    # Ensure flat QR code exists
    if not os.path.exists(qr_path):
        import generate_qr
        
    # Colors
    c_navy = RGBColor(15, 23, 42)          # Slate 900 (#0F172A)
    c_slate = RGBColor(71, 85, 105)        # Slate 600 (#475569)
    c_indigo = RGBColor(79, 70, 229)       # Electric Indigo (#4F46E5)
    c_bg_border = RGBColor(226, 232, 240)  # Slate 200

    for target_path in [alt_path, pptx_path]:
        try:
            prs = Presentation(target_path)
        except Exception as e:
            print(f"Cannot open {target_path}: {e}")
            continue
            
        s15 = prs.slides[14]
        
        # 1. Update Title Shape (Shape 0: TextBox 2)
        title_shp = s15.shapes[0]
        title_shp.left = Inches(3.00)
        title_shp.top = Inches(1.40)
        title_shp.width = Inches(14.00)
        title_shp.height = Inches(2.20)
        
        tf_title = title_shp.text_frame
        tf_title.word_wrap = True
        while len(tf_title.paragraphs) > 0:
            p_rem = tf_title.paragraphs[-1]._p
            p_rem.getparent().remove(p_rem)
            
        p0 = tf_title.add_paragraph()
        p0.alignment = PP_ALIGN.CENTER
        p0.space_after = Pt(6)
        r0 = p0.add_run()
        r0.text = "THANK YOU!"
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(54)
        r0.font.bold = True
        r0.font.color.rgb = c_navy
        
        p1 = tf_title.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        r1 = p1.add_run()
        r1.text = "Questions & Academic Evaluation — NewsScope Classifier"
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(22)
        r1.font.bold = True
        r1.font.color.rgb = c_indigo
        
        # 2. Update QR Code: Replace old Picture 27 with clean flat QR code
        # Remove old picture or hide it
        old_pic = s15.shapes[5]
        old_pic.left = Inches(-20)
        
        # Check if Slide15_FlatQR already exists
        qr_shp = None
        for shp in s15.shapes:
            if shp.name == "Slide15_FlatQR":
                qr_shp = shp
                break
                
        qr_size = Inches(3.80)
        qr_left = Inches((20.0 - 3.80) / 2) # Centered at 8.10"
        qr_top = Inches(3.90)
        
        if qr_shp:
            qr_shp.left = qr_left
            qr_shp.top = qr_top
            qr_shp.width = qr_size
            qr_shp.height = qr_size
        else:
            qr_shp = s15.shapes.add_picture(qr_path, qr_left, qr_top, qr_size, qr_size)
            qr_shp.name = "Slide15_FlatQR"
            
        # 3. Update URL & Repo Info (Shape 4: TextBox 25)
        url_shp = s15.shapes[4]
        url_shp.left = Inches(2.00)
        url_shp.top = Inches(8.00)
        url_shp.width = Inches(16.00)
        url_shp.height = Inches(2.20)
        
        tf_url = url_shp.text_frame
        tf_url.word_wrap = True
        while len(tf_url.paragraphs) > 0:
            p_rem = tf_url.paragraphs[-1]._p
            p_rem.getparent().remove(p_rem)
            
        # Paragraph 1: Scan label
        p_sub = tf_url.add_paragraph()
        p_sub.alignment = PP_ALIGN.CENTER
        p_sub.space_after = Pt(6)
        r_sub = p_sub.add_run()
        r_sub.text = "Scan the QR code above or visit the project repository:"
        r_sub.font.name = "Segoe UI"
        r_sub.font.size = Pt(17)
        r_sub.font.bold = False
        r_sub.font.color.rgb = c_slate
        
        # Paragraph 2: Massive, bold, high-contrast URL for distant visibility
        p_link = tf_url.add_paragraph()
        p_link.alignment = PP_ALIGN.CENTER
        p_link.space_after = Pt(6)
        r_link = p_link.add_run()
        r_link.text = "https://github.com/Abhijeet0848/NewsLens"
        r_link.font.name = "Consolas"
        r_link.font.size = Pt(26) # Massive & crystal clear!
        r_link.font.bold = True
        r_link.font.color.rgb = c_indigo
        
        # Paragraph 3: Subtitle / Explanatory tag
        p_info = tf_url.add_paragraph()
        p_info.alignment = PP_ALIGN.CENTER
        r_info = p_info.add_run()
        r_info.text = "Full Source Code  •  Pretrained Joblib Models  •  Complete Academic Report"
        r_info.font.name = "Segoe UI"
        r_info.font.size = Pt(15)
        r_info.font.bold = True
        r_info.font.color.rgb = c_navy
        
        # 4. Presenter Speaker Notes for Slide 15
        try:
            notes_slide = s15.notes_slide
            tf_notes = notes_slide.notes_text_frame
            tf_notes.text = (
                "Thank you respected members of the examination committee and Dr. Vikas Mittal for your time and guidance. "
                "NewsScope demonstrates that fast, transparent, and accurate news classification can be achieved using a zero-data-leakage NLP pipeline and calibrated Linear SVMs without heavy supercomputing overhead. "
                "All code, datasets, evaluation matrices, and pretrained models are publicly available on GitHub at the link and QR code shown on screen. "
                "I would now be delighted to answer any questions or demonstrate the live application."
            )
            print(f"Speaker notes added to Slide 15 in {target_path}")
        except Exception as e:
            print(f"Notes warning in {target_path}: {e}")
            
        try:
            prs.save(target_path)
            print(f"Slide 15 successfully updated in {target_path}!")
        except Exception as e:
            print(f"Error saving {target_path}: {e}")

if __name__ == "__main__":
    update_slide15()
