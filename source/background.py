"""Cream paper background, blue torn-paper corners and small decorations (built once, moved with parallax)."""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from gfx import H, W, rgba

M = 48  # extra margin for parallax movement


def _noise1d(n, ctrl, rng, amp):
    """Smooth random curve with n samples built from `ctrl` control points + fine jitter."""
    c = rng.normal(0, 1, ctrl + 3)
    xs = np.linspace(0, ctrl, n)
    i = np.floor(xs).astype(int)
    f = xs - i
    f = f * f * (3 - 2 * f)
    smooth = c[i] * (1 - f) + c[i + 1] * f
    return smooth * amp


def torn_path(p0, p1, rng, amp=16, jitter=3.2, n=320):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    big = _noise1d(n, 7, rng, amp)
    mid = _noise1d(n, 40, rng, amp * 0.25)
    fine = rng.uniform(-jitter, jitter, n)
    pts = []
    for k in range(n):
        t = k / (n - 1)
        d = big[k] + mid[k] + fine[k]
        pts.append((x0 + (x1 - x0) * t + nx * d, y0 + (y1 - y0) * t + ny * d))
    return pts


def torn_poly(corners, seed, amp=14, closed_extra=()):
    """Polygon whose listed edges are torn. corners: list of points; all edges are torn."""
    rng = np.random.default_rng(seed)
    pts = []
    for a, b in zip(corners, corners[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        pts += torn_path(a, b, rng, amp=amp, n=max(40, int(L / 3)))
    return pts + list(closed_extra)


def _grad(w, h, c1, c2, angle=35):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = math.radians(angle)
    t = (xx * math.cos(a) + yy * math.sin(a))
    t = (t - t.min()) / (t.max() - t.min())
    c1, c2 = np.array(c1, np.float32), np.array(c2, np.float32)
    img = c1 * (1 - t[..., None]) + c2 * t[..., None]
    return Image.fromarray(img.astype(np.uint8), "RGB")


def _paper_piece(layer, pts, c1, c2, ss, rim=9, seed=0, angle=35):
    """Draw a torn paper piece: white fibrous rim + shadow + gradient fill."""
    Wl, Hl = layer.size
    sp = [((x + M) * ss, (y + M) * ss) for x, y in pts]
    # rim = the polygon grown a bit (white torn fibre edge)
    rim_mask = Image.new("L", (Wl, Hl), 0)
    ImageDraw.Draw(rim_mask).polygon(sp, fill=255)
    rim_mask = rim_mask.filter(ImageFilter.MaxFilter(int(rim * ss) | 1))
    rng = np.random.default_rng(seed)
    # fibrous: knock random speckles off the rim edge
    edge_noise = Image.fromarray((rng.random((Hl // 4, Wl // 4)) * 255).astype(np.uint8)).resize((Wl, Hl), Image.BILINEAR)
    rim_np = np.asarray(rim_mask, np.float32) / 255
    body = Image.new("L", (Wl, Hl), 0)
    ImageDraw.Draw(body).polygon(sp, fill=255)
    body_np = np.asarray(body, np.float32) / 255
    fib = np.clip((np.asarray(edge_noise, np.float32) / 255 - 0.18) * 3, 0, 1)
    rim_np = np.maximum(body_np, rim_np * fib)
    # shadow under the paper
    sh = Image.fromarray((rim_np * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9 * ss))
    sh_np = np.roll(np.asarray(sh, np.float32) / 255, int(6 * ss), axis=0) * 0.28
    _over(layer, (40, 60, 100), sh_np)
    _over(layer, (252, 252, 250), rim_np)
    fill = _grad(Wl, Hl, c1, c2, angle)
    _over_img(layer, fill, body_np)


def _over(layer, col, alpha):
    _over_img(layer, np.broadcast_to(np.array(col, np.float32), alpha.shape + (3,)), alpha)


def _over_img(layer, img, alpha):
    """Straight-alpha 'over' of a colour image with coverage `alpha` onto the layer (in place)."""
    arr = np.asarray(layer, np.float32)
    a = alpha[..., None]
    al = arr[..., 3:4] / 255
    out_a = a + al * (1 - a)
    rgb = (np.asarray(img, np.float32) * a + arr[..., :3] * al * (1 - a)) / np.maximum(out_a, 1e-6)
    layer.paste(Image.fromarray(np.concatenate([rgb, out_a * 255], axis=2).clip(0, 255).astype(np.uint8), "RGBA"))


def build_base():
    rng = np.random.default_rng(11)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.empty((H, W, 3), np.float32)
    base[:] = (241, 234, 221)
    for cx, cy, r, col, a in [(260, 760, 720, (226, 234, 247), 0.55), (840, 1260, 620, (249, 245, 236), 0.7),
                              (900, 360, 520, (231, 237, 248), 0.45), (200, 1650, 500, (236, 240, 248), 0.5)]:
        m = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * (r / 1.7) ** 2))) * a
        base = base * (1 - m[..., None]) + np.array(col, np.float32) * m[..., None]
    lf = Image.fromarray(((rng.normal(0, 1, (H // 6, W // 6)) * 40 + 128).clip(0, 255)).astype(np.uint8))
    lf = np.asarray(lf.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3)), np.float32) - 128
    base += lf[..., None] * 0.055
    base += rng.normal(0, 3.0, (H, W, 1))
    # faint grid
    g = np.zeros((H, W), np.float32)
    g[:, ::54] = 1
    g[::54, :] = 1
    base -= g[..., None] * 4.5
    return Image.fromarray(base.clip(0, 255).astype(np.uint8), "RGB").convert("RGBA")


def build_decor():
    ss = 2
    img = Image.new("RGBA", ((W + 2 * M) * ss, (H + 2 * M) * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    dot = (110, 135, 185, 150)
    for (x0, y0, cols, rows) in [(690, 120, 6, 4), (52, 600, 5, 5), (880, 690, 5, 4), (70, 1470, 4, 5),
                                 (830, 1360, 6, 3), (430, 1580, 5, 3)]:
        for i in range(cols):
            for j in range(rows):
                x, y = (x0 + i * 19 + M) * ss, (y0 + j * 19 + M) * ss
                d.ellipse([x - 3.2 * ss, y - 3.2 * ss, x + 3.2 * ss, y + 3.2 * ss], fill=dot)
    mark = (95, 110, 140, 150)
    for (x, y, kind) in [(300, 150, "+"), (150, 1280, "x"), (980, 610, "+"), (650, 1500, "+"), (940, 1170, "x"),
                         (120, 880, "+"), (560, 660, "x")]:
        x, y = (x + M) * ss, (y + M) * ss
        r = 11 * ss
        if kind == "+":
            d.line([x - r, y, x + r, y], fill=mark, width=3 * ss)
            d.line([x, y - r, x, y + r], fill=mark, width=3 * ss)
        else:
            d.line([x - r * .75, y - r * .75, x + r * .75, y + r * .75], fill=mark, width=3 * ss)
            d.line([x - r * .75, y + r * .75, x + r * .75, y - r * .75], fill=mark, width=3 * ss)
    # dashed arcs
    dash = (120, 140, 180, 120)
    for (cx, cy, r, a0, a1) in [(1010, 330, 280, 95, 235), (-60, 1180, 420, -70, 60)]:
        a = a0
        while a < a1:
            p0 = (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            p1 = (cx + r * math.cos(math.radians(a + 3)), cy + r * math.sin(math.radians(a + 3)))
            d.line([((p0[0] + M) * ss, (p0[1] + M) * ss), ((p1[0] + M) * ss, (p1[1] + M) * ss)], fill=dash, width=3 * ss)
            a += 6
    return img.resize((W + 2 * M, H + 2 * M), Image.LANCZOS)


def build_torn():
    ss = 1
    layer = Image.new("RGBA", ((W + 2 * M) * ss, (H + 2 * M) * ss), (0, 0, 0, 0))
    deep1, deep2 = (24, 74, 168), (40, 104, 206)
    light1, light2 = (176, 204, 242), (138, 178, 234)
    # top-left corner
    tl = torn_poly([(760, -M), (-M, 470)], seed=3, amp=18) + [(-M, -M)]
    _paper_piece(layer, tl, deep1, deep2, ss, seed=31, angle=40)
    tl2 = torn_poly([(470, -M), (-M, 300)], seed=5, amp=14) + [(-M, -M)]
    _paper_piece(layer, tl2, (60, 126, 222), (24, 70, 160), ss, rim=7, seed=32, angle=210)
    # bottom-right big light piece + deep piece
    br = torn_poly([(W + M, 1300), (300, H + M)], seed=7, amp=20) + [(W + M, H + M)]
    _paper_piece(layer, br, light1, light2, ss, seed=33, angle=30)
    br2 = torn_poly([(W + M, 1590), (690, H + M)], seed=9, amp=16) + [(W + M, H + M)]
    _paper_piece(layer, br2, deep2, deep1, ss, seed=34, angle=30)
    # right middle patch
    rm = torn_poly([(W + M, 760), (1012, 800), (996, 940), (1030, 1070), (W + M, 1110)], seed=13, amp=4)
    _paper_piece(layer, rm, deep2, deep1, ss, rim=7, seed=35)
    # left middle patch
    lm = torn_poly([(-M, 1190), (36, 1214), (54, 1330), (22, 1430), (-M, 1452)], seed=17, amp=4)
    _paper_piece(layer, lm, deep1, deep2, ss, rim=7, seed=36)
    return layer


def shifted(layer, dx, dy):
    """Return a WxH view of an oversized layer shifted by a sub-pixel (dx, dy)."""
    return layer.transform((W, H), Image.AFFINE, (1, 0, M - dx, 0, 1, M - dy), resample=Image.BILINEAR)


class Background:
    def __init__(self):
        self.base = build_base()
        self.decor = build_decor()
        self.torn = build_torn()

    def frame(self, t):
        f = self.base.copy()
        f.alpha_composite(shifted(self.decor, 7 * math.sin(t * 2 * math.pi / 10), 9 * math.sin(t * 2 * math.pi / 13 + 1)))
        f.alpha_composite(shifted(self.torn, 6 * math.sin(t * 2 * math.pi / 9 + 0.5), 8 * math.sin(t * 2 * math.pi / 11)))
        return f


# ====================================================================== DARK SERIES BACKGROUND
class ImageBackground:
    """Animated background from a still image (e.g. a Gemini-made plate in assets/backgrounds/).
    Adds: very slow zoom + drift, light pulses running along the green circuit lines, twinkling particles."""
    ZOOM = 1.06  # extra size so the drift never shows an edge

    def __init__(self, path, seed=1, effects=True):
        self.effects = effects  # circuit pulses + glowing particles (dark theme only)
        src = Image.open(path).convert("RGB")
        bw = int(W * self.ZOOM)
        bh = int(round(src.height * bw / src.width))
        if bh < H * self.ZOOM:
            bh = int(H * self.ZOOM)
            bw = int(round(src.width * bh / src.height))
        self.base = np.asarray(src.resize((bw, bh), Image.LANCZOS), np.uint8).copy()
        self.bw, self.bh = bw, bh
        a = self.base.astype(np.int16)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        line = (g > 150) & (g - r > 60) & (g - b > 25)          # bright green circuit traces
        ys, xs = np.nonzero(line)
        self.ly, self.lx = ys, xs
        ang = (np.arctan2(ys - bh / 2, (xs - bw / 2) * (bh / bw)) / (2 * np.pi)) % 1.0
        self.lang = ang.astype(np.float32)
        rng = np.random.default_rng(seed)
        n = 70
        self.px = rng.uniform(0, W, n)
        self.py = rng.uniform(0, H, n)
        self.pv = rng.uniform(8, 26, n)          # rise speed px/s
        self.pp = rng.uniform(0, 2 * np.pi, n)   # twinkle phase
        self.pk = rng.integers(0, 3, n)          # colour index
        self.ps = rng.uniform(0.5, 1.15, n)
        self.dots = [self._dot(c) for c in [(0, 200, 255), (190, 120, 255), (90, 255, 120)]]

    @staticmethod
    def _dot(col):
        s = 40
        im = Image.new("L", (s, s), 0)
        d = ImageDraw.Draw(im)
        d.ellipse([s / 2 - 10, s / 2 - 10, s / 2 + 10, s / 2 + 10], fill=70)
        im = im.filter(ImageFilter.GaussianBlur(5))
        ImageDraw.Draw(im).ellipse([s / 2 - 2.2, s / 2 - 2.2, s / 2 + 2.2, s / 2 + 2.2], fill=255)
        out = Image.new("RGBA", (s, s), col + (0,))
        out.putalpha(im)
        return out

    def frame(self, t):
        from gfx import put  # local import: gfx imports nothing from here
        arr = self.base.copy()
        # two light pulses travelling around the circuit frame
        if self.effects and len(self.lang):
            inten = np.zeros_like(self.lang)
            for ph in (t / 7.0, t / 7.0 + 0.5):
                dd = np.abs(((self.lang - ph) + 0.5) % 1.0 - 0.5)
                inten += np.exp(-(dd / 0.035) ** 2)
            add = (inten[:, None] * np.array([150, 255, 190], np.float32) * 0.85)
            px = arr[self.ly, self.lx].astype(np.float32) + add
            arr[self.ly, self.lx] = np.clip(px, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr, "RGB")
        z = 1.0 + 0.03 * (0.5 - 0.5 * math.cos(math.pi * min(t / 60.0, 1.0)))
        dx = 14 * math.sin(t * 2 * math.pi / 17)
        dy = 18 * math.sin(t * 2 * math.pi / 23 + 0.7)
        cx, cy = self.bw / 2 + dx, self.bh / 2 + dy
        f = img.transform((W, H), Image.AFFINE, (1 / z, 0, cx - W / (2 * z), 0, 1 / z, cy - H / (2 * z)),
                          resample=Image.BILINEAR).convert("RGBA")
        # floating, twinkling particles
        for i in range(len(self.px) if self.effects else 0):
            y = (self.py[i] - self.pv[i] * t) % (H + 40) - 20
            x = self.px[i] + 10 * math.sin(t * 0.6 + self.pp[i])
            tw = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * 2.2 + self.pp[i]))
            put(f, self.dots[self.pk[i]], x, y, self.ps[i], tw * 0.9)
        return f
