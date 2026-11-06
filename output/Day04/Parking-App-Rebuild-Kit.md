# Parking App Rebuild Kit — "BlaBlaCar for Parking"

> One guide that explains how a real parking-sharing app works — architecture, data model, flows, screens —
> plus the **copy-paste prompts** that make Claude build the same kind of app for you.

| | |
|---|---|
| **Idea** | BlaBlaCar shares empty car seats. This app shares **empty parking spaces** — in front of a home, a plot, a driveway or a shop. |
| **Who uses it** | **Drivers** find and request parking near a station, market or office. **Hosts** list their empty space and earn. |
| **Built with** | Expo (React Native + TypeScript) app · Node.js + Express API · SQLite / Turso (libsql) database |
| **Based on** | ParkingFriend — a working app built with Claude Code by Ayush Tomar (@computer__hub) |
| **Kit version** | 1.0 — 06-Nov-2026 |

---

## Contents

1. [What the app does](#1-what-the-app-does)
2. [Architecture](#2-architecture)
3. [Data model](#3-data-model)
4. [The core flows](#4-the-core-flows)
5. [API endpoints](#5-api-endpoints)
6. [Screens and design system](#6-screens-and-design-system)
7. [How to rebuild it with Claude — step by step](#7-how-to-rebuild-it-with-claude--step-by-step)
8. [The MASTER PROMPT (copy-paste this)](#8-the-master-prompt-copy-paste-this)
9. [Follow-up prompts](#9-follow-up-prompts)
10. [Going live — costs and checklist](#10-going-live--costs-and-checklist)
11. [Rules, safety and privacy](#11-rules-safety-and-privacy)

---

## 1. What the app does

In Indian cities, parking near railway stations, markets, hospitals and offices is almost impossible —
people circle for a long time and often get a no-parking challan. At the same time, thousands of homes,
plots and shops have empty space in front of them for most of the day.

The app connects the two sides:

1. **A host lists a space** — pins it on a map, adds the address, landmark and nearest station, the vehicle
   types (car / bike / bicycle), how many vehicles fit, a price per day (or free), and when it is available.
2. **A driver searches** near a place ("near Sector 29 metro") and sees open spaces on a map and in a list,
   with distance, price, rating and photos.
3. **The driver sends a request** for a date and time. The host gets a notification.
4. **The host accepts or declines.** Only after **accept** does the driver see the host's phone number
   (privacy first). The host also gets the driver's number.
5. **They chat inside the app** during the booking. The chat closes and is deleted when the parking is done.
6. **Payment is direct** — the driver pays the owner by UPI or cash. The app never moves money (no payment
   gateway needed to start). The "Wallet" only keeps a tally of savings (driver) and earnings (host).
7. **After the parking, both sides rate each other** — drivers rate hosts and spots, hosts rate drivers.
   Hosts see a driver's rating before accepting.

**Core design rules (learned from the real app):**
- The phone number is revealed **only after the host accepts**.
- Every list screen shows **four states**: loading, error (with retry), empty (with a helpful action), data.
- The app works in a **demo mode** (bundled sample data) with one switch, so you can build and test the UI
  before any server exists.
- No payment language anywhere — the app never touches money.

---

## 2. Architecture

```text
 ┌────────────────────────────── Phone app (Expo · React Native · TypeScript) ──────────────────────────────┐
 │  Screens (React Navigation)  →  services/*Service.ts  →  config/apiConfig.ts  ← THE ONE SWITCH           │
 │                                                          ├─ API_URL = ""     → DEMO: bundled JSON + AsyncStorage
 │                                                          └─ API_URL = https… → REAL: REST API below      │
 └───────────────────────────────────────────────────────────────┬───────────────────────────────────────────┘
                                                                 │ HTTPS + JSON, JWT "Bearer" token
 ┌────────────────────────────── REST API (Node.js · Express 4) ─▼───────────────────────────────────────────┐
 │  /api/auth  /api/spots  /api/host  /api/bookings  /api/messages  /api/ratings  /api/wallet               │
 │  /api/telemetry   /admin (founder dashboard, ADMIN_KEY)   /health                                         │
 │  db.js = the ONLY file that talks to storage (all functions async)                                       │
 └───────────────┬──────────────────────────────────────────────────────────────┬────────────────────────────┘
                 │                                                              │
   libsql client │  file:data/app.db  (local dev)                               │  push: Expo Push → FCM → phone
                 │  libsql://…turso.io (production, free cloud SQLite)           │  SMS OTP: 2Factor (India, DLT)
                 ▼                                                              ▼
           SQLite / Turso                                           External services (all have free tiers)

 Maps on the phone: Leaflet in a WebView with OpenStreetMap (or Mapbox) tiles · Place search: Ola Maps (India
 data) with Photon fallback · Directions: Google Maps URL (no API key) · Location: expo-location
```

**Why this shape works for a solo builder:**
- **One switch** (`API_URL`) moves the whole app from demo to real backend — no code changes in screens.
- **One storage file** (`db.js`) — moving from SQLite to Turso to Postgres later touches only this file.
- **Server-side truth** — availability, phone reveal, ratings and earnings are decided by the API, never trusted
  from the phone.
- **Free to run** for a pilot: Render (API), Turso (database), Expo EAS (builds), OSM/Photon (maps/search).

**Tech stack**

| Layer | Choice |
|---|---|
| App | Expo SDK (managed workflow), React Native, TypeScript, React Navigation (native-stack + bottom-tabs) |
| Animation / UI | Reanimated, Gesture Handler, Moti, `@gorhom/bottom-sheet`, `expo-linear-gradient`, `react-native-svg` |
| Fonts / icons | Poppins (headings) + Inter (body) via `@expo-google-fonts`, `@expo/vector-icons` |
| Device | `expo-location`, `expo-image-picker`, `expo-notifications`, `expo-haptics`, AsyncStorage |
| Maps | `react-native-webview` + Leaflet + OpenStreetMap tiles (Mapbox optional), web build uses an iframe |
| API | Node.js, Express 4, `jsonwebtoken` (30-day JWT), `cors`, `@libsql/client` |
| Database | SQLite file locally, Turso (libsql) in production; Postgres-ready repository layer |
| Hosting | Render.com free web service (`render.yaml` blueprint) + Turso free database |
| Builds | Expo EAS (`eas.json`: preview APK, production AAB) |

---

## 3. Data model

| Table | Key fields | Notes |
|---|---|---|
| `users` | id, phone (unique), name, email, avatar, rating, reviewsCount, driverRating, driverRatingCount, verified, responseTime, pushToken, createdAt | Two reputations: as **host** (`rating`) and as **driver** (`driverRating`). Auto-created on first OTP login. |
| `spots` | id, hostId, title, type (`home`/`driveway`/`garage`/`openlot`/`basement`), vehicleTypes, capacity, address, area, city, landmark, nearStation, latitude, longitude, pricePerHour, pricePerDay, isFree, images, amenities, availableFrom/To (time), availableAlways, availableStartDate/EndDate, available, instructions, views | `remainingCount` = capacity − accepted bookings (computed). `availabilityState` = open / upcoming / ended / off (computed by the server). |
| `bookings` | id, userId (driver), spotId, date, time, startTime, endTime, durationHours, vehicleType, vehicleNumber, status, totalAmount, contactUnlocked, otp, cancelReason, cancelledBy, createdAt | Status: `pending → confirmed → active → completed`, or `cancelled`. `hostPhone` is returned **only** when `contactUnlocked`. |
| `host_requests` | id, hostId, spotId, bookingId, spotTitle, requesterId, requesterName, requesterPhone, requesterAvatar, vehicleType, date, time, status, cancelledBy | One per booking. Status: `pending / accepted / declined / cancelled`. |
| `earnings` | id, userId, kind (`saving`/`earning`), title, subtitle, amount, date, bookingId | Tallies only — the app never moves money. |
| `ratings` | id, bookingId, spotId, raterId, rateeId, raterRole, stars (1–5), comment, createdAt | **Unique (bookingId, raterRole)** — one rating per side per booking. |
| `messages` | id, bookingId, senderId, text, createdAt | Index on (bookingId, createdAt). Deleted when the parking ends. |
| `events`, `client_errors`, `devices` | anonymous telemetry + crash reports | Optional; idempotent batches, kill-switch. |

---

## 4. The core flows

### 4.1 Login (phone OTP)
- `request-otp {phone}` → in **dev mode** the code is always `123456`; with an SMS provider configured, a random
  6-digit code is sent by SMS, expires in **5 minutes**, max **5 wrong tries**, **1 per minute and 5 per hour**
  per number (stops SMS bombing that burns your credit).
- `verify-otp {phone, otp, name?}` → with `name` = register (create account), without = login (unknown number
  returns 404 so the app sends them to Register). Returns a 30-day JWT.

### 4.2 Request → accept → reveal phone (the heart of the app)
```text
Driver: POST /api/bookings {spotId, date, time…}
   → booking.status = "pending", contactUnlocked = false, hostPhone = null
   → host_requests row created (with the driver's phone) → push to host "New parking request"

Host:   POST /api/host/requests/:id/respond {accept:true}
   → request "accepted", booking "confirmed", contactUnlocked = true → push to driver "Accepted!"
   → driver now sees hostPhone + "Call" and "Directions" buttons; host sees requesterPhone
Host:   {accept:false} → request "declined", booking "cancelled" (phone never revealed)

Either side may cancel later (reason saved, cancelledBy = driver | host).
Multi-statement writes run as ONE atomic transaction (booking + request, or respond + earning).
```

### 4.3 Availability
- A spot is bookable only if `available` is on **and** today is inside its date window (or `availableAlways`).
- The server computes `availabilityState` so the app can say *why* it is closed ("opens on 12 Nov",
  "listing ended", "switched off") without trusting the phone's clock.
- `remainingCount` stops over-booking when capacity is full.

### 4.4 Chat
- Exists only between the two people of one booking (403 for anyone else).
- Open from the moment of the request until the parking completes or the request dies — then closed and
  messages deleted. Max 500 characters per message. Each message triggers a push.

### 4.5 Ratings (two-sided, like ride-share)
- After a booking is accepted **and** its date has passed, it counts as completed; both sides get a
  "rate your …" prompt (`GET /api/ratings/pending`).
- Driver → host: updates the host's rating and the spot's rating (public).
- Host → driver: updates the driver's rating (shown to hosts on future requests).
- 1–5 stars, optional comment, one rating per side per booking (database unique index).

### 4.6 Wallet (tally, not payments)
- Driver: "saved" amounts; host: "earned" amounts per completed parking day; last 3 months + lifetime.

### 4.7 Maps, search and directions
- Search box → **Ola Maps** places (India: sectors, chowks, societies) with **Photon** fallback.
- Results filtered by distance (haversine) and shown as pins + cards; "350 m away" formatting.
- "Directions" opens Google Maps with the spot's coordinates (`google.com/maps/dir/?api=1&destination=lat,lng`).

### 4.8 Push notifications
- The server sends to Expo Push → FCM; fire-and-forget, never slows the API. Until FCM credentials exist,
  the app falls back to polling — nothing breaks.

---

## 5. API endpoints

| Method | Path | Auth | What it does |
|---|---|---|---|
| GET | `/health` | – | `{ok:true, db}` |
| POST | `/api/auth/request-otp` | – | `{phone}` → sends OTP (dev: `123456`) |
| POST | `/api/auth/verify-otp` | – | `{phone, otp, name?, email?}` → `{token, user}` |
| GET / PATCH | `/api/me` | ✓ | current user / update name, email, avatar |
| GET | `/api/spots` | – | search: `query`, `vehicleType`, `freeOnly`, `maxPrice`, `sort=recommended\|price_low\|price_high\|rating` |
| GET | `/api/spots/popular` | – | top 6 by rating |
| GET | `/api/spots/:id` | – | one spot (adds a view) |
| GET / POST | `/api/host/listings` | ✓ | your spots / create a listing (with latitude, longitude) |
| GET | `/api/host/requests` | ✓ | requests for your spots (with driver phone + rating) |
| POST | `/api/host/requests/:id/respond` | ✓ | `{accept}` → accept/decline |
| GET / POST | `/api/bookings` | ✓ | your bookings / request a spot |
| POST | `/api/bookings/:id/cancel` | ✓ | `{reason?}` |
| GET / POST | `/api/messages/:bookingId` | ✓ | chat thread / send `{text}` |
| GET | `/api/ratings/pending` | ✓ | what you still need to rate |
| POST | `/api/ratings` | ✓ | `{bookingId, stars, comment?}` |
| GET | `/api/wallet/summary`, `/api/wallet/entries` | ✓ | savings + earnings tallies |
| POST | `/api/telemetry/events`, `/api/telemetry/errors` | optional | analytics + crash reports |
| GET | `/admin` | ADMIN_KEY | founder dashboard (disabled unless `ADMIN_KEY` ≥ 8 chars is set) |

All errors return a status code with `{"error": "message in plain English"}`.

---

## 6. Screens and design system

**Navigation**
```text
Splash → Onboarding → Welcome → Login / Register → OTP
Main tabs: Home (driver search) · Bookings · POST (centre button: host hub) · Wallet · Profile
Pushed: Explore (map search) · SearchResults · SpotDetail · BookingDetail · Chat · ListSpace (map-first) ·
        HostRequests · Favorites · Notifications · Settings · EditProfile · HelpSupport · About ·
        TermsPrivacy · Feedback · Reports
```

**Design tokens (light theme; a dark theme mirrors them)**

| Token | Value | Use |
|---|---|---|
| primary | `#0FB57E` emerald | actions, active states |
| secondary | `#6C5CE7` violet | highlights |
| accent / star | `#FFB020` | ratings, badges |
| bg / surface | `#F6F8FA` / `#FFFFFF` | screen / cards |
| text levels | `#0B1B2B` · `#54677A` · `#94A3B8` | three levels only |
| fonts | Poppins (headings), Inter (body) | |
| spacing | screen edge 20 px, touch targets ≥ 44 px | |

**UI rules**
- Every screen reads colours/spacing/fonts from `useTheme()` — never hard-coded.
- Shared components: Screen, Header, Card, Button, Input, Chip, Avatar, Toast, SpotCard, Skeleton, EmptyState,
  ErrorState, LiveMap (read-only) and MapPicker (pin your space), bottom sheets for rating/cancel/calendar.
- Every data screen: loading → error (retry) → empty (helpful action) → data, via one `useAsync` hook.
- Currency always ₹ in en-IN format; friendly empty states ("Be the first to host here").

---

## 7. How to rebuild it with Claude — step by step

You need: a computer with **Node.js 20+**, a phone with **Expo Go** (or an Android emulator), and
**Claude Code** (desktop app, CLI or IDE extension). Claude.ai chat also works, but Claude Code can create the
files and run them for you.

1. **Make an empty folder**, e.g. `D:\parking-app`.
2. **Open Claude Code in that folder.**
3. **Pick your brand and look.** In the master prompt, change the `BRAND` and `DESIGN BRIEF` blocks
   (name, city, colours). Leave them and Claude uses a fresh, friendly look.
4. **Copy the whole MASTER PROMPT** (section 8) and paste it as one message.
5. **Let Claude work in phases** (app in demo mode → API → connect → maps → chat/ratings/push → deploy files).
   If it stops (long jobs can hit limits), send **Follow-up prompt A**.
6. **Run the app:** `npx expo start` → scan the QR with Expo Go (same Wi-Fi), or press `w` for web.
7. **Run the API:** `cd server` → `npm install` → `npm run seed` → `npm start` → open
   `http://localhost:4000/health`.
8. **Connect them:** set `API_URL` in `src/config/apiConfig.ts` to your PC's LAN address
   (e.g. `http://192.168.1.4:4000`) and log in with OTP `123456`.
9. **Test the full loop with two phones** (or phone + web): host lists a space → driver requests →
   host accepts → driver sees the phone number → chat → mark complete → both rate.
10. **Go live** with **Follow-up prompt E** and section 10.

> Tip: if your plan has smaller limits, use **Follow-up prompt F** (one phase at a time).

---

## 8. The MASTER PROMPT (copy-paste this)

Copy everything inside the box.

```text
You are building a two-sided PARKING-SHARING mobile app for India — "BlaBlaCar for parking".
Hosts list the empty parking space in front of their home, plot, driveway or shop. Drivers find
and request a space near a railway/metro station, market, hospital or office. The app never moves
money: the driver pays the host directly (UPI or cash).

BRAND (replace if you want):
  App name: ParkingFriend · Tagline: "Your parking friend" · Launch city: Gurugram, India
DESIGN BRIEF (replace if you want):
  Warm, trustworthy, premium mobility feel. Emerald primary #0FB57E, violet secondary #6C5CE7,
  amber accent #FFB020, light background #F6F8FA, white cards, rounded corners, soft shadows.
  Poppins for headings, Inter for body. Full dark theme. Friendly illustrations for empty states.

=====================================================================
0. WORKING RULES
=====================================================================
- Build in phases, in this order, and run/verify at the end of each phase:
  Phase 1  App UI on DEMO data (no server): theme, components, navigation, all screens
  Phase 2  REST API + database (server/ folder) with tests/smoke script
  Phase 3  Connect app to API through ONE switch (src/config/apiConfig.ts)
  Phase 4  Maps, place search, directions, availability windows
  Phase 5  Chat, two-sided ratings, push notifications, wallet tallies
  Phase 6  Production hardening + deploy files (render.yaml, eas.json, docs)
- Create CLAUDE.md (short rules + pointer) and docs/PROJECT-CONTEXT.md (what we build,
  decisions, status, next steps, change log newest first) at the start; update after each phase.
- Simple, clear English in all UI text. Commands for Windows users in PowerShell 5.1 syntax.
- Never put secrets or API keys in code that ships; read them from env/config files that are
  git-ignored. Never commit databases, .env files, keystores or the Android SDK.
- TypeScript in the app, plain JavaScript (CommonJS) in the server. Small focused files.

=====================================================================
1. APP — TECH AND STRUCTURE (Expo managed workflow)
=====================================================================
Expo SDK (latest stable) + TypeScript, React Navigation (native-stack + bottom-tabs), Reanimated,
Gesture Handler, Moti, @gorhom/bottom-sheet, expo-linear-gradient, react-native-svg,
@expo-google-fonts (Poppins, Inter), @expo/vector-icons, AsyncStorage, expo-location,
expo-image-picker, expo-notifications, expo-haptics, react-native-webview (maps).
Import alias "@/..." -> src/ (babel-plugin-module-resolver + tsconfig paths).

src/
  theme/       tokens (colors light+dark, spacing, radius, typography, shadows, gradients) +
               ThemeProvider/useTheme. Screens NEVER hard-code colours, spacing or fonts.
  components/ui/  Screen, Header, SectionHeader, Card, Button(primary|outline|ghost|gradient|danger,
               sm|md|lg), Input, OtpInput, Chip, Avatar, Badge, Toast, SpotCard, Skeleton,
               EmptyState, ErrorState, ErrorBoundary, LiveMap (read-only), MapPicker (pin a spot),
               bottom sheets: RatingSheet, CancelReasonSheet, CalendarModal, ConfirmDialog
  components/illustrations/  small SVG illustrations for empty/success states
  models/types.ts   User, Host, ParkingSpot, Booking, HostRequest, ChatMessage, ChatThread,
               PendingRating, SpotReview, EarningEntry, WalletSummary, NotificationItem
  data/        demo JSON (spots, bookings, users, faqs, onboarding…)
  services/    one service per domain (auth, spot, booking, host, chat, rating, wallet,
               notification, places, push). Each checks isApiEnabled(): demo path = bundled JSON +
               AsyncStorage with simulated latency; API path = fetch with JWT.
  config/apiConfig.ts   export const API_URL = ""  ("" = demo mode). The ONLY switch.
  hooks/       useAsync (loading/error/empty/data), useDebounce, useFavorites, useUserLocation,
               useLiveRefresh (poll fallback), usePendingRequestCount
  context/     AuthContext (token + user in AsyncStorage)
  navigation/  RootNavigator, MainTabs, route types
  screens/     one folder per screen (see section 3)
Every Pressable has accessibilityRole + accessibilityLabel; touch targets >= 44 px;
long text gets numberOfLines; ₹ amounts via formatCurrency (en-IN).

=====================================================================
2. DATA MODEL (server tables; app types mirror them exactly)
=====================================================================
users(id, phone UNIQUE, name, email, avatar, rating REAL default 5, reviewsCount,
      driverRating, driverRatingCount, verified, responseTime, pushToken, createdAt)
spots(id, hostId, title, type[home|driveway|garage|openlot|basement], vehicleTypes JSON
      [car|bike|bicycle], capacity (1-50), address, area, city, landmark, nearStation,
      distanceMeters, latitude, longitude, pricePerHour, pricePerDay, isFree, images JSON,
      amenities JSON, availableFrom, availableTo (HH:MM), availableAlways, availableStartDate,
      availableEndDate (YYYY-MM-DD), available (on/off), instructions, views, createdAt)
      computed in responses: remainingCount = capacity - accepted bookings that day;
      availabilityState = open|upcoming|ended|off (server timezone); host object embedded.
bookings(id, userId, spotId, date, time, startTime, endTime, durationHours, vehicleType,
      vehicleNumber, status[pending|confirmed|active|completed|cancelled], totalAmount,
      contactUnlocked, otp, cancelReason, hostCancelReason, cancelledBy[driver|host], createdAt)
host_requests(id, hostId, spotId, bookingId, spotTitle, requesterId, requesterName,
      requesterPhone, requesterAvatar, vehicleType, date, time,
      status[pending|accepted|declined|cancelled], cancelledBy)
earnings(id, userId, kind[saving|earning], title, subtitle, amount, date, bookingId)
ratings(id, bookingId, spotId, raterId, rateeId, raterRole[driver|host], stars 1-5, comment,
      createdAt)  + UNIQUE(bookingId, raterRole)
messages(id, bookingId, senderId, text, createdAt) + INDEX(bookingId, createdAt)
events / client_errors / devices for optional first-party telemetry.
Use ALTER TABLE ... ADD COLUMN migrations for columns added later (never drop data).

=====================================================================
3. SCREENS AND NAVIGATION
=====================================================================
Splash -> Onboarding (3 slides) -> Welcome -> Login / Register -> OtpVerification
Main bottom tabs: Home (driver search, recent activity, popular spots) · Bookings ·
  POST (raised centre button = host hub: list a space, incoming requests with accept/decline,
  earnings strip, your spaces) · Wallet (savings + earnings tally, NO payments) · Profile
Pushed: Explore (full-screen map search with pins + bottom sheet list), SearchResults (filters:
  vehicle type, free only, max price, sort), SpotDetail (photos, host card with rating, map,
  amenities, instructions, availability reason, "Request parking" CTA), BookingDetail (status
  timeline; after accept: host phone with Call + Directions; Chat; Cancel with reason),
  Chat, ListSpace (map-first: pin on MapPicker, then details, vehicle types, capacity, price/free,
  time window, always-available or date range), HostRequests, Favorites, Notifications,
  Settings (dark mode), EditProfile (photo via image picker), HelpSupport (FAQ), About,
  TermsPrivacy, Feedback, Reports.
Every data screen renders 4 states: skeleton loading, ErrorState with retry, EmptyState with a
helpful action, data.

=====================================================================
4. CORE BUSINESS RULES (the server enforces them; the app mirrors them in demo mode)
=====================================================================
A. Auth: phone OTP. request-otp {phone}; verify-otp {phone, otp, name?}. With name = register,
   without = login (unknown number -> 404 "please register"). 30-day JWT (Bearer).
   Dev mode: OTP is always 123456 when no SMS provider is configured.
   Real mode (env SMS_PROVIDER + SMS_API_KEY, e.g. 2Factor for India with DLT template):
   random crypto 6-digit code, 5-minute expiry, max 5 wrong attempts, 1 send per minute and
   5 per hour per number. Never return the real code in the response.
B. Request -> accept -> reveal phone:
   - Driver POST /api/bookings -> booking "pending", contactUnlocked=false, hostPhone=null,
     plus a pending host_request carrying the driver's phone. Both rows in ONE transaction.
   - Host accepts -> request "accepted", booking "confirmed", contactUnlocked=true (driver now
     gets hostPhone; host has requesterPhone). Host declines -> "declined" + booking "cancelled".
   - Either side can cancel later with a reason; record cancelledBy.
   - hostPhone is ALWAYS null in responses until contactUnlocked. Never leak phones.
C. Availability: bookable only if available=true AND today is inside the date window (or
   availableAlways). Server computes availabilityState so the app can explain why it is closed.
   Re-check on booking. Respect capacity via remainingCount (no over-booking).
D. Chat: only the booking's driver and host (403 otherwise). Open from request until the parking
   completes or the request is declined/cancelled; then closed and messages deleted. Max 500
   chars. Push the other side on each message.
E. Ratings: a booking is "completed" when it was accepted and its date has passed. Each side
   rates the other once (1-5 stars + optional comment). Driver->host updates host + spot rating;
   host->driver updates driverRating, shown to hosts on future requests. GET /api/ratings/pending
   powers a "rate your last parking" prompt.
F. Wallet: tallies only — driver "saving", host "earning" per completed parking day; summary for
   last 3 months + lifetime. No payment gateway, no payment wording anywhere in the UI.
G. Push: server -> Expo Push API -> FCM, fire-and-forget (never slow or fail the API call).
   Save the user's Expo push token via PATCH /api/me. Keep a polling fallback in the app.

=====================================================================
5. API (Node.js + Express 4, CommonJS) — server/ folder
=====================================================================
Files: src/index.js (express, cors, json 1mb limit, request log, routes, 404, central error
handler that never crashes), src/db.js (the ONLY storage layer, all async, @libsql/client:
file:data/app.db locally, libsql://... Turso in production via TURSO_DATABASE_URL +
TURSO_AUTH_TOKEN), src/auth.js (signToken, requireAuth), src/otpStore.js, src/sms.js,
src/push.js, src/seed.js (schema only, idempotent), routes/: auth, spots, host, bookings,
messages, ratings, wallet, telemetry, admin.
Endpoints:
  GET  /health -> {ok:true, db}
  POST /api/auth/request-otp, POST /api/auth/verify-otp, GET/PATCH /api/me
  GET  /api/spots?query&vehicleType&freeOnly&maxPrice&sort(recommended|price_low|price_high|rating)
  GET  /api/spots/popular (top 6 by rating), GET /api/spots/:id (increments views)
  GET/POST /api/host/listings, GET /api/host/requests, POST /api/host/requests/:id/respond
  GET/POST /api/bookings, POST /api/bookings/:id/cancel
  GET/POST /api/messages/:bookingId
  GET /api/ratings/pending, POST /api/ratings
  GET /api/wallet/summary, GET /api/wallet/entries
  POST /api/telemetry/events|errors (optional auth, idempotent ids, always 2xx, 410 kill-switch)
  GET /admin founder dashboard: enabled ONLY if env ADMIN_KEY (>= 8 chars) is set; timing-safe key
  check; HttpOnly signed cookie session; login rate-limited per IP.
Validate every input (types, lengths, enums, dates YYYY-MM-DD, times HH:MM, capacity 1-50,
stars 1-5) and return {"error": "plain English"} with the right status code.
app.set("trust proxy", 1) behind Render. Rate-limit OTP and admin login.
Write a smoke-test script (curl or node) that runs the full loop: host lists -> driver requests
-> host accepts -> driver sees phone -> chat -> complete -> both rate.

=====================================================================
6. MAPS, SEARCH, LOCATION, DIRECTIONS
=====================================================================
- Maps: Leaflet inside react-native-webview (iframe on web) with free OpenStreetMap tiles;
  optional Mapbox public token in src/config/mapConfig.ts. LiveMap shows pins; MapPicker lets a
  host drag a pin and returns latitude/longitude.
- Place search: placesService.search/reverse/nearby. Use Ola Maps Places (India data: sectors,
  chowks, societies) when OLA_MAPS_API_KEY is set, and fall back to Photon (photon.komoot.io,
  free, no key) on any error. Keys come from git-ignored config, never hard-coded in the repo.
- "Near me": expo-location with a clear permission message; haversine distance; "350 m away".
- Directions: open https://www.google.com/maps/dir/?api=1&destination=LAT,LNG&travelmode=driving
  (no API key) via Linking.

=====================================================================
7. DEPLOY FILES AND DOCS
=====================================================================
- render.yaml: free web service, rootDir server, build "npm install", start "npm start",
  healthCheckPath /health, JWT_SECRET generateValue, TURSO_DATABASE_URL and TURSO_AUTH_TOKEN
  (sync:false), optional SMS_PROVIDER, SMS_API_KEY, SMS_TEMPLATE, ADMIN_KEY.
- eas.json: "preview" (APK for sharing) and "production" (AAB for Play Store).
- app.json: name, slug, scheme, bundle id/package, icons, splash (primary colour), location +
  photos + notifications permissions with friendly explanations.
- Windows helpers: run-on-web.bat, run-on-phone.bat (Expo Go + tunnel), build-apk.bat.
- README.md, DEPLOYMENT.md (local -> Render + Turso -> EAS build -> Play Store),
  LAUNCH-CHECKLIST.md (what needs a paid account), UI-GUIDE.md (design rules).
- .gitignore: node_modules, .expo, dist, android/, ios/, android-sdk/, *.jks, *.keystore, .env*,
  server/data/, logs.

=====================================================================
8. DONE MEANS
=====================================================================
- Demo mode: the whole app works offline with sample data on phone and web.
- API mode: two accounts can complete the full loop (list -> request -> accept -> phone revealed
  -> chat -> complete -> rate) with the smoke test passing.
- No phone number leaks before accept; no secrets in the repo; every screen has 4 data states.
- Finish with a short report: what was built, test output, how to run, what you could not verify.
Start now with Phase 1.
```

---

## 9. Follow-up prompts

**A — Continue after a stop**
```text
Continue from where you stopped. First read CLAUDE.md and docs/PROJECT-CONTEXT.md, run the app
and the API smoke test, then continue with the next unfinished phase.
```

**B — Change only the look**
```text
Keep all logic, services, API calls and navigation exactly as they are. Redesign only the theme
tokens and component styles to this style: <describe your style>. Keep 4 data states on every
screen and dark mode working. Show me screenshots of Home, Explore, SpotDetail and the POST tab.
```

**C — Turn on real SMS OTP (India)**
```text
Wire real SMS OTP into server/src/sms.js using 2Factor (DLT-approved template). Keep the dev OTP
123456 when SMS env vars are missing. Random 6-digit codes, 5-minute expiry, 5 wrong tries max,
1 send/minute and 5/hour per number. Never return the code in the response. Add a test.
```

**D — Move the database to Turso (free, survives redeploys)**
```text
Make server/src/db.js work with Turso via @libsql/client: TURSO_DATABASE_URL + TURSO_AUTH_TOKEN,
local file mode when unset. Keep every repository function async and multi-step writes in one
batch transaction. Give me the exact Turso CLI steps to create the database and token.
```

**E — Put it live (Render + Turso + APK)**
```text
Prepare everything to go live for free: check .gitignore blocks secrets/databases, show git status,
then give me exact PowerShell steps for: GitHub repo, Turso database, Render Blueprint deploy,
setting API_URL in the app, and building a shareable APK with EAS (preview profile).
Do not push anything without my OK.
```

**F — Phased mode (for smaller plans)**
```text
Use the master prompt above as the full spec. Only do Phase <N> now. Verify it, update
docs/PROJECT-CONTEXT.md, and stop.
```

**G — Add online payments later (optional)**
```text
Add optional in-app UPI payment with Razorpay test keys only, behind a feature flag that is OFF by
default. Keep the direct UPI/cash flow as the default. Add the payment status to bookings, a
webhook route with signature verification, and update the wallet wording only when the flag is on.
```

**H — Launch a new city**
```text
Add city support: a city picker on Home, default map centre and search bias per city, and
"popular stations" chips per city. Start with Gurugram, Delhi, Noida, Bengaluru, Pune.
```

---

## 10. Going live — costs and checklist

| Gate | Cost | Needed for |
|---|---|---|
| Render (API) + Turso (database) | Free tiers | App works outside your Wi-Fi |
| Expo EAS build | Free tier | Shareable APK / Play Store bundle |
| Google Play Console | $25 one-time | Android store release |
| SMS provider (India, DLT) | ≈ ₹0.15–0.25 per SMS | Real OTP login |
| Apple Developer | $99 per year | iPhone App Store (optional at launch) |

**Before real users**
1. Host the API (Render) and database (Turso); set a strong `JWT_SECRET` and an `ADMIN_KEY`.
2. Turn on real SMS OTP (until then: internal testing only — anyone can log in with 123456).
3. Write a privacy policy page (required: location + phone number) and fill Play Store "Data safety".
4. Seed real supply: list 5–10 real spaces near your target stations so first users don't see an empty app.
5. Test the full loop with two real phones.
6. Free-tier note: Render sleeps after ~15 minutes idle (first request ~30–60 s).

---

## 11. Rules, safety and privacy

- **Local rules:** renting out private space for parking may need permission from your society/RWA or local
  authority in some cities. Check before you launch, and tell hosts to check too.
- **Privacy:** phone numbers only after accept; chats deleted after the parking; ask location permission with
  a clear reason; never sell data; declare everything honestly in the store forms.
- **Trust:** two-sided ratings, host sees the driver's rating before accepting, reasons for cancellations.
- **Money:** with direct UPI/cash, write clear terms that the platform is not part of the payment.
- **Keys:** keep API keys (maps, SMS, Firebase) out of public repos; restrict browser/app keys in each
  provider's dashboard.

> This kit explains an app idea and how to build it. You are responsible for your launch, your users and
> local rules. When in doubt, ask a legal or tax advisor.

---

Made for the **Plan B for Software Engineers** series by **Computer Hub** — follow **@computer__hub** on Instagram.
