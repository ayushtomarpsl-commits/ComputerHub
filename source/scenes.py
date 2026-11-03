"""All scene graphics. Each scene draws itself for time t (seconds) on the frame.
Timings follow the narration word timestamps in captions_data.py."""
import math
import os
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter

from gfx import (BLUE, BORDER, CYAN, DARK, DARK_YEL, GREEN, INK, INK2, LGREEN, LINE, LOGO_GLOW, LOGO_GLOW_A, MUTED,
                 ORANGE, PANEL, PAPER, PURPLE, SKEL, T_CYAN, T_GREEN, T_YELLOW,
                 SM, WHITE, YELLOW, Pen, canvas,
                 card, clamp, cursor_sprite, font, icon, in_cubic, lerp, out_back, out_cubic, pop, prog, put,
                 rgba, smooth, text_w, tile, tint, trans)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(ROOT, "assets", "logo_transparent.png")
CX = 540


# ------------------------------------------------------------------ shared sprites
@lru_cache(None)
def logo(size):
    return Image.open(LOGO).convert("RGBA").resize((size, size), Image.LANCZOS)


@lru_cache(None)
def logo_shadow(size):
    pad = 80
    im = Image.new("L", (size + 2 * pad, size + 2 * pad), 0)
    ImageDraw.Draw(im).ellipse([pad - 6, pad + 4, pad + size + 6, pad + size + 16], fill=LOGO_GLOW_A)
    im = im.filter(ImageFilter.GaussianBlur(34))
    out = Image.new("RGBA", im.size, LOGO_GLOW + (0,))
    out.putalpha(im)
    return out


@lru_cache(None)
def ring(r, col, width=6):
    return canvas(2 * r + 20, 2 * r + 20, lambda p: p.circ(r + 10, r + 10, r, outline=rgba(col), width=width))


@lru_cache(None)
def cursor():
    return cursor_sprite()


@lru_cache(None)
def pill(text, bg, fg, kind="mono", size=22, spacing=3, padx=26, h=56, icon_name=None, icon_col=None, border=None):
    tw = text_w(text, kind, size, spacing)
    iw = (h * 0.5 + 12) if icon_name else 0
    w = int(tw + iw + 2 * padx)

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(bg), outline=rgba(border) if border else None, width=2)
        x = padx
        if icon_name:
            icon(p, icon_name, x + h * 0.25, h / 2, h * 0.5, icon_col or fg, bg=bg)
            x += iw
        p.text(x, h / 2, text, kind, size, rgba(fg), anchor="lm", spacing=spacing)
    return canvas(w, h, cb)


@lru_cache(None)
def handle_pill(size=36):
    t1, t2 = "@", "computer__hub"
    w = int(text_w(t1, "bold", size) + text_w(t2, "bold", size) + 64)
    h = int(size * 1.9)

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(PAPER, 235), outline=rgba(CYAN), width=2)
        x = 32
        p.text(x, h / 2, t1, "bold", size, rgba(BLUE), anchor="lm")
        p.text(x + text_w(t1, "bold", size), h / 2, t2, "bold", size, rgba(INK), anchor="lm")
    return with_shadow_pill(canvas(w, h, cb), h)


def with_shadow_pill(img, h):
    from gfx import _shadow
    out = _shadow(img.width, img.height, int(h / 2), 0.8).copy()
    out.alpha_composite(img, (SM, SM))
    return out


def header_label(p, w, y, text, col=BLUE, size=20, spacing=4):
    p.text(w / 2, y, text, "mono", size, rgba(col), anchor="mm", spacing=spacing)


# ------------------------------------------------------------------ S1a: logo intro (0 - 1.75)
def s_logo_intro(f, t):
    t0, t1 = 0.0, 1.5
    s, a, dy = trans(t, t0, t1, din=0.6, dout=0.3, s0=0.5)
    cy = 1000 + dy
    for t_r in (0.12, 0.7):
        pr = prog(t, t_r, 1.1)
        if 0 < pr < 1:
            put(f, ring(200, CYAN, 5), CX, cy, s=0.95 + 0.55 * out_cubic(pr), a=(1 - pr) * 0.55 * a)
    put(f, logo_shadow(420), CX, cy, s, a * 0.9)
    put(f, logo(420), CX, cy, s, a)
    ps, pa = pop(t, 0.42, 0.35)
    put(f, handle_pill(), CX, 1300 + dy, ps * s, pa * a)


# ------------------------------------------------------------------ S1b: tech industry card (1.55 - 4.45)
TECH = [("code", GREEN, "Code"), ("cloud", CYAN, "Cloud"), ("spark", PURPLE, "AI"),
        ("db", BLUE, "Data"), ("chip", CYAN, "Hardware"), ("gear", DARK_YEL, "DevOps")]


@lru_cache(None)
def tech_card():
    def cb(p):
        tile(p, 78, 76, 80, CYAN, "laptop")
        p.text(140, 60, "Tech Industry", "bold", 42, rgba(INK), anchor="lm")
        p.text(141, 102, "SOFTWARE · CLOUD · AI · DATA", "mono", 18, rgba(MUTED), anchor="lm", spacing=2)
        p.line([(36, 146), (764, 146)], rgba(LINE), 2, caps=False)
    return card(800, 560, 36, cb)


@lru_cache(None)
def tech_tile(i):
    name, col, label = TECH[i]

    def cb(p):
        p.rr((2, 2, 208, 168), 28, fill=rgba(tint(col, 0.9)), outline=rgba(tint(col, 0.75)), width=2)
        icon(p, name, 105, 66, 62, col, bg=tint(col, 0.9))
        p.text(105, 136, label, "semi", 26, rgba(INK2), anchor="mm")
    return canvas(210, 170, cb)


