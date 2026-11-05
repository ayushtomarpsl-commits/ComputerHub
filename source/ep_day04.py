"""DAY 4 — "App idea: BlaBlaCar for Parking".

Voice: episodes/day04/voice.mp3 (86.75 s). Word timings from faster-whisper (episodes/day04/words.json),
start times nudged to the real pauses. Same look as Day 1-3.
"""
import math
import os
from functools import lru_cache

from gfx import (BLUE, BORDER, CYAN, DARK, DARK_YEL, GREEN, INK, INK2, LINE, MUTED, ORANGE, PANEL, PURPLE, SKEL,
                 T_GREEN, WHITE, YELLOW, canvas, card, clamp, icon, lerp, out_back, out_cubic, pop, prog, put, rgba,
                 smooth, text_w, tile, tint, trans)
from scenes import (CX, bar_fill, big_num, check_sprite, cursor, follow_btn, handle_pill, header_label, logo,
                    logo_shadow, pill, ring)
from ep_day01 import _at, arrow_right, day_card, plus_small, qmark, track_dot
from ep_day02 import avatar, big_cross, node, side_box, stage, stamp, title_two
from ep_day03 import comment_box, label_pill

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.path.join(ROOT, "episodes", "day04", "voice.mp3")
VOICE_LEN = 86.75
TOTAL_LEN = 89.9
CAP_END = 87.3
HEADER = "COMPUTER HUB · PLAN B · DAY 4"
RED = (226, 64, 64)

