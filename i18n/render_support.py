# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from gen_locales import ALL_LOCALES, url_for, lang_switch_html, hreflang_tags, nav_prefix
from content_support import SUPPORT

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PATH = "support/"

def render(code, seg, label):
    t = SUPPORT[code]
    p = nav_prefix(seg)
    canonical = f"https://www.veloworkspaces.com{url_for(seg, PATH)}"
    switcher = lang_switch_html(seg, PATH, code)
    hreflang = hreflang_tags(PATH)

    # FAQPage JSON-LD — plain text answers (not translated HTML), same 6 Q&A as English source.
    faq_entries = [
        (t['ld_shared_q'], t['ld_shared_a']),
        (t['ld_clip_q'], t['ld_clip_a']),
        (t['ld_deb_q'], t['ld_deb_a']),
        (t['ld_fed_q'], t['ld_fed_a']),
        (t['ld_disp_q'], t['ld_disp_a']),
        (t['ld_win_q'], t['ld_win_a']),
    ]
    main_entity = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in faq_entries
    ]
    ld_json = json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": main_entity},
        ensure_ascii=False, indent=2,
    )

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

<script type="application/ld+json">
{ld_json}
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
        <a href="{p}/support/">{t['nav_support']}</a>
      </span>
      {switcher}
      <a class="btn btn-primary" data-app-store-link href="https://apps.apple.com/app/velo-workspaces/id6805509975">{t['nav_download']}</a>
    </nav>
  </div>
</header>

