"""DAY 2 — "First paying customers: a 3-phase distribution plan".

Voice: episodes/day02/voice.mp3 (90.36 s). Word timings from faster-whisper (episodes/day02/words.json),
start times nudged to the real pauses in the speech envelope. Same look as Day 1 / the isometric reference.
"""
import math
import os
from functools import lru_cache

from gfx import (BLUE, BORDER, CYAN, DARK, DARK_YEL, GREEN, INK, INK2, LINE, MUTED, ORANGE, PANEL, PURPLE, SKEL,
                 T_GREEN, T_YELLOW, WHITE, YELLOW, canvas, card, clamp, icon, in_cubic, lerp, out_back, out_cubic,
                 pop, prog, put, rgba, smooth, text_w, tile, tint, trans)
from scenes import (CX, bar_fill, big_num, check_sprite, cursor, follow_btn, handle_pill, header_label, logo,
                    logo_shadow, pill, ring, skeleton)
from ep_day01 import _at, arrow_right, coin, day_card, plus_small, qmark, track_dot

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.path.join(ROOT, "episodes", "day02", "voice.mp3")
VOICE_LEN = 90.36
TOTAL_LEN = 93.5   # ~3.1 s outro tail
CAP_END = 90.9
HEADER = "COMPUTER HUB · PLAN B · DAY 2"

