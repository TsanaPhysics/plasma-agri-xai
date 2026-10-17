import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_clean_3d_book_mockup(cover_path, target_h=1050):
    """Creates a sleek, elegant 3D book mockup with realistic depth and clean shadows."""
    if not os.path.exists(cover_path):
        cover_path = "figures/cover_preview.png"
    
    cover = Image.open(cover_path).convert("RGBA")
    w, h = cover.size
    aspect = w / h
    new_w = int(target_h * aspect)
    cover = cover.resize((new_w, target_h), Image.Resampling.LANCZOS)
    
    spine_w = 52
    canvas_w = new_w + spine_w + 110
    canvas_h = target_h + 110
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    
    # 1. Soft Floor Shadow
    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([(20, target_h + 10), (canvas_w - 20, target_h + 80)], fill=(0, 0, 0, 200))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
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
        font_sp = ImageFont.truetype("fonts/THSarabun Bold.ttf", 26)
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
    edge_w = 16
    p_edge = Image.new("RGBA", (edge_w, target_h - 10), (230, 230, 225, 255))
    pedraw = ImageDraw.Draw(p_edge)
    for y in range(0, target_h - 10, 4):
        pedraw.line([(0, y), (edge_w, y)], fill=(195, 195, 190, 150), width=1)
        
    bx = 35
    by = 25
    canvas.paste(spine_img, (bx, by))
    canvas.paste(cover_comp, (bx + spine_w, by))
    canvas.paste(p_edge, (bx + spine_w + new_w - 4, by + 5))
    
    return canvas

