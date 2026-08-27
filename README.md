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
assets/icon.png     App icon — used as both the favicon and the header/footer brand mark
assets/screenshots/ Four app screenshots shown in the home page hero (see below)
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

**Size:** **1600×1200px (4:3), PNG**, for each. They don't need to be pixel-exact — the CSS crops each image
to a 4:3 tile with `object-fit: cover`, cropped from the top — but aim for landscape screenshots close to
that ratio so the crop doesn't cut off anything important, and keep them as PNG (not JPEG) so UI text and
edges stay sharp. Take them at a Retina/2× resolution and downscale to 1600×1200 if needed — that's plenty
sharp for the roughly 380–400px-wide tile these render at on a real page, without shipping an oversized file.

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
