"""Render the Computer Hub reel video track (1080x1920, 30 fps) with captions and motion graphics.

Usage:
  py -I source/render.py stills 0.5 5.6 23.5      -> PNG test frames in work/qc/
  py -I source/render.py video                    -> work/video_only.mp4 (no audio)
"""
import math
import os
import subprocess
import sys
import time
from functools import lru_cache
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import imageio_ffmpeg  # noqa: E402
from PIL import Image  # noqa: E402

from episode import CAP_END, FPS, HEADER, PHRASES, SCENES, TOTAL_LEN  # noqa: E402
from gfx import BLUE, CAP_BLUE, CAP_INK, CYAN, INK, INK2, PAPER, H, W, canvas, card, clamp, font, out_back, out_cubic, prog, put, rgba, text_w  # noqa: E402
import background  # noqa: E402
import scenes  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
WORK = os.path.join(ROOT, "work")

# ---------------------------------------------------------------- captions
CAP_TOP = 292
CAP_SIZE = 62
CAP_MAXW = 800
PADX, PADY, LINE_H = 52, 24, 82


def layout_phrases():
    f = font("bold", CAP_SIZE)
    space = f.getlength(" ") * 1.25
    out = []
    for i, (words, end) in enumerate(PHRASES):
        lines, cur, lw = [], [], 0.0
        for (wd, tw, hl) in words:
            ww = f.getlength(wd)
            if cur and lw + space + ww > CAP_MAXW:
                lines.append((cur, lw))
                cur, lw = [], 0.0
            lw = lw + (space if cur else 0) + ww
            cur.append((wd, tw, hl, ww))
        lines.append((cur, lw))
        bw = int(max(max(l for _, l in lines) + 2 * PADX, 360))
        bh = int(len(lines) * LINE_H + 2 * PADY)
        items = []
        for li, (ws, l) in enumerate(lines):
            x = (bw - l) / 2
            yc = PADY + LINE_H * (li + 0.5)
            for (wd, tw, hl, ww) in ws:
                items.append((wd, tw, hl, x + ww / 2 - bw / 2, yc - bh / 2))
                x += ww + space
        t_in = words[0][1] - 0.05
        out.append({"bw": bw, "bh": bh, "items": items, "t_in": t_in})
    for i, ph in enumerate(out):
        ph["t_out"] = out[i + 1]["t_in"] if i + 1 < len(out) else CAP_END
    return out


PH = layout_phrases()


@lru_cache(None)
def cap_box(bw, bh):
    return card(bw, bh, 30, fill=(255, 255, 255), border=(255, 255, 255), shadow=0.9, fill_a=255)


@lru_cache(None)
def word_sprite(word, hl):
    f = font("bold", CAP_SIZE)
    w = int(f.getlength(word) + 24)
    h = LINE_H
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(im).text((12, h / 2 + CAP_SIZE * 0.34), word, font=f, fill=rgba(CAP_BLUE if hl else CAP_INK), anchor="ls")
    return im


def draw_captions(frame, t):
    for ph in PH:
        if not (ph["t_in"] <= t < ph["t_out"]):
            continue
        pi = prog(t, ph["t_in"], 0.3)
        po = prog(t, ph["t_out"] - 0.12, 0.12)
        s = (0.8 + 0.2 * out_back(pi)) * (1 - 0.06 * po)
        a = out_cubic(clamp(pi * 2)) * (1 - po)
        cx = 540
        cy = CAP_TOP + ph["bh"] / 2 + 16 * (1 - out_cubic(pi))
        put(frame, cap_box(ph["bw"], ph["bh"]), cx, cy, s, a)
        for (wd, tw, hl, rx, ry) in ph["items"]:
            t0 = max(tw - 0.05, ph["t_in"])
            if t < t0:
                continue
            p = prog(t, t0, 0.24)
            ws = 0.55 + 0.45 * out_back(p, 2.2)
            wa = clamp(p * 3)
            wdy = 12 * (1 - out_cubic(p))
            put(frame, word_sprite(wd, hl), cx + rx * s, cy + (ry + wdy) * s, ws * s, wa * a)


# ---------------------------------------------------------------- header
@lru_cache(None)
def header():
    txt = HEADER
    size, sp = 22, 5
    tw = text_w(txt, "mono", size, sp)
    lg = 50
    h = 66
    w = int(8 + lg + 16 + tw + 40)

    def cb(p):
        p.rr((0, 0, w - 1, h - 1), h / 2, fill=rgba(PAPER, 225), outline=rgba(CYAN), width=2)
        p.text(8 + lg + 16, h / 2, txt, "mono", size, rgba(INK2), anchor="lm", spacing=sp)
        p.circ(8 + lg + 16 + tw + 18, h / 2, 4, fill=rgba(CYAN))
    img = canvas(w, h, cb)
    img.alpha_composite(scenes.logo(lg), (8, (h - lg) // 2))
    return scenes.with_shadow_pill(img, h)


def draw_header(frame, t):
    a = out_cubic(prog(t, 0.1, 0.5))
    put(frame, header(), 540, 222, 1.0, a)


# ---------------------------------------------------------------- frame
_bg = None


BG_IMAGE = os.environ.get("BG", os.path.join(ASSETS, "backgrounds", "ref_bg.png"))  # series background


def get_bg():
    global _bg
    if _bg is None and os.path.exists(BG_IMAGE):
        import gfx
        _bg = background.ImageBackground(BG_IMAGE, effects=(gfx.THEME == "dark"))
    if _bg is None:
        paths = [os.path.join(ASSETS, n) for n in ("bg_base.png", "bg_decor.png", "bg_torn.png")]
        b = background.Background.__new__(background.Background)
        if all(os.path.exists(p) for p in paths):
            b.base, b.decor, b.torn = [Image.open(p).convert("RGBA") for p in paths]
        else:
            b.__init__()
            for p, im in zip(paths, (b.base, b.decor, b.torn)):
                im.save(p)
        _bg = b
    return _bg


def render_frame(t):
    f = get_bg().frame(t)
    for (a, b, fn) in SCENES:
        if a <= t < b:
            fn(f, t)
    draw_header(f, t)
    draw_captions(f, t)
    return f


def _work(i):
    return render_frame(i / FPS).convert("RGB").tobytes()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "video"
    os.makedirs(WORK, exist_ok=True)
    get_bg()  # builds & saves bg layers once
    if mode == "stills":
        qc = os.path.join(WORK, "qc")
        os.makedirs(qc, exist_ok=True)
        for ts in sys.argv[2:]:
            t = float(ts)
            st = time.time()
            render_frame(t).convert("RGB").save(os.path.join(qc, f"t_{t:06.2f}.png"))
            print(f"t={t:.2f} {time.time() - st:.2f}s")
        return
    n = int(round(TOTAL_LEN * FPS))
    out = os.path.join(WORK, os.environ.get("OUT", "video_only.mp4"))
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    st = time.time()
    with Pool(int(os.environ.get("WORKERS", "10"))) as pool:
        for i, buf in enumerate(pool.imap(_work, range(n), chunksize=3)):
            ff.stdin.write(buf)
            if i % 150 == 0:
                print(f"frame {i}/{n}  {time.time() - st:.0f}s", flush=True)
    ff.stdin.close()
    ff.wait()
    print("done", out, f"{time.time() - st:.0f}s")


if __name__ == "__main__":
    main()
