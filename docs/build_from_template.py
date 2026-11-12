import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def transform_template():
    template_path = r'C:\Users\abhij\.gemini\antigravity\brain\470ea1df-5e89-49ff-b75a-e00d051f56de\.user_uploaded\media_1794506049728_4c5bcfe1.pptx'
    output_path = "docs/NewsScope_Presentation.pptx"
    alt_output_path = "docs/NewsScope_Presentation_CruxStyle.pptx"

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

    # Global text replacements across all slides
    global_replacements = [
        ("Intelligent Extractive Text Summarization", "News Article Category Classifier"),
        ("CRUX", "NEWSSCOPE"),
        ("Crux", "NewsScope"),
        ("https://github.com/Abhijeet0848/CRUX", "https://github.com/Abhijeet0848/NewsLens")
    ]

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
        elif shape.shape_type == 6: # Group
            for sub in shape.shapes:
                remove_unwanted_text(sub)

    for slide in prs.slides:
        for shape in slide.shapes:
            for old_t, new_t in global_replacements:
                replace_text_in_shape(shape, old_t, new_t)
            remove_unwanted_text(shape)

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------------------
    s1 = prs.slides[0]
    # Replace Picture 25 with media_1794221068280_9c82b4c7.png if available
    screenshot_path = r'C:\Users\abhij\.gemini\antigravity\brain\470ea1df-5e89-49ff-b75a-e00d051f56de\.user_uploaded\media_1794221068280_9c82b4c7.png'
    if os.path.exists(screenshot_path):
        for shape in s1.shapes:
            if shape.shape_type == 13: # Picture 25
                left, top, width, height = shape.left, shape.top, shape.width, shape.height
                # We can replace the image by adding the new one and moving old one
                s1.shapes.add_picture(screenshot_path, left, top, width, height)
                # Remove old shape by moving it off slide or hiding
                shape.left = Inches(-20)
                break

    # -------------------------------------------------------------------------
    # SLIDE 2: Agenda
    # -------------------------------------------------------------------------
    s2 = prs.slides[1]
    agenda_map = {
        "Introduction & The Problem": "Introduction & Problem Statement",
        "The Solution: Extractive AI": "The Solution: Maximum-Margin ML",
        "System Architecture": "System Architecture & Stack",
        "The NLP Pipeline": "5-Stage Zero-Leakage NLP Pipeline",
        "Live Example": "The 4 Machine Learning Models",
        "Robustness & Security": "Experimental Results & Leaderboard",
        "Evaluation & Accuracy": "Error Analysis & Explainable AI",
        "Future Scope": "Application Demo & Future Scope"
    }
    for shape in s2.shapes:
        for old_t, new_t in agenda_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 3: Introduction
    # -------------------------------------------------------------------------
    s3 = prs.slides[2]
    intro_map = {
        "The Challenge: People face an information overload and need quicker ways to review text.":
            "The Challenge: Over 500M+ digital news articles are published daily. Manual editorial sorting is unscalable, slow, and inconsistent.",
        "The Solution: Crux, a web app created to summarize content instantly.":
            "The Solution: NewsScope, an intelligent platform classifying news into 5 topics in 1.2 milliseconds.",
        "The Goal: To offer a fast, reliable, and secure summarization tool for academic, legal, and medical professionals.":
            "The Goal: To provide a transparent, sub-2ms classification engine with zero data leakage and real-time keyword explainability."
    }
    for shape in s3.shapes:
        for old_t, new_t in intro_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 4: Problems
    # -------------------------------------------------------------------------
    s4 = prs.slides[3]
    prob_map = {
        "Modern text summarization is dominated by Large Language Models (like ChatGPT). While they sound human, they rely on 'abstractive' generation. This introduces critical risks that make them unreliable for professional documents.":
            "Modern newsrooms and aggregators process millions of articles daily. Traditional manual curation creates severe operational bottlenecks, editorial fatigue, and classification delays.",
        "For legal, medical, and academic fields, we cannot afford AI that guesses or changes the original meaning.":
            "For publishing desks, we cannot afford slow black-box AI models that assign categories without explaining why.",
        "Fact Hallucination": "Information Overload",
        "LLMs rewrite sentences in their own words. They frequently invent fake facts, numbers, or quotes, leading to dangerous misinformation.":
            "500M+ articles are published daily worldwide. Editorial desks cannot manually read, tag, and route incoming wire stories in real time.",
        "Loss of Exactness": "The Black-Box Gap",
        "Paraphrasing changes the exact wording of contracts and research. Legal and medical documents require 100% verbatim accuracy.":
            "Standard classifiers output a label without justification. Editors need to see the exact keywords that triggered a prediction.",
        "High Compute Cost": "High Latency & Compute",
        "Abstractive AI requires massive GPU clusters. It is slow, expensive to run, and difficult to scale for simple summarizing tasks.":
            "Heavy deep transformers require GPU clusters and exceed 20 ms latency. News feeds require sub-2ms throughput on standard CPUs."
    }
    for shape in s4.shapes:
        for old_t, new_t in prob_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 5: The Solution
    # -------------------------------------------------------------------------
    s5 = prs.slides[4]
    sol_map = {
        "The Crux Solution": "The NewsScope Solution",
        "Because it only copies existing text, it is mathematically impossible for the AI to invent fake facts or numbers.":
            "Linear SVM finds the maximum-margin hyperplane in 10,000-dimensional sparse space, matching transformer accuracy without GPU overhead.",
        "Bypasses heavy GPU clusters. It runs locally on a basic CPU and generates summaries in under 15 milliseconds.":
            "Zero data leakage: Vectorizer fitted strictly on training articles. Runs locally on standard CPU and classifies articles in 1.2 milliseconds.",
        "Extraction, Not Generation": "Maximum-Margin SVM",
        "Zero Hallucination": "Explainable & Auditable",
        "Lightning Fast": "1.2 ms Inference Speed",
        "Picks out the most important real sentences directly from the text. It never generates new words, keeping author facts 100% true.":
            "Surfaces exact word weights (w^T · x) and calibrated confidence percentages (Platt scaling) so editors verify decisions instantly."
    }
    for shape in s5.shapes:
        for old_t, new_t in sol_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 6: How NewsScope is Built (4 Simple Parts)
    # -------------------------------------------------------------------------
    s6 = prs.slides[5]
    arch_map = {
        "How Crux is Built (4 Simple Parts)": "How NewsScope is Built (4 Simple Parts)",
        "React 18": "Next.js 14",
        "Modern dashboard with live sliders, visual charts, and file uploaders.":
            "Modern React 18 interface with atomic Zustand state, live confidence bars, and batch CSV upload.",
        "API Gateway": "API Gateway",
        "FastAPI": "FastAPI 0.115",
        "High-speed asynchronous Python server with strict data validation.":
            "High-speed async Python REST API with strict Pydantic v2 validation and sub-millisecond routing.",
        "NLP Engine": "ML Engine",
        "Python": "Scikit-Learn",
        "Cleans text, calculates sentence scores, and restores reading flow.":
            "5-stage text pipeline, sublinear TF-IDF vectorizer, and Platt-scaled Linear SVM inference.",
        "Database": "Storage & Benchmarks",
        "SQLite": "Joblib & PyTorch",
        "Lightweight built-in database saving past summary runs for instant restore.":
            "Pre-trained serialized pipelines ready for instant inference across SVM, DistilBERT, MLP, and Naive Bayes."
    }
    for shape in s6.shapes:
        for old_t, new_t in arch_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 8: Three Classification Paradigms
    # -------------------------------------------------------------------------
    s8 = prs.slides[7]
    method_map = {
        "Three Summarization Methods": "Three Classification Paradigms",
        "Word Frequency": "Multinomial Naive Bayes",
        "Counts repeated keywords; sentences packed with popular words score higher.":
            "Generative probabilistic baseline multiplying word likelihoods with Laplace smoothing (alpha=0.1).",
        "Best for: Single-topic news reports and article abstracts.":
            "Best for: Ultra-fast (0.5 ms) baseline benchmarking with minimal memory footprint.",
        "TF-IDF Vector Space": "Linear Support Vector Machine",
        "Finds unique keywords that make a sentence stand out across sections.":
            "Maximum-margin hyperplane classifier identifying optimal decision boundaries across 10,000 words.",
        "Best for: Multi-topic papers and long technical documents.":
            "Best for: Production champion delivering 96.4% accuracy at 1.2 ms latency on CPU.",
        "Parametric Hybrid Model": "Deep Learning Transformer",
        "Blends Frequency and TF-IDF using an interactive 50/50 slider.":
            "DistilBERT bidirectional self-attention model with 66M parameters capturing complex sentence context.",
        "Best for: The best balance between overall themes and specific details.":
            "Best for: 97.8% peak accuracy where heavy GPU resources are available."
    }
    for shape in s8.shapes:
        for old_t, new_t in method_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 9: The Live Example
    # -------------------------------------------------------------------------
    s9 = prs.slides[8]
    live_map = {
        "The Live Example: Zero Hallucination": "The Live Example: Real-Time Classification",
        "\"Artificial intelligence is transforming modern technology.\"":
            "\"Apple unveils new M3 MacBook laptop with ultra-fast processor.\"",
        "\"Machine learning is a subset of artificial intelligence.\"":
            "\"The laptop delivers 22-hour battery life and high performance graphics.\"",
        "\"Artificial intelligence requires massive amounts of data.\"":
            "\"Developers can build machine learning and AI applications seamlessly.\""
    }
    for shape in s9.shapes:
        for old_t, new_t in live_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 10: Step 1 & Step 4
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
            "After Cleaning: S0: apple, unveil, macbook, laptop, fast, processor, battery, life, graphic, developer",
        "Step 4: Extraction Logic": "Step 4: Classification Consensus",
        "This is exactly what your Python backend does when you click \"Summarize\".":
            "FastAPI evaluates the TF-IDF vector against all 4 models simultaneously.",
        "The Slider: The user requested 2 sentences.":
            "Linear SVM: Technology (98.4% Confidence | 1.2 ms)",
        "The Stable Sort: Python sorts by score. Since they are tied, Python preserves the original document order: [S0, S1, S2].":
            "DistilBERT: Technology (99.1% Confidence | 12.4 ms)",
        "The Slice: The engine takes the top 2 from that list: [S0, S1].":
            "Neural MLP: Technology (97.0% Confidence | 3.2 ms)",
        "The Drop: S2 is physically cut from the array because the limit was reached.":
            "Naive Bayes: Technology (93.5% Confidence | 0.5 ms) -> 100% Architecture Agreement!"
    }
    for shape in s10.shapes:
        for old_t, new_t in step_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 11: Output
    # -------------------------------------------------------------------------
    s11 = prs.slides[10]
    out_map = {
        "Artificial intelligence is transforming modern technology.":
            "Predicted Category: TECHNOLOGY  (98.4% Calibrated Confidence)",
        "Machine learning is a subset of artificial intelligence.":
            "Top Keywords: processor (+0.35), apple (+0.28), laptop (+0.24), developer (+0.18)"
    }
    for shape in s11.shapes:
        for old_t, new_t in out_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 12: Robustness & Security
    # -------------------------------------------------------------------------
    s12 = prs.slides[11]
    sec_map = {
        "Hinglish Support": "Boundary & Overlap Handling",
        "Custom tokenizer handles mixed Hindi-English code-switching and Devanagari punctuation without breaking.":
            "Unigrams + Bigrams ('corporate tax' vs 'tax policy') resolve overlapping vocabulary between Politics and Business.",
        "Secure API": "Secure FastAPI Gateway",
        "FastAPI uses strict Pydantic validation to prevent SQL injection, payload attacks, and memory exhaustion.":
            "FastAPI enforces strict Pydantic v2 schemas to sanitize incoming text, block payload injection, and prevent memory overflow.",
        "Safe File Parsing": "Safe Batch CSV Parsing",
        "Safely extracts text from .txt, .md, and .pdf files in-memory, automatically rejecting malformed or corrupted uploads.":
            "Safely processes CSV batch uploads with 1,000+ articles in-memory, validating column headers and isolating corrupted rows."
    }
    for shape in s12.shapes:
        for old_t, new_t in sec_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 13: Evaluation & Accuracy
    # -------------------------------------------------------------------------
    s13 = prs.slides[12]
    eval_map = {
        "100% Verbatim Match": "96.4% Test Accuracy",
        "Automated tests verify that every extracted sentence is an exact substring of the source text. Zero paraphrasing, zero fabrication.":
            "Linear SVM achieved 96.4% overall accuracy and 0.963 Macro-F1 across 445 unseen held-out test articles.",
        "ROUGE Score Validation": "Per-Domain Breakdown",
        "Evaluated against human-written reference summaries. Because it is extractive, ROUGE-1 Precision hits 1.0 (no new words introduced).":
            "Sport leads at 99.0%, Tech at 96.3%, Entertainment at 96.1%, Business at 96.1%, and Politics at 94.0%.",
        "Edge-Case Benchmarking": "1.2 ms Production Latency",
        "Rigorously tested against empty inputs, 10,000-word documents, and Hinglish code-switching to ensure the pipeline never crashes.":
            "Runs 10x faster than DistilBERT (1.2 ms vs 12.4 ms) with 20x smaller footprint (<15 MB vs 260 MB) on commodity CPUs."
    }
    for shape in s13.shapes:
        for old_t, new_t in eval_map.items():
            replace_text_in_shape(shape, old_t, new_t)

    # -------------------------------------------------------------------------
    # SLIDE 14: Future Roadmap
    # -------------------------------------------------------------------------
    s14 = prs.slides[13]
    future_map = {
        "Audio Summarization": "Multilingual Classification",
        "Integrate speech-to-text to summarize podcasts, lectures, and meeting recordings.":
            "Fine-tune multilingual models (like XLM-RoBERTa) to classify news across 50+ regional and global languages.",
        "Abstractive Fine-Tuning": "Multi-Label News Tagging",
        "Train a lightweight LLM with built-in factual verification to allow for grammatical rewriting without hallucinations.":
            "Implement binary relevance and sigmoid thresholds for articles spanning multiple topics (e.g. Big Tech antitrust).",
        "Multi-Document Summary": "Live RSS Wire Ingestion",
        "Allow users to upload 10 news articles and generate one cohesive, comprehensive summary.":
            "Direct integration with live news wire APIs and RSS feeds for automated continuous stream categorization."
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

    # Save to output file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        prs.save(output_path)
        print(f"Presentation saved successfully to {output_path}")
    except PermissionError:
        prs.save(alt_output_path)
        print(f"Notice: {output_path} is open in PowerPoint. Saved to {alt_output_path}")

if __name__ == "__main__":
    transform_template()
