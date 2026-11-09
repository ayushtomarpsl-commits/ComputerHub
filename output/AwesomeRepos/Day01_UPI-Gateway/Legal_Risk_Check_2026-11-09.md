# UPI Gateway (mynkdev-21/upi-gateway) — legal / RBI risk check for commercial use

Checked: 2026-11-09, repo at commit `3cdedc8` ("fix: restore installer hosting compatibility").
This is a technical + regulatory risk reading, **not legal advice**. Before taking real customer payments at scale,
confirm with a CA / lawyer and with your bank.

## Short answer
**Using it for your OWN shop/website, with money going into YOUR OWN business (current / merchant) UPI account,
is low risk from an RBI point of view.** You are the merchant collecting your own sales; the software holds no money,
so it is not a "Payment Aggregator". The real risks are practical: bank-account type, the unofficial Paytm endpoint,
fake-payment fraud, and normal business compliance (GST, data protection, refund policy).

**Offering it to OTHER businesses (multi-merchant, paid plans) is a different story** — that starts to look like
running a payment gateway / payment service. Take legal advice before doing that.

## What the code actually does (verified)
- Money goes customer → merchant's own UPI ID directly (UPI deep link / dynamic QR). README: "The platform is not
  designed to hold or pool merchant funds." No escrow/nodal account, no settlement code.
- Verification options (`app/Services/Verifiers/`):
  - `PaytmBusinessVerifier` — polls Paytm's **unofficial** legacy endpoint `securegw.paytm.in/merchant-status/getTxnStatus`
    with your MID + order id; checks order id and exact amount. No signature from Paytm. README marks it
    "Unofficial / Experimental"; can be turned off with `GATEWAY_ENABLE_PAYTM_BUSINESS=false`.
  - `PaytmPgVerifier`, `PhonePePgVerifier` — **official** gateway APIs (those providers are RBI-authorised; they
    charge their own fees).
  - `ManualVerifier` — customer submits UTR; merchant approves after checking the bank/UPI app.
- Stores customer name, email, mobile on orders (`app/Models/Order.php`).
- Public merchant sign-up is **off by default** (`ALLOW_REGISTRATION=false`). Admin can create merchants.
- License: **MIT** — commercial use of the code is allowed.
- The default landing page (`resources/views/welcome.blade.php`) markets the software like a paid service:
  Pricing ₹999 / ₹2,999 per month and a table saying "RBI registration needed: No".

## Rules that matter
1. **RBI — Payment Aggregator Directions, 15 Sep 2025.** A Payment Aggregator receives customers' money for merchants
   and settles it to them (funds must sit in escrow) → needs RBI authorisation. A **Payment Gateway** = technology that
   routes/processes payments **without handling funds**. This software, used for your own sales, handles no funds →
   not a PA. Risk rises if you run it for other merchants (contracting, KYC/due-diligence, FIU and RBI scrutiny).
2. **Bank / NPCI account rules.** UPI separates P2P (person-to-person) and P2M (person-to-merchant). The repo's own docs:
   personal savings-account UPI used for commercial sales "may violate bank terms of service, trigger automated
   velocity blocks, or result in account restrictions". → Use a **current account / merchant VPA** (Paytm for Business,
   PhonePe Business, BharatPe, bank merchant QR).
3. **Account rotation** (spreading orders across many UPI IDs) — fine for load balancing your own registered business
   accounts; **using it to stay under bank limits or split turnover is exactly what the repo forbids** and can look like
   evasion to the bank / tax department.
4. **Paytm terms.** The Paytm for Business verifier uses an undocumented endpoint. That is a contract / terms risk with
   Paytm (MID could be restricted; endpoint can stop any day), not an RBI issue.
5. **Data protection — DPDP Act 2023 (+ Rules, phased in).** You store name / email / phone → you are a data fiduciary:
   privacy notice, purpose limit, reasonable security, breach handling.
6. **Consumer Protection (E-Commerce) Rules 2020** for an online shop: seller details, refund / return / cancellation
   policy, grievance contact on the website.
7. **Tax.** UPI receipts are business income; GST invoices as applicable. Normal, same as any gateway.

## Risk table (own website / own shop)
| Risk | Level | Why | Fix |
|---|---|---|---|
| RBI action for "running a payment gateway" | Low | No funds held, own sales only | Don't onboard other merchants; don't advertise it as a gateway service |
| Bank blocks / freezes the receiving account | **Medium–High** if savings account | Commercial receipts on personal UPI | Use current account / merchant VPA |
| Paytm unofficial endpoint stops or MID restricted | Medium | Undocumented API, no SLA | Prefer official Paytm PG / PhonePe PG, or set `GATEWAY_ENABLE_PAYTM_BUSINESS=false` + manual check |
| Fake payment (fake UTR / screenshot) | **Medium–High** with manual mode | UTR typed by customer | Never ship on UTR alone; confirm credit in bank app; auto-verify for high volume |
| Chargebacks / disputes / refunds | Medium | No gateway dispute flow; refunds are manual UPI | Clear refund policy; keep records |
| Data breach of customer details | Medium | Self-hosted = your security | HTTPS, updates, backups, strong admin password, DPDP notice |
| Misleading claims on the landing page | Medium | ₹999/₹2,999 plans, "RBI registration: No" | Replace/hide the marketing page if you only use it as your own checkout |
| Software bugs (release candidate) | Medium | README: v1.1.0 RC, test before live | Test with ₹1 payments; start small |

## Before using it commercially (checklist)
1. Receive into a **current account / merchant UPI ID** in your business name (KYC done).
2. Prefer **official verification** (Paytm PG / PhonePe PG) for volume; if you keep Paytm for Business, accept the risk
   or switch it off and verify manually.
3. **Never release goods on UTR alone** — check the credit in your bank app.
4. Edit or hide the default **welcome/pricing page**; put your shop's own terms, privacy policy, refund policy,
   contact/grievance details on your site.
5. Keep **one UPI account** (or only your own registered business accounts); don't use rotation to dodge limits.
6. HTTPS on, `APP_DEBUG=false`, keep the app updated, back up the database, restrict admin access.
7. Do test payments with GPay / PhonePe / Paytm / BHIM before going live; keep transaction records for GST/IT.
8. If you ever plan to **sell this as a service to other merchants**, get legal advice first (RBI PA/PG Directions 2025).

## Sources
- RBI (Regulation of Payment Aggregators) Directions, 2025 — https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12896 ·
  press release https://website.rbi.org.in/web/rbi/-/press-releases/rbi-issues-the-reserve-bank-of-india-regulation-of-payment-aggregators-directions-2025 ·
  analysis https://indiacorplaw.in/2025/10/09/decoding-rbis-overhaul-of-the-payment-aggregator-directions/ ·
  https://www.khaitanco.com/sites/default/files/2025-10/ERGO%20-%20PA%20Master%20Directions%20-%203%20Oct%202025.pdf
- UPI P2P vs P2M basics — https://www.idfcfirst.bank.in/finfirst-blogs/savings-account/latest-upi-payment-rules-charges-limits-explained
- Repo files read: README.md (Integration notes, compliance advisory), docs/INSTALLATION.md ("Payment accounts and
  compliance"), app/Services/Verifiers/*.php, app/Models/Order.php, config/auth.php, routes/web.php,
  resources/views/welcome.blade.php.