PHRASES = [
    ([("Day", 0.00, 1), ("2", 0.42, 1), ("of", 0.76, 0), ("building", 1.04, 0)], 1.30),
    ([("Plan", 1.30, 1), ("B", 1.72, 1), ("for", 1.92, 0), ("Software", 2.28, 1), ("Engineers.", 2.64, 1)], 3.32),
    ([("Kal", 4.26, 0), ("ki", 4.42, 0), ("video", 4.56, 0), ("mein", 4.84, 0)], 4.98),
    ([("humne", 4.98, 0), ("dekha", 5.18, 0), ("tha", 5.50, 0), ("ki", 5.70, 0)], 6.00),
    ([("AI", 6.00, 1), ("ki", 6.46, 0), ("madad", 6.60, 0), ("se", 6.82, 0)], 7.10),
    ([("Chrome", 7.10, 1), ("Extension", 7.54, 1), ("kaise", 8.14, 0), ("banani", 8.44, 0), ("hai.", 8.80, 0)], 8.86),
    ([("Code", 9.50, 1), ("toh", 10.20, 0), ("likh", 10.54, 0), ("liya,", 10.72, 0)], 10.96),
    ([("lekin", 11.64, 0), ("ab", 11.80, 0), ("sabse", 11.94, 0), ("bada", 12.40, 0), ("sawaal", 12.56, 1),
      ("hai —", 13.00, 0)], 13.34),
    ([("pehle", 13.80, 0), ("Paying", 14.02, 1), ("Customers", 14.42, 1), ("kahan", 14.94, 0), ("se", 15.12, 0),
      ("layein?", 15.24, 0)], 15.34),
    ([("Aur", 15.92, 0), ("apna", 16.04, 0), ("product", 16.22, 1), ("bechein", 16.68, 1), ("kaise?", 16.96, 0)], 17.26),
    ([("Zyadatar", 18.64, 0), ("log", 19.16, 0), ("pehle", 19.50, 0), ("hi", 19.94, 0), ("din", 20.06, 0)], 20.26),
    ([("har", 20.26, 0), ("jagah", 20.58, 0), ("links", 20.86, 1), ("spam", 21.20, 1), ("karna", 21.56, 0)], 21.88),
    ([("shuru", 21.88, 0), ("kar", 22.12, 0), ("dete", 22.30, 0), ("hain.", 22.54, 0)], 22.56),
    ([("Aapko", 23.16, 0), ("ye", 23.52, 0), ("galti", 23.68, 1), ("bilkul", 23.98, 0), ("nahi", 24.46, 1),
      ("karni.", 24.62, 0)], 24.86),
    ([("Apne", 25.34, 0), ("distribution", 25.58, 1), ("ko", 26.26, 0)], 26.54),
    ([("teen", 26.54, 1), ("phase", 26.84, 1), ("mein", 27.10, 0), ("baanto.", 27.22, 0)], 27.48),
    ([("Pehla", 27.96, 1), ("phase", 28.22, 0), ("hai —", 28.56, 0), ("Communities.", 28.76, 1)], 29.74),
    ([("Reddit", 30.12, 1), ("ke", 30.48, 0), ("r/sideproject", 30.70, 1)], 32.16),
    ([("aur", 32.16, 0), ("X", 32.38, 1), ("par", 32.70, 0), ("jao.", 32.82, 0)], 32.98),
    ([("Wahan", 33.42, 0), ("seedhe", 33.80, 0), ("bechne", 34.08, 1), ("ki", 34.38, 0), ("koshish", 34.54, 0),
      ("mat", 34.82, 1), ("karo,", 35.00, 0)], 35.20),
    ([("balki", 35.56, 0), ("logon", 35.84, 0), ("ko", 36.20, 0), ("batao", 36.34, 1)], 36.74),
    ([("ki", 36.74, 0), ("aapne", 37.10, 0), ("yeh", 37.54, 0), ("extension", 37.68, 0)], 38.24),
    ([("kis", 38.24, 0), ("problem", 38.62, 1), ("ko", 38.98, 0), ("solve", 39.12, 1)], 39.44),
    ([("karne", 39.44, 0), ("ke", 39.70, 0), ("liye", 39.80, 0), ("banayi", 39.92, 0), ("hai.", 40.18, 0)], 40.24),
    ([("Doosra", 40.84, 1), ("phase —", 41.22, 0)], 41.98),
    ([("Competitor", 41.98, 1), ("Review", 42.46, 1), ("Mining.", 42.96, 1)], 43.28),
    ([("Yeh", 43.88, 0), ("sabse", 44.12, 0), ("powerful", 44.62, 1), ("tareeka", 45.24, 0), ("hai.", 45.54, 0)], 45.68),
    ([("Apne", 46.16, 0), ("competitors", 46.38, 1), ("ke", 47.04, 0)], 47.20),
    ([("Chrome", 47.20, 1), ("Store", 47.56, 1), ("reviews", 47.78, 1), ("padho", 48.20, 0)], 48.42),
    ([("aur", 48.42, 0), ("samjho", 48.88, 0), ("ki", 49.26, 0), ("users", 49.60, 0), ("ko", 50.14, 0)], 50.28),
    ([("kis", 50.28, 0), ("baat", 50.70, 0), ("se", 50.88, 0), ("pareshani", 51.04, 1), ("ho", 51.52, 0),
      ("rahi", 51.68, 0), ("hai.", 51.92, 0)], 51.98),
    ([("Jaise", 52.38, 0), ("— tool", 52.70, 0), ("bahut", 53.38, 0), ("mehenga", 53.66, 1), ("hai,", 53.98, 0)], 54.18),
    ([("ya", 54.54, 0), ("koi", 54.66, 0), ("feature", 54.80, 1), ("theek", 55.24, 0), ("se", 55.42, 0)], 55.62),
    ([("kaam", 55.62, 0), ("nahi", 55.88, 1), ("kar", 56.04, 0), ("raha.", 56.24, 0)], 56.40),
    ([("Ab", 56.86, 0), ("usi", 57.00, 0), ("problem", 57.40, 1), ("ko", 57.86, 0)], 58.06),
    ([("apni", 58.06, 0), ("extension", 58.34, 0), ("mein", 58.88, 0), ("solve", 59.00, 1), ("karo,", 59.28, 0)], 59.56),
    ([("aur", 59.56, 0), ("uska", 59.90, 0), ("ek", 60.14, 0), ("chhota", 60.34, 0), ("demo", 60.66, 1),
      ("video", 61.00, 1)], 61.40),
    ([("social", 61.40, 1), ("media", 61.78, 1), ("par", 62.08, 0), ("share", 62.24, 1), ("karo.", 62.56, 0)], 62.74),
    ([("Teesra", 63.30, 1), ("phase", 63.64, 0), ("hai —", 63.96, 0), ("Directories.", 64.24, 1)], 65.10),
    ([("Toolify", 65.54, 1), ("aur", 66.06, 0), ("TinyLaunch", 66.28, 1)], 67.00),
    ([("jaisi", 67.00, 0), ("directories", 67.22, 0), ("par", 67.78, 0)], 68.00),
    ([("apna", 68.00, 0), ("tool", 68.36, 0), ("list", 68.74, 1), ("karo,", 69.04, 0)], 69.22),
    ([("aur", 69.58, 0), ("shuruaati", 69.72, 0), ("users", 70.20, 0), ("ke", 70.60, 0), ("liye", 70.80, 0)], 70.98),
    ([("ek", 70.98, 0), ("special", 71.22, 1), ("launch", 71.74, 1), ("discount", 72.10, 1), ("rakho.", 72.60, 0)], 72.80),
    ([("Aur", 73.28, 0), ("agar", 73.46, 0), ("aap", 73.66, 0), ("bhi", 74.02, 0), ("apni", 74.24, 0)], 74.48),
    ([("9-to-5", 74.48, 1), ("job", 75.16, 1), ("ke", 75.44, 0), ("saath", 75.64, 0)], 75.98),
    ([("ek", 75.98, 0), ("solid", 76.20, 0), ("Plan", 76.74, 1), ("B", 77.08, 1), ("banana", 77.26, 0),
      ("chahte", 77.54, 0), ("hain,", 77.84, 0)], 78.02),
    ([("toh", 78.02, 0), ("mujhe", 78.38, 0), ("abhi", 78.64, 0), ("follow", 79.02, 1), ("kar", 79.28, 0),
      ("lijiye.", 79.48, 0)], 79.68),
    ([("Kyunki", 80.10, 0), ("yahan", 80.32, 0), ("hum", 80.78, 0), ("har", 81.06, 1), ("din", 81.36, 1),
      ("lekar", 81.52, 0), ("aayenge", 81.86, 0)], 82.18),
    ([("naye", 82.18, 0), ("software", 82.50, 1), ("ideas,", 82.98, 1)], 83.76),
    ([("AI", 83.76, 1), ("tools", 83.96, 1), ("aur", 84.40, 0), ("business", 84.76, 1),
      ("opportunities.", 85.16, 1)], 85.92),
    ([("Chalo,", 86.28, 0), ("milte", 86.86, 0), ("hain", 87.18, 0), ("Day", 87.32, 1), ("3", 87.74, 1),
      ("mein,", 88.02, 0)], 88.18),
    ([("ek", 88.46, 0), ("bilkul", 88.60, 0), ("naye", 89.14, 1), ("idea", 89.40, 1), ("ke", 89.70, 0),
      ("saath!", 89.84, 0)], 90.20),
]


# ------------------------------------------------------------------ shared bits
@lru_cache(None)
def stage_pill(txt, col=BLUE, fg=WHITE, ic=None):
    return pill(txt, col, fg, size=24, h=64, icon_name=ic, icon_col=fg)


@lru_cache(None)
def node(name, ic, col, w=230, h=190):
    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 28, fill=rgba(tint(col, 0.9)), outline=rgba(tint(col, 0.55)), width=3)
        p.rr((w / 2 - 42, 28, w / 2 + 42, 112), 22, fill=rgba(col))
        icon(p, ic, w / 2, 70, 46, WHITE, bg=col)
        p.text(w / 2, 150, name, "bold", 28, rgba(INK), anchor="mm")
    return canvas(w, h, cb)


