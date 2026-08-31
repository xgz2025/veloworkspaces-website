# veloworkspaces.com

Marketing site, privacy policy, and support/FAQ page for [Velo Workspaces](https://www.veloworkspaces.com).

Plain static HTML + CSS. No framework, no build step, no JavaScript beyond one small script that fills in
the App Store download link. This is deliberate — it keeps the site fast, dependency-free, and easy for
search engines to crawl.

The site is localized into 10 languages (see "Localization" below) — still plain static HTML per locale,
still no build step for deployment. The `i18n/` scripts are authoring tooling only, used to keep 30 generated
pages consistent; they never run at request time and are excluded from the deployed assets.

## Structure

```
index.html          Home / marketing page                 (English, at /)
privacy/index.html  Privacy policy                         → served at /privacy/
support/index.html  Support & FAQ                           → served at /support/
404.html            Not-found page
de/ fr/ it/ es/ pt-br/ ja/ ko/ zh-hans/ zh-hant/
                     Same three pages + 404, per locale     → served at /<locale>/, /<locale>/privacy/, etc.
i18n/                Authoring scripts that generate every localized page — see "Localization" below
robots.txt
sitemap.xml          Generated — lists all 30 localized URLs with hreflang alternates
_redirects          Cloudflare Workers assets: path-level redirects (none active — see below)
_headers            Cloudflare Workers assets: security + cache headers
wrangler.jsonc      Deploy config (Workers static assets, no worker code)
.assetsignore       Keeps .git, this README, i18n/, etc. out of the deployed assets
assets/style.css    All styling
assets/app-store.js Fills in every [data-app-store-link] button's href from one place
assets/icon.png     App icon — used as both the favicon and the header/footer brand mark
assets/screenshots/ Four app screenshots shown in the home page hero (see below)
```

## Localization

Every page exists in English plus 9 other locales — German, French, Italian, Spanish, Brazilian
Portuguese, Japanese, Korean, Simplified Chinese, and Traditional Chinese — at `/<locale>/`
(`/de/`, `/fr/`, `/zh-hans/`, etc.), matching the app's own in-app localizations (profile names, "AI
Bridge", "Disposable" terminology are kept consistent with `Localizable.xcstrings` in the app repo). The
app's product name, "Velo Workspaces", is never translated.

**This is generated, not hand-maintained per file.** The English copy for each page and the corresponding
translations live as Python dicts in `i18n/content_home.py`, `i18n/content_privacy.py`, and
`i18n/content_support.py` — one dict key per translatable string, one entry per locale, with shell
commands and code blocks (e.g. the Rosetta setup scripts) shared verbatim across all locales rather than
retyped. `i18n/render_*.py` assemble the actual HTML from those dicts plus the shared header/footer/nav/
hreflang scaffolding in `i18n/gen_locales.py`.

**To change site copy:**
1. Edit the relevant field in `i18n/content_home.py` / `content_privacy.py` / `content_support.py` — for
   the English page, edit the `"en"` entry; for a translation, edit that locale's entry directly. (Don't
   hand-edit the generated HTML files — a rebuild will overwrite them.)
2. Run `python3 i18n/build.py` from the repo root. This regenerates all 30 pages (+ 10 404 pages) and
   `sitemap.xml`.
3. Diff the result, then commit both the `content_*.py` change and the regenerated HTML together.

**To add an 11th locale:** add an entry to `LOCALES` in `i18n/gen_locales.py` (BCP-47 code, URL segment,
native display name), add a matching entry to every dict in the three `content_*.py` files (same keys as
`"en"`) and to `render_404.py`'s `NOTFOUND` dict, then run `i18n/build.py`.

Each page's `<head>` carries `hreflang` alternate links to every locale variant plus `x-default` (pointing
at English), and a `<details class="lang-switch">` menu in the header lets visitors jump between locales
of the current page — no JavaScript required, consistent with the rest of the site.

## Deploying on Cloudflare (Workers static assets)

This repo is connected as a **Cloudflare Workers** project (static assets, no worker code) rather than
classic Pages — that's what Cloudflare's dashboard provisioned when the repo was connected, and
`wrangler.jsonc` in this repo matches it. The build step Cloudflare runs is:

```
npx wrangler deploy
```

That's it — no separate build command, `assets.directory` in `wrangler.jsonc` is `.` (the repo root).
Every push to the connected branch redeploys automatically.

**Important:** because the assets directory is the repo root, `wrangler deploy` would otherwise upload
`.git/` itself as public, downloadable static assets. `.assetsignore` (gitignore-style syntax) excludes it,
along with this README and the wrangler/git config files — don't remove that file.

### Routing www and the apex domain

This site is entirely built around `www.veloworkspaces.com` (see the canonical URLs throughout). The apex
(`veloworkspaces.com`) should 301 to it — done as a zone-level Redirect Rule, not a Custom Domain, so there's
exactly one thing that can ever handle apex traffic (no need to reason about Redirect Rules vs. Custom
Domain precedence):

