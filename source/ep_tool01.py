"""AWESOME TOOLS · DAY 1 — TurtleReels promo (turtlereels.com).

Same look as Plan B / Awesome Repos: light theme, isometric plate, white cards, white pop-up captions, logo outro.
Voice: episodes/tool01/voice.mp3 (ElevenLabs Viraj, 69.96 s). Timings: ep_tool01_timing.py (from words.json).
Real UI: output/promotions/TurtleReels/elements/hd/*.png. Real renders (Ayush's account) play inside phone frames:
work/tool01_clips/c1..c3/*.jpg (15 fps, 540x960, extracted from 'clip of sample video').
"""
import math
import os
from functools import lru_cache

from PIL import Image, ImageDraw

from gfx import (BLUE, BORDER, CYAN, DARK, DARK_YEL, GREEN, INK, INK2, LINE, MUTED, ORANGE, PANEL, PURPLE, SKEL,
                 SM, T_GREEN, WHITE, YELLOW, canvas, card, clamp, icon, lerp, out_back, out_cubic, pop, prog, put,
                 rgba, smooth, text_w, tile, tint, trans)
from scenes import CX, big_num, cursor, follow_btn, handle_pill, header_label, logo, logo_shadow, pill, ring
from ep_day01 import _at, arrow_right, coin
from ep_day02 import avatar, big_cross, node, stage, stamp, title_two
from ep_day03 import comment_box, label_pill, num_text
from ep_tool01_timing import CAP_END, K, PHRASES, TOTAL_LEN, VOICE_LEN  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.path.join(ROOT, "episodes", "tool01", "voice.mp3")
HD = os.path.join(ROOT, "output", "promotions", "TurtleReels", "elements", "hd")
CLIPS = os.path.join(ROOT, "work", "tool01_clips")
HEADER = "COMPUTER HUB · AWESOME TOOLS · DAY 1"
MINT = (32, 200, 140)          # TurtleReels brand green (darkened a bit for white cards)
MINT_BG = (46, 230, 166)
RED = (226, 64, 64)
YT_RED = (255, 0, 51)
NIGHT = (24, 30, 58)


# ------------------------------------------------------------------ shared sprites
@lru_cache(None)
def pic(name, w, r=22):
    """An HD element from elements/hd, resized to width w with rounded corners."""
    im = Image.open(os.path.join(HD, name + ".png")).convert("RGBA")
    h = int(round(w * im.height / im.width))
    im = im.resize((w, h), Image.LANCZOS)
    if r:
        m = Image.new("L", (w * 2, h * 2), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, fill=255)
        a = Image.composite(im.getchannel("A"), Image.new("L", im.size, 0), m.resize((w, h), Image.LANCZOS))
        im.putalpha(a)
    return im


@lru_cache(None)
def pic_card(name, w, r=26):
    im = pic(name, w, r)
    out = card(w, im.height, r)
    out.alpha_composite(im, (SM, SM))
    return out


@lru_cache(None)
def browser(name, url, w=900):
    im = pic(name, w - 36, 14)
    bar = 70
    h = bar + 18 + im.height + 18

    def cb(p):
        p.rr((0, 0, w - 1, bar), 34, fill=rgba(PANEL))
        p.rect((0, 38, w - 1, bar), fill=rgba(PANEL))
        p.line([(0, bar), (w, bar)], rgba(LINE), 2, caps=False)
        for k, c in enumerate([(255, 96, 92), (255, 190, 50), (40, 200, 70)]):
            p.circ(38 + k * 26, 35, 8, fill=rgba(c))
        p.rr((130, 16, w - 70, 54), 19, fill=rgba(WHITE), outline=rgba(LINE), width=2)
        icon(p, "shield", 154, 35, 20, GREEN)
        p.text(176, 35, url, "monor", 20, rgba(INK2), anchor="lm")
    out = card(w, h, 34, cb)
    out.alpha_composite(im, (SM + 18, SM + bar + 18))
    return out


# --- phone with a real TurtleReels render playing inside ---------------------------------------
PH_W, PH_H, PH_PAD = 330, 640, 12


