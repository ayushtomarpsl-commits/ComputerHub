# Awesome Repos · Day 3 — Graveyard Check (research, benefits, hooks, video sequence)

**Repo:** https://github.com/TahaKotwal12/graveyard-check · **Site:** https://graveyard-check-ouxi.vercel.app/
**Developer (credit him):** Taha Kotwal — GitHub `@TahaKotwal12`
**Facts (checked 09-Nov-2026):** MIT license · TypeScript · v0.4.0 (released 18-Jul-2026) · npm package `graveyard-check`
· 10 stars, 1 fork, 13 commits, 10 open issues · topics: dependency-management, supply-chain, security, npm, python.
Site + CLI + GitHub Action + public "successor dataset". (The npm website showed a bot check, so no npm-page shot.)

---

## 1. What it is (one line)
**A free CLI that scans your project's dependencies, tells you which ones are dead (with proof), and tells you what
to switch to.** Works for JavaScript (npm, pnpm, yarn) and Python (requirements.txt, uv, Poetry).

Its own line: *"Dependabot tells you when there's a new version. Nothing tells you when there will never be a new version."*

## 2. The problem it solves (who feels the pain)
| Who | Pain |
|---|---|
| Developers on older projects | `npm install` floods "deprecated" warnings; nobody knows what is safe to replace |
| Teams / tech leads | A library died in 2022, the app still ships it; nobody noticed because "no updates available" |
| Security-minded devs | Dead library = no security fixes ever. `npm audit` says **"No fix available"** |
| Python devs | `nose`, `pycrypto`, `oauth2client` break on new Python versions; which fork is the real successor? |
| Freelancers / agencies | Inherit client projects full of abandoned packages; need a fast health report |
| Open-source maintainers | Want a weekly CI check that fails the build before a dead dependency hurts users |

**Real incidents it is built around:** `request` deprecated (Feb 2020), `node-sass` replaced by `sass`, `moment` in
maintenance mode, `tslint` → ESLint, and the Jan-2022 `colors`/`faker` sabotage. Python: `nose`, `pycrypto`,
`oauth2client`, `distutils`, `mock`.

## 3. How it works
1. Reads your lockfile (package-lock, pnpm-lock, yarn.lock, requirements.txt, uv.lock, poetry.lock).
2. Checks every dependency against the npm registry, PyPI and GitHub (deprecation flag, PyPI "Inactive" classifier,
   archived repo, last commit / release, README deprecation notes).
3. Gives one of **4 verdicts, always with evidence**: `maintained` · `at-risk` (12–24 months quiet) ·
   `likely-abandoned` (deprecated / inactive / archived / 24+ months) · `insufficient-data` (never guesses).
4. Suggests **verified successors** from a public, reviewable YAML dataset (e.g. request → got / axios,
   pycrypto → pycryptodome, oauth2client → google-auth).

Commands: `npm i graveyard-check` → `graveyard-check scan` · `graveyard-check check <pkg>` (exit code 1 if risky)
· `--json`, `--ecosystem pypi`, `--direct-only`, `--severity`. GitHub Action: `TahaKotwal12/graveyard-check@v1`
with `fail-on: likely-abandoned`, runs weekly.

## 4. Key benefits (pitch list)
1. **Finds dead dependencies Dependabot can't see** — Dependabot only acts when a new version exists.
2. **Tells you what to use instead** — verified successors, not just a red flag.
3. **Evidence, not vibes** — every verdict comes with proof ("No release in 3.1 years").
4. **Never guesses** — missing data = "insufficient-data", not a fake "maintained".
5. **JavaScript + Python in one tool** — npm, pnpm, yarn, pip, uv, Poetry.
6. **CI guard** — GitHub Action fails the build when a dependency is abandoned; weekly, not noisy.
7. **Security win** — abandoned code never gets security patches; catch it before attackers do.
8. **Private by design** — MIT, no account, no server, no telemetry; runs on your machine.
9. **Script-friendly** — JSON output and exit codes (use as a pre-install gate).
10. **Try in the browser, no install** — type a package name on the website and get the verdict live.
11. **Community dataset** — anyone can add a successor record via PR; no TypeScript needed.
12. **Free & open source** — a perfect first open-source contribution for students and devs.

