# MilesWeb AI Builder promo — elements map (made 08-Nov-2026)

Cut by `source/milesweb_elements.py` from the two videos in `../elements or clips demo/`:
- **rec** = Ayush's screen recording of the live MilesWeb dashboard (1918x1014, sharp)
- **tut** = MilesWeb's official tutorial "Build a Website with MilesWeb AI Builder" (1920x1080; softer, but readable)

Not used on purpose: login screen (email/password), KYC popup, the staff account name ("Welcome, …"), and frames
showing other apps (Claude, Google Docs).

**Note:** the demo account has no active hosting plan, so the AI Builder shows "Choose your AI website builder plan"
instead of generating. The OUTPUT (AI chat → generating → PetBloom website → publish) therefore comes from
MilesWeb's own tutorial. If MilesWeb activates a plan/credits on the account, record a café demo and we swap it in.

## Stills (`hd/`)
| File | Shows |
|---|---|
| 01_title_build_with_ai | "Build Your Website with AI" title card |
| 02_how_to_build_options | "How would you like to build your website?" — Build with AI / WordPress / Blank |
| 03_prompt_box_empty_dark | **INPUT** — "Prompt It. Build It. Launch It." with an EMPTY prompt box (for our own typing animation) |
| 04_prompt_box_filled_dark | **INPUT** — same box with the café prompt filled in |
| 05_whats_on_your_mind_empty | **INPUT** — "What's on your mind?" empty prompt (light UI) |
| 06_whats_on_your_mind_typed | **INPUT** — pet-care prompt typed |
| 07_ai_chat_questions | AI asks brand name, city, contact email |
| 08_generating_progress | **GENERATING** — progress bar + "Responsive Design / One-Click Publish / Generating Content" |
| 09_editor_services | **OUTPUT** in editor — services section + chat "website updated successfully" |
| 10_editor_hero | **OUTPUT** in editor — PetBloom hero |
| 11_domain_setup | Domain setup — existing / temporary / add domain |
| 12_published_successfully | "Published successfully · petbloom.herositepro.com · Connected" |
| 13_final_site_hero | **FINAL WEBSITE** hero (full frame) |
| 14_final_site_testimonials | Final website — testimonials section |
| 15_plans_ai_credits | Plans ₹69 / ₹99 / ₹149 + "One-time AI credits included with every plan" |
| 16_template_gallery | Ready template prompts (fashion, hotel, …) |

## Clips (`clips/`, 30 fps, silent)
| File | Length | Use |
|---|---|---|
| c1_prompt_typing | 5 s | real typing in the prompt box |
| c2_ai_chat | 8 s | AI asking questions, user answering |
| c3_generating | 7 s | generating with progress bar |
| c4_result_in_editor | 6 s | generated site appears in the editor |
| c5_publish | 9 s | publish dialog → "Published successfully" |
| c6_final_site_scroll | 7 s | live website |
| c7_dark_prompt_paste | 5 s | live dashboard: empty → filled café prompt |

## Script line → element
| Script line | Element |
|---|---|
| Hook: "2 hafte / ₹50,000 … bas 5 minute" | our own graphics (calendar, ₹ cross, timer) |
| "Awesome Tools Day 2 — MilesWeb AI Builder" | 01_title_build_with_ai + MilesWeb logo pill |
| "Dashboard mein AI Builder kholo" | 02_how_to_build_options ("Build with AI" highlighted) |
| "Apna idea likho…" | **03 empty dark box + our typing animation of the café prompt** (or c7) |
| "AI poori website khud bana raha hai" | 07_ai_chat_questions → 08_generating_progress / c3 |
| "Ye raha final result" | 13_final_site_hero / c6 (+ phone frame for "mobile-friendly") |
| "Theme dark green kar do… section add karo" | 09/10 editor + typed change-prompts (our animation) |
| "Domain, SSL, backups, live kar do" | 11_domain_setup → 12_published_successfully / c5 |
| "Hosting plans mein included, free AI credits, ₹69 se" | 15_plans_ai_credits |
| CTA "comment WEBSITE" | comment box + DM bubble (our graphics) |

---

# UPDATE 10-Nov-2026 — REAL demo on the client account (Chai Adda Café) ✅
Made by `source/milesweb_demo_elements.py` from Ayush's two new recordings:
- **R1** = `Recording 2026-11-10 111730.mp4` (2:54): prompt → AI chat → blueprint → generating → result in editor
- **R2** = `Recording 2026-11-10 111835.mp4` (24 s): final website full-screen scroll → "Your Websites" list

