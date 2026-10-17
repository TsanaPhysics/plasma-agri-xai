import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

# 1. Load original pristine cover_v12_whitejacket.jpg
base = Image.open('figures/cover_v12_whitejacket.jpg').convert('RGBA')
W, H = 1200, 1800
base = base.resize((W, H), Image.Resampling.LANCZOS)

# 2. Mask the old green CV scanner text cleanly (x: 480..820, y: 920..1240)
# This is entirely on his white jacket torso and below his chin (NO TOUCHING HIS FACE!)
mask_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
m_draw = ImageDraw.Draw(mask_layer)

# Smooth gradient patch over the old green text area
m_draw.rounded_rectangle([480, 930, 800, 1220], radius=12, fill=(12, 22, 38, 235))
# Smooth dark AMOLED plate over the phone screen crosshair
m_draw.polygon([(340, 920), (460, 905), (480, 1140), (360, 1155)], fill=(8, 16, 28, 240))

mask_blur = mask_layer.filter(ImageFilter.GaussianBlur(8))
base = Image.alpha_composite(base, mask_blur)
base = Image.alpha_composite(base, mask_layer)

# 3. Create high-energy Cold Atmospheric Plasma (CAP) Jet Plume
plasma_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
p_draw = ImageDraw.Draw(plasma_layer)

# Device nozzle / emitter tip: x=380, y=910
# Leaf treatment focal center: x=270, y=990
nx, ny = 380, 910
lx, ly = 270, 990

# Multistage discharge beam connecting nozzle to leaf
steps = 55
for s in range(steps):
    t = s / float(steps)
    cx = (1 - t) * nx + t * lx + 12 * math.sin(t * math.pi * 1.5)
    cy = (1 - t) * ny + t * ly

    r_outer = int(18 + 36 * t)
    r_mid = int(10 + 22 * t)
    r_core = int(4 + 8 * t)

    p_draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=(138, 43, 226, 85))
    p_draw.ellipse([cx - r_mid, cy - r_mid, cx + r_mid, cy + r_mid], fill=(0, 240, 255, 150))
    p_draw.ellipse([cx - r_core, cy - r_core, cx + r_core, cy + r_core], fill=(255, 255, 255, 230))

# Broad ionization halo over leaf surface
for r in range(160, 15, -12):
    al = int(55 * (1 - r / 160.0))
    p_draw.ellipse([lx - r, ly - r, lx + r, ly + r], fill=(147, 50, 255, al))

for r in range(95, 10, -10):
    al = int(120 * (1 - r / 95.0))
    p_draw.ellipse([lx - r, ly - r, lx + r, ly + r], fill=(0, 255, 255, al))

for r in range(35, 2, -4):
    al = int(230 * (1 - r / 35.0))
    p_draw.ellipse([lx - r, ly - r, lx + r, ly + r], fill=(255, 255, 255, al))

# Branching Dielectric Barrier Discharge (DBD) filamentary micro-streamers
branches = [
    (10, 75), (35, 105), (65, 85), (105, 65), (145, 95),
    (185, 80), (220, 100), (260, 115), (300, 80), (340, 65)
]
for ang, leng in branches:
    rad = math.radians(ang)
    ex = lx + leng * math.cos(rad)
    ey = ly + leng * math.sin(rad)
    p_draw.line([lx, ly, ex, ey], fill=(0, 255, 255, 210), width=2)
    p_draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(255, 255, 255, 240))

plasma_blur = plasma_layer.filter(ImageFilter.GaussianBlur(8))
base = Image.alpha_composite(base, plasma_blur)
base = Image.alpha_composite(base, plasma_layer)

# 4. Floating 3D Reactive Oxygen & Nitrogen Species (RONS) Badges
badge_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
b_draw = ImageDraw.Draw(badge_layer)

try:
    font_badge = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 16)
    font_sub = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 11)
    font_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 12)
    font_code = ImageFont.truetype('/System/Library/Fonts/Courier.dfont', 10)
except Exception:
    font_badge = font_sub = font_title = font_code = ImageFont.load_default()

badges = [
    (lx - 95, ly - 75, '·OH', (0, 230, 255)),
    (lx + 85, ly - 85, 'O3', (200, 70, 255)),
    (lx - 105, ly + 70, 'NO3-', (50, 255, 130)),
    (lx + 70, ly + 85, 'H2O2', (255, 210, 50)),
    (lx - 10, ly - 135, 'ONOO-', (255, 90, 160))
]

for bx, by, formula, col in badges:
    for gr in range(32, 16, -2):
        al = int(45 * (1 - gr / 32.0))
        b_draw.ellipse([bx - gr, by - gr, bx + gr, by + gr], fill=(col[0], col[1], col[2], al))
    b_draw.ellipse([bx - 22, by - 22, bx + 22, by + 22], fill=(10, 20, 35, 240), outline=(col[0], col[1], col[2], 255), width=2)
    bbox = font_badge.getbbox(formula)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    b_draw.text((bx - tw / 2, by - th / 2 - 1), formula, font=font_badge, fill=(255, 255, 255, 255))

# 5. UI Elements on Phone Screen (AMOLED Interface)
ph_ui = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ph_draw = ImageDraw.Draw(ph_ui)

