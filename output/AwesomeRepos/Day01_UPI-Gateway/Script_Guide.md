# Awesome Repos · Day 1 — Script guide (UPI Gateway)

**Series:** "Awesome Repos" — every day one useful open-source GitHub repo for developers in the AI era.
**Header pill in video:** `COMPUTER HUB · AWESOME REPOS · DAY 1`
**Length target:** 60–75 seconds (≈ 160–190 spoken words). Same voice (Viraj), same light UI as Plan B.
**Goal:** people (1) save money by using the repo, (2) star the repo + follow Mayank, (3) follow @computer__hub.

---

## 1. Story shape (use this for every Awesome Repos episode)

| Time | Beat | What to say | What we show |
|---|---|---|---|
| 0–4 s | **Hook (pain + number)** | Razorpay takes ~2.36% of every payment | Big "₹23,600 / month" counter going up |
| 4–12 s | **Problem** | Small business / indie dev loses money every month | Razorpay-style fee slip, money flying out |
| 12–20 s | **Reveal + credit** | "Awesome Repos Day 1… by Mayank Singh" | GitHub page `mynkdev-21/upi-gateway`, logo |
| 20–45 s | **How it works (3–4 steps)** | QR → pay → direct to bank → auto verify → webhook | `payment_page`, `verifying_card`, `success_card`, `dashboard_stats` |
| 45–55 s | **Honest note** | UPI only, self-host, own business | `money_stays_yours`, small "⚠️" chip |
| 55–70 s | **CTA** | Comment REPO / star / follow | Logo outro + Follow click (same as Plan B) |

Rule: **one idea per caption line**, numbers on screen, and credit the developer **twice** (reveal + end).

---

## 2. Hook options (pick one — first 3 seconds decide everything)

1. **Money hook:** "Razorpay har payment pe 2% + GST kaat-ta hai. Monthly 10 lakh ki sale? Matlab 23 hazaar rupaye har mahine gaye."
2. **Curiosity hook:** "Ek Indian developer ne Razorpay jaisa UPI payment gateway bana ke… bilkul free mein open source kar diya."
3. **Direct hook:** "Agar aapki website pe payment gateway lagaa hai, toh ye video aapke hazaaron rupaye bacha sakti hai."

My pick: **#1** (number + pain = most stops), then #2's line right after as the reveal.

---

## 3. Ready script (Hinglish, ~70 s) — edit freely, then make the voice

> **[Hook]** Razorpay har payment pe 2% plus GST kaat-ta hai. Agar aapki monthly sale 10 lakh hai… toh 23 hazaar rupaye har mahine sirf fees mein gaye.
>
> **[Reveal]** Lekin ek Indian developer ne iska free solution open source kar diya hai. Awesome Repos, Day 1: **UPI Gateway**, by **Mayank Singh**.
>
> **[How it works]** Ye ek self-hosted UPI payment gateway hai. Aap isse apne server pe host karo, aur apni website se order banao. Customer ko har order ka dynamic QR milta hai — GPay, PhonePe, Paytm, kisi se bhi pay kare. Paisa seedha aapke bank account mein jaata hai — beech mein koi nahi. Gateway khud payment verify karta hai, aur aapki website ko signed webhook bhejta hai: order paid.
>
> **[Extra]** Dashboard, API docs, multiple UPI accounts ka rotation, sab ready hai. Laravel mein bana hai, setup bas kuch commands ka.
>
> **[Honest note]** Bas dhyaan rahe: ye UPI payments ke liye hai, aur apne business ke liye use karo.
>
> **[CTA]** Repo ka link chahiye? Comment karo **"REPO"**, main DM kar dunga. GitHub pe Mayank ko ek star zaroor do — aise developers ko support milna chahiye. Aur aise hi awesome repos ke liye follow karo Computer Hub.

(≈ 175 words. If it runs long, cut the **[Extra]** line first.)

**Pronunciation tips for ElevenLabs:** write "two percent" as "2 percent", "UPI" as "U-P-I", "webhook" as "web-hook",
"Laravel" as "Laa-ra-vel" if it sounds wrong. Keep "Razorpay" as is.

---

## 4. Call-to-action options (use 1 main + 1 support)

| CTA | Why it works |
|---|---|
| **Comment "REPO" → I'll DM the link** | Boosts comments (algorithm) + you can send via ManyChat later |
| **Link in bio → "All resource link" → UPI Gateway** | Works even without DMs (add a card on the link page) |
| **Star the repo on GitHub** | Real help to the developer — the promotion he asked for |
| **Follow for Day 2** | Builds the series audience |
| **Save this reel** | "Website banane se pehle save kar lo" — saves = strong signal |

Credit line for screen + caption: **"Built by Mayank Singh (@mynkdev-21 on GitHub) — go give it a ⭐"**.
If Mayank has an Instagram handle, ask him and tag him as a **collaborator** on the post (doubles reach).

---

## 5. What NOT to say (keeps you and the developer safe)
- Don't say "Razorpay band karo" or "100% replacement" → say "UPI payments ke liye free alternative".
- Don't promise "zero cost" → say "no gateway fee; bas apna server".
- Don't tell people to run it as a gateway for other businesses (RBI rules).

---

## 6. Before you post (checklist)
- [ ] Ask Mayank to add a **LICENSE** file (README says MIT, but GitHub shows no license yet).
- [ ] Add a **"UPI Gateway (Awesome Repos Day 1)"** card on computerhub-links.vercel.app (I can do this).
- [ ] Voice ready → put it in `episodes/repo01/voice.mp3` and tell me → I render the reel with the UI elements.
- [ ] Cover: "FREE Razorpay Alternative? 🤯" + repo logo + "Awesome Repos · Day 1".
- [ ] Pinned comment: "⭐ Repo: github.com/mynkdev-21/upi-gateway — built by Mayank Singh. Comment REPO for the link in DM."
