"""DAY 3 — "Micro-SaaS idea: e-commerce report -> GST-ready file (GSTR-1)".

Voice: episodes/day03/voice.mp3 (93.07 s). Word timings from faster-whisper (episodes/day03/words.json); the
71-79 s part was re-transcribed alone because the first pass skipped it. Same look as Day 1 / Day 2.
Uses Ayush's own tool screenshot (episodes/day03/gst_tool.png) in the solution scene.
"""
import math
import os
from functools import lru_cache

from PIL import Image, ImageDraw

from gfx import (BLUE, BORDER, CYAN, DARK, DARK_YEL, GREEN, INK, INK2, LINE, MUTED, ORANGE, PANEL, PURPLE, SKEL,
                 T_GREEN, WHITE, YELLOW, canvas, card, clamp, icon, lerp, out_back, out_cubic, pop, prog, put, rgba,
                 smooth, text_w, tile, tint, trans)
from scenes import (CX, SM, bar_fill, big_num, check_sprite, cursor, follow_btn, handle_pill, header_label, logo,
                    logo_shadow, pill, ring)
from ep_day01 import _at, arrow_right, coin, day_card, plus_small, track_dot
from ep_day02 import avatar, big_cross, node, stage, stamp, title_two

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.path.join(ROOT, "episodes", "day03", "voice.mp3")
SHOT = os.path.join(ROOT, "episodes", "day03", "gst_tool.png")
VOICE_LEN = 93.07
TOTAL_LEN = 96.2
CAP_END = 93.6
HEADER = "COMPUTER HUB · PLAN B · DAY 3"

