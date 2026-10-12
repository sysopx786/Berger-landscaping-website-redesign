# Berger Landscaping website — handover

## Links

| Link | Who can open it | URL |
|---|---|---|
| **Public site** (GitHub Pages) | Anyone | https://sysopx786.github.io/Berger-landscaping-website-redesign/docs/ |
| Public site, short link (redirects to the one above) | Anyone | https://sysopx786.github.io/Berger-landscaping-website-redesign/ |
| **Private preview** (Claude artifact) | Only Mujtaba, until shared from the artifact's Share menu | https://claude.ai/artifact/ASZx8CCXS3LXUJDdjN9rCD |
| Source code | Anyone (repo is public) | https://github.com/sysopx786/Berger-landscaping-website-redesign |
| Google listing / reviews (used on site) | Anyone | https://maps.app.goo.gl/VcP8FdZ8u5XwiSSY7 |
| Google "Leave a review" (used on site) | Anyone | https://maps.app.goo.gl/hmSA2zj3VKHFWFtV6 |

Notes:
- GitHub Pages currently serves from `main` / root, so the site sits under `/docs/`. Switching Settings → Pages to `main` / `/docs` puts the site at the root URL instead (the short link then shows the site directly).
- The private preview is a snapshot of v1. The Google Map and call/text buttons don't work inside it; they work on the public site.
- Final home: `https://www.bergerlandscaping.net/` once Drew approves and DNS is pointed at GitHub Pages.

Static multi-page site. No build step needed to host it; a Python generator rebuilds pages from content data.

## What's built

| Page | File | Notes |
|---|---|---|
| Home | `index.html` | Hero with layered SVG mist parallax, credibility strip, services bento, date-driven seasonal rail, 7-photo mosaic, Why Berger, 3 Google reviews, 5 FAQs, Meet Drew, CTA |
| Services overview | `services.html` | All 10 services |
| Service pages ×10 | `mowing.html`, `aeration-sod-seeding.html` (draft, adapted from the Wolf's site copy, Oct 11), `property-maintenance.html`, `custom-landscaping.html`, `yard-clean-up.html`, `leaf-removal.html`, `trimming.html`, `tree-planting.html` (draft, added Oct 11), `junk-removal.html`, `snow-services.html` | Verbatim copy from notes, "What's included", 3 photos, 15 FAQs, related services, seasonal tip, Service + FAQPage + BreadcrumbList JSON-LD |
| Gallery | `gallery.html` | 225 photos, 8 filters, "Show more" paging (36 at a time), keyboard/swipe lightbox, before/after slider (hidden until pairs are added), Facebook link |
| Reviews | `reviews.html` | 4 Google reviews + owner replies, Google attribution |
| FAQs | `faqs.html` | All 150, sticky category nav, live search, accordions |
| About | `about.html` | Drew's story, stacked logo, licensed & insured, hiring |
| Contact | `contact.html` | tel/sms/email + copy buttons, address, hours, consent-gated Google Map, quote steps, optional form (off), hiring |
| Privacy | `privacy.html` | Matches actual site behavior |
| 404 | `404.html` | noindex |

Also: `sitemap.xml` (16 URLs), `robots.txt`, `.nojekyll`, `site.webmanifest`, favicon set, Open Graph image (`assets/og-image.jpg`).

Site-wide: ⌘/Ctrl-K (or `/`) search over pages, services, and 150 FAQs; shrinking sticky header with scroll progress; mobile Call · Text · Quote bar; back-to-top; light/dark theme (remembers choice); cross-document view transitions (Chrome/Edge; other browsers just navigate normally); `prefers-reduced-motion` respected.

## Hosting (GitHub Pages)

1. The site lives in `docs/` (keep `docs/.nojekyll`).
2. Settings → Pages → Deploy from a branch → `main` / `/docs`.
3. Point `www.bergerlandscaping.net` at GitHub Pages (CNAME file + DNS). Canonicals, sitemap, and OG tags already use `https://www.bergerlandscaping.net/`. If the domain changes, edit `SITE` in `data.py` and rebuild.
4. Before switching DNS, list the old site's URLs and add redirects; I could not access the current site to map them.

## Editing content

Generator files (in `_source/`, next to `docs/`): `data.py` (business facts, services, seasonal rail, reviews), `build.py` (page templates), plus the FAQ markdown path at the top of `data.py`.

```
cd _source
python3 build.py      # rewrites every .html, search index, and sitemap in ../docs
```

Small text fixes can also be made directly in the HTML, but they'll be overwritten by the next rebuild.

## Quote form (ON)

The quote form on `contact.html` is live, posting to FormSubmit's AJAX endpoint. The endpoint is set once in `_source/data.py` (`FORM_ENDPOINT`) and injected on every page as `window.BERGER_CONFIG`.

- Current inbox: mujtaba.valli@gmail.com (pitch/testing). After Drew approves, change `FORM_ENDPOINT` to `https://formsubmit.co/ajax/drew@bergerlandscaping.net` and rebuild.
- First submission sends FormSubmit's activation email to the inbox. Until it's activated, the form shows the "didn't go through, call or text" fallback.
- After activation, FormSubmit can issue a random alias for the endpoint so the email address isn't in the page source; swap it into `FORM_ENDPOINT`.
- Fields: first/last name, phone (10 digits), email, service, address line 1, line 2 (optional), city, state (defaults to PA), ZIP (5 digits), message. All required except line 2 and photos; checked in `site.js` before sending.
- Photos: optional, up to 5 files, 10 MB total (FormSubmit's limit), images or PDF. Sent as `attachment_1`…`attachment_5`.
- Spam: honeypot field (`website`) blocks basic bots before anything is sent.
- Privacy page names FormSubmit. If you switch services (Formspree, Basin), update `privacy()` in `build.py`.

## Add before/after pairs

Drop images into `img/`, then set `beforeAfter:[{before:"img/x-before.webp",after:"img/x-after.webp",caption:"Front bed refresh"}]` in the same config. The Gallery section appears automatically. Slider works with mouse, touch, and arrow keys.

## Adding more photos (225 of 722 are on the site)

1. Curate first. 722 Facebook uploads include near-duplicates; 80–150 strong photos will beat 722 average ones.
2. Run the photo script (`_source/imgs.py`) against the folder: it grades, resizes to 640/1280 WebP + 1024 JPEG, and writes `photos.json`. Add a `category` column to a manifest CSV first.
3. Append the new entries to `_source/photos.json` (use unique IDs like `berger-lawn-s017`; the source number keeps them unique), then rebuild. The gallery reads from `photos.json`.
4. Past ~150 photos, paginate or "load more" the gallery, and host images on a CDN (Cloudflare R2/Images, or a separate GitHub Pages repo) to keep the main repo small. GitHub Pages has a 1 GB soft limit per site.

## Photo processing applied

All 225 photos (50 from the first batch, 175 added Oct 11 from the "100 More" and "75 More" sets): EXIF-rotated, slight desaturation + cool lift for a consistent grade, 640w and 1280w WebP (q74) and 1024w JPEG fallback (q78), explicit width/height, lazy loading below the fold, hero preloaded with `fetchpriority=high`. Total about 125 MB on disk; a visitor downloads only the sizes their screen needs.

## Logos

Background removed from the JPEG samples (no recoloring; tones preserved through alpha). Knockout (light-on-dark) versions created for dark mode and the footer. **The sources are low-resolution JPEGs (the horizontal lockup is only 781 px wide).** Ask the designer for SVG or high-res PNG files and swap them into `assets/`.
