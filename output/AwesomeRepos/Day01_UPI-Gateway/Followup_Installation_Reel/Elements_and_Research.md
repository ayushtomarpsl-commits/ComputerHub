# UPI Gateway follow-up reel — elements + research (2026-11-09)

For: a reel Ayush makes for the repo owner Mayank Singh (@mynkdev-21) to post. Theme: easy installation wizard +
security doubts cleared. Script NOT written yet (see `Idea_Notes.md`).

## Research — what changed in the repo since our viral reel
Checked with `gh api` on 2026-11-09 (repo: github.com/mynkdev-21/upi-gateway).
- **Stars 0 → 112, forks 46** (our reel effect). Last push 2026-11-09.
- **LICENSE file added (MIT)** — the "no license" issue we flagged is fixed. `SECURITY.md` added (how to report
  vulnerabilities privately; scope: auth bypass, XSS/CSRF/SQLi/SSRF, payment data exposure, key leakage, webhook forgery).
- **Installation wizard** (browser): open `https://yourdomain.com/install` → Requirements check → Database setup
  (test connection) → Migrations → Admin account → done. Installer **locks itself** after setup.
- **Production ZIP**: `upi-gateway-production.zip` (with SHA-256 checksum) — **no SSH, Composer, Node.js or npm needed**
  on the hosting server. Guides for **cPanel** (shared hosting) and **Ubuntu VPS**.
- **Security hardening** (Nov 8 commits: "security: complete gateway hardening and reliability remediation",
  "remediate verification node ID, installer HTTPS detection, production insecure flags"):
  - Separate **Live and Sandbox** environments, keys and data.
  - **Timestamped HMAC-SHA256 webhook signatures** (`t=…,v1=…`) with a 5-minute validity window (stops replay).
  - Separate **encrypted** Live/Sandbox webhook signing secrets; event IDs + sequence numbers; durable webhook outbox
    with retries.
  - "Confirm your password" screen before sensitive pages (seen in demo 1); login error message on wrong credentials.
  - Strict account rotation rule: never silently falls back; "must not be used to bypass bank velocity caps".
  - 79 automated tests passing; CI builds the production package.
- **Read-only live demo**: https://appnk.site/ (demo login is published in the README; data changes disabled).
- **Free installation support** on WhatsApp and GitHub issues (README warns: never share passwords / `.env`).
- Release status (README): v1.1.0 "stable release candidate"; developer still advises own testing before live payments.

## ⚠️ Flags — ask Mayank before using
1. **Demo 2 ends on "Installation complete — Setup not ready"** (red warning icon) although all 5 steps show ✓.
   Bad promo ending → ask for a clean success recording, or end on the migrations-success / admin screens + our own
   "Installation complete ✓" graphic.
2. Live site **Pricing section** (Free / Pro ₹999 / Business ₹2,999 per month) — conflicts with "100% free open source".
   Ask what these plans are before showing anything about price.
3. Live site **"What our users say" testimonials** — don't show unless Mayank confirms they are real users.
4. Comparison table says **"RBI registration needed: No"** — legal claim; don't put on screen as a promise.
5. `install_admin-account.png` shows Mayank's email (public in his README anyway) — fine for his own post, or blur.
6. Demo videos are small screen recordings (816×416, no audio) → fine as moving clips inside a phone/browser frame;
   use the HD repo screenshots for big still shots.

## HD update (2026-11-09)
Ayush sent the original HD screen recordings (same content, 1886×956, 60 fps):
`demo_videos/demo1_HD_app_tour.mov` (55 s) and `demo_videos/demo2_HD_install_wizard.mov` (48 s).
**Use `elements/demo_stills_HD/`** (same file names as `demo_stills/`, full 1886×956 + `d2_*_card.png` wizard crops
~1070×690) instead of the low-quality WhatsApp stills. HD tour timings: dashboard 31 s, orders 34 s, UPI accounts 35 s,
API reference 37 s, API & webhooks 39 s, confirm password 41 s, merchants 45 s, orders 53 s.
The HD wizard still ends on "Setup not ready" too (FLAG #1 stays).

## Elements (all in `elements/`)
| File | Size | Use for |
|---|---|---|
| `repo_screens/install_database-setup.png` | 1700×1816 | Wizard step: database setup (HD) |
| `repo_screens/install_migrations-success.png` | 1662×1840 | Wizard step: migrations log "completed successfully" (HD) |
| `repo_screens/install_admin-account.png` | 1408×1650 | Wizard step: create admin account (HD; shows his email) |
| `repo_screens/install_dashboard.png`, `install_home.png`, `install_payment-account.png` | ~2900 wide | Dashboard / homepage / add UPI account |
| `repo_screens/download.png` | 1584×396 | Mayank Singh profile banner → credit scene |
| `demo_stills/d2_01..05_*_card_2x.png` | ~920 wide | New polished wizard: readiness ✓, DB config, run migrations, create admin, complete (FLAG #1) |
| `demo_stills/d1_02_login.png`, `d1_03_login_error.png` | 816×416 | New login page + wrong-password error (security) |
| `demo_stills/d1_07_api_webhooks_live_sandbox.png` | 816×416 | Live / Sandbox keys (security) |
| `demo_stills/d1_08_confirm_password.png` | 816×416 | Confirm password before sensitive pages (security) |
| `demo_stills/d1_04_dashboard.png`, `d1_05_upi_accounts.png`, `d1_09_merchants.png`, `d1_10_orders_live_sandbox.png` | 816×416 | App tour |
| `live_demo/live_01_hero.png` | 2880×1640 | Homepage hero (HD) |
| `live_demo/live_02_stats_upi_apps.png` | 2880×660 | ₹0 fee · <5 s verify · 99.9% · 6 UPI apps + app logos strip |
| `live_demo/live_03_vs_traditional_gateways.png` | 1920×1120 | UPI Gateway vs traditional PG table (FLAG #4 on RBI row) |
| `live_demo/live_04_four_steps.png` | 2400×1180 | "Live in four simple steps" + API code card |
| `live_demo/live_login_2x.png` | 2880×1800 | New login page (HD) |
| `live_demo/live_05_pricing_FLAG.png` | 2400×800 | Pricing section — do not use until FLAG #2 is answered |
| `demo_videos/demo1_6.06PM.mp4` (55 s), `demo2_6.07PM.mp4` (48 s) | 816×416, 60 fps, silent | Moving clips: login→dashboard tour; full install wizard |
| `work_frames/` | — | every 2 s frames + contact sheets (reference only) |
Also reuse from Day 1: `../ui/elements/` (logo, QR card, payment success, GitHub page) and the Day 1 reel itself.