PHRASES = [
    ([("Day", 0.00, 1), ("3", 0.34, 1), ("of", 0.70, 0), ("building", 1.02, 0)], 1.32),
    ([("Plan", 1.32, 1), ("B", 1.72, 1), ("for", 2.00, 0), ("Software", 2.28, 1), ("Engineers.", 2.60, 1)], 3.20),
    ([("Aaj", 3.88, 0), ("main", 4.08, 0), ("aapko", 4.18, 0), ("ek", 4.62, 0), ("aisa", 4.92, 0)], 5.22),
    ([("real", 5.22, 1), ("Micro-SaaS", 5.72, 1), ("idea", 6.32, 1), ("bata", 6.60, 0), ("raha", 6.82, 0),
      ("hoon,", 7.02, 0)], 7.30),
    ([("jise", 7.66, 0), ("aap", 7.80, 0), ("AI", 8.14, 1), ("ki", 8.54, 0), ("madad", 8.70, 0), ("se", 8.92, 0)], 9.20),
    ([("zero", 9.20, 1), ("cost", 9.62, 1), ("mein", 9.96, 0), ("bana", 10.06, 0), ("sakte", 10.26, 0),
      ("ho,", 10.56, 0)], 10.62),
    ([("aur", 11.12, 0), ("iske", 11.22, 0), ("liye", 11.48, 0), ("market", 11.64, 0), ("mein", 12.20, 0)], 12.36),
    ([("Paying", 12.36, 1), ("Customers", 12.78, 1), ("pehle", 13.52, 0), ("se", 13.80, 0)], 14.00),
    ([("taiyaar", 14.00, 1), ("baithe", 14.40, 0), ("hain!", 14.62, 0)], 14.84),
    ([("Bharat", 15.44, 0), ("mein", 15.78, 0), ("lakhon", 15.98, 1), ("log", 16.50, 0)], 16.78),
    ([("Amazon,", 16.78, 1), ("Flipkart", 17.64, 1), ("aur", 18.12, 0), ("Meesho", 18.38, 1)], 18.70),
    ([("par", 18.70, 0), ("selling", 18.90, 1), ("kar", 19.24, 0), ("rahe", 19.38, 0), ("hain,", 19.60, 0)], 19.66),
    ([("lekin", 20.26, 0), ("har", 20.46, 0), ("mahine", 20.78, 1), ("unki", 21.18, 0)], 21.50),
    ([("sabse", 21.50, 0), ("badi", 22.04, 0), ("sirdardi", 22.40, 1), ("hoti", 22.82, 0), ("hai —", 23.14, 0)], 23.38),
    ([("GSTR-1", 23.68, 1), ("file", 24.76, 0), ("karna!", 24.98, 0)], 25.26),
    ([("E-commerce", 25.94, 0), ("portals", 27.24, 0), ("se", 27.66, 0), ("jo", 27.92, 0)], 28.00),
    ([("sales", 28.00, 1), ("report", 28.38, 1), ("download", 28.68, 0), ("hoti", 29.08, 0), ("hai,", 29.36, 0)], 29.52),
    ([("woh", 29.88, 0), ("sarkari", 30.00, 0), ("GST", 30.50, 1), ("portal", 30.94, 1)], 31.40),
    ([("seedhe", 31.40, 0), ("accept", 31.74, 0), ("nahi", 32.12, 1), ("karta.", 32.32, 0)], 32.48),
    ([("Chhote", 33.18, 0), ("sellers", 33.48, 0), ("na", 33.94, 0), ("toh", 34.16, 0)], 34.28),
    ([("har", 34.28, 0), ("mahine", 34.54, 0), ("mehenge", 34.98, 1), ("CA", 35.32, 1), ("ka", 35.70, 0),
      ("kharcha", 35.88, 0)], 36.20),
    ([("utha", 36.20, 0), ("sakte", 36.40, 0), ("hain,", 36.74, 0)], 36.88),
    ([("na", 37.32, 0), ("hi", 37.50, 0), ("unhe", 37.60, 0), ("ghanton", 37.88, 1), ("Excel", 38.38, 1),
      ("mein", 38.84, 0)], 39.04),
    ([("data", 39.04, 0), ("saaf", 39.48, 1), ("karna", 39.64, 0), ("aata", 39.94, 0), ("hai.", 40.18, 0)], 40.22),
    ([("Isi", 40.80, 0), ("problem", 41.04, 1), ("ko", 41.44, 0), ("solve", 41.60, 1), ("karne", 41.88, 0),
      ("ke", 42.14, 0), ("liye", 42.34, 0)], 42.52),
    ([("aap", 42.52, 0), ("ek", 42.86, 0), ("simple", 42.98, 1), ("web", 43.52, 1), ("tool", 43.84, 1)], 44.00),
    ([("bana", 44.00, 0), ("sakte", 44.20, 0), ("ho!", 44.52, 0)], 44.64),
    ([("Yeh", 45.12, 0), ("tool", 45.26, 0), ("kisi", 45.58, 0), ("bhi", 45.94, 0)], 46.10),
    ([("e-commerce", 46.10, 0), ("report", 46.52, 1), ("ko", 47.02, 0)], 47.26),
    ([("sirf", 47.26, 0), ("ek", 47.76, 1), ("click", 47.96, 1), ("mein", 48.24, 0)], 48.50),
    ([("GST", 48.76, 1), ("compliant", 49.28, 1), ("Excel", 49.76, 1), ("ya", 50.26, 0), ("JSON", 50.58, 1),
      ("file", 51.04, 0), ("mein", 51.32, 0)], 51.42),
    ([("convert", 51.42, 1), ("kar", 51.86, 0), ("deta", 52.02, 0), ("hai.", 52.26, 0)], 52.30),
    ([("Ise", 52.82, 0), ("aap", 53.04, 0), ("Claude", 53.28, 1), ("aur", 53.76, 0), ("Cursor", 53.96, 1)], 54.38),
    ([("ki", 54.38, 0), ("madad", 54.56, 0), ("se", 54.76, 0), ("kuch", 55.18, 0), ("hi", 55.36, 0),
      ("ghanton", 55.48, 1), ("mein", 55.74, 0)], 55.90),
    ([("bana", 55.90, 0), ("sakte", 56.08, 0), ("ho,", 56.42, 0)], 56.60),
    ([("aur", 56.94, 0), ("Vercel", 57.10, 1), ("ya", 57.64, 0), ("onrender.com", 57.90, 1), ("par", 58.94, 0)], 59.26),
    ([("muft", 59.26, 1), ("mein", 59.58, 0), ("deploy", 59.70, 1), ("kar", 60.16, 0), ("sakte", 60.28, 0),
      ("ho.", 60.56, 0)], 60.60),
    ([("Business", 61.16, 1), ("model", 61.54, 1), ("bilkul", 61.98, 0), ("seedha", 62.40, 0), ("hai —", 62.64, 0)], 62.80),
    ([("shuruaati", 63.34, 0), ("sellers", 63.78, 0), ("ko", 64.12, 0)], 64.40),
    ([("30", 64.40, 1), ("din", 64.74, 1), ("ka", 64.92, 0), ("free", 65.12, 1), ("trial", 65.46, 1), ("do,", 65.72, 0)], 65.84),
    ([("aur", 66.22, 0), ("uske", 66.32, 0), ("baad", 66.58, 0), ("sirf", 66.82, 0)], 67.36),
    ([("₹299", 67.36, 1), ("se", 68.20, 0), ("₹499", 68.58, 1), ("ka", 69.74, 0)], 69.88),
    ([("monthly", 69.88, 1), ("subscription.", 70.34, 1)], 70.90),
    ([("Agar", 71.82, 0), ("sirf", 72.16, 0), ("100", 72.64, 1), ("active", 72.98, 1), ("sellers", 73.32, 1)], 73.62),
    ([("bhi", 73.62, 0), ("jud", 73.80, 0), ("gaye,", 73.96, 0)], 74.44),
    ([("toh", 74.44, 0), ("aapki", 74.62, 0), ("mahine", 74.98, 0), ("ki", 75.34, 0)], 75.56),
    ([("₹30", 75.56, 1), ("se", 76.00, 0), ("50", 76.22, 1), ("hazaar", 76.74, 1), ("rupaye", 77.12, 0),
      ("ki", 77.36, 0)], 77.56),
    ([("fix", 77.56, 0), ("passive", 78.04, 1), ("income", 78.42, 1), ("shuru!", 78.78, 0)], 79.12),
    ([("Agar", 79.72, 0), ("aapko", 79.94, 0), ("is", 80.18, 0), ("tool", 80.32, 0), ("ko", 80.54, 0)], 80.74),
    ([("step-by-step", 80.74, 1), ("banane", 81.50, 0), ("ki", 81.88, 0)], 82.06),
    ([("poori", 82.06, 0), ("guide", 82.50, 1), ("aur", 82.92, 0), ("architecture", 83.12, 1), ("chahiye,", 83.70, 0)], 84.34),
    ([("toh", 84.34, 0), ("comment", 84.44, 1), ("mein", 84.78, 0), ("likho", 84.90, 0), ("'GST',", 85.16, 1)], 85.84),
    ([("main", 86.30, 0), ("seedhe", 86.38, 0), ("aapke", 86.86, 0), ("DM", 87.10, 1), ("mein", 87.34, 0),
      ("bhej", 87.48, 0), ("dunga!", 87.68, 0)], 87.92),
    ([("aur", 88.42, 0), ("apne", 88.52, 0), ("software", 88.72, 1), ("career", 89.24, 1), ("ka", 89.60, 0)], 89.72),
    ([("solid", 89.72, 0), ("Plan", 90.28, 1), ("B", 90.64, 1), ("banane", 90.86, 0), ("ke", 91.16, 0), ("liye,", 91.34, 0)], 91.52),
    ([("abhi", 91.52, 0), ("Follow", 92.02, 1), ("kar", 92.28, 0), ("lijiye!", 92.46, 0)], 92.90),
]


# ------------------------------------------------------------------ shared bits
@lru_cache(None)
def doc(label, sub, col, w=230, h=260):
    def cb(p):
        p.poly([(4, 4), (w - 60, 4), (w - 4, 60), (w - 4, h - 4), (4, h - 4)], fill=rgba(WHITE),
               outline=rgba(tint(col, 0.4)), width=4)
        p.poly([(w - 60, 4), (w - 60, 60), (w - 4, 60)], fill=rgba(tint(col, 0.7)))
        p.rr((22, 30, 70, 78), 12, fill=rgba(col))
        for k, ww in enumerate([150, 120, 160, 100]):
            p.rr((22, 100 + k * 26, 22 + ww, 112 + k * 26), 6, fill=rgba(tint(col, 0.75)))
        p.text(w / 2, h - 50, label, "bold", 30, rgba(INK), anchor="mm")
        p.text(w / 2, h - 20, sub, "mono", 16, rgba(MUTED), anchor="mm", spacing=2)
    return canvas(w, h, cb)


