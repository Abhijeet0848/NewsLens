import os
import zipfile
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def update_slide7_pptx():
    pptx_path = "docs/NewsScope_Presentation.pptx"
    alt_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    
    # 1. Update title on slide 7 via python-pptx
    prs = Presentation(pptx_path)
    s7 = prs.slides[6]
    
    title_shp = s7.shapes[1]
    title_shp.left = Inches(3.00)
    title_shp.top = Inches(1.50)
    title_shp.width = Inches(14.00)
    title_shp.height = Inches(0.90)
    
    p = title_shp.text_frame.paragraphs[0]
    p.text = "The NLP Preprocessing Pipeline"
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Segoe UI"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(15, 23, 42) # Dark Navy (#0F172A)
    
    prs.save(pptx_path)
    prs.save(alt_path)
    print("Slide 7 title updated via python-pptx")
    
    # 2. Update SmartArt XML in ppt/diagrams/data1.xml and ppt/diagrams/drawing1.xml
    replacements = [
        ("Preprocessing", "Cleaning &amp; Normalization"),
        ("Regex cleaning removes artifacts, normalizes Unicode, and supports Hindi.",
         "Lowercases text, removes HTML tags, URLs, and punctuation to reduce noise."),
        
        ("Tokenization", "Tokenization &amp; Stopwords"),
        ("Splits the document into independent, structural sentences.",
         "Splits the article into individual words and removes common filler words like &quot;the&quot;, &quot;is&quot;, and &quot;at&quot;."),
        
        ("Scoring", "Lemmatization"),
        ("Calculates sentence importance using TF-IDF and Word Frequency.",
         "Reduces words to their base dictionary form (e.g., &quot;running&quot; becomes &quot;run&quot;) to standardize vocabulary."),
        
        ("Extraction &amp; Reorder ", "TF-IDF Vectorization"),
        ("Extraction &amp; Reorder", "TF-IDF Vectorization"),
        ("Selects top-scoring sentences and restores them to chronological order.",
         "Converts the cleaned words into 10,000 mathematical features, highlighting unique and important terms.")
    ]
    
    for target_file in [pptx_path, alt_path]:
        temp_zip = target_file + ".tmp.zip"
        with zipfile.ZipFile(target_file, "r") as zin:
            with zipfile.ZipFile(temp_zip, "w", compression=zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename in ["ppt/diagrams/data1.xml", "ppt/diagrams/drawing1.xml"]:
                        text = data.decode("utf-8")
                        for old_val, new_val in replacements:
                            text = text.replace(old_val, new_val)
                        data = text.encode("utf-8")
                        print(f"Patched {item.filename} in {target_file}")
                    zout.writestr(item, data)
        os.replace(temp_zip, target_file)
        print(f"Successfully updated SmartArt diagram in {target_file}")

if __name__ == "__main__":
    update_slide7_pptx()

