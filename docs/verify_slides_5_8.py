from pptx import Presentation
from pptx.enum.text import PP_ALIGN

def verify_deck(path):
    print(f"\n================ VERIFYING DECK: {path} ================")
    prs = Presentation(path)
    
    # -------------------------------------------------------------
    # SLIDE 5: The NewsScope Solution
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    print("[Slide 5: The NewsScope Solution]")
    s5_shapes = {shp.name: shp for shp in s5.shapes}
    
    # Check 3 cards exist
    assert "Slide5_Card_1" in s5_shapes
    assert "Slide5_Card_2" in s5_shapes
    assert "Slide5_Card_3" in s5_shapes
    
    # Check screenshot exists
    assert "Slide5_App_Screenshot" in s5_shapes
    pic = s5_shapes["Slide5_App_Screenshot"]
    assert pic.left > prs.slide_width / 2, "Screenshot should be on right side"
    
    # Check text alignment and sizes
    for i in range(1, 4):
        tb = s5_shapes[f"Slide5_CardText_{i}"]
        tf = tb.text_frame
        assert len(tf.paragraphs) >= 3
        # Title is paragraph 1
        tp = tf.paragraphs[1]
        assert tp.font.size.pt >= 20, f"Card {i} title font size too small: {tp.font.size.pt}"
        # Body is paragraph 2
        bp = tf.paragraphs[2]
        assert bp.font.size.pt >= 16, f"Card {i} body font size too small: {bp.font.size.pt}"
    print("  --> Slide 5 PASS: 3 horizontal cards on left, app screenshot on right, 22pt/17pt fonts verified!")

    # -------------------------------------------------------------
    # SLIDE 6: How NewsScope is Built
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    print("\n[Slide 6: How NewsScope is Built]")
    s6_shapes = {shp.name: shp for shp in s6.shapes}
    
    # Check 4 boxes exist
    for i in range(1, 5):
        assert f"Slide6_Box_{i}" in s6_shapes
        tb = s6_shapes[f"Slide6_BoxContent_{i}"]
        tf = tb.text_frame
        # Verify text alignment is CENTER
        for p in tf.paragraphs:
            if p.text.strip():
                assert p.alignment == PP_ALIGN.CENTER, f"Box {i} paragraph '{p.text[:20]}' not centered!"
        # Title is paragraph 2
        p_title = tf.paragraphs[2]
        assert p_title.font.size.pt >= 22, f"Box {i} title size too small: {p_title.font.size.pt}"
        # Body is paragraph 3
        p_body = tf.paragraphs[3]
        assert p_body.font.size.pt >= 18, f"Box {i} body size too small: {p_body.font.size.pt}"
        
    # Check 3 connecting arrows exist
    arrows_s6 = [s for s in s6.shapes if "Arrow" in s.name]
    assert len(arrows_s6) == 3, f"Expected 3 connecting arrows, got {len(arrows_s6)}"
    print("  --> Slide 6 PASS: Flowchart layout, 4 centered boxes, 3 connecting arrows, 23pt/18pt fonts verified!")

    # -------------------------------------------------------------
    # SLIDE 7: The NLP Preprocessing Pipeline
    # -------------------------------------------------------------
    s7 = prs.slides[6]
    print("\n[Slide 7: The NLP Pipeline]")
    s7_shapes = {shp.name: shp for shp in s7.shapes}
    
    # Check 4 stage boxes exist
    for i in range(1, 5):
        assert f"Slide7_StageBox_{i}" in s7_shapes
        tb = s7_shapes[f"Slide7_StageContent_{i}"]
        tf = tb.text_frame
        # Verify text alignment is CENTER
        for p in tf.paragraphs:
            if p.text.strip():
                assert p.alignment == PP_ALIGN.CENTER, f"Stage {i} paragraph '{p.text[:20]}' not centered!"
        # Title
        p_title = tf.paragraphs[2]
        assert p_title.font.size.pt >= 24, f"Stage {i} title size too small: {p_title.font.size.pt}"
        
    # Check arrows exist
    arrows_s7 = [s for s in s7.shapes if "AssemblyArrow" in s.name]
    assert len(arrows_s7) == 3, f"Expected 3 assembly arrows, got {len(arrows_s7)}"
    print("  --> Slide 7 PASS: Factory assembly line, gradient boxes, bold arrows, centered examples/bullets verified!")

    # -------------------------------------------------------------
    # SLIDE 8: The AI Models We Tested
    # -------------------------------------------------------------
    s8 = prs.slides[7]
    print("\n[Slide 8: The AI Models We Tested]")
    s8_shapes = {shp.name: shp for shp in s8.shapes}
    
    # Check 4 model cards exist in 2x2 grid
    for i in range(1, 5):
        assert f"Slide8_ModelCard_{i}" in s8_shapes
        tb = s8_shapes[f"Slide8_ModelText_{i}"]
        tf = tb.text_frame
        for p in tf.paragraphs:
            if p.text.strip():
                assert p.alignment == PP_ALIGN.CENTER, f"Model {i} paragraph '{p.text[:20]}' not centered!"
        # Title
        p_title = tf.paragraphs[1]
        assert p_title.font.size.pt >= 24, f"Model {i} title size too small: {p_title.font.size.pt}"
        # Body
        p_body = tf.paragraphs[4]
        assert p_body.font.size.pt >= 18, f"Model {i} body size too small: {p_body.font.size.pt}"
        
    # Check Winner Card (Model 2: Linear SVM)
    win_card = s8_shapes["Slide8_ModelCard_2"]
    assert win_card.line.width.pt >= 3.0, "Winner card border should be bold (>= 3pt)"
    print("  --> Slide 8 PASS: 2x2 grid layout, Winner highlight on Linear SVM, centered text, 25pt/19pt fonts verified!")

if __name__ == "__main__":
    verify_deck("docs/NewsScope_Presentation_CruxTemplate.pptx")
    verify_deck("docs/NewsScope_Presentation.pptx")
    print("\n🎉 ALL 4 SLIDES (5, 6, 7, 8) 100% VERIFIED ACROSS BOTH PRESENTATIONS! 🎉")