@lru_cache(None)
def num_text(txt, col=INK, size=120):
    w = int(text_w(txt, "black", size) + 24)
    return canvas(w, int(size * 1.3), lambda p: p.text(w / 2, size * 0.66, txt, "black", size, rgba(col), anchor="mm"))


@lru_cache(None)
def label_pill(txt, bg, fg, ic=None, size=20, h=52):
    return pill(txt, bg, fg, size=size, h=h, icon_name=ic, icon_col=fg)


# ------------------------------------------------------------------ S1: DAY 3 calendar (0 - 3.8)
def s_day(f, t):
    s, a, dy = trans(t, 0.02, 3.8, din=0.5, s0=0.6)
    cx, cy = CX, 960 + dy
    at = _at(cx, cy, 560, 600, s)
    put(f, day_card(), cx, cy, s, a)
    ps, pa = pop(t, 0.34, 0.45, s0=0.2)
    x, y = at(280, 300)
    put(f, big_num("3", INK, 240), x, y, ps * s, pa * a)
    for k in range(5):
        ps, pa = pop(t, 0.8 + k * 0.08, 0.3)
        x, y = at(170 + k * 55, 430)
        put(f, track_dot(k < 3), x, y, ps * s, pa * a)
        if k == 2:
            rp = prog(t, 1.3, 0.8)
            if 0 < rp < 1:
                put(f, ring(16, CYAN, 3), x, y, s * (1 + 1.2 * rp), a * (1 - rp))
    ps, pa = pop(t, 1.32, 0.36)
    x, y = at(280, 520)
    put(f, title_two("Building ", "Plan B", 40, BLUE, "bold"), x, y, ps * s, pa * a)
    ps, pa = pop(t, 2.28, 0.36)
    put(f, pill("FOR SOFTWARE ENGINEERS", WHITE, INK, size=22, h=60, icon_name="code", icon_col=CYAN, border=BORDER),
        CX, 1335 + dy, ps * s, pa * a)


# ------------------------------------------------------------------ S2: today's idea — real Micro-SaaS (3.8 - 15.0)
@lru_cache(None)
def idea_card():
    w, h = 800, 640

    def cb(p):
        header_label(p, w, 56, "TODAY'S IDEA", BLUE, 22, 6)
        p.line([(50, 400), (w - 50, 400)], rgba(LINE), 2, caps=False)
        p.text(60, 448, "Paying customers", "bold", 34, rgba(INK), anchor="lm")
    return card(w, h, 38, cb)


@lru_cache(None)
def zero_cost():
    w, h = 300, 150

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 30, fill=rgba(tint(GREEN, 0.88)), outline=rgba(tint(GREEN, 0.5)), width=3)
        p.text(w / 2, 62, "₹0", "black", 84, rgba(GREEN), anchor="mm")
        p.text(w / 2, 124, "BUILD COST", "mono", 18, rgba(T_GREEN), anchor="mm", spacing=3)
    return canvas(w, h, cb)


@lru_cache(None)
def ai_box():
    w, h = 300, 150

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 30, fill=rgba(tint(PURPLE, 0.9)), outline=rgba(tint(PURPLE, 0.5)), width=3)
        p.rr((24, 33, 108, 117), 22, fill=rgba(PURPLE))
        icon(p, "spark", 66, 75, 50, WHITE, bg=PURPLE)
        p.text(128, 62, "Built", "bold", 32, rgba(INK), anchor="lm")
        p.text(128, 98, "with AI", "bold", 32, rgba(PURPLE), anchor="lm")
    return canvas(w, h, cb)