PHRASES = [
    ([("Day", 0.00, 1), ("4", 0.38, 1), ("of", 0.78, 0), ("building", 1.02, 0)], 1.28),
    ([("Plan", 1.28, 1), ("B", 1.68, 1), ("for", 1.80, 0), ("Software", 2.10, 1), ("Engineers.", 2.52, 1)], 3.14),
    ([("Agar", 4.24, 0), ("aap", 4.46, 0), ("ek", 4.62, 0), ("software", 4.72, 1), ("engineer", 5.26, 1), ("hain,", 5.70, 0)], 5.88),
    ([("toh", 5.88, 0), ("aapko", 6.24, 0), ("9-to-5", 6.60, 1), ("ki", 7.30, 0), ("salary", 7.40, 1), ("se", 7.88, 0)], 8.20),
    ([("bahar", 8.20, 1), ("sochna", 8.54, 1), ("hi", 8.98, 0), ("padega,", 9.12, 0)], 9.44),
    ([("kyunki", 9.86, 0), ("AI", 10.06, 1), ("ki", 10.52, 0), ("wajah", 10.70, 0), ("se", 10.88, 0)], 11.16),
    ([("tech", 11.16, 1), ("industry", 11.66, 1), ("bahut", 12.16, 0)], 12.80),
    ([("tezi", 12.80, 1), ("se", 13.08, 0), ("badal", 13.28, 1), ("rahi", 13.54, 0), ("hai.", 13.74, 0)], 13.84),
    ([("Aaj", 14.30, 0), ("main", 14.60, 0), ("aapke", 14.70, 0), ("liye", 15.02, 0), ("ek", 15.22, 0), ("aisa", 15.54, 0)], 15.94),
    ([("app", 15.94, 1), ("idea", 16.26, 1), ("lekar", 16.52, 0), ("aaya", 16.80, 0), ("hoon", 17.02, 0)], 17.20),
    ([("jo", 17.20, 0), ("Bharat", 17.42, 0), ("ki", 17.78, 0), ("sabse", 18.02, 0), ("badi", 18.66, 0)], 18.90),
    ([("daily", 18.90, 1), ("problem", 19.26, 1), ("ko", 19.60, 0), ("solve", 19.72, 0), ("karta", 20.06, 0),
      ("hai —", 20.32, 0)], 20.42),
    ([("Parking", 20.94, 1), ("ki", 21.34, 0), ("samasya!", 21.48, 1)], 21.88),
    ([("Aapne", 22.42, 0), ("BlaBlaCar", 22.74, 1), ("ka", 23.40, 0), ("naam", 23.50, 0)], 23.70),
    ([("toh", 23.70, 0), ("suna", 23.86, 0), ("hi", 24.04, 0), ("hoga,", 24.18, 0)], 24.40),
    ([("jahan", 24.74, 0), ("log", 25.06, 0), ("apni", 25.20, 0), ("car", 25.40, 0), ("ki", 25.84, 0)], 25.98),
    ([("khaali", 25.98, 1), ("seats", 26.34, 1), ("share", 26.70, 1), ("karte", 27.00, 0), ("hain.", 27.32, 0)], 27.38),
    ([("Bilkul", 27.82, 0), ("usi", 28.28, 0), ("concept", 28.66, 1), ("par", 29.16, 0)], 29.30),
    ([("aap", 29.30, 0), ("bana", 29.58, 0), ("sakte", 29.80, 0), ("hain —", 29.98, 0)], 30.34),
    ([("“BlaBlaCar", 30.60, 1), ("for", 31.38, 1), ("Parking”!", 31.72, 1)], 32.10),
    ([("Aaj", 32.64, 0), ("har", 32.94, 0), ("bade", 33.22, 0), ("shehar", 33.46, 0), ("mein", 33.76, 0)], 34.00),
    ([("railway", 34.00, 1), ("station,", 34.44, 1), ("markets", 35.22, 1), ("aur", 35.72, 0), ("hospitals", 36.02, 1)], 36.58),
    ([("ke", 36.58, 0), ("bahar", 36.76, 0), ("parking", 37.42, 0), ("milna", 37.84, 0)], 38.12),
    ([("namumkin", 38.12, 1), ("hai.", 38.76, 0)], 38.90),
    ([("Log", 39.44, 0), ("ghanton", 40.46, 1), ("bhatakte", 41.04, 1), ("hain", 41.52, 0)], 41.68),
    ([("aur", 41.68, 0), ("no-parking", 42.12, 1), ("mein", 42.74, 0)], 43.04),
    ([("bhaari", 43.04, 1), ("challan", 43.46, 1), ("katwa", 43.84, 0), ("baithte", 44.08, 0), ("hain.", 44.44, 0)], 44.50),
    ([("Is", 45.02, 0), ("app", 45.18, 0), ("ke", 45.40, 0), ("zariye", 45.54, 0)], 45.86),
    ([("koi", 45.86, 0), ("bhi", 46.24, 0), ("insaan", 46.38, 0), ("apne", 46.82, 0)], 47.20),
    ([("ghar", 47.20, 1), ("ke", 47.46, 0), ("saamne", 47.66, 0), ("ki", 47.94, 0)], 48.18),
    ([("khaali", 48.18, 1), ("jagah,", 48.48, 1), ("plot", 49.16, 1)], 49.48),
    ([("ya", 49.48, 0), ("dukaan", 49.82, 1), ("ke", 50.16, 0), ("aage", 50.36, 0), ("ka", 50.54, 0), ("space", 50.68, 1)], 51.14),
    ([("list", 51.14, 1), ("kar", 51.50, 0), ("sakta", 51.66, 0), ("hai.", 51.92, 0)], 52.00),
    ([("Aur", 52.40, 0), ("jab", 52.54, 0), ("bhi", 52.84, 0), ("kisi", 52.98, 0), ("driver", 53.20, 1), ("ko", 53.66, 0)], 53.84),
    ([("us", 53.84, 0), ("ilaake", 54.06, 0), ("mein", 54.38, 0), ("parking", 54.52, 1), ("chahiye", 54.90, 0),
      ("hogi,", 55.28, 0)], 55.66),
    ([("app", 55.94, 0), ("use", 56.22, 0), ("sabse", 56.48, 0), ("nazdeeki", 57.00, 1)], 57.42),
    ([("khaali", 57.42, 1), ("jagah", 57.84, 1), ("aur", 58.20, 0), ("directions", 58.50, 1), ("dikha", 58.98, 0),
      ("dega.", 59.22, 0)], 59.44),
    ([("Shuruaat", 59.84, 0), ("mein", 60.30, 0), ("aapko", 60.48, 0), ("koi", 60.88, 0)], 61.08),
    ([("complex", 61.08, 0), ("payment", 61.58, 1), ("gateway", 61.96, 1), ("bhi", 62.34, 0), ("nahi", 62.46, 1),
      ("chahiye —", 62.66, 0)], 62.86),
    ([("driver", 63.32, 0), ("seedhe", 63.80, 0), ("jagah", 64.32, 0), ("ke", 64.64, 0), ("maalik", 64.82, 1), ("ko", 65.12, 0)], 65.44),
    ([("UPI", 65.44, 1), ("ya", 66.04, 0), ("cash", 66.28, 1), ("de", 66.60, 0), ("sakta", 66.74, 0), ("hai.", 67.04, 0)], 67.10),
    ([("Is", 67.58, 0), ("tarah", 67.76, 0), ("ka", 68.00, 0), ("poora", 68.30, 0), ("MVP", 68.64, 1)], 69.12),
    ([("aap", 69.12, 0), ("Claude", 69.60, 1), ("aur", 69.98, 0), ("Cursor", 70.26, 1), ("ki", 70.66, 0),
      ("madad", 70.86, 0), ("se", 71.10, 0)], 71.48),
    ([("kuch", 71.48, 0), ("hi", 71.68, 0), ("dinon", 71.74, 1), ("mein", 71.96, 0)], 72.06),
    ([("code", 72.06, 1), ("kar", 72.32, 0), ("sakte", 72.46, 0), ("hain.", 72.76, 0)], 72.88),
    ([("Agar", 73.26, 0), ("aapko", 73.50, 0), ("is", 73.78, 0), ("parking", 73.92, 1), ("app", 74.32, 1), ("ka", 74.56, 0)], 74.72),
    ([("poora", 74.72, 0), ("system", 75.10, 1), ("design", 75.50, 1), ("aur", 76.16, 0)], 76.28),
    ([("step-by-step", 76.28, 1), ("guide", 77.10, 1), ("chahiye,", 77.42, 0)], 77.74),
    ([("toh", 77.74, 0), ("comment", 78.10, 1), ("mein", 78.48, 0), ("likho", 78.62, 0), ("'PARKING',", 78.88, 1)], 79.48),
    ([("main", 79.86, 0), ("seedhe", 80.00, 0), ("aapke", 80.50, 0), ("DM", 80.74, 1), ("mein", 80.98, 0),
      ("bhej", 81.10, 0), ("dunga.", 81.32, 0)], 81.58),
    ([("Aur", 81.96, 0), ("is", 82.08, 0), ("series", 82.20, 0), ("ke", 82.50, 0), ("final", 82.72, 1), ("part", 83.12, 1)], 83.52),
    ([("yaani", 83.52, 0), ("Day", 83.86, 1), ("5", 84.08, 1), ("ke", 84.46, 0), ("liye,", 84.60, 0)], 84.90),
    ([("mujhe", 84.92, 0), ("abhi", 85.50, 0), ("Follow", 85.80, 1), ("kar", 86.08, 0), ("lijiye!", 86.26, 0)], 86.60),
]


# ------------------------------------------------------------------ shared bits
@lru_cache(None)
def place_tile(name, ic, col, tag=None, tag_col=ORANGE, w=240, h=250):
    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 30, fill=rgba(WHITE), outline=rgba(BORDER), width=3)
        p.rr((w / 2 - 54, 30, w / 2 + 54, 138), 30, fill=rgba(tint(col, 0.85)))
        icon(p, ic, w / 2, 84, 70, col, bg=tint(col, 0.85))
        p.text(w / 2, 178, name, "bold", 30, rgba(INK), anchor="mm")
        if tag:
            tw = text_w(tag, "mono", 18, 3) + 30
            p.rr((w / 2 - tw / 2, 204, w / 2 + tw / 2, 236), 16, fill=rgba(tag_col))
            p.text(w / 2, 220, tag, "mono", 18, rgba(WHITE), anchor="mm", spacing=3)
    return canvas(w, h, cb)


