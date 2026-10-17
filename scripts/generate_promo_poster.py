import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from generate_promptpay import generate_promptpay_payload
import qrcode

def wrap_text(text, font, max_width, draw):
    """Wraps Thai/English text to fit within max_width."""
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def create_clean_3d_book_mockup(cover_path, target_h=1180):
    """Creates a sleek, elegant 3D book mockup with realistic depth and clean shadows."""
    if not os.path.exists(cover_path):
        cover_path = "figures/cover_preview.png"
    
    cover = Image.open(cover_path).convert("RGBA")
    w, h = cover.size
    aspect = w / h
    new_w = int(target_h * aspect)
    cover = cover.resize((new_w, target_h), Image.Resampling.LANCZOS)
    
    spine_w = 55
    canvas_w = new_w + spine_w + 120
    canvas_h = target_h + 120
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    
    # 1. Soft Floor Shadow
    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([(30, target_h + 10), (canvas_w - 30, target_h + 80)], fill=(0, 0, 0, 190))
    shadow = shadow.filter(ImageFilter.GaussianBlur(30))
    canvas.paste(shadow, (0, 0), shadow)
    
    # 2. Book Spine
    spine_img = Image.new("RGBA", (spine_w, target_h), (15, 23, 42, 255))
    sp_draw = ImageDraw.Draw(spine_img)
    for x in range(spine_w):
        factor = math.sin((x / spine_w) * math.pi)
        shade = int(25 + 40 * factor)
        sp_draw.line([(x, 0), (x, target_h)], fill=(shade, shade + 8, shade + 22, 255))
    sp_draw.line([(spine_w - 2, 0), (spine_w - 2, target_h)], fill=(90, 110, 150, 160), width=2)
    sp_draw.line([(1, 0), (1, target_h)], fill=(0, 0, 0, 220), width=2)
    
    try:
        font_sp = ImageFont.truetype("fonts/THSarabun Bold.ttf", 28)
        txt_img = Image.new("RGBA", (target_h - 120, spine_w), (0, 0, 0, 0))
        tdraw = ImageDraw.Draw(txt_img)
        tdraw.text((20, 8), "พลาสมาฟิสิกส์และปัญญาประดิษฐ์ เพื่อการเกษตรและสิ่งแวดล้อม  •  ผศ.ดร.ชีวะ ทัศนา", 
                   font=font_sp, fill=(240, 245, 255, 240))
        txt_rot = txt_img.rotate(270, expand=True)
        rx = (spine_w - txt_rot.width) // 2
        ry = (target_h - txt_rot.height) // 2
        spine_img.paste(txt_rot, (rx, ry), txt_rot)
    except Exception as e:
        print("Spine text error:", e)
        
    # 3. Book Cover with subtle lighting gradient
    gloss = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gloss)
    for x in range(new_w // 4):
        alpha = int(45 * (1 - x / (new_w // 4)))
        gdraw.line([(x, 0), (x, target_h)], fill=(255, 255, 255, alpha))
    cover_comp = Image.alpha_composite(cover, gloss)
    
    # 4. Book Edge Pages
    edge_w = 18
    p_edge = Image.new("RGBA", (edge_w, target_h - 10), (230, 230, 225, 255))
    pedraw = ImageDraw.Draw(p_edge)
    for y in range(0, target_h - 10, 4):
        pedraw.line([(0, y), (edge_w, y)], fill=(195, 195, 190, 150), width=1)
        
    bx = 40
    by = 30
    canvas.paste(spine_img, (bx, by))
    canvas.paste(cover_comp, (bx + spine_w, by))
    canvas.paste(p_edge, (bx + spine_w + new_w - 4, by + 5))
    
    return canvas

def generate_full_promo_poster(output_png="figures/promo_poster_plasma_book.png"):
    W, H = 2400, 3200
    poster = Image.new("RGBA", (W, H), (11, 17, 32, 255))
    draw = ImageDraw.Draw(poster)
    
    # Background Ambient Lighting
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([(-250, -250), (1300, 1100)], fill=(14, 116, 144, 75))
    gdraw.ellipse([(1300, -200), (2650, 950)], fill=(109, 40, 217, 85))
    gdraw.ellipse([(150, 1350), (1650, 2350)], fill=(5, 150, 105, 55))
    gdraw.ellipse([(1000, 2150), (2600, 3350)], fill=(3, 105, 161, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    poster = Image.alpha_composite(poster, glow)
    draw = ImageDraw.Draw(poster)
    
    # Fonts
    font_bold_file = "fonts/THSarabun Bold.ttf"
    font_reg_file = "fonts/THSarabun.ttf"
    
    f_univ = ImageFont.truetype(font_bold_file, 44)
    f_badge = ImageFont.truetype(font_bold_file, 38)
    f_title1 = ImageFont.truetype(font_bold_file, 92)
    f_title2 = ImageFont.truetype(font_bold_file, 82)
    f_sub = ImageFont.truetype(font_bold_file, 44)
    f_en = ImageFont.truetype(font_bold_file, 34)
    f_author_title = ImageFont.truetype(font_reg_file, 36)
    f_author_name = ImageFont.truetype(font_bold_file, 56)
    f_author_aff = ImageFont.truetype(font_reg_file, 36)
    
    f_card_title = ImageFont.truetype(font_bold_file, 40)
    f_card_body = ImageFont.truetype(font_reg_file, 30)
    
    f_cta_title = ImageFont.truetype(font_bold_file, 50)
    f_cta_body = ImageFont.truetype(font_reg_file, 36)
    f_cta_price = ImageFont.truetype(font_bold_file, 68)
    
    # ----------------------------------------------------
    # 1. TOP HEADER & BADGE
    # ----------------------------------------------------
    header_y = 75
    draw.text((W//2, header_y), "มหาวิทยาลัยราชภัฏรำไพพรรณี  •  คณะวิทยาศาสตร์และเทคโนโลยี", font=f_univ, fill="#94A3B8", anchor="mm")
    
    # Pill Badge
    b_txt = "นวัตกรรมตำราวิชาการใหม่ : บูรณาการฟิสิกส์พลาสมา ปุ๋ยยูเรียเขียว และปัญญาประดิษฐ์เชิงลึก (ฉบับสมบูรณ์ 199 หน้า)"
    b_w, b_h = 1800, 70
    b_x = (W - b_w) // 2
    b_y = header_y + 40
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=35, fill=(15, 23, 42, 230), outline="#06B6D4", width=3)
    draw.text((W//2, b_y + b_h//2), b_txt, font=f_badge, fill="#38BDF8", anchor="mm")
    
    # ----------------------------------------------------
    # 2. HERO SECTION: 3D Book on Left, Titles on Right
    # ----------------------------------------------------
    hero_y = b_y + b_h + 45
    
    # 3D Book Mockup
    book_img = create_clean_3d_book_mockup("figures/compiled_cover_p1-001.png", target_h=1180)
    poster.paste(book_img, (110, hero_y), book_img)
    
    right_x = 1040
    ty = hero_y + 35
    
    # Category tag
    draw.rounded_rectangle([(right_x, ty), (right_x + 380, ty + 50)], radius=12, fill=(30, 41, 59, 230), outline="#818CF8", width=2)
    draw.text((right_x + 190, ty + 25), "TEXTBOOK & RESEARCH MONOGRAPH", font=ImageFont.truetype(font_bold_file, 25), fill="#A5B4FC", anchor="mm")
    
    ty += 75
    # Title Line 1
    draw.text((right_x, ty), "พลาสมาฟิสิกส์และปัญญาประดิษฐ์", font=f_title1, fill="#FFFFFF")
    ty += 105
    # Title Line 2
    draw.text((right_x, ty), "เพื่อการเกษตรและสิ่งแวดล้อม", font=f_title2, fill="#38BDF8")
    ty += 95
    # Subtitle Thai
    draw.text((right_x, ty), "จากฟิสิกส์การคายประจุและการเรียนรู้เชิงลึกสู่นวัตกรรมยั่งยืน", font=f_sub, fill="#FBBF24")
    ty += 65
    # Subtitle English
    draw.text((right_x, ty), "PLASMA PHYSICS AND ARTIFICIAL INTELLIGENCE", font=f_en, fill="#CBD5E1")
    ty += 42
    draw.text((right_x, ty), "FOR AGRICULTURE AND ENVIRONMENT", font=f_en, fill="#CBD5E1")
    
    ty += 65
    # Divider line
    draw.line([(right_x, ty), (W - 120, ty)], fill="#334155", width=3)
    
    # Author Card
    ty += 30
    author_box_w = W - 120 - right_x
    author_box_h = 230
    draw.rounded_rectangle([(right_x, ty), (right_x + author_box_w, ty + author_box_h)], radius=20, fill=(15, 23, 42, 230), outline="#0284C7", width=2)
    
    portrait_path = "figures/dr_chewa_official_portrait.jpg"
    if os.path.exists(portrait_path):
        try:
            port = Image.open(portrait_path).convert("RGBA")
            port = port.resize((170, 170), Image.Resampling.LANCZOS)
            mask = Image.new("L", (170, 170), 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.ellipse((0, 0, 170, 170), fill=255)
            poster.paste(port, (right_x + 30, ty + 30), mask)
            draw.ellipse((right_x + 28, ty + 28, right_x + 202, ty + 202), outline="#38BDF8", width=3)
        except Exception as e:
            print("Portrait error:", e)
    
    text_lead_x = right_x + 230
    draw.text((text_lead_x, ty + 35), "ผู้แต่ง / นักวิจัยหลัก :", font=f_author_title, fill="#94A3B8")
    draw.text((text_lead_x, ty + 90), "ผู้ช่วยศาสตราจารย์ ดร.ชีวะ ทัศนา", font=f_author_name, fill="#F8FAFC")
    draw.text((text_lead_x, ty + 150), "สาขาวิชาฟิสิกส์และวิทยาศาสตร์ทั่วไป คณะวิทยาศาสตร์และเทคโนโลยี", font=f_author_aff, fill="#38BDF8")
    draw.text((text_lead_x, ty + 188), "มหาวิทยาลัยราชภัฏรำไพพรรณี จังหวัดจันทบุรี", font=f_author_aff, fill="#94A3B8")
    
    # Badges under author
    ty += author_box_h + 25
    badges = [
        ("• 199 หน้าฉบับเต็ม •", "#0284C7"),
        ("• 11 บทวิชาการ •", "#7C3AED"),
        ("• 6 ภาคผนวกสมบูรณ์ •", "#059669"),
        ("• 35+ บรรณานุกรม APA 7th •", "#D97706"),
    ]
    cur_bx = right_x
    for b_title, b_color in badges:
        bw = 285
        draw.rounded_rectangle([(cur_bx, ty), (cur_bx + bw, ty + 50)], radius=12, fill=(30, 41, 59, 240), outline=b_color, width=2)
        draw.text((cur_bx + bw//2, ty + 25), b_title, font=ImageFont.truetype(font_bold_file, 26), fill="#FFFFFF", anchor="mm")
        cur_bx += bw + 15
    
    # ----------------------------------------------------
    # 3. CONTENT PILLARS (6 High-Impact Feature Cards)
    # ----------------------------------------------------
    grid_y = hero_y + 1240
    draw.text((W//2, grid_y), "จุดเด่นและสาระสำคัญอันทรงคุณค่าในเล่ม (Comprehensive Knowledge Pillars)", 
              font=ImageFont.truetype(font_bold_file, 48), fill="#E2E8F0", anchor="mm")
    
    grid_top = grid_y + 45
    cards = [
        ("1. ฟิสิกส์การคายประจุ & OES", 
         "เจาะลึกกลไก Townsend, Streamer, กฎของ Paschen และการวินิจฉัยพลาสมาอุณหภูมิต่ำด้วยเทคนิค Optical Emission Spectroscopy (OES) แม่นยำระดับนาโนเมตร",
         "#38BDF8"),
        ("2. นวัตกรรมปุ๋ยยูเรียเขียว (Green Urea)", 
         "การตรึงไนโตรเจนจากอากาศสู่สารละลายไนไตรต์-ไนเตรต (PAW) และกลไกสังเคราะห์ปุ๋ยยูเรียเขียวไร้ก๊าซเรือนกระจก ทางเลือกยั่งยืนแทน Haber-Bosch",
         "#34D399"),
        ("3. เกษตรแม่นยำ & รักษาโรคพืช", 
         "การประยุกต์น้ำพลาสมาทำลายสปอร์เชื้อรา Phytophthora palmivora สาเหตุโรครากเน่าโคนเน่าทุเรียน และเทคนิคกระตุ้นเมล็ดพันธุ์เร่งการงอก",
         "#FBBF24"),
        ("4. Deep Learning, PINN & Edge AI", 
         "สถาปัตยกรรม Physics-Informed Neural Networks บูรณาการสมการฟิสิกส์เข้าสู่ Loss Function พร้อมโค้ด PyTorch ต้นฉบับและระบบควบคุม Modbus RTU",
         "#A78BFA"),
        ("5. ความปลอดภัย & มาตรฐานสากล", 
         "ขีดจำกัดความปลอดภัยก๊าซโอโซนและ NOx ตามเกณฑ์ OSHA, ACGIH, ระบบสายดินไฟฟ้าแรงสูง NFPA 70E และการประเมินวงจรชีวิต LCA เทียบความคุ้มค่า",
         "#F87171"),
        ("6. ภาคผนวก ก–ฉ & บรรณานุกรม APA 7th", 
         "คู่มือ SOP ภาคสนาม 4 ฉบับ, 30 ปฏิกิริยาเคมีฟิสิกส์, อภิธานศัพท์และคำย่อ 2 ภาษา, และดรรชนีสืบค้นภาษาไทย-อังกฤษ จัดเรียงตามมาตรฐานสากล",
         "#F472B6"),
    ]
    
    c_w = (W - 240 - 40) // 2
    c_h = 165
    
    for idx, (c_title, c_desc, c_border) in enumerate(cards):
        row = idx // 2
        col = idx % 2
        cx = 120 + col * (c_w + 40)
        cy = grid_top + row * (c_h + 20)
        
        draw.rounded_rectangle([(cx, cy), (cx + c_w, cy + c_h)], radius=16, fill=(15, 23, 42, 230), outline=c_border, width=2)
        draw.text((cx + 25, cy + 32), c_title, font=f_card_title, fill=c_border)
        wrapped_lines = wrap_text(c_desc, f_card_body, c_w - 50, draw)
        text_y = cy + 78
        for line in wrapped_lines[:2]:
            draw.text((cx + 25, text_y), line, font=f_card_body, fill="#CBD5E1")
            text_y += 38
    
    # ----------------------------------------------------
    # 4. BOTTOM SECTION: Ordering Info & PromptPay Card
    # ----------------------------------------------------
    bot_y = grid_top + 3 * (c_h + 20) + 35
    draw.line([(120, bot_y), (W - 120, bot_y)], fill="#334155", width=3)
    
    cta_y = bot_y + 35
    pack_w = 1420
    pack_h = 600
    draw.rounded_rectangle([(120, cta_y), (120 + pack_w, cta_y + pack_h)], radius=24, fill=(15, 23, 42, 240), outline="#38BDF8", width=3)
    
    pdraw = ImageDraw.Draw(poster)
    px = 120 + 45
    py = cta_y + 35
    pdraw.text((px, py), "ข้อมูลการสั่งจองและสนับสนุนผลงานวิชาการ", font=f_cta_title, fill="#38BDF8")
    py += 60
    pdraw.text((px, py), "• รูปเล่มตำราขนาด Pocket Book สากล (6 x 9 นิ้ว) จำนวน 199 หน้า ปกอาร์ตการ์ดเคลือบด้าน พรีเมียม", font=f_cta_body, fill="#E2E8F0")
    py += 48
    pdraw.text((px, py), "• ภาพประกอบ 4 สี ตาราง และวงจรเทคนิค คมชัด 100% มาตรฐานเดียวกับตำราวิชาการระดับโลก", font=f_cta_body, fill="#E2E8F0")
    py += 48
    pdraw.text((px, py), "• มอบพร้อมสิทธิ์ดาวน์โหลดโค้ดตัวอย่าง Python / PyTorch PINN และแบบจำลองฟิสิกส์ในเล่ม", font=f_cta_body, fill="#E2E8F0")
    py += 48
    pdraw.text((px, py), "• เหมาะสำหรับ: นักศึกษาระดับปริญญาตรี-โท-เอก, อาจารย์, นักวิจัย และผู้พัฒนานวัตกรรม AI เกษตร", font=f_cta_body, fill="#E2E8F0")
    
    # Special Price Banner
    py += 55
    draw.rounded_rectangle([(px, py), (px + pack_w - 90, py + 120)], radius=16, fill=(30, 41, 59, 240), outline="#F59E0B", width=2)
    pdraw.text((px + 30, py + 35), "ราคาจำหน่ายเล่มละ :", font=ImageFont.truetype(font_bold_file, 42), fill="#FCD34D")
    pdraw.text((px + 330, py + 25), "450 บาท", font=f_cta_price, fill="#F59E0B")
    pdraw.text((px + 620, py + 45), "(รวมค่าจัดส่งด่วน EMS ทั่วประเทศ)", font=ImageFont.truetype(font_reg_file, 34), fill="#94A3B8")
    
    py += 140
    pdraw.text((px, py), "• รายได้ทั้งหมดสมทบทุนสนับสนุนงานวิจัยนวัตกรรมฟิสิกส์เกษตร มหาวิทยาลัยราชภัฏรำไพพรรณี •", 
               font=ImageFont.truetype(font_bold_file, 32), fill="#34D399")
    
    # Right Box: PromptPay Card (precisely scaled to fit inside pack_h)
    pp_box_x = 120 + pack_w + 35
    pp_box_w = W - 120 - pp_box_x
    pp_box_h = pack_h
    
    draw.rounded_rectangle([(pp_box_x, cta_y), (pp_box_x + pp_box_w, cta_y + pp_box_h)], radius=24, fill=(255, 255, 255, 255), outline="#0284C7", width=3)
    
    pp_card_path = "figures/promptpay_qr_card.png"
    if os.path.exists(pp_card_path):
        pp_card = Image.open(pp_card_path).convert("RGBA")
        # Fit inside pp_box_w - 10, pp_box_h - 10
        scale_w = (pp_box_w - 10) / pp_card.width
        scale_h = (pp_box_h - 10) / pp_card.height
        scale = min(scale_w, scale_h)
        new_pp_w = int(pp_card.width * scale)
        new_pp_h = int(pp_card.height * scale)
        pp_card = pp_card.resize((new_pp_w, new_pp_h), Image.Resampling.LANCZOS)
        
        # Center in box
        off_x = pp_box_x + (pp_box_w - new_pp_w) // 2
        off_y = cta_y + (pp_box_h - new_pp_h) // 2
        poster.paste(pp_card, (off_x, off_y), pp_card)
    
    # ----------------------------------------------------
    # 5. FOOTER
    # ----------------------------------------------------
    foot_y = H - 75
    draw.text((W//2, foot_y), "ติดต่อสอบถาม / แจ้งหลักฐานการโอน : โทร 093-742-2654  |  สาขาวิชาฟิสิกส์ มหาวิทยาลัยราชภัฏรำไพพรรณี  |  GitHub: TsanaPhysics/plasma-agri-xai", 
              font=ImageFont.truetype(font_bold_file, 32), fill="#64748B", anchor="mm")
    
    # Save Images
    poster.save(output_png, quality=95)
    jpg_path = output_png.replace(".png", ".jpg")
    poster.convert("RGB").save(jpg_path, quality=92)
    print(f"Successfully generated clean promo poster to {output_png} and {jpg_path}")
    return output_png

if __name__ == "__main__":
    generate_full_promo_poster()