def s_idea(f, t):
    stage(f, t, "REAL MICRO-SAAS IDEA", 3.9, 15.0, YELLOW, DARK, "bolt")
    s, a, dy = trans(t, 4.6, 15.0)
    cx, cy = CX, 1080 + dy
    at = _at(cx, cy, 800, 640, s)
    put(f, idea_card(), cx, cy, s, a)
    ps, pa = pop(t, 5.72, 0.45, s0=0.3)
    x, y = at(400, 150)
    put(f, title_two("Micro-", "SaaS", 100, BLUE), x, y, ps * s, pa * a)
    ps, pa = pop(t, 8.14, 0.38)
    x, y = at(220, 310)
    put(f, ai_box(), x, y, ps * s, pa * a)
    ps, pa = pop(t, 9.2, 0.45, s0=0.3)
    bump = 1 + 0.05 * math.sin(math.pi * prog(t, 9.62, 0.35))
    x, y = at(580, 310)
    put(f, zero_cost(), x, y, ps * s * bump, pa * a)
    for k, col in enumerate([CYAN, PURPLE, DARK_YEL, GREEN]):
        ps, pa = pop(t, 12.36 + k * 0.14, 0.34)
        x, y = at(110 + k * 110, 545)
        put(f, avatar(col), x, y, ps * s * 0.75, pa * a)
        cs, ca = pop(t, 12.9 + k * 0.14, 0.3, s0=0.2)
        put(f, coin(20), x + 36 * s, y - 36 * s, cs * s, ca * a)
    ps, pa = pop(t, 14.0, 0.38, s0=0.3)
    x, y = at(640, 545)
    put(f, label_pill("READY TO PAY", GREEN, WHITE, "check", 20, 56), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S3: lakhs of sellers in India (15.0 - 19.95)
@lru_cache(None)
def sellers_card():
    w, h = 800, 560

    def cb(p):
        header_label(p, w, 56, "ONLINE SELLERS IN INDIA", BLUE, 22, 5)
        p.line([(50, 400), (w - 50, 400)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


@lru_cache(None)
def market_pill(name):
    return pill(name, WHITE, INK, kind="bold", size=30, spacing=0, h=70, border=BORDER)


def s_sellers(f, t):
    s, a, dy = trans(t, 15.0, 19.95)
    cx, cy = CX, 1010 + dy
    at = _at(cx, cy, 800, 560, s)
    put(f, sellers_card(), cx, cy, s, a)
    cols = [CYAN, PURPLE, DARK_YEL, GREEN, BLUE]
    for k in range(14):  # "lakhon log" — the grid fills fast
        r, c = divmod(k, 7)
        ps, pa = pop(t, 15.98 + k * 0.05, 0.3)
        x, y = at(110 + c * 97, 160 + r * 120)
        put(f, avatar(cols[k % 5]), x, y, ps * s * 0.72, pa * a)
    ps, pa = pop(t, 16.2, 0.36)
    x, y = at(400, 345)
    put(f, label_pill("LAKHS OF SELLERS", INK, WHITE, "users", 20, 54), x, y, ps * s, pa * a)
    for k, (nm, ts) in enumerate([("Amazon", 16.78), ("Flipkart", 17.64), ("Meesho", 18.38)]):
        ps, pa = pop(t, ts, 0.36)
        x, y = at(150 + k * 250, 480)
        put(f, market_pill(nm), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S4: monthly headache — GSTR-1 (20.0 - 25.6)
@lru_cache(None)
def gstr_doc():
    w, h = 360, 440

    def cb(p):
        p.poly([(4, 4), (w - 80, 4), (w - 4, 80), (w - 4, h - 4), (4, h - 4)], fill=rgba(WHITE),
               outline=rgba(tint(ORANGE, 0.4)), width=5)
        p.poly([(w - 80, 4), (w - 80, 80), (w - 4, 80)], fill=rgba(tint(ORANGE, 0.7)))
        p.text(w / 2 - 20, 130, "GSTR-1", "black", 70, rgba(INK), anchor="mm")
        p.text(w / 2 - 20, 196, "MONTHLY RETURN", "mono", 18, rgba(MUTED), anchor="mm", spacing=3)
        for k, ww in enumerate([260, 220, 270, 180, 240]):
            p.rr((40, 250 + k * 34, 40 + ww, 264 + k * 34), 7, fill=rgba(SKEL))
    return canvas(w, h, cb)


@lru_cache(None)
def month_card():
    w, h = 250, 250

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 34, fill=rgba(WHITE), outline=rgba(BORDER), width=3)
        p.rr((2, 2, w - 2, 70), 34, fill=rgba(ORANGE))
        p.rect((2, 40, w - 2, 70), fill=rgba(ORANGE))
        p.text(w / 2, 38, "EVERY", "mono", 24, rgba(WHITE), anchor="mm", spacing=6)
        p.text(w / 2, 150, "MONTH", "black", 46, rgba(INK), anchor="mm")
        p.text(w / 2, 205, "again & again", "semi", 26, rgba(MUTED), anchor="mm")
    return canvas(w, h, cb)


def s_headache(f, t):
    _, a, dy = trans(t, 20.0, 25.6)
    ps, pa = pop(t, 20.7, 0.38)
    rot = 1 + 0.03 * math.sin((t - 20.7) * 5) * (t > 21.1)
    put(f, month_card(), CX - 215, 960 + dy, ps * rot, pa * a)
    ps, pa = pop(t, 22.4, 0.38, s0=0.3)
    shake = 7 * math.sin((t - 22.4) * 40) * (1 - prog(t, 22.4, 0.5)) if t > 22.4 else 0
    put(f, label_pill("#1 HEADACHE", ORANGE, WHITE, "warn", 24, 66), CX - 215 + shake, 1170 + dy, ps, pa * a)
    ps, pa = pop(t, 23.62, 0.45, s0=0.3)
    put(f, gstr_doc(), CX + 175, 1020 + dy, ps, pa * a)
    ps, pa = pop(t, 24.76, 0.3, s0=0.2)
    put(f, label_pill("FILE IT", tint(ORANGE, 0.85), (190, 80, 0), "clock", 18, 48), CX + 175, 1290 + dy, ps, pa * a)


# ------------------------------------------------------------------ S5: report not accepted by GST portal (25.7 - 32.75)
@lru_cache(None)
def portal_box():
    w, h = 300, 260

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 34, fill=rgba(WHITE), outline=rgba(BORDER), width=3)
        p.rr((w / 2 - 54, 30, w / 2 + 54, 138), 30, fill=rgba(BLUE))
        icon(p, "globe", w / 2, 84, 70, WHITE, bg=BLUE)
        p.text(w / 2, 180, "GST Portal", "bold", 34, rgba(INK), anchor="mm")
        p.text(w / 2, 222, "government", "mono", 18, rgba(MUTED), anchor="mm", spacing=3)
    return canvas(w, h, cb)


def s_reject(f, t):
    stage(f, t, "THE PROBLEM", 25.9, 33.15, ORANGE, WHITE, "warn")
    _, a, dy = trans(t, 25.9, 33.15)
    y = 1010 + dy
    ps, pa = pop(t, 27.24, 0.38)
    put(f, label_pill("E-COMMERCE PORTAL", WHITE, INK, "users", 18, 48, ), CX - 220, 815 + dy, ps, pa * a)
    ps, pa = pop(t, 28.0, 0.4)
    put(f, doc("Sales Report", "CSV / EXCEL", GREEN), CX - 220, y, ps, pa * a)
    ap = out_cubic(prog(t, 29.9, 0.5))
    if ap > 0:
        put(f, arrow_right(MUTED, 150), CX, y, 1.0, a, sx=max(ap, 0.02))
    ps, pa = pop(t, 30.5, 0.4)
    put(f, portal_box(), CX + 230, y, ps, pa * a)
    ps, pa = pop(t, 32.12, 0.42, s0=0.2)
    put(f, big_cross(), CX, y, ps * 0.6, pa * a)
    ps, pa = pop(t, 32.2, 0.4, s0=2.0)
    put(f, stamp("NOT ACCEPTED", ORANGE), CX, y + 245, ps * 0.62, pa * a)


# ------------------------------------------------------------------ S6: small sellers can't afford a CA / clean Excel (32.9 - 40.6)
@lru_cache(None)
def pain_row(k):
    title, sub, ic, col = [("CA fees every month", "too expensive", "rupee", ORANGE),
                           ("Hours of Excel cleanup", "hard + slow", "clock", PURPLE)][k]
    w, h = 800, 220

    def cb(p):
        tile(p, 100, h / 2, 120, col, ic)
        p.text(190, h / 2 - 26, title, "bold", 40, rgba(INK), anchor="lm")
        p.text(191, h / 2 + 28, sub, "semi", 28, rgba(MUTED), anchor="lm")
    return card(w, h, 36, cb)


@lru_cache(None)
def messy_grid():
    w, h = 300, 150

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), 14, fill=rgba(WHITE), outline=rgba(GREEN), width=3)
        for r in range(5):
            for c in range(5):
                x0, y0 = 10 + c * 56, 10 + r * 27
                bad = (r * 7 + c * 3) % 5 == 0
                p.rect((x0, y0, x0 + 50, y0 + 21), fill=rgba(tint(ORANGE, 0.6) if bad else tint(GREEN, 0.86)))
    return canvas(w, h, cb)


