import json, random, math, os, html, re, shutil, datetime
from data import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs")
PHOTOS = {p["id"]: p for p in json.load(open(os.path.join(HERE, "photos.json")))}
for k, v in ALT_FIX.items(): PHOTOS[k]["alt"] = v
E = html.escape
TODAY = "2026-10-11"
VER = "12"

# ---------------- icons ----------------
SVG = lambda inner, vb="0 0 24 24", cls="": f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}>{inner}</svg>'
ICON = {
 "mowing":'<path d="M3 20h18"/><path d="M5 20v-4M8 20v-6.5M11 20v-4.5M14 20v-6M17 20v-4M20 20v-5.5"/><path d="M3 9.5c3-2 6 2 9 0s6 2 9 0"/><path d="M3 5.5c3-2 6 2 9 0s6 2 9 0" opacity=".55"/>',
 "property":'<path d="M3 11.5 10 5.5l7 6"/><path d="M5 10v10h10V10"/><path d="M8.5 20v-5h3v5"/><path d="M20 4.5l-2.6 4.2h1.6l-2.4 4h1.6L16 16.5h8l-2.2-3.8h1.6l-2.4-4H22L20 4.5z" transform="translate(-1.5 0) scale(.92)"/>',
 "custom":'<path d="M12 2.8l3.8 5.4h-2.3l3.3 4.6h-2.5l3.2 4.8H6.5l3.2-4.8H7.2l3.3-4.6H8.2L12 2.8z"/><path d="M12 17.6v3.6"/><path d="M3 21.2h18"/>',
 "cleanup":'<path d="M14.5 2.8 9.2 13.2"/><path d="M4.5 12.2l9.5 4.8"/><path d="M5.2 12.6l-2 4M8 14l-2 4M10.8 15.4l-2 4M13.6 16.8l-2 4"/>',
 "leaf":'<path d="M4.5 19.5C4.2 10.5 10 4.6 20 4c.3 9.8-5.6 15.6-15.5 15.5z"/><path d="M4.5 19.5 14 10"/><path d="M9 15h4.5M11.5 12.5v-3"/>',
 "trimming":'<circle cx="6.5" cy="17.5" r="2.6"/><circle cx="17.5" cy="17.5" r="2.6"/><path d="M8.3 15.6 17 3.5M15.7 15.6 7 3.5"/>',
 "junk":'<path d="M2.5 6.5h11v9.5h-11z"/><path d="M13.5 9.5h4l3 3.2V16h-7"/><circle cx="6.5" cy="17.6" r="1.9"/><circle cx="16.8" cy="17.6" r="1.9"/><path d="M5.5 9.5h5M5.5 12.5h3"/>',
 "tree":'<path d="M12 21.2v-7.5"/><path d="M12 15.5 9.2 12.8M12 16.6l2.9-2.6"/><path d="M7.6 14.2a4.6 4.6 0 0 1-1-8.6 5.2 5.2 0 0 1 10 .1 4.6 4.6 0 0 1-.2 8.5z"/><path d="M8.2 21.2h7.6"/>',
 "seed":'<path d="M12 21v-8.5"/><path d="M12 13c0-3.6-2.6-6.2-6.8-6.4.1 4 2.7 6.5 6.8 6.4z"/><path d="M12 15.2c.2-3.3 2.6-5.6 6.4-5.8-.2 3.6-2.6 5.8-6.4 5.8z"/><path d="M4 21h16"/>',
 "snow":'<path d="M12 2.5v19M3.8 7.2l16.4 9.6M20.2 7.2 3.8 16.8"/><path d="M9.6 4 12 6.3 14.4 4M9.6 20 12 17.7l2.4 2.3M4.2 11l2.9.9-.8 2.9M19.8 13l-2.9-.9.8-2.9"/>',
 "phone":'<path d="M5 3.5h3.2l1.6 4.3-2.1 1.4a11 11 0 0 0 7.1 7.1l1.4-2.1 4.3 1.6V19a1.8 1.8 0 0 1-1.9 1.8C10.4 20.3 3.7 13.6 3.2 5.4A1.8 1.8 0 0 1 5 3.5z"/>',
 "text":'<path d="M4 5.5h16v10.5H9.5L5 19.5V16H4z"/><path d="M8 9.5h8M8 12.5h5"/>',
 "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
 "search":'<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.3-4.3"/>',
 "sun":'<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/>',
 "moon":'<path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/>',
 "menu":'<path d="M4 7h16M4 12h16M4 17h16"/>',
 "close":'<path d="M6 6l12 12M18 6 6 18"/>',
 "arrow":'<path d="M5 12h14M13 6l6 6-6 6"/>',
 "down":'<path d="m6 9 6 6 6-6"/>',
 "left":'<path d="m15 6-6 6 6 6"/>',
 "right":'<path d="m9 6 6 6-6 6"/>',
 "up":'<path d="M12 19V5M6 11l6-6 6 6"/>',
 "check":'<circle cx="12" cy="12" r="9"/><path d="m8 12.3 2.7 2.7L16.2 9.5"/>',
 "plus":'<path d="M12 5v14M5 12h14"/>',
 "pin":'<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "shield":'<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6L12 3z"/><path d="m8.8 12 2.3 2.3 4.2-4.4"/>',
 "family":'<circle cx="8" cy="7" r="2.6"/><circle cx="16.5" cy="8" r="2.1"/><path d="M3.5 20v-3.5A4.5 4.5 0 0 1 12.5 16.5V20"/><path d="M13.8 20v-3a3.6 3.6 0 0 1 6.7-1.8"/>',
 "chart":'<path d="M4 20V4M4 20h16"/><path d="m7.5 15 3.5-4 3 2.5 5-6"/>',
 "drop":'<path d="M12 3.5s6 6.4 6 10.5a6 6 0 0 1-12 0c0-4.1 6-10.5 6-10.5z"/><path d="M9.5 14.5a2.6 2.6 0 0 0 2.5 2.5"/>',
 "recycle":'<path d="M8.5 7.5 11 3.6a1.2 1.2 0 0 1 2 0l2.2 3.6"/><path d="m16.8 11 2.5 4.2a1.2 1.2 0 0 1-1 1.8H14"/><path d="M10 17H5.8a1.2 1.2 0 0 1-1-1.8L7 11.3"/><path d="m14.5 5.5.7 1.8-1.9.4M15.5 19l-1.5-2 1.5-1.6M5.6 10.6l1.5.8.6-1.8"/>',
 "building":'<path d="M4 20.5V5.5l8-2v17M12 9.5h8v11"/><path d="M7 8h2M7 11.5h2M7 15h2M15 13h2M15 16.5h2M2.5 20.5h19"/>',
 "map":'<path d="m3 6.5 6-2.5 6 2.5 6-2.5v13.5l-6 2.5-6-2.5-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/>',
 "copy":'<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5.5A1.5 1.5 0 0 0 14.5 4h-9A1.5 1.5 0 0 0 4 5.5v9A1.5 1.5 0 0 0 5.5 16H8"/>',
 "camera":'<path d="M4 8h3l1.8-2.5h6.4L17 8h3v11H4z"/><circle cx="12" cy="13.2" r="3.4"/>',
}
def ic(name, cls=""): return SVG(ICON[name], cls=cls)

STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.8l2.8 6 6.5.7-4.9 4.4 1.4 6.4L12 17l-5.8 3.3 1.4-6.4-4.9-4.4 6.5-.7z"/></svg>'
def stars(n=5): return f'<span class="stars" aria-hidden="true">{STAR*n}</span>'
# Google "G" mark — official four-color glyph, unaltered (verify against Google brand resources before launch)
GLOGO = '<svg class="g-logo" viewBox="0 0 48 48" role="img" aria-label="Google"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>'
FBLOGO = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#0866FF"/><path fill="#fff" d="M16.6 15.5l.5-3.5h-3.3V9.8c0-1 .5-1.9 2-1.9h1.5V5c0 0-1.4-.2-2.7-.2-2.8 0-4.6 1.7-4.6 4.7V12H7v3.5h3V24c.6.1 1.2.1 1.8.1s1.3 0 1.9-.1v-8.5h2.9z"/></svg>'

# ---------------- deer + mist generators ----------------
DEER_BODY = "M14 26c0-4 6-6 14-6h12c4 0 6-3 7-7l3-1 4 2-1 2h-3c-1 4-3 8-4 11v13h-2l-1-10h-5l-1 10h-2l-1-11H24l-2 11h-2V30c-2 1-3 3-3 10h-2v-9c-2-1-2-3-1-5z"
DEER_ANT = "M48 12.5 46 6.5 43 2.5M46 6.5l2-3.5M49.5 12l2.5-5 3-4M52 7l3-1M44.6 4.6 42 4"
def deer(x, y, s, fill, extra=""):
    return f'<g transform="translate({x} {y}) scale({s})" {extra}><path d="{DEER_BODY}" style="fill:{fill}"/><path d="{DEER_ANT}" style="stroke:{fill}" fill="none" stroke-width="1.7" stroke-linecap="round"/></g>'
DEER_ICON = f'<svg viewBox="0 0 64 44" aria-hidden="true"><path d="{DEER_BODY}" fill="currentColor"/><path d="{DEER_ANT}" stroke="currentColor" fill="none" stroke-width="1.7" stroke-linecap="round"/></svg>'

