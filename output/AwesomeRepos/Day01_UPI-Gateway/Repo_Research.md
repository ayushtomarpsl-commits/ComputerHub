# Awesome Repos · Day 1 — UPI Gateway (research notes)

**Repo:** https://github.com/mynkdev-21/upi-gateway
**Developer (give credit):** Mayank Singh — GitHub `@mynkdev-21`, Full Stack Developer, Founder @ AmTech INFO, Gorakhpur (India)
**Developer links (from his README):** LinkedIn linkedin.com/in/mynk-dev · Portfolio mayankdeveloper.site · Company amtechinfo.online · Telegram @mayankdeveloper
**Checked on:** 06-Nov-2026 (repo created 02-Nov-2026, last update 05-Nov-2026, 0 stars, 0 forks, 7 commits)

---

## 1. What it is — in one line
A **self-hosted UPI payment gateway**: your website creates an order → customer scans a dynamic QR (or taps
GPay/PhonePe/Paytm) → money goes **straight into your own UPI / bank account** → the gateway confirms the payment
and tells your website with a signed webhook. No middleman holds your money.

Repo's own tagline: *"Accept UPI payments directly in your bank account"* · *"Now live · 0% transaction fee"* ·
*"A complete UPI checkout, without a payment aggregator"*.

## 2. Why people care (the money angle)
- Razorpay pricing page (checked 06-Nov-2026): **2% platform fee per successful transaction** on domestic
  instruments (UPI, cards, netbanking) **+ 18% GST on the fee** → about **2.36%** per payment. Setup fee ₹0.
- Example: ₹1,00,000 sales/month → about **₹2,360/month** in fees. ₹10,00,000 → about **₹23,600/month**
  (≈ ₹2.8 lakh a year).
- With UPI Gateway + your own UPI ID / Paytm for Business QR: **no gateway % fee**. Your cost is only the server
  (a small VPS, roughly ₹300–800/month) and your time.

## 3. Features (from code + README)
| Feature | What it means |
|---|---|
| Dynamic QR per order | Exact amount + unique order reference in every QR (`upi://pay?pa=…&am=…&tr=ORD…`) |
| Hosted payment page | Ready checkout page: QR, GPay/PhonePe/Paytm/BHIM buttons, 15-min countdown timer |
| Auto verification | Checks payment status every ~3 s (Paytm for Business; Paytm PG; PhonePe PG) |
| Manual UTR fallback | For any UPI ID: customer enters 12-digit UTR, merchant approves |
| UPI account rotation | Many UPI accounts, daily limit per account, new orders move to the next account |
| Signed webhooks | `order.paid` / `order.expired`, HMAC-SHA256 `X-Signature`, retries + delivery logs |
| REST API | `POST /api/v1/orders`, `GET /api/v1/orders/{id}`, `GET /api/v1/accounts` (API key + secret) |
| Multi-merchant | Each merchant has own login, API keys, UPI accounts; admin panel for all |
| Dashboard | Collected today, total, pending, success rate, 7-day chart, getting-started checklist |
| API docs page | Built-in `/docs` page |

**Stack:** Laravel 12 · PHP 8.2+ · MySQL 8 or SQLite · Blade + Tailwind · Laravel Queue · Nginx + Supervisor.
**Install (dev):** `git clone` → `composer install` + `npm install` → `cp .env.example .env` → `php artisan key:generate`
→ `php artisan migrate` → `php artisan app:create-admin you@example.com` → `composer run dev` → open `127.0.0.1:8000`.

**Setup guide check (06-Nov-2026):** README has a full setup guide (local install + production: Nginx, Supervisor
queue worker, cron scheduler, MySQL, `.env` table) and it matches the code (`app:create-admin` exists and asks for a
password; `composer run dev` starts server + queue + logs + scheduler). Missing: no Windows/XAMPP or Docker steps,
no step-by-step for getting Paytm Business MID or PhonePe PG keys (only short hints on the "Add payment account"
screen), the one-command `composer run setup` is not mentioned, and `GATEWAY_ORDER_EXPIRY_MINUTES` (default 15) is
not in `.env.example`.

## 4. Payment flow (for the video animation)
1. Your website calls the API: "create order ₹199".
2. Gateway returns a payment link + UPI intent.
3. Customer scans the QR / taps their UPI app and pays.
4. Money lands **directly** in your UPI / bank account.
5. Gateway verifies the payment (auto, or UTR).
6. Order = PAID → signed webhook to your website → "Payment successful" page.

## 5. Honest limits (say at least one in the video — builds trust)
- **UPI only** for the free path. Cards / netbanking only through the Paytm PG or PhonePe PG options, and those
  providers charge their own fees.
- **Paytm for Business auto-verify uses an unofficial status API** (README says it "may stop working without
  notice"). The "Any UPI ID" mode needs manual UTR checking.
- **You host it yourself:** server, HTTPS, backups, queue worker and cron are your job.
- **Legal:** the README itself says the software is not a payment licence. Using it for **your own business** money
  into **your own account** is the safe use. Running it as a gateway for other businesses may need RBI
  payment-aggregator rules → take legal advice.
- No refunds, subscriptions or international payments like Razorpay.

**Fair wording for the video:** "Razorpay ka free alternative — **UPI payments ke liye**", not "Razorpay ko poora
replace kar dega".

## 6. Notes to send the developer before the promo (optional, helps him)
- README says **MIT License**, but the repo has **no LICENSE file** → GitHub shows "no license". Add a `LICENSE`
  file so people can legally use it (2 minutes on GitHub: Add file → Create new file → `LICENSE` → choose MIT).
- Add GitHub **topics** (upi, payment-gateway, laravel, razorpay-alternative, india) so people can find it.
- A short demo GIF at the top of the README and a live demo link would help a lot when traffic comes.

## 7. UI elements ready for the video
Folder: `ui/elements/` (made by `source/repo01_ui_elements.py` from the repo's own `screenshots/`). Originals in
`ui/original/`. Contact sheet: `ui/elements_contact_sheet.jpg`.

| File | Use in video |
|---|---|
| `upi_gateway_logo.png` | Repo logo (indigo tile + lightning bolt, rebuilt from the repo's logo component) |
| `github_repo_page.png`, `github_repo_header.png` | Credit scene: "mynkdev-21 / upi-gateway" on GitHub |
| `hero_headline.png` | "Accept UPI payments directly in your bank account" + "0% transaction fee" pill |
| `hero_qr_card.png` | QR card with "Payment received ₹2,499" + `order.paid → 200 OK` |
| `features_title.png`, `features_grid.png` | "A complete UPI checkout, without a payment aggregator" + 6 feature cards |
| `payment_page.png` | Customer checkout: QR, app buttons, 14:39 timer, UTR box |
| `verifying_card.png` | "Verifying your payment" |
| `success_card.png` | "Payment successful ₹199.90" |
| `dashboard_full.png`, `dashboard_stats.png` | Merchant dashboard |
| `provider_picker.png` | Paytm for Business / PhonePe PG / Paytm PG / Any UPI ID |
| `money_stays_yours.png` | "Your money stays yours… We never hold or settle funds." |
| `api_docs_hero.png` | API Reference banner (developer scene) |

**Repo brand colours:** indigo `#6366F1` → `#4338CA` (primary `#4F46E5`), dark navy checkout panel, success green,
font Inter. These fit our light theme well (white cards + indigo accents).
