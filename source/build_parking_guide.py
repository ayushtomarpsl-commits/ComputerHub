"""Build linkpage/parking-guide.html from output/Day04/Parking-App-Rebuild-Kit.md.

Run:  py -I source/build_parking_guide.py
The Markdown file is the source of truth; edit it, then re-run this script.
Only the small Markdown subset used in the kit is supported.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "output" / "Day04" / "Parking-App-Rebuild-Kit.md"
OUT = ROOT / "linkpage" / "parking-guide.html"
SITE = "https://computerhub-links.vercel.app"


def slug(text):
    t = re.sub(r"[^\w\s-]", "", text.lower())
    return t.replace(" ", "-")


def inline(text):
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>" + html.escape(p[1:-1]) + "</code>")
            continue
        s = html.escape(p, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        out.append(s)
    return "".join(out)


def split_row(line):
    line = line.strip().strip("|")
    cells = re.split(r"(?<!\\)\|", line)
    return [c.strip().replace("\\|", "|") for c in cells]


def render(md):
    lines = md.splitlines()
    i = 0
    title = ""
    hero, sections = [], []
    cur = hero
    code_n = 0
    sec_title = ""

    def para_end(j):
        return (j >= len(lines) or not lines[j].strip()
                or re.match(r"(#{1,3} |```|\||- |\d+\. |> |---$)", lines[j]))

    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# "):
            title = ln[2:].strip()
            i += 1
        elif ln.startswith("## "):
            sec_title = ln[3:].strip()
            cur = []
            sections.append((sec_title, cur))
            i += 1
        elif ln.startswith("### "):
            h = ln[4:].strip()
            cur.append(f'<h3 id="{slug(h)}">{inline(h)}</h3>')
            i += 1
        elif ln.startswith("```"):
            lang = ln[3:].strip()
            j = i + 1
            body = []
            while j < len(lines) and not lines[j].startswith("```"):
                body.append(lines[j])
                j += 1
            code_n += 1
            text = "\n".join(body)
            is_master = sec_title.startswith("8.")
            cid = "master-prompt" if is_master else f"code{code_n}"
            cls = "code master" if is_master else "code"
            if is_master or sec_title.startswith("9."):
                cls += " prose"
            label = "MASTER PROMPT" if is_master else ("PROMPT" if sec_title.startswith("9.") else (lang or "text").upper())
            btn = "Copy all" if is_master else "Copy"
            cur.append(
                f'<div class="{cls}" id="{cid}-box"><div class="code-bar"><span>{label}</span>'
                f'<button class="copy" data-target="{cid}" type="button">{btn}</button></div>'
                f'<pre id="{cid}">{html.escape(text)}</pre></div>')
            i = j + 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            head = split_row(rows[0])
            body = [split_row(r) for r in rows[2:]]
            t = ['<div class="table"><table>']
            if any(head):
                t.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>")
            t.append("<tbody>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            cur.append("".join(t))
        elif re.match(r"(- |\d+\. )", ln):
            ordered = bool(re.match(r"\d+\. ", ln))
            items = []
            while i < len(lines) and re.match(r"(- |\d+\. |   +\S)", lines[i]):
                l2 = lines[i]
                if re.match(r"   +\S", l2) and items:
                    items[-1] += " " + l2.strip()
                else:
                    items.append(re.sub(r"^(- |\d+\. )", "", l2))
                i += 1
            tag = "ol" if ordered else "ul"
            cur.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
        elif ln.startswith("> "):
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i][1:].strip())
                i += 1
            cur.append(f'<blockquote>{inline(" ".join(q))}</blockquote>')
        elif ln.strip() == "---" or not ln.strip():
            i += 1
        else:
            p = [ln.strip()]
            i += 1
            while not para_end(i):
                p.append(lines[i].strip())
                i += 1
            cur.append(f"<p>{inline(' '.join(p))}</p>")
    return title, hero, sections


def build():
    title, hero, sections = render(SRC.read_text(encoding="utf-8"))
    nav = []
    body = []
    for name, parts in sections:
        sid = slug(name)
        if name.lower() == "contents":
            continue
        m = re.match(r"(\d+)\.\s*(.*)", name)
        num, label = (m.group(1), m.group(2)) if m else ("", name)
        short = label.split("(")[0].split("—")[0].strip()
        nav.append(f'<a href="#{sid}"><b>{num}</b>{html.escape(short)}</a>')
        star = " star" if num == "8" else ""
        body.append(
            f'<section class="card reveal{star}" id="{sid}"><h2><span class="num">{num}</span>'
            f'{inline(label)}</h2>{"".join(parts)}</section>')

    page = TEMPLATE
    page = page.replace("{{TITLE}}", html.escape(title))
    page = page.replace("{{HERO}}", "".join(hero))
    page = page.replace("{{NAV}}", "".join(nav))
    page = page.replace("{{BODY}}", "\n".join(body))
    page = page.replace("{{SITE}}", SITE)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT} ({len(page):,} bytes, {len(sections)} sections)")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Parking App Rebuild Kit · Computer Hub</title>
<meta name="description" content="Free guide: architecture, data model, API and a copy-paste MASTER PROMPT that makes Claude build a parking-sharing app (BlaBlaCar for parking). By @computer__hub.">
<meta property="og:title" content="Parking App Rebuild Kit · BlaBlaCar for Parking">
<meta property="og:description" content="Architecture + copy-paste master prompt to build a parking-sharing app with Claude. Free, from @computer__hub.">
<meta property="og:image" content="{{SITE}}/og.jpg">
<meta property="og:url" content="{{SITE}}/parking-guide.html">
<meta property="og:type" content="article">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f7f3ec">
<link rel="icon" type="image/png" href="favicon.png">
<style>
  :root {
    --bg: #f7f3ec; --card: #ffffff; --ink: #141b2d; --ink2: #34405c; --muted: #7a859d;
    --line: #e4e9f2; --blue: #1e6fe0; --cyan: #00aaec; --green: #22b04b; --purple: #a05ce2;
    --yellow: #ffc828; --codebg: #0f1a2e; --codeink: #dce6f7;
    --shadow: 0 10px 30px rgba(24, 42, 88, 0.10), 0 2px 6px rgba(24, 42, 88, 0.06);
    --radius: 22px;
  }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; scroll-padding-top: 76px; }
  body {
    margin: 0; background: var(--bg); color: var(--ink);
    font-family: "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif;
    font-size: 16px; line-height: 1.6; -webkit-font-smoothing: antialiased;
  }
  body::before {
    content: ""; position: fixed; inset: 0; z-index: -1; opacity: .35;
    background: url(bg.jpg) center / cover no-repeat;
  }
  a { color: var(--blue); }
  .top {
    position: sticky; top: 0; z-index: 10; display: flex; align-items: center; gap: 10px;
    padding: 10px 16px; background: rgba(247, 243, 236, .88); backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--line);
  }
  .top img { width: 34px; height: 34px; border-radius: 50%; box-shadow: var(--shadow); }
  .top .brand { font-weight: 800; letter-spacing: .02em; font-size: 15px; }
  .top .brand small { display: block; font-weight: 600; color: var(--muted); font-size: 12px; letter-spacing: 0; }
  .top .back {
    margin-left: auto; text-decoration: none; font-weight: 700; font-size: 13px; color: var(--ink2);
    background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 7px 14px;
  }
  .wrap { max-width: 920px; margin: 0 auto; padding: 22px 16px 120px; }
  .hero {
    background: var(--card); border-radius: var(--radius); box-shadow: var(--shadow);
    padding: 28px 24px; position: relative; overflow: hidden;
  }
  .hero::after {
    content: ""; position: absolute; right: -60px; top: -60px; width: 220px; height: 220px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,170,236,.18), transparent 70%);
  }
  .pill {
    display: inline-block; font-size: 12px; font-weight: 800; letter-spacing: .08em;
    color: #fff; background: linear-gradient(90deg, var(--blue), var(--cyan));
    padding: 6px 12px; border-radius: 999px;
  }
  h1 { font-size: clamp(28px, 6vw, 42px); line-height: 1.12; margin: 14px 0 10px; letter-spacing: -.02em; }
  h1 em { font-style: normal; color: var(--blue); }
  .hero blockquote { margin: 0 0 16px; border: 0; padding: 0; font-size: 17px; color: var(--ink2); background: none; }
  .cta { display: flex; flex-wrap: wrap; gap: 10px; margin: 18px 0 6px; }
  .btn {
    display: inline-flex; align-items: center; gap: 8px; border: 0; cursor: pointer; text-decoration: none;
    font: inherit; font-weight: 800; font-size: 15px; border-radius: 14px; padding: 12px 18px; min-height: 46px;
  }
  .btn.primary { color: #fff; background: linear-gradient(90deg, var(--blue), var(--cyan)); box-shadow: 0 8px 20px rgba(30,111,224,.3); }
  .btn.ghost { color: var(--ink); background: #f1f4f9; }
  nav.toc { display: flex; gap: 8px; overflow-x: auto; padding: 16px 2px 6px; scrollbar-width: none; }
  nav.toc::-webkit-scrollbar { display: none; }
  nav.toc a {
    flex: 0 0 auto; text-decoration: none; color: var(--ink2); font-weight: 700; font-size: 13px;
    background: var(--card); border: 1px solid var(--line); border-radius: 999px; padding: 7px 13px; white-space: nowrap;
  }
  nav.toc a b { color: var(--blue); margin-right: 6px; }
  .card {
    background: var(--card); border-radius: var(--radius); box-shadow: var(--shadow);
    padding: 24px; margin-top: 18px;
  }
  .card.star { outline: 3px solid rgba(30,111,224,.35); }
  h2 { display: flex; align-items: center; gap: 12px; font-size: clamp(21px, 4.4vw, 27px); line-height: 1.25; margin: 0 0 14px; }
  h2 .num {
    flex: 0 0 auto; width: 38px; height: 38px; border-radius: 12px; display: grid; place-items: center;
    color: #fff; font-size: 17px; background: linear-gradient(135deg, var(--blue), var(--cyan));
  }
  h3 { font-size: 18px; margin: 22px 0 8px; color: var(--ink); }
  p, li { color: var(--ink2); }
  strong { color: var(--ink); }
  ul, ol { padding-left: 22px; }
  li { margin: 4px 0; }
  code {
    font-family: Consolas, "Cascadia Mono", Menlo, monospace; font-size: .88em;
    background: #eef3fb; color: #17407e; padding: 1px 6px; border-radius: 6px; word-break: break-word;
  }
  blockquote {
    margin: 14px 0; padding: 12px 16px; border-left: 4px solid var(--yellow);
    background: #fff9e6; border-radius: 0 12px 12px 0; color: var(--ink2);
  }
  .table { overflow-x: auto; margin: 12px 0; border: 1px solid var(--line); border-radius: 14px; }
  table { border-collapse: collapse; width: 100%; font-size: 14.5px; }
  th, td { text-align: left; vertical-align: top; padding: 10px 12px; border-bottom: 1px solid var(--line); }
  th { background: #f4f7fc; color: var(--ink); font-size: 13px; text-transform: uppercase; letter-spacing: .04em; }
  tr:last-child td { border-bottom: 0; }
  td:first-child { font-weight: 600; color: var(--ink); }
  .hero .table td:first-child { width: 120px; }
  .code { margin: 14px 0; border-radius: 16px; overflow: hidden; background: var(--codebg); }
  .code-bar {
    display: flex; align-items: center; justify-content: space-between; gap: 10px;
    padding: 8px 10px 8px 16px; background: #17243d; color: #9fb3d6; font-size: 12px; font-weight: 800; letter-spacing: .08em;
  }
  .code.master .code-bar { background: linear-gradient(90deg, var(--blue), var(--cyan)); color: #fff; }
  .copy {
    font: inherit; font-size: 13px; font-weight: 800; letter-spacing: 0; cursor: pointer; border: 0;
    border-radius: 10px; padding: 8px 14px; min-height: 36px; color: var(--ink); background: #fff; white-space: nowrap;
  }
  .copy.done { background: var(--green); color: #fff; }
  pre {
    margin: 0; padding: 16px; overflow: auto; color: var(--codeink);
    font-family: Consolas, "Cascadia Mono", Menlo, monospace; font-size: 13px; line-height: 1.55; white-space: pre;
  }
  .code.master pre { max-height: 560px; }
  .code.prose pre { white-space: pre-wrap; word-break: break-word; }
  .float {
    position: fixed; left: 50%; bottom: 16px; transform: translateX(-50%); z-index: 20;
    box-shadow: 0 12px 30px rgba(20, 40, 90, .35); white-space: nowrap;
  }
  footer { text-align: center; color: var(--muted); font-size: 14px; margin-top: 28px; }
  footer a { font-weight: 800; text-decoration: none; }
  .reveal { animation: up .5s ease both; }
  @keyframes up { from { transform: translateY(14px); } to { transform: none; } }
  @media (max-width: 560px) {
    .card, .hero { padding: 20px 16px; border-radius: 18px; }
    pre { font-size: 12px; }
    .top .brand small { display: none; }
    .hero .table td:first-child { width: 92px; }
    th, td { padding: 9px 10px; }
  }
  @media (prefers-reduced-motion: reduce) { .reveal { animation: none; } html { scroll-behavior: auto; } }
  @media print { .top, .float, nav.toc, body::before { display: none; } .code.master pre { max-height: none; } pre { white-space: pre-wrap; } }
</style>
</head>
<body>
<header class="top">
  <img src="logo.png" alt="Computer Hub logo">
  <div class="brand">COMPUTER HUB<small>Plan B for Software Engineers · Day 4</small></div>
  <a class="back" href="./">← All links</a>
</header>
<main class="wrap">
  <section class="hero reveal">
    <span class="pill">FREE GUIDE · DAY 4</span>
    <h1>Parking App Rebuild Kit<br><em>"BlaBlaCar for Parking"</em></h1>
    {{HERO}}
    <div class="cta">
      <a class="btn primary" href="#master-prompt-box">📋 Get the Master Prompt</a>
      <a class="btn ghost" href="#2-architecture">See the architecture</a>
    </div>
  </section>
  <nav class="toc" aria-label="Sections">{{NAV}}</nav>
  {{BODY}}
  <footer>
    <p>Made for the <strong>Plan B for Software Engineers</strong> series by Computer Hub.<br>
    Follow <a href="https://www.instagram.com/computer__hub/" target="_blank" rel="noopener">@computer__hub</a> for Day 5.</p>
    <p><a href="./">← Back to all links</a></p>
  </footer>
</main>
<button class="btn primary float" type="button" data-target="master-prompt" id="floatCopy">📋 Copy Master Prompt</button>
<script>
  function copyText(id, btn) {
    var el = document.getElementById(id);
    if (!el) return;
    var text = el.innerText;
    var old = btn.textContent;
    function ok() { btn.classList.add('done'); btn.textContent = '✓ Copied'; setTimeout(function () { btn.classList.remove('done'); btn.textContent = old; }, 1800); }
    function fallback() {
      var ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); ok(); } catch (e) { btn.textContent = 'Select & copy'; }
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(ok, fallback); else fallback();
  }
  document.querySelectorAll('[data-target]').forEach(function (b) {
    b.addEventListener('click', function () { copyText(b.getAttribute('data-target'), b); });
  });
  // Hide the floating button while the master prompt itself is on screen.
  var box = document.getElementById('master-prompt-box'), fl = document.getElementById('floatCopy');
  if ('IntersectionObserver' in window && box) {
    new IntersectionObserver(function (e) { fl.style.display = e[0].isIntersecting ? 'none' : ''; }).observe(box);
  }
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
