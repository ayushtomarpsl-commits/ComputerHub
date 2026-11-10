# Awesome Repos · Day 4 — Twenty (open-source CRM) · research notes

**Repo:** https://github.com/twentyhq/twenty · website https://twenty.com · docs https://docs.twenty.com
**Checked on:** 10-Nov-2026 (GitHub API + README + LICENSE + official pricing page + docs)

## 1. Numbers (for the screen)
| | |
|---|---|
| Stars | **60,700+** ⭐ |
| Forks | 10,000+ |
| Contributors | **465+** |
| Started | Dec 2022 (about 3 years) |
| Latest release | **v2.57.1 on 9 Nov 2026** (updated almost every day) |
| Tagline | "The #1 Open-Source CRM" · "The open alternative to Salesforce, designed for AI" |
| Stack | TypeScript, React, NestJS, PostgreSQL, Redis |

## 2. What it is (one line)
A **free, open-source CRM** (customer + sales management software), like Salesforce / HubSpot / Zoho CRM, that you can
**host on your own server** or use on their cloud. Every lead, customer, deal, email, meeting and follow-up in one place.

## 3. Key features (from README + user guide)
- **Your own data model:** make any object and field (Leads, Deals, Properties, Students, Patients…). Unlimited records.
- **Views:** Table, **Kanban pipeline** (drag deals across stages), Calendar. Custom record pages and sidebar.
- **Email + calendar sync:** Google and Microsoft. Every email and meeting lands on the right customer automatically.
- **Email campaigns** built on your CRM data.
- **Workflows:** automate repetitive steps (new lead → assign → reminder → email).
- **AI agents and chat:** hand multi-step CRM chores to AI (Cloud plans include AI usage limits).
- **Dashboards:** live sales numbers.
- **Roles & permissions:** who sees what.
- **Import:** CSV or migrate from another CRM; **REST + GraphQL API**, webhooks.
- **Apps as code:** `twenty` CLI and SDK to build custom objects, views, agents; official **agent skills for Claude Code,
  Codex, Cursor** (build CRM features with AI).

## 4. License (say it correctly)
Mostly **AGPL-3.0** (free to use, modify and self-host). Some files are under an **Enterprise (commercial) licence**
(marked `@license Enterprise`), and the SDK/CLI/UI packages are **MIT**. Extra permission: apps you build on Twenty's
APIs do **not** have to be open source. → Safe wording: "**open source, free to self-host**".

## 5. Pricing (official page, checked 10-Nov-2026)
| Plan | Price |
|---|---|
| **Self-host** | **₹0 licence** — you pay only for a server |
| Cloud Pro | **$9 / user / month** (free trial, no credit card) |
| Cloud Organization | $39 / user / month (SSO, custom roles, more AI) |
| Enterprise | from $50k / year |

**Competitors (third-party sources; confirm before quoting on screen):**
- Zoho CRM India: about **₹800 (Standard) / ₹1,400 (Professional) per user per month** on yearly billing, + GST.
- HubSpot Sales Hub Professional: about **$90–100 per seat per month** (+ onboarding fee).
- Salesforce Sales Cloud: about **$75–175 per user per month** depending on plan.

**Money hook example:** 10-person sales team on Zoho Professional = ₹1,400 × 10 × 12 = **₹1,68,000 a year + GST**.
Self-hosted Twenty = ₹0 licence + a small server.

## 6. Advantages
1. Free and open source; no per-seat bill when self-hosted.
2. **Your data stays on your server** (privacy, no vendor lock-in).
3. Fully custom: shape it for real estate, coaching, agency, clinic, distribution…
4. Modern, clean UI (Notion-like), easy for non-technical staff.
5. AI + workflows built in; API + webhooks for WhatsApp/website/forms integrations.
6. Huge, active project (60k+ stars, 465+ contributors, daily updates) → not going to die soon.
7. Developer-friendly: apps as code, agent skills for Claude Code/Cursor.

