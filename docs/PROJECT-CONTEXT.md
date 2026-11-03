# Project context — Computer Hub Instagram Reel series

## What we are building
A series of 9:16 Instagram Reels (1080x1920, 30 fps, H.264 + AAC) for Computer Hub (@computer__hub — two underscores).
Episode 1 narration = `voice.mp3` (Hindi/Hinglish intro about "My Plan B journey with AI", 56.7 s).

**Series look (updated 2026-11-01): LIGHT theme on Gemini background plates in logo colours.** Ayush tried a
dark version (`output/ComputerHub_Reel_dark.mp4`) and did not like it. Current candidates: `ComputerHub_Reel_layers.mp4`
and `ComputerHub_Reel_doodles.mp4`. The first paper version is `output/ComputerHub_Reel_final.mp4`.
(The "Series style rules" section below describes the dark setup; it is kept for reference only.)

## Series style rules (keep the same in every episode)
- **Background:** `assets/backgrounds/ref_bg.png` (made by Ayush in Gemini: dark navy nebula, cyan + purple light
  clouds, green circuit frame, dark empty centre). The renderer animates it: slow zoom + drift, light pulses running
  along the green circuit lines, ~70 twinkling particles.
- **New episode background:** make it in Gemini by uploading `ref_bg.png` as the style reference and changing only
  the pattern (hexagon grid, perspective grid floor, light waves, data streams...). Save as
  `assets/backgrounds/epNN.png`, then render with `$env:BG = "assets/backgrounds/epNN.png"`.
