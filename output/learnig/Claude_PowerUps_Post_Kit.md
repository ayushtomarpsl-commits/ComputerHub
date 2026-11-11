# Claude Power-Ups reel — post kit (11-Nov-2026)

Reel: `ComputerHub_Claude_PowerUps.mp4` (this folder) · built by `source/ep_learn01.py` (EP=learn01)
Voice used: `Claude_PowerUps_Voice_Script.txt` (v1, as generated).

## Verified facts (README / official plugin page, read 11-Nov-2026)
| # | Tool | Repo | Stars | What it really does | Install |
|---|---|---|---|---|---|
| 1 | OmniRoute | github.com/diegosouzapw/OmniRoute | ~86.4k, MIT | Self-hosted AI gateway: 1,400+ models, auto-fallback; "15–95% token savings" (eligible workloads) | `npm install -g omniroute` → `omniroute` |
| 2 | claude-mem | github.com/thedotmack/claude-mem | ~116k, Apache-2.0 | Claude Code plugin: memory of past sessions loaded into new ones | `npx claude-mem install` |
| 3 | Headroom | github.com/headroomlabs-ai/headroom | ~79.3k, Apache-2.0 | Compresses logs / tool outputs before the model; "21–57% fewer input tokens", same answers in their evals | `pip install "headroom-ai[all]"` → `headroom wrap claude` |
| 4 | claude-code-setup | claude.com/plugins/claude-code-setup | Anthropic verified, ~195K installs | Official plugin: scans the codebase, recommends subagents, hooks, skills, MCP servers, slash commands (read-only) | `/plugin install claude-code-setup@claude-plugins-official` |
| 5 | task-observer | github.com/rebelytics/one-skill-to-rule-them-all | ~3.9k, CC BY 4.0 | Claude skill: logs your corrections, suggests skill improvements — you approve | `npx skills add rebelytics/one-skill-to-rule-them-all --skill task-observer` |

## Where the v1 voice over-claims (screen shows the correct version)
- "99% developers" — made-up number (viral rules: no exaggeration).
- OmniRoute "90% tokens" — README: 15–95%, eligible workloads. "300+ models" is fine (1,400+).
- claude-mem "poora project yaad" — it remembers past sessions, not the whole codebase.
- Headroom "100% sateek" — not claimed; README: "same answers" in their tests, 21–57% fewer tokens.
- task-observer "auto-tune karta rehta hai" — it suggests; you approve. It does not change skills by itself.
- 3 CTAs (save + comment + follow) — rule is ONE CTA.

## v2 voice script (optional re-voice — fixes all of the above, ~75 s)
```
[frustrated] सिर्फ़ पाँच prompts… और Claude बोलता है—"Usage limit reached." [short pause] [confident] गलती Claude की नहीं, आपके setup की है। ये पाँच tools लगाओ—और आख़िरी वाला सबसे underrated है।
[thoughtful] नंबर एक: OmniRoute. एक free gateway, जो चौदह सौ से ज़्यादा AI models से जुड़ता है—एक model रुके, तो अपने-आप दूसरे पर switch। और prompts को compress करके tokens भी बचाता है। [chuckles] एकदम कंजूस दोस्त!
[thoughtful] नंबर दो: Claude Mem. अब Claude को गजनी वाली बीमारी नहीं—ये पिछले sessions का काम याद रखता है, तो हर नए chat में अपनी रामकथा दोबारा नहीं सुनानी पड़ेगी।
[thoughtful] नंबर तीन: Headroom. लंबे error logs और tool outputs को AI तक पहुँचने से पहले छोटा कर देता है—उनके tests में जवाब वही, पर input tokens बीस से सत्तावन प्रतिशत तक कम।
[thoughtful] नंबर चार: Claude Code Setup—Anthropic का अपना official plugin. आपका project scan करके बताता है कि कौन से subagents, hooks और skills लगाने चाहिए।
[curious] और नंबर पाँच—Task Observer. ये नोट करता है कि आप Claude को बार-बार क्या सुधारते हो, और आपकी skills बेहतर बनाने के suggestions देता है—approve आप करते हो।
[excited] पाँचों के links और install commands चाहिए? नीचे comment करो 'PLUGIN'—पूरी list सीधे आपके DM में!
```
(Follow only in the outro animation — no spoken follow line.)

## Caption (copy-paste)
```
Claude pe baar baar "Usage limit reached"? 😤 Galti Claude ki nahi, setup ki hai.

Ye 5 tools lagao 👇
1️⃣ OmniRoute — 1,400+ AI models ka gateway + auto-fallback
2️⃣ claude-mem — sessions ke beech Claude ki memory
3️⃣ Headroom — logs/tool output compress = kam tokens
4️⃣ claude-code-setup — Anthropic ka official setup advisor
5️⃣ task-observer — tumhari corrections se skills improve

💬 Comment "PLUGIN" — links + install commands seedhe DM mein

#ClaudeAI #ClaudeCode #AITools #Developers #Coding #AIIndia #Anthropic
```

## CreatorFlow DM (keyword PLUGIN, "next post")
```
Hey! 👋 Ye rahe 5 Claude power-ups 🚀

1) OmniRoute — AI gateway, 1,400+ models, auto-fallback
github.com/diegosouzapw/OmniRoute
npm install -g omniroute

2) claude-mem — memory across sessions
github.com/thedotmack/claude-mem
npx claude-mem install

3) Headroom — compresses logs & tool output
github.com/headroomlabs-ai/headroom
pip install "headroom-ai[all]"

4) claude-code-setup — official Anthropic plugin
claude.com/plugins/claude-code-setup
/plugin install claude-code-setup@claude-plugins-official

5) task-observer — improves your skills from your corrections
github.com/rebelytics/one-skill-to-rule-them-all

Note: apne API keys use karo aur har provider ke terms follow karo. Aise aur AI tools ke liye @computer__hub follow kar lo! 🙌
```
CreatorFlow: DM text max 1000 chars — this is ~820. Link button title max 20 chars ("Claude Power-Ups").
