"""DAY 1 — "Building my Plan B: Chrome Extension clone idea".

Voice: episodes/day01/voice.mp3 (58.75 s). Word timings from faster-whisper (episodes/day01/words.json),
checked against the speech envelope. Same look as the pilot (isometric background, light cards, white captions).
"""
import math
import os
from functools import lru_cache

from gfx import (BLUE, BORDER, CYAN, DARK, DARK_YEL, GREEN, INK, INK2, LINE, MUTED, ORANGE, PANEL, PURPLE, SKEL,
                 T_GREEN, T_YELLOW, WHITE, YELLOW, canvas, card, clamp, icon, in_cubic, lerp, out_back, out_cubic,
                 pop, prog, put, rgba, smooth, text_w, tile, tint, trans)
from scenes import (BH, BW, CX, bar_fill, big_num, browser_card, check_sprite, cursor, follow_btn, handle_pill,
                    header_label, logo, logo_shadow, pill, ring, skeleton)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.path.join(ROOT, "episodes", "day01", "voice.mp3")
VOICE_LEN = 58.75
TOTAL_LEN = 62.0   # 3.25 s outro tail after the voice ends
CAP_END = 59.3
HEADER = "COMPUTER HUB · PLAN B · DAY 1"

# (word, start, highlight) per phrase, phrase end time
PHRASES = [
    ([("Aaj", 0.00, 0), ("hai", 0.36, 0), ("Day", 0.58, 1), ("1", 0.98, 1)], 1.32),
    ([("of", 1.32, 0), ("building", 1.54, 0), ("my", 1.78, 0), ("Plan", 1.96, 1), ("B", 2.38, 1)], 2.58),
    ([("as", 2.58, 0), ("a", 2.86, 0), ("Software", 3.16, 1), ("Engineer!", 3.42, 1)], 4.20),
    ([("Kya", 4.56, 0), ("aap", 4.80, 0), ("bhi", 5.16, 0), ("meri", 5.26, 0), ("tarah", 5.48, 0)], 5.68),
    ([("job", 5.68, 1), ("ke", 6.12, 0), ("saath", 6.28, 0), ("freelancing", 6.48, 1), ("nahi", 6.98, 0),
      ("karte?", 7.18, 0)], 7.42),
    ([("Toh", 7.95, 0), ("sawaal", 8.10, 0), ("hai —", 8.60, 0), ("extra", 9.34, 1), ("income", 9.70, 1),
      ("kaise", 10.12, 0), ("banayein?", 10.46, 0)], 10.78),
    ([("Aaj", 11.24, 0), ("ka", 11.56, 0), ("idea", 11.66, 1), ("hai", 12.00, 0)], 12.26),
    ([("ek", 12.26, 0), ("Chrome", 12.44, 1), ("Extension", 12.78, 1), ("ka", 13.22, 0), ("clone", 13.46, 1),
      ("banana!", 13.94, 0)], 14.32),
    ([("Maine", 14.86, 0), ("ek", 15.00, 0), ("extension", 15.12, 0), ("dekha", 15.62, 0), ("hai,", 15.88, 0)], 16.12),
    ([("rocketsenter.com,", 16.25, 1), ("jo", 17.92, 0), ("Chrome", 18.00, 1), ("ke", 18.36, 0), ("saath", 18.50, 0)], 18.70),
    ([("connect", 18.70, 0), ("hokar", 19.06, 0), ("bulk", 19.50, 1), ("messaging", 19.82, 1)], 20.16),
    ([("ki", 20.16, 0), ("suvidha", 20.42, 0), ("deta", 20.74, 0), ("hai!", 21.06, 0)], 21.26),
    ([("Market", 21.64, 0), ("mein", 22.04, 0), ("aise", 22.24, 0), ("tools", 22.42, 0)], 22.92),
    ([("lagbhag", 22.92, 0), ("₹1,500", 23.50, 1), ("per", 24.82, 1), ("month", 25.14, 1)], 25.56),
    ([("mein", 25.56, 0), ("bik", 25.70, 0), ("rahe", 25.84, 0), ("hain!", 26.02, 0)], 26.16),
    ([("Toh", 26.60, 0), ("kyun", 26.84, 0), ("na", 27.08, 0), ("hum", 27.20, 0)], 27.38),
    ([("iska", 27.38, 0), ("ek", 27.66, 0), ("behtar", 27.86, 1), ("alternative", 28.22, 1), ("banayein?", 28.74, 0)], 29.06),
    ([("Claude", 29.44, 1), ("aur", 29.76, 0), ("reverse", 30.02, 1), ("engineering", 30.34, 1)], 30.86),
    ([("ki", 30.86, 0), ("madad", 31.02, 0), ("se", 31.22, 0), ("aisa", 31.60, 0), ("hi", 31.94, 0), ("ek", 32.10, 0),
      ("tool", 32.22, 1)], 32.44),
    ([("develop", 32.44, 1), ("karein,", 32.76, 0), ("jismein", 33.02, 0), ("kuch", 33.56, 0)], 33.74),
    ([("extra", 33.74, 1), ("features", 34.20, 1), ("bhi", 34.60, 0), ("hon!", 34.74, 0)], 34.88),
    ([("Isse", 35.36, 0), ("hum", 35.66, 0), ("short-term", 35.82, 1), ("mein", 36.44, 0)], 36.62),
    ([("ek", 36.62, 0), ("achha", 36.92, 0), ("revenue", 37.22, 1), ("stream", 37.60, 1), ("bana", 37.88, 0),
      ("sakte", 38.06, 0), ("hain!", 38.36, 0)], 38.44),
    ([("Lekin", 39.08, 0), ("ek", 40.08, 0), ("badi", 40.32, 1), ("problem", 40.60, 1), ("hai —", 41.04, 0)], 41.16),
    ([("software", 41.70, 0), ("banana", 42.18, 0), ("aasaan", 42.58, 1), ("hai,", 42.98, 0)], 43.24),
    ([("use", 43.62, 0), ("bechna", 43.80, 1), ("mushkil!", 44.42, 1)], 44.94),
    ([("Apna", 45.62, 0), ("product", 45.84, 1), ("kaise", 46.34, 0), ("bechenge", 46.66, 1)], 47.20),
    ([("aur", 47.20, 0), ("customers", 47.58, 1), ("kaise", 48.18, 0), ("layenge?", 48.46, 0)], 48.76),
    ([("Ye", 49.34, 0), ("hum", 49.52, 0), ("agle", 49.74, 1), ("video", 50.10, 1), ("mein", 50.36, 0),
      ("discuss", 50.46, 0), ("karenge!", 50.78, 0)], 51.18),
    ([("Toh", 51.58, 0), ("Plan", 51.72, 1), ("B", 52.06, 1), ("ki", 52.18, 0), ("is", 52.32, 0), ("journey", 52.48, 1),
      ("ko", 52.78, 0)], 52.94),
    ([("follow", 52.94, 1), ("karna", 53.30, 0), ("mat", 53.58, 0), ("bhoolna!", 53.76, 0)], 54.08),
    ([("Follow", 54.50, 1), ("karo,", 54.80, 0), ("kyunki", 55.42, 0), ("ab", 55.62, 0)], 55.98),
    ([("sirf", 55.98, 0), ("coding", 56.32, 1), ("nahi,", 56.72, 0), ("earning", 57.36, 1), ("bhi", 57.76, 0),
      ("seekhni", 57.94, 0), ("hai!", 58.28, 0)], 58.50),
]