## 5. Hooks — one per benefit (first line of the reel / on-screen title)
| Benefit | Hook (Hinglish) |
|---|---|
| Dead deps invisible | "Dependabot bolta hai sab up to date hai… par aapki library 2020 mein mar chuki hai 💀" |
| Successor | "Library dead hai — ab kya use karein? Ye tool naam bhi bata deta hai." |
| Evidence | "‘Ye package abandoned hai’ — proof ke saath: ‘No release in 4 years’." |
| Security | "Jo library update nahi hoti, uska security bug kabhi fix nahi hota. Kabhi nahi." |
| Python | "nose, pycrypto, oauth2client… Python 3.12 pe project kyun crash ho raha hai? Yahi wajah hai." |
| CI | "Dead dependency production mein jaane se pehle hi build fail kar do." |
| Privacy | "Na signup, na server, na tracking — sirf ek command: graveyard-check scan" |
| Browser try | "Install kiye bina check karo: package ka naam likho, 2 second mein verdict." |
| 2022 incident | "2022 mein ek developer ne apni hi library tod di — lakhon apps hil gaye. Aapka project safe hai?" |
| Contribution | "Pehla open-source PR karna hai? Ye repo ek YAML file se contribution leta hai." |

**Top 3 reel hooks (pick one):**
1. `[serious] Aapka project ek "zombie" library pe chal raha hai — aur Dependabot aapko kabhi nahi batayega. 💀`
2. `[curious] npm install karte hi ye yellow "deprecated" warnings dikhte hain? Unhe ignore karna sabse mehenga mistake hai.`
3. `[excited] Ek command — aur pata chal jayega aapke project ki kaunsi library mar chuki hai, aur uski jagah kya lagana hai.`

## 6. Draft voice script (~75 s, Hinglish — final version to be saved as Repo03_Voice_Script.txt)
```
[serious] Aapka project ek zombie library pe chal raha hai… aur Dependabot aapko kabhi nahi batayega.
[curious] npm install karte hi ye yellow "deprecated" warnings dikhte hain? Ya Python update karte hi tests crash?
[thoughtful] Problem ye hai: jo library abandoned ho chuki hai, usme kabhi new version aayega hi nahi — matlab koi security fix bhi nahi.
[excited] Welcome to Awesome Repos, Day 3 — Graveyard Check, by Taha Kotwal.
[informative] Ek command chalao — graveyard-check scan — aur ye aapki poori dependency list check karta hai: npm, pnpm, yarn, aur Python bhi.
[fast] Har package ko verdict milta hai — maintained, at-risk, ya likely-abandoned — aur saath mein proof: "No release in 4 years".
[happy] Sabse best part? Ye sirf problem nahi batata — replacement bhi batata hai. Request dead hai? Got ya axios use karo.
[informative] GitHub Action se ye har hafte check karta hai, aur dead dependency mile toh build fail kar deta hai.
[thoughtful] Na signup, na server, na tracking — MIT licensed, poora open source. Website pe bina install kiye bhi try kar sakte ho.
[friendly] Repo ka link chahiye? Comment karo "DEAD", main DM kar dunga. Taha ko GitHub pe ek star zaroor dena.
[excited] Aur aise hi awesome repos ke liye — Computer Hub ko abhi follow karo!
```