@lru_cache(None)
def title_two(a, b, size, col_b, kind="black"):
    w1 = text_w(a, kind, size)
    w = int(w1 + text_w(b, kind, size) + 16)

    def cb(p):
        p.text(8, size * 0.66, a, kind, size, rgba(INK), anchor="lm")
        p.text(8 + w1, size * 0.66, b, kind, size, rgba(col_b), anchor="lm")
    return canvas(w, int(size * 1.32), cb)


def stage(f, t, txt, t0, t1, col=BLUE, fg=WHITE, ic=None, y=700):
    ps, pa = pop(t, t0, 0.34)
    _, a, _ = trans(t, t0, t1)
    put(f, stage_pill(txt, col, fg, ic), CX, y, ps, pa * a)


# ------------------------------------------------------------------ S1: DAY 2 calendar (0 - 3.95)
def s_day(f, t):
    s, a, dy = trans(t, 0.02, 3.95, din=0.5, s0=0.6)
    cx, cy = CX, 960 + dy
    at = _at(cx, cy, 560, 600, s)
    put(f, day_card(), cx, cy, s, a)
    ps, pa = pop(t, 0.40, 0.45, s0=0.2)
    x, y = at(280, 300)
    put(f, big_num("2", INK, 240), x, y, ps * s, pa * a)
    for k in range(5):
        ps, pa = pop(t, 0.9 + k * 0.08, 0.3)
        x, y = at(170 + k * 55, 430)
        put(f, track_dot(k < 2), x, y, ps * s, pa * a)
        if k == 1:
            rp = prog(t, 1.4, 0.8)
            if 0 < rp < 1:
                put(f, ring(16, CYAN, 3), x, y, s * (1 + 1.2 * rp), a * (1 - rp))
    ps, pa = pop(t, 1.30, 0.36)
    x, y = at(280, 520)
    put(f, title_two("Building ", "Plan B", 40, BLUE, "bold"), x, y, ps * s, pa * a)
    ps, pa = pop(t, 2.28, 0.36)
    put(f, pill("FOR SOFTWARE ENGINEERS", WHITE, INK, size=22, h=60, icon_name="code", icon_col=CYAN, border=BORDER),
        CX, 1335 + dy, ps * s, pa * a)


# ------------------------------------------------------------------ S2: Day 1 recap (3.95 - 11.45)
@lru_cache(None)
def recap_card():
    w, h = 800, 580

    def cb(p):
        header_label(p, w, 56, "DAY 1 RECAP", BLUE, 22, 6)
        p.rr((50, 330, w - 50, h - 40), 24, fill=rgba(PANEL), outline=rgba(LINE), width=2)
        for k in range(4):
            p.text(78, 372 + k * 40, str(k + 1), "monor", 20, rgba(MUTED), anchor="lm")
    return card(w, h, 38, cb)