def s_pain(f, t):
    stage(f, t, "SMALL SELLERS CAN'T", 33.18, 40.6, INK, WHITE, "users")
    for k, (t0, tx) in enumerate([(34.6, 35.88), (37.6, 38.38)]):
        s, a, dy = trans(t, t0, 40.6)
        y = 900 + k * 290 + dy
        put(f, pain_row(k), CX, y, s, a)
        cs, ca = pop(t, tx, 0.36, s0=0.2)
        put(f, big_cross(), CX + 330 * s, y - 70 * s, cs * 0.32, ca * a)
    ps, pa = pop(t, 38.6, 0.4)
    _, a2, _ = trans(t, 38.6, 40.6)
    put(f, messy_grid(), CX + 210, 1400, ps, pa * a2)
    ps, pa = pop(t, 39.48, 0.34)
    put(f, label_pill("DATA CLEANING?!", tint(PURPLE, 0.86), PURPLE, "search", 18, 48), CX - 170, 1400, ps, pa * a2)


# ------------------------------------------------------------------ S7: the solution — your GST tool (40.7 - 52.75)
SHOT_CROP = (205, 0, 1255, 535)   # header + "Upload your reports folder" + buttons (zoomed)
SHOT_W = 780
BTN_UPLOAD = (618 - 205, 391)     # "Upload & process" centre in the crop
BRW_W, BRW_H = 840, 74 + 20 + int(SHOT_W * 535 / 1050) + 26


@lru_cache(None)
def tool_browser():
    im = Image.open(SHOT).convert("RGBA").crop(SHOT_CROP)
    sh = int(SHOT_W * im.height / im.width)
    im = im.resize((SHOT_W, sh), Image.LANCZOS)
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=16, fill=255)
    im.putalpha(mask)

    def cb(p):
        p.rr((0, 0, BRW_W - 1, 74), 36, fill=rgba(PANEL))
        p.rect((0, 40, BRW_W - 1, 74), fill=rgba(PANEL))
        p.line([(0, 74), (BRW_W, 74)], rgba(LINE), 2, caps=False)
        for k, c in enumerate([(255, 96, 92), (255, 190, 50), (40, 200, 70)]):
            p.circ(40 + k * 28, 37, 9, fill=rgba(c))
        p.rr((140, 17, 700, 57), 20, fill=rgba(WHITE), outline=rgba(LINE), width=2)
        icon(p, "globe", 166, 37, 22, MUTED)
        p.text(188, 37, "your-gst-tool.app", "monor", 20, rgba(INK2), anchor="lm")
    out = card(BRW_W, BRW_H, 36, cb)
    out.alpha_composite(im, (SM + 30, SM + 94))
    return out


def btn_pos(cx, cy, s):
    """Frame position of the 'Upload & process' button inside the browser card."""
    k = SHOT_W / (SHOT_CROP[2] - SHOT_CROP[0])
    rx = 30 + BTN_UPLOAD[0] * k
    ry = 94 + BTN_UPLOAD[1] * k
    return cx + (rx - BRW_W / 2) * s, cy + (ry - BRW_H / 2) * s


@lru_cache(None)
def out_file(kind):
    col, name, ic = (GREEN, "Excel", "chart") if kind == "x" else (PURPLE, "JSON", "code")
    w, h = 300, 130

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 30, fill=rgba(WHITE), outline=rgba(col), width=4)
        p.rr((22, 25, 102, 105), 22, fill=rgba(col))
        icon(p, ic, 62, 65, 48, WHITE, bg=col)
        p.text(124, 50, name, "black", 40, rgba(INK), anchor="lm")
        p.text(125, 92, "GST READY", "mono", 18, rgba(col), anchor="lm", spacing=3)
    return canvas(w, h, cb)


@lru_cache(None)
def down_arrow():
    def cb(p):
        p.line([(30, 6), (30, 70)], rgba(BLUE), 10)
        p.poly([(10, 62), (30, 92), (50, 62)], fill=rgba(BLUE))
    return canvas(60, 96, cb)