<main id="main">

  <section class="section" style="padding-bottom:32px;">
    <div class="container">
      <span class="eyebrow">{t['eyebrow']}</span>
      <h1>{t['h1']}</h1>
      <p style="max-width:60ch;">{t['intro_pre']} <a href="mailto:support@veloworkspaces.com">support@veloworkspaces.com</a> {t['intro_post']}</p>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="container">
      <h2>{t['gs_h2']}</h2>

      <div class="card" style="margin-bottom:24px;">
        <h3>{t['gs1_h3']}</h3>
        <ol class="steps" style="margin-top:20px;">
          <li>
            <div>
              <h3>{t['gs1_s1_h']}</h3>
              <p>{t['gs1_s1_p']}</p>
            </div>
          </li>
          <li>
            <div>
              <h3>{t['gs1_s2_h']}</h3>
              <p>{t['gs1_s2_p']}</p>
            </div>
          </li>
          <li>
            <div>
              <h3>{t['gs1_s3_h']}</h3>
              <p>{t['gs1_s3_p']}</p>
            </div>
          </li>
        </ol>
      </div>

      <div class="card">
        <h3>{t['gs2_h3']}</h3>
        <ol class="steps" style="margin-top:20px;">
          <li>
            <div>
              <h3>{t['gs2_s1_h']}</h3>
              <p>{t['gs2_s1_p']}</p>
            </div>
          </li>
          <li>
            <div>
              <h3>{t['gs2_s2_h']}</h3>
              <p>{t['gs2_s2_p']}</p>
            </div>
          </li>
          <li>
            <div>
              <h3>{t['gs2_s3_h']}</h3>
              <p>{t['gs2_s3_p']}</p>
            </div>
          </li>
        </ol>
      </div>
    </div>
  </section>

  <section class="section section-alt">
    <div class="container">
      <h2 style="margin-bottom:32px;">{t['faq_h2']}</h2>

      <div class="faq-group">
        <h2>{t['faq_shared_h2']}</h2>
        <details class="faq-item">
          <summary>{t['faq_shared_q']}</summary>
          <div class="faq-answer">
            <p><strong>{t['faq_shared_a1_strong']}</strong>{t['faq_shared_a1']} <code>{t['faq_shared_a1_code']}</code>{t['faq_shared_a1b']}</p>
            <p><strong>{t['faq_shared_a2_strong']}</strong>{t['faq_shared_a2']}</p>
            <pre><code>{t['faq_shared_code']}</code></pre>
            <p>{t['faq_shared_a3']}</p>
          </div>
        </details>
      </div>

      <div class="faq-group">
        <h2>{t['faq_clip_h2']}</h2>
        <details class="faq-item">
          <summary>{t['faq_clip_q']}</summary>
          <div class="faq-answer">
            <p>{t['faq_clip_a1']}</p>
            <ol>
              <li>{t['faq_clip_li1_pre']} <strong>{t['faq_clip_li1_strong']}</strong> {t['faq_clip_li1_post']}</li>
              <li>{t['faq_clip_li2_pre']} <code>{t['faq_clip_li2_code_inline']}</code> {t['faq_clip_li2_post']}
                <pre><code>{t['faq_clip_li2_code']}</code></pre>
              </li>
              <li>{t['faq_clip_li3_pre']}
                <pre><code>{t['faq_clip_li3_code']}</code></pre>
                {t['faq_clip_li3_post_pre']} <code>{t['faq_clip_li3_code_inline']}</code>{t['faq_clip_li3_post']}
              </li>
              <li>{t['faq_clip_li4']} <code>{t['faq_clip_li4_code']}</code> {t['faq_clip_li4_post']}</li>
            </ol>
            <p>{t['faq_clip_a2']}</p>
          </div>
        </details>
      </div>

      <div class="faq-group">
        <h2>{t['faq_rosetta_h2']}</h2>
        <details class="faq-item">
          <summary>{t['faq_rosetta_deb_q']}</summary>
          <div class="faq-answer">
            <p>{t['faq_rosetta_deb_a_pre']} <code>{t['faq_rosetta_deb_a_code1']}</code> {t['faq_rosetta_deb_a_mid']} <code>{t['faq_rosetta_deb_a_code2']}</code> {t['faq_rosetta_deb_a_post']}</p>
            <pre><code>{t['faq_rosetta_deb_code']}</code></pre>
          </div>
        </details>
        <details class="faq-item">
          <summary>{t['faq_rosetta_fed_q']}</summary>
          <div class="faq-answer">
            <p>{t['faq_rosetta_fed_a_pre']} <code>{t['faq_rosetta_fed_a_code1']}</code> {t['faq_rosetta_fed_a_mid']} <code>{t['faq_rosetta_fed_a_code2']}</code>{t['faq_rosetta_fed_a_post']} <code>{t['faq_rosetta_fed_a_code3']}</code> {t['faq_rosetta_fed_a_post2']}</p>
            <pre><code>{t['faq_rosetta_fed_code']}</code></pre>
            <p>{t['faq_rosetta_fed_note_pre']} <code>{t['faq_rosetta_fed_note_code']}</code> {t['faq_rosetta_fed_note_post']}</p>
          </div>
        </details>
      </div>

      <div class="faq-group">
        <h2>{t['faq_aib_h2']}</h2>
        <details class="faq-item">
          <summary>{t['faq_aib_q']}</summary>
          <div class="faq-answer">
            <ol>
              <li>{t['faq_aib_li1']}</li>
              <li>{t['faq_aib_li2']}</li>
              <li>{t['faq_aib_li3']}</li>
              <li>{t['faq_aib_li4']}</li>
            </ol>
          </div>
        </details>
      </div>

      <div class="faq-group">
        <h2>{t['faq_disp_h2']}</h2>
        <details class="faq-item">
          <summary>{t['faq_disp1_q']}</summary>
          <div class="faq-answer">
            <p>{t['faq_disp1_a']}</p>
          </div>
        </details>
        <details class="faq-item">
          <summary>{t['faq_disp2_q']}</summary>
          <div class="faq-answer">
            <p>{t['faq_disp2_a_pre']} <strong>{t['faq_disp2_a_strong']}</strong> {t['faq_disp2_a_post']}</p>
          </div>
        </details>
        <details class="faq-item">
          <summary>{t['faq_disp3_q']}</summary>
          <div class="faq-answer">
            <p>{t['faq_disp3_a_pre']} <code>{t['faq_disp3_a_code']}</code> {t['faq_disp3_a_post']}</p>
          </div>
        </details>
      </div>

      <div class="faq-group">
        <h2>{t['faq_gen_h2']}</h2>
        <details class="faq-item">
          <summary>{t['faq_gen1_q']}</summary>
          <div class="faq-answer">
            <p>{t['faq_gen1_a']}</p>
          </div>
        </details>
        <details class="faq-item">
          <summary>{t['faq_gen2_q']}</summary>
          <div class="faq-answer">
            <p>{t['faq_gen2_a']}</p>
          </div>
        </details>
        <details class="faq-item">
          <summary>{t['faq_gen3_q']}</summary>
          <div class="faq-answer">
            <p>{t['faq_gen3_a']}</p>
          </div>
        </details>
      </div>
    </div>
  </section>

  <section class="section" style="text-align:center;">
    <div class="container">
      <h2>{t['stuck_h2']}</h2>
      <p style="max-width:52ch; margin:0 auto 20px;">{t['stuck_p']}</p>
      <a class="btn btn-primary" href="mailto:support@veloworkspaces.com">support@veloworkspaces.com</a>
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
        d = os.path.join(REPO, seg, "support") if seg else os.path.join(REPO, "support")
        os.makedirs(d, exist_ok=True)
        out_path = os.path.join(d, "index.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render(code, seg, label))
        print("wrote", out_path)

if __name__ == "__main__":
    write_all()
