from pptx import Presentation

prs = Presentation("docs/NewsScope_Presentation.pptx")
s7 = prs.slides[6]
for i in [5, 7, 9, 11]:
    shp = s7.shapes[i]
    p = shp.text_frame.paragraphs[0]
    r = p.runs[0] if p.runs else None
    f_name = r.font.name if r else "None"
    print(f"Shape [{i}] {shp.name}: text={repr(p.text)}, font={f_name}")
    for char in p.text:
        if char in '0123456789O':
            print(f"  char: {repr(char)}, ord: {ord(char)}")