def s_solution(f, t):
    stage(f, t, "THE SOLUTION", 40.8, 52.75, GREEN, WHITE, "check")
    s, a, dy = trans(t, 42.4, 52.75, din=0.5)
    cx, cy = CX, 1010 + dy
    put(f, tool_browser(), cx, cy, s, a)
    top, bot = cy - BRW_H / 2 * s, cy + BRW_H / 2 * s
    ps, pa = pop(t, 43.0, 0.36)
    put(f, label_pill("SIMPLE WEB TOOL", tint(BLUE, 0.88), BLUE, "globe", 18, 48), CX + 250 * s, top - 26 * s,
        ps * s, pa * a)
    bx, by = btn_pos(cx, cy, s)
    # the e-commerce report flies into the upload button
    fp = prog(t, 46.3, 1.0)
    if 0 < fp < 1:
        e = out_cubic(fp)
        put(f, doc("Report", "AMAZON / FLIPKART", CYAN), lerp(CX - 300, bx, e),
            lerp(1360, by, e) - 120 * math.sin(math.pi * e), 0.75 - 0.55 * e, a * (1 - smooth(prog(t, 47.0, 0.3))))
    # cursor clicks "Upload & process" on "click"
    cm = out_cubic(prog(t, 47.1, 0.6))
    press = prog(t, 47.96, 0.2)
    if cm > 0:
        leave = out_cubic(prog(t, 48.9, 0.5))
        put(f, cursor(), lerp(bx + 260, bx + 16, cm) + 140 * leave, lerp(by + 300, by + 18, cm) + 140 * leave,
            1.15 - 0.12 * math.sin(press * math.pi), clamp(cm * 3) * (1 - leave) * a)
    rp = prog(t, 47.98, 0.6)
    if 0 < rp < 1:
        put(f, ring(70, BLUE, 5), bx, by, 0.6 + 1.2 * rp, (1 - rp) * 0.7 * a)
    ps, pa = pop(t, 48.76, 0.36)
    put(f, label_pill("GST COMPLIANT", GREEN, WHITE, "check", 22, 58), CX, bot + 42, ps, pa * a)
    for kind, ts, x in [("x", 49.76, CX - 175), ("j", 50.58, CX + 175)]:
        ps, pa = pop(t, ts, 0.4, s0=0.3)
        put(f, out_file(kind), x, bot + 160, ps, pa * a)
    ps, pa = pop(t, 51.42, 0.38, s0=0.3)
    put(f, label_pill("CONVERTED", tint(GREEN, 0.85), T_GREEN, "check", 18, 46), CX - 250 * s, top - 26 * s,
        ps * s, pa * a)


# ------------------------------------------------------------------ S8: build with Claude + Cursor, deploy free (52.8 - 60.7)
@lru_cache(None)
def deploy_card():
    w, h = 820, 620

    def cb(p):
        header_label(p, w, 56, "BUILD + DEPLOY", BLUE, 22, 6)
        p.line([(50, 330), (w - 50, 330)], rgba(LINE), 2, caps=False)
        p.text(60, 380, "Deploy on", "semi", 30, rgba(INK2), anchor="lm")
    return card(w, h, 38, cb)


@lru_cache(None)
def host_chip(name):
    return pill(name, WHITE, INK, kind="bold", size=30, spacing=0, h=74, icon_name="globe", icon_col=BLUE, border=BORDER)


@lru_cache(None)
def hours_box():
    return node("Few hours", "clock", DARK_YEL)


