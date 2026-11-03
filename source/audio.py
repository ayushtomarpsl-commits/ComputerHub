"""Make the soundtrack: original voice (gain only) + soft ambient synth music (ducked under the voice)
+ subtle UI sound effects. Writes assets/music_bed.wav, assets/sfx/*.wav and work/mix.wav.

Usage: py -I source/audio.py
"""
import json
import os
import re
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from scipy import signal
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import episode  # noqa: E402
from episode import TOTAL_LEN, VOICE_LEN  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
FF = imageio_ffmpeg.get_ffmpeg_exe()
rng = np.random.default_rng(5)

VOICE_TARGET = -14.0      # LUFS (stereo) for the narration, Instagram-friendly
MUSIC_UNDER_VOICE = -20.0  # music level relative to voice while speaking (~10% perceived)
DUCK_DB = 5.0              # extra dip while the narration is playing
SFX_UNDER_VOICE = -15.0    # sound effects stay well below the voice


def lufs(x):
    """Integrated loudness via ffmpeg loudnorm analysis."""
    tmp = os.path.join(ROOT, "work", "_lufs.wav")
    write(tmp, x)
    r = subprocess.run([FF, "-hide_banner", "-i", tmp, "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    js = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S).group(0))
    return float(js["input_i"]), float(js["input_tp"])


def write(path, x):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    y = np.clip(x, -1, 1)
    wavfile.write(path, SR, (y * 32767).astype(np.int16))


def db(v):
    return 10 ** (v / 20)


def load_voice():
    raw = subprocess.run([FF, "-v", "error", "-i", episode.VOICE, "-f", "f32le", "-ac", "1",
                          "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def limit(x, ceiling_db=-1.5):
    """Lookahead peak limiter (ffmpeg alimiter)."""
    tmp_in = os.path.join(ROOT, "work", "_lim_in.f32")
    x.astype(np.float32).tofile(tmp_in)
    raw = subprocess.run([FF, "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", tmp_in, "-af",
                          f"alimiter=limit={db(ceiling_db):.4f}:attack=4:release=60:asc=1:level=disabled",
                          "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)[: len(x)]


# ------------------------------------------------------------------ music
def note_hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def pad_voice(freq, dur, detune_cents=7):
    t = np.arange(int(dur * SR)) / SR
    out = np.zeros_like(t)
    for dc in (-detune_cents, 0, detune_cents):
        f = freq * 2 ** (dc / 1200)
        ph = rng.uniform(0, 2 * np.pi)
        for h in range(1, 9):
            if f * h > 9000:
                break
            out += np.sin(2 * np.pi * f * h * t + ph * h) / h ** 1.9
    return out / 3


def reverb(x, secs=2.8, mix=0.35):
    n = int(secs * SR)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * secs / 6.5))
    ir = signal.sosfilt(signal.butter(2, 5000, "low", fs=SR, output="sos"), ir)
    ir /= np.sqrt((ir ** 2).sum())
    wet = signal.fftconvolve(x, ir)[: len(x)]
    return x * (1 - mix) + wet * mix * 1.6


def make_music(length):
    n = int(length * SR)
    L = np.zeros(n)
    R = np.zeros(n)
    # D major ambient progression (MIDI notes), 7.5 s per chord
    chords = [[50, 62, 66, 69, 73], [47, 59, 62, 66, 69], [43, 55, 59, 62, 66], [45, 57, 62, 64, 69]]
    seg = 7.5
    k = 0
    tpos = 0.0
    while tpos < length:
        ch = chords[k % 4]
        dur = seg + 3.0
        st = int(tpos * SR)
        m = int(dur * SR)
        tt = np.arange(m) / SR
        env = np.minimum(1, tt / 2.2) * np.minimum(1, np.maximum(0, (dur - tt) / 2.8))
        env = env ** 1.5
        for j, nn in enumerate(ch):
            v = pad_voice(note_hz(nn), dur) * env * (0.55 if j == 0 else 0.32)
            pan = 0.5 + (j - 2) * 0.12
            e = min(n, st + m)
            L[st:e] += v[: e - st] * (1 - pan)
            R[st:e] += v[: e - st] * pan
        # soft sub
        sub = np.sin(2 * np.pi * note_hz(ch[0] - 12) * tt) * env * 0.25
        e = min(n, st + m)
        L[st:e] += sub[: e - st]
        R[st:e] += sub[: e - st]
        tpos += seg
        k += 1
    # gentle movement: slow low-pass "breathing" by mixing a darker copy
    sos = signal.butter(2, 900, "low", fs=SR, output="sos")
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * np.arange(n) / SR / 9.0)
    L = L * (0.55 + 0.45 * lfo) + signal.sosfilt(sos, L) * (1 - lfo) * 0.6
    R = R * (0.55 + 0.45 * (1 - lfo)) + signal.sosfilt(sos, R) * lfo * 0.6
    # sparse soft bell arpeggio (futuristic texture, no drums)
    tones = [74, 78, 81, 85, 86, 90, 93]
    t_ = 2.0
    while t_ < length - 2:
        if rng.random() < 0.55:
            f = note_hz(int(rng.choice(tones)))
            m = int(1.6 * SR)
            tt = np.arange(m) / SR
            bell = (np.sin(2 * np.pi * f * tt + 0.8 * np.sin(2 * np.pi * f * 2.0 * tt) * np.exp(-tt * 6))
                    * np.exp(-tt * 3.2) * np.minimum(1, tt / 0.004)) * 0.10
            st = int(t_ * SR)
            e = min(n, st + m)
            pan = rng.uniform(0.25, 0.75)
            L[st:e] += bell[: e - st] * (1 - pan)
            R[st:e] += bell[: e - st] * pan
        t_ += 0.6
    # airy noise texture
    noise = rng.normal(0, 1, (2, n))
    noise = signal.sosfilt(signal.butter(2, [2500, 7000], "band", fs=SR, output="sos"), noise)
    nl = 0.012 * (0.6 + 0.4 * np.sin(2 * np.pi * np.arange(n) / SR / 7.0))
    L += noise[0] * nl
    R += noise[1] * nl
    L, R = reverb(L), reverb(R)
    # fade in / out
    fade = np.ones(n)
    fi = int(1.2 * SR)
    fo = int(2.2 * SR)
    fade[:fi] = np.linspace(0, 1, fi)
    fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
    return np.stack([L * fade, R * fade])


# ------------------------------------------------------------------ sound effects
def env_exp(m, tau, attack=0.003):
    t = np.arange(m) / SR
    return np.minimum(1, t / attack) * np.exp(-t / tau)


def sfx_pop(pitch=1.0):
    m = int(0.18 * SR)
    t = np.arange(m) / SR
    f = (520 + 520 * np.exp(-t / 0.025)) * pitch
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * env_exp(m, 0.05, 0.002)
    return x * 0.8


def sfx_click():
    m = int(0.06 * SR)
    n = rng.normal(0, 1, m) * env_exp(m, 0.004, 0.0005)
    n = signal.sosfilt(signal.butter(2, 2500, "high", fs=SR, output="sos"), n)
    t = np.arange(m) / SR
    tone = np.sin(2 * np.pi * 2100 * t) * env_exp(m, 0.012, 0.0005)
    return n * 0.5 + tone * 0.45


def sfx_whoosh(dur=0.5, up=True):
    m = int(dur * SR)
    t = np.arange(m) / SR
    noise = rng.normal(0, 1, m)
    centers = [250, 400, 650, 1000, 1600, 2500, 4000, 6000]
    out = np.zeros(m)
    pos = t / dur
    track = np.log(300) + (np.log(5000) - np.log(300)) * (pos if up else 1 - pos)
    for c in centers:
        b = signal.sosfilt(signal.butter(2, [c / 1.35, c * 1.35], "band", fs=SR, output="sos"), noise)
        w = np.exp(-((np.log(c) - track) ** 2) / 0.35)
        out += b * w
    envl = np.sin(np.pi * pos) ** 1.6
    return out * envl * 0.35


def sfx_chime():
    m = int(1.0 * SR)
    t = np.arange(m) / SR
    out = np.zeros(m)
    for f, d in [(1046.5, 0.0), (1568.0, 0.09)]:
        st = int(d * SR)
        tt = t[: m - st]
        tone = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 8)) \
            * env_exp(len(tt), 0.28, 0.003)
        out[st:] += tone
    return out * 0.45


def sfx_alert():
    m = int(0.6 * SR)
    t = np.arange(m) / SR
    out = np.zeros(m)
    for f, d in [(784.0, 0.0), (622.3, 0.12)]:
        st = int(d * SR)
        tt = t[: m - st]
        out[st:] += np.sin(2 * np.pi * f * tt) * env_exp(len(tt), 0.12, 0.004)
    return out * 0.45


def sfx_rise():
    m = int(0.55 * SR)
    t = np.arange(m) / SR
    f = 380 + 620 * (t / t[-1]) ** 1.5
    ph = 2 * np.pi * np.cumsum(f) / SR
    e = np.sin(np.pi * np.minimum(1, t / 0.55)) ** 1.2
    return (np.sin(ph) + 0.3 * np.sin(2 * ph)) * e * 0.3


def sfx_shimmer():
    m = int(1.8 * SR)
    t = np.arange(m) / SR
    out = np.zeros(m)
    for k in range(9):
        f = rng.uniform(1800, 5200)
        d = rng.uniform(0, 0.4)
        st = int(d * SR)
        tt = t[: m - st]
        out[st:] += np.sin(2 * np.pi * f * tt + rng.uniform(0, 6)) * env_exp(len(tt), 0.35, 0.01) / 9
    return out * 1.1


def sfx_swipe():
    m = int(0.16 * SR)
    n = rng.normal(0, 1, m)
    n = signal.sosfilt(signal.butter(2, [1800, 7000], "band", fs=SR, output="sos"), n)
    pos = np.arange(m) / m
    return n * np.sin(np.pi * pos) ** 2 * 0.35


SFX = {"pop": sfx_pop, "click": sfx_click, "whoosh": sfx_whoosh, "chime": sfx_chime, "alert": sfx_alert,
       "rise": sfx_rise, "shimmer": sfx_shimmer, "swipe": sfx_swipe}

# (time s, type, level dB relative to SFX base, pan 0..1, extra)
EVENTS = [
    (0.08, "shimmer", -2, 0.5, {}), (0.12, "pop", -6, 0.5, {"pitch": 0.8}),
    (1.50, "whoosh", 0, 0.5, {}), (1.86, "pop", -6, 0.45, {}),
    (4.33, "whoosh", 0, 0.5, {}), (5.12, "click", -3, 0.65, {}),
    (7.56, "pop", -8, 0.4, {"pitch": 1.2}), (8.74, "rise", -6, 0.5, {}),
    (9.82, "whoosh", 0, 0.5, {}), (14.18, "pop", -3, 0.4, {"pitch": 0.7}),
    (16.26, "alert", -4, 0.6, {}),
    (18.06, "whoosh", -1, 0.7, {}),
    (22.38, "whoosh", -1, 0.5, {}), (23.28, "chime", -3, 0.5, {}),
    (24.96, "whoosh", -1, 0.5, {}), (26.80, "swipe", -4, 0.5, {}),
    (27.68, "rise", -5, 0.5, {}), (28.24, "pop", -6, 0.5, {}), (30.38, "click", -5, 0.6, {}),
    (30.82, "whoosh", -1, 0.5, {}), (33.72, "click", -2, 0.65, {}),
    (34.90, "whoosh", -1, 0.5, {}),
    (35.28, "pop", -7, 0.35, {"pitch": 1.0}), (37.00, "pop", -7, 0.65, {"pitch": 1.12}),
    (38.50, "pop", -7, 0.35, {"pitch": 1.25}), (41.22, "pop", -7, 0.65, {"pitch": 1.4}),
    (42.40, "click", -9, 0.5, {}),
    (43.56, "whoosh", -1, 0.5, {}), (46.00, "swipe", -5, 0.5, {}),
    (50.72, "rise", -5, 0.5, {}),
    (52.02, "whoosh", -1, 0.5, {}), (52.12, "shimmer", 0, 0.5, {}),
    (56.25, "pop", -5, 0.5, {"pitch": 0.9}), (56.98, "click", -1, 0.55, {}),
]


def voice_env(v):
    """Smoothed speech envelope 0..1 (fast attack, slow release) for ducking."""
    win = int(0.03 * SR)
    rms = np.sqrt(np.convolve(v ** 2, np.ones(win) / win, mode="same"))
    on = (rms > db(-40)).astype(np.float64)
    out = np.zeros_like(on)
    a_att = np.exp(-1 / (0.04 * SR))
    a_rel = np.exp(-1 / (0.45 * SR))
    y = 0.0
    for i in range(0, len(on), 48):  # 1 ms steps for speed
        x = on[i]
        a = a_att if x > y else a_rel
        y = a ** 48 * y + (1 - a ** 48) * x
        out[i:i + 48] = y
    return out


def main():
    n = int(TOTAL_LEN * SR)
    voice = load_voice()
    vi, vtp = lufs(np.stack([voice, voice]).T)  # measured as it plays: centred stereo
    g = VOICE_TARGET - vi
    voice = limit(voice * db(g))  # clean gain + transparent peak limiter (no EQ / no change to the words)
    vo, vtp2 = lufs(np.stack([voice, voice]).T)
    print(f"voice: {vi:.1f} LUFS, TP {vtp:.1f} -> gain {g:+.1f} dB + limiter -> {vo:.1f} LUFS, TP {vtp2:.1f}")
    v = np.zeros(n)
    v[: len(voice)] = voice[:n]
    vl, _ = lufs(np.stack([v, v])[:, : int(VOICE_LEN * SR)].T)

    music = make_music(TOTAL_LEN)
    ml, _ = lufs(music.T)
    music *= db(vl + MUSIC_UNDER_VOICE + DUCK_DB - ml)  # level in pauses; ducked while talking
    write(os.path.join(ROOT, "assets", "music_bed.wav" if episode.EP == "pilot" else f"music_bed_{episode.EP}.wav"), music.T)
    duck = db(-DUCK_DB * voice_env(v))
    music_d = music * duck[None, :]

    sfx = np.zeros((2, n))
    os.makedirs(os.path.join(ROOT, "assets", "sfx"), exist_ok=True)
    for name, fn in SFX.items():
        write(os.path.join(ROOT, "assets", "sfx", f"{name}.wav"), fn() if name != "pop" else fn(1.0))
    for (tm, kind, lvl, pan, kw) in (episode.EVENTS or EVENTS):
        x = SFX[kind](**kw) * db(lvl) * 0.5
        st = int(tm * SR)
        e = min(n, st + len(x))
        sfx[0, st:e] += x[: e - st] * np.sqrt(1 - pan) * 1.41
        sfx[1, st:e] += x[: e - st] * np.sqrt(pan) * 1.41
    sl, _ = lufs(sfx.T)
    sfx *= db(vl + SFX_UNDER_VOICE - sl)
    mix = np.stack([v, v]) + music_d + sfx
    pk = np.abs(mix).max()
    if pk > db(-1.0):
        mix *= db(-1.0) / pk
    write(episode.MIX, mix.T)
    mi, mtp = lufs(mix.T)
    m_only, _ = lufs((music_d[:, : int(VOICE_LEN * SR)]).T)
    print(f"mix: {mi:.1f} LUFS, TP {mtp:.1f}; voice {vl:.1f} LUFS, music under voice {m_only:.1f} LUFS "
          f"({m_only - vl:+.1f} dB vs voice); sfx track {vl + SFX_UNDER_VOICE:.1f} LUFS")


if __name__ == "__main__":
    main()