@lru_cache(None)
def phone_body(shorts_ui=True):
    w, h = PH_W, PH_H

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), 48, fill=rgba((18, 20, 28)))
        p.rr((w / 2 - 46, 22, w / 2 + 46, 34), 6, fill=rgba((40, 44, 56)))
    return card(w, h, 48, cb, fill=(18, 20, 28), border=(18, 20, 28))


@lru_cache(None)
def _screen_mask():
    iw, ih = PH_W - 2 * PH_PAD, PH_H - 2 * PH_PAD
    m = Image.new("L", (iw * 2, ih * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, iw * 2 - 1, ih * 2 - 1], radius=38 * 2, fill=255)
    return m.resize((iw, ih), Image.LANCZOS)


@lru_cache(maxsize=96)
def clip_frame(k, n):
    iw, ih = PH_W - 2 * PH_PAD, PH_H - 2 * PH_PAD
    im = Image.open(os.path.join(CLIPS, f"c{k}", f"{n:04d}.jpg")).convert("RGBA")
    im = im.resize((iw, int(iw * 960 / 540)), Image.BILINEAR)
    top = (im.height - ih) // 2
    im = im.crop((0, top, iw, top + ih))
    im.putalpha(_screen_mask())
    return im


@lru_cache(None)
def shorts_overlay():
    """Simple YouTube-Shorts-like icons on the right of the screen."""
    iw, ih = PH_W - 2 * PH_PAD, PH_H - 2 * PH_PAD

    def cb(p):
        for k, ic in enumerate(["heart", "chat", "share"]):
            y = ih - 250 + k * 70
            p.circ(iw - 34, y, 22, fill=(0, 0, 0, 90))
            icon(p, ic, iw - 34, y, 24, WHITE, bg=(30, 30, 30))
        p.rr((14, ih - 54, 150, ih - 22), 16, fill=(0, 0, 0, 110))
        p.text(30, ih - 38, "@your_channel", "bold", 16, (255, 255, 255, 230), anchor="lm")
    return canvas(iw, ih, cb)


@lru_cache(maxsize=24)
def phone_still(k, n, ui):
    out = phone_body().copy()
    out.alpha_composite(clip_frame(k, n), (SM + PH_PAD, SM + PH_PAD))
    if ui:
        out.alpha_composite(shorts_overlay(), (SM + PH_PAD, SM + PH_PAD))
    return out


def phone(f, t, k, t0, cx, cy, s=1.0, a=1.0, ui=True, speed=1.0):
    """Phone playing clip k (starts at t0). 345 frames @15 fps, loops."""
    n = int(max(0.0, (t - t0) * 15 * speed)) % 345 + 1
    put(f, phone_still(k, n, ui), cx, cy, s, a)


@lru_cache(None)
def chip(txt, col, fg=WHITE, size=26, h=66, ic=None):
    return pill(txt, col, fg, kind="bold", size=size, spacing=0, h=h, icon_name=ic, icon_col=fg)


@lru_cache(None)
def no_chip(txt):
    w, h = 250, 70

    def cb(p):
        p.rr((1, 1, w - 2, h - 2), h / 2, fill=rgba(WHITE), outline=rgba(tint(RED, 0.5)), width=3)
        p.circ(36, h / 2, 20, fill=rgba(RED))
        icon(p, "cross", 36, h / 2, 22, WHITE, bg=RED)
        p.text(68, h / 2, txt, "bold", 28, rgba(INK), anchor="lm")
    return canvas(w, h, cb)


def _bump(t, t0, k=0.06, d=0.35):
    return 1 + k * math.sin(math.pi * prog(t, t0, d))


@lru_cache(None)
def views_card(v):
    w, h = 300, 150

    def cb(p):
        p.text(28, 40, "VIEWS · 28 DAYS", "mono", 17, rgba(MUTED), anchor="lm", spacing=2)
        p.text(28, 96, f"{v:,}", "black", 56, rgba(INK), anchor="lm")
        icon(p, "trend", w - 44, 96, 40, GREEN)
    return card(w, h, 30, cb)


@lru_cache(None)
def tr_logo(size):
    return pic("00_logo_mark_512", size, 0)