def s_recap(f, t):
    stage(f, t, "PREVIOUSLY ON PLAN B", 4.26, 11.45, WHITE, INK, "play")
    s, a, dy = trans(t, 4.9, 11.45)
    cx, cy = CX, 1050 + dy
    at = _at(cx, cy, 800, 580, s)
    put(f, recap_card(), cx, cy, s, a)
    ps, pa = pop(t, 6.0, 0.36)
    x, y = at(190, 200)
    put(f, node("AI", "spark", PURPLE), x, y, ps * s, pa * a)
    ap = out_cubic(prog(t, 6.8, 0.35))
    if ap > 0:
        x, y = at(400, 200)
        put(f, arrow_right(BLUE, 110), x, y, s, a, sx=max(ap, 0.02))
    ps, pa = pop(t, 7.10, 0.36)
    x, y = at(610, 200)
    put(f, node("Extension", "puzzle", CYAN), x, y, ps * s, pa * a)
    for k, w in enumerate([420, 520, 360, 470]):  # code lines get written
        rv = smooth(prog(t, 9.5 + k * 0.22, 0.4))
        if rv > 0:
            x, y = at(110 + w * rv / 2, 372 + k * 40)
            put(f, skeleton(int(w), 18, tint([PURPLE, BLUE, GREEN, BLUE][k], 0.6)), x, y, s, a, sx=max(rv, 0.01))
    ps, pa = pop(t, 10.54, 0.36)
    x, y = at(610, 515)
    put(f, pill("CODE DONE", tint(GREEN, 0.85), T_GREEN, size=20, h=52, icon_name="check", icon_col=GREEN),
        x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S3: the big question (11.5 - 17.6)
@lru_cache(None)
def question_card():
    w, h = 800, 560

    def cb(p):
        header_label(p, w, 56, "THE BIGGEST QUESTION", BLUE, 22, 6)
        p.line([(50, 410), (w - 50, 410)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


@lru_cache(None)
def avatar(col):
    return canvas(120, 120, lambda p: (p.circ(60, 60, 54, fill=rgba(tint(col, 0.75))),
                                       icon(p, "user", 60, 66, 62, col, bg=tint(col, 0.75))))


def s_question(f, t):
    s, a, dy = trans(t, 11.5, 17.6)
    cx, cy = CX, 1020 + dy
    at = _at(cx, cy, 800, 560, s)
    put(f, question_card(), cx, cy, s, a)
    for k, col in enumerate([CYAN, PURPLE, DARK_YEL]):
        ps, pa = pop(t, 12.56 + k * 0.14, 0.36)
        x, y = at(220 + k * 180, 165)
        put(f, avatar(col), x, y, ps * s, pa * a)
        qs, qa = pop(t, 12.9 + k * 0.14, 0.3, s0=0.2)
        put(f, qmark(PURPLE, 22), x + 46 * s, y - 46 * s, qs * s, qa * a)
    ps, pa = pop(t, 14.0, 0.45, s0=0.3)
    x, y = at(400, 320)
    put(f, title_two("Paying ", "Customers?", 76, GREEN), x, y, ps * s, pa * a)
    for k in range(3):
        cs, ca = pop(t, 14.5 + k * 0.12, 0.34, s0=0.2)
        x, y = at(672 + k * 42, 170 + k * 8)
        put(f, coin(24), x, y, cs * s, ca * a)
    ps, pa = pop(t, 16.2, 0.36)
    x, y = at(400, 480)
    put(f, pill("HOW TO SELL YOUR PRODUCT?", tint(BLUE, 0.88), BLUE, size=22, h=60, icon_name="rupee",
                icon_col=BLUE), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S4: the spam mistake (17.65 - 25.15)
@lru_cache(None)
def group_card():
    w, h = 780, 640

    def cb(p):
        p.rr((0, 0, w - 1, 96), 38, fill=rgba(PANEL))
        p.rect((0, 60, w - 1, 96), fill=rgba(PANEL))
        p.line([(0, 96), (w, 96)], rgba(LINE), 2, caps=False)
        tile(p, 64, 48, 62, CYAN, "users")
        p.text(112, 36, "Dev Community", "bold", 30, rgba(INK), anchor="lm")
        p.text(113, 68, "group chat", "reg", 22, rgba(MUTED), anchor="lm")
    return card(w, h, 38, cb)


@lru_cache(None)
def spam_bubble(k):
    w, h = 470, 70

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 22, fill=rgba(tint(BLUE, 0.9)), outline=rgba(tint(BLUE, 0.7)), width=2)
        icon(p, "link", 42, h / 2, 34, BLUE, bg=tint(BLUE, 0.9))
        p.text(76, h / 2, ["Buy my tool!", "Check my link!!", "Buy now →", "My new tool!!"][k % 4], "semi", 26,
               rgba(INK), anchor="lm")
        p.text(w - 24, h / 2, "link", "mono", 18, rgba(BLUE), anchor="rm", spacing=2)
    return canvas(w, h, cb)


@lru_cache(None)
def stamp(txt, col):
    size = 72
    w = int(text_w(txt, "black", size, 6) + 70)
    h = int(size * 1.6)
    return canvas(w, h, lambda p: (p.rr((4, 4, w - 4, h - 4), 20, fill=(255, 255, 255, 230), outline=rgba(col), width=8),
                                   p.text(w / 2, h / 2 + 2, txt, "black", size, rgba(col), anchor="mm", spacing=6)))


@lru_cache(None)
def big_cross():
    return canvas(220, 220, lambda p: (p.circ(110, 110, 100, fill=rgba(ORANGE)), icon(p, "cross", 110, 110, 120, WHITE)))


def s_spam(f, t):
    s, a, dy = trans(t, 17.65, 25.15)
    cx, cy = CX, 1040 + dy
    at = _at(cx, cy, 780, 640, s)
    dim = 1 - 0.45 * smooth(prog(t, 23.7, 0.35))
    put(f, group_card(), cx, cy, s, a * dim)
    for k in range(6):  # links pile up, fast
        tk = 20.0 + k * 0.32
        ps, pa = pop(t, tk, 0.3)
        if pa <= 0:
            continue
        x, y = at(260 + (k % 2) * 260, 150 + k * 78)
        put(f, spam_bubble(k), x, y, ps * s, pa * a * dim)
    ps, pa = pop(t, 21.2, 0.4, s0=2.2)
    x, y = at(390, 340)
    put(f, stamp("SPAM", ORANGE), x, y, ps * s, pa * a * dim)
    ps, pa = pop(t, 23.68, 0.42, s0=0.2)
    put(f, big_cross(), CX, cy - 10, ps, pa * a)
    ps, pa = pop(t, 24.3, 0.34)
    put(f, pill("MISTAKE — DON'T DO THIS", ORANGE, WHITE, size=24, h=66, icon_name="warn", icon_col=WHITE),
        CX, cy + 190, ps, pa * a)


# ------------------------------------------------------------------ S5: 3-phase plan (25.2 - 29.85)
PHASES = [("Communities", "users", CYAN, "Reddit · X"), ("Review Mining", "search", PURPLE, "Competitor reviews"),
          ("Directories", "globe", GREEN, "Toolify · TinyLaunch")]


@lru_cache(None)
def phase_row(k, active=False):
    name, ic, col, sub = PHASES[k]
    w, h = 700, 130

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 30, fill=rgba(WHITE if active else PANEL),
             outline=rgba(BLUE if active else LINE), width=4 if active else 2)
        p.circ(62, h / 2, 34, fill=rgba(col))
        p.text(62, h / 2 + 2, str(k + 1), "black", 40, rgba(WHITE), anchor="mm")
        tile(p, 160, h / 2, 74, col, ic)
        p.text(220, h / 2 - 18, name, "bold", 36, rgba(INK), anchor="lm")
        p.text(221, h / 2 + 24, sub, "reg", 24, rgba(MUTED), anchor="lm")
    return canvas(w, h, cb)


def s_plan(f, t):
    stage(f, t, "DISTRIBUTION PLAN", 25.4, 29.85, BLUE, WHITE, "trend")
    _, a, dy = trans(t, 25.4, 29.85)
    for k, ts in enumerate([26.54, 26.84, 27.10]):
        ps, pa = pop(t, ts, 0.38)
        y = 860 + k * 160 + dy
        act = k == 0 and t >= 27.96
        put(f, phase_row(k, act), CX, y, ps * (1 + 0.03 * math.sin(math.pi * prog(t, 27.96, 0.35)) * (k == 0)),
            pa * a)
    ps, pa = pop(t, 28.0, 0.34)
    put(f, pill("START HERE", YELLOW, DARK, size=18, h=46), CX + 260, 790 + dy, ps, pa * a)


# ------------------------------------------------------------------ S6: phase 1 — communities (29.9 - 40.7)
@lru_cache(None)
def forum_card():
    w, h = 800, 290

    def cb(p):
        p.circ(70, 70, 36, fill=rgba(ORANGE))
        p.text(70, 72, "r/", "black", 34, rgba(WHITE), anchor="mm")
        p.text(124, 56, "r/sideproject", "bold", 32, rgba(INK), anchor="lm")
        p.text(125, 92, "community post", "reg", 22, rgba(MUTED), anchor="lm")
        p.text(40, 160, "I built a Chrome extension", "bold", 34, rgba(INK), anchor="lm")
        p.text(40, 204, "to solve this problem — feedback?", "semi", 30, rgba(INK2), anchor="lm")
        p.rr((40, 238, 380, 254), 8, fill=rgba(SKEL))
        icon(p, "up", w - 70, 140, 44, ORANGE)
        icon(p, "chat", w - 70, 220, 40, MUTED)
    return card(w, h, 34, cb)


@lru_cache(None)
def x_card():
    w, h = 800, 200

    def cb(p):
        p.circ(70, 64, 36, fill=rgba(INK))
        p.text(70, 66, "X", "black", 36, rgba(WHITE), anchor="mm")
        p.text(124, 50, "Post on X", "bold", 32, rgba(INK), anchor="lm")
        p.text(125, 86, "build in public", "reg", 22, rgba(MUTED), anchor="lm")
        p.rr((40, 128, 620, 146), 9, fill=rgba(SKEL))
        p.rr((40, 160, 440, 178), 9, fill=rgba(SKEL))
        icon(p, "heart", w - 70, 140, 40, (235, 70, 110))
    return card(w, h, 34, cb)


@lru_cache(None)
def rule_chip(ok):
    if ok:
        return pill("SHARE THE PROBLEM YOU SOLVE", tint(GREEN, 0.85), T_GREEN, size=22, h=62, icon_name="check",
                    icon_col=GREEN)
    return pill("DON'T SELL DIRECTLY", tint(ORANGE, 0.85), (190, 80, 0), size=22, h=62, icon_name="cross",
                icon_col=ORANGE)


def s_phase1(f, t):
    stage(f, t, "PHASE 1 · COMMUNITIES", 29.9, 40.7, CYAN, WHITE, "users")
    s, a, dy = trans(t, 30.1, 40.7)
    put(f, forum_card(), CX, 905 + dy, s, a)
    if t > 36.4:
        rp = prog(t, 36.4, 0.7)
        if rp < 1:
            put(f, ring(30, ORANGE, 4), CX + 330 * s, 905 + dy - 5 * s, s * (0.8 + 1.2 * rp), a * (1 - rp))
    s2, a2, dy2 = trans(t, 32.38, 40.7)
    put(f, x_card(), CX, 1180 + dy2, s2, a2 * a)
    ps, pa = pop(t, 34.08, 0.34)
    rv = 1 - 0.5 * smooth(prog(t, 35.56, 0.3))  # "don't" fades back when "do" arrives
    put(f, rule_chip(False), CX, 1340 + dy, ps, pa * a * rv)
    ps, pa = pop(t, 35.84, 0.36)
    put(f, rule_chip(True), CX, 1420 + dy, ps, pa * a)


# ------------------------------------------------------------------ S7: phase 2 — competitor review mining (40.8 - 63.25)
@lru_cache(None)
def mining_card():
    w, h = 760, 420

    def cb(p):
        p.rr((w / 2 - 80, 40, w / 2 + 80, 200), 44, fill=rgba(PURPLE))
        icon(p, "search", w / 2, 120, 96, WHITE, bg=PURPLE)
        p.text(w / 2, 262, "Competitor", "black", 58, rgba(INK), anchor="mm")
        p.text(w / 2, 334, "Review Mining", "black", 58, rgba(PURPLE), anchor="mm")
    return card(w, h, 38, cb)


REVIEWS = [(2, "Too expensive for me"), (1, "Feature not working"), (4, "")]


@lru_cache(None)
def reviews_card():
    w, h = 820, 620

    def cb(p):
        tile(p, 74, 70, 74, (150, 160, 180), "puzzle")
        p.text(132, 54, "Competitor Extension", "bold", 32, rgba(INK), anchor="lm")
        p.text(133, 92, "Chrome Store · reviews", "reg", 24, rgba(MUTED), anchor="lm")
        p.line([(40, 140), (w - 40, 140)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


@lru_cache(None)
def review_row(k, hl=False):
    stars, txt = REVIEWS[k]
    w, h = 740, 130

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 24, fill=rgba(tint(YELLOW, 0.8) if hl else PANEL),
             outline=rgba(DARK_YEL if hl else LINE), width=3 if hl else 2)
        p.circ(56, 50, 26, fill=rgba(tint([CYAN, PURPLE, GREEN][k], 0.55)))
        for i in range(5):
            icon(p, "star", 108 + i * 34, 38, 28, YELLOW if i < stars else (215, 220, 230))
        if txt:
            p.text(96, 88, "“" + txt + "”", "bold", 30, rgba(INK), anchor="lm")
        else:
            p.rr((96, 80, 520, 98), 9, fill=rgba(SKEL))
    return canvas(w, h, cb)


@lru_cache(None)
def magnifier():
    return canvas(150, 150, lambda p: (p.circ(62, 62, 48, fill=(255, 255, 255, 120), outline=rgba(PURPLE), width=10),
                                       p.line([(98, 98), (138, 138)], rgba(PURPLE), 16)))


@lru_cache(None)
def fix_card():
    w, h = 800, 330

    def cb(p):
        tile(p, 74, 70, 74, CYAN, "puzzle")
        p.text(132, 54, "Your Extension", "bold", 32, rgba(INK), anchor="lm")
        p.text(133, 92, "problems solved", "reg", 24, rgba(MUTED), anchor="lm")
        p.line([(40, 140), (w - 40, 140)], rgba(LINE), 2, caps=False)
        for k, txt in enumerate(["Fair price", "Feature that works"]):
            y = 192 + k * 74
            p.text(110, y, txt, "bold", 32, rgba(INK), anchor="lm")
            p.rr((480, y - 8, 680, y + 8), 8, fill=rgba(SKEL))
    return card(w, h, 34, cb)


@lru_cache(None)
def phone_demo():
    w, h = 300, 440

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), 44, fill=rgba(INK))
        p.rr((14, 14, w - 15, h - 15), 32, fill=rgba(tint(CYAN, 0.8)))
        p.rr((w / 2 - 40, 24, w / 2 + 40, 36), 6, fill=rgba(INK))
        tile(p, w / 2, 150, 110, CYAN, "puzzle", k=0.4)
        p.rr((40, 300, w - 40, 316), 8, fill=rgba(WHITE))
        p.rr((40, 330, w - 90, 346), 8, fill=rgba(WHITE))
        p.text(w / 2, 396, "DEMO", "mono", 22, rgba(BLUE), anchor="mm", spacing=6)
    return canvas(w, h, cb)


@lru_cache(None)
def play_btn():
    return canvas(110, 110, lambda p: (p.circ(55, 55, 50, fill=rgba(BLUE)), icon(p, "play", 60, 55, 54, WHITE)))


@lru_cache(None)
def social_tile(k):
    ic, col, lab = [("heart", (235, 70, 110), "Likes"), ("users", CYAN, "Reach"), ("share", GREEN, "Shares")][k]

    def cb(p):
        p.rr((2, 2, 298, 108), 28, fill=rgba(WHITE), outline=rgba(BORDER), width=2)
        tile(p, 56, 55, 70, col, ic)
        p.text(110, 55, lab, "bold", 32, rgba(INK), anchor="lm")
    return canvas(300, 110, cb)


def s_phase2(f, t):
    stage(f, t, "PHASE 2 · REVIEW MINING", 40.84, 63.25, PURPLE, WHITE, "search")
    # a) title card + "most powerful"
    if t < 46.3:
        s, a, dy = trans(t, 41.0, 46.3)
        put(f, mining_card(), CX, 1000 + dy, s, a)
        ps, pa = pop(t, 44.62, 0.4, s0=0.3)
        put(f, pill("MOST POWERFUL METHOD", YELLOW, DARK, size=24, h=66, icon_name="star", icon_col=DARK),
            CX, 1290 + dy, ps, pa * a)
    # b) read the reviews
    if 46.1 <= t < 56.75:
        s, a, dy = trans(t, 46.16, 56.75)
        cx, cy = CX, 1050 + dy
        at = _at(cx, cy, 820, 620, s)
        put(f, reviews_card(), cx, cy, s, a)
        for k in range(3):
            ps, pa = pop(t, 47.78 + k * 0.16, 0.34)
            hl = (k == 0 and t >= 53.66) or (k == 1 and t >= 54.80)
            x, y = at(410, 220 + k * 140)
            bump = 1 + 0.04 * math.sin(math.pi * prog(t, [53.66, 54.80, 99][k], 0.35))
            put(f, review_row(k, hl), x, y, ps * s * bump, pa * a)
        # magnifier scans the rows while "users ko kis baat se pareshani"
        if 48.3 < t < 53.5:
            ph = prog(t, 48.3, 3.6)
            ry = 220 + 280 * (0.5 - 0.5 * math.cos(ph * math.pi * 2))
            rx = 260 + 360 * ph
            x, y = at(rx, ry)
            put(f, magnifier(), x, y, s, a * clamp(prog(t, 48.3, 0.3)) * (1 - prog(t, 53.2, 0.3)))
        ps, pa = pop(t, 51.04, 0.34)
        x, y = at(640, 70)
        put(f, pill("USER PAIN", tint(ORANGE, 0.85), (190, 80, 0), size=18, h=46, icon_name="warn",
                    icon_col=ORANGE), x, y, ps * s, pa * a)
        for k, ts in enumerate([53.66, 54.80]):
            ps, pa = pop(t, ts + 0.1, 0.32)
            x, y = at(690, 220 + k * 140 - 40)
            put(f, pill(f"PROBLEM #{k + 1}", DARK_YEL, WHITE, size=16, h=40), x, y, ps * s, pa * a)
    # c) solve it + demo video for social media
    if t >= 56.7:
        s, a, dy = trans(t, 56.86, 63.25)
        cx, cy = CX, 892 + dy
        at = _at(cx, cy, 800, 330, s)
        put(f, fix_card(), cx, cy, s, a)
        for k, ts in enumerate([57.40, 58.34]):
            cs, ca = pop(t, ts, 0.32, s0=0.2)
            x, y = at(66, 192 + k * 74)
            put(f, check_sprite(44), x, y, cs * s, ca * a)
        ps, pa = pop(t, 59.0, 0.34)
        x, y = at(680, 70)
        put(f, pill("SOLVED", GREEN, WHITE, size=20, h=50, icon_name="check", icon_col=WHITE), x, y, ps * s, pa * a)
        s2, a2, dy2 = trans(t, 60.5, 63.25)
        put(f, phone_demo(), CX - 200, 1268 + dy2, s2 * 0.9, a2 * a)
        bs, ba = pop(t, 61.0, 0.4, s0=0.3)
        pulse = 1 + 0.06 * math.sin((t - 61.0) * 6) * (t > 61.4)
        put(f, play_btn(), CX - 200, 1223 + dy2, bs * s2 * pulse, ba * a2 * a)
        for k, ts in enumerate([61.40, 61.78, 62.24]):
            ps, pa = pop(t, ts, 0.34)
            put(f, social_tile(k), CX + 180, 1138 + k * 128 + dy2, ps, pa * a2 * a)


# ------------------------------------------------------------------ S8: phase 3 — directories (63.3 - 73.2)
@lru_cache(None)
def dir_card(k, listed=False):
    name, sub, col = [("Toolify", "AI tools directory", GREEN), ("TinyLaunch", "launch directory", BLUE)][k]
    w, h = 800, 190

    def cb(p):
        tile(p, 86, h / 2, 100, col, "globe")
        p.text(160, h / 2 - 22, name, "bold", 40, rgba(INK), anchor="lm")
        p.text(161, h / 2 + 26, sub, "reg", 26, rgba(MUTED), anchor="lm")
        bx = w - 220
        if listed:
            p.rr((bx, h / 2 - 34, w - 40, h / 2 + 34), 34, fill=rgba(tint(GREEN, 0.85)))
            icon(p, "check", bx + 40, h / 2, 36, GREEN)
            p.text(bx + 66, h / 2, "LISTED", "mono", 22, rgba(T_GREEN), anchor="lm", spacing=3)
        else:
            p.rr((bx, h / 2 - 34, w - 40, h / 2 + 34), 34, fill=rgba(BLUE))
            p.text((bx + w - 40) / 2, h / 2, "SUBMIT", "mono", 22, rgba(WHITE), anchor="mm", spacing=3)
    return card(w, h, 34, cb)


@lru_cache(None)
def discount_ticket():
    w, h = 680, 210

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), 30, fill=rgba(YELLOW))
        p.circ(0, h / 2, 26, fill=(0, 0, 0, 0))
        p.rr((200, 0, w - 1, h - 1), 30, fill=rgba(WHITE))
        p.rect((200, 0, 240, h - 1), fill=rgba(WHITE))
        for y in range(18, h - 10, 26):
            p.line([(200, y), (200, y + 12)], rgba(DARK_YEL), 4)
        icon(p, "ticket", 100, h / 2, 110, (160, 100, 0), bg=YELLOW)
        p.text(236, 70, "LAUNCH", "black", 50, rgba(INK), anchor="lm")
        p.text(236, 124, "DISCOUNT", "black", 50, rgba(DARK_YEL), anchor="lm")
        p.text(238, 172, "for early users", "semi", 26, rgba(MUTED), anchor="lm")
    return canvas(w, h, cb)


