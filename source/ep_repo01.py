"""AWESOME REPOS · DAY 1 — "UPI Gateway" by Mayank Singh (github.com/mynkdev-21/upi-gateway).

New series (open-source repo promos, credit the developer). Same look as Plan B Day 1-4: light theme,
isometric plate, white cards, white pop-up captions with blue keywords, logo outro + Follow click.
Voice: episodes/repo01/voice.mp3 (ElevenLabs Viraj, 88.03 s). Word timings: episodes/repo01/words.json.
Real UI from the repo: output/AwesomeRepos/Day01_UPI-Gateway/ui/elements/*.png.
"""
import math
import os
from functools import lru_cache

from PIL import Image, ImageDraw

from gfx import (BLUE, BORDER, CYAN, DARK, DARK_YEL, GREEN, INK, INK2, LINE, MUTED, ORANGE, PANEL, PURPLE, SKEL,
                 SM, T_GREEN, WHITE, YELLOW, canvas, card, clamp, icon, lerp, out_back, out_cubic, pop, prog, put,
                 rgba, smooth, text_w, tile, tint, trans)
from scenes import CX, big_num, cursor, follow_btn, handle_pill, header_label, logo, logo_shadow, pill, ring
from ep_day01 import _at, arrow_right, coin, day_card, track_dot
from ep_day02 import avatar, big_cross, node, stage, stamp, title_two
from ep_day03 import comment_box, label_pill, num_text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = os.path.join(ROOT, "episodes", "repo01", "voice.mp3")
UI = os.path.join(ROOT, "output", "AwesomeRepos", "Day01_UPI-Gateway", "ui", "elements")
HEADER = "COMPUTER HUB · AWESOME REPOS · DAY 1"
RED = (226, 64, 64)
INDIGO = (79, 70, 229)          # the repo's brand colour (tailwind brand-600)
GH_DARK = (13, 17, 23)          # GitHub dark page

from ep_repo01_timing import CAP_END, K, PHRASES, TOTAL_LEN, VOICE_LEN  # noqa: E402  (word timings)


# ------------------------------------------------------------------ shared sprites
@lru_cache(None)
def shot(name, w, r=22):
    """A repo screenshot, resized to width w, rounded corners."""
    im = Image.open(os.path.join(UI, name + ".png")).convert("RGBA")
    h = int(round(w * im.height / im.width))
    im = im.resize((w, h), Image.LANCZOS)
    mask = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, fill=255)
    im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", im.size, 0),
                                mask.resize((w, h), Image.LANCZOS)))
    return im


@lru_cache(None)
def shot_card(name, w, r=26, pad=0):
    """Screenshot floating as a card (soft shadow, thin border)."""
    im = shot(name, w - 2 * pad, max(4, r - pad))
    h = im.height + 2 * pad
    out = card(w, h, r)
    out.alpha_composite(im, (SM + pad, SM + pad))
    return out


@lru_cache(None)
def browser_shot(name, url, w=860):
    im = shot(name, w - 40, 14)
    bar = 74
    h = bar + 20 + im.height + 20

    def cb(p):
        p.rr((0, 0, w - 1, bar), 36, fill=rgba(PANEL))
        p.rect((0, 40, w - 1, bar), fill=rgba(PANEL))
        p.line([(0, bar), (w, bar)], rgba(LINE), 2, caps=False)
        for k, c in enumerate([(255, 96, 92), (255, 190, 50), (40, 200, 70)]):
            p.circ(40 + k * 28, 37, 9, fill=rgba(c))
        p.rr((140, 17, w - 80, 57), 20, fill=rgba(WHITE), outline=rgba(LINE), width=2)
        icon(p, "shield", 166, 37, 22, GREEN)
        p.text(188, 37, url, "monor", 20, rgba(INK2), anchor="lm")
    out = card(w, h, 36, cb)
    out.alpha_composite(im, (SM + 20, SM + bar + 20))
    return out


@lru_cache(None)
def repo_logo(size):
    return Image.open(os.path.join(UI, "upi_gateway_logo.png")).convert("RGBA").resize((size, size), Image.LANCZOS)


@lru_cache(None)
def chip(txt, col, fg=WHITE, size=26, h=66, ic=None):
    return pill(txt, col, fg, kind="bold", size=size, spacing=0, h=h, icon_name=ic, icon_col=fg)


@lru_cache(None)
def app_chip(name, col):
    return pill(name, WHITE, col, kind="bold", size=30, spacing=0, h=72, border=tint(col, 0.6))


@lru_cache(None)
def gh_star(size=60, col=DARK_YEL):
    return canvas(size, size, lambda p: icon(p, "star", size / 2, size / 2, size * 0.9, col))


def _bump(t, t0, k=0.06, d=0.35):
    return 1 + k * math.sin(math.pi * prog(t, t0, d))


# ------------------------------------------------------------------ S1: the fee hook (0 - K.s1_end)
@lru_cache(None)
def fee_card():
    w, h = 820, 600

    def cb(p):
        header_label(p, w, 56, "PAYMENT GATEWAY FEE", BLUE, 22, 6)
        p.line([(50, 400), (w - 50, 400)], rgba(LINE), 2, caps=False)
        p.text(70, 460, "on every payment", "semi", 32, rgba(MUTED), anchor="lm")
    return card(w, h, 38, cb)


