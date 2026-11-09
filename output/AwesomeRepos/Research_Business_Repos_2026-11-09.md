# Research: viral open-source repos for business owners (2026-11-09)

Goal: next Awesome Repos reels that can reach 1,000+ likes like the UPI Gateway reel (2.5–3 lakh views, client DMs).
What made UPI Gateway work: (1) a daily money pain (2% fees), (2) a free alternative, (3) an Indian connection.
GitHub numbers checked with `gh api` on 2026-11-09 (stars, last push, license, README).

## #1 Frappe Books — "Tally ka FREE alternative" (top pick)
- Repo: `frappe/books` · ⭐ 5,000+ · AGPL-3.0 · code active (last push Oct 2026; last release v0.36.0, Nov 2025)
- What: small-business accounting desktop app — invoicing, GST, POS (billing counter), inventory, reports.
- India: made in India (Frappe, Mumbai). Code has GST reports: `reports/GoodsAndServiceTax/GSTR1.ts`, `GSTR2.ts`,
  and an India regional model.
- Money hook: TallyPrime Silver ≈ ₹22,500 + GST, Gold ≈ ₹67,500 + GST, plus yearly renewal (TSS ≈ ₹4,500 / ₹13,500
  + GST). Frappe Books = ₹0. (Prices mostly from resellers — confirm on Tally's official site before using on screen.)
- Biggest plus: download-and-run desktop app (Windows/Mac/Linux), works OFFLINE, no server — any shop owner can use it.
- Caveats: not a full Tally replacement (check e-invoice / e-way bill); say "small business ke liye".
- Hook: "Tally ke ₹22,500 bachao 💸 Ye FREE accounting app GST bill bhi banata hai, aur internet ke bina bhi chalta hai!"

## #2 Listmonk — "Zerodha ke CTO ne banaya free Mailchimp"
- Repo: `knadh/listmonk` · ⭐ 24,000+ · AGPL-3.0 · active. Built by Kailash Nadh (Zerodha CTO); Zerodha Tech badge.
- What: self-hosted newsletter / mailing list manager (single binary + PostgreSQL, Docker).
- Hook: Mailchimp bills grow with contacts; this is free (pay only for sending, e.g. Amazon SES).
- Caveat: needs a server → good "setup as a service" angle for clients.

## #3 Chatwoot — WhatsApp + Instagram + website chat in one inbox
- Repo: `chatwoot/chatwoot` · ⭐ 39,000+ · active. Indian founders. "Captain" AI agent.
- Channels: website live chat, email, Facebook, Instagram, Twitter, WhatsApp, Telegram, Line, SMS.
- Replaces Intercom / Zendesk / WATI-type tools. Caveat: WhatsApp needs WhatsApp Business API (Meta charges per
  conversation).

## More options for later episodes
| Repo | Stars | Free alternative to | Note |
|---|---|---|---|
| frappe/erpnext | 41k | SAP / Zoho / full ERP | made in India, GST ready, heavy setup |
| twentyhq/twenty | 60k | Salesforce / Zoho CRM | AI-first CRM, trending |
| gitroomhq/postiz-app | 41k | Buffer / Hootsuite | social media scheduler |
| bagisto/bagisto | 28k | Shopify | Webkul (Noida) |
| makeplane/plane | 62k | Jira / Monday | Indian startup |
| nocodb/nocodb | 65k | Airtable | spreadsheet → app |
| n8n-io/n8n | 210k | Zapier | huge but already over-covered on reels |
| frappe/hrms | 9k | payroll software | salary + attendance |
| krayin/laravel-crm | 24k | CRM | Webkul (India) |
| documenso/documenso, OpenSignLabs/OpenSign | 16k / 7k | DocuSign | e-sign |
| invoiceninja/invoiceninja, akaunting/akaunting | 10k each | invoicing / accounting | |
| opensourcepos/opensourcepos | 4.5k | POS | |

## Order to make
1. Frappe Books (Tally) — biggest audience, easiest install, clear ₹ saving.
2. Listmonk (Zerodha CTO story) — story hook + client setup service.
3. Chatwoot (all DMs in one inbox) — business owners + agencies.
Every reel: client CTA "Setup karwana hai? DM 'BUILD'".

## Sources
- GitHub API (`gh api repos/<owner>/<repo>`, READMEs, file lists) — 2026-11-09.
- Tally prices: https://tallysolutions.com/business-guides/tallyprime-total-cost-of-ownership-india/ ·
  https://markitsolutions-website.pages.dev/pricing · https://markitsolutions-website.pages.dev/services/tally-renewal ·
  https://tallyatcloud.com/articles/tallyprime-pricing-in-india-2026-official-guide-for-businesses ·
  https://www.aiaccountant.com/blog/tally-prime-pricing-india (different figure: ₹18,000 / ₹54,000)
