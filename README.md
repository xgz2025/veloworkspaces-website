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
_redirects          Cloudflare Pages: apex → www redirect
_headers            Cloudflare Pages: security + cache headers
assets/style.css    All styling
assets/app-store.js Fills in every [data-app-store-link] button's href from one place
assets/favicon.svg
```

## Deploying on Cloudflare Pages

1. In the Cloudflare dashboard: **Workers & Pages → Create → Pages → Connect to Git**, and select this
   repository (`xgz2025/veloworkspaces-website`).
2. Build settings — this site has no build step:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `/`
3. Deploy. Cloudflare will build and serve the site on a `*.pages.dev` URL immediately.
4. **Custom domain:** in the Pages project → **Custom domains**, add both:
   - `www.veloworkspaces.com` (the canonical domain used throughout this site)
   - `veloworkspaces.com` (the apex — needed so `_redirects` can 301 it to `www`)

   If `veloworkspaces.com` is already on Cloudflare DNS (orange-clouded / proxied), adding it as a custom
   domain here is usually enough — Cloudflare manages the DNS record for you. If it's on a different
   registrar/DNS provider, point it at Cloudflare per Cloudflare's own custom-domain instructions for Pages.
5. Enable **Always Use HTTPS** (Cloudflare's SSL/TLS settings) if it isn't already on for the zone.

Every push to the connected branch redeploys automatically — no CI to maintain here.

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