def s_tech(f, t):
    t0, t1 = 1.52, 4.45
    s, a, dy = trans(t, t0, t1)
    cy = 1040 + dy
    put(f, tech_card(), CX, cy, s, a)
    for i in range(6):
        col, row = i % 3, i // 3
        tx = CX + (col - 1) * 238 * s
        ty = cy + (-280 + 270 + row * 190) * s
        ps, pa = pop(t, 1.84 + i * 0.11, 0.34)
        bob = 3 * math.sin(t * 2.4 + i)
        put(f, tech_tile(i), tx, ty + bob, ps * s, pa * a)


# ------------------------------------------------------------------ S2: AI code editor (4.38 - 9.75)
CODE = [
    [("def ", PURPLE), ("build_my_app", BLUE), ("():", INK)],
    [("    idea = ", INK), ('"side project"', GREEN)],
    [("    ai = ", INK), ("Assistant", BLUE), ("()", INK)],
    [("    code = ai.", INK), ("write", BLUE), ("(idea)", INK)],
    [("    test", BLUE), ("(code)", INK)],
    [("    return ", PURPLE), ("ship", BLUE), ("(code)", INK)],
    [("# AI is changing how we code", MUTED)],
]
CODE_W, CODE_H = 840, 600


@lru_cache(None)
def editor_card():
    def cb(p):
        p.rr((0, 0, CODE_W - 1, 74), 36, fill=rgba(PANEL))
        p.rect((0, 40, CODE_W - 1, 74), fill=rgba(PANEL))
        p.line([(0, 74), (CODE_W, 74)], rgba(LINE), 2, caps=False)
        for k, c in enumerate([(255, 96, 92), (255, 190, 50), (40, 200, 70)]):
            p.circ(40 + k * 28, 37, 9, fill=rgba(c))
        p.rr((140, 18, 300, 58), 12, fill=rgba(PAPER), outline=rgba(LINE), width=2)
        p.text(220, 38, "main.py", "monor", 20, rgba(INK2), anchor="mm")
        for i in range(len(CODE)):
            p.text(52, 128 + i * 60, str(i + 1), "monor", 22, rgba(MUTED), anchor="rm")
    return card(CODE_W, CODE_H, 36, cb)


def _code_chars(t):
    """How many characters of each line are visible at time t."""
    out = []
    human = [(4.55, 0.42), (4.95, 0.45)]  # line start time, duration (human typing)
    for i, line in enumerate(CODE):
        n = sum(len(s) for s, _ in line)
        if i < 2:
            st, du = human[i]
            out.append(int(n * prog(t, st, du)))
        else:
            st = 5.2 + (i - 2) * 0.16  # AI fills fast
            out.append(n if t >= st else 0)
    return out


def _ai_ghost(t, i):
    if i < 2:
        return 0.0
    st = 5.2 + (i - 2) * 0.16
    return 1 - prog(t, st + 0.2, 0.35)


def s_code(f, t):
    t0, t1 = 4.38, 9.75
    s, a, dy = trans(t, t0, t1)
    cy = 960 + dy
    base = editor_card().copy()
    d = ImageDraw.Draw(base)
    fnt = font("monor", 27)
    chars = _code_chars(t)
    last = None
    for i, line in enumerate(CODE):
        x = SM + 80
        y = SM + 128 + i * 60
        left = chars[i]
        g = _ai_ghost(t, i)
        for seg, col in line:
            if left <= 0:
                break
            part = seg[:left]
            c = tuple(int(lerp(cc, pc, g)) for cc, pc in zip(col, tint(PURPLE, 0.45)))
            d.text((x, y), part, font=fnt, fill=c, anchor="lm")
            x += fnt.getlength(part)
            left -= len(part)
        if chars[i] > 0:
            last = (x, y)
    if last and (t < 5.2 or t > 6.3) and int(t * 2.5) % 2 == 0:
        d.rectangle([last[0] + 3, last[1] - 17, last[0] + 6, last[1] + 17], fill=rgba(BLUE))
    put(f, base, CX, cy, s, a)
    # AI assist chip
    ps, pa = pop(t, 5.12, 0.36)
    put(f, pill("AI ASSIST", tint(PURPLE, 0.86), PURPLE, size=20, h=50, icon_name="spark", icon_col=PURPLE),
        CX + (CODE_W / 2 - 130) * s, cy - (CODE_H / 2 - 37) * s, ps * s, pa * a)
    # workflow strip: Plan -> Code -> Ship
    steps = [("PLAN", 7.56), ("CODE", 7.8), ("SHIP", 8.04)]
    for k, (lab, ts) in enumerate(steps):
        x = CX + (k - 1) * 270
        ps, pa = pop(t, ts, 0.32)
        y = 1350 + dy
        put(f, pill(lab, PAPER, INK, size=24, h=64, border=BORDER), x, y, ps * s, pa * a)
        on = prog(t, 8.74 + k * 0.14, 0.2)
        if on > 0:
            put(f, pill(lab, BLUE, WHITE, size=24, h=64), x, y, ps * s * (1 + 0.06 * math.sin(on * math.pi)), on * a)
        if k < 2:
            pa2 = prog(t, ts + 0.12, 0.2)
            if pa2 > 0:
                put(f, arrow_sprite(), x + 135, y, s, pa2 * a, sx=pa2)


