# veloworkspaces.com

Marketing site, blog, roadmap, privacy policy and support/FAQ for [Velo Workspaces](https://www.veloworkspaces.com).

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
roadmap/index.html  Roadmap (English only, hand-written)    → served at /roadmap/
blog/               Blog (English only): index.html, feed.xml (RSS), one folder per post
404.html            Not-found page
de/ fr/ it/ es/ pt-br/ ja/ ko/ zh-hans/ zh-hant/
                     Same three pages + 404, per locale     → served at /<locale>/, /<locale>/privacy/, etc.
i18n/                Authoring scripts that generate every localized page — see "Localization" below
robots.txt
sitemap.xml          Generated: every localized page with hreflang alternates, plus the roadmap and every blog post, all with <lastmod>
_redirects          Cloudflare Workers assets: path-level redirects (old blog PNG URLs → their WebP versions)
_headers            Cloudflare Workers assets: security + cache headers
wrangler.jsonc      Deploy config (Workers static assets, no worker code)
.assetsignore       Keeps .git, this README, i18n/, etc. out of the deployed assets
assets/style.css    All styling
assets/app-store.js Fills in every [data-app-store-link] button's href from one place
assets/lightbox.js  Opens a blog screenshot full size in a <dialog> (loaded only by posts that have them)
assets/icon.png     App icon — used as both the favicon and the header/footer brand mark
assets/screenshots/ Four app screenshots shown in the home page hero (WebP served, PNG kept as source)
assets/og/          1200×630 share images: default.jpg plus one per blog post (generated, see "Blog")
assets/blog/        Images used inside blog posts (WebP); assets/blog/guides/ holds the step-by-step guides'
                     screenshots and the 30-second screen recording
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

## Blog

The blog is English only. Each post's **body** is hand-written HTML inside
`<div class="container article-body">` in `blog/<slug>/index.html`. Everything around the body is
generated from `i18n/blog_posts.py` by `i18n/render_blog.py`: the `<head>` (title, meta description,
canonical, Open Graph and Twitter tags, `BlogPosting` + `BreadcrumbList` JSON-LD), the site header, the
article header (eyebrow, h1, lede, byline with dates) and the footer. It also writes `blog/index.html`
(grouped cards, `Blog` JSON-LD) and `blog/feed.xml` (RSS).

`i18n/blog_posts.py` has one entry per post, in index order, grouped by `GROUPS`:

| Field | Used for | Guideline |
|---|---|---|
| `title` | `<title>`, og:title, search results | Under 60 characters, lead with what people search for |
| `description` | meta description, og:description, RSS | 120–155 characters |
| `h1` | The heading on the page | Can be longer than `title` |
| `card_title`, `card_summary` | The card on the blog index | |
| `lede` | The paragraph under the h1 (HTML allowed) | |
| `published`, `modified` | Byline, JSON-LD, sitemap `<lastmod>`, RSS | ISO dates; bump `modified` on real edits |
| `trademarks` | Extra trademark line in the footer | |
| `hero` *(optional)* | `{"src", "alt"}`: a screenshot under the byline, the post's card thumbnail on the blog index, and the inset on its share image | Guides have one |
| `video` *(optional)* | `{"name", "description", "src", "poster", "uploaded", "duration"}`: `VideoObject` JSON-LD for a recording in the body | |
| `toc` *(optional)* | `"open"` shows the table of contents expanded. Posts with five or more `h2`s get a collapsed one anyway | Guides use `"open"` |

The renderer also gives every `h2` in a body an `id` (kept if it already has one) for the table of
contents, adds the reading time to the byline, and loads `assets/lightbox.js` on posts with screenshots.

**Guide components** (all in `assets/style.css`): `figure.shot` with an `a.shot-frame` around the image is
a framed, zoomable screenshot (`shot-wide` lets it overhang the text column, `shot-narrow` keeps a small
one small, `div.shot-pair` sets two side by side); `div.guide-steps` holding `section.guide-step`s, each
starting with an `h2`, gives numbered step badges; `div.note` with `note-tip`, `note-pro` or `note-warn` is
a callout; `dl.guide-facts` is the "at a glance" box; `div.guide-next` is a row of link cards. Give every
`img` its `width` and `height` and `loading="lazy"`. Screenshots are WebP, cropped to what the step is
about, with an orange ring on the control to click.

**To add a post:** copy an existing post's folder, replace the body, add its entry to `POSTS`, then run
`python3 i18n/make_og_images.py <slug>` (its share image) and `python3 i18n/build.py`.
`render_blog.py` refuses to run if a folder in `blog/` has no entry or an entry has no folder.

**Share images** (`assets/og/`): `python3 i18n/make_og_images.py` renders `default.jpg` and one card per
post from its eyebrow and `card_title` (and its `hero` screenshot, when it has one), using Node +
Playwright (`npm i -g playwright`). Re-run it for a post whenever its `card_title` or `hero` changes.

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

`assets/app-store.js` holds the listing URL (`APP_STORE_URL`) that every download button uses. To change it:

1. Open `assets/app-store.js`.
2. Replace the `APP_STORE_URL` value.
3. Commit and push — every button on every page updates from that one change.

(Each button also has a static fallback `href` baked into the HTML for no-JS visitors and crawlers; you can
leave those as-is, or update them to match once you're touching the file anyway.)

## App icon

`assets/icon.png` (512×512 PNG) is both the favicon and the brand mark in the header and footer. Replace
the file to change it; nothing in the HTML needs to change.

## Home page screenshots

The hero shows four screenshots, one per persona: `assets/screenshots/{software-engineers,ai-researchers,
devops-professionals,qa-engineers}`. The pages load the `.webp` files (960 px wide, about 60 KB each); the
`.png` files are the full-size sources. The CSS crops each to 8:5 with `object-fit: cover`, anchored to the
top, so capture at 1440×900 and convert with, for example:

```sh
sips -Z 960 in.png --out tmp.png && cwebp -q 82 tmp.png -o assets/screenshots/qa-engineers.webp
```

## Social preview images

Every page has `og:image` and `twitter:card` tags. Home, support, privacy, the roadmap and the blog index use
`assets/og/default.jpg`; each blog post uses `assets/og/<slug>.jpg`. See "Blog" for regenerating them.

## Local preview

No build tooling needed — any static file server works:

```sh
python3 -m http.server 8080
# or: npx serve .
```

Then open `http://localhost:8080`.

## Content ownership

Site copy should stay in sync with the App Store listing description and the app's actual feature set —
in particular the guest OS list, the cloud image and automatic-install lists, Free vs. Pro, the SSH/Access
tab behavior, Rosetta instructions and shared-folder/clipboard behavior in the support FAQ and the blog's
OS guides, since those describe exact in-app mechanics rather than general marketing claims. UI names
quoted in localized pages (Settings › Images, Access, Open Terminal…) come from the app's
`Localizable.xcstrings`; keep them matching. Windows guests are not supported and must not be presented
as available.