def generate_visual_promo_poster(output_png="figures/promo_poster_plasma_book.png"):
    W, H = 2400, 3200
    poster = Image.new("RGBA", (W, H), (10, 15, 28, 255))
    draw = ImageDraw.Draw(poster)
    
    # Background Ambient Lighting
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([(-200, -200), (1300, 1100)], fill=(14, 116, 144, 80))
    gdraw.ellipse([(1300, -200), (2650, 950)], fill=(109, 40, 217, 90))
    gdraw.ellipse([(150, 1300), (1650, 2300)], fill=(5, 150, 105, 60))
    gdraw.ellipse([(1000, 2100), (2600, 3300)], fill=(3, 105, 161, 75))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    poster = Image.alpha_composite(poster, glow)
    draw = ImageDraw.Draw(poster)
    
    # Fonts
    font_bold = "fonts/THSarabun Bold.ttf"
    font_reg = "fonts/THSarabun.ttf"
    
    f_univ = ImageFont.truetype(font_bold, 42)
    f_badge = ImageFont.truetype(font_bold, 36)
    f_title1 = ImageFont.truetype(font_bold, 86)
    f_title2 = ImageFont.truetype(font_bold, 76)
    f_sub = ImageFont.truetype(font_bold, 42)
    f_en = ImageFont.truetype(font_bold, 32)
    
    f_author_title = ImageFont.truetype(font_reg, 34)
    f_author_name = ImageFont.truetype(font_bold, 54)
    f_author_aff = ImageFont.truetype(font_reg, 34)
    
    f_sec_title = ImageFont.truetype(font_bold, 44)
    f_part_title = ImageFont.truetype(font_bold, 38)
    f_part_sub = ImageFont.truetype(font_bold, 32)
    f_part_desc = ImageFont.truetype(font_reg, 28)
    
    f_cta_title = ImageFont.truetype(font_bold, 48)
    f_cta_body = ImageFont.truetype(font_reg, 34)
    f_cta_price = ImageFont.truetype(font_bold, 66)
    
    # ----------------------------------------------------
    # 1. TOP HEADER & BADGE
    # ----------------------------------------------------
    header_y = 65
    draw.text((W//2, header_y), "มหาวิทยาลัยราชภัฏรำไพพรรณี  •  คณะวิทยาศาสตร์และเทคโนโลยี", font=f_univ, fill="#94A3B8", anchor="mm")
    
    # Pill Badge
    b_txt = "นวัตกรรมตำราวิชาการใหม่ : บูรณาการฟิสิกส์พลาสมา ปุ๋ยยูเรียเขียว และปัญญาประดิษฐ์เชิงลึก (ฉบับสมบูรณ์ 199 หน้า)"
    b_w, b_h = 1800, 64
    b_x = (W - b_w) // 2
    b_y = header_y + 35
    draw.rounded_rectangle([(b_x, b_y), (b_x + b_w, b_y + b_h)], radius=32, fill=(15, 23, 42, 230), outline="#06B6D4", width=3)
    draw.text((W//2, b_y + b_h//2), b_txt, font=f_badge, fill="#38BDF8", anchor="mm")
    
    # ----------------------------------------------------
    # 2. HERO SHOWCASE: 3D Book on Left, Master Titles on Right
    # ----------------------------------------------------
    hero_y = b_y + b_h + 35
    
    # Left: 3D Book
    book_img = create_clean_3d_book_mockup("figures/compiled_cover_p1-001.png", target_h=1020)
    poster.paste(book_img, (90, hero_y), book_img)
    
    right_x = 940
    ty = hero_y + 20
    
    # Category tag
    draw.rounded_rectangle([(right_x, ty), (right_x + 380, ty + 46)], radius=12, fill=(30, 41, 59, 230), outline="#818CF8", width=2)
    draw.text((right_x + 190, ty + 23), "TEXTBOOK & RESEARCH MONOGRAPH", font=ImageFont.truetype(font_bold, 24), fill="#A5B4FC", anchor="mm")
    
    ty += 65
    draw.text((right_x, ty), "พลาสมาฟิสิกส์และปัญญาประดิษฐ์", font=f_title1, fill="#FFFFFF")
    ty += 95
    draw.text((right_x, ty), "เพื่อการเกษตรและสิ่งแวดล้อม", font=f_title2, fill="#38BDF8")
    ty += 85
    draw.text((right_x, ty), "จากฟิสิกส์การคายประจุและการเรียนรู้เชิงลึกสู่นวัตกรรมยั่งยืน", font=f_sub, fill="#FBBF24")
    ty += 58
    draw.text((right_x, ty), "PLASMA PHYSICS AND ARTIFICIAL INTELLIGENCE", font=f_en, fill="#CBD5E1")
    ty += 38
    draw.text((right_x, ty), "FOR AGRICULTURE AND ENVIRONMENT", font=f_en, fill="#CBD5E1")
    
    ty += 55
    draw.line([(right_x, ty), (W - 90, ty)], fill="#334155", width=2)
    
    # Author Card
    ty += 24
    author_box_w = W - 90 - right_x
    author_box_h = 205
    draw.rounded_rectangle([(right_x, ty), (right_x + author_box_w, ty + author_box_h)], radius=18, fill=(15, 23, 42, 230), outline="#0284C7", width=2)
    
    portrait_path = "figures/dr_chewa_official_portrait.jpg"
    if os.path.exists(portrait_path):
        try:
            port = Image.open(portrait_path).convert("RGBA")
            port = port.resize((150, 150), Image.Resampling.LANCZOS)
            mask = Image.new("L", (150, 150), 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.ellipse((0, 0, 150, 150), fill=255)
            poster.paste(port, (right_x + 25, ty + 27), mask)
            draw.ellipse((right_x + 23, ty + 25, right_x + 177, ty + 179), outline="#38BDF8", width=3)
        except Exception as e:
            print("Portrait error:", e)
    
    text_lead_x = right_x + 200
    draw.text((text_lead_x, ty + 26), "ผู้แต่ง / นักวิจัยหลัก :", font=f_author_title, fill="#94A3B8")
    draw.text((text_lead_x, ty + 75), "ผู้ช่วยศาสตราจารย์ ดร.ชีวะ ทัศนา", font=f_author_name, fill="#F8FAFC")
    draw.text((text_lead_x, ty + 130), "สาขาวิชาฟิสิกส์และวิทยาศาสตร์ทั่วไป คณะวิทยาศาสตร์และเทคโนโลยี", font=f_author_aff, fill="#38BDF8")
    draw.text((text_lead_x, ty + 165), "มหาวิทยาลัยราชภัฏรำไพพรรณี จังหวัดจันทบุรี", font=f_author_aff, fill="#94A3B8")
    
    # Badges row under author
    ty += author_box_h + 20
    badges = [
        ("• 199 หน้าฉบับเต็ม •", "#0284C7"),
        ("• 11 บทวิชาการ •", "#7C3AED"),
        ("• 6 ภาคผนวกสมบูรณ์ •", "#059669"),
        ("• 35+ บรรณานุกรม APA 7th •", "#D97706"),
    ]
    cur_bx = right_x
    for b_title, b_color in badges:
        bw = 320
        draw.rounded_rectangle([(cur_bx, ty), (cur_bx + bw, ty + 46)], radius=10, fill=(30, 41, 59, 240), outline=b_color, width=2)
        draw.text((cur_bx + bw//2, ty + 23), b_title, font=ImageFont.truetype(font_bold, 25), fill="#FFFFFF", anchor="mm")
        cur_bx += bw + 15
    
    # ----------------------------------------------------
    # 3. 3D VISUAL SYLLABUS ROADMAP (5 PARTS WITH 3D ICONS)
    # ----------------------------------------------------
    roadmap_y = hero_y + 1090
    draw.text((W//2, roadmap_y), "สารบัญภาพและโครงสร้างสาระสำคัญ 4 ภาควิชาการ + ภาคผนวก", font=f_sec_title, fill="#E2E8F0", anchor="mm")
    
    roadmap_top = roadmap_y + 35
    
    parts_data = [
        ("figures/icons_3d/badge_part1_plasma.png",
         "ภาค 1 : รากฐานฟิสิกส์พลาสมาและปรากฏการณ์การคายประจุ",
         "บทที่ 1–3  •  การกำเนิดพลาสมา, สปีชีส์ไวต่อปฏิกิริยา RONS, และการวินิจฉัยสเปกตรัม OES",
         "เจาะลึกกลไก Townsend breakdown, กฎ Paschen, Streamer, พลาสมาอุณหภูมิต่ำ และปฏิกิริยาเคมีฟิสิกส์ 30 สมการ",
         "#38BDF8"),
        
        ("figures/icons_3d/badge_part2_agri.png",
         "ภาค 2 : นวัตกรรมพลาสมาเพื่อการเกษตรแม่นยำและจัดการหลังการเก็บเกี่ยว",
         "บทที่ 4–6  •  ปุ๋ยยูเรียเขียว (Green Urea), น้ำกระตุ้น PAW, และรักษาโรครากเน่าโคนเน่าทุเรียน",
         "การตรึง N2 จากอากาศ, การกระตุ้นเมล็ดพันธุ์เร่งการงอก, สลายเชื้อรา Phytophthora, และสุขาภิบาลผลผลิต",
         "#34D399"),
        
        ("figures/icons_3d/badge_part3_env.png",
         "ภาค 3 : วิศวกรรมพลาสมาเพื่อการบำบัดและฟื้นฟูสิ่งแวดล้อม",
         "บทที่ 7–9  •  บำบัดกลิ่นยางพาราและสารอินทรีย์ระเหย VOCs, กำจัด PFAS, และฟื้นฟูดินด้วยไบโอชาร์",
         "เทคโนโลยีพลาสมาอุณหภูมิปกติบำบัดอากาศเสีย, ย่อยสลายสารมลพิษตกค้างยาวนานในน้ำ, และปรับปรุงคุณสมบัติดิน",
         "#2DD4BF"),
        
        ("figures/icons_3d/badge_part4_ai.png",
         "ภาค 4 : สถาปัตยกรรม AI, Deep Learning และวิศวกรรมระบบกำเนิดพลาสมา",
         "บทที่ 10–11  •  โมเดล Physics-Informed Neural Networks (PINN), ซอร์สโค้ด PyTorch, และ Solid-State Marx",
         "ปัญญาประดิษฐ์เรียนรู้สมการฟิสิกส์, แหล่งจ่ายพัลส์ไฟฟ้าแรงสูง SiC/GaN, มาตรฐานความปลอดภัย และการประเมิน LCA",
         "#A78BFA"),
        
        ("figures/icons_3d/badge_appendix_sop.png",
         "ภาคผนวก ก–ฉ : คู่มือปฏิบัติงานมาตรฐานภาคสนาม (SOPs) & บรรณานุกรม",
         "ภาคผนวก 6 ภาค  •  4 คู่มือ SOP ภาคสนาม, ค่าคงที่ทางฟิสิกส์, ซอร์สโค้ดระบบ, และดรรชนีสืบค้น 2 ภาษา",
         "SOP เตรียมน้ำ PAW, SOP กระตุ้นเมล็ด, SOP สอบเทียบ OES, SOP รักษาโรคทุเรียน, และ 35+ บรรณานุกรม APA 7th",
         "#F59E0B")
    ]
    
    # 5 Horizontal Cards with 3D Icons on Left
    card_h = 145
    card_gap = 16
    for idx, (icon_path, p_title, p_sub, p_desc, p_color) in enumerate(parts_data):
        cy = roadmap_top + idx * (card_h + card_gap)
        cx = 90
        cw = W - 180
        
        # Glass Card Background
        draw.rounded_rectangle([(cx, cy), (cx + cw, cy + card_h)], radius=18, fill=(15, 23, 42, 230), outline=p_color, width=2)
        
        # 3D Icon on Left
        if os.path.exists(icon_path):
            try:
                icon_img = Image.open(icon_path).convert("RGBA")
                # scale to 125x125
                icon_img = icon_img.resize((125, 125), Image.Resampling.LANCZOS)
                poster.paste(icon_img, (cx + 20, cy + 10), icon_img)
            except Exception as e:
                print("Icon error:", e)
        
        # Text block
        tx = cx + 165
        # Title
        draw.text((tx, cy + 18), p_title, font=f_part_title, fill="#FFFFFF")
        # Subtitle
        draw.text((tx, cy + 62), p_sub, font=f_part_sub, fill=p_color)
        # Description
        draw.text((tx, cy + 100), p_desc, font=f_part_desc, fill="#CBD5E1")
    
    # ----------------------------------------------------
    # 4. BOTTOM SECTION: ORDERING INFO & PROMPTPAY CARD
    # ----------------------------------------------------
    bot_y = roadmap_top + 5 * (card_h + card_gap) + 20
    draw.line([(90, bot_y), (W - 90, bot_y)], fill="#334155", width=2)
    
    cta_y = bot_y + 25
    pack_w = 1440
    pack_h = 580
    draw.rounded_rectangle([(90, cta_y), (90 + pack_w, cta_y + pack_h)], radius=22, fill=(15, 23, 42, 240), outline="#38BDF8", width=3)
    
    pdraw = ImageDraw.Draw(poster)
    px = 90 + 40
    py = cta_y + 30
    pdraw.text((px, py), "ข้อมูลการสั่งจองและสนับสนุนผลงานวิชาการ", font=f_cta_title, fill="#38BDF8")
    py += 55
    pdraw.text((px, py), "• รูปเล่มตำราขนาด Pocket Book สากล (6 x 9 นิ้ว) จำนวน 199 หน้า ปกอาร์ตการ์ดเคลือบด้าน พรีเมียม", font=f_cta_body, fill="#E2E8F0")
    py += 44
    pdraw.text((px, py), "• ภาพประกอบ 4 สี ตาราง และวงจรเทคนิค คมชัด 100% มาตรฐานเดียวกับตำราวิชาการระดับโลก", font=f_cta_body, fill="#E2E8F0")
    py += 44
    pdraw.text((px, py), "• มอบพร้อมสิทธิ์ดาวน์โหลดโค้ดตัวอย่าง Python / PyTorch PINN และแบบจำลองฟิสิกส์ในเล่ม", font=f_cta_body, fill="#E2E8F0")
    py += 44
    pdraw.text((px, py), "• เหมาะสำหรับ: นักศึกษาระดับปริญญาตรี-โท-เอก, อาจารย์, นักวิจัย และผู้พัฒนานวัตกรรม AI เกษตร", font=f_cta_body, fill="#E2E8F0")
    
    # Special Price Banner
    py += 50
    draw.rounded_rectangle([(px, py), (px + pack_w - 80, py + 115)], radius=16, fill=(30, 41, 59, 240), outline="#F59E0B", width=2)
    pdraw.text((px + 25, py + 32), "ราคาจำหน่ายเล่มละ :", font=ImageFont.truetype(font_bold, 40), fill="#FCD34D")
    pdraw.text((px + 320, py + 22), "450 บาท", font=f_cta_price, fill="#F59E0B")
    pdraw.text((px + 600, py + 42), "(รวมค่าจัดส่งด่วน EMS ทั่วประเทศ)", font=ImageFont.truetype(font_reg, 32), fill="#94A3B8")
    
    py += 135
    pdraw.text((px, py), "• รายได้ทั้งหมดสมทบทุนสนับสนุนงานวิจัยนวัตกรรมฟิสิกส์เกษตร มหาวิทยาลัยราชภัฏรำไพพรรณี •", 
               font=ImageFont.truetype(font_bold, 30), fill="#34D399")
    
    # Right Box: PromptPay Card
    pp_box_x = 90 + pack_w + 35
    pp_box_w = W - 90 - pp_box_x
    pp_box_h = pack_h
    
    draw.rounded_rectangle([(pp_box_x, cta_y), (pp_box_x + pp_box_w, cta_y + pp_box_h)], radius=22, fill=(255, 255, 255, 255), outline="#0284C7", width=3)
    
    pp_card_path = "figures/promptpay_qr_card.png"
    if os.path.exists(pp_card_path):
        pp_card = Image.open(pp_card_path).convert("RGBA")
        scale_w = (pp_box_w - 10) / pp_card.width
        scale_h = (pp_box_h - 10) / pp_card.height
        scale = min(scale_w, scale_h)
        new_pp_w = int(pp_card.width * scale)
        new_pp_h = int(pp_card.height * scale)
        pp_card = pp_card.resize((new_pp_w, new_pp_h), Image.Resampling.LANCZOS)
        
        off_x = pp_box_x + (pp_box_w - new_pp_w) // 2
        off_y = cta_y + (pp_box_h - new_pp_h) // 2
        poster.paste(pp_card, (off_x, off_y), pp_card)
    
    # ----------------------------------------------------
    # 5. FOOTER
    # ----------------------------------------------------
    foot_y = H - 65
    draw.text((W//2, foot_y), "ติดต่อสอบถาม / แจ้งหลักฐานการโอน : โทร 093-742-2654  |  สาขาวิชาฟิสิกส์ มหาวิทยาลัยราชภัฏรำไพพรรณี  |  GitHub: TsanaPhysics/plasma-agri-xai", 
              font=ImageFont.truetype(font_bold, 30), fill="#64748B", anchor="mm")
    
    # Save Images
    poster.save(output_png, quality=95)
    jpg_path = output_png.replace(".png", ".jpg")
    poster.convert("RGB").save(jpg_path, quality=92)
    print(f"Successfully generated 3D icon-centric visual promo poster to {output_png} and {jpg_path}")
    return output_png

if __name__ == "__main__":
    generate_visual_promo_poster()
