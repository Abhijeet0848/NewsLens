# NewsScope — 3-Minute Academic Demo Video Script
**Format:** Loom Screen Recording with Voiceover  
**Tone:** Academic, Factual, Engineering-Focused (Zero Marketing Fluff)  
**Total Target Duration:** 3 minutes (180 seconds)  

---

### Section 1: Introduction to NewsScope (0:00 – 0:15)

- **Timestamp:** `0:00 – 0:15` (15s)
- **Action to Perform:** 
  - Start recording on the NewsScope homepage (`http://localhost:3000` or deployed URL).
  - Hover cursor over the main title heading: *"NewsScope — News Article Category Classifier"*.
  - Keep camera/screen centered on the hero section.
- **On-Screen Annotation:** 
  - `[CALLOUT: NewsScope — Production NLP & ML System]`
  - `[HIGHLIGHT: Subtitle — 5 BBC Domains & Calibrated Linear SVM]`
- **Spoken Script (Voiceover):**
  > "Hello. This is the demonstration of NewsScope, an end-to-end natural language processing and machine learning system for automated news article categorization. Developed as an MCA academic project, NewsScope ingests raw, unstructured news articles and classifies them into five BBC domains using a Platt-calibrated Linear Support Vector Machine operating over a 10,000-dimensional TF-IDF feature space."

---

### Section 2: Homepage & Taxonomy Tour (0:15 – 0:45)

- **Timestamp:** `0:15 – 0:45` (30s)
- **Action to Perform:** 
  - Slowly scroll past the hero down to the 5 category badges: Business, Entertainment, Politics, Sport, Technology.
  - Hover briefly over each category pill to show the distinct theme colors and dataset distribution counts.
  - Point out the quick navigation bar at the top (`Classifier`, `Batch`, `Analytics`, `Architecture`).
  - Click on the **"Classify Article"** CTA button or `Classifier` in the navbar to navigate to `/classifier`.
- **On-Screen Annotation:** 
  - `[HIGHLIGHT: 5 BBC Domains — Business, Entertainment, Politics, Sport, Technology]`
  - `[CALLOUT: 2,225 BBC News Corpus Articles · 80/20 Stratified Split]`
  - `[ZOOM: Navbar Navigation Links]`
- **Spoken Script (Voiceover):**
  > "The system is trained on the benchmark BBC News corpus comprising 2,225 articles balanced across five canonical categories: Business, Entertainment, Politics, Sport, and Technology. The dataset was split into an 80% stratified training partition and a 20% held-out test partition with strict zero data leakage. Let us navigate directly to the interactive classifier interface to examine the real-time inference pipeline."

---

### Section 3: Live Test 1 — Sport Article (0:45 – 1:30)

- **Timestamp:** `0:45 – 1:30` (45s)
- **Action to Perform:** 
  - Show the clean two-column classifier interface.
  - Paste the sample Sport article into the textarea:
    > *"Real Madrid secured their 15th Champions League title on Saturday, defeating Borussia Dortmund 2-0 at Wembley Stadium. Goals from Dani Carvajal and Vinícius Júnior sealed the victory in front of 86,000 spectators at the iconic London venue."*
  - Point out word count badge updating dynamically (`41 words`).
  - Click **"Classify Article"** (or press `Ctrl + Enter`).
  - Result card renders instantly on the right.
  - Hover over the green **"Sport"** badge, then the confidence meter (`86.1%`), the latency readout (`~3.7 ms`), and the top salient keyword chips (`league`, `champions`, `wembley`, `madrid`, `title`).
- **On-Screen Annotation:** 
  - `[ZOOM: Article Content Input textarea]`
  - `[HIGHLIGHT: Classified Result — Sport Badge ✅]`
  - `[HIGHLIGHT: Confidence — 86.1%]`
  - `[CALLOUT: Latency: 3.7 ms · Calibrated Sigmoidal Probability]`
  - `[ZOOM: Salient Keywords — TF-IDF Weight Attribution]`