# ------------------------------------------------------------------ S1: hook — faceless channels, lakhs of views
def s_hook(f, t):
    s, a, dy = trans(t, 0.05, K["s1_end"], din=0.5, s0=0.7)
    phone(f, t, 2, -11.0, CX + 60, 1040 + dy, s * 1.12, a)
    for txt, key, x, y in [("No face", "face", CX - 330, 860), ("No editing", "edit", CX + 330, 990)]:
        ps, pa = pop(t, K[key], 0.4, s0=0.3)
        put(f, no_chip(txt), x, y + dy, ps * _bump(t, K[key] + 0.35), pa * a)
    ps, pa = pop(t, K["views"], 0.45, s0=0.3)
    v = int(71016 * smooth(prog(t, K["views"], 1.2)))
    put(f, views_card(max(v, 0)), CX - 300, 1330 + dy, ps, pa * a)
    ps, pa = pop(t, K["views"] + 0.5, 0.36)
    put(f, label_pill("ONE REAL CHANNEL", tint(GREEN, 0.85), T_GREEN, "check", 16, 42), CX - 300, 1440 + dy, ps,
        pa * a)



# ------------------------------------------------------------------ S2: Awesome Tools · Day 1 → TurtleReels
@lru_cache(None)
def tool_day_card():
    w, h = 560, 600

    def cb(p):
        p.rr((0, 0, w - 1, 150), 38, fill=rgba(MINT))
        p.rect((0, 100, w - 1, 150), fill=rgba(MINT))
        for x in (150, w - 150):
            p.circ(x, 0, 18, fill=rgba(WHITE))
            p.circ(x, 0, 9, fill=rgba((16, 130, 90)))
        p.text(w / 2, 82, "DAY", "mono", 46, rgba(WHITE), anchor="mm", spacing=14)
        p.line([(50, 470), (w - 50, 470)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


def s_reveal(f, t):
    t_in, t_out = K["s1_end"], K["s2_end"]
    s, a, dy = trans(t, t_in, K["tool"] - 0.05, din=0.5, s0=0.6)
    cx, cy = CX, 1000 + dy
    at = _at(cx, cy, 560, 600, s)
    put(f, tool_day_card(), cx, cy, s, a)
    ps, pa = pop(t, t_in + 0.25, 0.45, s0=0.2)
    x, y = at(280, 300)
    put(f, big_num("1", INK, 240), x, y, ps * s, pa * a)
    ps, pa = pop(t, K["awesome"], 0.4)
    x, y = at(280, 530)
    put(f, title_two("Awesome ", "Tools", 46, MINT, "bold"), x, y, ps * s, pa * a)
    # the tool itself
    s2, a2, dy2 = trans(t, K["tool"], t_out, din=0.5, s0=0.6)
    tr = out_cubic(prog(t, K["tool"], 0.8))
    for k in range(3):
        rp = prog(t, K["turtlereels"] + k * 0.35, 1.2)
        if 0 < rp < 1:
            put(f, ring(150, MINT_BG, 6), CX, 880 + dy2, 0.8 + 0.7 * rp, (1 - rp) * 0.6 * a2)
    put(f, logo_shadow(260), CX, 880 + dy2, s2, a2 * 0.8)
    put(f, tr_logo(260), CX, 880 + dy2 - 6 * math.sin(t * 2.2) * tr, s2, a2)
    ps, pa = pop(t, K["turtlereels"], 0.45, s0=0.4)
    put(f, pic_card("01_wordmark_card", 640, 30), CX, 1180 + dy2, ps * s2, pa * a2)


# ------------------------------------------------------------------ S3: code draws mandala, spiral, geometric art
@lru_cache(None)
def code_chip():
    w, h = 400, 84

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(INK))
        p.text(36, h / 2, ">>>", "mono", 26, rgba(MINT_BG), anchor="lm")
        p.text(96, h / 2, "turtle.draw()", "mono", 30, rgba(WHITE), anchor="lm")
    return canvas(w, h, cb)


def s_code(f, t):
    _, a, dy = trans(t, K["s2_end"], K["s3_end"])
    ps, pa = pop(t, K["ai"], 0.4)
    put(f, code_chip(), CX, 640 + dy, ps, pa * a)
    for k, (key, x, rot) in enumerate([("mandala", CX - 330, -1), ("spiral", CX, 0), ("geometric", CX + 330, 1)]):
        ps, pa = pop(t, K[key], 0.45, s0=0.4)
        phone(f, t, [3, 2, 1][k], K[key] - 9.0, x, 1080 + dy + 40 * abs(rot), ps * 0.9, pa * a, ui=False)
        lp, la = pop(t, K[key] + 0.2, 0.34)
        put(f, chip(["Mandala", "Spiral", "Geometric Art"][k], [PURPLE, CYAN, MINT][k], WHITE, 24, 60),
            x, 1430 + dy + 40 * abs(rot), lp, la * a)
    ps, pa = pop(t, K["khud"], 0.4)
    put(f, label_pill("AUTOMATIC", GREEN, WHITE, "bolt", 22, 58), CX, 1560 + dy, ps, pa * a)


# ------------------------------------------------------------------ S4: unique visuals, colors, quotes, music
def s_unique(f, t):
    s, a, dy = trans(t, K["s3_end"], K["s4_end"])
    put(f, pic_card("13_your_videos", 880, 26), CX, 940 + dy, s, a)
    for k, (txt, key, col, ic) in enumerate([("Unique visuals", "visuals", PURPLE, "spark"),
                                              ("New colors", "colors", ORANGE, "star"),
                                              ("Quotes", "quotes", BLUE, "chat"),
                                              ("Copyright-free music", "music", GREEN, "check")]):
        ps, pa = pop(t, K[key], 0.38, s0=0.3)
        x = CX - 210 + (k % 2) * 420
        y = 1370 + (k // 2) * 90
        put(f, chip(txt, col, WHITE, 26, 70, ic), x, y + dy, ps * _bump(t, K[key] + 0.3), pa * a)


# ------------------------------------------------------------------ S5: title, description, hashtags, auto-post
@lru_cache(None)
def yt_tile():
    return node("YouTube", "play", YT_RED, w=240)


def s_auto(f, t):
    s, a, dy = trans(t, K["s4_end"], K["s5_end"])
    put(f, pic_card("03_auto_title_panel", 560, 26), CX - 175, 1020 + dy, s, a)
    for k, (txt, key) in enumerate([("TITLE", "title"), ("DESCRIPTION", "desc"), ("HASHTAGS", "hashtags")]):
        ps, pa = pop(t, K[key], 0.36, s0=0.3)
        put(f, chip(txt, MINT, WHITE, 22, 58, "check"), CX + 330, 820 + k * 90 + dy, ps, pa * a)
    ps, pa = pop(t, K["youtube"], 0.42, s0=0.3)
    put(f, pic("16_connect_youtube_btn", 360, 0), CX + 300, 1150 + dy, ps, pa * a)
    rp = prog(t, K["youtube"] + 0.1, 0.7)
    if 0 < rp < 1:
        put(f, ring(110, YT_RED, 5), CX + 300, 1150 + dy, 0.8 + 0.7 * rp, (1 - rp) * 0.7 * a)
    ps, pa = pop(t, K["autopilot"], 0.45, s0=0.3)
    put(f, chip("AUTOPILOT ON", GREEN, WHITE, 30, 84, "bolt"), CX, 1440 + dy, ps * _bump(t, K["autopilot"] + 0.4), pa * a)


# ------------------------------------------------------------------ S6: choose a style, set a schedule
def s_choose(f, t):
    s, a, dy = trans(t, K["s5_end"], K["s6_end"])
    put(f, browser("12_create_autopilot", "turtlereels.com", 900), CX, 1050 + dy, s, a)
    ps, pa = pop(t, K["style"], 0.4)
    put(f, label_pill("1 · PICK A STYLE", PURPLE, WHITE, "spark", 22, 58), CX - 200, 640 + dy, ps, pa * a)
    ps, pa = pop(t, K["schedule"], 0.4)
    put(f, label_pill("2 · SET SCHEDULE", MINT, WHITE, "clock", 22, 58), CX + 200, 640 + dy, ps, pa * a)
    # cursor taps "Every day"
    cm = out_cubic(prog(t, K["schedule"] - 0.3, 0.6))
    press = prog(t, K["schedule"] + 0.35, 0.2)
    if cm > 0:
        lv = out_cubic(prog(t, K["schedule"] + 1.3, 0.5))
        tx, ty = CX - 40, 1180 + dy
        put(f, cursor(), lerp(tx + 260, tx, cm) + 140 * lv, lerp(ty + 300, ty, cm) + 140 * lv,
            1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - lv) * a)
        rp = prog(t, K["schedule"] + 0.37, 0.6)
        if 0 < rp < 1:
            put(f, ring(50, MINT, 5), tx - 10, ty - 10, 0.6 + 1.2 * rp, (1 - rp) * 0.7 * a)


# ------------------------------------------------------------------ S7: laptop off / sleeping — posts keep going
@lru_cache(None)
def laptop_off():
    w, h = 300, 230

    def cb(p):
        p.rr((40, 20, w - 40, 170), 18, fill=rgba(NIGHT))
        p.rr((52, 32, w - 52, 158), 10, fill=rgba((12, 14, 26)))
        p.rr((10, 172, w - 10, 196), 10, fill=rgba((150, 160, 180)))
        p.text(w / 2, 96, "OFF", "black", 40, rgba((90, 100, 130)), anchor="mm")
    return canvas(w, h, cb)


@lru_cache(None)
def moon():
    s = 150

    def cb(p):  # crescent: draw the disc, then punch a transparent disc out of it
        p.circ(s / 2, s / 2, s / 2 - 6, fill=rgba(YELLOW))
        p.circ(s / 2 + 34, s / 2 - 26, s / 2 - 14, fill=(0, 0, 0, 0))
    return canvas(s, s, cb)


@lru_cache(None)
def posted_row(tm):
    w, h = 460, 92

    def cb(p):
        p.rr((1, 1, w - 2, h - 2), 26, fill=rgba(WHITE), outline=rgba(BORDER), width=2)
        p.rr((18, 18, 74, 74), 16, fill=rgba(YT_RED))
        icon(p, "play", 46, 46, 30, WHITE, bg=YT_RED)
        p.text(92, 34, "Short posted", "bold", 28, rgba(INK), anchor="lm")
        p.text(93, 66, tm + " · on autopilot", "semi", 20, rgba(MUTED), anchor="lm")
        p.circ(w - 44, h / 2, 20, fill=rgba(GREEN))
        icon(p, "check", w - 44, h / 2, 22, WHITE, bg=GREEN)
    return card(w, h, 26, cb)


def s_sleep(f, t):
    _, a, dy = trans(t, K["s6_end"], K["s7_end"])
    ps, pa = pop(t, K["laptop"], 0.42)
    put(f, laptop_off(), CX - 230, 800 + dy, ps, pa * a)
    ps, pa = pop(t, K["sleep"], 0.42)
    put(f, moon(), CX + 220, 780 + dy + 8 * math.sin(t * 2), ps, pa * a)
    for k in range(3):
        zp = prog(t, K["sleep"] + 0.3 + k * 0.5, 1.4)
        if 0 < zp < 1:
            put(f, num_text("z", INK2, 40 + 12 * k), CX + 300 + 30 * k, 720 - 120 * zp + dy, 1.0, (1 - zp) * a)
    for k, tm in enumerate(["6:00 AM", "12:00 PM", "6:00 PM"]):
        ps, pa = pop(t, K["posted"] + k * 0.45, 0.4, s0=0.4)
        put(f, posted_row(tm), CX, 1070 + k * 130 + dy, ps, pa * a)
    ps, pa = pop(t, K["daily"], 0.38)
    put(f, label_pill("EVERY DAY · ON TIME", MINT, WHITE, "clock", 20, 56), CX, 1470 + dy, ps, pa * a)


# ------------------------------------------------------------------ S8: start free, no credit card
@lru_cache(None)
def card_strike():
    w, h = 300, 190

    def cb(p):
        p.rr((10, 20, w - 10, h - 20), 20, fill=rgba(tint(BLUE, 0.6)))
        p.rect((10, 52, w - 10, 80), fill=rgba(INK2))
        p.rr((30, 110, 120, 130), 6, fill=rgba(WHITE))
        p.line([(20, h - 20), (w - 20, 20)], rgba(RED), 14)
    return canvas(w, h, cb)


def s_free(f, t):
    s, a, dy = trans(t, K["s7_end"], K["s8_end"])
    put(f, pic_card("08_signup_free_card", 520, 26), CX - 180, 1080 + dy, s, a)
    ps, pa = pop(t, K["free"], 0.45, s0=0.3)
    put(f, num_text("₹0", GREEN, 150), CX + 290, 820 + dy, ps * _bump(t, K["free"] + 0.4, 0.08), pa * a)
    ps, pa = pop(t, K["free"] + 0.3, 0.36)
    put(f, chip("FREE TRIAL", GREEN, WHITE, 24, 62, "check"), CX + 290, 930 + dy, ps, pa * a)
    ps, pa = pop(t, K["card"], 0.42, s0=0.3)
    put(f, card_strike(), CX + 290, 1130 + dy, ps, pa * a)
    ps, pa = pop(t, K["card"] + 0.3, 0.36)
    put(f, chip("NO CREDIT CARD", RED, WHITE, 22, 58, "cross"), CX + 290, 1260 + dy, ps, pa * a)
    ps, pa = pop(t, K["trial"], 0.4)
    put(f, label_pill("FIRST SHORT FREE", tint(GREEN, 0.85), T_GREEN, "spark", 20, 54), CX + 290, 1380 + dy, ps, pa * a)



# ------------------------------------------------------------------ S9: link in bio + comment TOOL → DM
@lru_cache(None)
def link_card():
    w, h = 840, 190

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), 34, fill=rgba((255, 251, 236)), outline=rgba(YELLOW), width=4)
        p.rr((34, 45, 134, 145), 26, fill=rgba(tint(GREEN, 0.85)))
        p.rr((58, 70, 110, 120), 10, outline=rgba(GREEN), width=5)
        p.poly([(77, 83), (77, 107), (97, 95)], fill=rgba(GREEN))
        tw = text_w("AWESOME TOOLS · NEW", "mono", 18, 3) + 30
        p.rr((166, 30, 166 + tw, 64), 17, fill=rgba(YELLOW))
        p.text(181, 47, "AWESOME TOOLS · NEW", "mono", 18, rgba(DARK), anchor="lm", spacing=3)
        p.text(166, 102, "TurtleReels: YouTube Shorts on Autopilot", "bold", 31, rgba(INK), anchor="lm")
        p.text(167, 146, "Faceless satisfying Shorts drawn by Python", "semi", 25, rgba(MUTED), anchor="lm")
        p.text(w - 40, h / 2, "›", "bold", 56, rgba(MUTED), anchor="mm")
    return card(w, h, 34, cb)