def s_deploy(f, t):
    s, a, dy = trans(t, 52.8, 60.7)
    cx, cy = CX, 1030 + dy
    at = _at(cx, cy, 820, 620, s)
    put(f, deploy_card(), cx, cy, s, a)
    for nm, ic, col, rx, ts in [("Claude", "spark", PURPLE, 140, 53.28), ("Cursor", "code", INK, 400, 53.96)]:
        ps, pa = pop(t, ts, 0.36)
        x, y = at(rx, 200)
        put(f, node(nm, ic, col), x, y, ps * s * 0.95, pa * a)
    ps, pa = pop(t, 53.7, 0.3)
    x, y = at(270, 200)
    put(f, plus_small(), x, y, ps * s, pa * a)
    ap = out_cubic(prog(t, 55.1, 0.35))
    if ap > 0:
        x, y = at(540, 200)
        put(f, arrow_right(GREEN, 80), x, y, s, a, sx=max(ap, 0.02))
    ps, pa = pop(t, 55.48, 0.38)
    x, y = at(680, 200)
    put(f, hours_box(), x, y, ps * s * 0.95, pa * a)
    for nm, rx, ts in [("Vercel", 230, 57.10), ("onrender.com", 560, 57.90)]:
        ps, pa = pop(t, ts, 0.36)
        x, y = at(rx, 460)
        put(f, host_chip(nm), x, y, ps * s, pa * a)
    ps, pa = pop(t, 59.26, 0.45, s0=0.3)
    x, y = at(400, 560)
    put(f, label_pill("FREE  ·  ₹0 HOSTING", GREEN, WHITE, "check", 22, 60), x, y, ps * s, pa * a)
    ps, pa = pop(t, 59.7, 0.34)
    x, y = at(640, 380)
    put(f, label_pill("DEPLOYED", tint(GREEN, 0.85), T_GREEN, "up", 18, 46), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S9: business model (60.8 - 71.0)
@lru_cache(None)
def trial_card():
    w, h = 800, 280

    def cb(p):
        p.rr((40, 50, 220, 230), 40, fill=rgba(tint(GREEN, 0.86)))
        p.text(130, 128, "30", "black", 96, rgba(GREEN), anchor="mm")
        p.text(130, 196, "DAYS", "mono", 22, rgba(T_GREEN), anchor="mm", spacing=6)
        p.text(260, 118, "Free Trial", "black", 64, rgba(INK), anchor="lm")
        p.text(262, 184, "for early sellers", "semi", 30, rgba(MUTED), anchor="lm")
    return card(w, h, 36, cb)


@lru_cache(None)
def price_card():
    w, h = 800, 300

    def cb(p):
        p.text(60, 60, "THEN MONTHLY", "mono", 22, rgba(BLUE), anchor="lm", spacing=5)
        p.text(w - 60, 240, "/ month", "bold", 40, rgba(MUTED), anchor="rm")
    return card(w, h, 36, cb)


def s_model(f, t):
    stage(f, t, "BUSINESS MODEL", 61.1, 71.0, BLUE, WHITE, "rupee")
    s, a, dy = trans(t, 64.3, 71.0)
    put(f, trial_card(), CX, 900 + dy, s, a)
    s2, a2, dy2 = trans(t, 66.6, 71.0)
    cy = 1225 + dy2
    put(f, price_card(), CX, cy, s2, a2)
    ps, pa = pop(t, 67.36, 0.42, s0=0.3)
    put(f, num_text("₹299", INK, 110), CX - 210, cy + 5, ps * s2, pa * a2)
    ps, pa = pop(t, 68.2, 0.3)
    put(f, num_text("–", MUTED, 90), CX - 20, cy + 5, ps * s2, pa * a2)
    ps, pa = pop(t, 68.58, 0.42, s0=0.3)
    put(f, num_text("₹499", BLUE, 110), CX + 170, cy + 5, ps * s2, pa * a2)
    ps, pa = pop(t, 70.34, 0.34)
    put(f, label_pill("SUBSCRIPTION", tint(PURPLE, 0.86), PURPLE, "clock", 18, 46), CX - 230, cy + 100, ps, pa * a2)


# ------------------------------------------------------------------ S10: 100 sellers = ₹30K-₹50K / month (71.1 - 79.3)
@lru_cache(None)
def math_card():
    w, h = 800, 640

    def cb(p):
        header_label(p, w, 56, "THE MATH", BLUE, 22, 6)
        p.line([(50, 330), (w - 50, 330)], rgba(LINE), 2, caps=False)
        p.text(w / 2, 372, "MONTHLY INCOME", "mono", 22, rgba(MUTED), anchor="mm", spacing=5)
    return card(w, h, 38, cb)


@lru_cache(None)
def k_range(a_k, b_k):
    return num_text(f"₹{a_k}K – ₹{b_k}K", GREEN, 96)


def s_math(f, t):
    s, a, dy = trans(t, 71.1, 79.3)
    cx, cy = CX, 1040 + dy
    at = _at(cx, cy, 800, 640, s)
    put(f, math_card(), cx, cy, s, a)
    cnt = int(round(100 * smooth(prog(t, 72.4, 0.9))))
    if t >= 72.3:
        ps, _ = pop(t, 72.4, 0.4, s0=0.6)
        x, y = at(230, 190)
        put(f, num_text(str(cnt), INK, 130), x, y, ps * s, a)
    ps, pa = pop(t, 73.32, 0.36)
    x, y = at(230, 290)
    put(f, label_pill("ACTIVE SELLERS", tint(CYAN, 0.86), BLUE, "users", 18, 46), x, y, ps * s, pa * a)
    ps, pa = pop(t, 73.9, 0.36)
    x, y = at(570, 200)
    put(f, num_text("× ₹299–499", INK2, 54), x, y, ps * s, pa * a)
    # result counts up: ₹30K - ₹50K
    rv = smooth(prog(t, 75.5, 1.3))
    if t >= 75.45:
        lo, hi = int(round(30 * rv)), int(round(50 * rv))
        ps, _ = pop(t, 75.5, 0.4, s0=0.6)
        bump = 1 + 0.05 * math.sin(math.pi * prog(t, 76.8, 0.35))
        x, y = at(400, 460)
        put(f, k_range(lo, hi), x, y, ps * s * bump, a)
    ps, pa = pop(t, 78.04, 0.4, s0=0.3)
    x, y = at(400, 570)
    put(f, label_pill("PASSIVE INCOME", GREEN, WHITE, "trend", 22, 60), x, y, ps * s, pa * a)
    for k in range(3):
        cs, ca = pop(t, 76.8 + k * 0.15, 0.32, s0=0.2)
        x, y = at(660 + k * 44, 560 - k * 20)
        put(f, coin(22), x, y, cs * s, ca * a)


# ------------------------------------------------------------------ S11: comment "GST" -> guide in DM (79.4 - 88.1)
@lru_cache(None)
def guide_doc():
    w, h = 800, 330

    def cb(p):
        tile(p, 90, 90, 100, CYAN, "book")
        p.text(170, 66, "Step-by-step Guide", "bold", 42, rgba(INK), anchor="lm")
        p.text(171, 114, "+ full architecture", "semi", 30, rgba(BLUE), anchor="lm")
        for k, ww in enumerate([520, 460, 560]):
            y = 190 + k * 44
            p.circ(58, y, 15, fill=rgba(tint(CYAN, 0.5)))
            p.text(58, y + 1, str(k + 1), "bold", 18, rgba(WHITE), anchor="mm")
            p.rr((90, y - 9, 90 + ww, y + 9), 9, fill=rgba(SKEL))
    return card(w, h, 36, cb)


@lru_cache(None)
def comment_box(txt, sent=False):
    w, h = 800, 130

    def cb(p):
        p.circ(64, h / 2, 34, fill=rgba(tint(PURPLE, 0.6)))
        icon(p, "user", 64, h / 2 + 4, 40, WHITE, bg=tint(PURPLE, 0.6))
        p.rr((116, 26, w - 140, h - 26), 39, fill=rgba(PANEL), outline=rgba(BORDER), width=2)
        if txt:
            p.text(144, h / 2, txt, "black", 40, rgba(INK), anchor="lm")
        else:
            p.text(144, h / 2, "Add a comment…", "reg", 30, rgba(MUTED), anchor="lm")
        p.text(w - 70, h / 2, "Post", "bold", 32, rgba(GREEN if sent else BLUE), anchor="mm")
    return card(w, h, 36, cb)


@lru_cache(None)
def dm_bubble():
    w, h = 640, 150

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 40, fill=rgba(BLUE))
        icon(p, "chat", 70, h / 2, 64, WHITE, bg=BLUE)
        p.text(126, 52, "DM: GST Guide", "bold", 36, rgba(WHITE), anchor="lm")
        p.text(127, 102, "+ architecture · sent!", "semi", 28, rgba(tint(BLUE, 0.8)), anchor="lm")
    return canvas(w, h, cb)


def s_comment(f, t):
    s, a, dy = trans(t, 80.6, 88.1)
    put(f, guide_doc(), CX, 880 + dy, s, a)
    s2, a2, dy2 = trans(t, 84.3, 88.1)
    typed = "GST"[:max(0, min(3, int((t - 85.1) / 0.12) + 1))] if t >= 85.1 else ""
    sent = t >= 85.75
    put(f, comment_box(typed, sent), CX, 1150 + dy2, s2, a2)
    # 'GST' comment pill above the comment box once sent
    ps, pa = pop(t, 85.8, 0.36, s0=0.3)
    put(f, label_pill("COMMENTED “GST”", YELLOW, DARK, "check", 22, 60), CX - 180, 1265 + dy2, ps, pa * a2)
    ps, pa = pop(t, 87.05, 0.45, s0=0.3)
    put(f, dm_bubble(), CX + 60, 1380 + dy2, ps, pa * a2)


