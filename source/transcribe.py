# Transcribe voice.mp3 with word-level timestamps (Hinglish model + small Hindi model for cross-check)
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
from faster_whisper import WhisperModel

audio = sys.argv[1]; out = sys.argv[2]
import subprocess, numpy as np, imageio_ffmpeg
raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", audio, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
res = {}
for name, path, lang in [("hinglish", "Hub84/faster-whisper-hinglish-prime", "hi"), ("small", "small", "hi")]:
    m = WhisperModel(path, device="cpu", compute_type="int8", cpu_threads=12)
    segs, info = m.transcribe(audio, language=lang, word_timestamps=True, vad_filter=False, beam_size=5)
    words = []
    for s in segs:
        for w in s.words:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)})
    res[name] = words
    print(name, " ".join(x["w"] for x in words), flush=True)
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