@lru_cache(None)
def bio_card():
    w, h = 840, 250

    def cb(p):
        p.text(220, 76, "computer__hub", "black", 44, rgba(INK), anchor="lm")
        p.text(221, 124, "AI tools · websites & apps", "semi", 26, rgba(MUTED), anchor="lm")
        p.rr((220, 160, 660, 220), 30, fill=rgba(tint(BLUE, 0.9)), outline=rgba(tint(BLUE, 0.6)), width=2)
        icon(p, "link", 254, 190, 28, BLUE, bg=tint(BLUE, 0.9))
        p.text(282, 190, "All resource link", "bold", 28, rgba(BLUE), anchor="lm")
    return card(w, h, 36, cb)


@lru_cache(None)
def dm_bubble():
    w, h = 640, 140

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 40, fill=rgba(BLUE))
        icon(p, "chat", 66, h / 2, 60, WHITE, bg=BLUE)
        p.text(118, 50, "DM: TurtleReels link", "bold", 34, rgba(WHITE), anchor="lm")
        p.text(119, 96, "sent straight to your inbox!", "semi", 26, rgba(tint(BLUE, 0.8)), anchor="lm")
    return canvas(w, h, cb)


def s_cta(f, t):
    s, a, dy = trans(t, K["s8_end"], K["s9_end"])
    cy = 720 + dy
    put(f, bio_card(), CX, cy, s, a)
    ls, la = pop(t, K["s8_end"] + 0.15, 0.4)
    put(f, logo(140), CX - 300 * s, cy, ls * s, la * a)
    press = prog(t, K["bio"] + 0.3, 0.2)
    cm = out_cubic(prog(t, K["bio"] - 0.4, 0.6))
    if cm > 0:
        lv = out_cubic(prog(t, K["bio"] + 1.0, 0.5))
        put(f, cursor(), lerp(CX + 360, CX + 20, cm) + 160 * lv, lerp(cy + 300, cy + 82, cm) + 120 * lv,
            1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - lv) * a)
    rp = prog(t, K["bio"] + 0.35, 0.6)
    if 0 < rp < 1:
        put(f, ring(60, BLUE, 5), CX - 20, cy + 64, 0.6 + 1.2 * rp, (1 - rp) * 0.7 * a)
    s2, a2, d2 = trans(t, K["bio"] + 0.5, K["s9_end"])
    put(f, link_card(), CX, 980 + d2, s2, a2)
    s3, a3, d3 = trans(t, K["comment"] - 0.6, K["s9_end"])
    word = "TOOL"
    typed = word[:max(0, min(len(word), int((t - K["tool_word"]) / 0.1) + 1))] if t >= K["tool_word"] else ""
    put(f, comment_box(typed, t >= K["tool_word"] + 0.5), CX, 1210 + d3, s3, a3)
    ps, pa = pop(t, K["dm"], 0.45, s0=0.3)
    put(f, dm_bubble(), CX + 50, 1390 + d3, ps, pa * a3)


