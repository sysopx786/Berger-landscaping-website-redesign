# MWDS 3.0 release report — Berger Landscaping

Build date: October 11, 2026 · Release: v1 (pitch build, not deployed to a public domain)

## Release checklist

| Item | Status | Evidence / gap |
|---|---|---|
| Source code updated | **Passed** | 17 pages, CSS, JS, search index, sitemap, robots, manifest generated from `_source/` |
| Build and automated tests passed | **Passed** | Playwright (Chromium headless) + axe-core 4.10: 17 pages × 4 widths (320/390/768/1440) × light/dark. 0 horizontal overflow, 0 console errors, 0 axe violations (WCAG 2 A/AA + best-practice), exactly one H1 per page. 39/40 functional checks passed (below) |
| Live public website verified | **Not verified** | Not deployed to bergerlandscaping.net. Published as a private Claude artifact preview only |
| Desktop browser reviewed | **Passed** (headless Chromium only) | Screenshots reviewed at 1440 light/dark. Not checked in Safari or Firefox |
| Mobile browser reviewed | **Passed** (emulated) | 390 px emulation with touch: action bar, menu, swipe, tap targets. Emulation is not a real phone |
| Physical Android device tested | **Not verified** | No device available |
| SEO and indexing readiness checked | **Passed** (pre-launch) | Unique titles/descriptions, canonicals, sitemap, robots, OG/Twitter, JSON-LD parses on every page. Search Console not set up; nothing is indexed |
| README and handover updated | **Passed** | `README.md` |

Fonts note: the test sandbox blocks Google Fonts, so tests loaded identical local copies of Fraunces and Archivo. Font delivery from Google itself was not verified.

## Functional tests (latest run)

Passed: services dropdown (click, hover, Esc) · ⌘K palette open, search, Enter → opens the target FAQ on another page · seasonal rail defaults to fall in October, arrow keys switch · mosaic images load · theme toggle stores and survives reload · one header logo per theme · gallery filter · lightbox open, arrows, swipe, Esc, focus return · before/after hidden without pairs, works with mouse/keyboard when configured · FAQ search, empty state, accordions by click and keyboard · map stays unloaded until consent, then inserts iframe · quote form hidden by default; when enabled, validates name/phone · mobile menu open/Esc · action bar tel/sms/quote hrefs · sticky header doesn't cover H1 · reduced motion disables parallax · no broken internal links, images, or anchors (including all 120 search targets) · no JS errors.

Minor: the "Join the crew" link in the top hiring strip is 33 px tall on mobile. It passes WCAG 2.2 AA (24 px minimum) but is under the 44 px comfort target.

## Needs owner confirmation (MWDS 1.6)

Site uses neutral wording for each until confirmed.

