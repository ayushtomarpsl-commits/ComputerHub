"""TurtleReels promo: cut clean HD UI elements from the raw captures.

Run:  py -I source/promo_turtlereels_elements.py
Input : output/promotions/TurtleReels/elements/raw/*   (site_* = 2x headless Edge captures of public pages,
        app_* = logged-in captures from Chrome)  +  elements/site/logo-mark.png
Output: output/promotions/TurtleReels/elements/hd/*.png  + hd_contact_sheet.jpg
Boxes are (left, top, right, bottom) in each raw image's pixels.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
E = ROOT / "output" / "promotions" / "TurtleReels" / "elements"
RAW, OUT = E / "raw", E / "hd"

CROPS = {
    # name                     source                    box                         round-corner radius (0 = none)
    "01_wordmark_card":       ("site_home_2x.png",     (16, 700, 1274, 1140),    40),
    "02_feature_tiles":       ("site_home_2x.png",     (1288, 1155, 2556, 2155), 0),
    "03_auto_title_panel":    ("site_home_2x.png",     (60, 3870, 1110, 5080),   0),
    "04_long_video_card":     ("site_home_2x.png",     (1110, 3850, 2520, 5090), 0),
    "05_pricing_title":       ("site_pricing_2x.png",  (40, 300, 2000, 620),     0),
    "06_pricing_table":       ("site_pricing_2x.png",  (40, 680, 2500, 2160),    0),
    "07_styles_by_plan":      ("site_pricing_2x.png",  (40, 2400, 2500, 4040),   0),
    "08_signup_free_card":    ("site_signup_2x.png",   (40, 150, 1260, 1800),    0),
    "09_dashboard":           ("app_dashboard.png",    (0, 0, 1568, 710),        0),
    "10_dashboard_header":    ("app_dashboard.png",    (0, 0, 1568, 360),        0),
    "11_create_box":          ("app_create_now.png",   (0, 0, 1053, 739),        0),
    "12_create_autopilot":    ("app_create_repeat.png", (0, 0, 1075, 819),       0),
    "13_your_videos":         ("app_your_videos.png",  (0, 90, 1098, 863),       0),
    "14_music_no_copyright":  ("app_music.png",        (0, 0, 1448, 335),        0),
    "15_laptop_off_note":     ("app_coming_up.png",    (16, 16, 750, 610),         0),
    "16_connect_youtube_btn": ("app_connect_youtube.png", (12, 12, 688, 178),    44),
}


def rounded(im, r):
    if not r:
        return im
    im = im.convert("RGBA")
    m = Image.new("L", (im.width * 2, im.height * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, m.width - 1, m.height - 1], radius=r * 2, fill=255)
    im.putalpha(m.resize(im.size, Image.LANCZOS))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cache, made = {}, []
    for name, (src, box, r) in CROPS.items():
        if src not in cache:
            cache[src] = Image.open(RAW / src).convert("RGB")
        im = cache[src]
        box = (max(0, box[0]), max(0, box[1]), min(im.width, box[2]), min(im.height, box[3]))
        c = rounded(im.crop(box), r)
        c.save(OUT / f"{name}.png", optimize=True)
        made.append((name, c))
        print(f"{name:26s} {c.size}")
    logo = Image.open(E / "site" / "logo-mark.png").convert("RGBA")
    logo.resize((512, 512), Image.LANCZOS).save(OUT / "00_logo_mark_512.png")
    made.insert(0, ("00_logo_mark_512", Image.open(OUT / "00_logo_mark_512.png")))

    cols, cw, ch = 4, 420, 300
    rows = (len(made) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw + 16) + 16, rows * (ch + 34) + 16), (120, 120, 130))
    d = ImageDraw.Draw(sheet)
    for i, (n, c) in enumerate(made):
        t = c.convert("RGBA")
        t.thumbnail((cw, ch))
        x, y = 16 + (i % cols) * (cw + 16), 16 + (i // cols) * (ch + 34)
        sheet.paste(t, (x, y + 20), t)
        d.text((x, y + 2), n, fill=(255, 255, 0))
    sheet.save(E / "hd_contact_sheet.jpg", quality=85)


if __name__ == "__main__":
    main()