@lru_cache(None)
def arrow_sprite():
    def cb(p):
        p.line([(4, 18), (50, 18)], rgba(BLUE), 5)
        p.poly([(44, 8), (60, 18), (44, 28)], fill=rgba(BLUE))
    return canvas(64, 36, cb)


# ------------------------------------------------------------------ S3: engineer + one income (9.85 - 17.4)
@lru_cache(None)
def profile_card():
    def cb(p):
        p.circ(118, 125, 78, fill=rgba(CYAN))
        p.text(118, 128, "</>", "mono", 54, rgba(WHITE), anchor="mm")
        p.text(232, 92, "Software Engineer", "bold", 46, rgba(INK), anchor="lm")
        p.text(233, 146, "Full-time job · Tech", "reg", 28, rgba(MUTED), anchor="lm")
    return card(800, 250, 36, cb)


@lru_cache(None)
def income_card():
    def cb(p):
        p.text(52, 50, "INCOME SOURCES", "mono", 20, rgba(BLUE), anchor="lm", spacing=4)
        p.text(250, 128, "Only one job", "bold", 38, rgba(INK), anchor="lm")
        p.rr((250, 190, 748, 222), 16, fill=rgba(SKEL))
    return card(800, 320, 36, cb)


@lru_cache(None)
def big_num(txt, col, size=170):
    w = int(text_w(txt, "black", size) + 30)
    return canvas(w, int(size * 1.25), lambda p: p.text(w / 2, size * 0.62, txt, "black", size, rgba(col), anchor="mm"))


@lru_cache(None)
def bar_fill(w, col):
    w = max(32, int(w))
    return canvas(w, 32, lambda p: p.rr((0, 0, w - 1, 31), 16, fill=rgba(col)))


def s_engineer(f, t):
    t0, t1 = 9.85, 17.4
    s, a, dy = trans(t, t0, t1)
    cy1 = 830 + dy
    put(f, profile_card(), CX, cy1, s, a)
    risk = prog(t, 16.26, 0.2)
    put(f, pill("EMPLOYED", tint(GREEN, 0.85), T_GREEN, size=18, h=44), CX + (-400 + 232 + 80) * s,
        cy1 + 58 * s, s, a * (1 - risk))
    if risk > 0:
        ps, _ = pop(t, 16.26, 0.3)
        put(f, pill("AT RISK", tint(YELLOW, 0.78), T_YELLOW, size=18, h=44), CX + (-400 + 232 + 74) * s,
            cy1 + 58 * s, ps * s, a * risk)
    # income card
    s2, a2, dy2 = trans(t, 13.6, t1)
    cy2 = 1150 + dy2
    put(f, income_card(), CX, cy2, s2, a2)
    ps, pa = pop(t, 14.18, 0.4, s0=0.3)
    put(f, big_num("1", BLUE), CX + (-400 + 130) * s2, cy2 + 20 * s2, ps * s2, pa * a2)
    fill = out_cubic(prog(t, 14.45, 0.8))
    col = tuple(int(lerp(c1, c2, risk)) for c1, c2 in zip(BLUE, ORANGE))
    if fill > 0:
        bw = 498 * fill
        put(f, bar_fill(bw, col), CX + (-400 + 250 + bw / 2) * s2, cy2 + (-160 + 206) * s2, s2, a2)
    lab = "SALARY  100%"
    put(f, pill(lab, PAPER, MUTED, size=18, h=40, padx=0), CX + (-400 + 250 + text_w(lab, "mono", 18, 3) / 2) * s2,
        cy2 + (-160 + 262) * s2, s2, a2 * prog(t, 14.9, 0.3))
    # warning badge
    if t >= 16.2:
        ps, pa = pop(t, 16.26, 0.36, s0=0.4)
        shake = 7 * math.sin((t - 16.26) * 40) * (1 - prog(t, 16.26, 0.5))
        put(f, pill("NOT SAFE", YELLOW, DARK, size=24, h=66, icon_name="warn", icon_col=DARK),
            CX + 240 * s2 + shake, cy2 - 150 * s2, ps * s2, pa * a2)


# ------------------------------------------------------------------ S4: news + Plan B (18.0 - 25.05)
NEWS = [("BREAKING", "Tech Layoffs", ORANGE, 18.14), ("NEWS", "Job Loss", BLUE, 19.0),
        ("TRENDING", "Tech News Today", PURPLE, 19.74)]


@lru_cache(None)
def news_card(i):
    tag, title, col, _ = NEWS[i]

    def cb(p):
        tile(p, 82, 82, 96, col, "news")
        tw = text_w(tag, "mono", 17, 3) + 30
        p.rr((152, 26, 152 + tw, 60), 17, fill=rgba(tint(col, 0.85)))
        p.text(167, 43, tag, "mono", 17, rgba(col), anchor="lm", spacing=3)
        p.text(152, 96, title, "bold", 36, rgba(INK), anchor="lm")
        p.rr((152, 128, 600, 142), 7, fill=rgba(SKEL))
        p.rr((610, 128, 720, 142), 7, fill=rgba(SKEL))
    return card(780, 166, 30, cb)


@lru_cache(None)
def thinking_pill():
    return pill("THINKING", PAPER, INK2, size=20, h=56, padx=96, border=BORDER)


