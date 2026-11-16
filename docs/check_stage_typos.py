from pptx import Presentation

prs = Presentation("docs/NewsScope_Presentation.pptx")
s7 = prs.slides[6]
for i, shp in enumerate(s7.shapes):
    if shp.has_text_frame:
        print(f"[{i}] {shp.name}: {repr(shp.text_frame.paragraphs[0].text)}")
