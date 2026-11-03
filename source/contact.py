"""Make a contact sheet of PNG frames: py -I source/contact.py out.jpg cols scale files..."""
import sys
from PIL import Image, ImageDraw
out, cols, sc = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
ims = [Image.open(p).convert("RGB") for p in sys.argv[4:]]
w, h = int(1080 * sc), int(1920 * sc)
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h), "black")
for k, (im, p) in enumerate(zip(ims, sys.argv[4:])):
    sheet.paste(im.resize((w, h), Image.LANCZOS), ((k % cols) * w, (k // cols) * h))
    ImageDraw.Draw(sheet).text(((k % cols) * w + 6, (k // cols) * h + 4), p.split("_")[-1][:-4], fill="red")
sheet.save(out, quality=90)
