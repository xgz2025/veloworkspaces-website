# veloworkspaces.com

Marketing site, privacy policy, and support/FAQ page for [Velo Workspaces](https://www.veloworkspaces.com).

Plain static HTML + CSS. No framework, no build step, no JavaScript beyond one small script that fills in
the App Store download link. This is deliberate — it keeps the site fast, dependency-free, and easy for
search engines to crawl.

## Structure

```
index.html          Home / marketing page
privacy/index.html  Privacy policy       → served at /privacy/
support/index.html  Support & FAQ        → served at /support/
404.html            Not-found page
robots.txt
sitemap.xml
_redirects          Cloudflare Workers assets: path-level redirects (none active — see below)
_headers            Cloudflare Workers assets: security + cache headers
wrangler.jsonc      Deploy config (Workers static assets, no worker code)
.assetsignore       Keeps .git, this README, etc. out of the deployed assets
assets/style.css    All styling
assets/app-store.js Fills in every [data-app-store-link] button's href from one place
assets/favicon.svg
```

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

This site is entirely built around `www.veloworkspaces.com` (see the canonical URLs throughout). To make
that live:

1. Cloudflare dashboard → **Workers & Pages** → the `veloworkspaces-website` worker → **Settings → Domains
   & Routes → Add → Custom Domain** → enter `www.veloworkspaces.com`. Cloudflare provisions the DNS record
   for you as long as `veloworkspaces.com` is already an active zone on this Cloudflare account.
2. For `veloworkspaces.com` (the bare apex), **don't** add it as a second Custom Domain on this worker —
   redirecting it to `www` has to happen *before* a request would ever reach the worker, and Workers-assets
   `_redirects` can't express a cross-hostname redirect (it only accepts relative-path sources; that's what
   failed the first deploy attempt). Instead, at the zone level: **veloworkspaces.com → Rules → Redirect
   Rules → Create rule**:
   - When incoming requests match: **Hostname equals `veloworkspaces.com`**
   - Then: **Dynamic**, target `concat("https://www.veloworkspaces.com", http.request.uri.path)`,
     status code **301**, preserve query string on.
   - This needs an A/AAAA (or CNAME) record for the bare apex pointed at Cloudflare (proxied/orange-clouded)
     for the rule to ever see the request — add a proxied placeholder record for `veloworkspaces.com` in DNS
     if one doesn't already exist.
3. Enable **Always Use HTTPS** (SSL/TLS settings for the zone) if it isn't already on.

## Updating the App Store link

The app is still in App Store review, so `assets/app-store.js` currently points every download button at
Apple's App Store homepage as a safe placeholder. Once the app is approved:

1. Open `assets/app-store.js`.
2. Replace the `APP_STORE_URL` value with the real listing URL.
3. Commit and push — every button on every page updates from that one change.

(Each button also has a static fallback `href` baked into the HTML for no-JS visitors and crawlers; you can
leave those as-is, or update them to match once you're touching the file anyway.)

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