@lru_cache(None)
def pay_row():
    w, h = 300, 130

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 30, fill=rgba(tint(GREEN, 0.9)), outline=rgba(tint(GREEN, 0.5)), width=3)
        p.text(30, 46, "PAYMENT", "mono", 18, rgba(T_GREEN), anchor="lm", spacing=3)
        p.text(30, 92, "₹1,000", "black", 50, rgba(INK), anchor="lm")
    return canvas(w, h, cb)


def s_fee(f, t):
    s, a, dy = trans(t, 0.05, K["s1_end"], din=0.5, s0=0.6)
    cx, cy = CX, 1010 + dy
    at = _at(cx, cy, 820, 600, s)
    put(f, fee_card(), cx, cy, s, a)
    ps, pa = pop(t, K["razorpay"], 0.4)
    x, y = at(410, 140)
    put(f, chip("Razorpay & others", INK, WHITE, 30, 74, "chip"), x, y, ps * s, pa * a)
    ps, pa = pop(t, K["two"], 0.45, s0=0.3)
    x, y = at(300, 290)
    put(f, num_text("2%", RED, 150), x, y, ps * s * _bump(t, K["two"] + 0.3), pa * a)
    ps, pa = pop(t, K["gst"], 0.4, s0=0.3)
    x, y = at(560, 290)
    put(f, chip("+ GST", ORANGE, WHITE, 40, 92), x, y, ps * s, pa * a)
    ps, pa = pop(t, K["payment"], 0.36)
    x, y = at(620, 470)
    put(f, pay_row(), x, y, ps * s * 0.85, pa * a)
    # coins leak out of the payment, again and again
    for k in range(6):
        t0 = K["two"] + 0.2 + k * 0.32
        cp = prog(t, t0, 0.8)
        if 0 < cp < 1:
            x0, y0 = at(620, 450)
            put(f, coin(18), x0 + 140 * cp * s, y0 - 220 * out_cubic(cp) * s + 260 * cp * cp * s, s, a * (1 - cp))


# ------------------------------------------------------------------ S2: 10 lakh sales -> ₹23,600 gone every month
@lru_cache(None)
def loss_card():
    w, h = 820, 660

    def cb(p):
        header_label(p, w, 56, "EVERY MONTH", BLUE, 22, 6)
        p.text(w / 2, 120, "SALES", "mono", 22, rgba(MUTED), anchor="mm", spacing=5)
        p.line([(50, 300), (w - 50, 300)], rgba(LINE), 2, caps=False)
        p.text(w / 2, 352, "GONE IN FEES", "mono", 22, rgba(RED), anchor="mm", spacing=5)
    return card(w, h, 38, cb)


@lru_cache(None)
def inr(v, col, size):
    s = f"{v:,}"
    if v >= 100000:  # Indian grouping
        x = str(v)
        s = x[:-3]
        s = ",".join([s[max(0, i - 2):i] for i in range(len(s), 0, -2)][::-1]) + "," + x[-3:]
    return num_text("₹" + s, col, size)


def s_loss(f, t):
    s, a, dy = trans(t, K["s1_end"], K["s2_end"])
    cx, cy = CX, 1040 + dy
    at = _at(cx, cy, 820, 660, s)
    put(f, loss_card(), cx, cy, s, a)
    v = int(round(1000000 * smooth(prog(t, K["lakh"], 0.7)) / 1000) * 1000)
    if t >= K["lakh"] - 0.05:
        ps, _ = pop(t, K["lakh"], 0.4, s0=0.6)
        x, y = at(410, 205)
        put(f, inr(v, INK, 100), x, y, ps * s, a)
    fee = int(round(23600 * smooth(prog(t, K["hazaar"], 1.0)) / 100) * 100)
    if t >= K["hazaar"] - 0.05:
        ps, _ = pop(t, K["hazaar"], 0.4, s0=0.6)
        x, y = at(410, 450)
        put(f, inr(fee, RED, 120), x, y, ps * s * _bump(t, K["hazaar"] + 1.0), a)
    ps, pa = pop(t, K["fees"], 0.4, s0=2.0)
    x, y = at(410, 580)
    put(f, stamp("₹2.8 LAKH / YEAR", RED), x, y, ps * s * 0.62, pa * a)
    for k in range(4):
        cp = prog(t, K["hazaar"] + 0.15 + k * 0.25, 0.9)
        if 0 < cp < 1:
            x0, y0 = at(640 + k * 30, 430)
            put(f, coin(20), x0 + 120 * cp * s, y0 - 260 * out_cubic(cp) * s, s, a * (1 - cp))