def s_news(f, t):
    t1 = 22.45
    for i, (_, _, _, ts) in enumerate(NEWS):
        p = prog(t, ts - 0.05, 0.5)
        if p <= 0:
            continue
        _, a, dy = trans(t, ts - 0.05, t1)
        x = CX + 560 * (1 - out_cubic(p))
        y = 790 + i * 195 + dy * 0.3
        dim = 1 - 0.25 * prog(t, 20.9, 0.4)
        put(f, news_card(i), x, y, 1.0, a * clamp(p * 2) * dim)
    ps, pa = pop(t, 20.9, 0.34)
    if pa > 0:
        _, a, _ = trans(t, 20.9, t1)
        y = 1385
        put(f, thinking_pill(), CX, y, ps, pa * a)
        for k in range(3):
            bounce = abs(math.sin((t - 20.9) * 6 - k * 0.6)) * 9
            put(f, dot_sprite(), CX - 128 + k * 22, y - bounce * 0.6 + 2, ps, pa * a)


@lru_cache(None)
def dot_sprite():
    return canvas(16, 16, lambda p: p.circ(8, 8, 6, fill=rgba(BLUE)))


@lru_cache(None)
def planb_card():
    def cb(p):
        header_label(p, 780, 64, "THE QUESTION", BLUE, 22, 6)
    return card(780, 600, 38, cb)


@lru_cache(None)
def planb_title():
    size = 150
    w1 = text_w("Plan ", "black", size)
    w2 = text_w("B?", "black", size)
    w = int(w1 + w2 + 20)

    def cb(p):
        p.text(10, size * 0.62, "Plan ", "black", size, rgba(INK), anchor="lm")
        p.text(10 + w1, size * 0.62, "B?", "black", size, rgba(BLUE), anchor="lm")
    return canvas(w, int(size * 1.25), cb)


@lru_cache(None)
def plan_row(which):
    w, h = 660, 104
    if which == "A":
        name, sub, col, ic, tag, tcol = "Plan A", "One job", DARK_YEL, "briefcase", "RISKY", T_YELLOW
    else:
        name, sub, col, ic, tag, tcol = "Plan B", "AI + side income", PURPLE, "spark", "BUILDING", PURPLE

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), 26, fill=rgba(PANEL), outline=rgba(LINE), width=2)
        tile(p, 56, h / 2, 70, col, ic)
        p.text(112, 38, name, "bold", 32, rgba(INK), anchor="lm")
        p.text(112, 74, sub, "reg", 24, rgba(MUTED), anchor="lm")
        tw = text_w(tag, "mono", 17, 3) + 30
        p.rr((w - 30 - tw, h / 2 - 19, w - 30, h / 2 + 19), 19, fill=rgba(tint(col, 0.82)))
        p.text(w - 30 - tw / 2, h / 2, tag, "mono", 17, rgba(tcol), anchor="mm", spacing=3)
    return canvas(w, h, cb)


def s_planb(f, t):
    t0, t1 = 22.42, 25.05
    s, a, dy = trans(t, t0, t1)
    cy = 1030 + dy
    put(f, planb_card(), CX, cy, s, a)
    ps, pa = pop(t, 23.28, 0.45, s0=0.3)
    pulse = 1 + 0.05 * math.sin(prog(t, 24.3, 0.4) * math.pi)
    put(f, planb_title(), CX, cy - 135 * s, ps * s * pulse, pa * a)
    for k, (wh, ts) in enumerate([("A", 22.6), ("B", 24.18)]):
        ps, pa = pop(t, ts, 0.36)
        put(f, plan_row(wh), CX, cy + (70 + k * 124) * s, ps * s, pa * a)


# ------------------------------------------------------------------ S5: you + AI (25.0 - 30.75)
@lru_cache(None)
def shift_card():
    def cb(p):
        header_label(p, 820, 60, "THE SHIFT", BLUE, 22, 6)
        p.text(60, 480, "Project started", "semi", 28, rgba(INK2), anchor="lm")
        p.rr((60, 520, 760, 548), 14, fill=rgba(SKEL))
    return card(820, 620, 38, cb)


@lru_cache(None)
def node(kind):
    r = 92
    col = CYAN if kind == "you" else PURPLE
    lab = "YOU" if kind == "you" else "AI"

    def cb(p):
        p.circ(r + 10, r + 10, r + 8, fill=rgba(tint(col, 0.8)))
        p.circ(r + 10, r + 10, r, fill=rgba(col))
        icon(p, "user" if kind == "you" else "spark", r + 10, r + 6 if kind == "you" else r + 10, r * 1.0, WHITE, bg=col)
        p.text(r + 10, 2 * r + 60, lab, "bold", 32, rgba(INK), anchor="mm")
    return canvas(2 * r + 20, 2 * r + 84, cb)


@lru_cache(None)
def vs_badge():
    return canvas(120, 120, lambda p: (p.circ(60, 60, 52, fill=rgba(YELLOW)),
                                       p.text(60, 62, "VS", "black", 44, rgba(DARK), anchor="mm")))


@lru_cache(None)
def plus_badge():
    return canvas(110, 110, lambda p: (p.circ(55, 55, 46, fill=rgba(GREEN)), icon(p, "plus", 55, 55, 56, WHITE)))


