import os
from PIL import Image, ImageDraw

def make_clean_icons():
    # 1. Newspaper Icon (Transparent PNG, 1024x1024)
    size = 1024
    img_news = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d_news = ImageDraw.Draw(img_news)
    
    # Electric Indigo & Blue
    stroke_color = (99, 102, 241, 255)  # #6366F1
    fold_color = (129, 140, 248, 255)   # #818CF8
    fill_subtle = (238, 242, 255, 180)  # #EEF2FF
    line_color = (79, 70, 229, 255)    # #4F46E5
    
    # Scale: centered in 1024x1024
    ox, oy = 212, 160
    w, h = 600, 704
    corner = 180
    lw = 40
    
    # Main document shape: (x0, y0) to (x1-corner, y0) -> fold -> (x1, y1) -> (x0, y1)
    pts = [
        (ox, oy),
        (ox + w - corner, oy),
        (ox + w, oy + corner),
        (ox + w, oy + h),
        (ox, oy + h)
    ]
    d_news.polygon(pts, fill=fill_subtle, outline=stroke_color, width=lw)
    
    # Fold corner tab
    fold_pts = [
        (ox + w - corner, oy),
        (ox + w - corner, oy + corner),
        (ox + w, oy + corner)
    ]
    d_news.polygon(fold_pts, fill=(199, 210, 254, 255), outline=stroke_color, width=lw)
    
    # Header box (representing article image / headline box)
    d_news.rounded_rectangle(
        [ox + 80, oy + 100, ox + 260, oy + 260],
        radius=24,
        fill=(224, 231, 255, 255),
        outline=line_color,
        width=20
    )
    
    # Headline lines next to header box
    d_news.rounded_rectangle([ox + 300, oy + 120, ox + w - 80, oy + 160], radius=16, fill=line_color)
    d_news.rounded_rectangle([ox + 300, oy + 200, ox + w - 80, oy + 240], radius=16, fill=fold_color)
    
    # Body text lines below
    d_news.rounded_rectangle([ox + 80, oy + 320, ox + w - 80, oy + 360], radius=16, fill=line_color)
    d_news.rounded_rectangle([ox + 80, oy + 420, ox + w - 80, oy + 460], radius=16, fill=line_color)
    d_news.rounded_rectangle([ox + 80, oy + 520, ox + w - 160, oy + 560], radius=16, fill=fold_color)
    
    img_news_out = img_news.resize((512, 512), Image.Resampling.LANCZOS)
    img_news_out.save("docs/newspaper_simple_icon.png", "PNG")
    img_news_out.save("public/newspaper_simple_icon.png", "PNG")
    print("Created newspaper_simple_icon.png")

    # 2. Brain / Neural Network Icon (Transparent PNG, 1024x1024)
    img_brain = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d_brain = ImageDraw.Draw(img_brain)
    
    # Nodes and edges for a neural network brain
    cx, cy = 512, 512
    nodes = [
        # Left hemisphere
        (cx - 180, cy - 200), (cx - 260, cy - 80), (cx - 280, cy + 60), (cx - 220, cy + 200), (cx - 120, cy + 260),
        (cx - 80, cy - 260), (cx - 120, cy - 100), (cx - 140, cy + 80), (cx - 40, cy + 180),
        # Right hemisphere
        (cx + 180, cy - 200), (cx + 260, cy - 80), (cx + 280, cy + 60), (cx + 220, cy + 200), (cx + 120, cy + 260),
        (cx + 80, cy - 260), (cx + 120, cy - 100), (cx + 140, cy + 80), (cx + 40, cy + 180),
        # Central bridge nodes
        (cx, cy - 160), (cx, cy), (cx, cy + 120)
    ]
    
    # Draw connections
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (5, 0), (5, 6), (6, 1), (6, 7), (7, 2), (7, 8), (8, 3), (8, 4),
        (9, 10), (10, 11), (11, 12), (12, 13), (14, 9), (14, 15), (15, 10), (15, 16), (16, 11), (16, 17), (17, 12), (17, 13),
        (5, 18), (14, 18), (6, 19), (15, 19), (7, 19), (16, 19), (8, 20), (17, 20), (18, 19), (19, 20)
    ]
    for n1, n2 in edges:
        d_brain.line([nodes[n1], nodes[n2]], fill=(165, 180, 252, 220), width=14)
        
    # Draw nodes
    for idx, (nx, ny) in enumerate(nodes):
        r = 32 if idx in [18, 19, 20] else 26
        d_brain.ellipse([nx - r, ny - r, nx + r, ny + r], fill=(238, 242, 255, 255), outline=stroke_color, width=12)
        d_brain.ellipse([nx - 12, ny - 12, nx + 12, ny + 12], fill=line_color)
        
    img_brain_out = img_brain.resize((512, 512), Image.Resampling.LANCZOS)
    img_brain_out.save("docs/brain_network_icon.png", "PNG")
    img_brain_out.save("public/brain_network_icon.png", "PNG")
    print("Created brain_network_icon.png")

if __name__ == "__main__":
    make_clean_icons()
