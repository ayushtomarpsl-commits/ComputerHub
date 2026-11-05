"""Drawing helpers: fonts, easing, anti-aliased shapes, card sprites, icons, sprite placement."""
import math
import os
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
SS = 2  # supersampling for anti-aliased shapes

# ---- palette (from the Computer Hub logo). THEME env: "light" (default) or "dark" ----
THEME = os.environ.get("THEME", "light").lower()
if THEME == "dark":  # dark glass cards on the ref_bg nebula
    INK = (240, 244, 252)      # main text on cards
    INK2 = (196, 206, 228)
    MUTED = (140, 156, 192)
    LINE = (46, 62, 100)       # dividers on cards
    DARK = (14, 20, 36)        # dark text on bright chips (yellow)
    BLUE = (70, 156, 255)
    CYAN = (0, 186, 246)
    GREEN = (60, 214, 100)
    PURPLE = (184, 120, 255)
    YELLOW = (255, 206, 46)
    ORANGE = (255, 150, 40)
    PAPER = (14, 21, 42)       # card fill
    PANEL = (22, 32, 60)       # chrome bars / rows inside cards
    SKEL = (40, 54, 88)        # skeleton bars, empty progress bars
    BORDER = (52, 112, 178)    # card outline
    GLOW = (0, 150, 240)       # card glow colour
    CARD_ALPHA = 232           # slightly see-through glass
    SHADOW_DY, SHADOW_A = 6, 60
    T_GREEN, T_YELLOW, T_CYAN = (84, 232, 60), (255, 206, 46), (0, 186, 246)  # text on tinted chips
    DARK_YEL = (255, 190, 40)
    LOGO_GLOW, LOGO_GLOW_A = (0, 186, 246), 150
else:  # light: white cards with soft shadows on a light background
    INK = (20, 27, 45)
    INK2 = (52, 64, 92)
    MUTED = (128, 140, 165)
    LINE = (230, 235, 244)
    DARK = (20, 27, 45)
    BLUE = (30, 111, 224)
    CYAN = (0, 170, 236)
    GREEN = (34, 176, 75)
    PURPLE = (160, 92, 226)
    YELLOW = (255, 200, 40)
    ORANGE = (255, 140, 30)
    PAPER = (255, 255, 255)
    PANEL = (246, 248, 252)
    SKEL = (234, 238, 245)
    BORDER = (226, 232, 243)
    GLOW = (24, 42, 88)        # neutral drop shadow
    CARD_ALPHA = 255
    SHADOW_DY, SHADOW_A = 16, 52
    T_GREEN, T_YELLOW, T_CYAN = (20, 130, 55), (150, 95, 0), (0, 120, 175)
    DARK_YEL = (214, 150, 0)
    LOGO_GLOW, LOGO_GLOW_A = (20, 40, 90), 80
LGREEN = (84, 222, 60)     # logo green (accents)
WHITE = (255, 255, 255)
# caption box stays white with dark text in both themes
CAP_INK = (20, 27, 45)
CAP_BLUE = (30, 111, 224)

FONT_DIR = r"C:\Windows\Fonts"
FONTS = {"bold": "segoeuib.ttf", "semi": "seguisb.ttf", "black": "seguibl.ttf",
         "reg": "segoeui.ttf", "mono": "consolab.ttf", "monor": "consola.ttf"}


@lru_cache(None)
def font(kind, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, FONTS[kind]), int(round(size)))


def tint(col, k):
    """Mix colour with the dark card colour (k=1 -> card colour). Used for chip/tile backgrounds."""
    return tuple(int(c + (p - c) * k) for c, p in zip(col[:3], PAPER))


def rgba(col, a=255):
    return (col[0], col[1], col[2], int(a))


# ---- easing ----
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def prog(t, t0, dur):
    return clamp((t - t0) / dur) if dur > 0 else float(t >= t0)


def out_cubic(x):
    return 1 - (1 - x) ** 3


def in_cubic(x):
    return x ** 3


def smooth(x):
    return x * x * (3 - 2 * x)


def out_back(x, s=1.70158):
    x = x - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


def lerp(a, b, k):
    return a + (b - a) * k