## 7. Video sequence (scene by scene, ~75 s, same Awesome Repos format: light theme cards + dark dev shots)
| # | Time | Voice beat | Elements (folder `elements/`) | Animation |
|---|---|---|---|---|
| 1 | 0–4 s | Hook: zombie library | `dev_errors/e09_dependabot_all_clear` → red glitch → skull | Card pops in, green ✓ flips to red ✗, small shake |
| 2 | 4–10 s | "deprecated" warnings / Python crash | `e01_npm_install_deprecated`, `e04_python_nose_crash` | **Typing animation** of `npm install`, yellow warnings scroll in line by line; zoom on `request@2.88.2` |
| 3 | 10–16 s | No new version = no security fix | `e02_npm_audit_no_fix`, `e11_security_risk_card`, `e05_colors_liberty_2022` | Zoom shot on "No fix available" (red underline sweep), LIBERTY lines flicker |
| 4 | 16–21 s | Awesome Repos · Day 3 reveal + credit | `hd/01_logo_wordmark`, `hd/03_headline`, `hd/27_github_repo_header`, `hd/31_github_star_button` | Day card (indigo) → logo slide → GitHub header, "by Taha Kotwal" pill |
| 5 | 21–28 s | One command scan | `hd/05_install_commands`, `hd/07_scan_terminal_npm` | **Typing animation** `npm i graveyard-check` → `graveyard-check scan`, output lines type in; zoom on "2 likely abandoned" |
| 6 | 28–36 s | Verdicts + proof | `hd/14_verdict_cards`, `hd/17_check_output` | 4 verdict chips drop in one by one; zoom to "No commits in 2.4 years" |
| 7 | 36–44 s | Replacement suggestion | `hd/25_try_it_request_result`, `hd/26_try_it_verdict_zoom` | Fake input **types "request"** + Check click (cursor) → result card slides up, zoom on "got / axios" |
| 8 | 44–50 s | Python too | `hd/12_scan_terminal_pypi`, `e06_pip_pycrypto_fail` | Split: red error left → green successor right (pycrypto → pycryptodome) |
| 9 | 50–57 s | GitHub Action / CI | `hd/18_github_action_yaml`, `e07_ci_build_failed`, `e08_scan_success` | YAML types in, CI run turns red ✗, then a later run turns green ✓ |
| 10 | 57–64 s | Private, open source, try in browser | `hd/09_features_row1`, `hd/10_features_row2`, `hd/28_github_about` | Feature cards fly in; badges "MIT · No server · No telemetry" |
| 11 | 64–71 s | CTA: comment DEAD + star | `hd/31_github_star_button`, comment box, DM bubble | Cursor clicks ⭐ Star (10 → 11 burst), comment types "DEAD", DM bubble |
| 12 | 71–76 s | Follow Computer Hub | Computer Hub logo outro | Same outro as every reel (Follow click) |

**Look:** keep our light isometric background + white caption box; dark terminal/screens sit on it as "devices"
(rounded, soft shadow). Accent colour = the site's orange (#ff8a1f) + red for errors, green for fixes.

## 8. Honest notes (keep the video trustworthy)
- It is **not a vulnerability scanner** — it complements `npm audit` / Dependabot, it doesn't replace them.
- Needs a `GITHUB_TOKEN` for big scans (GitHub allows only 60 requests/hour without one).
- Young project (10 stars, v0.4.0) — say "new tool", not "used by thousands".
- The error screens in `dev_errors/` are **recreations** of real, well-known messages (illustrations).

## 9. Elements index
- `elements/hd/01–24` — website, 2x HD (headline, terminals, features, verdicts, CLI, Action YAML, dataset, FAQ)
- `elements/hd/25–26` — live "Try it" result for `request` (real, from the website)
- `elements/hd/27–32` — GitHub repo (dark): header, About, files, README, Star button, v0.4.0 release
- `elements/dev_errors/e01–e11` — dark developer error / security screens
- Contact sheets: `elements/site_contact_sheet.jpg`, `elements/dev_errors_contact_sheet.jpg`
- Scripts: `source/repo03_ui_elements.py`, `source/repo03_dev_errors.py` (local only)