def _at(cx, cy, w, h, s):
    """Map card-local coords (0..w, 0..h) to the frame for a card centred at (cx, cy) with scale s."""
    return lambda rx, ry: (cx + (rx - w / 2) * s, cy + (ry - h / 2) * s)


# ------------------------------------------------------------------ S1: DAY 1 calendar (0 - 4.45)
@lru_cache(None)
def day_card():
    w, h = 560, 600

    def cb(p):
        p.rr((0, 0, w - 1, 150), 38, fill=rgba(CYAN))
        p.rect((0, 100, w - 1, 150), fill=rgba(CYAN))
        for x in (150, w - 150):
            p.circ(x, 0, 18, fill=rgba(WHITE))
            p.circ(x, 0, 9, fill=rgba((0, 120, 180)))
        p.text(w / 2, 82, "DAY", "mono", 46, rgba(WHITE), anchor="mm", spacing=14)
        p.line([(50, 470), (w - 50, 470)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


@lru_cache(None)
def plan_b_line():
    size = 40
    a, b = "Building my ", "Plan B"
    w1 = text_w(a, "bold", size)
    w = int(w1 + text_w(b, "bold", size) + 10)

    def cb(p):
        p.text(4, size * 0.72, a, "bold", size, rgba(INK), anchor="lm")
        p.text(4 + w1, size * 0.72, b, "bold", size, rgba(BLUE), anchor="lm")
    return canvas(w, int(size * 1.45), cb)


@lru_cache(None)
def track_dot(on):
    return canvas(40, 40, lambda p: p.circ(20, 20, 13, fill=rgba(CYAN)) if on else
                  p.circ(20, 20, 11, outline=rgba(tint(CYAN, 0.55)), width=4))


def s_day(f, t):
    s, a, dy = trans(t, 0.02, 4.45, din=0.5, s0=0.6)
    cx, cy = CX, 960 + dy
    at = _at(cx, cy, 560, 600, s)
    put(f, day_card(), cx, cy, s, a)
    ps, pa = pop(t, 0.95, 0.45, s0=0.2)
    x, y = at(280, 300)
    put(f, big_num("1", INK, 240), x, y, ps * s, pa * a)
    ps, pa = pop(t, 1.96, 0.36)
    x, y = at(280, 520)
    put(f, plan_b_line(), x, y, ps * s, pa * a)
    for k in range(5):
        ps, pa = pop(t, 1.4 + k * 0.08, 0.3)
        x, y = at(170 + k * 55, 430)
        put(f, track_dot(k == 0), x, y, ps * s, pa * a)
    ps, pa = pop(t, 3.16, 0.36)
    put(f, pill("SOFTWARE ENGINEER", WHITE, INK, size=22, h=60, icon_name="code", icon_col=CYAN, border=BORDER),
        CX, 1335 + dy, ps * s, pa * a)


# ------------------------------------------------------------------ S2: job vs freelancing (4.45 - 7.65)
@lru_cache(None)
def work_card():
    w, h = 800, 430

    def cb(p):
        header_label(p, w, 56, "YOUR WORK RIGHT NOW", BLUE, 22, 5)
        for k, (ic, col, title, sub) in enumerate([("briefcase", DARK_YEL, "Full-time Job", "Salary every month"),
                                                    ("laptop", CYAN, "Freelancing", "Extra projects")]):
            y = 160 + k * 150
            p.rr((40, y - 60, w - 40, y + 60), 26, fill=rgba(PANEL), outline=rgba(LINE), width=2)
            tile(p, 110, y, 84, col, ic)
            p.text(176, y - 16, title, "bold", 36, rgba(INK), anchor="lm")
            p.text(177, y + 24, sub, "reg", 24, rgba(MUTED), anchor="lm")
    return card(w, h, 36, cb)


@lru_cache(None)
def toggle(on):
    w, h = 110, 60
    return canvas(w, h, lambda p: (p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(GREEN if on else (205, 211, 222))),
                                   p.circ(w - h / 2 if on else h / 2, h / 2, h / 2 - 7, fill=rgba(WHITE))))


@lru_cache(None)
def qmark(col=PURPLE, r=46):
    return canvas(2 * r + 8, 2 * r + 8, lambda p: (p.circ(r + 4, r + 4, r, fill=rgba(col)),
                                                   p.text(r + 4, r + 6, "?", "black", r * 1.3, rgba(WHITE), anchor="mm")))


def s_work(f, t):
    s, a, dy = trans(t, 4.45, 7.65)
    cx, cy = CX, 980 + dy
    at = _at(cx, cy, 800, 430, s)
    put(f, work_card(), cx, cy, s, a)
    ps, pa = pop(t, 5.68, 0.32, s0=0.2)
    x, y = at(690, 160)
    put(f, check_sprite(60), x, y, ps * s, pa * a)
    ps, pa = pop(t, 6.48, 0.3)
    x, y = at(680, 310)
    put(f, toggle(False), x, y, ps * s, pa * a)
    ps, pa = pop(t, 7.12, 0.36, s0=0.2)
    x, y = at(760, 30)
    put(f, qmark(), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S3: extra income? (7.7 - 11.05)
@lru_cache(None)
def income_q_card():
    w, h = 760, 560

    def cb(p):
        header_label(p, w, 60, "THE QUESTION", BLUE, 22, 6)
        p.rr((60, 470, w - 60, 500), 15, fill=rgba(SKEL))
    return card(w, h, 38, cb)


@lru_cache(None)
def extra_income_title():
    size = 96
    a, b = "Extra ", "Income?"
    w1 = text_w(a, "black", size)
    w = int(w1 + text_w(b, "black", size) + 16)

    def cb(p):
        p.text(8, size * 0.65, a, "black", size, rgba(INK), anchor="lm")
        p.text(8 + w1, size * 0.65, b, "black", size, rgba(GREEN), anchor="lm")
    return canvas(w, int(size * 1.3), cb)


@lru_cache(None)
def coin(r=44):
    return canvas(2 * r + 8, 2 * r + 8, lambda p: (p.circ(r + 4, r + 4, r, fill=rgba((255, 196, 30))),
                                                   p.circ(r + 4, r + 4, r * 0.78, fill=rgba(YELLOW)),
                                                   p.text(r + 4, r + 6, "₹", "bold", r * 1.05, rgba((160, 100, 0)),
                                                          anchor="mm")))


def s_income(f, t):
    s, a, dy = trans(t, 7.7, 11.05)
    cx, cy = CX, 1000 + dy
    at = _at(cx, cy, 760, 560, s)
    put(f, income_q_card(), cx, cy, s, a)
    ps, pa = pop(t, 9.3, 0.45, s0=0.3)
    x, y = at(380, 170)
    put(f, extra_income_title(), x, y, ps * s, pa * a)
    for k in range(5):  # coins drop into a stack
        tk = 9.6 + k * 0.16
        p = prog(t, tk, 0.38)
        if p <= 0:
            continue
        drop = 1 - out_back(p, 1.3)
        x, y = at(250 + k * 65, 395 - 0 * k)
        put(f, coin(), x, y - 160 * drop * s, s, a * clamp(p * 3))
    fill = out_cubic(prog(t, 9.7, 1.0))
    if fill > 0:
        x, y = at(60 + 640 * fill / 2, 485)
        put(f, bar_fill(640 * fill, GREEN), x, y, s, a)


# ------------------------------------------------------------------ S4: today's idea — Chrome extension clone (11.1 - 14.6)
@lru_cache(None)
def ext_window():
    w, h = 820, 560

    def cb(p):
        p.rr((0, 0, w - 1, 74), 36, fill=rgba(PANEL))
        p.rect((0, 40, w - 1, 74), fill=rgba(PANEL))
        p.line([(0, 74), (w, 74)], rgba(LINE), 2, caps=False)
        for k, c in enumerate([(255, 96, 92), (255, 190, 50), (40, 200, 70)]):
            p.circ(40 + k * 28, 37, 9, fill=rgba(c))
        p.rr((140, 17, 640, 57), 20, fill=rgba(WHITE), outline=rgba(LINE), width=2)
        p.text(164, 37, "chrome://extensions", "monor", 20, rgba(INK2), anchor="lm")
        icon(p, "puzzle", 700, 37, 32, MUTED)
    return card(w, h, 36, cb)


@lru_cache(None)
def ext_tile(kind):
    w, h = 300, 250
    orig = kind == "orig"
    col = (150, 160, 180) if orig else CYAN

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 30, fill=rgba(WHITE if orig else tint(CYAN, 0.9)),
             outline=rgba(LINE if orig else CYAN), width=3)
        tile(p, w / 2, 92, 104, col, "puzzle")
        p.text(w / 2, 185, "Original" if orig else "Our Clone", "bold", 32, rgba(INK), anchor="mm")
        p.text(w / 2, 222, "EXTENSION" if orig else "+ BETTER", "mono", 16, rgba(MUTED if orig else T_GREEN),
               anchor="mm", spacing=3)
    return canvas(w, h, cb)


@lru_cache(None)
def idea_title():
    size = 46
    return canvas(int(text_w("Chrome Extension Clone", "bold", size) + 12), int(size * 1.4),
                  lambda p: p.text(6, size * 0.7, "Chrome Extension Clone", "bold", size, rgba(INK), anchor="lm"))


@lru_cache(None)
def arrow_right(col=BLUE, w=110):
    def cb(p):
        p.line([(6, 22), (w - 22, 22)], rgba(col), 8)
        p.poly([(w - 30, 6), (w - 4, 22), (w - 30, 38)], fill=rgba(col))
    return canvas(w, 44, cb)


def s_idea(f, t):
    ps, pa = pop(t, 11.22, 0.34)
    _, a0, _ = trans(t, 11.2, 14.6)
    put(f, pill("TODAY'S IDEA", YELLOW, DARK, size=24, h=62, icon_name="bolt", icon_col=DARK), CX, 700, ps, pa * a0)
    s, a, dy = trans(t, 11.6, 14.6)
    cx, cy = CX, 1050 + dy
    at = _at(cx, cy, 820, 560, s)
    put(f, ext_window(), cx, cy, s, a)
    rp = prog(t, 12.78, 0.6)
    if 0 < rp < 1:
        x, y = at(700, 37)
        put(f, ring(30, CYAN, 4), x, y, s * (0.8 + 1.2 * rp), a * (1 - rp))
    ps, pa = pop(t, 12.6, 0.34)
    x, y = at(410, 140)
    put(f, idea_title(), x, y, ps * s, pa * a)
    x, y = at(200, 370)
    put(f, ext_tile("orig"), x, y, s, a * prog(t, 12.78, 0.25))
    cp = out_cubic(prog(t, 13.46, 0.5))  # clone slides out of the original
    if cp > 0:
        x, y = at(lerp(200, 620, cp), 370)
        put(f, ext_tile("clone"), x, y, s, a * clamp(cp * 2))
        x, y = at(410, 370)
        put(f, arrow_right(), x, y, s, a * prog(t, 13.7, 0.25))


# ------------------------------------------------------------------ S5: existing tool — bulk messaging (14.7 - 21.45)
CONTACTS = 5


@lru_cache(None)
def bulk_panel():
    w, h = 600, 420

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), 28, fill=rgba(WHITE), outline=rgba(BORDER), width=2)
        tile(p, 50, 46, 56, GREEN, "chat")
        p.text(92, 46, "Bulk Messaging", "bold", 30, rgba(INK), anchor="lm")
        p.line([(24, 88), (w - 24, 88)], rgba(LINE), 2, caps=False)
        for k in range(CONTACTS):
            y = 122 + k * 54
            p.circ(56, y, 18, fill=rgba(tint([CYAN, PURPLE, DARK_YEL, GREEN, BLUE][k], 0.45)))
            p.rr((90, y - 8, 90 + [260, 200, 240, 180, 220][k], y + 8), 8, fill=rgba(SKEL))
    return canvas(w, h, cb)