def trans(t, t0, t1, din=0.45, dout=0.28, rise=46, s0=0.86):
    """Standard enter (pop + slide up + bounce) / exit (shrink + fade) for a scene element.
    Returns (scale, alpha, dy)."""
    pi = prog(t, t0, din)
    po = prog(t, t1 - dout, dout) if t1 is not None else 0.0
    s = (s0 + (1 - s0) * out_back(pi)) * (1 - 0.07 * in_cubic(po))
    a = out_cubic(clamp(pi * 1.7)) * (1 - smooth(po))
    dy = rise * (1 - out_cubic(pi)) - 36 * in_cubic(po)
    return s, a, dy


def pop(t, t0, dur=0.32, s0=0.5):
    p = prog(t, t0, dur)
    return s0 + (1 - s0) * out_back(p), clamp(p * 2.2)


# ---- pen that draws in 1x units onto a supersampled canvas ----
class Pen:
    def __init__(self, img, ss=SS):
        self.img, self.ss = img, ss
        self.d = ImageDraw.Draw(img)

    def _b(self, box):
        return [v * self.ss for v in box]

    def rr(self, box, r, fill=None, outline=None, width=0):
        self.d.rounded_rectangle(self._b(box), radius=r * self.ss, fill=fill, outline=outline,
                                 width=int(round(width * self.ss)))

    def rect(self, box, fill=None, outline=None, width=0):
        self.d.rectangle(self._b(box), fill=fill, outline=outline, width=int(round(width * self.ss)))

    def ell(self, box, fill=None, outline=None, width=0):
        self.d.ellipse(self._b(box), fill=fill, outline=outline, width=int(round(width * self.ss)))

    def circ(self, cx, cy, r, fill=None, outline=None, width=0):
        self.ell((cx - r, cy - r, cx + r, cy + r), fill, outline, width)

    def poly(self, pts, fill=None, outline=None, width=0):
        self.d.polygon([(x * self.ss, y * self.ss) for x, y in pts], fill=fill, outline=outline,
                       width=int(round(width * self.ss)))

    def line(self, pts, fill, width, caps=True):
        sp = [(x * self.ss, y * self.ss) for x, y in pts]
        wd = int(round(width * self.ss))
        self.d.line(sp, fill=fill, width=wd, joint="curve")
        if caps:
            r = wd / 2
            for x, y in (sp[0], sp[-1]):
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=fill)

    def arc(self, box, a0, a1, fill, width):
        self.d.arc(self._b(box), a0, a1, fill=fill, width=int(round(width * self.ss)))

    def text(self, x, y, s, kind, size, fill, anchor="la", spacing=0):
        f = font(kind, size * self.ss)
        if not spacing:
            self.d.text((x * self.ss, y * self.ss), s, font=f, fill=fill, anchor=anchor)
            return
        tw = text_w(s, kind, size, spacing)
        if anchor[0] == "m":
            x -= tw / 2
        elif anchor[0] == "r":
            x -= tw
        cx = x * self.ss
        for ch in s:
            self.d.text((cx, y * self.ss), ch, font=f, fill=fill, anchor="l" + anchor[1])
            cx += f.getlength(ch) + spacing * self.ss


def text_w(s, kind, size, spacing=0):
    f = font(kind, size)
    if not spacing:
        return f.getlength(s)
    return sum(f.getlength(c) for c in s) + spacing * (len(s) - 1)


def canvas(w, h, cb, ss=SS):
    """Draw with Pen on a supersampled canvas and return the 1x RGBA image."""
    big = Image.new("RGBA", (int(w * ss), int(h * ss)), (0, 0, 0, 0))
    cb(Pen(big, ss))
    return big.resize((int(w), int(h)), Image.LANCZOS) if ss != 1 else big


# ---- shadows & cards ----
SM = 64  # shadow margin around every card sprite


@lru_cache(None)
def _shadow(w, h, r, strength=1.0):
    sh = Image.new("L", (w + 2 * SM, h + 2 * SM), 0)
    d = ImageDraw.Draw(sh)
    d.rounded_rectangle([SM, SM + SHADOW_DY, SM + w, SM + h + SHADOW_DY], radius=r, fill=int(SHADOW_A * strength))
    soft = sh.filter(ImageFilter.GaussianBlur(24))
    tight = Image.new("L", sh.size, 0)
    ImageDraw.Draw(tight).rounded_rectangle([SM, SM + 3, SM + w, SM + h + 3], radius=r, fill=int(26 * strength))
    tight = tight.filter(ImageFilter.GaussianBlur(4))
    a = np.minimum(np.asarray(soft, np.uint16) + np.asarray(tight, np.uint16), 255).astype(np.uint8)
    out = Image.new("RGBA", sh.size, GLOW + (0,))
    out.putalpha(Image.fromarray(a))
    return out


