import os
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance

def make_3d_badge(crop_img, border_color="#38BDF8", size=260):
    """Takes an image, enhances contrast/saturation, applies circular mask, glassmorphism border and outer glow."""
    crop_img = ImageEnhance.Color(crop_img).enhance(1.3)
    crop_img = ImageEnhance.Contrast(crop_img).enhance(1.2)
    crop_sq = ImageOps.fit(crop_img, (size, size), Image.Resampling.LANCZOS)
    
    super_size = size * 2
    mask = Image.new("L", (super_size, super_size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse((8, 8, super_size - 8, super_size - 8), fill=255)
    mask = mask.resize((size, size), Image.Resampling.LANCZOS)
    
    circ = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circ.paste(crop_sq, (0, 0), mask)
    
    pad = 32
    badge_w = size + pad * 2
    badge = Image.new("RGBA", (badge_w, badge_w), (0, 0, 0, 0))
    
    # Outer Glow
    glow = Image.new("RGBA", (badge_w, badge_w), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((pad - 6, pad - 6, pad + size + 6, pad + size + 6), fill=border_color)
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    badge.paste(glow, (0, 0), glow)
    
    # Paste circular image
    badge.paste(circ, (pad, pad), circ)
    
    # Gloss highlight on upper half
    gloss = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gl_draw = ImageDraw.Draw(gloss)
    gl_draw.chord((0, 0, size, size), 180, 0, fill=(255, 255, 255, 45))
    gloss = Image.composite(gloss, Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask)
    badge.paste(gloss, (pad, pad), gloss)
    
    # Double Ring Border
    ring = Image.new("RGBA", (badge_w, badge_w), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(ring)
    rdraw.ellipse((pad, pad, pad + size, pad + size), outline=border_color, width=5)
    rdraw.ellipse((pad + 4, pad + 4, pad + size - 4, pad + size - 4), outline=(255, 255, 255, 140), width=2)
    badge = Image.alpha_composite(badge, ring)
    
    return badge

def create_all_3d_icons():
    os.makedirs("figures/icons_3d", exist_ok=True)
    
    urea_im = Image.open("figures/cover_art_concept_plasma_urea.jpg")
    rob_im = Image.open("figures/cover_option_a_robot_plasma.jpg")
    orch_im = Image.open("figures/cover_v9_cyber_orchard.jpg")
    
    # 1. Plasma Discharge: Plasma N2 Fixation column & glowing molecules
    p_crop = urea_im.crop((100, 700, 360, 960))
    b1 = make_3d_badge(p_crop, border_color="#38BDF8", size=240)
    b1.save("figures/icons_3d/badge_part1_plasma.png")
    
    # 2. Agriculture: Golden ripe durian fruit on tree
    d_crop = urea_im.crop((850, 680, 1110, 940))
    b2 = make_3d_badge(d_crop, border_color="#34D399", size=240)
    b2.save("figures/icons_3d/badge_part2_agri.png")
    
    # 3. Environment: Cyber orchard with environmental monitoring
    o_crop = orch_im.crop((120, 340, 480, 700))
    b3 = make_3d_badge(o_crop, border_color="#2DD4BF", size=240)
    b3.save("figures/icons_3d/badge_part3_env.png")
    
    # 4. AI & PINN Robot: 3D Robot Scientist
    r_crop = rob_im.crop((380, 520, 720, 860))
    b4 = make_3d_badge(r_crop, border_color="#A78BFA", size=240)
    b4.save("figures/icons_3d/badge_part4_ai.png")
    
    # 5. Appendix & SOP: Holographic OES spectral waveform screen
    s_crop = urea_im.crop((180, 920, 440, 1180))
    b5 = make_3d_badge(s_crop, border_color="#F59E0B", size=240)
    b5.save("figures/icons_3d/badge_appendix_sop.png")
    
    print("Enhanced 3D icon badges with true elements generated successfully!")

if __name__ == "__main__":
    create_all_3d_icons()
