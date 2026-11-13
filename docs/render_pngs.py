import os
from PIL import Image, ImageDraw, ImageFont

PUBLIC_DIR = "public"
DOCS_DIR = "docs"
ARTIFACT_DIR = r"C:\Users\abhij\.gemini\antigravity\brain\470ea1df-5e89-49ff-b75a-e00d051f56de"

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(len(c1)))

def draw_gradient_rounded_rect(draw, bbox, r, c_start, c_end):
    # bbox = (x0, y0, x1, y1)
    x0, y0, x1, y1 = bbox
    w = x1 - x0
    h = y1 - y0
    
    # We will create an internal mask and gradient image
    rect_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rect_img)
    
    # Draw rounded rect mask
    mask = Image.new("L", (w, h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle((0, 0, w, h), radius=r, fill=255)
    
    # Draw diagonal gradient
    grad = Image.new("RGBA", (w, h))
    for y in range(h):
        for x in range(w):
            # diagonal factor
            t = (x + y) / (w + h)
            col = lerp_color(c_start, c_end, t)
            grad.putpixel((x, y), (*col, 255))
            
    # Composite using mask
    rect_img.paste(grad, (0, 0), mask)
    return rect_img

def create_icon(scale=2):
    # Base size 512x512, supersampled by scale
    size = 512 * scale
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    # Rounded rect bbox
    pad = 32 * scale
    w = size - 2 * pad
    h = size - 2 * pad
    r = 112 * scale
    
    # Colors: #6366F1 to #9333EA
    c1 = hex_to_rgb("#6366F1")
    c2 = hex_to_rgb("#9333EA")
    
    # Create gradient rect with rounded corners
    mask = Image.new("L", (w, h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle((0, 0, w, h), radius=r, fill=255)
    
    grad = Image.new("RGBA", (w, h))
    # Fill gradient row by row for speed
    for y in range(h):
        for x in range(w):
            t = (x + y) / (w + h)
            c = lerp_color(c1, c2, t)
            grad.putpixel((x, y), (*c, 255))
            
    img.paste(grad, (pad, pad), mask)
    
    # Draw glyph on top
    # Scale glyph coordinates (24x24 viewBox to icon size)
    draw = ImageDraw.Draw(img)
    
    # Glyph center offset
    gx = 136 * scale
    gy = 116 * scale
    gs = 10 * scale
    
    # Document outline: M5 4 H15 L20 9 V20 H5 Z
    poly = [
        (gx + 5 * gs, gy + 4 * gs),
        (gx + 15 * gs, gy + 4 * gs),
        (gx + 20 * gs, gy + 9 * gs),
        (gx + 20 * gs, gy + 20 * gs),
        (gx + 5 * gs, gy + 20 * gs)
    ]
    draw.polygon(poly, fill=(255, 255, 255, 30), outline=(255, 255, 255, 255), width=int(1.8 * gs))
    
    # Fold corner: M15 4 V9 H20 Z
    corner = [
        (gx + 15 * gs, gy + 4 * gs),
        (gx + 15 * gs, gy + 9 * gs),
        (gx + 20 * gs, gy + 9 * gs)
    ]
    draw.polygon(corner, fill=(255, 255, 255, 75), outline=(255, 255, 255, 255), width=int(1.8 * gs))
    
    # Crease lines
    lw = int(1.6 * gs)
    # Line 1: x 8.5 to 15.5, y 12
    draw.line([(gx + 8.5 * gs, gy + 12 * gs), (gx + 15.5 * gs, gy + 12 * gs)], fill=(255, 255, 255, 240), width=lw)
    # Line 2: x 8.5 to 15.5, y 15
    draw.line([(gx + 8.5 * gs, gy + 15 * gs), (gx + 15.5 * gs, gy + 15 * gs)], fill=(255, 255, 255, 190), width=lw)
    # Line 3: x 8.5 to 13, y 18
    draw.line([(gx + 8.5 * gs, gy + 18 * gs), (gx + 13.0 * gs, gy + 18 * gs)], fill=(255, 255, 255, 140), width=lw)
    
    # Downsample with Lanczos for smooth antialiasing
    final_img = img.resize((512, 512), Image.Resampling.LANCZOS)
    return final_img

def create_horizontal_logo(icon_img, dark_mode=False):
    w, h = 1200, 320
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    
    # Paste resized icon (220x220)
    small_icon = icon_img.resize((220, 220), Image.Resampling.LANCZOS)
    img.paste(small_icon, (50, 50), small_icon)
    
    draw = ImageDraw.Draw(img)
    
    # Try finding system fonts (Segoe UI, Arial, etc.)
    font_bold = None
    font_sub = None
    font_badge = None
    
    font_paths = [
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\tahomabd.ttf"
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font_bold = ImageFont.truetype(fp, 108)
                font_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
                font_badge = ImageFont.truetype(fp, 18)
                break
            except:
                pass
                
    if not font_bold:
        font_bold = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        
    # Draw "News" and "Scope"
    text_news = "News"
    text_scope = "Scope"
    
    c_news = (255, 255, 255, 255) if dark_mode else (15, 23, 42, 255) # Slate 900
    c_scope = (147, 51, 234, 255) # Indigo / Purple
    
    draw.text((310, 68), text_news, fill=c_news, font=font_bold)
    # Calculate offset
    news_bbox = draw.textbbox((310, 68), text_news, font=font_bold)
    scope_x = news_bbox[2] + 4
    draw.text((scope_x, 68), text_scope, fill=c_scope, font=font_bold)
    
    # Subtitle
    sub_color = (148, 163, 184, 255) if dark_mode else (100, 116, 139, 255) # Slate 500
    draw.text((315, 200), "AI NEWS ARTICLE CLASSIFIER", fill=sub_color, font=font_sub)
    
    # Pill Badge: 96.4% ACC
    badge_bg = (30, 27, 75, 255) if dark_mode else (238, 242, 255, 255)
    badge_border = (67, 56, 202, 255) if dark_mode else (199, 210, 254, 255)
    badge_text_col = (165, 180, 252, 255) if dark_mode else (79, 70, 229, 255)
    
    draw.rounded_rectangle((940, 98, 1100, 140), radius=21, fill=badge_bg, outline=badge_border, width=2)
    draw.text((965, 108), "96.4% ACC", fill=badge_text_col, font=font_badge)
    
    return img

print("Generating high-resolution PNG logos...")
icon_img = create_icon(scale=2)
icon_img.save("public/logo-icon.png", "PNG")
icon_img.save("docs/logo-icon.png", "PNG")
icon_img.save(os.path.join(ARTIFACT_DIR, "logo-icon.png"), "PNG")
print("Saved logo-icon.png")

logo_light = create_horizontal_logo(icon_img, dark_mode=False)
logo_light.save("public/logo.png", "PNG")
logo_light.save("public/logo-horizontal.png", "PNG")
logo_light.save("docs/logo.png", "PNG")
logo_light.save("docs/logo-horizontal.png", "PNG")
logo_light.save(os.path.join(ARTIFACT_DIR, "logo.png"), "PNG")
logo_light.save(os.path.join(ARTIFACT_DIR, "logo-horizontal.png"), "PNG")
print("Saved logo.png")

logo_dark = create_horizontal_logo(icon_img, dark_mode=True)
logo_dark.save("public/logo-dark.png", "PNG")
logo_dark.save("docs/logo-dark.png", "PNG")
logo_dark.save(os.path.join(ARTIFACT_DIR, "logo-dark.png"), "PNG")
print("Saved logo-dark.png")
print("All PNG renders completed successfully!")