# ------------------------------------------------------------------ S3: an Indian developer made it free + open source
@lru_cache(None)
def dev_card():
    w, h = 820, 560

    def cb(p):
        p.circ(130, 150, 78, fill=rgba(tint(INDIGO, 0.85)))
        icon(p, "user", 130, 160, 96, INDIGO, bg=tint(INDIGO, 0.85))
        p.text(240, 120, "Indian Developer", "black", 48, rgba(INK), anchor="lm")
        p.text(242, 180, "made it public on GitHub", "semi", 30, rgba(MUTED), anchor="lm")
        p.line([(50, 280), (w - 50, 280)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


def s_dev(f, t):
    s, a, dy = trans(t, K["s2_end"], K["s3_end"])
    cx, cy = CX, 1000 + dy
    at = _at(cx, cy, 820, 560, s)
    put(f, dev_card(), cx, cy, s, a)
    for txt, col, ic, rx, key in [("100% FREE", GREEN, "check", 220, "free"),
                                  ("OPEN SOURCE", INDIGO, "code", 580, "opensource")]:
        ps, pa = pop(t, K[key], 0.4, s0=0.3)
        x, y = at(rx, 380)
        put(f, chip(txt, col, WHITE, 32, 84, ic), x, y, ps * s * _bump(t, K[key] + 0.35), pa * a)
    ps, pa = pop(t, K["solution"], 0.36)
    x, y = at(410, 490)
    put(f, label_pill("NO % CUT", tint(GREEN, 0.85), T_GREEN, "rupee", 20, 50), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S4: Awesome Repos · Day 1 — UPI Gateway by Mayank Singh
@lru_cache(None)
def repo_day_card():
    w, h = 560, 600

    def cb(p):
        p.rr((0, 0, w - 1, 150), 38, fill=rgba(INDIGO))
        p.rect((0, 100, w - 1, 150), fill=rgba(INDIGO))
        for x in (150, w - 150):
            p.circ(x, 0, 18, fill=rgba(WHITE))
            p.circ(x, 0, 9, fill=rgba((55, 48, 163)))
        p.text(w / 2, 82, "DAY", "mono", 46, rgba(WHITE), anchor="mm", spacing=14)
        p.line([(50, 470), (w - 50, 470)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


@lru_cache(None)
def repo_title_card():
    w, h = 820, 250

    def cb(p):
        p.text(230, 96, "UPI Gateway", "black", 64, rgba(INK), anchor="lm")
        p.text(232, 168, "by Mayank Singh", "bold", 36, rgba(INDIGO), anchor="lm")
        p.text(232, 210, "github.com/mynkdev-21", "monor", 22, rgba(MUTED), anchor="lm")
    return card(w, h, 38, cb)


def s_series(f, t):
    t_in, t_out = K["s3_end"], K["s4_end"]
    # day card first ("Awesome Repos, Day One")
    s, a, dy = trans(t, t_in, K["upi_gw"] + 0.4, din=0.5, s0=0.6)
    cx, cy = CX, 1000 + dy
    at = _at(cx, cy, 560, 600, s)
    put(f, repo_day_card(), cx, cy, s, a)
    ps, pa = pop(t, K["day1"], 0.45, s0=0.2)
    x, y = at(280, 300)
    put(f, big_num("1", INK, 240), x, y, ps * s, pa * a)
    ps, pa = pop(t, K["awesome"], 0.4)
    x, y = at(280, 530)
    put(f, title_two("Awesome ", "Repos", 46, INDIGO, "bold"), x, y, ps * s, pa * a)
    rp = prog(t, K["day1"] + 0.2, 0.9)
    if 0 < rp < 1:
        x, y = at(280, 300)
        put(f, ring(150, INDIGO, 5), x, y, s * (0.9 + 0.5 * rp), a * (1 - rp) * 0.6)
    # then the repo itself
    s2, a2, dy2 = trans(t, K["upi_gw"] + 0.3, t_out, din=0.5)
    cy2 = 860 + dy2
    put(f, repo_title_card(), CX, cy2, s2, a2)
    ls, la = pop(t, K["upi_gw"] + 0.4, 0.45, s0=0.3)
    put(f, repo_logo(150), CX + (130 - 410) * s2, cy2, ls * s2, la * a2)
    s3, a3, dy3 = trans(t, K["mayank"] - 0.1, t_out, din=0.5)
    put(f, shot_card("github_repo_header", 980, 26), CX, 1190 + dy3, s3, a3)
    ps, pa = pop(t, K["mayank"] + 0.3, 0.38)
    put(f, label_pill("CREDIT: @mynkdev-21", YELLOW, DARK, "star", 20, 54), CX, 1375 + dy3, ps, pa * a3)


# ------------------------------------------------------------------ S5: self-hosted on your own server
@lru_cache(None)
def server_node():
    return node("Your Server", "db", INDIGO, w=250)


def s_selfhost(f, t):
    stage(f, t, "SELF-HOSTED UPI GATEWAY", K["s4_end"] + 0.05, K["s5_end"], INDIGO, WHITE, "bolt")
    s, a, dy = trans(t, K["s4_end"] + 0.3, K["s5_end"])
    put(f, browser_shot("hero_headline", "your-domain.com", 760), CX - 40, 1060 + dy, s, a)
    ps, pa = pop(t, K["server"], 0.4, s0=0.3)
    put(f, server_node(), CX + 270, 1330 + dy, ps * _bump(t, K["server"] + 0.3), pa * a)
    ps, pa = pop(t, K["host"], 0.36)
    put(f, label_pill("HOST IT YOURSELF", tint(INDIGO, 0.86), INDIGO, "cloud", 20, 52), CX - 200, 1330 + dy, ps,
        pa * a)


# ------------------------------------------------------------------ S6: every order gets a dynamic QR — any UPI app
def s_qr(f, t):
    s, a, dy = trans(t, K["s5_end"], K["s6_end"])
    put(f, shot_card("payment_page", 640, 30), CX, 1040 + dy, s, a)
    ps, pa = pop(t, K["customer"], 0.36)
    put(f, label_pill("CUSTOMER ORDERS", WHITE, INK, "user", 20, 54), CX - 150, 690 + dy, ps, pa * a)
    ps, pa = pop(t, K["qr"], 0.42, s0=0.3)
    put(f, chip("UNIQUE DYNAMIC QR", INDIGO, WHITE, 28, 76, "bolt"), CX + 120, 690 + dy,
        ps * _bump(t, K["qr"] + 0.35), pa * a)
    rp = prog(t, K["qr"] + 0.1, 0.8)
    if 0 < rp < 1:
        put(f, ring(150, INDIGO, 6), CX + 70, 930 + dy, 0.8 + 0.6 * rp, (1 - rp) * 0.7 * a)
    for k, (nm, col, key) in enumerate([("GPay", BLUE, "gpay"), ("PhonePe", PURPLE, "phonepe"),
                                         ("Paytm", CYAN, "paytm")]):
        ps, pa = pop(t, K[key], 0.36, s0=0.3)
        put(f, app_chip(nm, col), CX - 260 + k * 260, 1400 + dy, ps, pa * a)


# ------------------------------------------------------------------ S7: money goes straight to your bank — 0% commission
@lru_cache(None)
def flow_tile(name, ic, col, w=240, h=230):
    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 30, fill=rgba(WHITE), outline=rgba(BORDER), width=3)
        p.rr((w / 2 - 54, 30, w / 2 + 54, 138), 30, fill=rgba(tint(col, 0.85)))
        icon(p, ic, w / 2, 84, 70, col, bg=tint(col, 0.85))
        p.text(w / 2, 186, name, "bold", 30, rgba(INK), anchor="mm")
    return canvas(w, h, cb)


@lru_cache(None)
def middle_tile():
    w, h = 200, 160

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 28, fill=rgba(PANEL), outline=rgba(BORDER), width=3)
        icon(p, "chip", w / 2, 62, 60, MUTED, bg=PANEL)
        p.text(w / 2, 126, "Middleman", "bold", 26, rgba(MUTED), anchor="mm")
    return canvas(w, h, cb)


def s_direct(f, t):
    stage(f, t, "DIRECT TO YOUR BANK", K["s6_end"] + 0.05, K["s7_end"], GREEN, WHITE, "check")
    _, a, dy = trans(t, K["s6_end"] + 0.05, K["s7_end"])
    y = 960 + dy
    ps, pa = pop(t, K["paisa"], 0.38)
    put(f, flow_tile("Customer", "user", CYAN), CX - 300, y, ps, pa * a)
    ps, pa = pop(t, K["bichauliye"] - 0.2, 0.36)
    mid_a = a * (1 - 0.5 * smooth(prog(t, K["bichauliye"] + 0.5, 0.3)))
    put(f, middle_tile(), CX, y + 175, ps * 0.9, pa * mid_a)
    cs, ca = pop(t, K["bichauliye"] + 0.4, 0.36, s0=0.2)
    put(f, big_cross(), CX, y + 175, cs * 0.34, ca * a)
    ps, pa = pop(t, K["bank"], 0.38)
    put(f, flow_tile("Your Bank", "rupee", GREEN), CX + 300, y, ps, pa * a)
    ap = out_cubic(prog(t, K["seedhe"], 0.5))
    if ap > 0:
        put(f, arrow_right(GREEN, 200), CX, y, 1.0, a, sx=max(ap, 0.02))
    for k in range(5):  # money flies straight across
        cp = prog(t, K["seedhe"] + 0.3 + k * 0.35, 0.8)
        if 0 < cp < 1:
            e = smooth(cp)
            put(f, coin(20), lerp(CX - 200, CX + 200, e), y - 30 - 50 * math.sin(math.pi * e), 1.0, a * clamp(4 * (1 - cp)))
    ps, pa = pop(t, K["zero"], 0.45, s0=0.3)
    put(f, num_text("0%", GREEN, 190), CX - 150, 1370 + dy, ps * _bump(t, K["zero"] + 0.4, 0.08), pa * a)
    ps, pa = pop(t, K["commission"], 0.38)
    put(f, chip("COMMISSION", GREEN, WHITE, 32, 84, "check"), CX + 190, 1370 + dy, ps, pa * a)
    ps, pa = pop(t, K["commission"] + 0.4, 0.38)
    put(f, shot_card("money_stays_yours", 620, 24), CX, 1600 + dy, ps, pa * a)


# ------------------------------------------------------------------ S8: auto verify -> webhook "order paid"
@lru_cache(None)
def webhook_pill(ok=False):
    w, h = 560, 96

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(INK))
        icon(p, "link", 52, h / 2, 40, CYAN, bg=INK)
        p.text(92, h / 2, "order.paid", "mono", 34, rgba(WHITE), anchor="lm")
        p.text(w - 40, h / 2, "200 OK" if ok else "→ sending", "mono", 30, rgba(GREEN if ok else MUTED), anchor="rm")
    return canvas(w, h, cb)


@lru_cache(None)
def site_node():
    return node("Your Website", "globe", BLUE, w=250)


def s_verify(f, t):
    _, a, dy = trans(t, K["s7_end"], K["s8_end"])
    t_ok = K["successful"]
    sw = smooth(prog(t, K["webhook"] - 0.4, 0.4))   # verifying -> success swap
    s1, a1, d1 = trans(t, K["s7_end"] + 0.1, K["successful"] - 0.3)
    put(f, shot_card("verifying_card", 860, 28), CX, 930 + d1 + dy, s1, a1 * a)
    s2, a2, d2 = trans(t, K["successful"] - 0.45, K["s8_end"])
    put(f, shot_card("success_card", 860, 28), CX, 930 + d2, s2, a2)
    ps, pa = pop(t, K["verify"], 0.38)
    put(f, label_pill("AUTO VERIFY", INDIGO, WHITE, "shield", 22, 58), CX - 240, 620 + dy, ps, pa * a * (1 - 0.0 * sw))
    ps, pa = pop(t, K["webhook"], 0.4, s0=0.3)
    put(f, webhook_pill(t >= t_ok), CX - 120, 1400 + dy, ps, pa * a)
    ps, pa = pop(t, K["website"], 0.38)
    put(f, site_node(), CX + 300, 1400 + dy, ps * 0.85, pa * a)
    cs, ca = pop(t, t_ok, 0.4, s0=0.2)
    put(f, check_badge(), CX + 390, 1320 + dy, cs, ca * a)
    rp = prog(t, t_ok, 0.7)
    if 0 < rp < 1:
        put(f, ring(70, GREEN, 5), CX + 300, 1400 + dy, 0.8 + 0.8 * rp, (1 - rp) * 0.7 * a)


@lru_cache(None)
def check_badge(size=64):
    return canvas(size, size, lambda p: (p.circ(size / 2, size / 2, size / 2 - 2, fill=rgba(GREEN)),
                                         icon(p, "check", size / 2, size / 2, size * 0.6, WHITE, bg=GREEN)))


# ------------------------------------------------------------------ S9: dashboard, API docs, UPI account rotation
@lru_cache(None)
def upi_row(k, active):
    name = ["shop@paytm", "store@ybl", "biz@okaxis"][k]
    w, h = 300, 92

    def cb(p):
        col = INDIGO if active else BORDER
        p.rr((2, 2, w - 2, h - 2), 26, fill=rgba(tint(INDIGO, 0.9) if active else WHITE), outline=rgba(col),
             width=4 if active else 3)
        p.circ(44, h / 2, 14, fill=rgba(GREEN if active else SKEL))
        p.text(72, h / 2, name, "mono", 24, rgba(INK if active else MUTED), anchor="lm")
    return canvas(w, h, cb)


def s_features(f, t):
    _, a, dy = trans(t, K["s8_end"], K["s9_end"])
    s1, a1, d1 = trans(t, K["s8_end"] + 0.05, K["s9_end"])
    put(f, browser_shot("dashboard_full", "pay.your-domain.com/dashboard", 860), CX, 900 + d1, s1, a1)
    ps, pa = pop(t, K["dashboard"], 0.36)
    put(f, label_pill("FULL DASHBOARD", WHITE, INK, "chart", 22, 58), CX - 210, 580 + dy, ps, pa * a)
    ps, pa = pop(t, K["api"], 0.4)
    put(f, shot_card("api_docs_hero", 700, 24), CX - 70, 1290 + dy, ps, pa * a)
    ps, pa = pop(t, K["api"] + 0.2, 0.36)
    put(f, label_pill("API DOCS", INDIGO, WHITE, "code", 22, 58), CX + 230, 580 + dy, ps, pa * a)
    # rotation: three UPI IDs, the active one moves round
    for k in range(3):
        ps, pa = pop(t, K["rotation"] - 0.6 + k * 0.12, 0.36)
        act = t >= K["rotation"] and int((t - K["rotation"]) / 0.45) % 3 == k
        put(f, upi_row(k, act), CX - 330 + k * 330, 1520 + dy, ps * 0.98, pa * a)
    ps, pa = pop(t, K["rotation"], 0.38)
    put(f, label_pill("UPI ROTATION", GREEN, WHITE, "share", 20, 52), CX, 1630 + dy, ps, pa * a)


# ------------------------------------------------------------------ S10: built with Laravel — setup in a few commands
CMDS = ["git clone mynkdev-21/upi-gateway", "composer run setup", "php artisan app:create-admin", "composer run dev"]


@lru_cache(None)
def term_card():
    w, h = 860, 520

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), 34, fill=rgba(INK))
        for k, c in enumerate([(255, 96, 92), (255, 190, 50), (40, 200, 70)]):
            p.circ(44 + k * 28, 40, 9, fill=rgba(c))
        p.text(w / 2, 40, "terminal", "monor", 20, rgba(MUTED), anchor="mm")
    return card(w, h, 34, cb, fill=INK, border=INK)