# ------------------------------------------------------------------ S10: outro — follow Computer Hub
def s_outro(f, t):
    t0 = K["s9_end"]
    s, a, dy = trans(t, t0, None, din=0.6, s0=0.5)
    bob = 5 * math.sin((t - t0) * 2.0) * prog(t, t0 + 1.0, 1.0)
    cy = 860 + dy + bob
    tr, k = t0 + 0.15, 0
    while tr < t and k < 8:
        pr = prog(t, tr, 1.4)
        if 0 < pr < 1:
            put(f, ring(165, MINT if k % 2 == 0 else CYAN, 5), CX, cy, s * (0.98 + 0.5 * out_cubic(pr)),
                (1 - pr) * 0.45 * a)
        tr += 1.5
        k += 1
    put(f, logo_shadow(330), CX, cy, s, a * 0.9)
    put(f, logo(330), CX, cy, s, a)
    ps, pa = pop(t, t0 + 0.2, 0.4)
    put(f, pill("AWESOME TOOLS · DAY 1", tint(MINT, 0.86), (16, 120, 84), size=20, h=52, icon_name="star",
                icon_col=(16, 120, 84)), CX, 640, ps, pa)
    ps, pa = pop(t, t0 + 0.35, 0.4)
    put(f, handle_pill(42), CX, 1100, ps, pa)
    for lab, ic, bg, tc, x, key in [("AI TOOLS", "spark", tint(PURPLE, 0.86), PURPLE, CX - 150, "ai_era"),
                                    ("STAY UPDATED", "bolt", tint(CYAN, 0.86), BLUE, CX + 165, "updated")]:
        ps, pa = pop(t, K[key], 0.34)
        put(f, pill(lab, bg, tc, size=20, h=56, icon_name=ic, icon_col=tc), x, 1205, ps, pa)
    tf = K["follow"]
    ps, pa = pop(t, tf - 1.0, 0.42, s0=0.4)
    press = prog(t, tf, 0.2)
    kk = 1 - 0.07 * math.sin(press * math.pi)
    put(f, follow_btn(press > 0.5), CX, 1320, ps * kk, pa)
    rp = prog(t, tf + 0.02, 0.6)
    if 0 < rp < 1:
        put(f, ring(100, BLUE, 5), CX, 1320, 0.9 + 1.0 * rp, (1 - rp) * 0.6)
    cm = out_cubic(prog(t, tf - 0.55, 0.5))
    if cm > 0:
        lv = out_cubic(prog(t, tf + 0.7, 0.5))
        put(f, cursor(), lerp(CX + 330, CX + 70, cm) + 120 * lv, lerp(1530, 1340, cm) + 160 * lv,
            1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - lv))
    ps, pa = pop(t, tf + 0.9, 0.4)
    put(f, label_pill("LINK IN BIO · COMMENT “TOOL”", tint(BLUE, 0.88), BLUE, "chat", 20, 56), CX, 1430, ps, pa)


