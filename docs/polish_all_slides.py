import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def polish_presentation():
    prs_path = "docs/NewsScope_Presentation_CruxTemplate.pptx"
    prs = Presentation(prs_path)
    
    # -------------------------------------------------------------
    # COLOR PALETTE
    # -------------------------------------------------------------
    c_white = RGBColor(255, 255, 255)
    c_navy = RGBColor(15, 23, 42)          # Slate 900 (#0F172A)
    c_slate_dark = RGBColor(51, 65, 85)    # Slate 700 (#334155)
    c_slate_mid = RGBColor(100, 116, 139)  # Slate 500 (#64748B)
    c_slate_sub = RGBColor(226, 232, 240)  # Slate 200 (#E2E8F0)
    c_border = RGBColor(203, 213, 225)     # Slate 300 (#CBD5E1)
    
    c_indigo = RGBColor(79, 70, 229)       # Indigo 600 (#4F46E5)
    c_indigo_bdr = RGBColor(99, 102, 241)  # Indigo 500 (#6366F1)
    c_cyan = RGBColor(56, 189, 248)        # Sky 400 (#38BDF8)
    c_emerald = RGBColor(5, 150, 105)      # Emerald 600 (#059669)
    c_emerald_dark = RGBColor(6, 78, 59)   # Emerald 900 (#064E3B)
    c_emerald_bg = RGBColor(240, 253, 244) # Emerald 50 (#F0FDF4)
    c_amber = RGBColor(217, 119, 6)        # Amber 600 (#D97706)
    
    print("==================================================")
    print("POLISHING ALL 15 SLIDES (SIMPLE ENGLISH & CLEAN LAYOUT)")
    print("==================================================")

    # -------------------------------------------------------------
    # SLIDE 1: Cover Page
    # -------------------------------------------------------------
    print("\n[Slide 1] Checking title and subtitle...")
    s1 = prs.slides[0]
    for shp in s1.shapes:
        if shp.has_text_frame:
            txt = shp.text_frame.text
            if "NEWSCOPE" in txt:
                shp.text_frame.paragraphs[0].text = "NEWSSCOPE"
                print("  Fixed 'NEWSCOPE' -> 'NEWSSCOPE'")

    # -------------------------------------------------------------
    # SLIDE 2: Agenda
    # -------------------------------------------------------------
    print("\n[Slide 2] Updating Agenda item 4 to '4-Step Text Preprocessing'...")
    s2 = prs.slides[1]
    for shp in s2.shapes:
        if shp.has_text_frame and "5-Step" in shp.text_frame.text:
            shp.text_frame.paragraphs[0].text = "4-Step Text Preprocessing"
            print("  Updated '5-Step Text Preprocessing' -> '4-Step Text Preprocessing'")

    # -------------------------------------------------------------
    # SLIDE 3: Introduction
    # -------------------------------------------------------------
    print("\n[Slide 3] Removing old duplicate text boxes and setting simple English...")
    s3 = prs.slides[2]
    # Remove old off-screen duplicate boxes (TextBox 9, TextBox 10, Group 6)
    s3_to_remove = []
    for shp in s3.shapes:
        if shp.name in ["TextBox 9", "TextBox 10", "Group 6"] or shp.left < 0:
            s3_to_remove.append(shp)
    for shp in s3_to_remove:
        sp = shp._element
        sp.getparent().remove(sp)
        print(f"  Removed duplicate shape: {shp.name}")
        
    # Update text to simple English
    for shp in s3.shapes:
        if shp.name == "TextBox 13":
            shp.text_frame.paragraphs[0].text = "The Challenge: Too Much News. Millions of articles are published online daily. Humans cannot read and sort them all by hand."
        elif shp.name == "TextBox 15":
            shp.text_frame.paragraphs[0].text = "The Solution: NewsScope, a fast web app that sorts news into categories in 1 millisecond."
        elif shp.name == "TextBox 17":
            shp.text_frame.paragraphs[0].text = "The Goal: Help newsrooms and readers organize news automatically, and clearly explain why each category was chosen."

    # -------------------------------------------------------------
    # SLIDE 4: Problem Statement
    # -------------------------------------------------------------
    print("\n[Slide 4] Refining Problem Statement subtitle...")
    s4 = prs.slides[3]
    for shp in s4.shapes:
        if shp.name == "TextBox 9":
            tf = shp.text_frame
            while len(tf.paragraphs) > 0:
                p_rem = tf.paragraphs[-1]._p
                p_rem.getparent().remove(p_rem)
            p = tf.add_paragraph()
            p.text = "Over 500 million news articles appear online every day. Sorting them by hand is too slow, expensive, and tiring for human editors. Regular AI models are 'black boxes'—they give an answer without explaining why.\n\nNews editors and readers need an AI tool that is super fast, fair, and clearly explains its work."
            p.font.name = "Segoe UI"
            p.font.size = Pt(17)
            p.font.color.rgb = c_slate_dark

    # -------------------------------------------------------------
    # SLIDE 5: The NewsScope Solution
    # -------------------------------------------------------------
    print("\n[Slide 5] Simplifying English on Dashboard Solution cards...")
    s5 = prs.slides[4]
    for shp in s5.shapes:
        if shp.name == "Slide5_Header":
            tf = shp.text_frame
            tf.paragraphs[1].text = "A smart tool that sorts news stories in 1 millisecond and explains its reasoning."
        elif shp.name == "Slide5_CardText_1":
            tf = shp.text_frame
            tf.paragraphs[1].text = "Shows Its Work (Explainable AI)"
            tf.paragraphs[2].text = "Saliency keyword weights reveal the exact words driving each decision. Editors see why, not just what."
        elif shp.name == "Slide5_CardText_2":
            tf = shp.text_frame
            tf.paragraphs[1].text = "High Accuracy (96.4%)"
            tf.paragraphs[2].text = "Tested on thousands of real news stories. Correct 96 out of 100 times across all 5 news categories."
        elif shp.name == "Slide5_CardText_3":
            tf = shp.text_frame
            tf.paragraphs[1].text = "Super Fast (1.2 ms Speed)"
            tf.paragraphs[2].text = "Sorts an entire article in a millisecond on standard computers without expensive parts or delay."

    # -------------------------------------------------------------
    # SLIDE 6: How NewsScope is Built
    # -------------------------------------------------------------
    print("\n[Slide 6] Simplifying English on Architecture Flowchart...")
    s6 = prs.slides[5]
    for shp in s6.shapes:
        if shp.name == "Slide6_Header":
            tf = shp.text_frame
            tf.paragraphs[1].text = "How an article travels from your screen to the AI answer in 4 simple steps."
        elif shp.name == "Slide6_BoxContent_1":
            tf = shp.text_frame
            tf.paragraphs[2].text = "Frontend (The Screen)\nNext.js 14"
            tf.paragraphs[3].text = "The screen you see.\nA clean, fast website where you paste the article. Never lags or freezes."
        elif shp.name == "Slide6_BoxContent_2":
            tf = shp.text_frame
            tf.paragraphs[2].text = "API Gateway (The Waiter)\nFastAPI"
            tf.paragraphs[3].text = "The waiter.\nTakes your text, makes sure it is valid, and hands it to the AI in 1 millisecond."
        elif shp.name == "Slide6_BoxContent_3":
            tf = shp.text_frame
            tf.paragraphs[2].text = "ML Engine (The Kitchen)\nScikit-Learn"
            tf.paragraphs[3].text = "The kitchen.\nCleans the text, scores the words, and calculates the best news category."
        elif shp.name == "Slide6_BoxContent_4":
            tf = shp.text_frame
            tf.paragraphs[2].text = "Saved Models (Recipe Book)\nJoblib"
            tf.paragraphs[3].text = "The recipe book.\nPre-trained models loaded in memory so answers come back instantly."

    # -------------------------------------------------------------
    # SLIDE 7: The NLP Preprocessing Pipeline
    # -------------------------------------------------------------
    print("\n[Slide 7] Simplifying English on Assembly Line...")
    s7 = prs.slides[6]
    for shp in s7.shapes:
        if shp.name == "Slide7_Header":
            tf = shp.text_frame
            tf.paragraphs[1].text = "4 simple steps to clean messy text and turn words into numbers the AI understands."
        elif shp.name == "Slide7_StageContent_1":
            tf = shp.text_frame
            tf.paragraphs[2].text = "Step 1: Clean Text"
            tf.paragraphs[4].text = "• Makes all letters lowercase"
            tf.paragraphs[5].text = "• Removes punctuation & symbols"
            tf.paragraphs[6].text = "• Cleans web links and noise"
        elif shp.name == "Slide7_StageContent_2":
            tf = shp.text_frame
            tf.paragraphs[2].text = "Step 2: Remove Filler"
            tf.paragraphs[4].text = "• Drops useless grammar words"
            tf.paragraphs[5].text = "• Removes filler: 'the', 'is', 'with'"
            tf.paragraphs[6].text = "• Keeps words with real meaning"
        elif shp.name == "Slide7_StageContent_3":
            tf = shp.text_frame
            tf.paragraphs[2].text = "Step 3: Root Words"
            tf.paragraphs[4].text = "• Changes words to basic form"
            tf.paragraphs[5].text = "• Turns plurals into singulars"
            tf.paragraphs[6].text = "• Groups word variations together"
        elif shp.name == "Slide7_StageContent_4":
            tf = shp.text_frame
            tf.paragraphs[2].text = "Step 4: Score Words"
            tf.paragraphs[4].text = "• Gives rare, key words high scores"
            tf.paragraphs[5].text = "• Downweights common generic words"
            tf.paragraphs[6].text = "• Turns the article into numbers for AI"

    # -------------------------------------------------------------
    # SLIDE 8: The AI Models We Tested
    # -------------------------------------------------------------
    print("\n[Slide 8] Simplifying English on Models Grid...")
    s8 = prs.slides[7]
    for shp in s8.shapes:
        if shp.name == "Slide8_Header":
            tf = shp.text_frame
            tf.paragraphs[1].text = "We tested 4 different AI models on 2,225 BBC news articles to find the champion."
        elif shp.name == "Slide8_ModelText_1":
            tf = shp.text_frame
            tf.paragraphs[1].text = "Naive Bayes (Simple Guesser)"
            tf.paragraphs[3].text = "Word Count Multi-Class Baseline"
            tf.paragraphs[4].text = "Guesses the topic based on word counts.\nVery fast and lightweight, but assumes all words are completely independent."
        elif shp.name == "Slide8_ModelText_2":
            tf = shp.text_frame
            tf.paragraphs[1].text = "Linear SVM (Our Winner ⭐)"
            tf.paragraphs[3].text = "Draws Dividing Lines in Word Space"
            tf.paragraphs[4].text = "Draws clear dividing boundaries between news topics.\nMatches deep learning accuracy with 10× faster CPU inference."
        elif shp.name == "Slide8_ModelText_3":
            tf = shp.text_frame
            tf.paragraphs[1].text = "Neural MLP (The Mini-Brain)"
            tf.paragraphs[3].text = "Small Neural Network with Hidden Layers"
            tf.paragraphs[4].text = "Dense hidden layers learning complex word combinations.\nFast CPU execution without needing expensive graphics cards."
        elif shp.name == "Slide8_ModelText_4":
            tf = shp.text_frame
            tf.paragraphs[1].text = "DistilBERT (Deep Learning)"
            tf.paragraphs[3].text = "Bidirectional Contextual Transformer"
            tf.paragraphs[4].text = "Reads full sentences forward and backward for highest accuracy.\n10× slower latency and uses 20× more computer memory."

    # -------------------------------------------------------------
    # SLIDE 9: Step 1: The Raw Input (CRITICAL PURGE OF OLD HALLUCINATIONS)
    # -------------------------------------------------------------
    print("\n[Slide 9] PURGING old summarization math shapes and rebuilding clean Step 1 card...")
    s9 = prs.slides[8]
    # Remove ALL existing shapes on Slide 9 to guarantee zero leftover text
    for shp in list(s9.shapes):
        sp = shp._element
        sp.getparent().remove(sp)
        
    # Title Header
    tb_s9 = s9.shapes.add_textbox(Inches(1.20), Inches(0.70), Inches(17.60), Inches(1.30))
    tb_s9.name = "Slide9_Header"
    tf_s9 = tb_s9.text_frame
    tf_s9.word_wrap = True
    
    p9_0 = tf_s9.paragraphs[0]
    p9_0.alignment = PP_ALIGN.CENTER
    p9_0.text = "The Live Example: Step-by-Step"
    p9_0.font.name = "Segoe UI"
    p9_0.font.size = Pt(34)
    p9_0.font.bold = True
    p9_0.font.color.rgb = c_white
    p9_0.space_after = Pt(4)
    
    p9_sub = tf_s9.add_paragraph()
    p9_sub.alignment = PP_ALIGN.CENTER
    p9_sub.text = "Step 1: The Raw News Article"
    p9_sub.font.name = "Segoe UI"
    p9_sub.font.size = Pt(18)
    p9_sub.font.color.rgb = c_slate_sub
    
    # Large Centered Card
    card_w_s9 = Inches(14.00)
    card_h_s9 = Inches(6.80)
    card_left_s9 = (prs.slide_width - card_w_s9) / 2
    card_top_s9 = Inches(2.60)
    
    c9_rect = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_left_s9, card_top_s9, card_w_s9, card_h_s9)
    c9_rect.name = "Slide9_Card"
    c9_rect.fill.solid()
    c9_rect.fill.fore_color.rgb = c_white
    c9_rect.line.color.rgb = c_border
    c9_rect.line.width = Pt(2.0)
    
    c9_tb = s9.shapes.add_textbox(card_left_s9 + Inches(0.60), card_top_s9 + Inches(0.50), card_w_s9 - Inches(1.20), card_h_s9 - Inches(1.00))
    c9_tb.name = "Slide9_CardContent"
    tf9 = c9_tb.text_frame
    tf9.word_wrap = True
    
    # Badge
    p9_b = tf9.paragraphs[0]
    p9_b.alignment = PP_ALIGN.CENTER
    p9_b.text = "STEP 1  •  RAW INPUT TEXT"
    p9_b.font.name = "Segoe UI"
    p9_b.font.size = Pt(13)
    p9_b.font.bold = True
    p9_b.font.color.rgb = c_indigo
    p9_b.space_after = Pt(10)
    
    # Card Title
    p9_t = tf9.add_paragraph()
    p9_t.alignment = PP_ALIGN.CENTER
    p9_t.text = "📄  Original News Article"
    p9_t.font.name = "Segoe UI"
    p9_t.font.size = Pt(26)
    p9_t.font.bold = True
    p9_t.font.color.rgb = c_navy
    p9_t.space_after = Pt(24)
    
    # Article Text
    p9_art = tf9.add_paragraph()
    p9_art.alignment = PP_ALIGN.CENTER
    p9_art.text = '"Apple unveils new M3 MacBook laptop with ultra-fast processor. The laptop delivers 22-hour battery life and high performance graphics for developers."'
    p9_art.font.name = "Segoe UI"
    p9_art.font.size = Pt(21)
    p9_art.font.italic = True
    p9_art.font.bold = True
    p9_art.font.color.rgb = c_navy
    p9_art.space_after = Pt(28)
    
    # Explainer
    p9_exp = tf9.add_paragraph()
    p9_exp.alignment = PP_ALIGN.CENTER
    p9_exp.text = "To a human reader, this article is clearly about Technology.\nIn the next steps, we will see how NewsScope proves this mathematically in just 1.2 milliseconds."
    p9_exp.font.name = "Segoe UI"
    p9_exp.font.size = Pt(18)
    p9_exp.font.color.rgb = c_slate_dark

    # -------------------------------------------------------------
    # SLIDE 10: Steps 2 & 3: Word Scoring & Decision
    # -------------------------------------------------------------
    print("\n[Slide 10] Simplifying English on Step 2 & 3 cards...")
    s10 = prs.slides[9]
    for shp in s10.shapes:
        if shp.name == "Slide10_Title":
            tf = shp.text_frame
            tf.paragraphs[1].text = "Step 2: Scoring the Words  ➔  Step 3: Picking the Category"
        elif shp.name == "Card1_Content":
            tf = shp.text_frame
            tf.paragraphs[0].text = "STEP 02  •  WORD SCORING (TF-IDF)"
            tf.paragraphs[1].text = "Step 2: Scoring Important Words"
            tf.paragraphs[2].text = "The Math: The model converts the cleaned words into numbers."
            tf.paragraphs[3].text = 'Word Count (TF): The word "apple" appears 1 time in the article.'
            tf.paragraphs[4].text = 'Word Importance (IDF): Common words like "the" appear everywhere, so they get 0 score. Rare tech words like "processor" and "macbook" get huge math weights.'
            tf.paragraphs[5].text = "Top Saliency Word Weights Extracted:"
        elif shp.name == "Card2_Content":
            tf = shp.text_frame
            tf.paragraphs[0].text = "STEP 03  •  WINNER SELECTION (LINEAR SVM)"
            tf.paragraphs[1].text = "Step 3: Picking the Winner"
            tf.paragraphs[2].text = "How the AI Decides: It multiplies the word scores by the category weights:"
            tf.paragraphs[3].text = "Total Score = (Word Score) × (Category Match)"
            tf.paragraphs[4].text = 'Because of strong words like "processor" and "macbook", the Technology score is huge.'
            tf.paragraphs[5].text = "Final Probability Scores:"
            tf.paragraphs[11].text = "✔ All 4 AI models agreed 100% on Technology."

    # -------------------------------------------------------------
    # SLIDE 11: Step 4: Final Classification Result (PURGE OVERLAPS)
    # -------------------------------------------------------------
    print("\n[Slide 11] PURGING duplicate screenshots & text, rebuilding clean Step 4 layout...")
    s11 = prs.slides[10]
    # Remove ALL existing shapes on Slide 11
    for shp in list(s11.shapes):
        sp = shp._element
        sp.getparent().remove(sp)
        
    # Title Header
    tb_s11 = s11.shapes.add_textbox(Inches(1.20), Inches(0.50), Inches(17.60), Inches(1.10))
    tb_s11.name = "Slide11_Header"
    tf_s11 = tb_s11.text_frame
    tf_s11.word_wrap = True
    
    p11_0 = tf_s11.paragraphs[0]
    p11_0.alignment = PP_ALIGN.CENTER
    p11_0.text = "The Live Example: Step-by-Step"
    p11_0.font.name = "Segoe UI"
    p11_0.font.size = Pt(32)
    p11_0.font.bold = True
    p11_0.font.color.rgb = c_white
    
    p11_sub = tf_s11.add_paragraph()
    p11_sub.alignment = PP_ALIGN.CENTER
    p11_sub.text = "Step 4: The Final Classification Result"
    p11_sub.font.name = "Segoe UI"
    p11_sub.font.size = Pt(17)
    p11_sub.font.color.rgb = c_slate_sub
    
    # Result Banner
    banner_w = Inches(16.40)
    banner_h = Inches(1.15)
    banner_left = (prs.slide_width - banner_w) / 2
    banner_top = Inches(1.75)
    
    ban_rect = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, banner_left, banner_top, banner_w, banner_h)
    ban_rect.name = "Slide11_Banner"
    ban_rect.fill.solid()
    ban_rect.fill.fore_color.rgb = c_white
    ban_rect.line.color.rgb = c_emerald
    ban_rect.line.width = Pt(2.5)
    
    ban_tb = s11.shapes.add_textbox(banner_left + Inches(0.30), banner_top + Inches(0.12), banner_w - Inches(0.60), banner_h - Inches(0.24))
    ban_tb.name = "Slide11_BannerText"
    btf = ban_tb.text_frame
    btf.word_wrap = True
    
    bp0 = btf.paragraphs[0]
    bp0.alignment = PP_ALIGN.CENTER
    bp0.text = "Predicted Category: TECHNOLOGY  (97.7% Calibrated Confidence  •  1.20 ms)"
    bp0.font.name = "Segoe UI"
    bp0.font.size = Pt(23)
    bp0.font.bold = True
    bp0.font.color.rgb = c_emerald
    bp0.space_after = Pt(2)
    
    bp1 = btf.add_paragraph()
    bp1.alignment = PP_ALIGN.CENTER
    bp1.text = "Top Clues Found: processor (+0.35)  •  macbook (+0.32)  •  apple (+0.28)  •  battery (+0.18)"
    bp1.font.name = "Segoe UI"
    bp1.font.size = Pt(16)
    bp1.font.bold = True
    bp1.font.color.rgb = c_slate_dark
    
    # Single UI Screenshot (Centered, clean)
    pic_w = Inches(16.40)
    pic_h = Inches(7.70)
    pic_left = (prs.slide_width - pic_w) / 2
    pic_top = Inches(3.10)
    
    pic11 = s11.shapes.add_picture("docs/slide11_ui_screenshot.png", pic_left, pic_top, pic_w, pic_h)
    pic11.name = "Slide11_CleanScreenshot"

    # -------------------------------------------------------------
    # SLIDE 12: Handling Difficult Cases
    # -------------------------------------------------------------
    print("\n[Slide 12] Simplifying subtitle and card texts...")
    s12 = prs.slides[11]
    for shp in s12.shapes:
        if shp.shape_type == 6: # Group 38
            for sub in shp.shapes:
                if sub.name == "TextBox 5":
                    tf = sub.text_frame
                    tf.paragraphs[0].text = "Handling Difficult Cases"
                    if len(tf.paragraphs) > 1:
                        tf.paragraphs[1].text = "How NewsScope handles confusing words, bad text inputs, and large file uploads."
                elif sub.name == "TextBox 33":
                    sub.text_frame.paragraphs[0].text = "FastAPI checks all input text immediately to make sure nothing crashes or breaks the server."

    # -------------------------------------------------------------
    # SLIDE 13: Test Results & Accuracy
    # -------------------------------------------------------------
    print("\n[Slide 13] Simplifying subtitle and card texts...")
    s13 = prs.slides[12]
    for shp in s13.shapes:
        if shp.shape_type == 6: # Group 38
            for sub in shp.shapes:
                if sub.name == "TextBox 5":
                    tf = sub.text_frame
                    tf.paragraphs[0].text = "Test Results & Accuracy"
                    if len(tf.paragraphs) > 1:
                        tf.paragraphs[1].text = "Real test results on 445 brand new BBC news articles the AI had never seen before."
                elif sub.name == "TextBox 16":
                    sub.text_frame.paragraphs[0].text = "Tested on 445 new articles. The AI got 429 correct and made only 16 small mistakes."
                elif sub.name == "TextBox 33":
                    sub.text_frame.paragraphs[0].text = "Sport was easiest at 99.0%. Entertainment was 96.1%. Politics was 94.0% due to overlapping business words."

    # -------------------------------------------------------------
    # SLIDE 14: Future Roadmap
    # -------------------------------------------------------------
    print("\n[Slide 14] Adding clean subtitle and simple English...")
    s14 = prs.slides[13]
    for shp in s14.shapes:
        if shp.shape_type == 6: # Group 38
            for sub in shp.shapes:
                if sub.name == "TextBox 5":
                    tf = sub.text_frame
                    tf.paragraphs[0].text = "Future Roadmap"
                    if len(tf.paragraphs) > 1:
                        tf.paragraphs[1].text = "What we plan to build next to make NewsScope even more powerful."
                    else:
                        p = tf.add_paragraph()
                        p.text = "What we plan to build next to make NewsScope even more powerful."
                        p.font.name = "Segoe UI"
                        p.font.size = Pt(18)
                        p.font.color.rgb = c_slate_sub

    # -------------------------------------------------------------
    # SLIDE 15: Thank You
    # -------------------------------------------------------------
    print("\n[Slide 15] Polishing Thank You slide and URL...")
    s15 = prs.slides[14]
    for shp in s15.shapes:
        if shp.name == "TextBox 2":
            tf = shp.text_frame
            tf.paragraphs[0].text = "THANK YOU!"
            if len(tf.paragraphs) > 1:
                tf.paragraphs[1].text = "Questions & Feedback — NewsScope Project Evaluation"
        elif shp.name == "TextBox 25":
            tf = shp.text_frame
            tf.paragraphs[0].text = "Scan the QR code above or visit the project repository on GitHub:"
            tf.paragraphs[1].text = "https://github.com/Abhijeet0848/NewsScope"
            tf.paragraphs[2].text = "Full Source Code   •   Pretrained AI Models   •   Complete Academic Report"

    # Save to CruxTemplate
    prs.save(prs_path)
    print(f"\n[Saved] All 15 slides successfully polished in {prs_path}!")

    # Synchronize to NewsScope_Presentation.pptx
    target = "docs/NewsScope_Presentation.pptx"
    try:
        shutil.copy2(prs_path, target)
        print(f"[Synchronized] Successfully copied to {target}!")
    except Exception as e:
        print(f"[Error] Failed to copy to {target}: {e}")

if __name__ == "__main__":
    polish_presentation()