def pine(cx, base, h, w, rnd, tiers=9):
    top = base - h; pts = [(cx, top)]; trunk = w * .05; right = []
    for i in range(tiers):
        f = (i + 1) / tiers
        y = top + h * .86 * f
        xo = cx + (w / 2) * f * (0.75 + rnd.random() * .45)
        right.append((xo, y))
        right.append((cx + w * .12 * f + 1, y - h * .03))
    right = right[:-1]
    right += [(cx + trunk, base - h * .1), (cx + trunk, base)]
    left = [(2 * cx - x, y) for x, y in reversed(right)]
    pts += right + left
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"

def hill(W, H, base, amp, seed, n=7):
    r = random.Random(seed); xs = [W * i / n for i in range(n + 1)]
    ys = [base - amp * (0.4 + r.random() * .6) for _ in xs]
    d = f"M0 {H} L0 {ys[0]:.1f}"
    for i in range(1, len(xs)):
        mx = (xs[i - 1] + xs[i]) / 2
        d += f" C{mx:.1f} {ys[i-1]:.1f} {mx:.1f} {ys[i]:.1f} {xs[i]:.1f} {ys[i]:.1f}"
    return d + f" L{W} {H}Z", ys

def hero_mist():
    W, H = 1440, 240; r = random.Random(7); out = []
    layers = [  # (hill base, amp, pine count, pine h range, fill, opacity, depth)
        (150, 30, 26, (90, 150), "#E6ECEA", .12, 3),
        (178, 26, 18, (70, 120), "#E6ECEA", .2, 6),
        (214, 18, 0, (60, 100), "var(--bg)", 1, 12),
    ]
    for li, (base, amp, n, (h0, h1), fill, op, depth) in enumerate(layers):
        d, ys = hill(W, H, base, amp, 11 + li)
        paths = [d]
        for k in range(n):
            x = r.uniform(0, W)
            if 120 < x < 760 and li == 1: continue  # keep the area under the headline calm
            yb = base - amp * .5 + 6
            h = r.uniform(h0, h1); paths.append(pine(x, yb, h, h * .3, r, tiers=11))
        if li == 2:
            for x, h in [(1210, 92), (1244, 70), (1338, 104), (1376, 78)]:
                paths.append(pine(x, base - amp * .6 + 4, h, h * .3, r, tiers=11))
        g = "".join(f'<path d="{p}"/>' for p in paths)
        if li == 2:
            g += deer(1262, base - amp * .6 - 36, .78, fill)
        out.append(f'<g class="layer" data-depth="{depth}" style="fill:{fill};opacity:{op}">{g}</g>')
    birds = "".join(f'<path d="M{x} {y} q4 -4 8 0 q4 -4 8 0" fill="none" stroke="#E6ECEA" stroke-width="1.4" opacity=".6"/>' for x, y in [(1260,30),(1282,20),(1300,36),(1322,16),(1338,30),(1236,22),(1360,24)])
    out.append(f'<g class="layer" data-depth="4">{birds}</g>')
    return f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">{"".join(out)}</svg>'
HERO_MIST = hero_mist()

def edge(fill_back, fill_front, seed=3, H=90):
    W = 1440; d1, _ = hill(W, H, 58, 30, seed, 6); d2, _ = hill(W, H, 80, 22, seed + 5, 5)
    return f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true" focusable="false" style="display:block;width:100%;height:clamp(36px,5vw,70px)"><path d="{d1}" style="fill:{fill_back};opacity:.55"/><path d="{d2}" style="fill:{fill_front}"/></svg>'
def mist_divider():
    return f'<div class="divider" aria-hidden="true">{DEER_ICON.replace("<svg ", "<svg style=\"width:46px\" ")}</div>'

# ---------------- media helpers ----------------
def pic(pid, sizes="(max-width:760px) 90vw, 40vw", eager=False, cls="", alt=None):
    p = PHOTOS[pid]; a = E(alt if alt is not None else p["alt"])
    ld = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="img/{pid}-640.webp 640w, img/{pid}-1280.webp 1280w" sizes="{sizes}">'
            f'<img src="img/{pid}-1024.jpg" width="{p["w"]}" height="{p["h"]}" alt="{a}" {ld} decoding="async"{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}></picture>')
def placeholder(label="Replace with project photo"):
    return f'<div class="placeholder" role="img" aria-label="Placeholder: {E(label)}" style="width:100%;height:100%"><div><img src="assets/logo-icon-sm.webp" alt="" width="140" height="235">{E(label)}</div></div>'

# ---------------- head / chrome ----------------
FONTS = "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,300..700&family=Fraunces:ital,opsz,wght@0,9..144,300..650;1,9..144,300..500&display=swap"
NAV = [("services.html","Services"),("gallery.html","Gallery"),("reviews.html","Reviews"),("faqs.html","FAQs"),("about.html","About"),("contact.html","Contact")]

def head(p):
    canon = SITE + ("" if p["file"] == "index.html" else p["file"])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in p.get("ld", []))
    pre = ""
    if p.get("preload"):
        pid = p["preload"]
        pre = f'<link rel="preload" as="image" type="image/webp" imagesrcset="img/{pid}-640.webp 640w, img/{pid}-1280.webp 1280w" imagesizes="100vw" fetchpriority="high">'
    robots = '<meta name="robots" content="noindex">' if p.get("noindex") else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(p["title"])}</title>