@lru_cache(None)
def big_icon(ic, col, size=220):
    return canvas(size, size, lambda p: (p.rr((0, 0, size - 1, size - 1), size * 0.26, fill=rgba(col)),
                                         icon(p, ic, size / 2, size / 2, size * 0.6, WHITE, bg=col)))


@lru_cache(None)
def no_parking(size=220):
    def cb(p):
        p.circ(size / 2, size / 2, size / 2 - 4, fill=rgba(WHITE), outline=rgba(RED), width=18)
        p.text(size / 2, size / 2 + 4, "P", "black", size * 0.55, rgba(BLUE), anchor="mm")
        r = size / 2 - 22
        p.line([(size / 2 - r * 0.7, size / 2 - r * 0.7), (size / 2 + r * 0.7, size / 2 + r * 0.7)], rgba(RED), 18)
    return canvas(size, size, cb)


# ------------------------------------------------------------------ S1: DAY 4 calendar (0 - 4.2)
def s_day(f, t):
    s, a, dy = trans(t, 0.02, 4.2, din=0.5, s0=0.6)
    cx, cy = CX, 960 + dy
    at = _at(cx, cy, 560, 600, s)
    put(f, day_card(), cx, cy, s, a)
    ps, pa = pop(t, 0.38, 0.45, s0=0.2)
    x, y = at(280, 300)
    put(f, big_num("4", INK, 240), x, y, ps * s, pa * a)
    for k in range(5):
        ps, pa = pop(t, 0.8 + k * 0.08, 0.3)
        x, y = at(170 + k * 55, 430)
        put(f, track_dot(k < 4), x, y, ps * s, pa * a)
        if k == 3:
            rp = prog(t, 1.3, 0.8)
            if 0 < rp < 1:
                put(f, ring(16, CYAN, 3), x, y, s * (1 + 1.2 * rp), a * (1 - rp))
    ps, pa = pop(t, 1.28, 0.36)
    x, y = at(280, 520)
    put(f, title_two("Building ", "Plan B", 40, BLUE, "bold"), x, y, ps * s, pa * a)
    ps, pa = pop(t, 2.10, 0.36)
    put(f, pill("FOR SOFTWARE ENGINEERS", WHITE, INK, size=22, h=60, icon_name="code", icon_col=CYAN, border=BORDER),
        CX, 1335 + dy, ps * s, pa * a)


# ------------------------------------------------------------------ S2: think beyond 9-to-5 (4.2 - 14.2)
@lru_cache(None)
def beyond_arrow():
    w, h = 170, 90

    def cb(p):
        p.line([(10, h / 2), (w - 40, h / 2)], rgba(GREEN), 14)
        p.poly([(w - 50, 12), (w - 6, h / 2), (w - 50, h - 12)], fill=rgba(GREEN))
    return canvas(w, h, cb)


def s_beyond(f, t):
    stage(f, t, "SOFTWARE ENGINEERS", 4.7, 14.2, INK, WHITE, "code")
    _, a, dy = trans(t, 4.7, 14.2)
    cy = 1015 + dy
    ps, pa = pop(t, 6.6, 0.4)
    put(f, side_box("job"), CX - 230, cy, ps, pa * a)
    ap = out_cubic(prog(t, 8.2, 0.45))
    if ap > 0:
        put(f, beyond_arrow(), CX - 5, cy, 1.0, a, sx=max(ap, 0.02))
    ps, pa = pop(t, 8.54, 0.42, s0=0.4)
    put(f, side_box("plan"), CX + 230, cy, ps, pa * a)
    ps, pa = pop(t, 8.3, 0.34)
    put(f, label_pill("THINK BEYOND SALARY", GREEN, WHITE, "trend", 22, 58), CX, cy - 230, ps, pa * a)
    ps, pa = pop(t, 10.06, 0.36)
    put(f, label_pill("AI IS CHANGING TECH", tint(PURPLE, 0.86), PURPLE, "spark", 22, 60), CX - 110, cy + 255, ps,
        pa * a)
    ps, pa = pop(t, 12.8, 0.36, s0=0.3)
    sh = 1 + 0.06 * math.sin(math.pi * prog(t, 13.28, 0.35))
    put(f, label_pill("FAST", YELLOW, DARK, "bolt", 22, 60), CX + 210, cy + 255, ps * sh, pa * a)


