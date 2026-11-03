"""Make a transparent logo: remove ONLY the black area outside the cyan scalloped border.
The black inside the badge is kept. Pixels of the artwork are not changed."""
import sys
import cv2
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
img = cv2.imread(src)
h, w = img.shape[:2]
# "dark" pixels = candidate outside background
dark = (img.max(axis=2) < 60).astype(np.uint8)
mask = np.zeros((h + 2, w + 2), np.uint8)
outside = np.zeros((h, w), np.uint8)
for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
    tmp = dark.copy()
    m = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(tmp, m, seed, 2)
    outside |= (tmp == 2).astype(np.uint8)
# Soft alpha at the border only (the cyan edge stays fully opaque)
alpha = 1.0 - outside.astype(np.float32)
blur = cv2.GaussianBlur(alpha, (0, 0), 0.8)
alpha = np.where(outside == 1, np.clip(blur, 0, 1) * 0.0 + np.clip((blur - 0.5) * 2, 0, 1), 1.0)
rgba = np.dstack([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (alpha * 255).astype(np.uint8)])
im = Image.fromarray(rgba, "RGBA")
im = im.crop(im.getbbox())
im.save(dst)
print("saved", dst, im.size, "outside px:", int(outside.sum()))
