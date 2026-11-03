"""Write output/ComputerHub_Reel_captions.srt from captions_data.PHRASES (same timings as the video)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from episode import PHRASES, SRT  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ts(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


lines = []
for i, (words, end) in enumerate(PHRASES):
    start = words[0][1]
    nxt = PHRASES[i + 1][0][0][1] if i + 1 < len(PHRASES) else end + 0.9
    stop = min(end + 0.35, nxt - 0.02)
    text = " ".join(w for w, _, _ in words).replace("'", "‘", 1).replace("'", "’", 1)
    lines.append(f"{i + 1}\n{ts(start)} --> {ts(stop)}\n{text}\n")
out = SRT
open(out, "w", encoding="utf-8").write("\n".join(lines))
print("wrote", out, len(lines), "cues")
