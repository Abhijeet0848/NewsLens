import shutil
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_stage_badges(prs_path):
    prs = Presentation(prs_path)
    s7 = prs.slides[6]
    
    badges = {
        "Slide7_StageContent_1": ("STAGE 01  •  CLEANING", RGBColor(3, 105, 161)),
        "Slide7_StageContent_2": ("STAGE 02  •  TOKEN & FILTER", RGBColor(2, 132, 199)),
        "Slide7_StageContent_3": ("STAGE 03  •  LEMMATIZATION", RGBColor(37, 99, 235)),
        "Slide7_StageContent_4": ("STAGE 04  •  VECTORIZATION", RGBColor(79, 70, 229)),
    }
    
    for shp in s7.shapes:
        if shp.name in badges:
            text_val, col = badges[shp.name]
            p = shp.text_frame.paragraphs[0]
            p.text = text_val
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                r.font.name = "Segoe UI"
                r.font.size = Pt(12)
                r.font.bold = True
                r.font.color.rgb = col
            print(f"  Updated {shp.name} -> '{text_val}' with Segoe UI font (ord 48 for '0')")
            
    # Also update Slide 10 badges to explicit Segoe UI
    s10 = prs.slides[9]
    for shp in s10.shapes:
        if shp.name in ["Card1_Content", "Card2_Content"]:
            p = shp.text_frame.paragraphs[0]
            for r in p.runs:
                r.font.name = "Segoe UI"
                r.font.size = Pt(12)
                r.font.bold = True
            print(f"  Updated Slide 10 {shp.name} badge font to Segoe UI")
            
    prs.save(prs_path)
    print(f"Saved {prs_path}")

update_stage_badges("docs/NewsScope_Presentation_CruxTemplate.pptx")

# Sync to NewsScope_Presentation.pptx
target = "docs/NewsScope_Presentation.pptx"
try:
    shutil.copy2("docs/NewsScope_Presentation_CruxTemplate.pptx", target)
    print(f"Successfully copied to {target}!")
except Exception as e:
    print(f"Error copying to {target}: {e}")