@lru_cache(None)
def term_line(txt, done):
    w, h = 780, 70

    def cb(p):
        p.text(0, h / 2, "$", "mono", 30, rgba(GREEN), anchor="lm")
        p.text(34, h / 2, txt, "monor", 28, rgba(WHITE), anchor="lm")
        if done:
            icon(p, "check", w - 24, h / 2, 34, GREEN, bg=INK)
    return canvas(w, h, cb)


def s_setup(f, t):
    stage(f, t, "SETUP IN A FEW COMMANDS", K["s9_end"] + 0.05, K["s10_end"], INK, WHITE, "code")
    s, a, dy = trans(t, K["s9_end"] + 0.2, K["s10_end"])
    cx, cy = CX, 1050 + dy
    at = _at(cx, cy, 860, 520, s)
    put(f, term_card(), cx, cy, s, a)
    t0 = K["setup"] - 0.9
    for k, cmd in enumerate(CMDS):
        ts = t0 + k * 0.6
        if t < ts:
            break
        n = int(clamp((t - ts) / 0.4) * len(cmd))
        x, y = at(430, 130 + k * 90)
        put(f, term_line(cmd[:max(1, n)], t > ts + 0.5), x, y, s, a)
    ps, pa = pop(t, K["laravel"], 0.42, s0=0.3)
    put(f, chip("Laravel 12", (240, 83, 64), WHITE, 32, 84, "code"), CX - 200, 1390 + dy, ps, pa * a)
    ps, pa = pop(t, K["laravel"] + 0.3, 0.38)
    put(f, chip("PHP + MySQL", INDIGO, WHITE, 28, 76, "db"), CX + 210, 1390 + dy, ps, pa * a)


