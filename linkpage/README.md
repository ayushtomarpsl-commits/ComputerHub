# Computer Hub — link-in-bio page

One page with all your links. Put its address in your Instagram bio once; after that you only edit this page.

Files: `index.html` (the page), `logo.png`, `favicon.png`, `bg.jpg` (isometric background), `og.jpg` (preview image
shown when the link is shared on WhatsApp / X).

## 1. Add your links

Open `index.html` in VS Code and search for `PASTE_`. Replace each one:

| Search for | Put |
|---|---|
| `PASTE_GST_GUIDE_LINK_HERE` | Link to the GST guide (Google Doc, Notion page, PDF on Drive…) |
| `PASTE_GST_TOOL_LINK_HERE` | Your GST Helper tool address |
| `PASTE_YOUTUBE_LINK_HERE` | Your YouTube channel |
| `PASTE_WHATSAPP_CHANNEL_LINK_HERE` | Your WhatsApp channel invite link |
| `PASTE_EMAIL_HERE` | Your contact email (keep the `mailto:` in front) |

A link that still says `PASTE_` shows as **Coming soon** and cannot be tapped, so the page is safe to publish now.
Instagram is already filled in: `https://www.instagram.com/computer__hub/`.
Episode cards open your Reels tab; paste a single reel's link in its `href` to open that reel directly.

## 2. Put it online for free (Vercel)

PowerShell (Node.js is already installed on this PC):

```
npm install -g vercel
cd "D:\New folder\ppc-master-prompt\linkpage"
vercel --prod
```

The first time it asks you to log in (use GitHub or email) and a few questions — press Enter for the defaults and give
the project a name like `computerhub`. At the end it prints your address, e.g. `https://computerhub.vercel.app`.

After you change links, run `vercel --prod` again from the same folder.

No-install option: open https://app.netlify.com/drop and drag the whole `linkpage` folder onto the page.

## 3. One small fix after it is online

WhatsApp and X need the full address of the preview image. In `index.html` change
`<meta property="og:image" content="og.jpg">` to `content="https://YOUR-ADDRESS/og.jpg"` and deploy again.

## 4. Add it to Instagram

Instagram app → Profile → **Edit profile** → **Links** → **Add external link** → paste your page address →
title `Free guides & tools` → Done.
