# Squire site

Marketing site for **Squire**, an independent developer of plugins for Even G2 smart glasses. The hero product is **Rideshare G2 by Squire**: an iOS-first, Uber-only, read-only plugin that shows ride status, approximate driver distance, pickup ETA, driver name and license plate, and switches pickup ETA to drop-off ETA once the ride starts.

Static HTML/CSS/JS. No build step, no framework, no dependencies.

## Files

- `index.html` – landing page (all page-specific CSS and the JS live inline in this file)
- `privacy.html` – Rideshare G2 privacy policy (page-specific CSS inline)
- `styles.css` – shared tokens, @font-face, header, buttons, badge, footer
- `fonts/` – self-hosted WOFF subsets (Latin-1)
- `img/` – production photos (WebP)
- `assets-src/` – original photos, the official G2 UI reference PNG, the Even logo. Not served; used to regenerate `img/`
- `tools/erase_hud.py` – removes baked-in green HUD graphics from a photo

## Run locally

`npx serve .` (or `python3 -m http.server`) and open http://localhost:3000. Fonts and images use relative paths, so opening the file directly also mostly works.

## Page structure (index.html, top to bottom)

1. Header: `SQUIRE` wordmark (text only, Diatype Extended, uppercase), links (Rideshare G2 → `#demo`, FAQ → `#faq`, Privacy), dark pill button "Find us in the G2 Marketplace" with Even logo.
2. Hero: badge "Rideshare G2 by Squire · Now in beta", h1 "Your ride, right where you look.", lead, marketplace button, photo `img/look.webp` with a live G2 overlay (`#hud`, cycles through 4 states).
3. Facts row: three icon + label items.
4. `#demo` "Call the ride. Close the app.": lens close-up `img/lens.webp` with overlay `#hud2`, driven by the step buttons (`#steps`), auto-advances until tapped.
5. `#less` "Built to do less.": three-panel ride sequence (`img/ride-1..3.webp`, each with a static overlay) and captions, then four points (Read-only, Nothing kept, iOS first, Uber only).
6. Dark band "Small software. Made with care." with `img/frames.webp` (transparent PNG-derived WebP).
7. `#faq` accordion (`<details>`).
8. `#early` dark "Ride with us early." panel: invite email `join@getsquire.dev` + copy button, "Request an invite" mailto, lens photo `img/lens-dark.webp` with overlay.
9. Footer.

## Design system

Inspired by popcorn.space: pale off-white page, centred headlines, grey sub-text, dark pill buttons, soft tinted/dark panels, 20–28px radii.

- Colours: tokens on `:root` in `styles.css` (`--bg #f7f7f6`, `--ink`, `--head`, `--text-2`, `--charcoal #2a2a2a`, sky/peach gradient tokens). Deliberately light-only (`color-scheme: light`).
- Type:
  - Headings (`h1–h3`, `--serif`): **Signifier Light** (`fonts/signifier-300.woff`). Only the Light weight exists; `font-synthesis: none` prevents faux bold. The test font has **no `?` or `’` glyphs**, so FAQ questions use Diatype instead. Swap in the licensed full font to lift both limits.
  - Body/UI (`--sans`): ABC Diatype 400/500.
  - Wordmark (`--wordmark`): ABC Diatype Extended 500, uppercase, `letter-spacing: .12em`.
  - Mono: ABC Diatype Mono.
  - G2 display text: **Share Tech** (Google Fonts), a close match to the G2 system font.
- Buttons: `.btn` (dark) and `.btn.light`. Marketplace buttons link to `https://www.evenrealities.com/smart-glasses` (target=_blank) and carry the Even logo as an inline 6×5-grid SVG (`svg.even`).

## G2 display overlays (important)

Every "screen" on the site is live HTML text projected onto a photo, not baked into the image.

- The official G2 canvas is **576×288**. Reference: `assets-src/official-ui-ride-in-progress.png` (pure `#00FF00` on transparent). Layout: status caps top-left; driver name and plate bottom-left; ETA at x=318 on the name line.
- Markup: `<div class="g2" data-quad="x1,y1,x2,y2,x3,y3,x4,y4" data-w="IMG_NATURAL_WIDTH" [data-cw data-ch]>` inside a `.shot` wrapper next to its `<img>`. Spans: `.s` status, `.n` name, `.p` plate, `.e` ETA, `.d` distance.
- `data-quad` = the four corners **TL, TR, BL, BR** in the image's natural pixel coordinates. JS (`fit()` in index.html) computes a projective transform (matrix3d) from the canvas to that quad and re-fits on resize via ResizeObserver.
- Canvas variants: default 576×288; `.g2.c` 300×240 stacked (ride panel 1); `.g2.w` 420×150 wide (ride panels 2–3). Pass `data-cw`/`data-ch` for non-default sizes.
- Ride states (JS `states` array): FINDING A DRIVER → DRIVER ON THE WAY → DRIVER ARRIVING → RIDE IN PROGRESS. Sample data: Maria K., Plate 7ABC123 (from the official UI reference).
- To add a new photo: remove any existing green UI with `tools/erase_hud.py`, export WebP to `img/`, measure the target quad corners in natural pixels, add the `.g2` block.

## Copy rules

Concise, simple, confident. Say "Rideshare G2 by Squire" where the product is introduced. Never imply affiliation with Uber or Even Realities; keep the footer disclaimer. Rideshare G2 is read-only: never claim it books, cancels, pays or shows maps.

## Open items before launch

- Privacy page placeholders filled (2026-09-29): effective date, Carmel IN address, 60-minute session TTL, Vercel Inc. as host, North America. Re-check hosting provider names and TTL against the real backend before launch. Have counsel review.
- Real G2 Marketplace listing URL (buttons currently go to evenrealities.com/smart-glasses).
- Font licences: ABC Diatype files are DINAMO trials and Signifier is a test font. Licence both before going public.
- Confirm rights to use Even Realities product photos and the Even logo.
- Ride panel photos are ~660px wide; supply higher-resolution versions for sharper phones/retina.