def card(w, h, r=34, cb=None, fill=PAPER, border=BORDER, shadow=1.0, border_w=2, fill_a=CARD_ALPHA):
    """Dark glass rounded card with a soft cyan glow. Returned sprite has SM margin on each side."""
    def draw(p):
        p.rr((0, 0, w - 1, h - 1), r, fill=rgba(fill, fill_a), outline=rgba(border), width=border_w)
        if fill_a < 255:  # thin top highlight = glass edge
            p.line([(r, 3), (w - r, 3)], (255, 255, 255, 40), 2, caps=False)
        if cb:
            cb(p)
    body = canvas(w, h, draw)
    if not shadow:
        out = Image.new("RGBA", (w + 2 * SM, h + 2 * SM), (0, 0, 0, 0))
    else:
        out = _shadow(w, h, r, shadow).copy()
    out.alpha_composite(body, (SM, SM))
    return out


def with_margin(img):
    out = Image.new("RGBA", (img.width + 2 * SM, img.height + 2 * SM), (0, 0, 0, 0))
    out.alpha_composite(img, (SM, SM))
    return out


# ---- placement with sub-pixel position, scale and alpha ----
def fade(img, a):
    if a >= 0.999:
        return img
    out = img.copy()
    al = np.asarray(img.getchannel("A"), np.float32) * a
    out.putalpha(Image.fromarray(al.astype(np.uint8)))
    return out


def put(frame, spr, cx, cy, s=1.0, a=1.0, sx=None):
    """Composite sprite centred at (cx, cy) with uniform scale s (or x-scale sx) and opacity a."""
    if a <= 0.004 or s <= 0.01:
        return
    sxx = s if sx is None else s * sx
    if sxx <= 0.01:
        return
    w, h = spr.size
    x0 = cx - w * sxx / 2
    y0 = cy - h * s / 2
    ix, iy = math.floor(x0), math.floor(y0)
    fx, fy = x0 - ix, y0 - iy
    if abs(sxx - 1) < 1e-3 and abs(s - 1) < 1e-3 and fx < 1e-3 and fy < 1e-3:
        img = spr
    else:
        ow, oh = int(math.ceil(w * sxx + fx)) + 1, int(math.ceil(h * s + fy)) + 1
        img = spr.transform((ow, oh), Image.AFFINE, (1 / sxx, 0, -fx / sxx, 0, 1 / s, -fy / s),
                            resample=Image.BILINEAR)
    if a < 0.999:
        img = fade(img, a)
    # clip to frame
    sx0, sy0 = max(0, -ix), max(0, -iy)
    dx0, dy0 = max(0, ix), max(0, iy)
    ex = min(img.width, W - ix)
    ey = min(img.height, H - iy)
    if ex <= sx0 or ey <= sy0:
        return
    frame.alpha_composite(img, (dx0, dy0), (sx0, sy0, ex, ey))