- **Spoken Script (Voiceover):**
  > "We first input a real-world sports dispatch detailing Real Madrid's Champions League victory. Upon execution, the FastAPI backend processes the request in under 4 milliseconds. The system categorizes the document as Sport with 86.1% calibrated confidence. Unlike standard SVM decision scores which are arbitrary geometric distances, our pipeline applies Platt scaling via CalibratedClassifierCV to produce a statistically valid posterior probability distribution. Notice the keyword saliency panel below: terms like 'champions', 'wembley', and 'madrid' carry the highest positive TF-IDF feature weights."

---

### Section 4: Live Test 2 — Technology Article (1:30 – 2:00)

- **Timestamp:** `1:30 – 2:00` (30s)
- **Action to Perform:** 
  - Click **"Clear"** or select all in the textarea and delete.
  - Paste the Tech article:
    > *"Apple unveiled its M4 chip at the WWDC 2024 keynote, claiming 40% faster neural engine performance for on-device AI tasks. The new processor debuts in the iPad Pro lineup this fall, followed by the MacBook Pro in early 2025."*
  - Click **"Classify Article"**.
  - Show the result update: **Tech**, **85.8% Confidence**, latency `~3.5 ms`.
  - Point to the horizontal distribution bar: Tech dominates at ~86%, with minor secondary probability for Business (~7%), and near-zero for Sport.
- **On-Screen Annotation:** 
  - `[ZOOM: Textarea with Tech Article]`
  - `[HIGHLIGHT: Predicted: Tech ✅ · 85.8% Confidence]`
  - `[CALLOUT: Categorical Distribution — Tech 85.8%, Business 6.8%, Sport 0.8%]`
- **Spoken Script (Voiceover):**
  > "Next, we evaluate an unseen technology article regarding Apple's M4 processor announcement. The model correctly assigns the Tech domain with 85.8% confidence. The probability distribution demonstrates sharp discriminative boundary separation: Technology captures 85.8%, Business registers a minor 6.8% due to commercial hardware context, while Sport and Entertainment remain near zero. This validates the effectiveness of our 10,000 unigram-plus-bigram feature vocabulary."

---

### Section 5: Robustness & Edge-Case Handling — Gibberish (2:00 – 2:20)

- **Timestamp:** `2:00 – 2:20` (20s)
- **Action to Perform:** 
  - Clear the textarea.
  - Type meaningless, non-informative gibberish:
    > *"asdkjfh askdjfh zxncvbb qwerpoi mnbvcxz lkjhgf poiuyt"*
  - Click **"Classify Article"**.
  - Show the result: Confidence drops significantly, and the 5-class distribution splits flatly (near-uniform ~20% across categories).
- **On-Screen Annotation:** 
  - `[ZOOM: Adversarial Gibberish Input]`
  - `[CALLOUT: Robustness Check — Out-of-Vocabulary Input]`
  - `[HIGHLIGHT: Uniform Probability Distribution (~20% per domain)]`
- **Spoken Script (Voiceover):**
  > "To evaluate adversarial resilience and boundary handling, we input random out-of-vocabulary character sequences. Notice how the system behaves safely: rather than generating an overconfident false prediction or throwing an unhandled exception, the calibrated model outputs a diffuse, near-uniform probability distribution across all five domains, signaling high classification entropy and uncertainty."

---

### Section 6: Analytics Page & Empirical Benchmark (2:20 – 2:40)

- **Timestamp:** `2:20 – 2:40` (20s)
- **Action to Perform:** 
  - Click **"Analytics"** in the top navigation bar to go to `/analytics`.
  - Point cursor across the top metric cards: Test Accuracy (`96.4%`), Macro F1 (`0.963`), Precision (`0.964`), Recall (`0.963`).
  - Scroll down to the **Architecture Comparison Leaderboard** table:
    - Linear SVM: 96.4% Accuracy, 1.2 ms
    - DistilBERT: 97.8% Accuracy, 12.4 ms
    - Neural MLP: 95.1% Accuracy, 3.2 ms
    - Naive Bayes: 92.1% Accuracy, 0.5 ms
  - Hover over the Confusion Matrix heatmap showing actual vs predicted counts.
