"""Which reel to build. Set env EP: unset or "pilot" = first reel (voice.mp3), "day01" = Day 1, ...

An episode module `ep_<name>.py` provides: VOICE, PHRASES, VOICE_LEN, TOTAL_LEN, CAP_END, HEADER, SCENES, EVENTS.
"""
import importlib
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = os.environ.get("EP", "pilot").lower()
FPS = 30

if EP == "pilot":
    import captions_data as _c
    import scenes as _s
    VOICE = os.path.join(ROOT, "voice.mp3")
    PHRASES, VOICE_LEN, TOTAL_LEN = _c.PHRASES, _c.VOICE_LEN, _c.TOTAL_LEN
    CAP_END = 57.4
    HEADER = "COMPUTER HUB · MY PLAN B JOURNEY"
    SCENES = _s.SCENES
    EVENTS = None  # audio.py uses its own pilot list
    MIX = os.path.join(ROOT, "work", "mix.wav")
    SRT = os.path.join(ROOT, "output", "ComputerHub_Reel_captions.srt")
else:
    _m = importlib.import_module("ep_" + EP)
    VOICE = _m.VOICE
    PHRASES, VOICE_LEN, TOTAL_LEN = _m.PHRASES, _m.VOICE_LEN, _m.TOTAL_LEN
    CAP_END = _m.CAP_END
    HEADER = _m.HEADER
    SCENES = _m.SCENES
    EVENTS = _m.EVENTS
    MIX = os.path.join(ROOT, "work", f"mix_{EP}.wav")
    SRT = os.path.join(ROOT, "episodes", EP, f"{EP}_captions.srt")
