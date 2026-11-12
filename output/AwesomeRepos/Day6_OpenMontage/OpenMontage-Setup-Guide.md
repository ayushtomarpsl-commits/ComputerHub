# OpenMontage — Windows Setup Guide

> Turn your AI coding assistant (Claude Code, Cursor, Copilot, Codex, Windsurf) into a full **video production
> studio**: you describe the video, the agent researches, writes the script, makes the voice, finds visuals and
> music, adds captions and renders the final video. Free and open source.

| | |
|---|---|
| **What it is** | An open-source, agentic video production system: 10+ pipelines, 100+ tools, 700+ agent skill files |
| **GitHub repo** | [github.com/OpenMontageInc/OpenMontage](https://github.com/OpenMontageInc/OpenMontage) — about 79.7K stars, 10.7K forks (12 Nov 2026) |
| **License** | AGPL-3.0 (free to use; read the note in section 11 before using it inside a paid product) |
| **Who it is for** | Creators, small businesses, marketers and developers who want explainers, promos, reels and short films |
| **You need** | Windows 10/11, Python 3.10+, Node.js 22.23.4+ (or 24.x), FFmpeg, Git, and an AI coding assistant |
| **Cost to start** | ₹0 — works with zero API keys (free voice, free stock and archive footage). Paid AI video is optional |
| **Made by** | OpenMontage (community project) · guide by @computer__hub · Awesome Repos |

---

## Contents

1. [What it does](#1-what-it-does)
2. [What you need](#2-what-you-need)
3. [Install the tools](#3-install-the-tools)
4. [Install OpenMontage](#4-install-openmontage)
5. [First test with zero API keys](#5-first-test-with-zero-api-keys)
6. [Make your first video](#6-make-your-first-video)
7. [Watch it live: the Backlot board](#7-watch-it-live-the-backlot-board)
8. [The MASTER PROMPT (copy-paste this)](#8-the-master-prompt-copy-paste-this)
9. [Follow-up prompts](#9-follow-up-prompts)
10. [Costs and API keys](#10-costs-and-api-keys)
11. [Honest notes](#11-honest-notes)

---

## 1. What it does

You type one request in your AI coding assistant. The agent runs a full production line:

1. **Research** — searches the web for facts, data and audience questions on your topic.
2. **Proposal** — gives you concepts, the tools it will use and a cost estimate before spending anything.
3. **Script** — writes the narration; you approve or change it.
4. **Scene plan** — plans every scene.
5. **Assets** — voice, images or video clips, music, sound.
6. **Edit and compose** — puts it all together with captions (Remotion or HyperFrames).
7. **Self-review** — checks the file, frames, audio levels and subtitles before it shows you the result.

**Pipelines you can use:** animated explainer, animation, avatar spokesperson, cinematic trailer, clip factory
(long video → many shorts), documentary montage (real footage), hybrid, localization and dub, podcast repurpose,
screen demo, talking head.

**Favourite feature:** paste a Reel, Short or YouTube video you like — the agent studies its pacing, hook and
structure and gives you 2–3 original versions for your own topic.

---

## 2. What you need

- **Windows 10 or 11**, 8 GB RAM or more (16 GB is better), about 5 GB free disk.
- **Python 3.10+**, **Node.js 22.23.4+ or 24.x**, **FFmpeg**, **Git**.
- **An AI coding assistant**: Claude Code, Cursor, GitHub Copilot, Windsurf or Codex.
- Optional: an NVIDIA GPU for free local video generation.

---

## 3. Install the tools

Open **PowerShell** and run these one by one (skip anything you already have):

```powershell
winget install Git.Git
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
winget install Gyan.FFmpeg
```

Close PowerShell and open it again, then check:

```powershell
git --version
py --version
node --version
ffmpeg -version
```

If `node --version` shows lower than 22.23.4, install the newer LTS from nodejs.org.

---

## 4. Install OpenMontage

```powershell
git clone https://github.com/OpenMontageInc/OpenMontage.git
cd OpenMontage
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install "pip>=26.2.2"
python -m pip install -r requirements.txt
cd remotion-composer
npm install
cd ..
python -m pip install piper-tts
Copy-Item .env.example .env
```

**Common errors**

- *"running scripts is disabled on this system"* when activating: run
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, answer **Y**, and run the activate line again.
- `npm install` fails with `ERR_INVALID_ARG_TYPE`: run `npx --yes npm install` instead (inside `remotion-composer`).
- Mac/Linux users can just run `make setup`.

---

## 5. First test with zero API keys

Still inside the `OpenMontage` folder with the virtual environment active:

```powershell
python render_demo.py --list
python render_demo.py
```

This renders demo videos with no API keys (animated charts, text and data visuals) so you know the setup works.

---

## 6. Make your first video

1. Open the `OpenMontage` folder in your AI coding assistant (for Claude Code: open a terminal in the folder and run `claude`).
2. Type what you want, for example:
   `Make a 45-second animated explainer about why the sky is blue`
3. Approve the proposal, the script and the storyboard when it asks.
4. The finished file lands in `projects/<project-name>/renders/final.mp4`.

**Free real-footage path:** ask for a *documentary montage* and say *use real footage only* — it cuts real
clips from Archive.org, NASA, Wikimedia Commons, Pexels and more.

---

## 7. Watch it live: the Backlot board

```powershell
python -m backlot open
```

A local board shows every stage as it runs: the script as a screenplay page, scene cards, costs, and an
approval gate before the expensive render. Run `python scripts/backlot_simulate_run.py` to see a demo run.

---

## 8. The MASTER PROMPT (copy-paste this)

Paste this into your AI coding assistant inside the OpenMontage folder. Change the parts in [brackets].

```text
Read AGENT_GUIDE.md and PROJECT_CONTEXT.md first, then pick the right pipeline.

Make a [45]-second vertical 9:16 video for Instagram Reels about [my topic, e.g. "3 ways a small café can get more customers"].
Audience: [small business owners in India]. Language: [Hinglish narration, English on-screen text].
Style: [bright, modern, animated explainer with bold kinetic text].
Structure: a strong hook in the first 2 seconds, then value, then one clear call to action: "[Comment GUIDE for the free checklist]".
Use word-level captions, background music at low volume, and keep every scene under 4 seconds.
Use only free tools and free stock/archive media unless I approve a paid provider.
Before generating assets, show me: the proposal, the script, the scene plan and the total estimated cost. Wait for my approval at each gate.
At the end, give me the final video path and a short Instagram caption with 5 hashtags.
```

---

## 9. Follow-up prompts

- `Here is a Reel I like: [link]. Keep its pacing and hook style, but make it about [my topic]. Give me 3 variants.`
- `Make the hook stronger and cut the video to 30 seconds.`
- `Change the voice to a warmer, energetic male voice and lower the music by 30%.`
- `Turn this 20-minute video [file] into 5 short clips with captions, ranked by hook strength.`
- `Translate and dub this video into Hindi and English with matching subtitles.`
- `Make a 60-second documentary montage about [topic]. Real footage only, no narration, emotional music.`

---

## 10. Costs and API keys

- **₹0 path:** Piper voice (offline), Archive.org / NASA / Wikimedia footage, Remotion and FFmpeg. Free keys for
  Pexels, Pixabay and Unsplash add more stock media.
- **With AI image or video providers:** the project's own examples cost about **$0.15–$5 per video**
  (e.g. a 60-second animated short for **$1.33**).
- Add keys in the `.env` file, only the ones you have — for example `ELEVENLABS_API_KEY`, `FAL_KEY`,
  `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `PEXELS_API_KEY`.
- It shows a cost estimate before spending and supports spend caps — always read the estimate before you approve.
- Your AI coding assistant (Claude Code, Cursor, etc.) is billed separately by its own plan.

---

## 11. Honest notes

- **It needs an AI coding assistant** — OpenMontage is the studio, your assistant is the director.
- **Free videos look simpler** than paid AI-video ones; the best-looking cinematic results use paid video models.
- **License is AGPL-3.0:** free to use, but if you change the code and offer it to others as an online service,
  you must share your changes. Ask a lawyer before building a paid product on top of it.
- **Respect rights:** use footage and music with the right licence; don't copy someone else's video, only its style.
- Keep your API keys private — never post the `.env` file.

Made with ❤️ by **@computer__hub** · Follow for more free tools.