@lru_cache(None)
def msg_bubble():
    return canvas(70, 56, lambda p: icon(p, "chat", 35, 28, 52, GREEN))


def s_tool(f, t):
    s, a, dy = trans(t, 14.7, 21.45)
    cx, cy = CX, 1010 + dy
    at = _at(cx, cy, BW, BH, s)
    put(f, browser_card("rocketsenter.com" if t >= 16.15 else "searching extensions…"), cx, cy, s, a)
    ps, pa = pop(t, 15.1, 0.4)
    x, y = at(BW / 2, 330)
    put(f, bulk_panel(), x, y, ps * s, pa * a)
    ps, pa = pop(t, 18.7, 0.34)
    put(f, pill("CONNECTS WITH CHROME", tint(CYAN, 0.85), BLUE, size=20, h=54, icon_name="puzzle", icon_col=BLUE),
        CX, cy - (BH / 2 + 45) * s, ps * s, pa * a)
    # bulk messaging: bubbles fly from the composer to every contact, each gets a tick
    for k in range(CONTACTS):
        t0 = 19.5 + k * 0.22
        p = prog(t, t0, 0.42)
        if p <= 0:
            continue
        ty = 330 - 210 + 122 + k * 54
        sx_, sy_ = at(BW / 2 - 200, 600)
        ex, ey = at(BW / 2 + 230, ty)
        if p < 1:
            e = out_cubic(p)
            put(f, msg_bubble(), lerp(sx_, ex, e), lerp(sy_, ey, e) - 60 * math.sin(math.pi * e) * s, 0.7 * s,
                a * (1 - in_cubic(p)))
        cs, ca = pop(t, t0 + 0.38, 0.28, s0=0.2)
        put(f, check_sprite(36), ex, ey, cs * s, ca * a)
    ps, pa = pop(t, 19.45, 0.34)
    x, y = at(BW / 2, 560)
    put(f, pill("SEND TO ALL", BLUE, WHITE, size=22, h=58, icon_name="chat", icon_col=WHITE), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S6: market price ₹1,500 / month (21.5 - 26.4)
@lru_cache(None)
def price_card():
    w, h = 780, 560

    def cb(p):
        header_label(p, w, 60, "MARKET PRICE", BLUE, 22, 6)
        p.line([(60, 330), (w - 60, 330)], rgba(LINE), 2, caps=False)
        p.text(60, 382, "Similar tools", "semi", 28, rgba(INK2), anchor="lm")
    return card(w, h, 38, cb)


@lru_cache(None)
def price_text(v):
    size = 130
    txt = f"₹{v:,}"
    w = int(text_w("₹9,999", "black", size) + 20)
    return canvas(w, int(size * 1.3), lambda p: p.text(w / 2, size * 0.66, txt, "black", size, rgba(INK), anchor="mm"))


@lru_cache(None)
def tool_tag(k):
    w, h = 200, 92
    col = [CYAN, PURPLE, DARK_YEL][k]

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 22, fill=rgba(PANEL), outline=rgba(LINE), width=2)
        tile(p, 46, h / 2, 52, col, "puzzle")
        p.text(84, h / 2 - 12, "Tool " + "ABC"[k], "bold", 24, rgba(INK), anchor="lm")
        p.text(84, h / 2 + 18, "₹/month", "mono", 16, rgba(MUTED), anchor="lm")
    return canvas(w, h, cb)