# ------------------------------------------------------------------ S11: honest note — UPI only, legit business
@lru_cache(None)
def note_card():
    w, h = 820, 560

    def cb(p):
        tile(p, 110, 110, 120, ORANGE, "shield")
        p.text(200, 88, "Keep in mind", "black", 52, rgba(INK), anchor="lm")
        p.text(202, 140, "use it the right way", "semi", 30, rgba(MUTED), anchor="lm")
        p.line([(50, 220), (w - 50, 220)], rgba(LINE), 2, caps=False)
    return card(w, h, 38, cb)


@lru_cache(None)
def note_row(k):
    txt, sub, ic, col = [("UPI payments only", "no cards / netbanking here", "rupee", INDIGO),
                         ("Your own legit business", "not a gateway for others", "briefcase", GREEN)][k]
    w, h = 720, 130

    def cb(p):
        tile(p, 60, h / 2, 90, col, ic)
        p.text(130, h / 2 - 20, txt, "bold", 36, rgba(INK), anchor="lm")
        p.text(131, h / 2 + 26, sub, "semi", 26, rgba(MUTED), anchor="lm")
    return canvas(w, h, cb)


def s_note(f, t):
    s, a, dy = trans(t, K["s10_end"], K["s11_end"])
    cx, cy = CX, 1010 + dy
    at = _at(cx, cy, 820, 560, s)
    put(f, note_card(), cx, cy, s, a)
    for k, key in enumerate(["upi_only", "legit"]):
        ps, pa = pop(t, K[key], 0.4)
        x, y = at(410, 310 + k * 150)
        put(f, note_row(k), x, y, ps * s, pa * a)