<meta name="description" content="{E(p["desc"])}">
<link rel="canonical" href="{canon}">{robots}
<meta property="og:type" content="website"><meta property="og:site_name" content="Berger Landscaping LLC">
<meta property="og:title" content="{E(p["title"])}"><meta property="og:description" content="{E(p["desc"])}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(p["title"])}"><meta name="twitter:description" content="{E(p["desc"])}"><meta name="twitter:image" content="{SITE}assets/og-image.jpg">
<meta name="theme-color" content="#F7F9F8" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#141D22" media="(prefers-color-scheme: dark)">
<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">
<script>try{{var t=localStorage.getItem("berger-theme");if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/site.css?v={VER}">{pre}
{ld}
</head>'''

def header(cur):
    svc_links = "".join(f'<a href="{s["slug"]}.html">{ic(s["icon"])}<span><strong>{E(s["name"])}</strong><small>{E(s["card"])}</small></span></a>' for s in SERVICES)
    is_svc = cur == "services.html" or cur.replace(".html","") in SVC
    links = []
    for href, label in NAV:
        if href == "services.html":
            links.append(f'''<div class="nav-dd{' is-current' if is_svc else ''}"><button type="button" aria-expanded="false" aria-controls="dd-services">Services {ic("down")}</button><div class="dd-panel" id="dd-services" hidden>{svc_links}<a class="dd-all" href="services.html">All services overview</a></div></div>''')
        else:
            links.append(f'<a href="{href}"{" aria-current=\"page\"" if href == cur else ""}>{label}</a>')
    sheet_nav = "".join(f'<a href="{h}">{l}{ic("right")}</a>' for h, l in [("index.html","Home")] + NAV)
    sheet_svcs = "".join(f'<a href="{s["slug"]}.html">{ic(s["icon"])}{E(s["name"].replace(" Solutions",""))}</a>' for s in SERVICES)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<aside class="hiring" aria-label="Hiring">We're hiring. <a href="contact.html#hiring">Join the crew</a></aside>
<header class="site-header" id="top">
 <div class="wrap hdr">
  <a class="brand" href="index.html" aria-label="Berger Landscaping home">
   <img class="brand-mark logo-light" src="assets/logo-icon-sm.webp" width="140" height="235" alt="">
   <img class="brand-mark logo-dark" src="assets/logo-icon-knockout-sm.webp" width="140" height="235" alt="">
   <img class="brand-word logo-light" src="assets/logo-wordmark.webp" width="488" height="157" alt="Berger Landscaping">
   <img class="brand-word logo-dark" src="assets/logo-wordmark-knockout.webp" width="488" height="157" alt="Berger Landscaping">
  </a>
  <nav class="nav" aria-label="Main">{"".join(links)}</nav>
  <div class="hdr-actions">
   <button class="search-btn" type="button" data-cmdk aria-label="Search the site">{ic("search")}<span>Search</span><kbd>⌘K</kbd></button>
   <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch theme">{ic("moon")}</button>
   <a class="btn btn-primary btn-sm hdr-call magnetic" href="tel:{BIZ["tel"]}">{ic("phone")}{BIZ["phone"]}</a>
   <button class="icon-btn menu-btn" type="button" aria-expanded="false" aria-controls="sheet" aria-label="Open menu">{ic("menu")}</button>
  </div>
 </div>
 <div class="progress" aria-hidden="true"></div>
</header>
<div class="sheet" id="sheet" hidden role="dialog" aria-modal="true" aria-label="Menu">
 <div class="sheet-top"><img src="assets/logo-icon-sm.webp" width="140" height="235" alt="" style="height:44px;width:auto" class="logo-light"><button class="icon-btn" type="button" data-close-sheet aria-label="Close menu">{ic("close")}</button></div>
 <nav aria-label="Mobile">{sheet_nav}</nav>
 <div><p class="label" style="margin-bottom:.6rem">Services</p><div class="sheet-svcs">{sheet_svcs}</div></div>
 <a class="btn btn-primary" href="tel:{BIZ["tel"]}">{ic("phone")}Call {BIZ["phone"]}</a>
</div>
<main id="main" tabindex="-1">'''

def footer():
    svc = "".join(f'<li><a href="{s["slug"]}.html">{E(s["name"])}</a></li>' for s in SERVICES)
    return f'''</main>
<footer class="site-footer">
 <div class="wrap">
  <div class="foot">
   <div style="display:grid;gap:1rem;align-content:start">
    <img class="foot-logo" src="assets/logo-horizontal-knockout-sm.webp" width="440" height="250" alt="Berger Landscaping">
    <img class="foot-logo-sm" src="assets/logo-stacked-knockout-sm.webp" width="419" height="535" alt="Berger Landscaping">
    <p>Family-owned landscaping and property care for {BIZ["area"]}. Fully licensed and insured.</p>
    <a class="fb-link" href="{BIZ["fb"]}" rel="noopener" target="_blank">{FBLOGO}Berger Landscaping on Facebook</a>
   </div>
   <div><h2>Services</h2><ul>{svc}</ul></div>
   <div><h2>Company</h2><ul><li><a href="about.html">About Drew &amp; the crew</a></li><li><a href="gallery.html">Gallery</a></li><li><a href="reviews.html">Reviews</a></li><li><a href="faqs.html">FAQs</a></li><li><a href="service-area.html">Service area</a></li><li><a href="contact.html#hiring">We're hiring</a></li><li><a href="privacy.html">Privacy Policy</a></li></ul></div>
   <div><h2>Contact</h2><ul><li><a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a> <span style="color:var(--band-muted)">call or text</span></li><li><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></li><li style="color:var(--band-muted)">{BIZ["street"]}<br>{BIZ["city"]}, {BIZ["region"]} {BIZ["zip"]}</li><li style="color:var(--band-muted)">Every day, 9 AM – 5 PM</li></ul></div>
  </div>
  <div class="foot-bottom"><span>© <span data-year>2026</span> Berger Landscaping LLC</span><span><a href="privacy.html">Privacy</a> · <a href="contact.html">Contact</a></span></div>
 </div>
</footer>
<nav class="actionbar" aria-label="Quick actions">
 <a class="ab-call" href="tel:{BIZ["tel"]}">{ic("phone")}Call</a>
 <a href="sms:{BIZ["tel"]}">{ic("text")}Text</a>
 <a href="contact.html#quote">{ic("mail")}Quote</a>
</nav>
<button class="totop" type="button" aria-label="Back to top">{ic("up")}</button>
<dialog class="cmdk" aria-label="Search the site">
 <div class="cmdk-box">
  <div class="cmdk-in">{ic("search")}<label class="vh" for="cmdk-q">Search services, FAQs, and pages</label><input id="cmdk-q" type="search" placeholder="Search services, FAQs, pages…" autocomplete="off" role="combobox" aria-expanded="true" aria-controls="cmdk-list" aria-autocomplete="list"><kbd>Esc</kbd></div>
  <ul id="cmdk-list" role="listbox" aria-label="Results"></ul>
  <div class="cmdk-foot"><span>↑↓ to move</span><span>Enter to open</span></div>
 </div>
</dialog>
<script src="assets/search-index.js?v={VER}" defer></script>
<script>window.BERGER_CONFIG={{quoteForm:{"true" if FORM_ENDPOINT else "false"},formEndpoint:"{FORM_ENDPOINT}",beforeAfter:[]}};</script>
<script src="assets/site.js?v={VER}" defer></script>
</body>
</html>'''

def page(p, body):
    return head(p) + "\n" + header(p["file"]) + body + footer()

def phero(title, lede, crumbs=None, extra="", label=None, icon_html=""):
    cr = ""
    if crumbs:
        items = "".join(f'<li><a href="{h}">{E(l)}</a></li>' for h, l in crumbs[:-1]) + f'<li aria-current="page">{E(crumbs[-1][1])}</li>'
        cr = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{items}</ol></nav>'
    lab = f'<p class="label">{label}</p>' if label else ""
    return f'''<section class="phero">
 <div class="wrap">{cr}{icon_html}{lab}<h1>{title}</h1><p class="lede">{lede}</p>{extra}</div>
 <div class="phero-mark" aria-hidden="true"><img src="assets/logo-icon-sm.webp" alt="" width="140" height="235"></div>
 <div class="mist-edge">{edge("var(--bg)", "var(--bg)", seed=len(title))}</div>
</section>'''

def cta_band(title="Ready for a property that looks cared for?", sub="Call or text Drew for a quote. Tell us your address and what you need."):
    return f'''<div style="background:var(--bg)">{edge("var(--band)","var(--band)",seed=21)}</div>
<section class="section band cta" aria-labelledby="cta-h">
 <div class="wrap cta-inner">
  <div style="display:grid;gap:.7rem"><h2 id="cta-h">{title}</h2><p class="lede">{sub}</p></div>
  <div class="btns"><a class="btn btn-primary magnetic" href="tel:{BIZ["tel"]}">{ic("phone")}Call {BIZ["phone"]}</a><a class="btn btn-ghost" href="sms:{BIZ["tel"]}">{ic("text")}Text us</a></div>
 </div>
 <img class="cta-mark" src="assets/logo-icon-knockout-sm.webp" alt="" width="140" height="235" aria-hidden="true">
</section>'''

def acc(items, idprefix=""):
    out = []
    for i, (q, a) in enumerate(items):
        a_html = E(a)
        a_html = a_html.replace("(610) 420-3338", f'<a href="tel:{BIZ["tel"]}">(610) 420-3338</a>').replace(BIZ["email"], f'<a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a>')
        a_html = a_html.replace("See our Trimming service.", 'See our <a href="trimming.html">Trimming service</a>.').replace("See our Custom Landscaping Solutions service.", 'See our <a href="custom-landscaping.html">Custom Landscaping Solutions</a> service.')
        pid = f' id="{idprefix}{i+1}"' if idprefix else ""
        out.append(f'<details{pid}><summary><span class="q">{E(q)}</span><span class="pm" aria-hidden="true">{ic("plus")}</span></summary><div class="ans"><p>{a_html}</p></div></details>')
    return '<div class="acc">' + "".join(out) + "</div>"

# ---------------- structured data ----------------
BIZ_ID = SITE + "#business"
LOCALBIZ = {"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","@id":BIZ_ID,"name":BIZ["name"],
  "url":SITE,"telephone":"+1-610-420-3338","email":BIZ["email"],"image":SITE+"assets/og-image.jpg","logo":SITE+"assets/icon-512.png",
  "address":{"@type":"PostalAddress","streetAddress":BIZ["street"],"addressLocality":BIZ["city"],"addressRegion":BIZ["region"],"postalCode":BIZ["zip"],"addressCountry":"US"},
  "areaServed":[{"@type":"Place","name":t+", PA"} for t in TOWNS],
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"09:00","closes":"17:00"}],
  "founder":{"@type":"Person","name":"Drew Berger"},"sameAs":[BIZ["fb"]],
  "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s["name"],"url":SITE+s["slug"]+".html"}} for s in SERVICES]}
def crumbs_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+("" if h=="index.html" else h)} for i,(h,n) in enumerate(items)]}
def faq_ld(items):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}

NUMW = {8:'Eight',9:'Nine',10:'Ten',11:'Eleven',12:'Twelve'}
PAGES = []  # (file, title, desc) for report/sitemap

def write(p, body):
    PAGES.append(dict(file=p["file"], title=p["title"], desc=p["desc"], noindex=p.get("noindex", False)))
    open(os.path.join(OUT, p["file"]), "w", encoding="utf-8").write(page(p, body))

def btn_call(cls="btn-primary"): return f'<a class="btn {cls} magnetic" href="tel:{BIZ["tel"]}">{ic("phone")}Call or text {BIZ["phone"]}</a>'