SCENES = [
    (0.0, K["s1_end"] + 0.05, s_hook),
    (K["s1_end"], K["s2_end"] + 0.05, s_reveal),
    (K["s2_end"], K["s3_end"] + 0.05, s_code),
    (K["s3_end"], K["s4_end"] + 0.05, s_unique),
    (K["s4_end"], K["s5_end"] + 0.05, s_auto),
    (K["s5_end"], K["s6_end"] + 0.05, s_choose),
    (K["s6_end"], K["s7_end"] + 0.05, s_sleep),
    (K["s7_end"], K["s8_end"] + 0.05, s_free),
    (K["s8_end"], K["s9_end"] + 0.05, s_cta),
    (K["s9_end"], TOTAL_LEN + 0.1, s_outro),
]


def _events():
    e = [(0.05, "shimmer", -2, 0.5, {}), (K["face"], "alert", -6, 0.35, {}), (K["edit"], "alert", -6, 0.65, {}),
         (K["views"], "rise", -6, 0.5, {})]
    for key in ["s1_end", "s2_end", "s3_end", "s4_end", "s5_end", "s6_end", "s7_end", "s8_end", "s9_end"]:
        e.append((K[key] - 0.02, "whoosh", -1, 0.5, {}))
    e += [(K["s1_end"] + 0.25, "pop", -3, 0.5, {"pitch": 0.75}), (K["turtlereels"], "shimmer", -3, 0.5, {}),
          (K["ai"], "click", -8, 0.5, {}), (K["mandala"], "pop", -7, 0.35, {}),
          (K["spiral"], "pop", -7, 0.5, {"pitch": 1.15}), (K["geometric"], "pop", -7, 0.65, {"pitch": 1.3}),
          (K["visuals"], "pop", -8, 0.35, {}), (K["colors"], "pop", -8, 0.65, {"pitch": 1.1}),
          (K["quotes"], "pop", -8, 0.35, {"pitch": 1.2}), (K["music"], "chime", -6, 0.6, {}),
          (K["title"], "pop", -8, 0.4, {}), (K["desc"], "pop", -8, 0.5, {"pitch": 1.1}),
          (K["hashtags"], "pop", -8, 0.6, {"pitch": 1.2}), (K["youtube"], "click", -5, 0.6, {}),
          (K["autopilot"], "rise", -5, 0.5, {}), (K["style"], "pop", -7, 0.4, {}),
          (K["schedule"] + 0.35, "click", -4, 0.5, {}), (K["laptop"], "swipe", -7, 0.4, {}),
          (K["sleep"], "shimmer", -6, 0.6, {}), (K["posted"], "pop", -7, 0.5, {}),
          (K["posted"] + 0.45, "pop", -7, 0.5, {"pitch": 1.15}), (K["posted"] + 0.9, "pop", -7, 0.5, {"pitch": 1.3}),
          (K["free"], "chime", -5, 0.5, {}), (K["card"], "alert", -6, 0.5, {}),
          (K["bio"] + 0.3, "click", -4, 0.5, {}), (K["tool_word"], "click", -6, 0.5, {}),
          (K["dm"], "chime", -5, 0.6, {}), (K["s9_end"] + 0.1, "shimmer", 0, 0.5, {}),
          (K["follow"], "click", -1, 0.55, {})]
    return sorted(e, key=lambda x: x[0])


EVENTS = _events()