These replace the tutorial (PetBloom) footage — use the tutorial only as backup now.
**Privacy:** the account holder's name (top-right "… K / Owner", and the greeting "What's on your mind, <name>?")
is blurred / removed (greeting now reads "What's on your mind?"), and Ayush's email is blurred everywhere
(chat reply, site "Find Us" box, site footer). Overview contact sheet: `demo_contact_sheet.jpg`.

## Sequence (same order as the approved script) → element
| Script beat | Stills (`hd/`) | Clip (`clips/`) |
|---|---|---|
| "Dashboard mein AI Builder kholo, apna idea likho" (DEMO) | 20_prompt_page_empty, 22b_prompt_box_empty_2x | **c11_prompt_typing_fullscreen** (8.8 s) |
| Prompt typing — close-up | 22_prompt_box_filled_2x, 21_prompt_page_filled | **c10_prompt_typing_box_2x** (8.8 s, 2260x620) |
| Prompt "dictated" (speech-to-text feel) | chat/47_dictation_mic_pill (overlay) | **c12_prompt_dictation_box_2x** (7.8 s, words land in bursts) |
| Prompt sent → AI replies in chat | 23_chat_prompt_sent, 23b_chat_prompt_sent_crop_2x, 24_chat_ai_question | **c13_chat_prompt_to_ai_question** (13.4 s, real) |
| AI makes a plan → Approve | 25_blueprint_full, 25b_blueprint_card_2x, 25c_blueprint_approve_hover_2x | **c14_blueprint_approve** (4.5 s, real click) |
| "AI poori website khud bana raha hai" | 26_generating_25pct(_card_2x), 27_generating_late(_card_2x) | **c15_generating_8x** (9 s = 72 s sped up 8x) |
| "Ye raha final result" (RESULT) | 28_result_reveal_editor, 29_result_editor_updated, 29b_chat_updated_successfully_2x | **c16_result_reveal_editor** (6.7 s, site appears) |
| Final website showcase | 30_site_hero, 31_site_menu, 32_site_menu_full, 33_site_offers, 34_site_gallery, 35_site_testimonials, 36_site_reserve_table, 37_site_map_footer | **c17_final_site_scroll** (12.8 s, R2) · c18_final_site_fullscreen_r1 (8 s) |
| Your websites list (it's saved in the dashboard) | 38_your_websites_dashboard | c19_your_websites_dashboard (1.9 s) |

## Chat-style text (`chat/`, transparent PNG, 2x, MilesWeb colours) — for "chat bubble" pop-ups in the reel
| File | Text (exact wording from the real chat) |
|---|---|
| 40_ai_welcome | "Welcome to Vibe Code Websites. Describe the website you want to create, and I'll handle the analysis, planning, and code generation." |
| 41_user_prompt | the café prompt (blue user bubble) |
| 42_ai_typing_dots | AI "…" typing indicator |
| 43_ai_question_email | "What is your contact email address for customer inquiries?" |
| 44_user_email_EXAMPLE | **example** address `hello@chaiaddacafe.in` (stand-in for the real, private one) |
| 45_ai_plan_ready | "I've analyzed all your requirements and prepared a plan. Review the details below and approve to start building." |
| 46_ai_website_updated | "Your website has been updated successfully! Check the preview to see the latest changes." |
| 47_dictation_mic_pill | "Speaking the prompt…" mic + waveform — **our own overlay**, MilesWeb has no voice input |

## Typing / dictation clips — how they are made
Not fake text: the clip reveals the **real rendered prompt text** from the recording letter by letter (c10/c11) or
word-burst by word-burst (c12), with a blinking caret, a live "n / 1500" counter, and the send button switching
from grey to black — on top of the real empty box. Browser spell-check squiggle removed.

## Still missing vs. the script (need a new recording if we want them)
1. **Customisation** (33–45 s): "theme dark green", "add testimonials", manual text/image edit — not recorded yet.
2. **Mobile view** of the result (script says "desktop scroll + mobile view") — use the editor's phone icon.
3. **Publish → domain → Published successfully** on the client account (the site is still **Draft**).
Until then: tutorial stills 11/12 (domain, published) and 09/10 (editor) can fill these beats.
