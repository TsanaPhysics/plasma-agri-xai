import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

# 1. Load base image (1200 x 1800 px)
base = Image.open('figures/cover_art_plasma_dr_chewa.jpg').convert('RGBA')
W, H = 1200, 1800
base = base.resize((W, H), Image.Resampling.LANCZOS)

# 2. Add Solar-Driven Plasma Nitrogen-to-Urea Reactor in background
reactor_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
r_draw = ImageDraw.Draw(reactor_layer)

rx, ry = 220, 680

# Clean font loading
try:
    font_bold = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 13)
    font_large = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 15)
    font_sub = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 11)
    font_code = ImageFont.truetype('/System/Library/Fonts/Courier.dfont', 10)
except Exception:
    font_bold = font_large = font_sub = font_code = ImageFont.load_default()

# Ambient Air Intake Stream (Inflow of atmospheric N2 and O2)
for ang in range(0, 360, 20):
    rad = math.radians(ang)
    for dist in range(40, 130, 15):
        al = int(35 * (1 - dist / 130.0))
        px = rx + dist * math.cos(rad) + 12 * math.sin(dist * 0.1)
        py = ry - 60 + dist * 0.4 * math.sin(rad)
        r_draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(200, 230, 255, al))

# High-voltage quartz discharge chamber (Gliding Arc / DBD)
cw, ch = 64, 120
cx1, cy1 = rx - cw // 2, ry - ch // 2
cx2, cy2 = rx + cw // 2, ry + ch // 2

r_draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=10, fill=(10, 24, 45, 170), outline=(0, 230, 255, 210), width=2)

# Swirling plasma arc (cleaving N2 triple bonds)
for step in range(50):
    t = step / 50.0
    py = cy1 + 10 + t * (ch - 20)
    px = rx + 18 * math.sin(t * math.pi * 5)
    r_draw.ellipse([px - 12, py - 6, px + 12, py + 6], fill=(138, 43, 226, 75))
    r_draw.ellipse([px - 7, py - 4, px + 7, py + 4], fill=(0, 240, 255, 130))
    r_draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255, 210))

# Solar PV energy canopy above the reactor
r_draw.polygon([(rx - 55, cy1 - 22), (rx + 55, cy1 - 22), (rx + 42, cy1 - 5), (rx - 42, cy1 - 5)], fill=(18, 42, 75, 230), outline=(0, 220, 255, 220))
r_draw.line([(rx, cy1 - 22), (rx, cy1 - 5)], fill=(0, 230, 255, 180), width=1)

# Pipeline carrying synthesized green Urea / PAW fertilizer into irrigation
pipe_pts = [(rx, cy2), (rx - 15, cy2 + 65), (rx + 25, cy2 + 145), (rx + 85, cy2 + 220)]
for p in range(len(pipe_pts) - 1):
    r_draw.line([pipe_pts[p], pipe_pts[p+1]], fill=(0, 255, 190, 180), width=3)
    r_draw.line([pipe_pts[p], pipe_pts[p+1]], fill=(255, 255, 255, 230), width=1)

# Glowing micro-droplets of green urea liquid mist
for mi in range(40):
    mx = rx + 35 + (mi * 6) % 110
    my = cy2 + 110 + mi * 3
    r_draw.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=(0, 255, 200, 150))

reactor_blur = reactor_layer.filter(ImageFilter.GaussianBlur(3))
base = Image.alpha_composite(base, reactor_blur)
base = Image.alpha_composite(base, reactor_layer)

# 3. Holographic Reaction Cycle Diagram (ASCII clean formulas without unicode font breaks)
info_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
i_draw = ImageDraw.Draw(info_layer)

# 4-stage process pills
flow_pills = [
    (rx - 75, ry - 145, 'Air N2 (78%)', (120, 210, 255)),
    (rx + 50, ry - 145, 'Plasma Arc N=N Cleavage', (190, 80, 255)),
    (rx + 185, ry - 145, 'Green Urea (NH2)2CO', (0, 255, 180)),
    (rx + 185, ry - 95, 'Bio-Nitrate (NO3-)', (50, 240, 120))
]

for fx, fy, label, col in flow_pills:
    bbox = font_bold.getbbox(label)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    i_draw.rounded_rectangle([fx - 8, fy - 5, fx + tw + 8, fy + th + 5], radius=6, fill=(8, 22, 38, 215), outline=(col[0], col[1], col[2], 220), width=1)
    i_draw.text((fx, fy), label, font=font_bold, fill=(255, 255, 255, 255))

# Connecting energy arrows
i_draw.line([(rx + 5, ry - 138), (rx + 40, ry - 138)], fill=(0, 230, 255, 210), width=2)
i_draw.line([(rx + 155, ry - 138), (rx + 175, ry - 138)], fill=(0, 255, 180, 210), width=2)
i_draw.line([(rx + 155, ry - 138), (rx + 175, ry - 88)], fill=(50, 240, 120, 190), width=2)

