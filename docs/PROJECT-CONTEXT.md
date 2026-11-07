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

- **Day 3 (Micro-SaaS: e-commerce report → GST/GSTR-1 file):** `source/ep_day03.py`, voice in
  `episodes/day03/voice.mp3` (original in `output/Day03/`). Uses Ayush's own tool screenshot
  `episodes/day03/gst_tool.png` (cropped) inside a browser frame. Output `output/Day03/ComputerHub_PlanB_Day03.mp4`
  (96.2 s) + `Day03_Post_Kit.md` + SRT. Voice CTA: comment "GST" → guide in DM.
- Note: Segoe UI / Consolas have no ✓ glyph — never type "✓" in sprite text; use the `check` icon instead.

## Link-in-bio page (2026-11-05)
- `linkpage/` = static page (index.html + logo, favicon, bg.jpg, og.jpg). Links still marked `PASTE_..._HERE` show as
  "Coming soon". Only Instagram is filled in; Ayush must add GST guide, GST tool, YouTube, WhatsApp channel, email.
- Deploy: `vercel --prod` inside `linkpage/` (steps in `linkpage/README.md`). After deploy, make og:image an absolute URL.
- Local preview: `.claude/launch.json` config "linkpage" (python http.server on port 8765).
- 2026-11-05: GST guide published as a readable PDF (`output/Day03/GST-Helper-Guide.pdf`, made from
  `D:\New folder\GST-Filing-E-Com\docs\GST-HELPER-REBUILD-KIT.html` via Edge print-to-PDF) and uploaded to the public
  Drive folder "GST Doc": https://drive.google.com/file/d/1DKXPbauUDKduDolWE5L2HczxlzaaaktO/view?usp=sharing
  (Drive shows the .html as raw code; Google Docs conversion failed). Link page: guide + GST tool
  (https://gst-helper-t4ug.onrender.com/) + Instagram filled. Instagram bio links can only be edited in the mobile app.
  The same Drive folder also holds Day03_Post_Kit.md (internal notes) — Ayush may want to move it out.

- **Day 4 (app idea: "BlaBlaCar for Parking"):** `source/ep_day04.py`, voice in `episodes/day04/voice.mp3` (original
  in `output/Day04/`). Output `output/Day04/ComputerHub_PlanB_Day04.mp4` (89.9 s) + `Day04_Post_Kit.md` + SRT.
  Voice CTA: comment "PARKING" → system design guide in DM. Next: Day 5 = final part of the series.
  New icons in gfx.py: car, pin, parking, home, shop, hospital, train.

- **Captions:** reusable SEO/engagement prompt in `docs/Caption_Generator_Prompt.md` (hook with keywords in line 1,
  4 different engagement actions, exactly 5 hashtags, alt text, pinned comment, reply templates). Day 4 post kit has
  the first caption written this way.

- **Link page is LIVE (2026-11-05):** https://computerhub-links.vercel.app (Vercel account ayushtomarpsl-6540, project
  `computerhub-links`). Redeploy after edits: `cd linkpage` then `vercel deploy --prod --yes`. `.vercelignore` keeps
  README.md and `.env*` off the site (Vercel wrote a private `.env.local` token file — never publish or commit it).
  Live links: GST guide PDF, GST tool, Instagram. "Coming soon": Parking guide (waiting for Ayush's doc), YouTube,
  WhatsApp, Contact. Instagram bio link must be changed in the mobile app (web can't edit links).
- **Comment replies:** GST reel — 1 comment for everyone + 24 personal replies posted on 2026-11-05 ~21:45 (pin the
  comment in the app). Next batch scheduled 22:53 (session-only cron). PARKING replies wait until the parking doc exists.
- **2026-11-05 22:53 result:** Instagram removed/hid 17 of the 24 batch replies (spam filter on similar replies); 7 still
  visible. Account Status all green (no limits). Decision: NO more scripted comment replies from Chrome. Use the pinned
  comment + Story link sticker + ManyChat (official API) instead. ~350 GST comments remain unreplied.
- **Parking guide is LIVE (2026-11-06):** https://computerhub-links.vercel.app/parking-guide.html — the "Parking App:
  System Design + Guide" card on the link page now opens it. Source of truth = `output/Day04/Parking-App-Rebuild-Kit.md`
  (architecture, data model, flows, API, screens, copy-paste MASTER PROMPT, follow-up prompts A–H, go-live costs).
  Based on a scan of `D:\New folder\parkingfriend` (Expo + Express + Turso). No secrets copied (Ola Maps key,
  google-services.json, JWT/ADMIN keys stay out). Rebuild the page: `py -I source/build_parking_guide.py`, then redeploy.
  PARKING commenters can now be pointed to the bio link (pinned comment / ManyChat, not scripted replies).

- **2026-11-06:** Posted the guide comment on the Day 4 reel (DfXL4qlyoFf) from Chrome: "📌 PARKING app ka FREE guide
  ready hai … computerhub-links.vercel.app/parking-guide.html | Link bio mein bhi hai …". Web menu only offers Delete,
  so Ayush must PIN it in the Instagram phone app (long-press / swipe left on the comment → pin icon).

## NEW SERIES: Awesome Repos (from 2026-11-06)
- One useful open-source GitHub repo per episode, promoted with credit to the developer. Same video format/UI as
  Plan B (light theme, white cards, Viraj voice). Header pill: `COMPUTER HUB · AWESOME REPOS · DAY N`.
- Folder per episode: `output/AwesomeRepos/DayNN_<Repo>/` with `Repo_Research.md`, `Script_Guide.md`,
  `ui/original/` (repo screenshots) and `ui/elements/` (crops + logo, made by `source/repoNN_ui_elements.py`).
- **Day 1 = UPI Gateway** by Mayank Singh (github.com/mynkdev-21/upi-gateway, Laravel 12, self-hosted UPI gateway,
  money goes straight to the merchant's own UPI; no gateway % fee). Razorpay pricing checked 06-Nov-2026: 2% + 18% GST.
  Honest limits: UPI only, Paytm for Business verify uses an unofficial API, self-host, own-business use (RBI).
  README says MIT but repo has no LICENSE file — ask Mayank to add one. Status: research + UI elements + script
  guide done. CTA: comment "REPO".
- **Day 1 reel RENDERED (2026-11-06):** `output/AwesomeRepos/Day01_UPI-Gateway/ComputerHub_AwesomeRepos_Day01.mp4`
  (91.2 s) + `repo01_captions.srt` + `Repo01_Post_Kit.md`. Code: `source/ep_repo01.py` (scenes) +
  `source/ep_repo01_timing.py` (PHRASES + `K` dict of keyword times — change times there, scenes follow).
  Voice: `episodes/repo01/voice.mp3` (ElevenLabs Viraj, 88.03 s). Series look: indigo (#4F46E5, the repo's colour)
  accents on our light theme, Day card in indigo with "Awesome Repos". Render (PowerShell):
  `$env:EP="repo01"; $env:THEME="light"; $env:BG="assets/backgrounds/isometric.png"; $env:OUT="video_repo01.mp4"`
  then `py -I source/audio.py`, `py -I source/render.py video`, `py -I source/make_srt.py`, mux with ffmpeg.

- Link page: "UPI Gateway: Free Razorpay Alternative" card (badge AWESOME REPOS · DAY 1) at the top of the list,
  opens the GitHub repo. Deployed 06-Nov-2026.

- **Positioning (2026-11-07):** Ayush is now a creator with 5+ years in tech who takes client work (websites, apps,
  AI tools, automation, UPI payments). Client CTA = DM "BUILD". Link page has a blue "Hire me" card at the top that
  opens Instagram DM (`https://ig.me/m/computer__hub`); add WhatsApp / email when Ayush gives them.
  Suggested Instagram name field: "Ayush Tomar | AI Developer · SaaS & Apps" (old fancy-font name is not searchable).

- **Link page order is automatic (2026-11-07):** lists with `data-sort="newest"` are sorted by each card's `data-date`,
  newest on top; undated cards (Instagram, YouTube, WhatsApp, Contact) stay at the bottom. New card = add
  `data-date="YYYY-MM-DDTHH:MM"`. TurtleReels card (Awesome Tools) added 2026-11-07, opens turtlereels.com.

- **TurtleReels promo (Awesome Tools, 2026-11-07):** folder `output/promotions/TurtleReels/` (Ayush's voice in
  `voice/`, his 1080x1920 sample renders in `clip of sample video/`). HD UI elements in `elements/hd/` (17 files,
  cut by `source/promo_turtlereels_elements.py`), map of element → script line in `elements/README.md`.
  CTA in the voice: link in bio + comment "TOOL" for DM.
- **TurtleReels reel RENDERED (2026-11-07):** `output/promotions/TurtleReels/ComputerHub_AwesomeTools_Day01_TurtleReels.mp4`
  (73.0 s) + `tool01_captions.srt`. Code: `source/ep_tool01.py` + `source/ep_tool01_timing.py` (K = keyword times).
  Env `EP=tool01`. Voice `episodes/tool01/voice.mp3` (69.96 s). Real renders play inside phone frames from
  `work/tool01_clips/c1..c3` (15 fps JPG frames). Header "COMPUTER HUB · AWESOME TOOLS · DAY 1", accent = mint green.

- **Auto DM (2026-11-07):** CreatorFlow free plan (500 DMs/month, 1 IG account; ManyChat free is only 25 contacts/month).
  Automation "Comments → DM" is LIVE: trigger = NEXT post or reel, any comment; DM text + button "Open TurtleReels"
  → https://turtlereels.com/; once per person. Public comment replies need CreatorFlow Pro. Manage at
  app.creatorflow.so/automations (Ayush's Google login). Instagram setting "Allow access to messages" must be ON.

## Change log (newest first)
- 2026-11-07: CreatorFlow comment-to-DM automation live for the next reel (TurtleReels link).
- 2026-11-07: Awesome Tools Day 1 reel (TurtleReels promo) rendered, 73 s.
- 2026-11-07: TurtleReels promo — HD elements captured (site 2x + logged-in dashboard) and mapped to the script.
- 2026-11-07: Link page — TurtleReels card + automatic newest-first sorting for links and episodes.
- 2026-11-07: Link page — "Hire me" card (Instagram DM) + new profile line (5+ yrs, builds for business).
- 2026-11-06: Awesome Repos Day 1 reel rendered (UPI Gateway, 91.2 s) + post kit + SRT.
- 2026-11-06: Link page — Awesome Repos Day 1 card (UPI Gateway → GitHub) added and deployed.
- 2026-11-06: Started "Awesome Repos" series; Day 1 (UPI Gateway) research, UI elements, script guide.
- 2026-11-06: Day 4 reel — parking guide comment posted (pin pending in the app).
- 2026-11-06: Parking App Rebuild Kit (md + styled HTML page with copy buttons) published at /parking-guide.html.
- 2026-11-05: Link page deployed to Vercel; Parking guide card + Day 4 episode added; journey strip = Day 4.
- 2026-11-05: SEO caption for Day 4 + reusable caption generator prompt.
- 2026-11-05: Day 4 episode rendered (parking app idea).
- 2026-11-05: Built the link-in-bio page (`linkpage/`).
- 2026-11-04: Day 3 episode rendered (GST Micro-SaaS idea, uses the real tool screenshot).
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
