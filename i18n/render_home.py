# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_locales import ALL_LOCALES, url_for, lang_switch_html, hreflang_tags, nav_prefix
from content_home import HOME

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def store_button(t, extra_style=""):
    style_attr = f' style="{extra_style}"' if extra_style else ""
    return f'''<a class="btn btn-store" data-app-store-link href="https://apps.apple.com/app/velo-workspaces/id6805509975"{style_attr}>
            <svg class="btn-store-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M16.365 1.43c0 1.14-.415 2.198-1.244 3.176-.995 1.164-2.197 1.838-3.5 1.732a3.72 3.72 0 0 1-.028-.46c0-1.09.475-2.253 1.32-3.204.42-.483.955-.885 1.604-1.206.648-.316 1.26-.49 1.834-.518.018.16.014.32.014.48zm4.29 16.61c-.31.716-.677 1.377-1.103 1.988-.582.835-1.06 1.412-1.427 1.73-.568.51-1.176.772-1.827.788-.468 0-1.032-.133-1.688-.403-.658-.27-1.263-.403-1.816-.403-.58 0-1.202.133-1.869.403-.667.27-1.205.41-1.617.424-.625.027-1.246-.242-1.865-.808-.397-.345-.897-.944-1.5-1.797-.647-.912-1.18-1.97-1.598-3.177-.448-1.302-.673-2.563-.673-3.784 0-1.398.302-2.605.907-3.618a5.33 5.33 0 0 1 1.902-1.94 5.11 5.11 0 0 1 2.573-.727c.497 0 1.148.154 1.958.457.807.304 1.325.458 1.552.458.169 0 .747-.18 1.729-.539.93-.332 1.716-.47 2.36-.415 1.744.14 3.055.827 3.928 2.066-1.56.945-2.333 2.269-2.318 3.966.014 1.322.492 2.423 1.432 3.298.427.405.903.719 1.432.943-.115.334-.237.654-.366.962z"/>
            </svg>
            <span class="btn-store-text"><small>{t['store_soon']}</small><strong>{t['store_name']}</strong></span>
          </a>'''

def check_svg():
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>'

def arrow_svg():
    return '<svg class="benchmark-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'