def s_shift(f, t):
    t0, t1 = 25.0, 30.75
    s, a, dy = trans(t, t0, t1)
    cy = 1020 + dy

    def at(rx, ry):
        return CX + (rx - 410) * s, cy + (ry - 310) * s
    put(f, shift_card(), CX, cy, s, a)
    pull = out_cubic(prog(t, 28.94, 0.4)) * 18
    for kind, rx, ts in [("you", 200 + pull, 25.52), ("ai", 620 - pull, 26.18)]:
        ps, pa = pop(t, ts, 0.38)
        x, y = at(rx, 250)
        put(f, node(kind), x, y + 30 * s, ps * s, pa * a)
    # VS + strike
    ps, pa = pop(t, 26.4, 0.3)
    gone = prog(t, 27.35, 0.3)
    x, y = at(410, 248)
    if pa > 0 and gone < 1:
        put(f, vs_badge(), x, y, ps * s, pa * a * (1 - gone))
        st = prog(t, 26.8, 0.22)
        if st > 0:
            put(f, strike_sprite(), x - 80 * s * (1 - st), y, s, a * (1 - gone), sx=st)
    # connection line + plus
    cl = out_cubic(prog(t, 27.68, 0.45))
    if cl > 0:
        x0, y0 = at(300 + pull, 248)
        x1, _ = at(520 - pull, 248)
        ln = (x1 - x0) * cl
        put(f, conn_sprite(), x0 + ln / 2, y0, s, a, sx=max(0.02, ln / (220 * s)))
    ps, pa = pop(t, 28.24, 0.38, s0=0.3)
    x, y = at(410, 248)
    put(f, plus_badge(), x, y, ps * s, pa * a)
    # progress bar
    fill = smooth(prog(t, 29.35, 1.0))
    if fill > 0:
        bw = 700 * fill
        x, y = at(60 + bw / 2, 534)
        put(f, bar_fill(bw * 1, GREEN), x, y, s, a, sx=1)
    pct = f"{int(round(fill * 100))}%"
    x, y = at(760, 480)
    if fill > 0:
        put(f, pct_sprite(pct), x - 40 * s, y, s, a)
    ps, pa = pop(t, 30.38, 0.3)
    x, y = at(700, 480)
    put(f, check_sprite(), x - 110 * s, y, ps * s, pa * a)


@lru_cache(None)
def strike_sprite():
    return canvas(160, 20, lambda p: p.line([(8, 10), (152, 10)], rgba((215, 60, 60)), 9))


@lru_cache(None)
def conn_sprite():
    def cb(p):
        for k in range(0, 220, 22):
            p.line([(k + 2, 10), (k + 14, 10)], rgba(GREEN), 7)
    return canvas(220, 20, cb)


@lru_cache(None)
def pct_sprite(txt):
    return canvas(110, 44, lambda p: p.text(108, 22, txt, "mono", 26, rgba(INK2), anchor="rm"))


@lru_cache(None)
def check_sprite(size=46, col=GREEN):
    return canvas(size + 4, size + 4, lambda p: icon(p, "check", size / 2 + 2, size / 2 + 2, size, col))


# ------------------------------------------------------------------ S6: platform / journey browser (30.85 - 34.8)
BW, BH = 840, 620


@lru_cache(None)
def browser_card(url):
    def cb(p):
        p.rr((0, 0, BW - 1, 74), 36, fill=rgba(PANEL))
        p.rect((0, 40, BW - 1, 74), fill=rgba(PANEL))
        p.line([(0, 74), (BW, 74)], rgba(LINE), 2, caps=False)
        for k, c in enumerate([(255, 96, 92), (255, 190, 50), (40, 200, 70)]):
            p.circ(40 + k * 28, 37, 9, fill=rgba(c))
        p.rr((170, 17, 700, 57), 20, fill=rgba(PAPER), outline=rgba(LINE), width=2)
        icon(p, "globe", 196, 37, 22, MUTED)
        p.text(218, 37, url, "monor", 20, rgba(INK2), anchor="lm")
    return card(BW, BH, 36, cb)


@lru_cache(None)
def skeleton(w, h=22, col=SKEL):
    return canvas(w, h, lambda p: p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(col)))


@lru_cache(None)
def journey_title():
    size = 56
    w1 = text_w("My New ", "bold", size)
    w = int(w1 + text_w("Journey", "bold", size) + 10)

    def cb(p):
        p.text(4, size * 0.7, "My New ", "bold", size, rgba(INK), anchor="lm")
        p.text(4 + w1, size * 0.7, "Journey", "bold", size, rgba(BLUE), anchor="lm")
    return canvas(w, int(size * 1.4), cb)


@lru_cache(None)
def journey_node(lab, col):
    return canvas(150, 110, lambda p: (p.circ(75, 24, 20, fill=rgba(col)), p.circ(75, 24, 9, fill=rgba(WHITE)),
                                       p.text(75, 82, lab, "semi", 26, rgba(INK2), anchor="mm")))


@lru_cache(None)
def share_btn(pressed=False):
    w, h = 210, 72

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(BLUE if not pressed else (20, 90, 200)))
        icon(p, "share", 52, h / 2, 30, WHITE, bg=BLUE)
        p.text(84, h / 2, "Share", "bold", 30, rgba(WHITE), anchor="lm")
    return canvas(w, h, cb)