def s_phase3(f, t):
    stage(f, t, "PHASE 3 · DIRECTORIES", 63.3, 73.2, GREEN, WHITE, "globe")
    _, a, dy = trans(t, 63.3, 73.2)
    for k, (ts, tl) in enumerate([(65.54, 68.74), (66.28, 68.95)]):
        ps, pa = pop(t, ts, 0.38)
        listed = t >= tl
        bump = 1 + 0.04 * math.sin(math.pi * prog(t, tl, 0.3))
        put(f, dir_card(k, listed), CX, 870 + k * 220 + dy, ps * bump, pa * a)
    ps, pa = pop(t, 71.22, 0.45, s0=0.3)
    sh = 1 + 0.04 * math.sin(math.pi * prog(t, 72.10, 0.35))
    put(f, discount_ticket(), CX, 1335 + dy, ps * sh, pa * a)


# ------------------------------------------------------------------ S9: 9-to-5 + Plan B (73.25 - 78.1)
@lru_cache(None)
def side_box(kind):
    w, h = 330, 330
    job = kind == "job"
    col = DARK_YEL if job else PURPLE

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 34, fill=rgba(WHITE), outline=rgba(tint(col, 0.5)), width=4)
        p.rr((w / 2 - 70, 40, w / 2 + 70, 180), 38, fill=rgba(col))
        icon(p, "clock" if job else "spark", w / 2, 110, 84, WHITE, bg=col)
        p.text(w / 2, 232, "9-to-5 Job" if job else "Plan B", "black", 42, rgba(INK), anchor="mm")
        p.text(w / 2, 280, "salary" if job else "extra income", "semi", 26, rgba(MUTED), anchor="mm")
    return canvas(w, h, cb)


