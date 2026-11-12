import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def transform_template_simple_english():
    template_path = r'C:\Users\abhij\.gemini\antigravity\brain\470ea1df-5e89-49ff-b75a-e00d051f56de\.user_uploaded\media_1794506049728_4c5bcfe1.pptx'
    output_path = "docs/NewsScope_Presentation.pptx"
    alt_output_path = "docs/NewsScope_Presentation_Simple.pptx"

    prs = Presentation(template_path)

    # Helper function to recursively replace text in shapes or groups
    def replace_text_in_shape(shape, old_text, new_text):
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                if old_text in p.text:
                    p.text = p.text.replace(old_text, new_text)
        elif shape.shape_type == 6: # Group shape
            for subshape in shape.shapes:
                replace_text_in_shape(subshape, old_text, new_text)

    # Clean out placeholder numbers or leftover labels from template
    def remove_unwanted_text(shape):
        unwanted = [
            "Revenue Growth", "Return on Investment", "Customer Acquisition Cost",
            "Customer Satisfaction", "Objective 01", "Objective 02", "Lorem ipsum",
            "80%", "10%", "20%", "75%"
        ]
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                for unw in unwanted:
                    if unw in p.text:
                        p.text = p.text.replace(unw, "").strip()
        elif shape.shape_type == 6:
            for sub in shape.shapes:
                remove_unwanted_text(sub)

    # 1. Clean out template leftovers
    for slide in prs.slides:
        for shape in slide.shapes:
            remove_unwanted_text(shape)

    # Global replacements
    global_replacements = [
        ("Intelligent Extractive Text Summarization", "News Article Category Classifier"),
        ("CRUX", "NEWSSCOPE"),
        ("Crux", "NewsScope")
    ]
    for slide in prs.slides:
        for shape in slide.shapes:
            for old_t, new_t in global_replacements:
                replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 1: Cover Page
    # -------------------------------------------------------------------------
    s1 = prs.slides[0]
    screenshot_path = r'C:\Users\abhij\.gemini\antigravity\brain\470ea1df-5e89-49ff-b75a-e00d051f56de\.user_uploaded\media_1794221068280_9c82b4c7.png'
    if os.path.exists(screenshot_path):
        for shape in s1.shapes:
            if shape.shape_type == 13: # Picture 25
                left, top, width, height = shape.left, shape.top, shape.width, shape.height
                s1.shapes.add_picture(screenshot_path, left, top, width, height)
                shape.left = Inches(-20)
                break

    # -------------------------------------------------------------------------
    # SLIDE 2: Agenda (Simple English)
    # -------------------------------------------------------------------------
    s2 = prs.slides[1]
    agenda_map = {
        "Introduction & The Problem": "The Big Problem",
        "The Solution: Extractive AI": "Our Smart Solution",
        "System Architecture": "How It Is Built (Architecture)",
        "The NLP Pipeline": "5-Step Text Preprocessing",
        "Live Example": "The 4 AI Models Tested",
        "Robustness & Security": "Step-by-Step Live Example",
        "Evaluation & Accuracy": "Test Results & Accuracy",
        "Future Scope": "Future Plans & Conclusion"
    }
    for shape in s2.shapes:
        for old_t, new_t in agenda_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 3: Introduction (Simple English)
    # -------------------------------------------------------------------------
    s3 = prs.slides[2]
    intro_map = {
        "The Challenge: People face an information overload and need quicker ways to review text.":
            "The Challenge: Too Much News. Millions of articles are published online daily. Humans cannot read and sort them all by hand.",
        "The Solution: Crux, a web app created to summarize content instantly.":
            "The Solution: NewsScope. A fast, smart web tool that reads any news article and categorizes it in just 1 millisecond.",
        "The Goal: To offer a fast, reliable, and secure summarization tool for academic, legal, and medical professionals.":
            "The Goal: Help news websites, editors, and readers organize news instantly and explain why each category was chosen."
    }
    for shape in s3.shapes:
        for old_t, new_t in intro_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 4: Problems (Simple English)
    # -------------------------------------------------------------------------
    s4 = prs.slides[3]
    prob_map = {
        "Modern text summarization is dominated by Large Language Models (like ChatGPT). While they sound human, they rely on 'abstractive' generation. This introduces critical risks that make them unreliable for professional documents.":
            "Over 500 million news articles appear online every day. Sorting them by hand is too slow, expensive, and tiring for human editors. Regular AI models are 'black boxes'—they give a category without explaining why.",
        "For legal, medical, and academic fields, we cannot afford AI that guesses or changes the original meaning.":
            "News editors and readers need an AI tool that is super fast, fair, and clearly explains its work.",
        "Fact Hallucination": "Information Overload",
        "LLMs rewrite sentences in their own words. They frequently invent fake facts, numbers, or quotes, leading to dangerous misinformation.":
            "Millions of articles are published daily. Editors cannot tag thousands of stories by hand fast enough.",
        "Loss of Exactness": "The Black-Box Gap",
        "Paraphrasing changes the exact wording of contracts and research. Legal and medical documents require 100% verbatim accuracy.":
            "Most AI tools just give an answer. They don't show which words caused the decision, making them hard to trust.",
        "High Compute Cost": "Slow & Expensive AI",
        "Abstractive AI requires massive GPU clusters. It is slow, expensive to run, and difficult to scale for simple summarizing tasks.":
            "Large AI models need expensive supercomputers. They are too slow and costly for instant news updates."
    }
    for shape in s4.shapes:
        for old_t, new_t in prob_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 5: The Solution (Simple English)
    # -------------------------------------------------------------------------
    s5 = prs.slides[4]
    sol_map = {
        "The Crux Solution": "The NewsScope Solution",
        "Because it only copies existing text, it is mathematically impossible for the AI to invent fake facts or numbers.":
            "Draws a clear dividing line between news topics. It reaches 96.4% accuracy without needing big, expensive supercomputers.",
        "Bypasses heavy GPU clusters. It runs locally on a basic CPU and generates summaries in under 15 milliseconds.":
            "Zero Data Leakage: We kept test articles completely separate. It runs on a normal laptop and sorts articles in 1.2 milliseconds.",
        "Extraction, Not Generation": "Draws a Clear Line",
        "Zero Hallucination": "Shows Its Work",
        "Lightning Fast": "1.2 ms Speed",
        "Picks out the most important real sentences directly from the text. It never generates new words, keeping author facts 100% true.":
            "Shows the exact words that caused the decision, plus an honest confidence score, so editors can verify predictions instantly."
    }
    for shape in s5.shapes:
        for old_t, new_t in sol_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 6: How NewsScope is Built (Simple English)
    # -------------------------------------------------------------------------
    s6 = prs.slides[5]
    arch_map = {
        "How Crux is Built (4 Simple Parts)": "How NewsScope is Built (4 Simple Parts)",
        "A modern full-stack decoupled architecture built for speed and maintainability.":
            "A clean system split into two halves: the screen you see and the engine that does the math.",
        "React 18": "Next.js 14",
        "Modern dashboard with live sliders, visual charts, and file uploaders.":
            "The screen you see. Fast, modern web page where typing never freezes or lags.",
        "API Gateway": "API Gateway",
        "FastAPI": "FastAPI",
        "High-speed asynchronous Python server with strict data validation.":
            "The waiter. Takes your article text, checks it safely, and sends it to the math engine in 1 millisecond.",
        "NLP Engine": "ML Engine",
        "Python": "Scikit-Learn",
        "Cleans text, calculates sentence scores, and restores reading flow.":
            "The kitchen. Cleans the text, turns words into numbers, and calculates topic scores.",
        "Database": "Saved Models",
        "SQLite": "Joblib",
        "Lightweight built-in database saving past summary runs for instant restore.":
            "The recipe book. Saved pre-trained models ready to give answers instantly."
    }
    for shape in s6.shapes:
        for old_t, new_t in arch_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 8: The 3 Models (Simple English)
    # -------------------------------------------------------------------------
    s8 = prs.slides[7]
    method_map = {
        "Three Summarization Methods": "The AI Models We Tested",
        "Word Frequency": "Naive Bayes (Simple Guesser)",
        "Counts repeated keywords; sentences packed with popular words score higher.":
            "Uses simple probability. It guesses based on word frequencies. Fast (0.5 ms), but makes simple mistakes.",
        "Best for: Single-topic news reports and article abstracts.":
            "Best for: A quick, lightweight baseline.",
        "TF-IDF Vector Space": "Linear SVM (Our Winner ⭐)",
        "Finds unique keywords that make a sentence stand out across sections.":
            "Draws a straight dividing line between topics in 10,000-word space. 96.4% accurate and super fast (1.2 ms).",
        "Best for: Multi-topic papers and long technical documents.":
            "Best for: Real-world news websites that need speed and high accuracy.",
        "Parametric Hybrid Model": "DistilBERT (The Bookworm)",
        "Blends Frequency and TF-IDF using an interactive 50/50 slider.":
            "Deep learning transformer that reads full sentences forward and backward to understand context (97.8% accurate).",
        "Best for: The best balance between overall themes and specific details.":
            "Best for: Offline research where speed doesn't matter."
    }
    for shape in s8.shapes:
        for old_t, new_t in method_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 9: The Live Example (Simple English)
    # -------------------------------------------------------------------------
    s9 = prs.slides[8]
    live_map = {
        "The Live Example: Zero Hallucination": "The Live Example: Step-by-Step",
        "\"Artificial intelligence is transforming modern technology.\"":
            "\"Apple unveils new M3 MacBook laptop with ultra-fast processor.\"",
        "\"Machine learning is a subset of artificial intelligence.\"":
            "\"The laptop delivers 22-hour battery life and high performance graphics.\"",
        "\"Artificial intelligence requires massive amounts of data.\"":
            "\"Developers can build machine learning applications seamlessly.\""
    }
    for shape in s9.shapes:
        for old_t, new_t in live_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 10: Steps 1 to 4 (Simple English)
    # -------------------------------------------------------------------------
    s10 = prs.slides[9]
    step_map = {
        "S0: \"Artificial intelligence is transforming modern technology.\"":
            "S0: \"Apple unveils new M3 MacBook laptop with ultra-fast processor...\"",
        "S1: \"Machine learning is a subset of artificial intelligence.\"":
            "S1: \"The laptop delivers 22-hour battery life and high performance graphics...\"",
        "S2: \"Artificial intelligence requires massive amounts of data.“":
            "S2: \"Developers can build machine learning applications seamlessly...\"",
        "After Cleaning (Lemmatized): S0: artificial, intelligence, transform, modern, technology":
            "After Cleaning: apple, unveil, macbook, laptop, fast, processor, battery, life, graphic, developer (removed useless filler words).",
        "Step 4: Extraction Logic": "Step 4: What the AI Models Predicted",
        "This is exactly what your Python backend does when you click \"Summarize\".":
            "All 4 models evaluate the text simultaneously:",
        "The Slider: The user requested 2 sentences.":
            "Linear SVM: Technology (98.4% Confidence | 1.2 ms)",
        "The Stable Sort: Python sorts by score. Since they are tied, Python preserves the original document order: [S0, S1, S2].":
            "DistilBERT: Technology (99.1% Confidence | 12.4 ms)",
        "The Slice: The engine takes the top 2 from that list: [S0, S1].":
            "Neural MLP: Technology (97.0% Confidence | 3.2 ms)",
        "The Drop: S2 is physically cut from the array because the limit was reached.":
            "Naive Bayes: Technology (93.5% Confidence | 0.5 ms) -> 100% agreement across all 4 models!"
    }
    for shape in s10.shapes:
        for old_t, new_t in step_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 11: Final Output (Simple English)
    # -------------------------------------------------------------------------
    s11 = prs.slides[10]
    out_map = {
        "OUTPUT": "FINAL RESULT",
        "Artificial intelligence is transforming modern technology.":
            "Predicted Category: TECHNOLOGY  (98.4% Calibrated Confidence)",
        "Machine learning is a subset of artificial intelligence.":
            "Top Words Found: processor (+0.35), apple (+0.28), laptop (+0.24), developer (+0.18)"
    }
    for shape in s11.shapes:
        for old_t, new_t in out_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 12: Robustness (Simple English)
    # -------------------------------------------------------------------------
    s12 = prs.slides[11]
    sec_map = {
        "Robustness & Security": "Handling Difficult Cases",
        "Hinglish Support": "Two-Word Clues (Bigrams)",
        "Custom tokenizer handles mixed Hindi-English code-switching and Devanagari punctuation without breaking.":
            "Politics and Business share words like 'tax'. Teaching the AI phrases like 'tax budget' vs 'corporate tax' fixed the confusion.",
        "Secure API": "Safe & Protected API",
        "FastAPI uses strict Pydantic validation to prevent SQL injection, payload attacks, and memory exhaustion.":
            "FastAPI checks all input text immediately to make sure nothing crashes or attacks the server.",
        "Safe File Parsing": "Safe File Uploads",
        "Safely extracts text from .txt, .md, and .pdf files in-memory, automatically rejecting malformed or corrupted uploads.":
            "Users can upload spreadsheets (CSV) with 1,000 articles. The app reads them safely and skips broken rows."
    }
    for shape in s12.shapes:
        for old_t, new_t in sec_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 13: Results & Accuracy (Simple English)
    # -------------------------------------------------------------------------
    s13 = prs.slides[12]
    eval_map = {
        "Evaluation & Accuracy": "Test Results & Accuracy",
        "100% Verbatim Match": "96.4% Overall Accuracy",
        "Automated tests verify that every extracted sentence is an exact substring of the source text. Zero paraphrasing, zero fabrication.":
            "Tested on 445 brand new, unseen BBC articles. It got 429 correct and made only 16 small mistakes.",
        "ROUGE Score Validation": "Scores by Category",
        "Evaluated against human-written reference summaries. Because it is extractive, ROUGE-1 Precision hits 1.0 (no new words introduced).":
            "Sport was easiest at 99.0%. Entertainment was 96.1%. Politics was 94.0% due to overlapping economic words.",
        "Edge-Case Benchmarking": "10x Faster Speed",
        "Rigorously tested against empty inputs, 10,000-word documents, and Hinglish code-switching to ensure the pipeline never crashes.":
            "Runs in 1.2 milliseconds. It is 10 times faster than deep learning models and takes 20 times less memory."
    }
    for shape in s13.shapes:
        for old_t, new_t in eval_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 14: Future Roadmap (Simple English)
    # -------------------------------------------------------------------------
    s14 = prs.slides[13]
    future_map = {
        "Audio Summarization": "More Languages",
        "Integrate speech-to-text to summarize podcasts, lectures, and meeting recordings.":
            "Teach the AI to classify news in Hindi, Spanish, and French, not just English.",
        "Abstractive Fine-Tuning": "Multiple Topics at Once",
        "Train a lightweight LLM with built-in factual verification to allow for grammatical rewriting without hallucinations.":
            "Allow an article to be both Tech and Business at the same time if it covers both.",
        "Multi-Document Summary": "Live News Feeds",
        "Allow users to upload 10 news articles and generate one cohesive, comprehensive summary.":
            "Connect directly to live news wires to sort articles automatically 24/7."
    }
    for shape in s14.shapes:
        for old_t, new_t in future_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 15: Thank You Slide
    # -------------------------------------------------------------------------
    s15 = prs.slides[14]
    for shape in s15.shapes:
        replace_text_in_shape(shape, "https://github.com/Abhijeet0848/CRUX", "https://github.com/Abhijeet0848/NewsLens")
        replace_text_in_shape(shape, "https://github.com/Abhijeet0848/NEWSSCOPE", "https://github.com/Abhijeet0848/NewsLens")

    # Save to disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        prs.save(output_path)
        print(f"Presentation saved successfully to {output_path}")
    except PermissionError:
        prs.save(alt_output_path)
        print(f"Notice: {output_path} is open in PowerPoint. Saved to {alt_output_path}")

if __name__ == "__main__":
    transform_template_simple_english()
