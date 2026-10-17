import os
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def crc16(data: str) -> str:
    crc = 0xFFFF
    for c in data.encode("ascii"):
        crc ^= (c << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def generate_promptpay_payload(mobile: str, amount: float = None) -> str:
    clean_mobile = "".join(filter(str.isdigit, mobile))
    if clean_mobile.startswith("0"):
        target = "0066" + clean_mobile[1:]
    else:
        target = clean_mobile
    
    subtag_aid = "0016A000000677010111"
    subtag_target = f"01{len(target):02d}{target}"
    tag29_data = subtag_aid + subtag_target
    tag29 = f"29{len(tag29_data):02d}{tag29_data}"
    
    parts = [
        "000201",
        "010211", # static
        tag29,
        "5303764", # THB
    ]
    if amount is not None and amount > 0:
        amt_str = f"{amount:.2f}"
        parts.append(f"54{len(amt_str):02d}{amt_str}")
        parts[1] = "010212" # dynamic
    parts.append("5802TH")
    
    raw = "".join(parts) + "6304"
    crc = crc16(raw)
    return raw + crc

def make_promptpay_card(output_path="figures/promptpay_qr_card.png"):
    payload = generate_promptpay_payload("0937422654")
    print(f"Generated Payload: {payload}")
    
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#002D62", back_color="white").convert("RGBA")
    
    card_w, card_h = 600, 800
    card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(card)
    
    # PromptPay Top Banner (Standard Navy Blue #003764)
    header_h = 130
    draw.rectangle([(0, 0), (card_w, header_h)], fill="#003B70")
    
    font_bold = ImageFont.truetype("fonts/THSarabun Bold.ttf", 38)
    font_sub = ImageFont.truetype("fonts/THSarabun.ttf", 26)
    font_header = ImageFont.truetype("fonts/THSarabun Bold.ttf", 46)
    font_en = ImageFont.truetype("fonts/THSarabun Bold.ttf", 28)
    
    # PromptPay Header Text
    draw.text((card_w//2, 35), "พร้อมเพย์ (PromptPay)", font=font_header, fill="#FFFFFF", anchor="mm")
    draw.text((card_w//2, 85), "สแกน QR เพื่อโอนเงินเข้าบัญชี", font=font_en, fill="#64B5F6", anchor="mm")
    
    # Paste QR Code
    qr_w, qr_h = qr_img.size
    qr_x = (card_w - qr_w) // 2
    qr_y = 150
    card.paste(qr_img, (qr_x, qr_y), qr_img)
    
    # Information Box below QR
    info_y = qr_y + qr_h + 15
    draw.line([(40, info_y), (card_w - 40, info_y)], fill="#E2E8F0", width=2)
    
    # Details
    draw.text((card_w//2, info_y + 35), "นายชีวะ ทัศนา", font=font_bold, fill="#0F172A", anchor="mm")
    draw.text((card_w//2, info_y + 75), "ธนาคารกรุงเทพ (Bangkok Bank)", font=font_sub, fill="#334155", anchor="mm")
    
    # Mobile pill
    pill_w, pill_h = 320, 50
    pill_x0 = (card_w - pill_w) // 2
    pill_y0 = info_y + 110
    draw.rounded_rectangle([(pill_x0, pill_y0), (pill_x0 + pill_w, pill_y0 + pill_h)], radius=12, fill="#F1F5F9", outline="#0284C7", width=2)
    draw.text((card_w//2, pill_y0 + pill_h//2), "093-742-2654", font=font_bold, fill="#0369A1", anchor="mm")
    
    draw.text((card_w//2, pill_y0 + pill_h + 35), "รับเงินโอนสะดวก ปลอดภัย ไม่มีค่าธรรมเนียม", font=font_sub, fill="#64748B", anchor="mm")
    
    card.save(output_path, dpi=(300, 300))
    print(f"Saved PromptPay card to {output_path}")
    return output_path

if __name__ == "__main__":
    make_promptpay_card()