# ------------------------------------------------------------------ S12: link in bio · comment -> DM
@lru_cache(None)
def bio_card():
    w, h = 820, 300

    def cb(p):
        p.text(230, 80, "computer__hub", "black", 44, rgba(INK), anchor="lm")
        p.text(231, 130, "Software Engineer building a Plan B", "semi", 26, rgba(MUTED), anchor="lm")
        p.rr((230, 172, 700, 236), 32, fill=rgba(tint(BLUE, 0.9)), outline=rgba(tint(BLUE, 0.6)), width=2)
        icon(p, "link", 266, 204, 30, BLUE, bg=tint(BLUE, 0.9))
        p.text(296, 204, "All resource link", "bold", 30, rgba(BLUE), anchor="lm")
    return card(w, h, 38, cb)


@lru_cache(None)
def link_page_card():
    w, h = 820, 190

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), 34, fill=rgba((255, 251, 236)), outline=rgba(YELLOW), width=4)
        p.rr((34, 45, 134, 145), 26, fill=rgba(tint(INDIGO, 0.88)))
        p.poly([(84 + (x - 12) * 3.2, 95 + (y - 12) * 3.2) for x, y in
                [(13.5, 2), (4, 14), (10.5, 14), (9.5, 22), (19, 10), (12.5, 10)]], fill=rgba(INDIGO))
        tw = text_w("AWESOME REPOS · DAY 1", "mono", 18, 3) + 30
        p.rr((166, 30, 166 + tw, 64), 17, fill=rgba(YELLOW))
        p.text(181, 47, "AWESOME REPOS · DAY 1", "mono", 18, rgba(DARK), anchor="lm", spacing=3)
        p.text(166, 102, "UPI Gateway: Free Razorpay Alternative", "bold", 32, rgba(INK), anchor="lm")
        p.text(167, 146, "Self-hosted UPI payments · open source", "semi", 25, rgba(MUTED), anchor="lm")
        p.text(w - 40, h / 2, "›", "bold", 56, rgba(MUTED), anchor="mm")
    return card(w, h, 34, cb, shadow=1.0)


@lru_cache(None)
def dm_bubble():
    w, h = 660, 150

    def cb(p):
        p.rr((2, 2, w - 2, h - 2), 40, fill=rgba(BLUE))
        icon(p, "chat", 70, h / 2, 64, WHITE, bg=BLUE)
        p.text(126, 52, "DM: UPI Gateway repo", "bold", 36, rgba(WHITE), anchor="lm")
        p.text(127, 102, "github link · sent!", "semi", 28, rgba(tint(BLUE, 0.8)), anchor="lm")
    return canvas(w, h, cb)