- **Cards:** dark glass (fill `PAPER` #0E152A at ~91% opacity, muted-cyan border, soft cyan glow, light text).
- **Captions:** stay WHITE boxes with dark text + blue keywords (most readable on mobile), upper part of screen,
  word-by-word pop-in.
- **Header pill:** dark glass with cyan border, mini logo + "COMPUTER HUB · …" (series/episode label can change).
- **Outro:** logo with cyan glow + rings, @computer__hub pill, Follow button click.
- Palette lives in `source/gfx.py` (top of file). One accent colour with cyan per episode; not all colours at once.
- Note: `ref_bg.png` has a small Gemini sparkle mark in the bottom-right corner. It is still visible in the video.

## Key decisions
- Captions in **Roman Hinglish** (same as the reference reel). "Plan B" follows the script (audio sounds like "plan bhi").
- Word timings from faster-whisper word timestamps (Hub84 Hinglish model + Whisper small). All timings live in
  `source/captions_data.py`.
- Everything is generated in code (Python + Pillow + numpy), no paid tools: motion graphics, music, sound effects.
- Fonts: Segoe UI (Bold/Black/Semibold) + Consolas (Windows built-in).
- Logo: `assets/logo_transparent.png` = original artwork, only the black outside the cyan scalloped edge removed.
- Video length 60.0 s: narration + 3.3 s outro tail.
- Audio: voice gain + transparent limiter only (−14 LUFS, −1 dBTP). Music ≈ −19 dB under voice + 5 dB ducking.

## Folder map
- `voice.mp3`, `logo.jpg`, `ref_reel.mp4` — original inputs (do not edit). `ref_bg.png` — Ayush's original Gemini plate.
- `source/` — all scripts. `background.py` has `ImageBackground` (dark series) and the old paper background.
- `assets/backgrounds/` — series background plates (`ref_bg.png`, later `ep02.png` …)
- `assets/` — transparent logo, `music_bed.wav`, `sfx/*.wav`
- `work/` — temp files (video renders, mix.wav, QC frames). Safe to delete.
- `output/` — deliverables: `ComputerHub_Reel_dark.mp4` (current), `ComputerHub_Reel_final.mp4` (old light), SRT, transcript, timeline

## How to rebuild (PowerShell, from the project folder)
```
py -I source/render.py video
py -I source/audio.py
py -I source/make_srt.py
```
Optional: pick another background and output name first:
```
$env:BG = "assets/backgrounds/ep02.png"
$env:OUT = "video_ep02.mp4"
```
Then mux (ffmpeg comes from the imageio-ffmpeg package):
```
$ff = py -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"
& $ff -y -i work/video_only.mp4 -i work/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest output/ComputerHub_Reel_dark.mp4
```
Test single frames: `py -I source/render.py stills 5.5 23.5` → `work/qc/`.

## Making the next episode (checklist)
1. New voiceover MP3 → transcribe with `source/transcribe.py` → write new `captions_data.py`.
2. New background from Gemini (style ref = `ref_bg.png`) → `assets/backgrounds/epNN.png`.
3. Write new scene functions in `scenes.py` for the new script (keep the card style and helpers).
4. Render, `audio.py`, `make_srt.py`, mux, QC frames.

## Status
- 2026-11-01: Dark series version rendered — `output/ComputerHub_Reel_dark.mp4`. Frames QC'd. Not yet checked by
  Ayush on a phone.

## Next steps
- Ayush reviews the dark version on phone. Then Episode 2 (new voiceover + new Gemini background).

## Background tests (2026-11-01)
- Ayush did NOT like the dark version. Going back to LIGHT backgrounds in logo colours. Dark code is still in the
  project (`ImageBackground`, dark palette in `gfx.py`); the light palette must be restored when a light background is chosen.
- `testing/` has 8 light 9:16 backgrounds (1536x2752 PNG) generated in Gemini (Pro account, model "4 Argon", Create image,
  9:16): 01 torn paper (+01b variant), 02 gradient mesh, 03 notebook doodles, 04 papercraft layers, 05 blueprint,
  06 frosted glass, 07 geometric flat, 08 isometric tech. Prompts are in the chat history (style + fixed rules block).
- Known issues: Gemini sparkle mark bottom-right on every image; image 01 has small fake text-like stamps on the edges.
- Ayush picked **layers** (04) and **doodles** (03). Copied to `assets/backgrounds/layers.png` and `doodles.png`.

## Theme switch (how it works now)
- `source/gfx.py` reads env `THEME` (default `light`). Light = white cards + soft drop shadows (first version's look).
  Dark = dark glass cards + cyan glow. Caption boxes are white in both.
- `BG` env = background plate. `ImageBackground` adds slow zoom + drift; circuit pulses and particles only in dark.
- Render one version (PowerShell):
  ```
  $env:THEME = "light"; $env:BG = "assets/backgrounds/doodles.png"; $env:OUT = "video_doodles.mp4"
  py -I source/render.py video
  ```
  then mux `work/video_doodles.mp4` + `work/mix.wav` into `output/` (same ffmpeg command as above).

## Episodes (from 2026-11-02)
- **Format chosen by Ayush:** the isometric version (`output/Final/ComputerHub_Reel_isometric.mp4`) is the reference
  look for every episode: `THEME=light`, `BG=assets/backgrounds/isometric.png`.
- Env `EP` picks the episode. Unset = pilot (`voice.mp3`, `captions_data.py`, `scenes.py`).
  `EP=day01` = `source/ep_day01.py` (VOICE, PHRASES, SCENES, EVENTS, HEADER, TOTAL_LEN, CAP_END in one file).
  Loader: `source/episode.py`. Per-episode files: `episodes/<ep>/` (voice copy, words.json, SRT); output `output/DayNN/`.
- **New episode steps (PowerShell, project folder):**
  ```
  py -I source/transcribe.py episodes/day02/voice.mp3 episodes/day02/words.json
  # write source/ep_day02.py (copy ep_day01.py: new PHRASES from words.json, new scenes, EVENTS)
  $env:EP = "day02"; $env:THEME = "light"; $env:BG = "assets/backgrounds/isometric.png"; $env:OUT = "video_day02.mp4"
  py -I source/render.py stills 1.0 10.0      # check frames in work/qc/
  py -I source/audio.py                         # -> work/mix_day02.wav
  py -I source/make_srt.py                      # -> episodes/day02/day02_captions.srt
  py -I source/render.py video                  # -> work/video_day02.mp4, then mux with mix_day02.wav
  ```
- **Day 1 (Chrome extension clone idea):** `output/Day01/ComputerHub_PlanB_Day01.mp4` (62 s) + `Day01_Post_Kit.md`
  (caption, cover, pinned comment, transcript, timeline) + SRT. Next video promised in the voice: Day 2 = how to sell
  and get customers.

- **Day 2 (first paying customers, 3-phase distribution):** `source/ep_day02.py`, voice copied to
  `episodes/day02/voice.mp3` (original in `output/Day 2/`). Output `output/Day02/ComputerHub_PlanB_Day02.mp4`
  (93.5 s) + `Day02_Post_Kit.md` + SRT. Day 2 reuses helpers from `ep_day01.py` (calendar card, coins, arrows).
  Voice promises Day 3 = "ek bilkul naya idea".

## Change log (newest first)
- 2026-11-03: Day 2 episode rendered. New icons: star, link, up, clock, cross, ticket.
- 2026-11-02: Episode system (`EP` env, `episode.py`, `ep_day01.py`). Rendered Day 1 pilot episode. New icons:
  puzzle, search, chat, play.
- 2026-11-01: Light/dark THEME switch added. Rendered `output/ComputerHub_Reel_layers.mp4` and
  `output/ComputerHub_Reel_doodles.mp4` (same voice, music, SFX, captions).
- 2026-11-01: Generated 8 light background tests in Gemini via Chrome and saved them in `testing/`.
- 2026-11-01: Switched to DARK series theme: `ref_bg.png` animated background (zoom/drift, circuit pulses, particles),
  dark glass cards with cyan glow, dark header/handle pills, cyan logo glow. `BG` / `OUT` env settings added.
- 2026-10-30: Fixed intro logo/Tech-card ghosting at 1.5 s; header pill for contrast; stereo loudness fix.
- 2026-10-30: Built renderer (background, captions, 11 scenes), synth music + SFX, final mux, SRT, transcript, timeline.
- 2026-10-30: Project started. Assets inspected, voice transcribed with faster-whisper.