def s_job(f, t):
    _, a, dy = trans(t, 73.25, 78.1)
    cy = 1010 + dy
    ps, pa = pop(t, 74.48, 0.38)
    put(f, side_box("job"), CX - 200, cy, ps, pa * a)
    ps, pa = pop(t, 75.98, 0.3)
    put(f, plus_small(), CX, cy, ps, pa * a)
    ps, pa = pop(t, 76.74, 0.42, s0=0.4)
    put(f, side_box("plan"), CX + 200, cy, ps, pa * a)
    ps, pa = pop(t, 76.2, 0.34)
    put(f, pill("SOLID PLAN B", tint(PURPLE, 0.86), PURPLE, size=22, h=58, icon_name="trend", icon_col=PURPLE),
        CX, cy + 250, ps, pa * a)


# ------------------------------------------------------------------ S10: outro (78.05 - 93.5)
@lru_cache(None)
def every_day_chip(k):
    lab, ic, col = [("SOFTWARE IDEAS", "code", BLUE), ("AI TOOLS", "spark", PURPLE),
                    ("BUSINESS OPPORTUNITIES", "trend", T_GREEN)][k]
    return pill(lab, tint(col, 0.86), col, size=20, h=56, icon_name=ic, icon_col=col)


def s_outro(f, t):
    t0 = 78.05
    s, a, dy = trans(t, t0, None, din=0.6, s0=0.5)
    bob = 5 * math.sin((t - t0) * 2.0) * prog(t, 79.0, 1.0)
    cy = 860 + dy + bob
    tr, k = 78.2, 0
    while tr < t and k < 12:
        pr = prog(t, tr, 1.4)
        if 0 < pr < 1:
            put(f, ring(165, CYAN if k % 2 == 0 else GREEN, 5), CX, cy, s * (0.98 + 0.5 * out_cubic(pr)),
                (1 - pr) * 0.45 * a)
        tr += 1.5
        k += 1
    put(f, logo_shadow(330), CX, cy, s, a * 0.9)
    put(f, logo(330), CX, cy, s, a)
    ps, pa = pop(t, 78.3, 0.38)
    put(f, pill("PLAN B JOURNEY · DAY 2", tint(BLUE, 0.88), BLUE, size=20, h=52), CX, 640, ps, pa)
    ps, pa = pop(t, 78.4, 0.4)
    put(f, handle_pill(42), CX, 1100, ps, pa)
    # follow button: cursor clicks it on "follow"
    ps, pa = pop(t, 78.6, 0.42, s0=0.4)
    press = prog(t, 79.02, 0.2)
    kk = 1 - 0.07 * math.sin(press * math.pi)
    put(f, follow_btn(press > 0.5), CX, 1225, ps * kk, pa)
    rp = prog(t, 79.04, 0.6)
    if 0 < rp < 1:
        put(f, ring(100, BLUE, 5), CX, 1225, 0.9 + 1.0 * rp, (1 - rp) * 0.6)
    cm = out_cubic(prog(t, 78.55, 0.45))
    if cm > 0:
        leave = out_cubic(prog(t, 79.7, 0.5))
        cx = lerp(CX + 330, CX + 70, cm) + 120 * leave
        cyy = lerp(1440, 1245, cm) + 160 * leave
        put(f, cursor(), cx, cyy, 1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - leave))
    # every day: software ideas, AI tools, business opportunities
    out = 1 - smooth(prog(t, 86.0, 0.3))
    ps, pa = pop(t, 81.06, 0.34)
    put(f, pill("EVERY DAY", INK, WHITE, size=18, h=44), CX, 1325, ps, pa * out)
    for k, (ts, x, y) in enumerate([(82.50, CX - 165, 1395), (83.76, CX + 190, 1395), (84.76, CX, 1462)]):
        ps, pa = pop(t, ts, 0.34)
        put(f, every_day_chip(k), x, y, ps, pa * out)
    # see you in Day 3 with a new idea
    ps, pa = pop(t, 87.32, 0.42, s0=0.4)
    put(f, pill("SEE YOU IN DAY 3", BLUE, WHITE, size=26, h=72, icon_name="play", icon_col=WHITE), CX, 1360, ps, pa)
    ps, pa = pop(t, 89.40, 0.36)
    put(f, pill("NEW IDEA", YELLOW, DARK, size=22, h=58, icon_name="bolt", icon_col=DARK), CX, 1450, ps, pa)