## 7. Disadvantages (say at least one — builds trust)
1. **Self-hosting needs a developer:** Docker, a server with **at least 2 GB RAM**, a domain + HTTPS (reverse proxy).
2. **Not India-specific:** no GST invoicing, no built-in WhatsApp or IndiaMART integration; needs API/workflow setup.
3. Some advanced features (SSO, custom roles, more AI) are on paid Cloud plans / enterprise licence.
4. Moves fast: frequent releases → plan upgrades and **backups** (losing the ENCRYPTION_KEY = losing stored secrets).
5. It is a CRM, not accounting/ERP (no billing, stock, payroll).
6. Free self-host = community support only (Discord), no SLA.

## 8. Who can use it
- Small businesses with leads/customers: **real estate, coaching institutes, travel agencies, clinics, interior designers,
  B2B distributors/dealers, event companies**.
- **Startups and SaaS** sales teams.
- **Digital/marketing agencies and freelancers** (client pipeline).
- **Developers** → build a custom CRM for clients = **Plan B service** (set up + customise + maintain).

## 9. How people use it (examples for the reel)
- Real estate: Lead → Site visit → Negotiation → Booked (Kanban).
- Coaching: Enquiry → Demo class → Admission, with follow-up reminders.
- Agency: Prospect → Proposal sent → Won → Project; emails auto-logged.
- Distributor: Dealers list, orders follow-up, visit calendar.

## 10. Setup steps (simple)
**A. Fastest (no developer):** twenty.com → Start free (trial, no card) → import contacts CSV → make pipeline.
**B. Free self-host (developer):**
1. Take a small VPS (2 GB+ RAM) and install Docker.
2. Run the one-line installer from the docs:
   `bash <(curl -sL https://raw.githubusercontent.com/twentyhq/twenty/main/packages/twenty-docker/scripts/install.sh)`
3. Open `http://your-server:3000`, set `SERVER_URL`, put it behind HTTPS (Nginx/Caddy).
4. Create workspace → import contacts (CSV) → build pipeline → connect Gmail/Outlook → add workflows.
5. Keep backups of the database and the `ENCRYPTION_KEY`.

## 11. Key points for the reel (in order)
1. Hook: CRM bill per user per month (Zoho/HubSpot/Salesforce) → yearly ₹ lakhs.
2. Reveal: Twenty — #1 open-source CRM, 60k+ stars, Salesforce alternative.
3. Show: pipeline Kanban, contact page with emails auto-logged, workflow, AI agent.
4. Custom for any business (real estate / coaching / agency examples).
5. Free self-host OR $9 cloud.
6. Honest note: self-host needs a developer + server; not GST/accounting.
7. Plan B / client angle: "Business owners — setup chahiye? DM BUILD." Developers — sell CRM setup as a service.
8. CTA: comment "CRM" for the link · ⭐ star the repo · follow.

## 12. Hook ideas
- `Zoho/Salesforce ka per-user bill band 💸 Ye open-source CRM free hai — 60,000+ developers ne star kiya!`
- `Har lead, har follow-up, har customer — ek free CRM mein. Salesforce ka open-source alternative 🔥`
- `10 logon ki sales team? CRM pe ₹1.6 lakh saal ka mat jalao — ye free hai.`

## Sources
- GitHub API + README + LICENSE: https://github.com/twentyhq/twenty
- Pricing (official): https://twenty.com/pricing
- Docker self-host guide: https://docs.twenty.com/developers/self-host/capabilities/docker-compose
- User guide: https://docs.twenty.com/user-guide/introduction
- Zoho CRM India pricing (third-party): https://itforsme.in/pricing/zoho-crm-india · https://cloudfysystems.com/blog/zoho-crm-pricing-india-2026
- HubSpot/Salesforce pricing (third-party): https://blog.hubspot.com/sales/hubspot-sales-hub-pricing · https://www.crmswitch.com/crm-cost/crm-cost-list/
