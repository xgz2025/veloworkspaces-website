#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-time authoring script that generates the localized static pages for
veloworkspaces-website. Output is plain static HTML committed to the repo —
this script is not part of the deployed site and is not run at request time.
"""
import os

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

LOCALES = [
    # code (BCP-47, used in lang= / hreflang),  url segment,           native label
    ("zh-Hans", "zh-hans", "简体中文"),
    ("zh-Hant", "zh-hant", "繁體中文"),
    ("fr",      "fr",      "Français"),
    ("de",      "de",      "Deutsch"),
    ("it",      "it",      "Italiano"),
    ("ja",      "ja",      "日本語"),
    ("ko",      "ko",      "한국어"),
    ("pt-BR",   "pt-br",   "Português (Brasil)"),
    ("es",      "es",      "Español"),
]
EN = ("en", "", "English")
ALL_LOCALES = [EN] + LOCALES

def url_for(seg, path):
    """path is '' for home, 'privacy/' or 'support/' for the other pages."""
    if seg == "":
        return f"/{path}"
    return f"/{seg}/{path}"

def lang_switch_html(seg_here, path, current_code):
    """<details> dropdown with links to the same page in every locale."""
    items = []
    for code, seg, label in ALL_LOCALES:
        href = url_for(seg, path)
        current = ' aria-current="true"' if code == current_code else ""
        items.append(f'          <li><a href="{href}" hreflang="{code}"{current}>{label}</a></li>')
    items_html = "\n".join(items)
    cur_label = dict((c, l) for c, s, l in ALL_LOCALES)[current_code]
    return f'''<details class="lang-switch">
        <summary><span class="lang-switch-label">{cur_label}</span> <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg></summary>
        <ul class="lang-menu">
{items_html}
        </ul>
      </details>'''

def hreflang_tags(path):
    lines = []
    for code, seg, label in ALL_LOCALES:
        href = f"https://www.veloworkspaces.com{url_for(seg, path)}"
        lines.append(f'<link rel="alternate" hreflang="{code}" href="{href}">')
    # x-default -> English
    lines.append(f'<link rel="alternate" hreflang="x-default" href="https://www.veloworkspaces.com/{path}">')
    return "\n".join(lines)

def nav_prefix(seg):
    """Root-relative prefix for same-site links, '' for English, '/xx' for others."""
    return "" if seg == "" else f"/{seg}"

if __name__ == "__main__":
    print("locale registry ready:", [l[0] for l in ALL_LOCALES])