def s_price(f, t):
    s, a, dy = trans(t, 21.5, 26.4)
    cx, cy = CX, 1010 + dy
    at = _at(cx, cy, 780, 560, s)
    put(f, price_card(), cx, cy, s, a)
    cnt = smooth(prog(t, 23.45, 1.2))
    v = int(round(cnt * 1500 / 10) * 10)
    if t >= 23.4:
        ps, _ = pop(t, 23.45, 0.4, s0=0.6)
        bump = 1 + 0.06 * math.sin(math.pi * prog(t, 24.65, 0.3))
        x, y = at(390, 185)
        put(f, price_text(v), x, y, ps * s * bump, a)
    ps, pa = pop(t, 25.1, 0.34)
    x, y = at(390, 285)
    put(f, pill("PER MONTH", tint(BLUE, 0.88), BLUE, size=22, h=54), x, y, ps * s, pa * a)
    for k in range(3):
        ps, pa = pop(t, 22.42 + k * 0.14, 0.32)
        x, y = at(150 + k * 240, 460)
        put(f, tool_tag(k), x, y, ps * s, pa * a)
    ps, pa = pop(t, 25.75, 0.34)
    x, y = at(640, 382)
    put(f, pill("SELLING NOW", tint(GREEN, 0.85), T_GREEN, size=18, h=46, icon_name="trend", icon_col=GREEN),
        x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S7: better alternative (26.5 - 29.25)
@lru_cache(None)
def vs_side(kind):
    w, h = 340, 400
    ours = kind == "ours"

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 32, fill=rgba(WHITE if ours else PANEL), outline=rgba(GREEN if ours else LINE),
             width=4 if ours else 2)
        tile(p, w / 2, 100, 110, CYAN if ours else (150, 160, 180), "puzzle")
        p.text(w / 2, 205, "Our Tool" if ours else "Existing Tool", "bold", 34, rgba(INK), anchor="mm")
        p.text(w / 2, 255, "Better + more" if ours else "₹1,500 / month", "semi", 26,
               rgba(T_GREEN if ours else MUTED), anchor="mm")
        if ours:
            for k in range(3):
                icon(p, "check", 90 + k * 80, 325, 40, GREEN)
        else:
            p.rr((70, 310, w - 70, 338), 14, fill=rgba(SKEL))
    return canvas(w, h, cb)


