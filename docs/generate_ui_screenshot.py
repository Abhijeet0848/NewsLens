import os
from PIL import Image, ImageDraw, ImageFont

def generate_ui_screenshot():
    # 2000 x 1100 high-res UI mockup
    W, H = 2000, 1100
    img = Image.new("RGBA", (W, H), (248, 250, 252, 255)) # Soft slate background #F8FAFC
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    def get_font(size, bold=False):
        names = ["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
        for n in names:
            p = os.path.join(r"C:\Windows\Fonts", n)
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except:
                    pass
        return ImageFont.load_default()

    font_title = get_font(38, bold=True)
    font_sub = get_font(18, bold=False)
    font_h2 = get_font(28, bold=True)
    font_h3 = get_font(20, bold=True)
    font_body = get_font(16, bold=False)
    font_body_bold = get_font(16, bold=True)
    font_badge = get_font(14, bold=True)
    font_mono = get_font(16, bold=True)
    font_small = get_font(14, bold=False)
    
    # 1. Top Browser / App Navigation Bar
    draw.rectangle([0, 0, W, 70], fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)
    
    # Browser window dots
    draw.ellipse([30, 28, 44, 42], fill=(239, 68, 68, 255))   # Red
    draw.ellipse([54, 28, 68, 42], fill=(245, 158, 11, 255))  # Yellow
    draw.ellipse([78, 28, 92, 42], fill=(16, 185, 129, 255))  # Green
    
    # App Logo & Brand
    logo_icon_path = "public/logo-icon.png"
    if os.path.exists(logo_icon_path):
        icon_small = Image.open(logo_icon_path).resize((36, 36), Image.Resampling.LANCZOS)
        img.paste(icon_small, (130, 17), icon_small)
    draw.text((175, 20), "NewsScope", fill=(15, 23, 42, 255), font=get_font(24, bold=True))
    draw.text((315, 26), "AI Article Classifier", fill=(100, 116, 139, 255), font=get_font(15, bold=False))
    
    # Nav tabs
    tabs = ["Classifier", "Batch Upload", "Model Analytics", "Architecture"]
    tx = 650
    for i, t in enumerate(tabs):
        is_active = (i == 0)
        t_col = (79, 70, 229, 255) if is_active else (100, 116, 139, 255)
        draw.text((tx, 25), t, fill=t_col, font=get_font(16, bold=is_active))
        if is_active:
            draw.rectangle([tx, 66, tx + 75, 70], fill=(79, 70, 229, 255))
        tx += 170
        
    # Right pill: Model Active
    draw.rounded_rectangle([W - 320, 18, W - 40, 52], radius=17, fill=(238, 242, 255, 255), outline=(199, 210, 254, 255), width=1)
    draw.text((W - 300, 25), "Model: Linear SVM (Platt)", fill=(67, 56, 202, 255), font=get_font(14, bold=True))
    
    # 2. Main Content Grid (Left: Input Panel, Right: Result Dashboard)
    
    # ================= LEFT: INPUT PANEL =================
    left_x0, left_y0, left_x1, left_y1 = 60, 105, 930, 1045
    draw.rounded_rectangle([left_x0, left_y0, left_x1, left_y1], radius=16, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)
    
    draw.text((left_x0 + 35, left_y0 + 30), "Article Content Input", fill=(15, 23, 42, 255), font=font_h2)
    draw.text((left_x0 + 35, left_y0 + 72), "Paste raw news text below to evaluate real-time multi-model inference.", fill=(100, 116, 139, 255), font=font_body)
    
    # Textarea container
    ta_x0, ta_y0, ta_x1, ta_y1 = left_x0 + 35, left_y0 + 115, left_x1 - 35, left_y0 + 440
    draw.rounded_rectangle([ta_x0, ta_y0, ta_x1, ta_y1], radius=12, fill=(248, 250, 252, 255), outline=(203, 213, 225, 255), width=2)
    
    sample_text = (
        "Apple unveils new M3 MacBook laptop with ultra-fast processor.\n"
        "The laptop delivers 22-hour battery life and high performance graphics.\n"
        "Developers can build machine learning applications seamlessly."
    )
    ty = ta_y0 + 25
    for line in sample_text.split("\n"):
        draw.text((ta_x0 + 25, ty), line, fill=(51, 65, 85, 255), font=get_font(18, bold=False))
        ty += 34
        
    # Textarea metadata footer
    draw.text((ta_x0 + 25, ta_y1 - 35), "Words: 28   Characters: 204   Extracted Tokens: 23   Pipeline Latency: 1.20 ms", fill=(100, 116, 139, 255), font=font_small)
    
    # Model Selector Radio Buttons inside Left Panel
    draw.text((left_x0 + 35, left_y0 + 475), "Select Active Inference Model:", fill=(15, 23, 42, 255), font=font_h3)
    
    models_info = [
        ("Linear SVM (Champion)", "1.2 ms latency | 96.4% test accuracy | Platt-scaled probabilities", True),
        ("DistilBERT Transformer", "12.4 ms latency | 97.8% test accuracy | 66M parameters attention", False),
        ("Neural MLP Baseline", "3.2 ms latency | 95.1% test accuracy | 2-layer dense network", False),
        ("Naive Bayes Baseline", "0.5 ms latency | 92.1% test accuracy | Multinomial frequency", False),
    ]
    my = left_y0 + 520
    for name, desc, sel in models_info:
        bg = (238, 242, 255, 255) if sel else (255, 255, 255, 255)
        bdr = (99, 102, 241, 255) if sel else (226, 232, 240, 255)
        draw.rounded_rectangle([left_x0 + 35, my, left_x1 - 35, my + 64], radius=10, fill=bg, outline=bdr, width=2 if sel else 1)
        
        # Radio circle
        draw.ellipse([left_x0 + 55, my + 22, left_x0 + 75, my + 42], outline=(99, 102, 241, 255) if sel else (203, 213, 225, 255), width=2)
        if sel:
            draw.ellipse([left_x0 + 60, my + 27, left_x0 + 70, my + 37], fill=(99, 102, 241, 255))
            
        draw.text((left_x0 + 90, my + 12), name, fill=(15, 23, 42, 255) if sel else (51, 65, 85, 255), font=font_body_bold)
        draw.text((left_x0 + 90, my + 35), desc, fill=(79, 70, 229, 255) if sel else (100, 116, 139, 255), font=font_small)
        my += 76
        
    # Classify Button (Active state)
    btn_x0, btn_y0, btn_x1, btn_y1 = left_x0 + 35, left_y1 - 85, left_x1 - 35, left_y1 - 25
    draw.rounded_rectangle([btn_x0, btn_y0, btn_x1, btn_y1], radius=12, fill=(79, 70, 229, 255))
    btn_text = "Classified Successfully in 1.20 ms"
    btn_bb = draw.textbbox((0, 0), btn_text, font=get_font(20, bold=True))
    btn_w = btn_bb[2] - btn_bb[0]
    draw.text((btn_x0 + (left_x1 - left_x0 - 70 - btn_w) // 2, btn_y0 + 17), btn_text, fill=(255, 255, 255, 255), font=get_font(20, bold=True))
    
    # ================= RIGHT: RESULT PANEL =================
    rx0, ry0, rx1, ry1 = 980, 105, W - 60, 1045
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=16, fill=(255, 255, 255, 255), outline=(226, 232, 240, 255), width=2)
    
    # Card Header
    draw.text((rx0 + 40, ry0 + 30), "PREDICTED BBC DOMAIN", fill=(100, 116, 139, 255), font=font_sub)
    draw.text((rx0 + 40, ry0 + 60), "Technology", fill=(15, 23, 42, 255), font=get_font(44, bold=True))
    
    # Green Verified Badge
    badge_x0 = rx0 + 320
    badge_y0 = ry0 + 72
    draw.rounded_rectangle([badge_x0, badge_y0, badge_x0 + 135, badge_y0 + 36], radius=18, fill=(236, 253, 245, 255), outline=(167, 243, 208, 255), width=2)
    # Checkmark drawn
    draw.line([badge_x0 + 18, badge_y0 + 19, badge_x0 + 24, badge_y0 + 25], fill=(4, 120, 87, 255), width=3)
    draw.line([badge_x0 + 24, badge_y0 + 25, badge_x0 + 34, badge_y0 + 13], fill=(4, 120, 87, 255), width=3)
    draw.text((badge_x0 + 42, badge_y0 + 8), "Verified", fill=(4, 120, 87, 255), font=get_font(15, bold=True))
    
    # Latency badge
    draw.text((rx0 + 40, ry0 + 125), "Latency: 1.20 ms  |  Zero Data Leakage Pipeline", fill=(5, 150, 105, 255), font=font_mono)
    
    # Right side of Header: Big Confidence
    draw.text((rx1 - 260, ry0 + 30), "CALIBRATED CONFIDENCE", fill=(100, 116, 139, 255), font=font_sub)
    draw.text((rx1 - 260, ry0 + 58), "98.4%", fill=(15, 23, 42, 255), font=get_font(46, bold=True))
    
    # Divider line
    draw.line([rx0 + 40, ry0 + 165, rx1 - 40, ry0 + 165], fill=(241, 245, 249, 255), width=2)
    
    # 5-Domain Probability Distribution
    draw.text((rx0 + 40, ry0 + 190), "5-CATEGORY PROBABILITY DISTRIBUTION", fill=(100, 116, 139, 255), font=font_sub)
    
    categories = [
        ("Tech", 0.984, (79, 70, 229, 255)),       # Electric Indigo
        ("Business", 0.011, (14, 165, 233, 255)),   # Sky Blue
        ("Politics", 0.002, (234, 88, 12, 255)),    # Orange
        ("Entertainment", 0.002, (236, 72, 153, 255)), # Pink
        ("Sport", 0.001, (16, 185, 129, 255)),      # Emerald Green
    ]
    
    py = ry0 + 230
    bar_width_max = (rx1 - rx0) - 340
    for cat, prob, col in categories:
        # Category label
        draw.text((rx0 + 40, py), cat, fill=(30, 41, 59, 255), font=font_body_bold)
        
        # Background bar
        bx0 = rx0 + 180
        bx1 = bx0 + bar_width_max
        draw.rounded_rectangle([bx0, py + 4, bx1, py + 16], radius=6, fill=(241, 245, 249, 255))
        
        # Fill bar
        fill_w = max(int(bar_width_max * prob), 8)
        draw.rounded_rectangle([bx0, py + 4, bx0 + fill_w, py + 16], radius=6, fill=col)
        
        # Percentage text (placed to the right of the bar)
        prob_str = f"{prob * 100:.1f}%"
        draw.text((bx1 + 25, py), prob_str, fill=(15, 23, 42, 255), font=font_mono)
        
        py += 44
        
    # Divider line
    draw.line([rx0 + 40, py + 10, rx1 - 40, py + 10], fill=(241, 245, 249, 255), width=2)
    
    # Saliency Keywords Section
    ky = py + 30
    draw.text((rx0 + 40, ky), "TOP SALIENCY KEYWORDS (TF-IDF FEATURE EXPLAINABILITY)", fill=(100, 116, 139, 255), font=font_sub)
    
    keywords = [
        ("processor", "+0.35 (35%)"),
        ("macbook", "+0.32 (32%)"),
        ("apple", "+0.28 (28%)"),
        ("laptop", "+0.24 (24%)"),
        ("graphics", "+0.21 (21%)"),
        ("developer", "+0.18 (18%)"),
    ]
    
    kw_x = rx0 + 40
    kw_y = ky + 45
    for word, wt in keywords:
        # Calculate dynamic pill width
        w_bb = draw.textbbox((0, 0), word, font=font_body_bold)
        t_bb = draw.textbbox((0, 0), wt, font=font_small)
        pill_w = (w_bb[2] - w_bb[0]) + (t_bb[2] - t_bb[0]) + 45
        
        draw.rounded_rectangle([kw_x, kw_y, kw_x + pill_w, kw_y + 44], radius=10, fill=(248, 250, 252, 255), outline=(203, 213, 225, 255), width=1)
        draw.text((kw_x + 14, kw_y + 11), word, fill=(15, 23, 42, 255), font=font_body_bold)
        
        # Weight badge inside
        wb_x0 = kw_x + (w_bb[2] - w_bb[0]) + 24
        wb_w = (t_bb[2] - t_bb[0]) + 14
        draw.rounded_rectangle([wb_x0, kw_y + 8, wb_x0 + wb_w, kw_y + 36], radius=6, fill=(236, 254, 255, 255), outline=(165, 243, 252, 255), width=1)
        draw.text((wb_x0 + 7, kw_y + 11), wt, fill=(14, 116, 144, 255), font=font_small)
        
        kw_x += pill_w + 16
        if kw_x > rx1 - 200:
            kw_x = rx0 + 40
            kw_y += 54
            
    # Automated Editorial Decision Box
    dec_y = kw_y + 70
    draw.rounded_rectangle([rx0 + 40, dec_y, rx1 - 40, dec_y + 95], radius=12, fill=(240, 253, 244, 255), outline=(187, 247, 208, 255), width=2)
    draw.text((rx0 + 65, dec_y + 18), "AUTOMATED EDITORIAL ROUTING: TECHNOLOGY DESK", fill=(21, 128, 61, 255), font=get_font(16, bold=True))
    draw.text((rx0 + 65, dec_y + 48), "Confidence (98.4%) exceeds the 80% automated threshold. Dispatched immediately without manual editor review.", fill=(22, 101, 52, 255), font=font_body)
    
    # Save image
    out_path = "docs/slide11_ui_screenshot.png"
    img.save(out_path, "PNG")
    print(f"Generated polished UI screenshot: {out_path} ({W}x{H})")
    return out_path

if __name__ == "__main__":
    generate_ui_screenshot()