# Floating Urea Chemical Structure Info Card
ux, uy = rx + 65, ry + 15
i_draw.rounded_rectangle([ux - 10, uy - 10, ux + 135, uy + 65], radius=8, fill=(6, 18, 34, 225), outline=(0, 255, 180, 230), width=2)
i_draw.text((ux, uy - 3), 'PLASMA UREA SYNTHESIS', font=font_sub, fill=(0, 230, 255, 255))
i_draw.text((ux, uy + 16), 'N2 + CO2 + 2H2O', font=font_bold, fill=(200, 230, 255, 240))
i_draw.text((ux, uy + 36), '-> (NH2)2CO + 2O2', font=font_large, fill=(0, 255, 180, 255))

# 4. Update HUD Telemetry Panel on Dr. Chewa's white jacket
hx, hy, hw, hh = 500, 940, 310, 310
i_draw.rounded_rectangle([hx, hy, hx + hw, hy + hh], radius=10, fill=(8, 20, 38, 240), outline=(0, 240, 255, 230), width=2)
i_draw.rounded_rectangle([hx + 4, hy + 4, hx + hw - 4, hy + hh - 4], radius=8, outline=(138, 43, 226, 120), width=1)

# Header
i_draw.rounded_rectangle([hx + 4, hy + 4, hx + hw - 4, hy + 30], radius=6, fill=(0, 160, 200, 230))
i_draw.text((hx + 12, hy + 8), 'PLASMA N2 FIXATION & UREA LAB', font=font_large, fill=(255, 255, 255, 255))

readouts = [
    ('Synthesis Target:', 'Atmospheric N2 -> Urea', (0, 255, 200)),
    ('Feedstock Gas:', 'Ambient Air (78% N2) + CO2', (200, 230, 255)),
    ('Reactor Discharge:', '8.50 kV Gliding Arc / DBD', (0, 240, 255)),
    ('Energy Consump.:', '2.8 MJ/mol N (Solar-Fed)', (180, 220, 255)),
    ('Urea Yield Rate:', '148.5 mg/L-h (Zero-C)', (0, 255, 180)),
    ('Nitrate Conc.:', '245 mg/L Bio-Fertilizer', (50, 255, 130)),
    ('PAW pH / ORP:', '3.62 / +585 mV (Active)', (255, 200, 80)),
    ('Haber-Bosch Offset:', '100% Carbon-Neutral', (255, 215, 0))
]

for i, (label, val, c_val) in enumerate(readouts):
    yy = hy + 36 + i * 19
    i_draw.text((hx + 10, yy), label, font=font_sub, fill=(180, 210, 240, 240))
    i_draw.text((hx + 138, yy), val, font=font_code, fill=c_val)

# OES Spectrum
gx, gy, gw, gh = hx + 10, hy + 190, hw - 20, 75
i_draw.rectangle([gx, gy, gx + gw, gy + gh], fill=(4, 10, 22, 230), outline=(0, 200, 255, 140), width=1)
i_draw.text((gx + 6, gy + 3), 'OES: N2 DISSOCIATION (300-800 nm)', font=font_sub, fill=(0, 220, 255, 220))

pts = []
for xi in range(gw):
    nm = 300 + (xi / float(gw)) * 500
    val = 6 + 3 * math.sin(xi * 0.4)
    val += 48 * math.exp(-((nm - 309) ** 2) / 12)
    val += 65 * math.exp(-((nm - 337) ** 2) / 14)
    val += 45 * math.exp(-((nm - 357) ** 2) / 14)
    val += 52 * math.exp(-((nm - 777) ** 2) / 14)
    val += 40 * math.exp(-((nm - 656) ** 2) / 15)
    yi = gy + gh - int(min(val, gh - 14)) - 4
    pts.append((gx + xi, yi))

for j in range(len(pts) - 1):
    i_draw.line([pts[j], pts[j + 1]], fill=(0, 255, 220, 240), width=2)

i_draw.text((gx + 12, gy + 16), '.OH', font=font_sub, fill=(0, 230, 255, 255))
i_draw.text((gx + 32, gy + 8), 'N2 (337nm)', font=font_sub, fill=(180, 100, 255, 255))
i_draw.text((gx + gw - 40, gy + 18), 'O I', font=font_sub, fill=(255, 180, 50, 255))

# Footer
i_draw.line([hx + 10, hy + 272, hx + hw - 10, hy + 272], fill=(0, 200, 255, 100), width=1)
i_draw.text((hx + 12, hy + 280), 'STATUS: N2-TO-UREA FIELD CONVERSION ACTIVE', font=font_sub, fill=(0, 255, 180, 255))

base = Image.alpha_composite(base, info_layer)

concept_art = base.convert('RGB')
concept_art.save('figures/cover_art_concept_plasma_urea.jpg', 'JPEG', quality=96)
print('Successfully generated clean figures/cover_art_concept_plasma_urea.jpg')