1. **Year founded.** About copy says 2021; the LLC filing is 09/19/2023. Site says "founded by Drew Berger" with no year.
2. **Hours.** 9 AM–5 PM, 7 days, per Google. Shown as listed, with "ask us about snow service timing during storms." Confirm Sunday hours and storm availability.
3. **Rating and count.** Site shows 5.0 and 4 reviews. Confirm live numbers; they will go stale as reviews come in.
4. **Service area.** Only "Southeastern Pennsylvania" is used. No towns or counties listed until Drew confirms them.
5. **Policies the FAQs leave as "ask us":** pricing method, contracts, snow trigger depth, accepted/refused junk items, mowing inclusions, walkway/step clearing.
6. **Mowing description is draft copy** (yours, not Drew's). Labeled on the page as draft.
7. **"Up to 12%" home-value claim** is client copy with no source. Labeled on the page; find a source or cut it.
8. **Hardscape photos.** 10 of 50 photos show patios, stone steps, and walls, but no hardscape installation service is listed. Either Drew does this (add it to Custom Landscaping copy) or these photos overstate the offer.
9. **Street address.** 110 Holby Lane is published (as in the notes). If it's a residence, Google lets service-area businesses hide it; consider removing it from the site and schema.
10. **Crew faces.** Three crew photos show identifiable people. Get their OK.
11. **Google listing URL.** Done (Oct 11): owner-supplied listing and "Leave a review" links are in place. Not click-tested from the build environment.
12. **Review dates.** Relative dates ("3 months ago") were dropped because they go stale.

13. **New photos show work not on the services list.** 9 tree-planting photos and a wood chipper suggest tree planting/tree work; 34 photos show stonework and patios (10 before). Confirm whether to add these services or keep the photos as examples of landscaping only.
14. **House numbers visible** in at least two customer photos (e.g. beds-s226 "607", beds-s252). Confirm customers are OK with this, or blur the numbers.
15. **Two near-identical photos** (trimming-s385 and trimming-s386) were both added as requested. Remove one if you prefer.

16. **Tree Planting page is entirely draft copy.** Built Oct 11 from project photos only; not in the original notes. Description, "What's included", and all 15 FAQs need Drew's review. Policy questions (supplying trees, guarantees, spacing, pricing) say "ask us." The page states PA One Call (811) is required before digging; confirm how Berger handles it.

17. **Aeration, Sod & Seeding page is draft.** Adapted Oct 11 from the Wolf's Landscaping site (sod-seeding page) and reworded for Berger so the two sites don't carry duplicate text; Wolf-specific claims (free estimates, Royersford) removed. Confirm Berger offers aeration, overseeding, seeding, sod, and grading. 9 of its 15 FAQs are new; aftercare figures (3 weeks damp, mow at ~4 in, cut ≤ 1/3) are general turf guidance. No Berger photos of this work yet (3 labeled placeholders).

## Deliberate deviations from the prompt (and why)

| Prompt asked | Built | Reason |
|---|---|---|
| Single-file SPA with hash routes | Multi-page static site | Hash routes are one URL to Google; per-page titles, canonicals, and sitemap would not work (MWDS 5 wins) |
| FAQPage JSON-LD on service pages **and** FAQ page | On the 8 service pages only | Google's guidance: mark up repeated FAQ content once. Note that FAQ rich results are currently limited to government and health sites, so this markup won't produce stars or dropdowns in search |
| `LocalBusiness` with rating | `HomeAndConstructionBusiness` without `aggregateRating` | Google ignores self-serving review markup on a business's own site |
| Google Map embed | Consent-gated (click to load) | Privacy (MWDS 13); also embeds don't render inside the Claude artifact preview |

## Business research (MWDS 1)

Limited. Confirmed facts come from your notes only. A web search returned no listing data for this business (an unrelated "Berger Landscaping & Construction" in Clyde, Ohio shares the name; watch for that in local SEO). The current site fetch wasn't permitted from this session. Competitor analysis (MWDS 1.7) was not done.

## Page titles and descriptions

| Page | Title | Description |
|---|---|---|
| Home | Berger Landscaping \| Lawn Care & Landscaping in Southeastern PA | Family-owned landscaping in Pottstown, PA: mowing, property care, custom landscaping, clean-ups, junk removal, and snow services. Call or text (610) 420-3338. |
| Services | Landscaping Services \| Berger Landscaping, Pottstown PA | Every Berger Landscaping service: mowing, aeration and seeding, property maintenance, landscaping, clean-ups, trimming, tree planting, junk removal, and snow. |
| Mowing | Lawn Mowing Service in Southeastern PA \| Berger Landscaping | Weekly lawn mowing with edging, trimming, and clean-up for homes, businesses, and HOAs, including large lawns and steep hills. Call or text (610) 420-3338. |
| Property Maintenance | Property Maintenance \| Berger Landscaping, Pottstown PA | Ongoing care of lawns, beds, shrubs, trees, hardscapes, and common areas: mowing, trimming, mulch, seasonal clean-ups, and debris removal. |
| Custom Landscaping | Custom Landscaping Design \| Berger Landscaping | Personalized landscape designs planned to reduce rainwater runoff and support natural weed and pest control. Residential and commercial. |
| Yard Clean-Up | Spring & Fall Yard Clean-Up \| Berger Landscaping | Yard clean-ups that remove weeds, rake leaves, and tidy garden beds, with debris hauled away. One-time or part of a maintenance plan. |
| Leaf Removal | Leaf Removal Service \| Berger Landscaping, Southeastern PA | Fall leaf raking and removal from lawns, beds, and walkways to prevent mold, fungus, and pests. Residential, commercial, and HOA. |
| Trimming | Tree & Shrub Trimming \| Berger Landscaping | Tree, bush, and hedge trimming for curb appeal, plant health, and safety, plus plant and shrub removal and full clean-up. |
| Junk Removal | Junk Removal \| Berger Landscaping, Pottstown PA | Junk removal from single items to full garage clean-outs: furniture, appliances, yard debris, and clutter, recycled or donated when possible. |
| Aeration, Sod & Seeding (draft) | Lawn Aeration, Overseeding & Sod \| Berger Landscaping | Core aeration, overseeding, grass seeding, and sod installation to thicken a thin lawn or start a new one in Southeastern PA. Call or text (610) 420-3338. |
| Tree Planting (draft) | Tree & Evergreen Planting \| Berger Landscaping, Southeastern PA | Tree and evergreen planting with clean mulch rings, including privacy screens along fence lines. Homes and businesses. Call or text (610) 420-3338. |
| Snow Services | Snow Plowing, Removal & Salting \| Berger Landscaping | Snow plowing and removal for driveways and commercial lots, plus salting and pet-safe ice-melt options in Southeastern PA. |
| Gallery | Project Gallery \| Berger Landscaping, Southeastern PA | Photos of Berger Landscaping work: striped lawns, mulch and planting beds, stone steps and patios, trimming, fall leaf clean-ups, and snow plowing. |
| Reviews | Customer Reviews \| Berger Landscaping | Read Google reviews of Berger Landscaping: customers describe a respectful, efficient, knowledgeable, and dependable crew. Owner replies included. |
| FAQs | Landscaping FAQs \| Berger Landscaping | Answers to 150 common questions about mowing, aeration and seeding, landscaping, clean-ups, trimming, tree planting, junk removal, and snow services. |
| About | About Drew Berger & Our Family-Owned Company \| Berger Landscaping | Meet Drew Berger, Penn State alumnus and founder of family-owned Berger Landscaping LLC, licensed and insured and serving Southeastern Pennsylvania. |
| Contact | Contact & Quotes \| Berger Landscaping, Pottstown PA | Call or text Berger Landscaping at (610) 420-3338, email drew@bergerlandscaping.net, or find us at 110 Holby Lane, Pottstown, PA. Open 9 AM to 5 PM daily. |
| Privacy | Privacy Policy \| Berger Landscaping | How the Berger Landscaping website handles your information: no analytics or tracking cookies, consent-gated Google Map, and contact details used only to respond. |
| 404 | Page Not Found \| Berger Landscaping | (noindex) |

## How the source files were used

- **Notes:** every business fact, all 8 service descriptions (verbatim), About copy (year removed), 4 reviews and replies, hiring note.
- **FAQs:** all 120 from the source file (plus 15 draft Tree Planting and 15 draft Aeration, Sod & Seeding FAQs added Oct 11) parsed programmatically onto service pages, the FAQ hub, the home preview (5), and the search index. "Ask us" wording kept.
- **MWDS v3:** drove the multi-page decision, consent gating, form-off default, Google branding block, single-instance FAQ markup, this report.
- **Logos:** horizontal → header/footer desktop; stacked → About, Meet Drew, mobile footer; badge → hero seal, favicons, OG image; icon → mobile header, watermarks, placeholders, 404. Overview sheet not displayed.

## Outstanding tasks

- [ ] Owner confirmations above (item 11 done)
- [ ] Vector/high-res logo files
- [ ] Junk removal and snow photos (4 labeled placeholders remain; the new snow photo is a road seen from a truck, not plowing work, so it's in the gallery but not on the Snow page)
- [ ] Before/after pairs, if Drew has them
- [ ] Verify the Google "G" mark and attribution against Google's current brand rules before launch
- [ ] Decide on optional features: quote form, Spanish version, analytics, Facebook feed
- [ ] Map old-site URLs → redirects; deploy; Search Console + sitemap submission
- [ ] Re-run tests on the live URL; Safari, Firefox, and a physical Android phone