def s_journey(f, t):
    t0, t1 = 30.85, 34.8
    s, a, dy = trans(t, t0, t1)
    cy = 1000 + dy

    def at(rx, ry):
        return CX + (rx - BW / 2) * s, cy + (ry - BH / 2) * s
    put(f, browser_card("computer-hub / my-journey"), CX, cy, s, a)
    loaded = prog(t, 32.95, 0.25)
    # loading skeleton shimmer
    if loaded < 1:
        sh = 0.75 + 0.25 * math.sin(t * 9)
        for (rx, ry, w) in [(60, 150, 420), (60, 210, 640), (60, 250, 560), (60, 330, 700)]:
            x, y = at(rx + w / 2, ry)
            put(f, skeleton(w), x, y, s, a * (1 - loaded) * sh)
    if loaded > 0:
        ps, pa = pop(t, 32.98, 0.36)
        x, y = at(60 + journey_title().width / 2, 160)
        put(f, journey_title(), x, y, ps * s, pa * a)
        # timeline
        ln = out_cubic(prog(t, 33.1, 0.6))
        if ln > 0:
            x0, y0 = at(110, 320)
            w = 620 * ln * s
            put(f, skeleton(620, 8, tint(BLUE, 0.6)), x0 + w / 2, y0, s, a, sx=max(0.01, ln))
        for k, (lab, col) in enumerate([("Start", CYAN), ("Learn", GREEN), ("Build", PURPLE), ("Grow", DARK_YEL)]):
            ps, pa = pop(t, 33.15 + k * 0.13, 0.3)
            x, y = at(110 + k * 206, 352)
            put(f, journey_node(lab, col), x, y, ps * s, pa * a)
    # share button + cursor click
    ps, pa = pop(t, 33.2, 0.3)
    bx, by = at(BW - 60 - 105, BH - 80)
    press = prog(t, 33.72, 0.18)
    k = 1 - 0.08 * math.sin(press * math.pi)
    put(f, share_btn(press > 0.3), bx, by, ps * s * k, pa * a)
    rp = prog(t, 33.74, 0.5)
    if 0 < rp < 1:
        put(f, ring(60, BLUE, 4), bx, by, s * (0.8 + 1.0 * rp), a * (1 - rp) * 0.7)
    cm = out_cubic(prog(t, 33.25, 0.42))
    if cm > 0:
        cx = lerp(bx + 260, bx + 18, cm)
        cyy = lerp(by + 240, by + 22, cm)
        put(f, cursor(), cx, cyy, 1.0 - 0.1 * math.sin(press * math.pi), a * clamp(cm * 3))
    ps, pa = pop(t, 34.0, 0.3)
    x, y = at(BW - 60 - 105 - 300, BH - 80)
    put(f, pill("SHARED", tint(GREEN, 0.85), T_GREEN, size=20, h=52, icon_name="check", icon_col=GREEN),
        x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S7: 4 pillars (34.9 - 43.62)
PILLARS = [("AI Tools", "spark", PURPLE, "WORK SMARTER", 35.28),
           ("Side Hustles", "briefcase", DARK_YEL, "START SMALL", 37.0),
           ("Passive Income", "rupee", GREEN, "EARN WHILE YOU SLEEP", 38.5),
           ("Social Media Brand", "users", CYAN, "GROW YOUR AUDIENCE", 41.22)]
PW, PH = 392, 310


@lru_cache(None)
def pillar_card(i):
    title, ic, col, sub, _ = PILLARS[i]

    def cb(p):
        tile(p, 66, 66, 84, col, ic)
        p.text(30, 150, title, "bold", 33 if len(title) > 14 else 36, rgba(INK), anchor="lm")
        p.text(31, 190, sub, "mono", 17, rgba(MUTED), anchor="lm", spacing=2)
        if i == 0:
            for k, (nm, c) in enumerate([("code", GREEN), ("bolt", DARK_YEL), ("chart", BLUE)]):
                tile(p, 54 + k * 66, 258, 52, c, nm, k=0.88)
        elif i == 1:
            for k in range(2):
                y = 238 + k * 40
                icon(p, "check", 44, y, 24, DARK_YEL)
                p.rr((66, y - 8, 66 + (250 if k == 0 else 190), y + 8), 8, fill=rgba(SKEL))
    return card(PW, PH, 32, cb)


def chart_sprite(t, kind):
    """Dynamic mini chart for Passive Income (line) or Social Media Brand (bars)."""
    w, h = 330, 92
    if kind == "line":
        pr = smooth(prog(t, 38.7, 1.3))
        pts = [(0, 80), (40, 70), (80, 74), (120, 56), (160, 60), (200, 40), (240, 44), (280, 20), (326, 8)]

        def cb(p):
            n = pr * (len(pts) - 1)
            k = int(n)
            vis = pts[:k + 1]
            if k < len(pts) - 1:
                fr = n - k
                (x0, y0), (x1, y1) = pts[k], pts[k + 1]
                vis = vis + [(x0 + (x1 - x0) * fr, y0 + (y1 - y0) * fr)]
            if len(vis) >= 2:
                p.poly(vis + [(vis[-1][0], h), (0, h)], fill=rgba(tint(GREEN, 0.82)))
                p.line(vis, rgba(GREEN), 5)
                p.circ(vis[-1][0], vis[-1][1], 8, fill=rgba(GREEN))
        return canvas(w + 10, h + 4, cb)
    else:
        pr = prog(t, 41.4, 1.0)

        def cb(p):
            for k, hh in enumerate([0.3, 0.45, 0.55, 0.75, 1.0]):
                g = out_back(clamp((pr * 5 - k * 0.7)))
                if g <= 0:
                    continue
                bh = hh * 84 * g
                x = 6 + k * 54
                p.rr((x, h - bh, x + 40, h), 10, fill=rgba(CYAN if k == 4 else tint(CYAN, 0.55)))
            hp = out_back(clamp(prog(t, 42.0, 0.35)))
            if hp > 0:
                icon(p, "heart", 300, 50, 46 * hp, (235, 70, 110))
        return canvas(w + 10, h + 4, cb)


def s_pillars(f, t):
    t1 = 43.62
    ps, pa = pop(t, 34.96, 0.34)
    _, a0, _ = trans(t, 34.96, t1)
    put(f, pill("MY PLAN B", BLUE, WHITE, size=22, h=58), CX, 700, ps, pa * a0)
    for i, (_, _, _, _, ts) in enumerate(PILLARS):
        s, a, dy = trans(t, ts - 0.04, t1, din=0.42, rise=36)
        if a <= 0:
            continue
        cx = CX + (-205 if i % 2 == 0 else 205)
        cy = 925 + (i // 2) * 330 + dy
        put(f, pillar_card(i), cx, cy, s, a)
        if i >= 2:
            spr = chart_sprite(t, "line" if i == 2 else "bars")
            put(f, spr, cx + (-PW / 2 + 30 + spr.width / 2) * s, cy + (PH / 2 - 60) * s, s, a)
        cs, ca = pop(t, 42.4 + i * 0.15, 0.3, s0=0.2)
        put(f, check_sprite(50), cx + (PW / 2 - 40) * s, cy + (-PH / 2 + 40) * s, cs * s, ca * a)


# ------------------------------------------------------------------ S8: website story -> guide (43.6 - 51.95)
@lru_cache(None)
def story_title():
    def cb(p):
        p.circ(60, 56, 52, fill=rgba(CYAN))
        p.text(60, 58, "</>", "mono", 36, rgba(WHITE), anchor="mm")
        p.text(136, 40, "My Story", "bold", 52, rgba(INK), anchor="lm")
        p.text(137, 88, "SOFTWARE ENGINEER → AI CREATOR", "mono", 17, rgba(MUTED), anchor="lm", spacing=2)
    return canvas(700, 116, cb)


GUIDE_ITEMS = [("Learn AI tools", 46.84), ("Start side hustles", 47.48), ("Build your brand", 48.16)]


@lru_cache(None)
def guide_card():
    def cb(p):
        header_label(p, 820, 58, "FOR EVERY TECH PROFESSIONAL", BLUE, 20, 4)
        tile(p, 92, 158, 96, CYAN, "book")
        p.text(162, 138, "The AI Era Guide", "bold", 48, rgba(INK), anchor="lm")
        p.text(163, 188, "Learn · Build · Grow", "reg", 28, rgba(MUTED), anchor="lm")
        p.line([(44, 236), (776, 236)], rgba(LINE), 2, caps=False)
    return card(820, 720, 38, cb)


@lru_cache(None)
def guide_item(txt):
    def cb(p):
        icon(p, "check", 26, 28, 44, GREEN)
        p.text(66, 28, txt, "semi", 32, rgba(INK), anchor="lm")
    return canvas(560, 58, cb)


def stairs_sprite(t):
    w, h = 700, 230

    def cb(p):
        for k in range(4):
            g = out_back(clamp(prog(t, 49.1 + k * 0.32, 0.4)))
            if g <= 0:
                continue
            bh = (40 + k * 40) * g
            x = 20 + k * 150
            p.rr((x, h - bh, x + 120, h), 16, fill=rgba(tint(BLUE, 0.75 - k * 0.2)))
        ar = out_cubic(prog(t, 50.72, 0.6))
        if ar > 0:
            x0, y0, x1, y1 = 40, 195, 40 + 600 * ar, 195 - 165 * ar
            p.line([(x0, y0), (x1, y1)], rgba(GREEN), 9)
            ang = math.atan2(y1 - y0, x1 - x0)
            hx, hy = x1 + 10 * math.cos(ang), y1 + 10 * math.sin(ang)
            a1, a2 = ang + 2.6, ang - 2.6
            p.poly([(hx, hy), (hx + 34 * math.cos(a1), hy + 34 * math.sin(a1)),
                    (hx + 34 * math.cos(a2), hy + 34 * math.sin(a2))], fill=rgba(GREEN))
    return canvas(w, h, cb)


def s_story_guide(f, t):
    # part A: website "My Story"
    flip_t = 46.02
    if t < flip_t + 0.2:
        s, a, dy = trans(t, 43.6, None)
        sx = 1 - smooth(prog(t, flip_t - 0.02, 0.2))
        cy = 1010 + dy
        put(f, browser_card("computer-hub / about"), CX, cy, s, a, sx=max(sx, 0.001))
        if sx > 0.02:
            ps, pa = pop(t, 43.86, 0.38)
            put(f, story_title(), CX, cy - 140 * s, ps * s, pa * a, sx=sx)
            for k, w in enumerate([700, 640, 690, 520, 600]):
                rv = smooth(prog(t, 44.3 + k * 0.18, 0.35))
                if rv > 0:
                    x = CX + (-BW / 2 + 70 + w * rv / 2) * s * sx
                    put(f, skeleton(w), x, cy + (-10 + k * 44) * s, s, a, sx=sx * max(rv, 0.01))
            ps, pa = pop(t, 44.98, 0.36)
            put(f, pill("MY JOURNEY", tint(CYAN, 0.85), T_CYAN, size=20, h=52, icon_name="book",
                        icon_col=T_CYAN), CX + 200 * s * sx, cy + 240 * s, ps * s, pa * a, sx=sx)
    # part B: guide card
    if t >= flip_t + 0.15:
        sx = smooth(prog(t, flip_t + 0.15, 0.22))
        _, a, dy = trans(t, flip_t + 0.15, 51.95, din=0.3, rise=0)
        s = 1.0 - 0.07 * in_cubic(prog(t, 51.95 - 0.28, 0.28))
        cy = 1060 + dy
        put(f, guide_card(), CX, cy, s, a, sx=max(sx, 0.001))
        for k, (txt, ts) in enumerate(GUIDE_ITEMS):
            ps, pa = pop(t, ts, 0.34)
            spr = guide_item(txt)
            put(f, spr, CX + (-410 + 52 + spr.width / 2) * s * sx, cy + (-360 + 278 + k * 62) * s, ps * s, pa * a,
                sx=sx)
        if t >= 49.0:
            spr = stairs_sprite(t)
            put(f, spr, CX, cy + (-360 + 582) * s, s, a)
            ps, pa = pop(t, 50.18, 0.34)
            put(f, pill("NEW AI ERA", tint(PURPLE, 0.86), PURPLE, size=20, h=50, icon_name="spark", icon_col=PURPLE),
                CX - 220 * s, cy + (-360 + 468) * s, ps * s, pa * a)
            ps, pa = pop(t, 51.02, 0.34)
            put(f, pill("LEVEL UP", tint(GREEN, 0.85), T_GREEN, size=20, h=50, icon_name="trend",
                        icon_col=GREEN), CX + 120 * s, cy + (-360 + 468) * s, ps * s, pa * a)


# ------------------------------------------------------------------ S9/S10: welcome + outro (52.05 - 60)
@lru_cache(None)
def welcome_text():
    size = 50
    a, b = "Welcome to ", "Computer Hub"
    w1 = text_w(a, "bold", size)
    w = int(w1 + text_w(b, "bold", size) + 12)

    def cb(p):
        p.text(6, size * 0.72, a, "bold", size, rgba(INK), anchor="lm")
        p.text(6 + w1, size * 0.72, b, "bold", size, rgba(BLUE), anchor="lm")
    return canvas(w, int(size * 1.45), cb)


@lru_cache(None)
def follow_btn(done=False):
    w, h = 420, 104

    def cb(p):
        if not done:
            p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(BLUE))
            icon(p, "plus", 120, h / 2, 40, WHITE)
            p.text(156, h / 2, "Follow", "bold", 44, rgba(WHITE), anchor="lm")
        else:
            p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(PAPER), outline=rgba(CYAN), width=4)
            icon(p, "check", 96, h / 2, 46, GREEN)
            p.text(134, h / 2, "Following", "bold", 44, rgba(BLUE), anchor="lm")
    img = canvas(w, h, cb)
    return with_shadow_pill(img, h)