# ================= HOME =================
def home():
    s = SVC
    def small(slug):
        x = s[slug]; tag = f'<span class="tag">{x["season"]}</span>' if x["season"] else ""
        return f'<a class="card reveal" href="{slug}.html" style="view-transition-name:svc-{slug}-card">{ic(x["icon"],"svc-ic")}{tag}<h3>{E(x["name"])}</h3><p>{E(x["card"])}</p><span class="more">Learn more {ic("arrow")}</span></a>'
    def wide(slug, pid):
        x = s[slug]; tag = f'<span class="tag">{x["season"]}</span>' if x["season"] else ""
        return f'<a class="card card-wide reveal" href="{slug}.html" style="view-transition-name:svc-{slug}-card"><div class="card-body">{ic(x["icon"],"svc-ic")}<h3>{E(x["name"])}</h3><p>{E(x["card"])}</p><span class="more">Learn more {ic("arrow")}</span></div><div class="card-media sk">{pic(pid,"(max-width:560px) 90vw, 25vw")}{tag}</div></a>'
    bento = (wide("mowing","berger-lawn-01") + small("property-maintenance") + small("trimming") +
             small("aeration-sod-seeding") + small("yard-clean-up") + small("leaf-removal") + small("tree-planting") +
             wide("custom-landscaping","berger-hardscape-04") + small("junk-removal") + small("snow-services"))
    tabs = "".join(f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{"true" if k=="fall" else "false"}" tabindex="{0 if k=="fall" else -1}">{v["label"]}</button>' for k, v in SEASONS.items())
    panels = ""
    for k, v in SEASONS.items():
        cards = ""
        for slug, line in v["items"]:
            base = slug.split("#")[0]; href = base + ".html" + ("#" + slug.split("#")[1] if "#" in slug else "")
            nm = "Pet-safe ice melt" if "#" in slug else s[base]["name"]
            cards += f'<a class="season-card" href="{href}">{ic(s[base]["icon"],"svc-ic")}<strong>{E(nm)}</strong><span>{E(line)}</span></a>'
        panels += f'<div class="season-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" data-season="{k}"{"" if k=="fall" else " hidden"}>{cards}</div>'
    mos_ids = ["berger-hardscape-03","berger-lawn-02","berger-beds-22","berger-hardscape-04","berger-beds-09","berger-beds-18","berger-lawn-06"]
    areas = "abcdefg"
    mosaic = "".join(f'<figure class="sk" style="grid-area:{areas[i]}">{pic(pid,"(max-width:760px) 78vw, 50vw")}<figcaption>{E(PHOTOS[pid]["alt"])}</figcaption></figure>' for i, pid in enumerate(mos_ids))
    rv = [REVIEWS[0], REVIEWS[2], REVIEWS[1]]
    quotes = "".join(f'<figure class="quote reveal">{stars()}<blockquote><p>“{E(r["text"])}”</p></blockquote><figcaption><strong>{E(r["name"])}</strong><span>Google review</span></figcaption></figure>' for r in rv)
    fq = [FAQS["Mowing"][14], FAQS["Property Maintenance"][14], FAQS["Custom Landscaping Solutions"][9], FAQS["Property Maintenance"][12], FAQS["Mowing"][4]]
    body = f'''
<section class="hero" aria-labelledby="hero-h">
 <div class="hero-media">{pic("berger-lawn-04","100vw",eager=True,alt="Freshly striped lawn leading up to a stone-front home, mowed by Berger Landscaping")}</div>
 <div class="mist" aria-hidden="true">{HERO_MIST}</div>
 <div class="seal" aria-hidden="true"><img src="assets/logo-badge-sm.webp" width="260" height="266" alt=""></div>
 <div class="wrap hero-inner">
  <p class="label eyebrow">Berger Landscaping LLC · Pottstown, PA</p>
  <h1 id="hero-h">Landscaping that looks <em>cared for</em>, all year.</h1>
  <p class="lede">Family-owned mowing, landscaping, and property care for homes, businesses, and communities, from spring clean-ups to winter plowing.</p>
  <p class="hero-area">Serving Pottstown, Royersford, Spring City, and <a href="service-area.html">nearby towns</a>.</p>
  <div class="hero-ctas">{btn_call()}<a class="btn btn-ghost" href="gallery.html">See our work {ic("arrow")}</a></div>
  <ul class="trust" aria-label="Highlights"><li>Family-owned</li><li>Licensed &amp; insured</li><li>Residential &amp; commercial</li><li>Pottstown area</li></ul>
 </div>
 <a class="scroll-cue" href="#services-h" aria-label="Skip to services">{DEER_ICON}<span class="tick"></span></a>
</section>

<section class="cred" aria-label="Credentials">
 <div class="wrap cred-row">
  <a class="cred-item" href="reviews.html" style="text-decoration:none;color:inherit">{GLOGO.replace('class="g-logo"','class="g-logo" style="width:32px;height:32px;flex:none"')}<span><strong><span class="rating-num">5.0</span> {stars()}</strong><small>Reviews from Google · 4 reviews</small></span></a>
  <div class="cred-item">{ic("shield")}<span><strong>Licensed &amp; insured</strong><small>Fully covered for residential and commercial work</small></span></div>
  <div class="cred-item">{ic("building")}<span><strong>Homes to communities</strong><small>Residential, commercial, and multi-living</small></span></div>
  <div class="cred-item">{ic("pin")}<span><strong>Serving the Pottstown area</strong><small>Royersford, Spring City &amp; more</small></span></div>
 </div>
</section>

<section class="section" aria-labelledby="services-h">
 <div class="wrap">
  <div class="sec-head"><div><p class="label">Services</p><h2 id="services-h">{NUMW[len(SERVICES)]} ways we look after your property</h2></div><a class="linkarrow" href="services.html">Compare all services {ic("arrow")}</a></div>
  {svc_cards("h3")}
 </div>
</section>

<div style="background:var(--bg)">{edge("var(--band)","var(--band)",seed=4)}</div>
<section class="section band" aria-labelledby="season-h" style="padding-top:clamp(1.5rem,2vw,2.5rem)">
 <div class="wrap season">
  <div style="display:grid;gap:1rem;align-content:start">
   <p class="label">What your property needs now</p>
   <h2 id="season-h" data-season-title>Fall: leaves off the lawn before winter sets in.</h2>
   <div class="tabs" role="tablist" aria-label="Season">{tabs}</div>
   <p class="season-note" data-season-note>Showing the current season. Pick another to plan ahead.</p>
  </div>
  <div>{panels}</div>
 </div>
</section>
<div style="background:var(--bg);transform:scaleY(-1)">{edge("var(--band)","var(--band)",seed=9)}</div>

<section class="section" aria-labelledby="work-h">
 <div class="wrap">
  <div class="sec-head"><div><p class="label">Recent work</p><h2 id="work-h">Beds, stone, and stripes from real Berger jobs</h2></div><div style="display:flex;gap:.75rem;align-items:center"><div class="carousel-ctl" data-for="mosaic"><button class="icon-btn" type="button" data-dir="-1" aria-label="Previous photos">{ic("left")}</button><button class="icon-btn" type="button" data-dir="1" aria-label="Next photos">{ic("right")}</button></div><a class="linkarrow" href="gallery.html">Full gallery {ic("arrow")}</a></div></div>
  <div class="mosaic" id="mosaic" tabindex="0" role="region" aria-label="Recent work photos" style="grid-template-areas:'a a a b b b' 'a a a c c d' 'e e f c c d' 'e e f g g g'">{mosaic}</div>
 </div>
</section>

<section class="section section-alt" aria-labelledby="why-h">
 <div class="wrap">
  <div class="sec-head"><div><p class="label">Why Berger</p><h2 id="why-h">A business-management mindset with a craftsman's eye</h2></div></div>
  <div class="why">
   <div>{ic("family")}<h3>Family-owned</h3><p>Drew Berger runs the company with his family's name on every job, serving Pottstown and nearby towns.</p></div>
   <div>{ic("chart")}<h3>Run like a business</h3><p>Drew built the company on experience in business management: clear communication and crews that show up.</p></div>
   <div>{ic("drop")}<h3>Designs that work</h3><p>Detail-oriented landscapes planned to reduce rainwater runoff and support natural weed and pest control.</p></div>
   <div>{ic("recycle")}<h3>Eco-minded hauling</h3><p>On junk removal jobs, items are recycled or donated whenever possible instead of going straight to the landfill.</p></div>
  </div>
 </div>
</section>

<section class="section" aria-labelledby="rev-h">
 <div class="wrap">
  <div class="sec-head"><div><p class="label">What customers say</p><h2 id="rev-h">Respectful, efficient, dependable</h2></div><div class="g-actions"><a class="g-badge" href="reviews.html">{GLOGO}<span>Reviews from Google · 5.0</span></a><a class="g-review-btn" href="{BIZ["greview"]}" target="_blank" rel="noopener">{GLOGO}<span class="g-review-txt"><strong>Leave a review</strong><small>on Google</small></span><span class="g-review-stars" aria-hidden="true">{STAR*5}</span></a></div></div>
  <div class="quotes" tabindex="0" role="region" aria-label="Customer reviews">{quotes}</div>
  <p style="margin-top:1.5rem;display:flex;flex-wrap:wrap;gap:.25rem 1.5rem"><a class="linkarrow" href="reviews.html">Read all reviews and Drew's replies {ic("arrow")}</a></p>
 </div>
</section>

<section class="section section-alt" aria-labelledby="faq-h">
 <div class="wrap svc-grid">
  <div class="sticky-col" style="display:grid;gap:1rem;align-content:start"><p class="label">Common questions</p><h2 id="faq-h">Quick answers before you call</h2><p class="lede">We've answered {sum(len(v) for v in FAQS.values())} questions across all {len(SERVICES)} services.</p><a class="linkarrow" href="faqs.html">Browse every FAQ {ic("arrow")}</a></div>
  {acc(fq)}
 </div>
</section>

<section class="section" aria-labelledby="drew-h">
 <div class="wrap split">
  <div class="logo-frame"><img class="logo-light" src="assets/logo-stacked-sm.webp" width="419" height="535" alt="Berger Landscaping stacked logo" loading="lazy"><img class="logo-dark" src="assets/logo-stacked-knockout-sm.webp" width="419" height="535" alt="Berger Landscaping stacked logo" loading="lazy"></div>
  <div style="display:grid;gap:1rem">
   <p class="label">Meet Drew</p>
   <h2 id="drew-h">A Penn State alum who'd rather be outside</h2>
   <p class="prose">Drew Berger founded Berger Landscaping with a background in business management and a passion for creating beautiful outdoor spaces. Off the clock, he's with his wife and three children, serving as a deacon at a local church, or out hunting and fishing.</p>
   <a class="linkarrow" href="about.html">Read our story {ic("arrow")}</a>
  </div>
 </div>
</section>
''' + cta_band("One call covers mowing to snow.", "Call or text (610) 420-3338 with your address and what you need. We're also hiring: ask about joining the crew.")
    write(dict(file="index.html", title="Berger Landscaping | Lawn Care & Landscaping, Pottstown PA",
               desc="Family-owned landscaping in Pottstown, PA: mowing, property care, custom landscaping, clean-ups, junk removal, and snow services. Call or text (610) 420-3338.",
               preload="berger-lawn-04", ld=[LOCALBIZ, {"@context":"https://schema.org","@type":"WebSite","name":"Berger Landscaping","url":SITE}]), body)

# ================= SERVICES OVERVIEW =================
def svc_cards(hl="h2"):
    rows = ""
    for x in SERVICES:
        pid = next((p for p in x["photos"] if p), None)
        tag = f'<span class="tag">{x["season"]}</span>' if x["season"] else ""
        rows += f'<a class="card card-wide reveal" href="{x["slug"]}.html" style="view-transition-name:svc-{x["slug"]}-card"><div class="card-body">{ic(x["icon"],"svc-ic")}<{hl} style="font-size:1.45rem">{E(x["name"])}</{hl}><p>{E(x["promise"])}</p><span class="more">{len(x["faqs"])} FAQs · Details {ic("arrow")}</span></div><div class="card-media{' sk' if pid else ''}">{pic(pid,"(max-width:560px) 90vw, 25vw") if pid else placeholder("Photo coming soon")}{tag}</div></a>'
    return f'<div class="bento svc-overview">{rows}</div>'

def services():
    rows = svc_cards("h2")
    body = phero("Services", f"Mowing to snow, for homes, businesses, and multi-living communities across {BIZ['area']}. Pick a service for what's included and answers to common questions.", [("index.html","Home"),("services.html","Services")], f'<div class="phero-ctas">{btn_call()}</div>') + f'''
<section class="section"><div class="wrap">{rows}</div></section>''' + cta_band()
    write(dict(file="services.html", title="Landscaping Services | Berger Landscaping, Pottstown PA",
               desc="Every Berger Landscaping service: mowing, aeration and seeding, property maintenance, landscaping, clean-ups, trimming, tree planting, junk removal, and snow.",
               ld=[crumbs_ld([("index.html","Home"),("services.html","Services")])]), body)

# ================= SERVICE PAGES =================
TITLES = {
 "mowing":("Lawn Mowing Service in Pottstown, PA | Berger Landscaping","Weekly lawn mowing with edging, trimming, and clean-up for homes, businesses, and HOAs, including large lawns and steep hills. Call or text (610) 420-3338."),
 "property-maintenance":("Property Maintenance | Berger Landscaping, Pottstown PA","Ongoing care of lawns, beds, shrubs, trees, hardscapes, and common areas: mowing, trimming, mulch, seasonal clean-ups, and debris removal."),
 "custom-landscaping":("Custom Landscaping Design | Berger Landscaping","Personalized landscape designs planned to reduce rainwater runoff and support natural weed and pest control. Residential and commercial."),
 "yard-clean-up":("Spring & Fall Yard Clean-Up | Berger Landscaping","Yard clean-ups that remove weeds, rake leaves, and tidy garden beds, with debris hauled away. One-time or part of a maintenance plan."),
 "leaf-removal":("Leaf Removal Service | Berger Landscaping, Pottstown PA","Fall leaf raking and removal from lawns, beds, and walkways to prevent mold, fungus, and pests. Residential, commercial, and HOA."),
 "trimming":("Tree & Shrub Trimming | Berger Landscaping","Tree, bush, and hedge trimming for curb appeal, plant health, and safety, plus plant and shrub removal and full clean-up."),
 "aeration-sod-seeding":("Lawn Aeration, Overseeding & Sod | Berger Landscaping","Core aeration, overseeding, grass seeding, and sod installation to thicken a thin lawn or start a new one around Pottstown, PA. Call or text (610) 420-3338."),
 "tree-planting":("Tree & Evergreen Planting | Berger Landscaping, Pottstown PA","Tree and evergreen planting with clean mulch rings, including privacy screens along fence lines. Homes and businesses. Call or text (610) 420-3338."),
 "junk-removal":("Junk Removal | Berger Landscaping, Pottstown PA","Junk removal from single items to full garage clean-outs: furniture, appliances, yard debris, and clutter, recycled or donated when possible."),
 "snow-services":("Snow Plowing, Removal & Salting | Berger Landscaping","Snow plowing and removal for driveways and commercial lots, plus salting and pet-safe ice-melt options around Pottstown, PA."),
}
def service_pages():
    for x in SERVICES:
        slug = x["slug"]
        desc = "".join(f"<p>{E(p)}</p>" for p in x["desc"])
        draft = '<p class="draft-note">Draft copy: this description was written for the new site and is waiting on owner review.</p>' if x.get("draft") else ""
        if slug == "aeration-sod-seeding":
            draft = '<p class="draft-note">Draft page: aeration, sod, and seeding aren\'t in Berger\'s original service list. Copy adapted for Berger and waiting on owner review.</p>'
        extra = ""
        for (h2, paras, bullets, closing) in x.get("sections", []):
            extra += f'<div style="display:grid;gap:1rem"><h2>{E(h2)}</h2><div class="prose">' + "".join(f"<p>{E(p)}</p>" for p in paras) + '</div>'
            if bullets: extra += '<ul class="checklist two-col">' + "".join(f'<li>{ic("check")}<span>{E(i)}</span></li>' for i in bullets) + '</ul>'
            if closing: extra += f'<p class="prose">{E(closing)}</p>'
            extra += '</div>'
        if x.get("aftercare"):
            extra += '<div style="display:grid;gap:1rem"><h2>Caring for a newly seeded lawn</h2><ol class="care-steps">' + "".join(f'<li><h3>{E(t)}</h3><p>{E(p)}</p></li>' for t, p in x["aftercare"]) + '</ol></div>'
        if slug == "tree-planting":
            draft = '<p class="draft-note">Draft page: tree planting isn\'t in the original service list. This page is based on project photos and is waiting on owner review.</p>'
        if slug == "custom-landscaping":
            draft = '<p class="draft-note">Owner to confirm: the source for the “up to 12%” home-value figure.</p>'
        inc = "".join(f'<li>{ic("check")}<span>{E(i)}</span></li>' for i in x["included"])
        photos = ""
        for pid in x["photos"]:
            if pid: photos += f'<figure class="sk">{pic(pid,"(max-width:560px) 50vw, 30vw")}<figcaption>{E(PHOTOS[pid]["alt"])}</figcaption></figure>'
            else: photos += f'<figure>{placeholder("Replace with aeration, seed, or sod photo" if slug=="aeration-sod-seeding" else "Replace with project photo")}</figure>'
        rel = ""
        for r in x["related"]:
            y = SVC[r]; rel += f'<a class="card" href="{r}.html">{ic(y["icon"],"svc-ic")}<h3>{E(y["name"])}</h3><p>{E(y["card"])}</p><span class="more">View {ic("arrow")}</span></a>'
        faq_items = x["faqs"]
        faq_html = acc(faq_items, idprefix=f"{slug}-q")
        if slug == "snow-services":
            faq_html = faq_html.replace(f'id="{slug}-q4"', 'id="pet-safe"')
        icon_html = f'<div style="view-transition-name:svc-{slug}-card;width:max-content">{ic(x["icon"],"svc-hero-ic")}</div>'
        ctas = f'<div class="phero-ctas">{btn_call()}<a class="btn btn-quiet" href="contact.html#quote">{ic("mail")}Request a quote</a></div>'
        crumbs = [("index.html","Home"),("services.html","Services"),(slug+".html",x["name"])]
        body = phero(E(x["name"]), E(x["promise"]), crumbs, ctas, icon_html=icon_html) + f'''
<section class="section">
 <div class="wrap svc-grid">
  <div style="display:grid;gap:2rem;min-width:0">
   <div style="display:grid;gap:1rem"><h2>About {E(x["name"].lower() if slug!="custom-landscaping" else "our custom landscaping")}</h2><div class="prose">{desc}</div>{draft}</div>{extra}
   <div style="display:grid;gap:1rem"><h2 class="vh">Photos</h2><div class="photo-row">{photos}</div><a class="linkarrow" href="gallery.html">See more in the gallery {ic("arrow")}</a></div>
  </div>
  <aside class="aside-stack" aria-label="Service summary">
   <div style="display:grid;gap:.75rem"><h2 style="font-size:1.4rem">What's included</h2><ul class="checklist">{inc}</ul></div>
   <div class="tip"><p class="label">Seasonal tip · {E(x["tip"][0])}</p><p>{E(x["tip"][1])}</p></div>
  </aside>
 </div>
</section>
<section class="section section-alt" aria-labelledby="faq-h">
 <div class="wrap svc-grid">
  <div class="sticky-col" style="display:grid;gap:.8rem;align-content:start"><p class="label">{len(faq_items)} questions</p><h2 id="faq-h">{E(x["name"])} FAQs</h2><p class="lede">Anything we haven't covered? Call or text {BIZ["phone"]}.</p><a class="linkarrow" href="faqs.html#{slug}">All FAQs by service {ic("arrow")}</a></div>
  {faq_html}
 </div>
</section>
<section class="section" aria-labelledby="rel-h"><div class="wrap"><div class="sec-head"><div><p class="label">Often paired with</p><h2 id="rel-h">Related services</h2></div></div><div class="related">{rel}</div></div></section>
''' + cta_band(f"Get a quote for {x['name'].lower()}.", "Call or text with your address and a short description. Photos help.")
        svc_ld = {"@context":"https://schema.org","@type":"Service","name":x["name"],"serviceType":x["name"],"description":" ".join(x["desc"])[:500],
                  "provider":{"@id":BIZ_ID,"@type":"HomeAndConstructionBusiness","name":BIZ["name"],"telephone":"+1-610-420-3338"},
                  "areaServed":[{"@type":"Place","name":t+", PA"} for t in TOWNS],"url":SITE+slug+".html"}
        t, d = TITLES[slug]
        write(dict(file=slug+".html", title=t, desc=d, ld=[svc_ld, faq_ld(faq_items), crumbs_ld(crumbs)]), body)

# ================= GALLERY =================
def gallery():
    order = [c for c, _ in CATS]
    ph = sorted(PHOTOS.values(), key=lambda p: (order.index(p["cat"]), p["id"]))
    counts = {c: sum(1 for p in ph if p["cat"] == c) for c in order}
    chips = f'<button class="chip" type="button" aria-pressed="true" data-filter="all">All <span>{len(ph)}</span></button>' + "".join(f'<button class="chip" type="button" aria-pressed="false" data-filter="{c}">{E(l)} <span>{counts[c]}</span></button>' for c, l in CATS)
    tiles = ""
    for i, p in enumerate(ph):
        tall = " tall" if p["h"] > p["w"] else ""
        tiles += f'<button type="button" class="sk{tall}" data-cat="{p["cat"]}" data-full="img/{p["id"]}-1280.webp" data-fallback="img/{p["id"]}-1024.jpg" data-cap="{E(p["alt"])}" aria-label="Open photo: {E(p["alt"])}">{pic(p["id"],"(max-width:600px) 92vw, (max-width:1100px) 45vw, 25vw")}<span class="gcap" aria-hidden="true">{E(p["alt"])}</span></button>'
    body = phero("Our work", f"{len(ph)} photos from Berger Landscaping jobs: lawns, beds, stonework, trimming, trees, fall clean-ups, and snow. Filter by type, then tap any photo to view it larger.", [("index.html","Home"),("gallery.html","Gallery")]) + f'''
<section class="section" aria-label="Photo gallery">
 <div class="wrap">
  <div class="sec-head" style="margin-bottom:0;align-items:center"><div role="group" aria-label="Filter photos" class="chips">{chips}</div><a class="linkarrow fb-link" href="{BIZ["fb_photos"]}" target="_blank" rel="noopener">{FBLOGO.replace("<svg ","<svg style=\"width:20px;height:20px\" ")}Full photo archive on Facebook {ic("arrow")}</a></div>
  <p class="vh" aria-live="polite" data-gallery-status></p>
  <div class="gallery" data-gallery data-page="36">{tiles}</div>
  <div class="gallery-more"><button class="btn btn-quiet" type="button" data-gallery-more hidden>Show more photos</button><p class="faq-count" data-gallery-count></p></div>
  <div data-ba-section hidden style="margin-top:3rem;display:grid;gap:1rem">
   <h2>Before &amp; after</h2>
   <p class="lede">Drag the handle, or focus it and use the arrow keys.</p>
   <div data-ba-list style="display:grid;gap:1.5rem"></div>
  </div>
 </div>
</section>
<dialog class="lb" aria-label="Photo viewer">
 <div class="lb-inner">
  <div class="lb-top"><span class="lb-count" aria-live="polite"></span><button type="button" class="lb-close" aria-label="Close viewer">{ic("close")}</button></div>
  <div class="lb-stage"><img alt=""><button type="button" class="lb-prev" aria-label="Previous photo">{ic("left")}</button><button type="button" class="lb-next" aria-label="Next photo">{ic("right")}</button></div>
  <p class="lb-cap"></p>
 </div>
</dialog>''' + cta_band("Like what you see?", "Call or text to talk through your property.")
    write(dict(file="gallery.html", title="Project Gallery | Berger Landscaping, Pottstown PA",
               desc="Photos of Berger Landscaping work: striped lawns, mulch and planting beds, stone steps and patios, trimming, fall leaf clean-ups, and snow plowing.",
               ld=[crumbs_ld([("index.html","Home"),("gallery.html","Gallery")])]), body)

# ================= REVIEWS =================
def reviews():
    items = ""
    for r in REVIEWS:
        ini = "".join(w[0] for w in r["name"].split()[:2])
        reply = f'<div class="owner"><b>Response from the owner</b>{E(r["reply"])}</div>' if r["reply"] else ""
        items += f'<article class="review"><div class="review-head"><div class="review-who"><span class="avatar" aria-hidden="true">{ini}</span><div><strong>{E(r["name"])}</strong><small>{E(r["meta"])}</small></div></div><span role="img" aria-label="Rated 5 out of 5">{stars()}</span></div><p>{E(r["text"])}</p>{reply}</article>'
    body = phero("Reviews", "What Berger Landscaping customers say on Google, with Drew's replies.", [("index.html","Home"),("reviews.html","Reviews")]) + f'''
<section class="section"><div class="wrap">
 <div class="rating-summary">
  <div class="rating-big" aria-hidden="true">5.0</div>
  <div style="display:grid;gap:.3rem"><span role="img" aria-label="5.0 out of 5 stars, based on 4 Google reviews">{stars()}</span><span style="color:var(--muted);font-size:.92rem">Based on 4 reviews</span></div>
  <div style="display:flex;flex-wrap:wrap;gap:.6rem;margin-left:auto"><a class="g-badge" href="{BIZ["gmaps"]}" target="_blank" rel="noopener">{GLOGO}<span>Read all reviews on Google</span></a><a class="btn btn-primary btn-sm" href="{BIZ["greview"]}" target="_blank" rel="noopener">{STAR.replace('<svg ','<svg style="width:1.1em;height:1.1em" ')}Leave a review</a></div>
 </div>
 <div class="review-list">{items}</div>
 <div class="help-panel" style="max-width:820px"><div style="display:grid;gap:.4rem"><h2>Worked with Berger?</h2><p>A short Google review helps neighbors find a crew they can trust. It takes about a minute.</p></div><div class="btns"><a class="btn btn-primary" href="{BIZ["greview"]}" target="_blank" rel="noopener">Leave a Google review</a></div></div>
 <p class="attr">Reviews are shown as posted on Google and are not edited. Google is a trademark of Google LLC; display here does not mean Google endorses Berger Landscaping. <a href="{BIZ["gmaps"]}" target="_blank" rel="noopener">See the listing and all reviews on Google Maps</a>.</p>
</div></section>''' + cta_band("Join the happy customers.", "Call or text to get on the schedule.")
    write(dict(file="reviews.html", title="Customer Reviews | Berger Landscaping",
               desc="Read Google reviews of Berger Landscaping: customers describe a respectful, efficient, knowledgeable, and dependable crew. Owner replies included.",
               ld=[crumbs_ld([("index.html","Home"),("reviews.html","Reviews")])]), body)

# ================= FAQS =================
def faqs():
    nq = sum(len(v) for v in FAQS.values())
    nav = "".join(f'<a href="#{FAQ_KEY[g]}" data-faq-link="{FAQ_KEY[g]}">{E(g.replace(" Solutions",""))}<span>{len(v)}</span></a>' for g, v in FAQS.items())
    groups = ""
    for g, v in FAQS.items():
        slug = FAQ_KEY[g]
        groups += f'<section class="faq-group" id="{slug}" data-faq-group aria-labelledby="h-{slug}"><h2 id="h-{slug}">{ic(SVC[slug]["icon"])}{E(g)}</h2>{acc(v)}<a class="linkarrow grp-link" href="{slug}.html">{E(g)} service details {ic("arrow")}</a></section>'
    body = phero("Frequently asked questions", f"{sum(len(v) for v in FAQS.values())} answers across all {len(SERVICES)} services. Search, or jump to a service.", [("index.html","Home"),("faqs.html","FAQs")],
                 f'<div class="searchbox" style="margin-top:.5rem">{ic("search")}<label class="vh" for="faq-q">Search the FAQs</label><input id="faq-q" type="search" placeholder="Try “steep hill”, “pet-safe”, or “contract”" autocomplete="off"></div><p class="faq-count" aria-live="polite" data-faq-count data-all-text="Showing all {nq} questions">Showing all {nq} questions</p>') + f'''
<section class="section"><div class="wrap faq-layout">
 <nav class="faq-nav" aria-label="FAQ categories">{nav}</nav>
 <div style="min-width:0">{groups}
  <p data-faq-empty hidden style="padding:2rem 0;color:var(--muted)">No questions match that search. Call or text {BIZ["phone"]} and ask us directly.</p>
  <div class="help-panel"><div style="display:grid;gap:.4rem"><h2>Still have a question?</h2><p>Call or text Drew. A quick message with your address and a photo gets the fastest answer.</p></div><div class="btns"><a class="btn btn-primary" href="tel:{BIZ["tel"]}">{ic("phone")}Call</a><a class="btn btn-quiet" href="sms:{BIZ["tel"]}">{ic("text")}Text</a></div></div>
 </div>
</div></section>'''
    write(dict(file="faqs.html", title="Landscaping FAQs | Berger Landscaping",
               desc="Answers to 150 common questions about mowing, aeration and seeding, landscaping, clean-ups, trimming, tree planting, junk removal, and snow services.",
               ld=[crumbs_ld([("index.html","Home"),("faqs.html","FAQs")])]), body)

# ================= ABOUT =================
def about():
    body = phero("Family-owned, rooted in Pottstown", "Berger Landscaping is a family-owned landscaping business proudly serving Pottstown and the surrounding communities.", [("index.html","Home"),("about.html","About")], label="About us") + f'''
<section class="section"><div class="wrap split">
 <div class="logo-frame"><img class="logo-light" src="assets/logo-stacked-sm.webp" width="419" height="535" alt="Berger Landscaping logo: misty pines with a standing deer"><img class="logo-dark" src="assets/logo-stacked-knockout-sm.webp" width="419" height="535" alt="Berger Landscaping logo: misty pines with a standing deer"></div>
 <div style="display:grid;gap:1.1rem">
  <h2>Meet Drew Berger</h2>
  <div class="prose">
   <p>Welcome to Berger Landscaping LLC! The company was founded by Drew Berger, a devoted Penn State alumnus. It's built on a foundation of experience in business management and a passion for creating beautiful outdoor spaces. Drew is dedicated to delivering meticulous and personalized landscaping solutions for every project.</p>
   <p>Outside of work, he enjoys time spent with his wife and three children, serves as a deacon at a local church, and is an avid hunter and fisherman. We deeply appreciate your ongoing support, which helps our growing family and allows us to make a positive impact in our community.</p>
   <p>Thank you for being an essential part of the Berger Landscaping LLC family!</p>
  </div>
 </div>
</div>
<div class="wrap"><div class="facts">
 <div>{ic("shield")}<strong>Licensed &amp; insured</strong><span>Fully licensed and insured for residential and commercial landscaping.</span></div>
 <div>{ic("building")}<strong>Every kind of property</strong><span>Homes, commercial businesses, and multi-living communities.</span></div>
 <div>{ic("pin")}<strong>Pottstown &amp; nearby towns</strong><span>Based in Pottstown. <a href="service-area.html">See the towns we serve</a>.</span></div>
</div></div></section>
{mist_divider()}
<section class="section" style="padding-top:1rem" aria-labelledby="hire-h"><div class="wrap"><div class="help-panel" style="margin-top:0"><div style="display:grid;gap:.4rem"><p class="label">Careers</p><h2 id="hire-h">We're currently hiring</h2><p>Want to work outside with a family-run crew? Call or text {BIZ["phone"]} if you're interested.</p></div><div class="btns"><a class="btn btn-primary" href="sms:{BIZ["tel"]}">{ic("text")}Text about a job</a><a class="btn btn-quiet" href="contact.html#hiring">Details</a></div></div></div></section>''' + cta_band()
    write(dict(file="about.html", title="About Drew Berger | Berger Landscaping, Pottstown PA",
               desc="Meet Drew Berger, Penn State alumnus and founder of family-owned Berger Landscaping LLC, licensed and insured and serving Pottstown, PA and nearby towns.",
               ld=[crumbs_ld([("index.html","Home"),("about.html","About")]), {"@context":"https://schema.org","@type":"AboutPage","name":"About Berger Landscaping","about":{"@id":BIZ_ID}}]), body)

# ================= CONTACT =================
def contact():
    opts = "".join(f'<option>{E(s["name"])}</option>' for s in SERVICES)
    body = phero("Contact Berger Landscaping", "Call or text for the fastest answer. Tell us your address, the service you need, and any photos.", [("index.html","Home"),("contact.html","Contact")], f'<div class="phero-ctas"><a class="btn btn-primary magnetic" href="tel:{BIZ["tel"]}">{ic("phone")}Call {BIZ["phone"]}</a><a class="btn btn-quiet" href="sms:{BIZ["tel"]}">{ic("text")}Text</a><a class="btn btn-quiet" href="mailto:{BIZ["email"]}">{ic("mail")}Email</a></div>') + f'''
<section class="section"><div class="wrap contact-grid">
 <div>
  <div class="cblock"><p class="label">Phone · call or text</p><span class="big">{BIZ["phone"]}</span><div class="row"><a class="btn btn-sm btn-quiet" href="tel:{BIZ["tel"]}">{ic("phone")}Call</a><a class="btn btn-sm btn-quiet" href="sms:{BIZ["tel"]}">{ic("text")}Text</a><button class="copy-btn" type="button" data-copy="{BIZ["phone"]}">Copy number</button></div></div>
  <div class="cblock"><p class="label">Email</p><span class="big" style="font-size:1.25rem">{BIZ["email"]}</span><div class="row"><a class="btn btn-sm btn-quiet" href="mailto:{BIZ["email"]}">{ic("mail")}Send email</a><button class="copy-btn" type="button" data-copy="{BIZ["email"]}">Copy email</button></div></div>
  <div class="cblock"><p class="label">Address</p><address style="font-style:normal">{BIZ["street"]}<br>{BIZ["city"]}, {BIZ["region"]} {BIZ["zip"]}</address></div>
  <div class="cblock"><p class="label">Hours</p><table class="hours"><caption class="vh">Business hours</caption><tbody><tr><td>Sunday – Saturday</td><td>9:00 AM – 5:00 PM</td></tr></tbody></table><p style="font-size:.88rem;color:var(--muted);margin-top:.5rem">For snow service timing during storms, ask us when you sign up.</p></div>
  <div class="cblock" style="border-bottom:0"><p class="label">Service area</p><p>Serving <strong>Pottstown, Royersford, Spring City</strong>, and nearby towns. <a href="service-area.html">See all the towns we serve</a>. Not sure we reach you? Call or text with your address.</p></div>
 </div>
 <div>
  <div class="map" data-map data-src="{BIZ["gembed"]}">
   <div class="map-gate">
    <svg class="mist-mini" viewBox="0 0 160 60" aria-hidden="true">{"".join(f'<path d="{pine(x,52,h,h*.42,random.Random(x))}" fill="currentColor" opacity="{o}"/>' for x,h,o in [(30,40,.5),(55,50,.8),(80,36,.5),(105,46,.8),(130,38,.5)])}<path d="M0 60 Q40 44 80 52 T160 50 V60Z" fill="currentColor"/></svg>
    <p>The map is provided by Google. Loading it shares your IP address and device details with Google.</p>
    <button class="btn btn-quiet" type="button" data-map-load>{ic("map")}Load Google Map</button>
   </div>
  </div>
  <div class="map-links"><a href="{BIZ["gdir"]}" target="_blank" rel="noopener">Get directions in Google Maps</a><a href="{BIZ["gmaps"]}" target="_blank" rel="noopener">View the Google listing</a></div>
 </div>
</div></section>
<section class="section section-alt" id="quote" aria-labelledby="quote-h"><div class="wrap">
 <div class="sec-head"><div><p class="label">Get a quote</p><h2 id="quote-h">Three steps to a quote</h2></div></div>
 <ol class="quote-steps">
  <li><h3>Call or text</h3><p>Reach Drew at <a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a>, or email <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a>.</p></li>
  <li><h3>Share the details</h3><p>Your address, the service you need, and anything unusual: a steep hill, locked gates, pets.</p></li>
  <li><h3>Send photos</h3><p>A few photos of the lawn, beds, or items for removal help us quote it accurately.</p></li>
 </ol>
 <form class="form" data-quote-form hidden novalidate aria-labelledby="form-h" method="post" action="{FORM_ENDPOINT}" enctype="multipart/form-data">
  <h3 id="form-h" class="full">Request a quote online</h3>
  <p class="full form-note">All fields are required unless marked optional.</p>
  <label>First name<input id="qf-first" name="first_name" autocomplete="given-name" required></label>
  <label>Last name<input id="qf-last" name="last_name" autocomplete="family-name" required></label>
  <label>Phone<input id="qf-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required></label>
  <label>Email<input id="qf-email" name="email" type="email" autocomplete="email" required></label>
  <label class="full">Service<select id="qf-service" name="service" required><option value="">Choose a service</option>{opts}</select></label>
  <label class="full">Address line 1<input id="qf-addr1" name="address_line_1" autocomplete="address-line1" placeholder="Street address" required></label>
  <label class="full"><span>Address line 2 <span class="opt">(optional)</span></span><input id="qf-addr2" name="address_line_2" autocomplete="address-line2" placeholder="Apt, suite, unit"></label>
  <div class="full addr-row">
   <label>City<input id="qf-city" name="city" autocomplete="address-level2" required></label>
   <label>State<select id="qf-state" name="state" autocomplete="address-level1" required><option value="AL">Alabama</option><option value="AK">Alaska</option><option value="AZ">Arizona</option><option value="AR">Arkansas</option><option value="CA">California</option><option value="CO">Colorado</option><option value="CT">Connecticut</option><option value="DE">Delaware</option><option value="DC">District of Columbia</option><option value="FL">Florida</option><option value="GA">Georgia</option><option value="HI">Hawaii</option><option value="ID">Idaho</option><option value="IL">Illinois</option><option value="IN">Indiana</option><option value="IA">Iowa</option><option value="KS">Kansas</option><option value="KY">Kentucky</option><option value="LA">Louisiana</option><option value="ME">Maine</option><option value="MD">Maryland</option><option value="MA">Massachusetts</option><option value="MI">Michigan</option><option value="MN">Minnesota</option><option value="MS">Mississippi</option><option value="MO">Missouri</option><option value="MT">Montana</option><option value="NE">Nebraska</option><option value="NV">Nevada</option><option value="NH">New Hampshire</option><option value="NJ">New Jersey</option><option value="NM">New Mexico</option><option value="NY">New York</option><option value="NC">North Carolina</option><option value="ND">North Dakota</option><option value="OH">Ohio</option><option value="OK">Oklahoma</option><option value="OR">Oregon</option><option value="PA" selected>Pennsylvania</option><option value="RI">Rhode Island</option><option value="SC">South Carolina</option><option value="SD">South Dakota</option><option value="TN">Tennessee</option><option value="TX">Texas</option><option value="UT">Utah</option><option value="VT">Vermont</option><option value="VA">Virginia</option><option value="WA">Washington</option><option value="WV">West Virginia</option><option value="WI">Wisconsin</option><option value="WY">Wyoming</option></select></label>
   <label>ZIP code<input id="qf-zip" name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="10" required></label>
  </div>
  <label class="full">What do you need?<textarea id="qf-message" name="message" required></textarea></label>
  <div class="full file-field">
   <span class="file-label" id="qf-files-label">Photos <span class="opt">(optional, up to 5 files, 10 MB total)</span></span>
   <label class="btn btn-quiet file-btn" for="qf-files">{ic("camera")}Attach photos</label>
   <input id="qf-files" class="file-input" name="attachments" type="file" multiple accept="image/*,.heic,.heif,.pdf" aria-labelledby="qf-files-label">
   <ul class="file-list" aria-live="polite"></ul>
  </div>
  <input type="hidden" name="_subject" value="New quote request: Berger Landscaping website"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="">
  <label class="hp" aria-hidden="true">Leave this empty<input id="qf-website" name="_honey" tabindex="-1" autocomplete="off"></label>
  <div class="full" style="display:flex;flex-wrap:wrap;gap:1rem;align-items:center"><button class="btn btn-primary" type="submit">Send request</button><p class="form-status" role="status"></p></div>
  <p class="full" style="font-size:.84rem;color:var(--muted)">Please don't include payment details or other sensitive information.</p>
 </form>
</div></section>
<section class="section" id="hiring" aria-labelledby="hiring-h"><div class="wrap"><div class="help-panel" style="margin-top:0"><div style="display:grid;gap:.4rem"><p class="label">Careers</p><h2 id="hiring-h">We're currently hiring</h2><p>Interested in joining the crew? Call or text {BIZ["phone"]}.</p></div><div class="btns"><a class="btn btn-primary" href="tel:{BIZ["tel"]}">{ic("phone")}Call</a><a class="btn btn-quiet" href="sms:{BIZ["tel"]}">{ic("text")}Text</a></div></div></div></section>'''
    write(dict(file="contact.html", title="Contact & Quotes | Berger Landscaping, Pottstown PA",
               desc="Call or text Berger Landscaping at (610) 420-3338, email drew@bergerlandscaping.net, or find us at 110 Holby Lane, Pottstown, PA. Open 9 AM to 5 PM daily.",
               ld=[LOCALBIZ, crumbs_ld([("index.html","Home"),("contact.html","Contact")])]), body)

# ================= PRIVACY / 404 =================
def privacy():
    FORM_PRIVACY = '<p>Our Contact page has an optional quote form. When you press “Send request,” the details you enter (name, phone, email, service, address, message, and any photos you attach) are sent through <a href="https://formsubmit.co/" target="_blank" rel="noopener">FormSubmit</a>, a form-to-email service, which delivers them to us by email. We use them only to respond and quote your job, keep the email only as long as we need it for that work, and do not sell or share it. Please don\'t include payment details or other sensitive information.</p>' if FORM_ENDPOINT else '<p>This site does not currently offer an online form. If one is added, this policy will be updated to say where submissions are sent and how long they are kept.</p>'
    body = phero("Privacy Policy", "What this website collects, and what it doesn't.", [("index.html","Home"),("privacy.html","Privacy Policy")], f'<p style="color:var(--muted);font-size:.9rem">Last updated October 12, 2026</p>') + f'''
<section class="section"><div class="wrap prose">
<h2>Summary</h2>
<p>This site does not use analytics, advertising trackers, or cookies. It does not ask you for an account, and it does not collect personal information unless you choose to contact us.</p>
<h2>Information stored in your browser</h2>
<p>If you switch between light and dark themes, your choice is saved in your browser's local storage so the site remembers it. If you choose to load the Google Map, that choice is remembered the same way. You can clear both at any time by clearing this site's data in your browser.</p>
<h2>Google Maps</h2>
<p>The map on our Contact page does not load until you press “Load Google Map.” When it loads, Google receives your IP address and device information and may set cookies, under <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google's Privacy Policy</a>. Links to Google Maps and Google reviews open Google's own site.</p>
<h2>Facebook</h2>
<p>We link to our Facebook page. We do not embed Facebook content on this site, so Facebook receives nothing from your visit here unless you follow a link to it.</p>
<h2>Phone, text, and email</h2>
<p>Call, text, and email buttons open apps on your own device. When you contact us, we use the details you send (such as your name, number, address, and photos) only to respond, quote, and do the work you ask for. We do not sell your information.</p>
<h2>Online quote form</h2>
{FORM_PRIVACY}
<h2>Fonts</h2>
<p>Typefaces are served by Google Fonts, which receives your IP address when your browser requests them.</p>
<h2>Questions</h2>
<p>Email <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a> or call {BIZ["phone"]}.</p>
</div></section>'''
    write(dict(file="privacy.html", title="Privacy Policy | Berger Landscaping",
               desc="How the Berger Landscaping site handles your information: no analytics or tracking cookies, consent-gated Google Map, and contact details used only to respond.",
               ld=[crumbs_ld([("index.html","Home"),("privacy.html","Privacy Policy")])]), body)

def notfound():
    body = phero("This page wandered off", "The page you're looking for isn't here. Try a service below or search the site.", None, f'<div class="phero-ctas"><a class="btn btn-primary" href="index.html">Go to the home page</a><button class="btn btn-quiet" type="button" data-cmdk>{ic("search")}Search the site</button></div>')
    write(dict(file="404.html", title="Page Not Found | Berger Landscaping", desc="This page could not be found.", noindex=True), body)

def service_area():
    items = "".join(f"<li>{E(t)}</li>" for t in TOWNS)
    body = phero("Towns we serve", "Pottstown, PA and the surrounding area.", [("index.html","Home"),("service-area.html","Service Area")]) + f'''
<section class="section"><div class="wrap"><ul class="towns" aria-label="Towns we serve">{items}</ul></div></section>'''
    write(dict(file="service-area.html", title="Service Area | Berger Landscaping, Pottstown PA",
               desc="Towns Berger Landscaping serves around Pottstown, PA, including " + ", ".join(t for t in TOWNS if t in ("Boyertown","Collegeville","Limerick","Phoenixville","Royersford","Spring City")) + ", and more.",
               ld=[LOCALBIZ, crumbs_ld([("index.html","Home"),("service-area.html","Service Area")])]), body)

def thanks():
    body = phero("Thanks, your request is in", f"We got your request. Drew will get back to you. Need us sooner? Call or text {BIZ['phone']}.", None, f'<div class="phero-ctas"><a class="btn btn-primary" href="tel:{BIZ["tel"]}">{ic("phone")}Call {BIZ["phone"]}</a><a class="btn btn-quiet" href="index.html">Back to the home page</a></div>')
    write(dict(file="thanks.html", title="Request Received | Berger Landscaping", desc="Your quote request was received.", noindex=True), body)

# ================= search index, sitemap, etc =================
def extras():
    idx = [dict(k="Page", t=t, d=d, u=u) for u, t, d in [
        ("index.html","Home","Landscaping that looks cared for, all year."),("services.html","All services",f"Compare all {len(SERVICES)} services"),
        ("gallery.html","Gallery",f"{len(PHOTOS)} photos of recent work"),("reviews.html","Reviews","Google reviews and owner replies"),
        ("faqs.html","FAQs",f"{sum(len(v) for v in FAQS.values())} answers by service"),("about.html","About Drew Berger","Family-owned, Penn State alumnus"),
        ("contact.html","Contact & hours","Phone, email, address, map, hours"),("contact.html#quote","Get a quote","Call, text, or email with details"),
        ("contact.html#hiring","We're hiring","Join the crew"),("service-area.html","Service area","Towns we serve around Pottstown"),("reviews.html","Leave a review","Review Berger Landscaping on Google"),("privacy.html","Privacy Policy","What this site collects")]]
    for s in SERVICES:
        idx.append(dict(k="Service", t=s["name"], d=s["promise"], u=s["slug"]+".html"))
    for g, v in FAQS.items():
        for i, (q, a) in enumerate(v):
            idx.append(dict(k=g.replace(" Solutions","").replace("Property Maintenance","Property"), t=q, d=a, u=f'{FAQ_KEY[g]}.html#{FAQ_KEY[g]}-q{i+1}' if not (FAQ_KEY[g]=="snow-services" and i==3) else "snow-services.html#pet-safe"))
    open(f"{OUT}/assets/search-index.js","w").write("window.SEARCH_INDEX=" + json.dumps(idx, ensure_ascii=False, separators=(",",":")) + ";")
    urls = "".join(f"<url><loc>{SITE}{'' if p['file']=='index.html' else p['file']}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES if not p["noindex"])
    open(f"{OUT}/sitemap.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(f"{OUT}/robots.txt","w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    open(f"{OUT}/.nojekyll","w").write("")
    open(f"{OUT}/site.webmanifest","w").write(json.dumps({"name":"Berger Landscaping","short_name":"Berger","start_url":"./","display":"standalone","background_color":"#F7F9F8","theme_color":"#2B3A42","icons":[{"src":"assets/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"assets/icon-512.png","sizes":"512x512","type":"image/png"}]}, indent=1))
    open(os.path.join(HERE, "pages.json"),"w").write(json.dumps(PAGES, indent=1))

home(); services(); service_pages(); gallery(); reviews(); faqs(); about(); contact(); privacy(); service_area(); notfound(); thanks(); extras()
print("pages:", len(PAGES))