# ------------------------------------------------------------------ S3: today's app idea — the parking problem (14.25 - 21.95)
@lru_cache(None)
def problem_card():
    w, h = 800, 620

    def cb(p):
        header_label(p, w, 56, "INDIA'S DAILY PROBLEM", BLUE, 22, 5)
        p.line([(50, 420), (w - 50, 420)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


@lru_cache(None)
def car_tile(col, size=110):
    return canvas(size, size, lambda p: tile(p, size / 2, size / 2, size, col, "car"))


def s_problem(f, t):
    stage(f, t, "TODAY'S APP IDEA", 14.3, 21.95, YELLOW, DARK, "bolt")
    s, a, dy = trans(t, 15.9, 21.95)
    cx, cy = CX, 1060 + dy
    at = _at(cx, cy, 800, 620, s)
    put(f, problem_card(), cx, cy, s, a)
    # a jam of cars appears
    for k, col in enumerate([CYAN, PURPLE, DARK_YEL, GREEN, BLUE]):
        ps, pa = pop(t, 16.3 + k * 0.12, 0.32)
        jig = 4 * math.sin(t * 8 + k) * (t > 18.9)
        x, y = at(130 + k * 135 + jig, 170)
        put(f, car_tile(col), x, y, ps * s, pa * a)
    ps, pa = pop(t, 18.9, 0.38)
    x, y = at(400, 280)
    put(f, label_pill("#1 DAILY PROBLEM", ORANGE, WHITE, "warn", 22, 60), x, y, ps * s, pa * a)
    ps, pa = pop(t, 20.94, 0.45, s0=0.3)
    x, y = at(190, 520)
    put(f, big_icon("parking", BLUE, 150), x, y, ps * s, pa * a)
    ps, pa = pop(t, 21.0, 0.45, s0=0.3)
    x, y = at(500, 520)
    put(f, title_two("Parking ", "?", 84, ORANGE), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S4: BlaBlaCar — share empty seats (22.3 - 27.65)
@lru_cache(None)
def car_top(filled=(True, True, False, False)):
    w, h = 420, 560

    def cb(p):
        p.rr((20, 10, w - 20, h - 10), 150, fill=rgba(tint(CYAN, 0.7)), outline=rgba(CYAN), width=8)
        p.rr((70, 60, w - 70, 150), 50, fill=rgba(tint(CYAN, 0.88)))
        p.rr((70, h - 130, w - 70, h - 60), 40, fill=rgba(tint(CYAN, 0.88)))
        for k in range(4):
            r, c = divmod(k, 2)
            x, y = 140 + c * 140, 230 + r * 150
            if filled[k]:
                p.rr((x - 52, y - 52, x + 52, y + 52), 26, fill=rgba(WHITE))
                icon(p, "user", x, y + 4, 70, BLUE)
            else:
                p.rr((x - 52, y - 52, x + 52, y + 52), 26, fill=rgba(WHITE), outline=rgba(GREEN), width=6)
                p.text(x, y + 2, "+", "black", 64, rgba(GREEN), anchor="mm")
    return canvas(w, h, cb)


def s_seats(f, t):
    s, a, dy = trans(t, 22.3, 27.65)
    cy = 1010 + dy
    ps, pa = pop(t, 22.74, 0.42)
    put(f, label_pill("BlaBlaCar", WHITE, INK, "car", 26, 70), CX, 720 + dy, ps, pa * a)
    put(f, car_top(), CX - 150, cy + 30, s * 0.92, a)
    for k, ts in enumerate([25.98, 26.12]):
        rp = prog(t, ts, 0.8)
        if 0 < rp < 1:
            r, c = divmod(k + 2, 2)
            x = CX - 150 + (140 + c * 140 - 210) * 0.92 * s
            y = cy + 30 + (230 + r * 150 - 280) * 0.92 * s
            put(f, ring(60, GREEN, 6), x, y, 0.8 + 0.6 * rp, a * (1 - rp))
    ps, pa = pop(t, 25.98, 0.38)
    put(f, label_pill("EMPTY SEATS", tint(GREEN, 0.85), T_GREEN, "users", 22, 60), CX + 225, cy - 60, ps, pa * a)
    ps, pa = pop(t, 26.7, 0.42, s0=0.3)
    put(f, label_pill("SHARED", GREEN, WHITE, "share", 24, 66), CX + 225, cy + 40, ps, pa * a)


# ------------------------------------------------------------------ S5: same concept — "BlaBlaCar for Parking" (27.7 - 32.3)
@lru_cache(None)
def concept_title():
    w, h = 760, 260

    def cb(p):
        p.text(w / 2, 80, "BlaBlaCar for", "black", 78, rgba(INK), anchor="mm")
        p.text(w / 2, 186, "Parking", "black", 96, rgba(BLUE), anchor="mm")
    return card(w, h, 40, cb)


def s_concept(f, t):
    _, a, dy = trans(t, 27.7, 32.3)
    y = 900 + dy
    a1 = a * (1 - 0.6 * smooth(prog(t, 30.5, 0.3)))
    ps, pa = pop(t, 27.9, 0.38)
    put(f, place_tile("Empty seats", "car", CYAN), CX - 250, y, ps, pa * a1)
    ps, pa = pop(t, 28.66, 0.34)
    put(f, label_pill("SAME CONCEPT", YELLOW, DARK, "bolt", 20, 56), CX, y - 170, ps, pa * a1)
    ap = out_cubic(prog(t, 28.8, 0.4))
    if ap > 0:
        put(f, arrow_right(GREEN, 130), CX, y, 1.0, a1, sx=max(ap, 0.02))
    ps, pa = pop(t, 29.3, 0.4)
    put(f, place_tile("Empty spots", "parking", BLUE), CX + 250, y, ps, pa * a1)
    ps, pa = pop(t, 30.6, 0.5, s0=0.3)
    sh = 1 + 0.04 * math.sin(math.pi * prog(t, 31.72, 0.35))
    put(f, concept_title(), CX, 1190 + dy, ps * sh, pa * a)


# ------------------------------------------------------------------ S6: no parking at stations, markets, hospitals (32.4 - 39.05)
def s_places(f, t):
    stage(f, t, "EVERY BIG CITY", 32.64, 39.05, INK, WHITE, "globe")
    _, a, dy = trans(t, 32.64, 39.05)
    y = 950 + dy
    for k, (nm, ic, col, ts) in enumerate([("Station", "train", PURPLE, 34.0), ("Markets", "shop", DARK_YEL, 35.22),
                                          ("Hospitals", "hospital", RED, 36.02)]):
        full = t >= 37.42 + k * 0.12
        ps, pa = pop(t, ts, 0.38)
        put(f, place_tile(nm, ic, col, "FULL" if full else None), CX + (k - 1) * 265, y, ps, pa * a)
    for k in range(4):
        ps, pa = pop(t, 34.2 + k * 0.4, 0.3)
        put(f, car_tile([CYAN, BLUE, GREEN, PURPLE][k], 90), CX - 270 + k * 180, y + 225, ps, pa * a)
    ps, pa = pop(t, 38.12, 0.42, s0=2.0)
    put(f, stamp("NO SPACE!", RED), CX, y + 370, ps * 0.62, pa * a)


# ------------------------------------------------------------------ S7: hours of searching + no-parking fines (39.1 - 44.95)
@lru_cache(None)
def loop_map():
    w, h = 800, 520

    def cb(p):
        for r in range(3):
            for c in range(4):
                x0, y0 = 60 + c * 180, 60 + r * 150
                p.rr((x0, y0, x0 + 130, y0 + 100), 18, fill=rgba(PANEL))
        pts = [(160, 450), (160, 290), (520, 290), (520, 130), (700, 130), (700, 450), (160, 450)]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(math.hypot(x1 - x0, y1 - y0) // 26)
            for i in range(n):
                if i % 2 == 0:
                    a0, a1 = i / n, (i + 1) / n
                    p.line([(x0 + (x1 - x0) * a0, y0 + (y1 - y0) * a0), (x0 + (x1 - x0) * a1, y0 + (y1 - y0) * a1)],
                           rgba(tint(ORANGE, 0.4)), 7)
    return card(w, h, 38, cb)


LOOP = [(160, 450), (160, 290), (520, 290), (520, 130), (700, 130), (700, 450), (160, 450)]


def loop_pos(u):
    segs = list(zip(LOOP, LOOP[1:]))
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    d = (u % 1.0) * sum(lens)
    for (a, b), L in zip(segs, lens):
        if d <= L:
            k = d / L
            return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
        d -= L
    return LOOP[-1]


@lru_cache(None)
def challan():
    w, h = 330, 380

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 26, fill=rgba(WHITE), outline=rgba(RED), width=6)
        p.rr((2, 2, w - 2, 80), 26, fill=rgba(RED))
        p.rect((2, 50, w - 2, 80), fill=rgba(RED))
        p.text(w / 2, 44, "CHALLAN", "mono", 28, rgba(WHITE), anchor="mm", spacing=6)
        p.text(w / 2, 168, "₹₹₹", "black", 96, rgba(RED), anchor="mm")
        p.text(w / 2, 248, "NO-PARKING FINE", "mono", 18, rgba(MUTED), anchor="mm", spacing=3)
        for k, ww in enumerate([230, 180, 210]):
            p.rr((50, 280 + k * 28, 50 + ww, 292 + k * 28), 6, fill=rgba(SKEL))
    return canvas(w, h, cb)


def s_search(f, t):
    s, a, dy = trans(t, 39.1, 44.95)
    cx, cy = CX, 960 + dy
    at = _at(cx, cy, 800, 520, s)
    a_map = a * (1 - 0.45 * smooth(prog(t, 42.1, 0.3)))
    put(f, loop_map(), cx, cy, s, a_map)
    u = (t - 39.3) / 2.4
    if t > 39.3:
        x, y = at(*loop_pos(u))
        put(f, car_tile(CYAN, 86), x, y, s, a_map)
    ps, pa = pop(t, 40.46, 0.38)
    put(f, label_pill("HOURS OF SEARCHING", ORANGE, WHITE, "clock", 22, 60), CX, cy - 300 * s, ps, pa * a)
    ps, pa = pop(t, 42.12, 0.45, s0=0.3)
    put(f, no_parking(220), CX - 200, cy + 30, ps, pa * a)
    ps, pa = pop(t, 43.46, 0.45, s0=0.3)
    shake = 8 * math.sin((t - 43.46) * 40) * (1 - prog(t, 43.46, 0.5)) if t > 43.46 else 0
    put(f, challan(), CX + 170 + shake, cy + 30, ps, pa * a)


# ------------------------------------------------------------------ S8: list your space (45.0 - 52.3)
SPACES = [("Space in front of home", "home", GREEN, 47.20), ("Empty plot", "pin", ORANGE, 49.16),
          ("Space in front of shop", "shop", DARK_YEL, 49.82)]


@lru_cache(None)
def list_card():
    w, h = 820, 620

    def cb(p):
        p.rr((0, 0, w - 1, 110), 38, fill=rgba(BLUE))
        p.rect((0, 70, w - 1, 110), fill=rgba(BLUE))
        icon(p, "parking", 74, 55, 60, WHITE, bg=BLUE)
        p.text(124, 42, "List your space", "bold", 36, rgba(WHITE), anchor="lm")
        p.text(125, 80, "earn from empty parking", "semi", 24, rgba(tint(BLUE, 0.75)), anchor="lm")
    return card(w, h, 38, cb)


@lru_cache(None)
def space_row(k, listed=False):
    name, ic, col, _ = SPACES[k]
    w, h = 740, 130

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 26, fill=rgba(PANEL), outline=rgba(LINE), width=2)
        tile(p, 66, h / 2, 84, col, ic)
        p.text(128, h / 2, name, "bold", 31, rgba(INK), anchor="lm")
        bx = w - 190
        if listed:
            p.rr((bx, h / 2 - 32, w - 26, h / 2 + 32), 32, fill=rgba(tint(GREEN, 0.85)))
            icon(p, "check", bx + 38, h / 2, 34, GREEN)
            p.text(bx + 64, h / 2, "LISTED", "mono", 20, rgba(T_GREEN), anchor="lm", spacing=2)
        else:
            p.rr((bx, h / 2 - 32, w - 26, h / 2 + 32), 32, fill=rgba(BLUE))
            p.text((bx + w - 26) / 2, h / 2, "+ LIST", "mono", 22, rgba(WHITE), anchor="mm", spacing=3)
    return canvas(w, h, cb)


def s_list(f, t):
    stage(f, t, "THE APP", 45.02, 52.3, BLUE, WHITE, "parking")
    s, a, dy = trans(t, 45.4, 52.3)
    cx, cy = CX, 1060 + dy
    at = _at(cx, cy, 820, 620, s)
    put(f, list_card(), cx, cy, s, a)
    for k, (_, _, _, ts) in enumerate(SPACES):
        ps, pa = pop(t, ts, 0.38)
        tl = 51.14 + k * 0.18
        listed = t >= tl
        bump = 1 + 0.04 * math.sin(math.pi * prog(t, tl, 0.3))
        x, y = at(410, 200 + k * 145)
        put(f, space_row(k, listed), x, y, ps * s * bump, pa * a)
    ps, pa = pop(t, 46.38, 0.34)
    x, y = at(650, 55)
    put(f, label_pill("ANYONE", WHITE, BLUE, "users", 18, 46), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S9: driver finds the nearest spot + directions (52.35 - 59.7)
MAP_W, MAP_H = 820, 640
PINS = [(150, 150), (640, 120), (300, 300), (700, 420), (210, 520)]
NEAREST = 2
CAR_AT = (560, 560)
ROUTE = [(560, 560), (560, 400), (300, 400), (300, 330)]


@lru_cache(None)
def city_map():
    def cb(p):
        p.rr((24, 24, MAP_W - 24, MAP_H - 24), 26, fill=rgba((236, 242, 236)))
        for x in (230, 450, 620):
            p.rect((x - 16, 24, x + 16, MAP_H - 24), fill=rgba(WHITE))
        for y in (220, 400):
            p.rect((24, y - 16, MAP_W - 24, y + 16), fill=rgba(WHITE))
        for (x0, y0, x1, y1) in [(40, 40, 200, 190), (260, 40, 420, 190), (480, 40, 590, 190), (650, 40, 790, 190),
                                 (40, 250, 200, 370), (480, 250, 590, 370), (650, 250, 790, 370),
                                 (40, 430, 200, 600), (260, 430, 420, 600), (650, 430, 790, 600)]:
            p.rr((x0, y0, x1, y1), 14, fill=rgba((214, 226, 216)))
        p.rr((262, 250, 418, 370), 14, fill=rgba(tint(GREEN, 0.7)))
    return card(MAP_W, MAP_H, 38, cb)


@lru_cache(None)
def pin_sprite(col, size=90):
    return canvas(size, size, lambda p: icon(p, "pin", size / 2, size / 2, size * 0.92, col))


@lru_cache(None)
def p_badge(col):
    return canvas(52, 52, lambda p: (p.rr((0, 0, 51, 51), 12, fill=rgba(col)),
                                     p.text(26, 28, "P", "black", 34, rgba(WHITE), anchor="mm")))


def route_sprite(pr):
    def cb(p):
        segs = list(zip(ROUTE, ROUTE[1:]))
        lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
        left = pr * sum(lens)
        pts = [ROUTE[0]]
        for (a, b), L in zip(segs, lens):
            if left <= 0:
                break
            k = min(1.0, left / L)
            pts.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
            left -= L
        if len(pts) >= 2:
            p.line(pts, rgba(BLUE), 12)
    return canvas(MAP_W, MAP_H, cb)


def s_map(f, t):
    stage(f, t, "DRIVER NEEDS PARKING", 52.5, 59.7, ORANGE, WHITE, "car")
    s, a, dy = trans(t, 52.6, 59.7)
    cx, cy = CX, 1060 + dy
    at = _at(cx, cy, MAP_W, MAP_H, s)
    put(f, city_map(), cx, cy, s, a)
    rp = smooth(prog(t, 58.5, 0.7))
    if rp > 0:
        put(f, route_sprite(rp), cx, cy, s, a)
    for k, (px, py) in enumerate(PINS):
        ps, pa = pop(t, 54.52 + k * 0.1, 0.34)
        near = k == NEAREST and t >= 57.0
        x, y = at(px, py - 30)
        put(f, pin_sprite(GREEN if near else BLUE, 100 if near else 84), x, y, ps * s, pa * a)
        if near:
            rr = prog(t, 57.0, 0.9)
            if rr < 1:
                put(f, ring(50, GREEN, 6), x, y + 30 * s, s * (0.8 + 1.0 * rr), a * (1 - rr))
    ps, pa = pop(t, 53.2, 0.38)
    x, y = at(*CAR_AT)
    put(f, car_tile(CYAN, 96), x, y, ps * s, pa * a)
    ps, pa = pop(t, 57.0, 0.36)
    x, y = at(300, 230)
    put(f, label_pill("NEAREST", GREEN, WHITE, "parking", 18, 46), x, y - 40 * s, ps * s, pa * a)
    ps, pa = pop(t, 58.5, 0.36)
    put(f, label_pill("DIRECTIONS", BLUE, WHITE, "trend", 20, 54), CX + 230 * s, cy + (MAP_H / 2 + 40) * s, ps, pa * a)


# ------------------------------------------------------------------ S10: no payment gateway — UPI or cash to the owner (59.8 - 67.4)
@lru_cache(None)
def gateway_box():
    w, h = 520, 170

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 30, fill=rgba(PANEL), outline=rgba(BORDER), width=3)
        tile(p, 86, h / 2, 100, (150, 160, 180), "chip")
        p.text(160, h / 2 - 20, "Payment Gateway", "bold", 36, rgba(INK2), anchor="lm")
        p.text(161, h / 2 + 24, "complex setup", "semi", 26, rgba(MUTED), anchor="lm")
    return canvas(w, h, cb)


@lru_cache(None)
def strike(w=540):
    return canvas(w, 24, lambda p: p.line([(10, 12), (w - 10, 12)], rgba(RED), 12))


def s_pay(f, t):
    _, a, dy = trans(t, 59.8, 67.4)
    a_gw = a * (1 - 0.5 * smooth(prog(t, 63.2, 0.3)))
    ps, pa = pop(t, 61.58, 0.38)
    put(f, gateway_box(), CX, 760 + dy, ps, pa * a_gw)
    sp = out_cubic(prog(t, 62.46, 0.3))
    if sp > 0:
        put(f, strike(), CX - 270 * (1 - sp), 760 + dy, 1.0, a_gw, sx=max(sp, 0.02))
        ps, pa = pop(t, 62.5, 0.34)
        put(f, label_pill("NOT NEEDED", RED, WHITE, "cross", 20, 52), CX + 190, 850 + dy, ps, pa * a_gw)
    # driver -> owner, paid by UPI or cash
    ps, pa = pop(t, 63.32, 0.38)
    put(f, place_tile("Driver", "car", CYAN), CX - 260, 1130 + dy, ps, pa * a)
    ps, pa = pop(t, 64.82, 0.38)
    put(f, place_tile("Owner", "home", GREEN), CX + 260, 1130 + dy, ps, pa * a)
    ap = out_cubic(prog(t, 63.8, 0.5))
    if ap > 0:
        put(f, arrow_right(GREEN, 170), CX, 1130 + dy, 1.0, a, sx=max(ap, 0.02))
    ps, pa = pop(t, 65.44, 0.4, s0=0.3)
    put(f, label_pill("UPI", BLUE, WHITE, "rupee", 26, 70), CX - 95, 1340 + dy, ps, pa * a)
    ps, pa = pop(t, 66.28, 0.4, s0=0.3)
    put(f, label_pill("CASH", GREEN, WHITE, "rupee", 26, 70), CX + 105, 1340 + dy, ps, pa * a)
    ps, pa = pop(t, 66.6, 0.34)
    put(f, label_pill("DIRECT", tint(GREEN, 0.85), T_GREEN, "check", 18, 46), CX, 1030 + dy, ps, pa * a)


# ------------------------------------------------------------------ S11: MVP in a few days with Claude + Cursor (67.5 - 73.05)
@lru_cache(None)
def mvp_card():
    w, h = 820, 560

    def cb(p):
        header_label(p, w, 56, "BUILD THE MVP", BLUE, 22, 6)
        p.line([(50, 330), (w - 50, 330)], rgba(LINE), 2, caps=False)
        p.rr((60, 380, w - 60, 500), 22, fill=rgba(INK))
        for k, (ww, col) in enumerate([(380, PURPLE), (520, CYAN), (300, GREEN)]):
            p.rr((90, 402 + k * 30, 90 + ww, 414 + k * 30), 6, fill=rgba(col))
    return card(w, h, 38, cb)


def s_mvp(f, t):
    s, a, dy = trans(t, 67.5, 73.05)
    cx, cy = CX, 1020 + dy
    at = _at(cx, cy, 820, 560, s)
    put(f, mvp_card(), cx, cy, s, a)
    ps, pa = pop(t, 68.64, 0.42, s0=0.3)
    x, y = at(410, 330)
    put(f, label_pill("MVP", YELLOW, DARK, "bolt", 26, 68), x, y, ps * s, pa * a)
    for nm, ic, col, rx, ts in [("Claude", "spark", PURPLE, 140, 69.6), ("Cursor", "code", INK, 400, 70.26)]:
        ps, pa = pop(t, ts, 0.36)
        x, y = at(rx, 190)
        put(f, node(nm, ic, col), x, y, ps * s * 0.9, pa * a)
    ps, pa = pop(t, 70.0, 0.3)
    x, y = at(270, 190)
    put(f, plus_small(), x, y, ps * s, pa * a)
    ap = out_cubic(prog(t, 71.2, 0.35))
    if ap > 0:
        x, y = at(540, 190)
        put(f, arrow_right(GREEN, 80), x, y, s, a, sx=max(ap, 0.02))
    ps, pa = pop(t, 71.74, 0.38)
    x, y = at(680, 190)
    put(f, node("Few days", "clock", DARK_YEL), x, y, ps * s * 0.9, pa * a)
    ps, pa = pop(t, 72.06, 0.34)
    x, y = at(660, 440)
    put(f, label_pill("CODE DONE", GREEN, WHITE, "check", 18, 46), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S12: comment "PARKING" -> system design guide in DM (73.1 - 81.9)
@lru_cache(None)
def design_doc():
    w, h = 800, 330

    def cb(p):
        tile(p, 90, 90, 100, BLUE, "parking")
        p.text(170, 66, "System Design", "bold", 42, rgba(INK), anchor="lm")
        p.text(171, 114, "+ step-by-step guide", "semi", 30, rgba(BLUE), anchor="lm")
        for k, (lab, col) in enumerate([("App", CYAN), ("API", PURPLE), ("Maps", GREEN), ("DB", DARK_YEL)]):
            x = 60 + k * 180
            p.rr((x, 190, x + 150, 260), 18, fill=rgba(tint(col, 0.85)), outline=rgba(col), width=3)
            p.text(x + 75, 225, lab, "bold", 28, rgba(INK), anchor="mm")
            if k < 3:
                p.line([(x + 152, 225), (x + 178, 225)], rgba(MUTED), 4)
        p.rr((60, 290, 520, 304), 7, fill=rgba(SKEL))
    return card(w, h, 36, cb)


@lru_cache(None)
def dm_bubble():
    w, h = 660, 150

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 40, fill=rgba(BLUE))
        icon(p, "chat", 70, h / 2, 64, WHITE, bg=BLUE)
        p.text(126, 52, "DM: Parking App Guide", "bold", 34, rgba(WHITE), anchor="lm")
        p.text(127, 102, "+ system design · sent!", "semi", 28, rgba(tint(BLUE, 0.8)), anchor="lm")
    return canvas(w, h, cb)


def s_comment(f, t):
    s, a, dy = trans(t, 74.9, 81.9)
    put(f, design_doc(), CX, 880 + dy, s, a)
    s2, a2, dy2 = trans(t, 77.9, 81.9)
    word = "PARKING"
    typed = word[:max(0, min(len(word), int((t - 78.8) / 0.08) + 1))] if t >= 78.8 else ""
    put(f, comment_box(typed, t >= 79.5), CX, 1150 + dy2, s2, a2)
    ps, pa = pop(t, 79.55, 0.36, s0=0.3)
    put(f, label_pill("COMMENTED “PARKING”", YELLOW, DARK, "check", 22, 60), CX - 150, 1265 + dy2, ps, pa * a2)
    ps, pa = pop(t, 80.74, 0.45, s0=0.3)
    put(f, dm_bubble(), CX + 50, 1380 + dy2, ps, pa * a2)
    # before the doc: "system design + guide" ask
    ps, pa = pop(t, 73.92, 0.36)
    _, a0, _ = trans(t, 73.9, 75.2)
    put(f, label_pill("FULL GUIDE?", WHITE, INK, "book", 26, 70), CX, 1000, ps, pa * a0)


# ------------------------------------------------------------------ S13: outro — final part Day 5 (82.0 - 89.9)
def s_outro(f, t):
    t0 = 82.0
    s, a, dy = trans(t, t0, None, din=0.6, s0=0.5)
    bob = 5 * math.sin((t - t0) * 2.0) * prog(t, 83.0, 1.0)
    cy = 860 + dy + bob
    tr, k = 82.15, 0
    while tr < t and k < 8:
        pr = prog(t, tr, 1.4)
        if 0 < pr < 1:
            put(f, ring(165, CYAN if k % 2 == 0 else GREEN, 5), CX, cy, s * (0.98 + 0.5 * out_cubic(pr)),
                (1 - pr) * 0.45 * a)
        tr += 1.5
        k += 1
    put(f, logo_shadow(330), CX, cy, s, a * 0.9)
    put(f, logo(330), CX, cy, s, a)
    ps, pa = pop(t, 82.72, 0.4, s0=0.4)
    put(f, label_pill("FINAL PART: DAY 5", YELLOW, DARK, "star", 22, 60), CX, 640, ps, pa)
    ps, pa = pop(t, 82.3, 0.4)
    put(f, handle_pill(42), CX, 1100, ps, pa)
    for kk in range(5):
        ps, pa = pop(t, 83.6 + kk * 0.08, 0.3)
        put(f, track_dot(kk < 4), CX - 110 + kk * 55, 1195, ps, pa)
        if kk == 4:
            rp = prog(t, 84.08, 0.9)
            if 0 < rp < 1:
                put(f, ring(16, YELLOW, 4), CX - 110 + kk * 55, 1195, 1 + 1.4 * rp, 1 - rp)
    ps, pa = pop(t, 84.9, 0.42, s0=0.4)
    press = prog(t, 85.80, 0.2)
    kk2 = 1 - 0.07 * math.sin(press * math.pi)
    put(f, follow_btn(press > 0.5), CX, 1310, ps * kk2, pa)
    rp = prog(t, 85.82, 0.6)
    if 0 < rp < 1:
        put(f, ring(100, BLUE, 5), CX, 1310, 0.9 + 1.0 * rp, (1 - rp) * 0.6)
    cm = out_cubic(prog(t, 85.25, 0.5))
    if cm > 0:
        leave = out_cubic(prog(t, 86.5, 0.5))
        cx = lerp(CX + 330, CX + 70, cm) + 120 * leave
        cyy = lerp(1520, 1330, cm) + 160 * leave
        put(f, cursor(), cx, cyy, 1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - leave))
    ps, pa = pop(t, 87.3, 0.4)
    put(f, label_pill("COMMENT “PARKING” FOR THE GUIDE", tint(BLUE, 0.88), BLUE, "chat", 20, 56), CX, 1420,
        ps, pa)


SCENES = [
    (0.0, 4.25, s_day),
    (4.2, 14.25, s_beyond),
    (14.25, 22.0, s_problem),
    (22.3, 27.7, s_seats),
    (27.7, 32.35, s_concept),
    (32.4, 39.1, s_places),
    (39.1, 45.0, s_search),
    (45.0, 52.35, s_list),
    (52.35, 59.75, s_map),
    (59.8, 67.45, s_pay),
    (67.5, 73.1, s_mvp),
    (73.1, 81.95, s_comment),
    (82.0, 90.0, s_outro),
]

EVENTS = [
    (0.05, "shimmer", -2, 0.5, {}), (0.38, "pop", -3, 0.5, {"pitch": 0.75}),
    (4.68, "whoosh", 0, 0.5, {}), (6.6, "pop", -7, 0.35, {}), (8.2, "rise", -6, 0.5, {}),
    (8.54, "pop", -6, 0.65, {"pitch": 1.2}), (10.06, "pop", -8, 0.4, {"pitch": 1.3}), (12.8, "click", -6, 0.6, {}),
    (14.28, "whoosh", -1, 0.5, {}), (16.3, "click", -9, 0.4, {}), (18.9, "alert", -5, 0.5, {}),
    (20.94, "pop", -4, 0.5, {"pitch": 0.8}),
    (22.28, "whoosh", -1, 0.5, {}), (22.74, "pop", -6, 0.5, {}), (26.7, "chime", -6, 0.6, {}),
    (27.68, "whoosh", -1, 0.5, {}), (28.8, "swipe", -7, 0.5, {}), (30.6, "rise", -5, 0.5, {}),
    (32.38, "whoosh", -1, 0.5, {}), (34.0, "pop", -8, 0.35, {}), (35.22, "pop", -8, 0.5, {"pitch": 1.15}),
    (36.02, "pop", -8, 0.65, {"pitch": 1.3}), (38.12, "alert", -4, 0.5, {}),
    (39.08, "whoosh", -1, 0.5, {}), (42.12, "pop", -5, 0.35, {"pitch": 0.8}), (43.46, "alert", -4, 0.6, {}),
    (44.98, "whoosh", -1, 0.5, {}), (47.2, "pop", -8, 0.4, {}), (49.16, "pop", -8, 0.5, {"pitch": 1.15}),
    (49.82, "pop", -8, 0.6, {"pitch": 1.3}), (51.14, "click", -5, 0.5, {}),
    (52.33, "whoosh", -1, 0.5, {}), (54.52, "pop", -8, 0.5, {"pitch": 1.2}), (57.0, "chime", -6, 0.4, {}),
    (58.5, "rise", -6, 0.5, {}),
    (59.78, "whoosh", -1, 0.5, {}), (62.46, "swipe", -5, 0.5, {}), (65.44, "pop", -6, 0.4, {}),
    (66.28, "pop", -6, 0.6, {"pitch": 1.2}),
    (67.48, "whoosh", -1, 0.5, {}), (68.64, "pop", -5, 0.5, {"pitch": 0.9}), (71.74, "rise", -6, 0.6, {}),
    (73.08, "whoosh", -1, 0.5, {}), (78.8, "click", -6, 0.5, {}), (79.5, "pop", -6, 0.4, {"pitch": 1.2}),
    (80.74, "chime", -5, 0.6, {}),
    (81.98, "whoosh", -1, 0.5, {}), (82.1, "shimmer", 0, 0.5, {}), (82.72, "pop", -5, 0.5, {}),
    (85.8, "click", -1, 0.55, {}), (87.3, "pop", -7, 0.5, {"pitch": 1.1}),
]