def s_outro(f, t):
    t0 = 52.05
    s, a, dy = trans(t, t0, None, din=0.6, s0=0.5)
    bob = 5 * math.sin((t - t0) * 2.0) * prog(t, 53.0, 1.0)
    cy = 900 + dy + bob
    k = 0
    tr = 52.2
    while tr < t and k < 8:
        pr = prog(t, tr, 1.4)
        if 0 < pr < 1:
            put(f, ring(180, CYAN if k % 2 == 0 else LGREEN_SOFT, 5), CX, cy, s * (0.98 + 0.5 * out_cubic(pr)),
                (1 - pr) * 0.5 * a)
        tr += 1.5
        k += 1
    put(f, logo_shadow(370), CX, cy, s, a * 0.9)
    put(f, logo(370), CX, cy, s, a)
    # welcome text -> handle
    sw = prog(t, 53.62, 0.22)
    ps, pa = pop(t, 52.86, 0.38)
    put(f, welcome_text(), CX, 1170, ps * (1 - 0.1 * sw), pa * (1 - sw))
    ps, pa = pop(t, 53.78, 0.4)
    put(f, handle_pill(44), CX, 1172, ps, pa)
    # learn / grow chips
    for lab, ic, col, tcol, x, ts in [("LEARN", "book", tint(GREEN, 0.85), T_GREEN, CX - 150, 54.78),
                                      ("GROW", "trend", tint(BLUE, 0.85), BLUE, CX + 150, 55.68)]:
        ps, pa = pop(t, ts, 0.34)
        put(f, pill(lab, col, tcol, size=24, h=62, icon_name=ic, icon_col=tcol), x, 1295, ps, pa)
    # follow button + click
    ps, pa = pop(t, 56.25, 0.42, s0=0.4)
    press = prog(t, 56.98, 0.2)
    kk = 1 - 0.07 * math.sin(press * math.pi)
    done = press > 0.5
    put(f, follow_btn(done), CX, 1420, ps * kk, pa)
    rp = prog(t, 57.0, 0.6)
    if 0 < rp < 1:
        put(f, ring(100, BLUE, 5), CX, 1420, 0.9 + 1.0 * rp, (1 - rp) * 0.6)
    cm = out_cubic(prog(t, 56.5, 0.45))
    if cm > 0:
        leave = out_cubic(prog(t, 57.6, 0.5))
        cx = lerp(CX + 330, CX + 70, cm) + 120 * leave
        cyy = lerp(1620, 1440, cm) + 160 * leave
        put(f, cursor(), cx, cyy, 1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - leave))


LGREEN_SOFT = (84, 222, 60)

# (start, end, function) — a scene is drawn only inside its window
SCENES = [
    (0.0, 1.5, s_logo_intro),
    (1.52, 4.5, s_tech),
    (4.35, 9.8, s_code),
    (9.85, 17.45, s_engineer),
    (18.05, 22.5, s_news),
    (22.4, 25.1, s_planb),
    (25.0, 30.8, s_shift),
    (30.85, 34.85, s_journey),
    (34.9, 43.65, s_pillars),
    (43.6, 52.0, s_story_guide),
    (52.05, 60.1, s_outro),
]
