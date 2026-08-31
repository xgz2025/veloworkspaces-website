# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_locales import ALL_LOCALES, url_for, lang_switch_html, hreflang_tags, nav_prefix
from content_privacy import PRIVACY

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PATH = "privacy/"

def render(code, seg, label):
    t = PRIVACY[code]
    p = nav_prefix(seg)
    canonical = f"https://www.veloworkspaces.com{url_for(seg, PATH)}"
    switcher = lang_switch_html(seg, PATH, code)
    hreflang = hreflang_tags(PATH)

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
        <a href="{p}/support/">{t['nav_support']}</a>
      </span>
      {switcher}
      <a class="btn btn-primary" data-app-store-link href="https://apps.apple.com/">{t['nav_download']}</a>
    </nav>
  </div>
</header>

<main id="main">
  <section class="section">
    <div class="container prose">
      <span class="eyebrow">{t['eyebrow']}</span>
      <h1>{t['h1']}</h1>
      <p class="updated">{t['updated']}</p>

      <p><strong>{t['intro_strong']}</strong> {t['intro']}</p>

      <h2>{t['h2_1']}</h2>
      <p>{t['p_1']}</p>

      <h2>{t['h2_2']}</h2>
      <p>{t['p_2']}</p>

      <h2>{t['h2_3']}</h2>
      <p>{t['p_3']}</p>
      <ul>
        <li><strong>{t['li_3a_strong']}</strong>{t['li_3a']}</li>
        <li><strong>{t['li_3b_strong']}</strong>{t['li_3b']}</li>
      </ul>
      <p>{t['p_3b']}</p>

      <h2>{t['h2_4']}</h2>
      <p>{t['p_4']} <strong>{t['p_4_strong']}</strong> {t['p_4b']}</p>

      <h2>{t['h2_5']}</h2>
      <p>{t['p_5']}</p>
      <ul>
        <li><strong>{t['li_5a_strong']}</strong>{t['li_5a']}</li>
        <li><strong>{t['li_5b_strong']}</strong>{t['li_5b']}</li>
      </ul>
      <p>{t['p_5b']}</p>

      <h2>{t['h2_6']}</h2>
      <p>{t['p_6']}</p>

      <h2>{t['h2_7']}</h2>
      <p>{t['p_7']}</p>

      <h2>{t['h2_8']}</h2>
      <p>{t['p_8']}</p>

      <h2>{t['h2_9']}</h2>
      <p>{t['p_9']} <a href="mailto:support@veloworkspaces.com">support@veloworkspaces.com</a>.</p>
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

<script src="/assets/app-store.js?v=2"></script>
</body>
</html>
'''
    return html

def write_all():
    for code, seg, label in ALL_LOCALES:
        d = os.path.join(REPO, seg, "privacy") if seg else os.path.join(REPO, "privacy")
        os.makedirs(d, exist_ok=True)
        out_path = os.path.join(d, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render(code, seg, label))
        print("wrote", out_path)

if __name__ == "__main__":
    write_all()