- **On-Screen Annotation:** 
  - `[ZOOM: Metric Cards — Accuracy 96.4%, Macro F1 0.963]`
  - `[HIGHLIGHT: Leaderboard — 4 Algorithmic Paradigms Benchmarked]`
  - `[ZOOM: 5x5 Confusion Matrix Heatmap]`
- **Spoken Script (Voiceover):**
  > "Moving to the Analytics dashboard, all metrics shown are dynamically loaded from our held-out 445-article test evaluation. The champion Linear SVM achieves 96.4% accuracy and a 0.963 Macro F1 score with 1.2-millisecond CPU latency. Our comparative benchmark contrasts this against a Multinomial Naive Bayes baseline at 92.1%, an MLP neural network at 95.1%, and fine-tuned DistilBERT at 97.8%. The 5-by-5 confusion matrix confirms high diagonal purity, with Sport reaching 99% recall."

---

### Section 7: Architecture Page & Mathematical Foundations (2:40 – 2:55)

- **Timestamp:** `2:40 – 2:55` (15s)
- **Action to Perform:** 
  - Click **"Architecture"** in the top navigation bar to go to `/architecture`.
  - Scroll smoothly through the 5-stage NLP pipeline diagram:
    - Cleaning $\to$ Tokenization $\to$ Stop-words $\to$ Lemmatization $\to$ TF-IDF.
  - Pause briefly on the mathematical formulation card for Soft-Margin Linear SVM: $\min \frac{1}{2}\|\mathbf{w}\|^2 + C\sum\xi_i$.
- **On-Screen Annotation:** 
  - `[ZOOM: 5-Stage NLP Pipeline Diagram]`
  - `[HIGHLIGHT: Soft-Margin Primal Formulation: min 1/2||w||² + C∑ξᵢ]`
  - `[CALLOUT: Sublinear TF-IDF + Platt Calibration Architecture]`
- **Spoken Script (Voiceover):**
  > "The Architecture section documents the theoretical foundations. The five-stage pipeline enforces text normalization, NLTK stop-word removal, WordNet lemmatization, and sublinear TF-IDF extraction. High-dimensional text spaces are naturally linearly separable, allowing the soft-margin SVM to construct maximum-margin hyperplanes that generalize with minimal computational overhead."

---

### Section 8: Wrap Up & Conclusion (2:55 – 3:00)

- **Timestamp:** `2:55 – 3:00` (5s)
- **Action to Perform:** 
  - Scroll up to the header or return to homepage.
  - Show clean live URL in browser address bar (`abhijeetkumar.dpdns.org`).
- **On-Screen Annotation:** 
  - `[CALLOUT: Deployed on Vercel · Full-Stack Serverless]`
  - `[HIGHLIGHT: NewsScope — Fully Functional MCA Academic Project]`
- **Spoken Script (Voiceover):**
  > "In conclusion, NewsScope delivers a verifiable, reproducible, and production-deployed text classification system. Thank you."

---

### Quick Recording Checklist for the Presenter

1. **Browser State Before Hitting Record:**
   - Close all unnecessary tabs.
   - Zoom browser viewport to 100% or 110% for crisp text legibility.
   - Have the Sport and Tech article texts copied to a notepad on a second screen or side window for instant pasting.
2. **Audio Setup:**
   - Use a clear external microphone or headset.
   - Speak at an even, steady academic pace (~130 words per minute).
3. **Loom Settings:**
   - Select **Screen Only** or **Screen + Small Bubble Cam** in lower corner.
   - Resolution: 1080p Full HD.
