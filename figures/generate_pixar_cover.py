import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
import math

# Target size: 6x9 inch at 200 DPI = 1200 x 1800 px (exact 2:3 ratio)
WIDTH = 1200
HEIGHT = 1800

# 1. Base Background: cover_v1_concept_pixar.jpg
bg = Image.open("figures/cover_v1_concept_pixar.jpg").convert("RGBA")
bg = bg.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

# 2. Load 3D Pixar Dr. Chewa character
char_img = Image.open("figures/author_chewa_pixar_alpha.png").convert("RGBA")

# Scale character appropriately so he fits in the lower-middle zone
char_w = 780
aspect = char_img.height / char_img.width
char_h = int(char_w * aspect)
char_img = char_img.resize((char_w, char_h), Image.Resampling.LANCZOS)

# Position character: centered horizontally, resting above the cyber-soil
char_x = (WIDTH - char_w) // 2 + 20
char_y = 660

# Create a composite canvas
canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
canvas.paste(bg, (0, 0))

# 3. Add soft ambient backlight/halo behind character for depth
halo = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw_halo = ImageDraw.Draw(halo)
glow_cx = char_x + char_w // 2
glow_cy = char_y + 350
for r in range(400, 50, -30):
    alpha = int(25 * (1 - r / 400.0))
    draw_halo.ellipse([glow_cx - r, glow_cy - r, glow_cx + r, glow_cy + r], fill=(255, 230, 160, alpha))
halo = halo.filter(ImageFilter.GaussianBlur(30))
canvas = Image.alpha_composite(canvas, halo)

# 4. Paste character onto canvas
canvas.paste(char_img, (char_x, char_y), char_img)

# 5. Create Cold Atmospheric Plasma (CAP) Effects
plasma_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw_plasma = ImageDraw.Draw(plasma_layer)

px_center = char_x + 160
py_center = char_y + 560

# Multi-layered glowing plasma sphere and streams
for r in range(160, 10, -10):
    alpha = int(55 * (1 - r / 160.0))
    draw_plasma.ellipse([px_center - r, py_center - r, px_center + r, py_center + r], fill=(0, 210, 255, alpha))

for r in range(100, 5, -8):
    alpha = int(90 * (1 - r / 100.0))
    draw_plasma.ellipse([px_center - r, py_center - r, px_center + r, py_center + r], fill=(180, 80, 255, alpha))

# Core brilliant white center
for r in range(35, 2, -4):
    alpha = int(180 * (1 - r / 35.0))
    draw_plasma.ellipse([px_center - r, py_center - r, px_center + r, py_center + r], fill=(255, 255, 255, alpha))

# Curved energy filaments/streamers
for angle in range(0, 360, 20):
    rad = math.radians(angle)
    length = 120 + 40 * math.sin(angle * 3)
    ex = px_center + length * math.cos(rad)
    ey = py_center + length * math.sin(rad)
    draw_plasma.line([px_center, py_center, ex, ey], fill=(0, 255, 255, 120), width=3)
    draw_plasma.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 255, 255, 200))

plasma_blur = plasma_layer.filter(ImageFilter.GaussianBlur(6))
canvas = Image.alpha_composite(canvas, plasma_blur)
canvas = Image.alpha_composite(canvas, plasma_layer)

# 6. Holographic Data HUD Rings around plasma reaction
hud_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
draw_hud = ImageDraw.Draw(hud_layer)

r1 = 180
draw_hud.ellipse([px_center - r1, py_center - r1, px_center + r1, py_center + r1], outline=(0, 255, 230, 160), width=2)
r2 = 220
draw_hud.ellipse([px_center - r2, py_center - r2, px_center + r2, py_center + r2], outline=(150, 100, 255, 120), width=1)

# Radical Badges: ·OH, O3, NO3-, H2O2
badges = [
    (px_center - 190, py_center - 110, "·OH", (0, 220, 255)),
    (px_center + 160, py_center - 120, "O3", (190, 80, 255)),
    (px_center - 180, py_center + 130, "NO3-", (50, 230, 120)),
    (px_center + 150, py_center + 110, "H2O2", (255, 200, 50))
]

for bx, by, text, col in badges:
    for gr in range(32, 18, -2):
        alpha = int(40 * (1 - gr / 32.0))
        draw_hud.ellipse([bx - gr, by - gr, bx + gr, by + gr], fill=(col[0], col[1], col[2], alpha))
    draw_hud.ellipse([bx - 24, by - 24, bx + 24, by + 24], fill=(20, 30, 50, 220), outline=(col[0], col[1], col[2], 255), width=2)

canvas = Image.alpha_composite(canvas, hud_layer)

# 7. Convert to RGB and save final high-res cover art
final_art = canvas.convert("RGB")
final_art.save("figures/cover_art_pixar_3d_master.jpg", "JPEG", quality=95)
print("Saved figures/cover_art_pixar_3d_master.jpg successfully!")
