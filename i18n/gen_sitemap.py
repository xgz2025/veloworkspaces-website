# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_locales import ALL_LOCALES, url_for

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

PAGES = [
    ("", "weekly", "1.0"),
    ("support/", "weekly", "0.8"),
    ("privacy/", "monthly", "0.3"),
]

# English-only long-form pages with no translations yet — listed without
# hreflang alternates rather than forced through the per-locale PAGES loop,
# which would otherwise emit alternate links to /de/blog/... paths that
# don't exist.
ENGLISH_ONLY_PAGES = [
    ("blog/", "weekly", "0.7"),
    ("blog/debian-on-apple-silicon/", "monthly", "0.6"),
    ("blog/ubuntu-on-apple-silicon/", "monthly", "0.6"),
    ("blog/qa-devops-disposable-vm-workflow/", "monthly", "0.6"),
    ("blog/arm-virtualization-performance/", "monthly", "0.6"),
    ("blog/ai-agent-security-risks/", "monthly", "0.6"),
    ("blog/velo-vs-parallels-vs-utm/", "monthly", "0.6"),
    ("blog/ai-bridge-architecture/", "monthly", "0.6"),
    ("blog/mlx-vm-setup-guide/", "monthly", "0.6"),
    ("blog/vm-inference-benchmark/", "monthly", "0.6"),
    ("blog/zero-tax-virtualization/", "monthly", "0.6"),
    ("blog/vm-sandboxing-cost/", "monthly", "0.6"),
]

def alternates_block(path, indent="    "):
    lines = []
    for code, seg, label in ALL_LOCALES:
        href = f"https://www.veloworkspaces.com{url_for(seg, path)}"
        lines.append(f'{indent}<xhtml:link rel="alternate" hreflang="{code}" href="{href}"/>')
    lines.append(f'{indent}<xhtml:link rel="alternate" hreflang="x-default" href="https://www.veloworkspaces.com/{path}"/>')
    return "\n".join(lines)

def build():
    entries = []
    for path, freq, prio in PAGES:
        for code, seg, label in ALL_LOCALES:
            loc = f"https://www.veloworkspaces.com{url_for(seg, path)}"
            entries.append(
                "  <url>\n"
                f"    <loc>{loc}</loc>\n"
                f"{alternates_block(path)}\n"
                f"    <changefreq>{freq}</changefreq>\n"
                f"    <priority>{prio}</priority>\n"
                "  </url>"
            )
    for path, freq, prio in ENGLISH_ONLY_PAGES:
        loc = f"https://www.veloworkspaces.com/{path}"
        entries.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{prio}</priority>\n"
            "  </url>"
        )
    body = "\n".join(entries)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    with open(os.path.join(REPO, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("wrote sitemap.xml with", len(entries), "url entries")

if __name__ == "__main__":
    build()