ph_draw.text((365, 940), 'CAP-JET: 8.5 kV', font=font_sub, fill=(0, 240, 255, 240))
ph_draw.text((365, 965), 'FREQ: 25.0 kHz', font=font_sub, fill=(180, 120, 255, 240))
ph_draw.text((365, 990), 'PAW: +580 mV', font=font_sub, fill=(255, 200, 80, 240))

# Miniature plasma wave on phone
for px_i in range(90):
    wx = 365 + px_i
    val = 14 * math.exp(-((px_i - 25) ** 2) / 35) + 18 * math.exp(-((px_i - 55) ** 2) / 45) + 3 * math.sin(px_i * 0.3)
    wy = int(1070 - val)
    ph_draw.ellipse([wx - 1, wy - 1, wx + 1, wy + 1], fill=(0, 255, 220, 240))

ph_draw.text((365, 1085), 'PLASMA ACTIVE', font=font_sub, fill=(0, 255, 150, 255))

# 6. Holographic Plasma Agri-Physics HUD Panel on white jacket (hx=500, hy=940)
hud = Image.new('RGBA', (W, H), (0, 0, 0, 0))
h_draw = ImageDraw.Draw(hud)

hx, hy, hw, hh = 500, 940, 310, 310

h_draw.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=10, fill=(8, 20, 38, 235), outline=(0, 240, 255, 230), width=2)
h_draw.rounded_rectangle([hx + 4, hy + 4, hx + hw - 4, hy + hh - 4], radius=8, outline=(138, 43, 226, 120), width=1)

# Header banner
h_draw.rounded_rectangle([hx + 4, hy + 4, hx + hw - 4, hy + 30], radius=6, fill=(0, 170, 220, 220))
h_draw.text((hx + 14, hy + 8), 'PLASMA AGRO-PHYSICS TELEMETRY', font=font_title, fill=(255, 255, 255, 255))

readouts = [
    ('Discharge Mode:', 'CAP Jet DBD (25 kHz)', (255, 255, 255)),
    ('Peak Potential:', '8.50 kV (Bipolar)', (0, 240, 255)),
    ('Plasma Temp Te:', '1.42 eV (Non-Thermal)', (180, 220, 255)),
    ('PAW Synthesis pH:', '3.62 (Acidic Activ)', (255, 200, 80)),
    ('Oxidation ORP:', '+585 mV (High Oxid)', (255, 120, 180)),
    ('Reactive Nitrogen:', 'NO3- 185 mg/L, O3 42ppm', (0, 255, 200)),
    ('Phytophthora Red.:', '99.98% Inactivation', (100, 255, 150)),
    ('Seed Vigour Index:', '+38.4% Germination', (255, 230, 100))
]

for i, (label, val, c_val) in enumerate(readouts):
    yy = hy + 36 + i * 19
    h_draw.text((hx + 10, yy), label, font=font_sub, fill=(180, 210, 240, 240))
    h_draw.text((hx + 140, yy), val, font=font_code, fill=c_val)

# Optical Emission Spectroscopy (OES) Spectrum Chart
gx, gy, gw, gh = hx + 10, hy + 190, hw - 20, 75
h_draw.rectangle([gx, gy, gx + gw, gy + gh], fill=(4, 10, 22, 220), outline=(0, 200, 255, 140), width=1)
h_draw.text((gx + 6, gy + 3), 'OES SPECTRUM (300 - 800 nm)', font=font_sub, fill=(0, 220, 255, 220))

pts = []
for xi in range(gw):
    nm = 300 + (xi / float(gw)) * 500
    val = 6 + 3 * math.sin(xi * 0.4)
    val += 48 * math.exp(-((nm - 309) ** 2) / 12)
    val += 58 * math.exp(-((nm - 337) ** 2) / 15)
    val += 38 * math.exp(-((nm - 357) ** 2) / 15)
    val += 42 * math.exp(-((nm - 777) ** 2) / 14)
    yi = gy + gh - int(min(val, gh - 14)) - 4
    pts.append((gx + xi, yi))

for j in range(len(pts) - 1):
    h_draw.line([pts[j], pts[j + 1]], fill=(0, 255, 230, 240), width=2)

h_draw.text((gx + 12, gy + 16), '·OH', font=font_sub, fill=(0, 230, 255, 255))
h_draw.text((gx + 32, gy + 10), 'N2', font=font_sub, fill=(180, 100, 255, 255))
h_draw.text((gx + gw - 35, gy + 18), 'O I', font=font_sub, fill=(255, 180, 50, 255))

# Footer
h_draw.line([hx + 10, hy + 272, hx + hw - 10, hy + 272], fill=(0, 200, 255, 100), width=1)
h_draw.text((hx + 12, hy + 280), 'STATUS: IN-SITU COLD PLASMA ACTIVE', font=font_sub, fill=(0, 255, 180, 255))

base = Image.alpha_composite(base, badge_layer)
base = Image.alpha_composite(base, ph_ui)
base = Image.alpha_composite(base, hud)

out_rgb = base.convert('RGB')
out_rgb.save('figures/cover_art_plasma_dr_chewa.jpg', 'JPEG', quality=96)
print('Successfully created master figures/cover_art_plasma_dr_chewa.jpg')