# ---- icons (drawn in 1x units with a Pen) ----
def star(cx, cy, ro, ri, n=4, rot=-90):
    pts = []
    for k in range(n * 2):
        r = ro if k % 2 == 0 else ri
        a = math.radians(rot + k * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def icon(p, name, cx, cy, s, col, bg=WHITE):
    h = s / 2
    c = rgba(col)
    if name == "code":
        p.text(cx, cy + s * 0.02, "</>", "mono", s * 0.62, c, anchor="mm")
    elif name == "laptop":
        p.rr((cx - h * 0.78, cy - h * 0.7, cx + h * 0.78, cy + h * 0.32), s * 0.06, outline=c, width=s * 0.085)
        p.rr((cx - h, cy + h * 0.42, cx + h, cy + h * 0.62), s * 0.05, fill=c)
    elif name == "cloud":
        p.circ(cx - h * 0.38, cy + h * 0.12, h * 0.36, fill=c)
        p.circ(cx + h * 0.08, cy - h * 0.12, h * 0.5, fill=c)
        p.circ(cx + h * 0.55, cy + h * 0.16, h * 0.32, fill=c)
        p.rr((cx - h * 0.74, cy + h * 0.1, cx + h * 0.87, cy + h * 0.48), h * 0.19, fill=c)
    elif name == "chip":
        p.rr((cx - h * 0.55, cy - h * 0.55, cx + h * 0.55, cy + h * 0.55), s * 0.08, outline=c, width=s * 0.08)
        p.rr((cx - h * 0.25, cy - h * 0.25, cx + h * 0.25, cy + h * 0.25), s * 0.03, fill=c)
        for k in (-0.3, 0, 0.3):
            for (x0, y0, x1, y1) in [(cx + k * h, cy - h * 0.62, cx + k * h, cy - h * 0.9),
                                     (cx + k * h, cy + h * 0.62, cx + k * h, cy + h * 0.9),
                                     (cx - h * 0.62, cy + k * h, cx - h * 0.9, cy + k * h),
                                     (cx + h * 0.62, cy + k * h, cx + h * 0.9, cy + k * h)]:
                p.line([(x0, y0), (x1, y1)], c, s * 0.07)
    elif name == "db":
        for k in range(3):
            y = cy - h * 0.55 + k * h * 0.5
            p.ell((cx - h * 0.7, y - h * 0.18, cx + h * 0.7, y + h * 0.42), fill=c)
            p.ell((cx - h * 0.62, y - h * 0.13, cx + h * 0.62, y + h * 0.17), fill=rgba(tint(col, 0.55)))
    elif name == "gear":
        pts = []
        for k in range(32):
            a = math.radians(k * 360 / 32)
            r = h * (0.88 if (k // 2) % 2 == 0 else 0.66)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        p.poly(pts, fill=c)
        p.circ(cx, cy, h * 0.28, fill=rgba(bg))
    elif name == "spark":
        p.poly(star(cx - h * 0.1, cy + h * 0.1, h * 0.85, h * 0.22), fill=c)
        p.poly(star(cx + h * 0.62, cy - h * 0.58, h * 0.32, h * 0.09), fill=c)
    elif name == "briefcase":
        p.rr((cx - h * 0.34, cy - h * 0.72, cx + h * 0.34, cy - h * 0.25), s * 0.07, outline=c, width=s * 0.075)
        p.rr((cx - h * 0.85, cy - h * 0.38, cx + h * 0.85, cy + h * 0.68), s * 0.1, fill=c)
        p.rect((cx - h * 0.85, cy + h * 0.02, cx + h * 0.85, cy + h * 0.1), fill=rgba(bg))
    elif name == "rupee":
        p.circ(cx, cy, h * 0.9, fill=c)
        p.text(cx, cy + h * 0.04, "\u20b9", "bold", s * 0.62, rgba(WHITE), anchor="mm")
    elif name == "user":
        p.circ(cx, cy - h * 0.3, h * 0.36, fill=c)
        p.d.pieslice(p._b((cx - h * 0.72, cy + h * 0.12, cx + h * 0.72, cy + h * 1.5)), 180, 360, fill=c)
    elif name == "users":
        lc = rgba(tint(col, 0.45))
        p.circ(cx + h * 0.38, cy - h * 0.3, h * 0.28, fill=lc)
        p.d.pieslice(p._b((cx - h * 0.05, cy + h * 0.05, cx + h * 0.95, cy + h * 1.2)), 180, 360, fill=lc)
        p.circ(cx - h * 0.18, cy - h * 0.25, h * 0.34, fill=c)
        p.d.pieslice(p._b((cx - h * 0.85, cy + h * 0.15, cx + h * 0.5, cy + h * 1.45)), 180, 360, fill=c)
    elif name == "news":
        p.rr((cx - h * 0.78, cy - h * 0.7, cx + h * 0.78, cy + h * 0.7), s * 0.08, outline=c, width=s * 0.08)
        p.rect((cx - h * 0.5, cy - h * 0.42, cx - h * 0.02, cy + h * 0.02), fill=c)
        for k, (x0, x1) in enumerate([(0.12, 0.5), (0.12, 0.5), (-0.5, 0.5)]):
            y = cy - h * 0.36 + k * h * 0.32 + (h * 0.18 if k == 2 else 0)
            p.line([(cx + x0 * h, y), (cx + x1 * h, y)], c, s * 0.07)
    elif name == "shield":
        p.poly([(cx, cy - h * 0.9), (cx + h * 0.75, cy - h * 0.6), (cx + h * 0.68, cy + h * 0.2),
                (cx, cy + h * 0.92), (cx - h * 0.68, cy + h * 0.2), (cx - h * 0.75, cy - h * 0.6)], fill=c)
        p.text(cx, cy - h * 0.02, "!", "black", s * 0.66, rgba(WHITE), anchor="mm")
    elif name == "warn":
        p.poly([(cx, cy - h * 0.86), (cx + h * 0.92, cy + h * 0.74), (cx - h * 0.92, cy + h * 0.74)], fill=c)
        p.text(cx, cy + h * 0.16, "!", "black", s * 0.6, rgba(DARK), anchor="mm")
    elif name == "check":
        p.circ(cx, cy, h * 0.92, fill=c)
        p.line([(cx - h * 0.42, cy + h * 0.02), (cx - h * 0.1, cy + h * 0.34), (cx + h * 0.46, cy - h * 0.3)],
               rgba(WHITE), s * 0.12)
    elif name == "chart":
        for k, hh in enumerate([0.45, 0.8, 1.25]):
            x = cx - h * 0.65 + k * h * 0.55
            p.rr((x, cy + h * 0.75 - hh * h, x + h * 0.36, cy + h * 0.75), s * 0.04, fill=c)
    elif name == "book":
        p.poly([(cx, cy - h * 0.45), (cx - h * 0.9, cy - h * 0.7), (cx - h * 0.9, cy + h * 0.6), (cx, cy + h * 0.82)], fill=c)
        p.poly([(cx, cy - h * 0.45), (cx + h * 0.9, cy - h * 0.7), (cx + h * 0.9, cy + h * 0.6), (cx, cy + h * 0.82)],
               fill=rgba(tint(col, 0.35)))
    elif name == "share":
        pts = [(cx - h * 0.55, cy), (cx + h * 0.5, cy - h * 0.55), (cx + h * 0.5, cy + h * 0.55)]
        p.line([pts[1], pts[0], pts[2]], c, s * 0.08)
        for x, y in pts:
            p.circ(x, y, h * 0.24, fill=c)
    elif name == "heart":
        p.circ(cx - h * 0.36, cy - h * 0.2, h * 0.42, fill=c)
        p.circ(cx + h * 0.36, cy - h * 0.2, h * 0.42, fill=c)
        p.poly([(cx - h * 0.76, cy - h * 0.06), (cx + h * 0.76, cy - h * 0.06), (cx, cy + h * 0.8)], fill=c)
    elif name == "trend":
        p.line([(cx - h * 0.85, cy + h * 0.55), (cx - h * 0.25, cy - h * 0.02), (cx + h * 0.12, cy + h * 0.3),
                (cx + h * 0.8, cy - h * 0.45)], c, s * 0.1)
        p.poly([(cx + h * 0.92, cy - h * 0.62), (cx + h * 0.42, cy - h * 0.56), (cx + h * 0.86, cy - h * 0.1)], fill=c)
    elif name == "plus":
        p.line([(cx - h * 0.5, cy), (cx + h * 0.5, cy)], c, s * 0.14)
        p.line([(cx, cy - h * 0.5), (cx, cy + h * 0.5)], c, s * 0.14)
    elif name == "bolt":
        p.poly([(cx + h * 0.15, cy - h * 0.9), (cx - h * 0.55, cy + h * 0.12), (cx - h * 0.02, cy + h * 0.12),
                (cx - h * 0.18, cy + h * 0.9), (cx + h * 0.55, cy - h * 0.15), (cx + h * 0.02, cy - h * 0.15)], fill=c)
    elif name == "puzzle":
        p.rr((cx - h * 0.7, cy - h * 0.45, cx + h * 0.45, cy + h * 0.75), s * 0.08, fill=c)
        p.circ(cx - h * 0.12, cy - h * 0.55, h * 0.24, fill=c)
        p.circ(cx + h * 0.58, cy + h * 0.15, h * 0.24, fill=c)
    elif name == "search":
        p.circ(cx - h * 0.15, cy - h * 0.15, h * 0.5, outline=c, width=s * 0.12)
        p.line([(cx + h * 0.24, cy + h * 0.24), (cx + h * 0.78, cy + h * 0.78)], c, s * 0.15)
    elif name == "chat":
        p.rr((cx - h * 0.85, cy - h * 0.68, cx + h * 0.85, cy + h * 0.42), h * 0.28, fill=c)
        p.poly([(cx - h * 0.45, cy + h * 0.3), (cx - h * 0.6, cy + h * 0.85), (cx - h * 0.05, cy + h * 0.38)], fill=c)
        for k in (-1, 0, 1):
            p.circ(cx + k * h * 0.4, cy - h * 0.13, h * 0.1, fill=rgba(bg))
    elif name == "star":
        p.poly(star(cx, cy + h * 0.06, h * 0.95, h * 0.4, n=5), fill=c)
    elif name == "link":
        for dx in (-0.32, 0.32):
            p.rr((cx + dx * h - h * 0.5, cy - h * 0.3, cx + dx * h + h * 0.5, cy + h * 0.3), h * 0.3, outline=c,
                 width=s * 0.11)
    elif name == "up":
        p.poly([(cx, cy - h * 0.8), (cx + h * 0.75, cy + h * 0.05), (cx + h * 0.3, cy + h * 0.05),
                (cx + h * 0.3, cy + h * 0.75), (cx - h * 0.3, cy + h * 0.75), (cx - h * 0.3, cy + h * 0.05),
                (cx - h * 0.75, cy + h * 0.05)], fill=c)
    elif name == "clock":
        p.circ(cx, cy, h * 0.85, outline=c, width=s * 0.1)
        p.line([(cx, cy), (cx, cy - h * 0.5)], c, s * 0.09)
        p.line([(cx, cy), (cx + h * 0.38, cy + h * 0.12)], c, s * 0.09)
    elif name == "cross":
        p.line([(cx - h * 0.55, cy - h * 0.55), (cx + h * 0.55, cy + h * 0.55)], c, s * 0.16)
        p.line([(cx - h * 0.55, cy + h * 0.55), (cx + h * 0.55, cy - h * 0.55)], c, s * 0.16)
    elif name == "ticket":
        p.rr((cx - h * 0.9, cy - h * 0.55, cx + h * 0.9, cy + h * 0.55), s * 0.08, fill=c)
        p.circ(cx - h * 0.9, cy, h * 0.2, fill=rgba(bg))
        p.circ(cx + h * 0.9, cy, h * 0.2, fill=rgba(bg))
        p.text(cx, cy + h * 0.02, "%", "black", s * 0.5, rgba(bg), anchor="mm")
    elif name == "car":
        p.rr((cx - h * 0.92, cy - h * 0.12, cx + h * 0.92, cy + h * 0.45), s * 0.1, fill=c)
        p.poly([(cx - h * 0.55, cy - h * 0.1), (cx - h * 0.35, cy - h * 0.55), (cx + h * 0.35, cy - h * 0.55),
                (cx + h * 0.6, cy - h * 0.1)], fill=c)
        p.poly([(cx - h * 0.38, cy - h * 0.14), (cx - h * 0.25, cy - h * 0.42), (cx - h * 0.02, cy - h * 0.42),
                (cx - h * 0.02, cy - h * 0.14)], fill=rgba(bg))
        p.poly([(cx + h * 0.06, cy - h * 0.14), (cx + h * 0.06, cy - h * 0.42), (cx + h * 0.28, cy - h * 0.42),
                (cx + h * 0.42, cy - h * 0.14)], fill=rgba(bg))
        for dx in (-0.5, 0.5):
            p.circ(cx + dx * h, cy + h * 0.48, h * 0.22, fill=c)
            p.circ(cx + dx * h, cy + h * 0.48, h * 0.09, fill=rgba(bg))
    elif name == "pin":
        p.circ(cx, cy - h * 0.25, h * 0.6, fill=c)
        p.poly([(cx - h * 0.5, cy - h * 0.02), (cx + h * 0.5, cy - h * 0.02), (cx, cy + h * 0.92)], fill=c)
        p.circ(cx, cy - h * 0.25, h * 0.24, fill=rgba(bg))
    elif name == "parking":
        p.rr((cx - h * 0.85, cy - h * 0.85, cx + h * 0.85, cy + h * 0.85), s * 0.18, fill=c)
        p.text(cx + h * 0.04, cy + h * 0.04, "P", "black", s * 0.95, rgba(bg), anchor="mm")
    elif name == "home":
        p.poly([(cx, cy - h * 0.85), (cx + h * 0.9, cy - h * 0.05), (cx - h * 0.9, cy - h * 0.05)], fill=c)
        p.rect((cx - h * 0.62, cy - h * 0.1, cx + h * 0.62, cy + h * 0.8), fill=c)
        p.rect((cx - h * 0.18, cy + h * 0.25, cx + h * 0.18, cy + h * 0.8), fill=rgba(bg))
    elif name == "shop":
        p.rect((cx - h * 0.8, cy - h * 0.1, cx + h * 0.8, cy + h * 0.8), fill=c)
        for k in range(4):
            x0 = cx - h * 0.9 + k * h * 0.45
            p.d.pieslice(p._b((x0, cy - h * 0.6, x0 + h * 0.45, cy - h * 0.05)), 0, 180, fill=c)
        p.rect((cx - h * 0.9, cy - h * 0.8, cx + h * 0.9, cy - h * 0.38), fill=c)
        p.rect((cx - h * 0.25, cy + h * 0.25, cx + h * 0.25, cy + h * 0.8), fill=rgba(bg))
    elif name == "hospital":
        p.rr((cx - h * 0.85, cy - h * 0.85, cx + h * 0.85, cy + h * 0.85), s * 0.14, fill=c)
        p.rect((cx - h * 0.16, cy - h * 0.55, cx + h * 0.16, cy + h * 0.55), fill=rgba(bg))
        p.rect((cx - h * 0.55, cy - h * 0.16, cx + h * 0.55, cy + h * 0.16), fill=rgba(bg))
    elif name == "train":
        p.rr((cx - h * 0.65, cy - h * 0.85, cx + h * 0.65, cy + h * 0.5), s * 0.16, fill=c)
        p.rr((cx - h * 0.45, cy - h * 0.62, cx + h * 0.45, cy - h * 0.12), s * 0.05, fill=rgba(bg))
        p.circ(cx - h * 0.35, cy + h * 0.2, h * 0.1, fill=rgba(bg))
        p.circ(cx + h * 0.35, cy + h * 0.2, h * 0.1, fill=rgba(bg))
        p.line([(cx - h * 0.4, cy + h * 0.6), (cx - h * 0.7, cy + h * 0.92)], c, s * 0.08)
        p.line([(cx + h * 0.4, cy + h * 0.6), (cx + h * 0.7, cy + h * 0.92)], c, s * 0.08)
    elif name == "play":
        p.poly([(cx - h * 0.4, cy - h * 0.62), (cx + h * 0.62, cy), (cx - h * 0.4, cy + h * 0.62)], fill=c)
    elif name == "globe":
        p.circ(cx, cy, h * 0.85, outline=c, width=s * 0.08)
        p.ell((cx - h * 0.38, cy - h * 0.85, cx + h * 0.38, cy + h * 0.85), outline=c, width=s * 0.07)
        p.line([(cx - h * 0.85, cy), (cx + h * 0.85, cy)], c, s * 0.07)


def tile(p, cx, cy, size, col, name, r=None, k=0.86):
    """Tinted rounded square with an icon."""
    r = size * 0.27 if r is None else r
    bgc = tint(col, k)
    p.rr((cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2), r, fill=rgba(bgc))
    icon(p, name, cx, cy, size * 0.52, col, bg=bgc)


def cursor_sprite():
    def cb(p):
        pts = [(4, 4), (4, 46), (15, 35), (23, 54), (31, 50), (23, 32), (39, 32)]
        p.poly(pts, fill=rgba(WHITE))
        inner = [(8, 12), (8, 38), (16, 30), (24, 47), (27, 45), (19, 28), (31, 28)]
        p.poly(inner, fill=rgba(DARK))
    return canvas(46, 60, cb, ss=4)