def s_link(f, t):
    s, a, dy = trans(t, K["s11_end"], K["s12_end"])
    cy = 760 + dy
    put(f, bio_card(), CX, cy, s, a)
    ls, la = pop(t, K["s11_end"] + 0.15, 0.4)
    put(f, logo(150), CX - 280 * s, cy - 2, ls * s, la * a)
    # tap on "All resource link" -> the link page card
    press = prog(t, K["bio"] + 0.3, 0.2)
    rp = prog(t, K["bio"] + 0.35, 0.6)
    if 0 < rp < 1:
        put(f, ring(60, BLUE, 5), CX + 25, cy + 54, 0.6 + 1.2 * rp, (1 - rp) * 0.7 * a)
    cm = out_cubic(prog(t, K["bio"] - 0.4, 0.6))
    if cm > 0:
        lv = out_cubic(prog(t, K["bio"] + 1.0, 0.5))
        put(f, cursor(), lerp(CX + 360, CX + 60, cm) + 160 * lv, lerp(cy + 300, cy + 74, cm) + 120 * lv,
            1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - lv) * a)
    s2, a2, d2 = trans(t, K["bio"] + 0.5, K["s12_end"])
    put(f, link_page_card(), CX, 1035 + d2, s2, a2)
    # comment -> DM
    s3, a3, d3 = trans(t, K["comment"] - 0.6, K["s12_end"])
    word = "REPO"
    typed = word[:max(0, min(len(word), int((t - K["comment"]) / 0.1) + 1))] if t >= K["comment"] else ""
    put(f, comment_box(typed, t >= K["comment"] + 0.6), CX, 1260 + d3, s3, a3)
    ps, pa = pop(t, K["dm"], 0.45, s0=0.3)
    put(f, dm_bubble(), CX + 50, 1450 + d3, ps, pa * a3)


# ------------------------------------------------------------------ S13: give Mayank a star on GitHub
def gh_star_btn_pos(cx, cy, s, w=860):
    """Star button inside the github_repo_header crop (1240x190 source)."""
    k = w / 1240
    return cx + (1160 * k - w / 2) * s, cy + (24 * k - (190 * k) / 2) * s


@lru_cache(None)
def starred_pill():
    return pill("STARRED", YELLOW, DARK, size=24, h=62, icon_name="star", icon_col=DARK)


def s_star(f, t):
    stage(f, t, "SUPPORT THE DEVELOPER", K["s12_end"] + 0.05, K["s13_end"], YELLOW, DARK, "star")
    s, a, dy = trans(t, K["s12_end"] + 0.2, K["s13_end"])
    cx, cy = CX, 960 + dy
    put(f, shot_card("github_repo_header", 980, 26), cx, cy, s, a)
    bx, by = gh_star_btn_pos(cx, cy, s, 980)
    ts = K["star"]
    cm = out_cubic(prog(t, ts - 0.6, 0.6))
    press = prog(t, ts, 0.2)
    if cm > 0:
        lv = out_cubic(prog(t, ts + 0.9, 0.5))
        put(f, cursor(), lerp(bx + 120, bx + 14, cm) + 140 * lv, lerp(by + 320, by + 20, cm) + 140 * lv,
            1.15 - 0.1 * math.sin(press * math.pi), clamp(cm * 3) * (1 - lv) * a)
    rp = prog(t, ts + 0.02, 0.6)
    if 0 < rp < 1:
        put(f, ring(50, DARK_YEL, 5), bx, by, 0.6 + 1.4 * rp, (1 - rp) * 0.8 * a)
    for k in range(7):  # star burst
        bp = prog(t, ts + 0.05, 0.9)
        if 0 < bp < 1:
            ang = -math.pi / 2 + (k - 3) * 0.42
            r = 40 + 190 * out_cubic(bp)
            put(f, gh_star(46), bx + r * math.cos(ang), by + r * math.sin(ang), 0.7 + 0.3 * (1 - bp), (1 - bp) * a)
    ps, pa = pop(t, ts + 0.15, 0.4, s0=0.3)
    put(f, starred_pill(), bx - 60, by + 150, ps, pa * a)
    ps, pa = pop(t, K["support"], 0.42, s0=0.3)
    put(f, chip("SUPPORT INDIAN DEVS", GREEN, WHITE, 30, 84, "heart"), CX, 1240 + dy, ps, pa * a)
    ps, pa = pop(t, K["support"] + 0.4, 0.38)
    put(f, repo_logo(110), CX - 290, 1240 + dy, ps, pa * a)