@lru_cache(None)
def vs_mid():
    return canvas(110, 110, lambda p: (p.circ(55, 55, 48, fill=rgba(YELLOW)),
                                       p.text(55, 57, "VS", "black", 40, rgba(DARK), anchor="mm")))


def s_better(f, t):
    _, a, dy = trans(t, 26.5, 29.25)
    cy = 1010 + dy
    ps, pa = pop(t, 26.55, 0.36)
    put(f, vs_side("theirs"), CX - 195, cy, ps, pa * a * (1 - 0.35 * prog(t, 28.2, 0.3)))
    ps, pa = pop(t, 27.86, 0.42, s0=0.4)
    glow = 1 + 0.04 * math.sin(math.pi * prog(t, 28.22, 0.4))
    put(f, vs_side("ours"), CX + 195, cy, ps * glow, pa * a)
    ps, pa = pop(t, 27.2, 0.3)
    put(f, vs_mid(), CX, cy, ps, pa * a)
    ps, pa = pop(t, 28.22, 0.34)
    put(f, pill("BETTER ALTERNATIVE", GREEN, WHITE, size=22, h=60, icon_name="trend", icon_col=WHITE),
        CX, cy - 270, ps, pa * a)


# ------------------------------------------------------------------ S8: build plan — Claude + reverse engineering (29.3 - 35.15)
@lru_cache(None)
def build_card():
    w, h = 820, 640

    def cb(p):
        header_label(p, w, 56, "THE BUILD PLAN", BLUE, 22, 6)
        p.text(60, 470, "Developing", "semi", 28, rgba(INK2), anchor="lm")
        p.rr((60, 505, w - 60, 533), 14, fill=rgba(SKEL))
    return card(w, h, 38, cb)


