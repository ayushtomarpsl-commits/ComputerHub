"""Awesome Repos Day 1 (UPI Gateway): cut UI elements from the repo screenshots.

Run:  py -I source/repo01_ui_elements.py
Input : output/AwesomeRepos/Day01_UPI-Gateway/ui/original/*.png  (copied from the repo's screenshots/ folder)
Output: output/AwesomeRepos/Day01_UPI-Gateway/ui/elements/*.png  + logo + contact sheet
Crop boxes are in original-pixel coordinates (left, top, right, bottom).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "output" / "AwesomeRepos" / "Day01_UPI-Gateway" / "ui"
SRC, OUT = BASE / "original", BASE / "elements"

CROPS = {
    "hero_headline":     ("1-home.png", (300, 250, 1500, 910)),
    "hero_qr_card":      ("1-home.png", (1480, 520, 2650, 1400)),
    "features_title":    ("2-features.png", (300, 190, 1700, 600)),
    "features_grid":     ("2-features.png", (320, 640, 2620, 1620)),
    "api_docs_hero":     ("3-docs.png", (0, 125, 2938, 836)),
    "dashboard_full":    ("4-dashboard.png", (0, 0, 2940, 1840)),
    "dashboard_stats":   ("4-dashboard.png", (580, 230, 2900, 600)),
    "provider_picker":   ("5-add-payment-account.png", (110, 330, 1600, 850)),
    "money_stays_yours": ("5-add-payment-account.png", (1640, 320, 2370, 600)),
    "payment_page":      ("6-payment-page.png", (80, 50, 1680, 1670)),
    "verifying_card":    ("7-verifying-payment.png", (190, 190, 1740, 1070)),
    "success_card":      ("8-payment-success.png", (100, 100, 1650, 1030)),
}

INDIGO_A, INDIGO_B = (99, 102, 241), (67, 56, 202)   # brand-500 -> brand-700 (repo tailwind config)


def logo(size=512):
    """Rebuild the repo's logo mark (logo.blade.php): indigo gradient tile + white lightning bolt."""
    ss = size * 4
    grad = Image.new("RGB", (ss, ss))
    px = grad.load()
    for y in range(ss):
        for x in range(ss):
            t = (x + y) / (2 * ss)
            px[x, y] = tuple(int(a + (b - a) * t) for a, b in zip(INDIGO_A, INDIGO_B))
    mask = Image.new("L", (ss, ss), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, ss - 1, ss - 1), radius=int(ss * 0.25), fill=255)
    tile = Image.new("RGBA", (ss, ss), (0, 0, 0, 0))
    tile.paste(grad, (0, 0), mask)
    # SVG path "M13.5 2 4 14h6.5L9.5 22 19 10h-6.5z" on a 24-unit box, drawn at 18/32 of the tile (as in the repo)
    pts = [(13.5, 2), (4, 14), (10.5, 14), (9.5, 22), (19, 10), (12.5, 10)]
    s = ss * (18 / 32) / 24
    off = (ss - 24 * s) / 2
    ImageDraw.Draw(tile).polygon([(off + x * s, off + y * s) for x, y in pts], fill="white")
    return tile.resize((size, size), Image.LANCZOS)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    thumbs = []
    for name, (fn, box) in CROPS.items():
        im = Image.open(SRC / fn).convert("RGB")
        box = (max(0, box[0]), max(0, box[1]), min(im.width, box[2]), min(im.height, box[3]))
        c = im.crop(box)
        c.save(OUT / f"{name}.png", optimize=True)
        thumbs.append((name, c))
        print(f"{name:18s} {c.size}")
    logo().save(OUT / "upi_gateway_logo.png")

    # contact sheet for a quick visual check
    cols, cw, ch = 3, 520, 360
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw + 20) + 20, rows * (ch + 40) + 20), (235, 238, 245))
    d = ImageDraw.Draw(sheet)
    for i, (name, c) in enumerate(thumbs):
        t = c.copy()
        t.thumbnail((cw, ch))
        x, y = 20 + (i % cols) * (cw + 20), 20 + (i // cols) * (ch + 40)
        sheet.paste(t, (x, y + 18))
        d.text((x, y), name, fill=(200, 0, 0))
    sheet.save(BASE / "elements_contact_sheet.jpg", quality=82)


if __name__ == "__main__":
    main()