def render(code, seg, label):
    t = HOME[code]
    p = nav_prefix(seg)  # '' for en, '/xx' otherwise
    canonical = f"https://www.veloworkspaces.com{url_for(seg, '')}"
    switcher = lang_switch_html(seg, "", code)
    hreflang = hreflang_tags("")

    og_image_block = '''<!-- TODO: add /assets/og-image.png (1200x630) and uncomment once it exists.
<meta property="og:image" content="https://www.veloworkspaces.com/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
-->'''

    html = f'''<!doctype html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['meta_description']}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" href="/assets/icon.png">
<link rel="stylesheet" href="/assets/style.css?v=2">
{hreflang}

<meta property="og:type" content="website">
<meta property="og:site_name" content="Velo Workspaces">
<meta property="og:title" content="{t['og_title']}">
<meta property="og:description" content="{t['og_description']}">
<meta property="og:url" content="{canonical}">
{og_image_block}
<meta name="twitter:title" content="{t['og_title']}">
<meta name="twitter:description" content="{t['og_description']}">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Velo Workspaces",
  "operatingSystem": "macOS",
  "applicationCategory": "DeveloperApplication",
  "description": "{t['ld_description']}",
  "url": "{canonical}",
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }}
}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="container">
    <a class="brand" href="{p}/">
      <img class="mark" src="/assets/icon.png" width="28" height="28" alt="Velo Workspaces">
      Velo Workspaces
    </a>
    <nav class="site-nav" aria-label="Primary">
      <span class="nav-links">
        <a href="{p}/#personas">{t['nav_who']}</a>
        <a href="{p}/#features">{t['nav_features']}</a>
        <a href="{p}/#pricing">{t['nav_pricing']}</a>
        <a href="{p}/support/">{t['nav_support']}</a>
      </span>
      {switcher}
      <a class="btn btn-primary" data-app-store-link href="https://apps.apple.com/app/velo-workspaces/id6805509975">{t['nav_download']}</a>
    </nav>
  </div>
</header>

<main id="main">

  <section class="hero">
    <div class="container hero-grid">
      <div>
        <span class="eyebrow">{t['eyebrow_silicon']}</span>
        <h1>{t['h1']}</h1>
        <p style="font-size:1.15rem; color:var(--color-text-secondary); max-width:52ch;">
          {t['hero_p']}
        </p>
        <div class="hero-actions">
          {store_button(t)}
          <a class="btn btn-outline" href="#personas">{t['hero_cta2']}</a>
        </div>
        <p class="hero-note">{t['hero_note']}</p>
      </div>
      <div class="hero-art">
        <div class="shot-tile" style="--accent: var(--color-accent-swe);">
          <img src="/assets/screenshots/software-engineers.png" alt="{t['shot_swe']}" loading="eager" width="960" height="600">
        </div>
        <div class="shot-tile" style="--accent: var(--color-accent-ai);">
          <img src="/assets/screenshots/ai-researchers.png" alt="{t['shot_ai']}" loading="eager" width="960" height="600">
        </div>
        <div class="shot-tile" style="--accent: var(--color-accent-devops);">
          <img src="/assets/screenshots/devops-professionals.png" alt="{t['shot_devops']}" loading="eager" width="960" height="600">
        </div>
        <div class="shot-tile" style="--accent: var(--color-accent-qa);">
          <img src="/assets/screenshots/qa-engineers.png" alt="{t['shot_qa']}" loading="eager" width="960" height="600">
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="personas">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">{t['personas_eyebrow']}</span>
        <h2>{t['personas_h2']}</h2>
        <p>{t['personas_p']}</p>
      </div>
      <div class="grid grid-4">
        <div class="card persona-card" style="--accent: var(--color-accent-swe);">
          <div class="icon-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="8 6 2 12 8 18"/><polyline points="16 6 22 12 16 18"/></svg>
          </div>
          <h3>{t['p_swe_h']}</h3>
          <p>{t['p_swe_p']}</p>
          <span class="persona-profile">{t['p_swe_tag']}</span>
        </div>
        <div class="card persona-card" style="--accent: var(--color-accent-qa);">
          <div class="icon-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1" stroke-dasharray="2 2"/><path d="M14 3h7v7h-7z"/><path d="M14 14h7v7h-7z"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>
          </div>
          <h3>{t['p_qa_h']}</h3>
          <p>{t['p_qa_p']}</p>
          <span class="persona-profile">{t['p_qa_tag']}</span>
        </div>
        <div class="card persona-card" style="--accent: var(--color-accent-devops);">
          <div class="icon-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
          </div>
          <h3>{t['p_devops_h']}</h3>
          <p>{t['p_devops_p']}</p>
          <span class="persona-profile">{t['p_devops_tag']}</span>
        </div>
        <div class="card persona-card" style="--accent: var(--color-accent-ai);">
          <div class="icon-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="3"/></svg>
          </div>
          <h3>{t['p_ai_h']}</h3>
          <p>{t['p_ai_p']}</p>
          <span class="persona-profile">{t['p_ai_tag']}</span>
        </div>
      </div>
    </div>
  </section>

  <section class="section section-alt" id="features">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">{t['features_eyebrow']}</span>
        <h2>{t['features_h2']}</h2>
      </div>

      <div class="grid" style="gap:24px; margin-bottom:24px;">
        <div class="card feature-card large" style="--accent: var(--color-accent-ai);">
          <div class="icon-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="3"/></svg>
          </div>
          <div>
            <h3>{t['aib_h3']}</h3>
            <p>{t['aib_p']}</p>
            <ul class="feature-list" style="margin-top:16px;">
              <li>{check_svg()} {t['aib_li1']}</li>
              <li>{check_svg()} {t['aib_li2']}</li>
              <li>{check_svg()} {t['aib_li3']}</li>
            </ul>

            <div class="benchmark">
              <p class="benchmark-label">{t['bench_label']}</p>
              <div class="benchmark-row">
                <span class="benchmark-metric">{t['bench_ttft']}</span>
                <span class="benchmark-values">
                  <strong>{t['bench_ttft_native']}</strong> {t['bench_native1']}
                  {arrow_svg()}
                  <strong>{t['bench_ttft_bridge']}</strong> {t['bench_bridge1']}
                </span>
                <span class="benchmark-delta">{t['bench_delta1']}</span>
              </div>
              <div class="benchmark-row">
                <span class="benchmark-metric">{t['bench_tput']}</span>
                <span class="benchmark-values">
                  <strong>{t['bench_tput_native']}</strong> {t['bench_native1']}
                  {arrow_svg()}
                  <strong>{t['bench_tput_bridge']}</strong> {t['bench_bridge1']}
                </span>
                <span class="benchmark-delta">{t['bench_delta2']}</span>
              </div>
              <p class="benchmark-footnote">{t['bench_footnote']}</p>
            </div>
          </div>
        </div>

        <div class="card feature-card large" style="--accent: var(--color-accent-qa);">
          <div class="icon-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1" stroke-dasharray="2 2"/><path d="M14 3h7v7h-7z"/><path d="M14 14h7v7h-7z"/><rect x="3" y="14" width="7" height="7" rx="1"/></svg>
          </div>
          <div>
            <h3>{t['disp_h3']}</h3>
            <p>{t['disp_p']}</p>
            <ul class="feature-list" style="margin-top:16px;">
              <li>{check_svg()} {t['disp_li1']}</li>
              <li>{check_svg()} {t['disp_li2']}</li>
              <li>{check_svg()} {t['disp_li3']}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">{t['integ_eyebrow']}</span>
        <h2>{t['integ_h2']}</h2>
      </div>
      <div class="grid grid-3">
        <div class="card">
          <h3>{t['int_shared_h']}</h3>
          <p>{t['int_shared_p']}</p>
        </div>
        <div class="card">
          <h3>{t['int_ssh_h']}</h3>
          <p>{t['int_ssh_p']}</p>
        </div>
        <div class="card">
          <h3>{t['int_serial_h']}</h3>
          <p>{t['int_serial_p']}</p>
        </div>
        <div class="card">
          <h3>{t['int_clip_h']}</h3>
          <p>{t['int_clip_p']}</p>
        </div>
        <div class="card">
          <h3>{t['int_rosetta_h']}</h3>
          <p>{t['int_rosetta_p']}</p>
        </div>
        <div class="card">
          <h3>{t['int_pause_h']}</h3>
          <p>{t['int_pause_p']}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section section-alt">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">{t['os_eyebrow']}</span>
        <h2>{t['os_h2']}</h2>
        <p>{t['os_p']}</p>
      </div>
      <div class="pill-row" style="justify-content:center;">
        <span class="pill">Ubuntu Desktop</span>
        <span class="pill">Ubuntu Server</span>
        <span class="pill">Debian</span>
        <span class="pill">Fedora Workstation</span>
        <span class="pill">Alpine Linux</span>
        <span class="pill">macOS guests</span>
      </div>
    </div>
  </section>

  <section class="section" id="pricing" style="text-align:center;">
    <div class="container">
      <span class="eyebrow">{t['pricing_eyebrow']}</span>
      <h2>{t['pricing_h2']}</h2>
      <p style="max-width:52ch; margin:0 auto 28px;">{t['pricing_p']}</p>
      {store_button(t, "display:inline-flex;")}
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="callout">
        <div class="icon-badge" style="--accent: var(--color-accent-devops);">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="10" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        </div>
        <div>
          <h2 style="margin-bottom:8px;">{t['callout_h2']}</h2>
          <p>{t['callout_p']} <a href="{p}/privacy/">{t['callout_link']}</a>.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" style="text-align:center;">
    <div class="container">
      <h2>{t['cta_h2']}</h2>
      <p style="max-width:56ch; margin:0 auto 28px;">{t['cta_p']}</p>
      {store_button(t, "display:inline-flex;")}
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <a class="brand" href="{p}/">
        <img class="mark" src="/assets/icon.png" width="28" height="28" alt="Velo Workspaces">
        Velo Workspaces
      </a>
      <nav class="footer-links" aria-label="Footer">
        <a href="{p}/support/">{t['nav_support']}</a>
        <a href="{p}/privacy/">{t['nav_privacy']}</a>
        <a href="mailto:support@veloworkspaces.com">support@veloworkspaces.com</a>
      </nav>
    </div>
    <p class="footer-fine">
      {t['footer_fine']}
    </p>
  </div>
</footer>

<script src="/assets/app-store.js?v=3"></script>
</body>
</html>
'''
    return html

def write_all():
    for code, seg, label in ALL_LOCALES:
        if seg == "":
            out_path = os.path.join(REPO, "index.html")
        else:
            d = os.path.join(REPO, seg)
            os.makedirs(d, exist_ok=True)
            out_path = os.path.join(d, "index.html")
        html = render(code, seg, label)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", out_path)

if __name__ == "__main__":
    write_all()