1. **DNS** for the `veloworkspaces.com` zone → add a placeholder record for the bare apex, proxied:
   - `A`, name `@` (or `veloworkspaces.com`), address `192.0.2.1`, Proxy status **Proxied**
   - Optionally also `AAAA`, name `@`, address `2001:DB8::1`, **Proxied**

   These are IANA-reserved documentation addresses — Cloudflare's own recommended placeholder for exactly
   this case. The address is never actually contacted; it only needs to exist so Cloudflare's edge sees and
   proxies apex requests at all, for the Redirect Rule below to have something to fire on. Do this *before*
   the next step, so there's no gap where the apex has no record at all.
2. Cloudflare dashboard → **Workers & Pages** → the `veloworkspaces-website` worker → **Settings → Domains &
   Routes** → add **only** `www.veloworkspaces.com` as a Custom Domain. Do **not** add the bare apex here —
   the whole point of this setup is that the Redirect Rule is the only thing that can ever answer for it.
3. **Rules → Redirect Rules → Create rule**, at the zone level:
   - When incoming requests match: **Hostname equals `veloworkspaces.com`**
   - Then: **Dynamic**, expression `concat("https://www.veloworkspaces.com", http.request.uri.path)`,
     status code **301**, preserve query string on
4. Verify: `curl -I https://veloworkspaces.com/` should return `301` with
   `location: https://www.veloworkspaces.com/`.
5. Enable **Always Use HTTPS** (SSL/TLS settings for the zone) if it isn't already on.

## Updating the App Store link

The app is still in App Store review, so `assets/app-store.js` currently points every download button at
Apple's App Store homepage as a safe placeholder. Once the app is approved:

1. Open `assets/app-store.js`.
2. Replace the `APP_STORE_URL` value with the real listing URL.
3. Commit and push — every button on every page updates from that one change.

(Each button also has a static fallback `href` baked into the HTML for no-JS visitors and crawlers; you can
leave those as-is, or update them to match once you're touching the file anyway.)

## Adding the real app icon

Every page currently references one file for both the browser-tab favicon and the small logo mark next to
"Velo Workspaces" in the header and footer:

- **Path:** `assets/icon.png`
- **Size:** **512×512px**, PNG, square. This matches the `icon_512x512@1x` (or `icon_256x256@2x`) export in
  a standard Xcode `AppIcon.appiconset`, so you can very likely drop in an existing export from the app's own
  asset catalog without resizing anything.

Just replace the file at that path with the real icon — nothing in the HTML/CSS needs to change, since every
page already points at `assets/icon.png` for both the `<link rel="icon">` favicon and the `<img class="mark">`
brand mark (displayed at 28×28, so 512px gives plenty of headroom for Retina displays without looking soft).

## Adding real screenshots to the home page

The home page hero currently shows four solid, accent-tinted placeholder tiles (a 2×2 grid, one per persona)
in place of real screenshots. Each tile is just an `<img>` waiting for a file — add these four, at these
exact paths, and the placeholders are replaced automatically, no HTML changes needed:

| Path                                            | Persona            | Suggested screen                          |
|--------------------------------------------------|---------------------|--------------------------------------------|
| `assets/screenshots/software-engineers.png`      | Software Engineers  | A workspace detail view, Code & Build profile |
| `assets/screenshots/ai-researchers.png`          | AI Researchers      | The AI Bridge tab, connected to a local model |
| `assets/screenshots/devops-professionals.png`    | DevOps Professionals| DevOps Lab workspace / serial console      |
| `assets/screenshots/qa-engineers.png`            | QA Engineers        | A Disposable Workspace, or the base image library |

**Size:** they don't need to be pixel-exact — the CSS crops each image to an 8:5 (16:10) tile with
`object-fit: cover`, anchored to the top, so any reasonably close landscape screenshot works without editing.
A screenshot captured at **1440×900** fits that tile exactly with zero cropping; **1440×846** (the other size
these have been captured at) is close enough that `cover` only trims a sliver off the sides — not enough to
plausibly cut into a sidebar or toolbar. Keep them as PNG (not JPEG) so UI text and window edges stay sharp.

They're plenty sharp to use straight from a 1440-wide capture — no resizing required — but each one renders
at roughly 380–450px wide on the actual page, so a 1440px-wide PNG is 3-4× larger than it needs to be
(slower page load for no visible benefit). If you want to trim that: downscale to around **960×600** (same
8:5 ratio, 2× the display size for Retina sharpness) with any image tool (`sips -Z 960 in.png --out out.png`
on macOS, Preview's Export, etc.) before dropping them in.

The suggested screen per persona is just that — a suggestion. Use whatever actually shows that persona's
workflow best.

## Adding a social preview image

Each page's `<head>` has a commented-out `og:image` / `twitter:card` block. Once you have a 1200×630 image
(e.g. `assets/og-image.png`), drop it in and uncomment those tags in `index.html`, `privacy/index.html`, and
`support/index.html`.

## Local preview

No build tooling needed — any static file server works:

```sh
python3 -m http.server 8080
# or: npx serve .
```

Then open `http://localhost:8080`.

## Content ownership

Site copy should stay in sync with the App Store listing description and the app's actual feature set —
in particular the guest OS list, Rosetta instructions, and shared-folder/clipboard behavior in
`support/index.html`, since those describe exact in-app mechanics rather than general marketing claims.