# ------------------------------------------------------------------ S14: outro — follow Computer Hub
def s_outro(f, t):
    t0 = K["s13_end"]
    s, a, dy = trans(t, t0, None, din=0.6, s0=0.5)
    bob = 5 * math.sin((t - t0) * 2.0) * prog(t, t0 + 1.0, 1.0)
    cy = 860 + dy + bob
    tr, k = t0 + 0.15, 0
    while tr < t and k < 8:
        pr = prog(t, tr, 1.4)
        if 0 < pr < 1:
            put(f, ring(165, INDIGO if k % 2 == 0 else CYAN, 5), CX, cy, s * (0.98 + 0.5 * out_cubic(pr)),
                (1 - pr) * 0.45 * a)
        tr += 1.5
        k += 1
    put(f, logo_shadow(330), CX, cy, s, a * 0.9)
    put(f, logo(330), CX, cy, s, a)
    ps, pa = pop(t, t0 + 0.2, 0.4)
    put(f, pill("AWESOME REPOS · DAY 1", tint(INDIGO, 0.88), INDIGO, size=20, h=52, icon_name="star",
                icon_col=INDIGO), CX, 640, ps, pa)
    ps, pa = pop(t, t0 + 0.35, 0.4)
    put(f, handle_pill(42), CX, 1100, ps, pa)
    for lab, ic, bg, tc, x, key in [("OPEN SOURCE", "code", tint(INDIGO, 0.86), INDIGO, CX - 170, "tools"),
                                    ("DEV TOOLS", "bolt", tint(CYAN, 0.86), BLUE, CX + 175, "tools2")]:
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
    ps, pa = pop(t, tf + 1.0, 0.4)
    put(f, label_pill("REPO LINK IN BIO · COMMENT FOR DM", tint(BLUE, 0.88), BLUE, "chat", 20, 56), CX, 1430, ps, pa)


SCENES = [
    (0.0, K["s1_end"] + 0.05, s_fee),
    (K["s1_end"], K["s2_end"] + 0.05, s_loss),
    (K["s2_end"], K["s3_end"] + 0.05, s_dev),
    (K["s3_end"], K["s4_end"] + 0.05, s_series),
    (K["s4_end"], K["s5_end"] + 0.05, s_selfhost),
    (K["s5_end"], K["s6_end"] + 0.05, s_qr),
    (K["s6_end"], K["s7_end"] + 0.05, s_direct),
    (K["s7_end"], K["s8_end"] + 0.05, s_verify),
    (K["s8_end"], K["s9_end"] + 0.05, s_features),
    (K["s9_end"], K["s10_end"] + 0.05, s_setup),
    (K["s10_end"], K["s11_end"] + 0.05, s_note),
    (K["s11_end"], K["s12_end"] + 0.05, s_link),
    (K["s12_end"], K["s13_end"] + 0.05, s_star),
    (K["s13_end"], TOTAL_LEN + 0.1, s_outro),
]


def _events():
    e = [(0.05, "shimmer", -2, 0.5, {}), (K["razorpay"], "pop", -6, 0.5, {}), (K["two"], "alert", -5, 0.4, {}),
         (K["gst"], "pop", -6, 0.6, {"pitch": 1.2})]
    for key in ["s1_end", "s2_end", "s3_end", "s4_end", "s5_end", "s6_end", "s7_end", "s8_end", "s9_end",
                "s10_end", "s11_end", "s12_end", "s13_end"]:
        e.append((K[key] - 0.02, "whoosh", -1, 0.5, {}))
    e += [(K["lakh"], "rise", -6, 0.4, {}), (K["hazaar"], "rise", -5, 0.6, {}), (K["fees"], "alert", -4, 0.5, {}),
          (K["free"], "chime", -6, 0.4, {}), (K["opensource"], "pop", -6, 0.6, {"pitch": 1.2}),
          (K["day1"], "pop", -3, 0.5, {"pitch": 0.75}), (K["upi_gw"], "shimmer", -3, 0.5, {}),
          (K["mayank"], "pop", -6, 0.5, {"pitch": 1.1}), (K["server"], "pop", -7, 0.6, {}),
          (K["qr"], "rise", -6, 0.5, {}), (K["gpay"], "pop", -8, 0.35, {}),
          (K["phonepe"], "pop", -8, 0.5, {"pitch": 1.15}), (K["paytm"], "pop", -8, 0.65, {"pitch": 1.3}),
          (K["bichauliye"] + 0.4, "swipe", -6, 0.5, {}), (K["zero"], "chime", -5, 0.5, {}),
          (K["verify"], "pop", -7, 0.4, {}), (K["webhook"], "swipe", -7, 0.5, {}),
          (K["successful"], "chime", -5, 0.6, {}), (K["dashboard"], "pop", -7, 0.4, {}),
          (K["api"], "pop", -7, 0.6, {"pitch": 1.15}), (K["rotation"], "click", -8, 0.5, {}),
          (K["setup"], "click", -9, 0.5, {}), (K["laravel"], "pop", -6, 0.4, {}),
          (K["upi_only"], "pop", -7, 0.4, {}), (K["legit"], "pop", -7, 0.6, {"pitch": 1.15}),
          (K["bio"] + 0.3, "click", -4, 0.5, {}), (K["comment"], "click", -6, 0.5, {}),
          (K["dm"], "chime", -5, 0.6, {}), (K["star"], "click", -2, 0.55, {}), (K["star"] + 0.05, "shimmer", -3, 0.5, {}),
          (K["support"], "pop", -6, 0.5, {}), (K["s13_end"] + 0.1, "shimmer", 0, 0.5, {}),
          (K["follow"], "click", -1, 0.55, {})]
    return sorted(e, key=lambda x: x[0])


EVENTS = _events()