SCENES = [
    (0.0, 4.0, s_day),
    (3.95, 11.5, s_recap),
    (11.5, 17.65, s_question),
    (17.65, 25.2, s_spam),
    (25.2, 29.9, s_plan),
    (29.9, 40.75, s_phase1),
    (40.8, 63.3, s_phase2),
    (63.3, 73.25, s_phase3),
    (73.25, 78.15, s_job),
    (78.05, 93.6, s_outro),
]

EVENTS = [
    (0.05, "shimmer", -2, 0.5, {}), (0.40, "pop", -3, 0.5, {"pitch": 0.75}),
    (3.93, "whoosh", 0, 0.5, {}), (6.0, "pop", -7, 0.4, {}), (7.10, "pop", -7, 0.6, {"pitch": 1.15}),
    (10.54, "click", -4, 0.6, {}),
    (11.48, "whoosh", -1, 0.5, {}), (12.56, "pop", -9, 0.5, {"pitch": 1.3}), (14.0, "rise", -6, 0.5, {}),
    (17.63, "whoosh", -1, 0.5, {}), (20.0, "click", -10, 0.4, {}), (20.64, "click", -10, 0.6, {}),
    (21.2, "pop", -4, 0.5, {"pitch": 0.7}), (23.68, "alert", -4, 0.5, {}),
    (25.18, "whoosh", -1, 0.5, {}), (26.54, "pop", -8, 0.5, {"pitch": 1.0}), (26.84, "pop", -8, 0.5, {"pitch": 1.15}),
    (27.10, "pop", -8, 0.5, {"pitch": 1.3}),
    (29.88, "whoosh", -1, 0.5, {}), (32.38, "pop", -7, 0.6, {}), (34.08, "swipe", -5, 0.5, {}),
    (35.84, "chime", -7, 0.5, {}),
    (40.78, "whoosh", -1, 0.5, {}), (44.62, "rise", -5, 0.5, {}),
    (46.14, "whoosh", -2, 0.5, {}), (48.3, "swipe", -7, 0.5, {}), (53.66, "click", -4, 0.4, {}),
    (54.80, "click", -4, 0.6, {}),
    (56.84, "whoosh", -1, 0.5, {}), (57.40, "pop", -8, 0.4, {"pitch": 1.2}), (58.34, "pop", -8, 0.6, {"pitch": 1.35}),
    (61.0, "pop", -5, 0.4, {"pitch": 0.9}),
    (63.28, "whoosh", -1, 0.5, {}), (68.74, "click", -4, 0.6, {}), (71.22, "chime", -5, 0.5, {}),
    (73.23, "whoosh", -1, 0.5, {}), (76.74, "pop", -6, 0.6, {"pitch": 1.1}),
    (78.03, "whoosh", -1, 0.5, {}), (78.15, "shimmer", 0, 0.5, {}), (79.02, "click", -1, 0.55, {}),
    (82.50, "pop", -9, 0.4, {}), (83.76, "pop", -9, 0.6, {"pitch": 1.15}), (84.76, "pop", -9, 0.5, {"pitch": 1.3}),
    (87.32, "chime", -5, 0.5, {}),
]
