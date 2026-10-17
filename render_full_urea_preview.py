import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Load the concept art
bg = Image.open('figures/cover_art_concept_plasma_urea.jpg').convert('RGBA')
W, H = 1200, 1800

# Typography layer
typo = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(typo)

# Fonts
font_badge = ImageFont.truetype('fonts/THSarabun Bold.ttf', 24)
font_sub = ImageFont.truetype('fonts/THSarabun Bold.ttf', 28)
font_main = ImageFont.truetype('fonts/THSarabun Bold.ttf', 135) # 55pt equivalent at 200 DPI
font_title2 = ImageFont.truetype('fonts/THSarabun Bold.ttf', 62)
font_pill = ImageFont.truetype('fonts/THSarabun Bold.ttf', 32)
font_eng1 = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 19)
font_eng2 = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 16)
font_author = ImageFont.truetype('fonts/THSarabun Bold.ttf', 44)
font_dept = ImageFont.truetype('fonts/THSarabun Bold.ttf', 28)
font_uni = ImageFont.truetype('fonts/THSarabun Bold.ttf', 28)

# 1. Category Badge
bx, by, bw, bh = W // 2 - 290, 75, 580, 38
draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=(10, 25, 47, 235))
badge_txt = "▶ TEXTBOOK SERIES IN APPLIED PHYSICS & PLASMA AGRICULTURE ◀"
bb = font_badge.getbbox(badge_txt)
draw.text((W // 2 - (bb[2] - bb[0]) // 2, by + 5), badge_txt, font=font_badge, fill=(255, 255, 255, 255))

# Sub-badge
sub_txt = "ตำราวิชาการและคู่มือการวิจัยขั้นสูง • มหาวิทยาลัยราชภัฏรำไพพรรณี"
sb = font_sub.getbbox(sub_txt)
draw.text((W // 2 - (sb[2] - sb[0]) // 2, 122), sub_txt, font=font_sub, fill=(10, 25, 47, 240))

# 2. Main Title Line 1: พลาสมาฟิสิกส์ (2.5x Size, Multicolored)
# Syllables: พลาส (Violet #6B21A8), มา (Cyan #0284C7), ฟิ (Emerald #047857), สิกส์ (Coral #C2410C)
syllables = [
    ("พลาส", (107, 33, 168)),
    ("มา", (2, 132, 199)),
    ("ฟิ", (4, 120, 87)),
    ("สิกส์", (194, 65, 12))
]

total_w = sum(font_main.getbbox(s[0])[2] - font_main.getbbox(s[0])[0] for s in syllables)
cur_x = W // 2 - total_w // 2 - 10
ty = 155

# Shadow layer first
s_x = cur_x
for txt, col in syllables:
    sw = font_main.getbbox(txt)[2] - font_main.getbbox(txt)[0]
    draw.text((s_x + 3, ty + 3), txt, font=font_main, fill=(255, 255, 255, 255))
    draw.text((s_x - 2, ty - 2), txt, font=font_main, fill=(255, 255, 255, 255))
    s_x += sw

# Foreground colored text
for txt, col in syllables:
    sw = font_main.getbbox(txt)[2] - font_main.getbbox(txt)[0]
    draw.text((cur_x, ty), txt, font=font_main, fill=(col[0], col[1], col[2], 255))
    cur_x += sw

# 3. Main Title Line 2: เพื่อการเกษตรและสิ่งแวดล้อม
t2_txt = "เพื่อการเกษตรและสิ่งแวดล้อม"
t2_b = font_title2.getbbox(t2_txt)
t2_x = W // 2 - (t2_b[2] - t2_b[0]) // 2
draw.text((t2_x + 2, 282), t2_txt, font=font_title2, fill=(255, 255, 255, 255))
draw.text((t2_x, 280), t2_txt, font=font_title2, fill=(27, 94, 32, 255))

# 4. Pill Subtitle Tag
pill_txt = "จากทฤษฎีสู่นวัตกรรมความยั่งยืน"
pb = font_pill.getbbox(pill_txt)
pw, ph = (pb[2] - pb[0]) + 36, 42
px, py = W // 2 - pw // 2, 355
draw.rounded_rectangle([px, py, px + pw, py + ph], radius=10, fill=(255, 255, 255, 140), outline=(0, 229, 255, 240), width=2)
draw.text((W // 2 - (pb[2] - pb[0]) // 2, py + 3), pill_txt, font=font_pill, fill=(10, 25, 47, 255))

# 5. English Subtitle
eng1 = "PLASMA PHYSICS FOR AGRICULTURE AND ENVIRONMENT"
e1b = font_eng1.getbbox(eng1)
draw.text((W // 2 - (e1b[2] - e1b[0]) // 2 + 1, 411), eng1, font=font_eng1, fill=(255, 255, 255, 255))
draw.text((W // 2 - (e1b[2] - e1b[0]) // 2, 410), eng1, font=font_eng1, fill=(10, 25, 47, 240))

eng2 = "(FROM FUNDAMENTAL DISCHARGE PHYSICS TO SUSTAINABLE SMART AGRO-AI INNOVATION)"
e2b = font_eng2.getbbox(eng2)
draw.text((W // 2 - (e2b[2] - e2b[0]) // 2, 436), eng2, font=font_eng2, fill=(20, 40, 70, 210))

# 6. Bottom Zone Gradient & Author Metadata
vignette = Image.new('RGBA', (W, H), (0, 0, 0, 0))
v_draw = ImageDraw.Draw(vignette)
for y_i in range(1580, 1800):
    al = int(220 * ((y_i - 1580) / 220.0))
    v_draw.line([(0, y_i), (W, y_i)], fill=(0, 0, 0, al))

typo = Image.alpha_composite(typo, vignette)
draw = ImageDraw.Draw(typo)

a_txt = "ผู้ช่วยศาสตราจารย์ ดร.ชีวะ ทัศนา"
ab = font_author.getbbox(a_txt)
draw.text((W // 2 - (ab[2] - ab[0]) // 2 + 2, 1632), a_txt, font=font_author, fill=(0, 0, 0, 255))
draw.text((W // 2 - (ab[2] - ab[0]) // 2, 1630), a_txt, font=font_author, fill=(255, 255, 255, 255))

d_txt = "สาขาวิชาปัญญาประดิษฐ์เพื่อเกษตรดิจิทัลและสิ่งแวดล้อม คณะวิทยาศาสตร์และเทคโนโลยี"
db = font_dept.getbbox(d_txt)
draw.text((W // 2 - (db[2] - db[0]) // 2 + 1, 1686), d_txt, font=font_dept, fill=(0, 0, 0, 255))
draw.text((W // 2 - (db[2] - db[0]) // 2, 1685), d_txt, font=font_dept, fill=(245, 245, 245, 255))

u_txt = "มหาวิทยาลัยราชภัฏรำไพพรรณี • พ.ศ. 2569"
ub = font_uni.getbbox(u_txt)
draw.text((W // 2 - (ub[2] - ub[0]) // 2 + 1, 1726), u_txt, font=font_uni, fill=(0, 0, 0, 255))
draw.text((W // 2 - (ub[2] - ub[0]) // 2, 1725), u_txt, font=font_uni, fill=(255, 214, 0, 255))

final = Image.alpha_composite(bg, typo)
final.convert('RGB').save('/Users/chewathassana/.gemini/antigravity-ide/brain/2b885d0d-b8d7-4a3e-a55d-811a4af535b7/preview_concept_urea_full_cover.jpg', 'JPEG', quality=95)
print('Saved full cover concept preview')