# ------------------------------------------------------------------ S12: outro (88.2 - 96.2)
def s_outro(f, t):
    t0 = 88.2
    s, a, dy = trans(t, t0, None, din=0.6, s0=0.5)
    bob = 5 * math.sin((t - t0) * 2.0) * prog(t, 89.2, 1.0)
    cy = 860 + dy + bob
    tr, k = 88.35, 0
    while tr < t and k < 8:
        pr = prog(t, tr, 1.4)
        if 0 < pr < 1:
            put(f, ring(165, CYAN if k % 2 == 0 else GREEN, 5), CX, cy, s * (0.98 + 0.5 * out_cubic(pr)),
                (1 - pr) * 0.45 * a)
        tr += 1.5
        k += 1
    put(f, logo_shadow(330), CX, cy, s, a * 0.9)
    put(f, logo(330), CX, cy, s, a)
    ps, pa = pop(t, 88.4, 0.38)
    put(f, pill("PLAN B JOURNEY · DAY 3", tint(BLUE, 0.88), BLUE, size=20, h=52), CX, 640, ps, pa)
    ps, pa = pop(t, 88.6, 0.4)
    put(f, handle_pill(42), CX, 1100, ps, pa)
    for lab, ic, bg, tc, x, ts in [("SOFTWARE CAREER", "code", tint(CYAN, 0.86), BLUE, CX - 175, 89.24),
                                   ("SOLID PLAN B", "trend", tint(PURPLE, 0.86), PURPLE, CX + 190, 90.28)]:
        ps, pa = pop(t, ts, 0.34)
        put(f, pill(lab, bg, tc, size=20, h=56, icon_name=ic, icon_col=tc), x, 1205, ps, pa)
    ps, pa = pop(t, 90.9, 0.42, s0=0.4)
    press = prog(t, 92.02, 0.2)
    kk = 1 - 0.07 * math.sin(press * math.pi)
    put(f, follow_btn(press > 0.5), CX, 1320, ps * kk, pa)
    rp = prog(t, 92.04, 0.6)
    if 0 < rp < 1:
        put(f, ring(100, BLUE, 5), CX, 1320, 0.9 + 1.0 * rp, (1 - rp) * 0.6)
    cm = out_cubic(prog(t, 91.45, 0.5))
    if cm > 0:
        leave = out_cubic(prog(t, 92.7, 0.5))
        cx = lerp(CX + 330, CX + 70, cm) + 120 * leave
        cyy = lerp(1530, 1340, cm) + 160 * leave
        put(f, cursor(), cx, cyy, 1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - leave))
    ps, pa = pop(t, 93.3, 0.4)
    put(f, label_pill("COMMENT “GST” FOR THE GUIDE", YELLOW, DARK, "chat", 20, 56), CX, 1430, ps, pa)


SCENES = [
    (0.0, 3.85, s_day),
    (3.85, 15.05, s_idea),
    (15.0, 20.0, s_sellers),
    (20.0, 25.65, s_headache),
    (25.7, 33.2, s_reject),
    (33.15, 40.65, s_pain),
    (40.7, 52.8, s_solution),
    (52.8, 60.75, s_deploy),
    (60.8, 71.05, s_model),
    (71.1, 79.35, s_math),
    (79.4, 88.15, s_comment),
    (88.2, 96.3, s_outro),
]

EVENTS = [
    (0.05, "shimmer", -2, 0.5, {}), (0.34, "pop", -3, 0.5, {"pitch": 0.75}),
    (3.83, "whoosh", 0, 0.5, {}), (5.72, "pop", -5, 0.5, {}), (8.14, "pop", -8, 0.35, {"pitch": 1.2}),
    (9.2, "rise", -6, 0.6, {}), (12.36, "pop", -9, 0.4, {"pitch": 1.3}), (14.0, "chime", -7, 0.6, {}),
    (14.98, "whoosh", -1, 0.5, {}), (15.98, "click", -10, 0.5, {}), (16.78, "pop", -8, 0.35, {}),
    (17.64, "pop", -8, 0.5, {"pitch": 1.15}), (18.38, "pop", -8, 0.65, {"pitch": 1.3}),
    (19.98, "whoosh", -1, 0.5, {}), (22.4, "alert", -5, 0.4, {}), (23.62, "pop", -4, 0.6, {"pitch": 0.8}),
    (25.68, "whoosh", -1, 0.5, {}), (28.0, "pop", -7, 0.35, {}), (30.5, "pop", -7, 0.65, {"pitch": 1.15}),
    (32.12, "alert", -4, 0.5, {}),
    (33.13, "whoosh", -1, 0.5, {}), (35.88, "swipe", -6, 0.6, {}), (38.38, "swipe", -6, 0.6, {}),
    (40.68, "whoosh", -1, 0.5, {}), (42.4, "pop", -6, 0.5, {}), (46.3, "swipe", -7, 0.3, {}),
    (47.96, "click", -1, 0.45, {}), (48.76, "rise", -6, 0.5, {}), (49.76, "pop", -6, 0.35, {"pitch": 1.1}),
    (50.58, "pop", -6, 0.65, {"pitch": 1.3}),
    (52.78, "whoosh", -1, 0.5, {}), (53.28, "pop", -8, 0.35, {}), (53.96, "pop", -8, 0.5, {"pitch": 1.15}),
    (55.48, "pop", -8, 0.65, {"pitch": 1.3}), (59.26, "chime", -6, 0.5, {}),
    (60.78, "whoosh", -1, 0.5, {}), (64.4, "pop", -5, 0.5, {"pitch": 0.9}), (67.36, "rise", -6, 0.4, {}),
    (68.58, "pop", -6, 0.6, {"pitch": 1.2}),
    (71.08, "whoosh", -1, 0.5, {}), (72.4, "rise", -6, 0.4, {}), (75.5, "rise", -5, 0.6, {}),
    (78.04, "chime", -6, 0.5, {}),
    (79.38, "whoosh", -1, 0.5, {}), (80.74, "pop", -6, 0.5, {}), (85.16, "click", -6, 0.5, {}),
    (85.75, "pop", -6, 0.4, {"pitch": 1.2}), (87.05, "chime", -5, 0.6, {}),
    (88.18, "whoosh", -1, 0.5, {}), (88.3, "shimmer", 0, 0.5, {}), (92.02, "click", -1, 0.55, {}),
    (93.3, "pop", -7, 0.5, {"pitch": 1.1}),
]