@lru_cache(None)
def build_node(kind):
    w, h = 220, 190
    name, ic, col = {"claude": ("Claude AI", "spark", PURPLE), "rev": ("Reverse Eng.", "search", DARK_YEL),
                     "tool": ("Our Tool", "puzzle", CYAN)}[kind]

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 28, fill=rgba(tint(col, 0.9)), outline=rgba(tint(col, 0.55)), width=3)
        p.rr((w / 2 - 42, 30, w / 2 + 42, 114), 22, fill=rgba(col))
        icon(p, ic, w / 2, 72, 46, WHITE, bg=col)
        p.text(w / 2, 150, name, "bold", 28, rgba(INK), anchor="mm")
    return canvas(w, h, cb)


@lru_cache(None)
def plus_small():
    return canvas(70, 70, lambda p: (p.circ(35, 35, 30, fill=rgba(INK2)), icon(p, "plus", 35, 35, 34, WHITE)))


@lru_cache(None)
def feature_chip():
    return pill("+ FEATURE", tint(GREEN, 0.85), T_GREEN, size=18, h=46)


def s_build(f, t):
    s, a, dy = trans(t, 29.3, 35.15)
    cx, cy = CX, 1020 + dy
    at = _at(cx, cy, 820, 640, s)
    put(f, build_card(), cx, cy, s, a)
    for kind, rx, ts in [("claude", 130, 29.42), ("rev", 390, 30.0)]:
        ps, pa = pop(t, ts, 0.36)
        x, y = at(rx, 210)
        put(f, build_node(kind), x, y, ps * s, pa * a)
    ps, pa = pop(t, 29.8, 0.3)
    x, y = at(260, 210)
    put(f, plus_small(), x, y, ps * s, pa * a)
    ap = out_cubic(prog(t, 31.2, 0.4))
    if ap > 0:
        x, y = at(545, 210)
        put(f, arrow_right(GREEN, 90), x, y, s, a, sx=max(ap, 0.02))
    ps, pa = pop(t, 32.18, 0.4, s0=0.3)
    x, y = at(700, 210)
    put(f, build_node("tool"), x, y, ps * s * 0.9, pa * a)
    fill = smooth(prog(t, 32.44, 1.3))
    if fill > 0:
        bw = 700 * fill
        x, y = at(60 + bw / 2, 519)
        put(f, bar_fill(bw, BLUE), x, y, s, a)
    for k in range(3):
        ps, pa = pop(t, 33.74 + k * 0.2, 0.32)
        x, y = at(160 + k * 250, 370)
        put(f, feature_chip(), x, y, ps * s, pa * a)
    ps, pa = pop(t, 34.6, 0.3)
    x, y = at(735, 470)
    put(f, check_sprite(46), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S9: short-term revenue stream (35.2 - 38.95)
@lru_cache(None)
def revenue_card():
    w, h = 780, 520

    def cb(p):
        header_label(p, w, 56, "SHORT-TERM GOAL", BLUE, 22, 6)
        tile(p, 98, 150, 84, GREEN, "rupee")
        p.text(160, 132, "Revenue Stream", "bold", 44, rgba(INK), anchor="lm")
        p.text(161, 180, "From our own tool", "reg", 26, rgba(MUTED), anchor="lm")
        for k in range(4):
            y = 260 + k * 62
            p.line([(60, y), (w - 60, y)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


def revenue_chart(t):
    w, h = 660, 230
    pr = smooth(prog(t, 37.1, 1.3))
    pts = [(0, 210), (80, 196), (160, 200), (240, 170), (320, 160), (400, 120), (480, 112), (560, 60), (650, 22)]

    def cb(p):
        n = pr * (len(pts) - 1)
        k = int(n)
        vis = pts[:k + 1]
        if k < len(pts) - 1:
            fr = n - k
            (x0, y0), (x1, y1) = pts[k], pts[k + 1]
            vis = vis + [(x0 + (x1 - x0) * fr, y0 + (y1 - y0) * fr)]
        if len(vis) >= 2:
            p.poly(vis + [(vis[-1][0], h), (0, h)], fill=rgba(tint(GREEN, 0.84)))
            p.line(vis, rgba(GREEN), 7)
            p.circ(vis[-1][0], vis[-1][1], 11, fill=rgba(GREEN))
    return canvas(w + 12, h + 4, cb)


def s_revenue(f, t):
    s, a, dy = trans(t, 35.2, 38.95)
    cx, cy = CX, 1010 + dy
    at = _at(cx, cy, 780, 520, s)
    put(f, revenue_card(), cx, cy, s, a)
    spr = revenue_chart(t)
    x, y = at(390, 375)
    put(f, spr, x, y, s, a)
    ps, pa = pop(t, 35.82, 0.34)
    x, y = at(620, 150)
    put(f, pill("SHORT-TERM", tint(PURPLE, 0.86), PURPLE, size=18, h=46), x, y - 60 * s, ps * s, pa * a)
    for k in range(3):
        ps, pa = pop(t, 37.7 + k * 0.18, 0.32, s0=0.2)
        x, y = at(520 + k * 70, 300 - k * 40)
        put(f, coin(26), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S10: the big problem — building easy, selling hard (39.0 - 45.35)
@lru_cache(None)
def problem_card():
    w, h = 800, 470

    def cb(p):
        for k, (title, ic, col) in enumerate([("Build software", "code", GREEN), ("Sell software", "users", ORANGE)]):
            y = 130 + k * 200
            tile(p, 100, y, 90, col, ic)
            p.text(168, y - 26, title, "bold", 38, rgba(INK), anchor="lm")
            p.rr((168, y + 22, 740, y + 50), 14, fill=rgba(SKEL))
    return card(w, h, 38, cb)


@lru_cache(None)
def level_pill(txt, col, tcol):
    return pill(txt, col, tcol, size=22, h=56)


def s_problem(f, t):
    s, a, dy = trans(t, 39.0, 45.35)
    cx, cy = CX, 1060 + dy
    at = _at(cx, cy, 800, 470, s)
    bs, ba = pop(t, 39.1, 0.34)
    ba *= 1 - smooth(prog(t, 40.15, 0.2))
    if ba > 0:
        put(f, big_num("But…", INK, 150), CX, 1000, bs, ba * a)
    ps, pa = pop(t, 40.3, 0.4, s0=0.3)
    shake = 8 * math.sin((t - 40.3) * 40) * (1 - prog(t, 40.3, 0.5)) if t > 40.3 else 0
    put(f, pill("BIG PROBLEM", YELLOW, DARK, size=26, h=70, icon_name="warn", icon_col=DARK), CX + shake, 700,
        ps, pa * a)
    a2 = a * prog(t, 41.05, 0.3)
    if a2 <= 0:
        return
    s2, _, _ = trans(t, 41.05, None)
    put(f, problem_card(), cx, cy, s2 * s, a2)
    fe = out_cubic(prog(t, 42.0, 0.6))  # easy: short fill
    if fe > 0:
        bw = 180 * fe
        x, y = at(168 + bw / 2, 166)
        put(f, bar_fill(bw, GREEN), x, y, s, a2)
    ps, pa = pop(t, 42.58, 0.34)
    x, y = at(650, 104)
    put(f, level_pill("EASY", tint(GREEN, 0.85), T_GREEN), x, y, ps * s, pa * a2)
    fh = out_cubic(prog(t, 43.75, 0.8))  # hard: long fill
    if fh > 0:
        bw = 560 * fh
        x, y = at(168 + bw / 2, 366)
        put(f, bar_fill(bw, ORANGE), x, y, s, a2)
    ps, pa = pop(t, 44.42, 0.36, s0=0.3)
    x, y = at(650, 304)
    put(f, level_pill("HARD", ORANGE, WHITE), x, y, ps * s, pa * a2)


# ------------------------------------------------------------------ S11: how to sell / get customers + next video (45.4 - 51.4)
@lru_cache(None)
def funnel_step(k):
    widths = [680, 540, 400]
    labels = ["Product", "Sell it", "Customers"]
    cols = [CYAN, PURPLE, GREEN]
    w, h = widths[k], 120

    def cb(p):
        inset = 40
        p.poly([(0, 0), (w, 0), (w - inset, h), (inset, h)], fill=rgba(tint(cols[k], 0.82)))
        p.text(w / 2, h / 2, labels[k], "bold", 38, rgba(INK), anchor="mm")
    return canvas(w, h, cb)


def s_sell(f, t):
    _, a, dy = trans(t, 45.4, 51.4)
    a_f = a * (1 - 0.7 * smooth(prog(t, 49.7, 0.35)))  # funnel dims when the "next video" card arrives
    ps, pa = pop(t, 45.55, 0.34)
    put(f, pill("HOW TO SELL?", WHITE, INK, size=24, h=62, icon_name="search", icon_col=BLUE, border=BORDER),
        CX, 700, ps, pa * a)
    for k, ts in enumerate([45.84, 46.66, 47.58]):
        ps, pa = pop(t, ts, 0.36)
        y = 850 + k * 145 + dy
        put(f, funnel_step(k), CX, y, ps, pa * a_f)
        if k > 0:
            qs, qa = pop(t, ts + 0.25, 0.32, s0=0.2)
            put(f, qmark(PURPLE if k == 1 else GREEN, 30), CX + [0, 300, 230][k], y, qs, qa * a_f)
    s2, a2, dy2 = trans(t, 49.7, 51.4, din=0.45, s0=0.7)
    if a2 > 0:
        put(f, next_card(), CX, 1040 + dy2, s2, a2 * a)


@lru_cache(None)
def next_card():
    w, h = 700, 330

    def cb(p):
        p.rr((40, 40, 170, 170), 36, fill=rgba(BLUE))
        icon(p, "play", 105, 105, 70, WHITE)
        p.text(210, 72, "NEXT VIDEO", "mono", 22, rgba(BLUE), anchor="lm", spacing=5)
        p.text(210, 120, "Day 2", "black", 56, rgba(INK), anchor="lm")
        p.text(40, 230, "How to sell & get customers", "bold", 36, rgba(INK), anchor="lm")
        p.rr((40, 270, 420, 290), 10, fill=rgba(SKEL))
    return card(w, h, 38, cb)


# ------------------------------------------------------------------ S12: outro — follow the journey (51.45 - 62)
def s_outro(f, t):
    t0 = 51.45
    s, a, dy = trans(t, t0, None, din=0.6, s0=0.5)
    bob = 5 * math.sin((t - t0) * 2.0) * prog(t, 52.5, 1.0)
    cy = 880 + dy + bob
    tr, k = 51.6, 0
    while tr < t and k < 8:
        pr = prog(t, tr, 1.4)
        if 0 < pr < 1:
            put(f, ring(170, CYAN if k % 2 == 0 else GREEN, 5), CX, cy, s * (0.98 + 0.5 * out_cubic(pr)),
                (1 - pr) * 0.45 * a)
        tr += 1.5
        k += 1
    put(f, logo_shadow(340), CX, cy, s, a * 0.9)
    put(f, logo(340), CX, cy, s, a)
    ps, pa = pop(t, 52.4, 0.38)
    put(f, pill("PLAN B JOURNEY · DAY 1", tint(BLUE, 0.88), BLUE, size=20, h=52), CX, 640, ps, pa)
    ps, pa = pop(t, 52.0, 0.4)
    put(f, handle_pill(42), CX, 1125, ps, pa)
    # coding + earning
    for lab, ic, bg, tc, x, ts in [("CODING", "code", tint(CYAN, 0.86), BLUE, CX - 140, 56.32),
                                   ("EARNING", "rupee", tint(GREEN, 0.85), T_GREEN, CX + 150, 57.36)]:
        ps, pa = pop(t, ts, 0.34)
        put(f, pill(lab, bg, tc, size=24, h=62, icon_name=ic, icon_col=tc), x, 1245, ps, pa)
    ps, pa = pop(t, 57.1, 0.3)
    put(f, plus_small(), CX + 5, 1245, ps * 0.7, pa)
    # follow button: pops on "follow karna", cursor clicks on "Follow karo"
    ps, pa = pop(t, 52.94, 0.42, s0=0.4)
    press = prog(t, 54.5, 0.2)
    kk = 1 - 0.07 * math.sin(press * math.pi)
    put(f, follow_btn(press > 0.5), CX, 1375, ps * kk, pa)
    rp = prog(t, 54.52, 0.6)
    if 0 < rp < 1:
        put(f, ring(100, BLUE, 5), CX, 1375, 0.9 + 1.0 * rp, (1 - rp) * 0.6)
    cm = out_cubic(prog(t, 53.9, 0.55))
    if cm > 0:
        leave = out_cubic(prog(t, 55.2, 0.5))
        cx = lerp(CX + 330, CX + 70, cm) + 120 * leave
        cyy = lerp(1590, 1395, cm) + 160 * leave
        put(f, cursor(), cx, cyy, 1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - leave))


SCENES = [
    (0.0, 4.5, s_day),
    (4.45, 7.7, s_work),
    (7.7, 11.1, s_income),
    (11.15, 14.65, s_idea),
    (14.7, 21.5, s_tool),
    (21.5, 26.45, s_price),
    (26.5, 29.3, s_better),
    (29.3, 35.2, s_build),
    (35.2, 39.0, s_revenue),
    (39.0, 45.4, s_problem),
    (45.4, 51.45, s_sell),
    (51.45, 62.1, s_outro),
]

# Sound effects: (time s, type, level dB, pan 0..1, extra) — only on real visual events
EVENTS = [
    (0.05, "shimmer", -2, 0.5, {}), (0.95, "pop", -3, 0.5, {"pitch": 0.75}),
    (4.42, "whoosh", 0, 0.5, {}), (5.68, "pop", -6, 0.6, {"pitch": 1.2}), (6.48, "click", -4, 0.6, {}),
    (7.12, "pop", -7, 0.6, {"pitch": 1.4}),
    (7.68, "whoosh", -1, 0.5, {}), (9.6, "pop", -8, 0.4, {"pitch": 1.3}), (9.92, "pop", -9, 0.6, {"pitch": 1.5}),
    (11.12, "whoosh", -1, 0.5, {}), (12.78, "click", -3, 0.65, {}), (13.46, "swipe", -4, 0.6, {}),
    (14.68, "whoosh", -1, 0.5, {}), (16.15, "click", -6, 0.5, {}), (19.5, "rise", -6, 0.5, {}),
    (21.48, "whoosh", -1, 0.5, {}), (23.45, "rise", -5, 0.5, {}), (25.1, "pop", -6, 0.5, {}),
    (26.48, "whoosh", -1, 0.5, {}), (27.86, "pop", -5, 0.65, {"pitch": 1.1}), (28.22, "chime", -6, 0.5, {}),
    (29.28, "whoosh", -1, 0.5, {}), (29.42, "pop", -7, 0.35, {}), (30.0, "pop", -7, 0.6, {"pitch": 1.15}),
    (32.18, "rise", -6, 0.6, {}), (33.74, "pop", -8, 0.5, {"pitch": 1.3}),
    (35.18, "whoosh", -1, 0.5, {}), (37.1, "rise", -6, 0.5, {}),
    (38.98, "whoosh", -1, 0.5, {}), (39.1, "pop", -9, 0.5, {"pitch": 0.9}), (40.3, "alert", -4, 0.5, {}), (42.58, "pop", -7, 0.4, {"pitch": 1.2}),
    (44.42, "swipe", -4, 0.6, {}),
    (45.38, "whoosh", -1, 0.5, {}), (49.7, "chime", -4, 0.5, {}),
    (51.42, "whoosh", -1, 0.5, {}), (51.5, "shimmer", 0, 0.5, {}), (52.94, "pop", -5, 0.5, {"pitch": 0.9}),
    (54.5, "click", -1, 0.55, {}), (56.32, "pop", -7, 0.4, {}), (57.36, "pop", -6, 0.6, {"pitch": 1.25}),
]
