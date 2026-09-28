#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds everything around the blog's article bodies from blog_posts.py:

- each post's <head> (title, description, canonical, Open Graph and Twitter
  cards, BlogPosting + BreadcrumbList structured data), site header, article
  header (eyebrow, h1, lede, byline) and footer;
- blog/index.html, with every post in its group;
- blog/feed.xml, an RSS feed of every post, newest first.

The article body — everything inside <div class="container article-body"> —
is hand-written HTML in blog/<slug>/index.html and is kept exactly as it is.
To add a post: create blog/<slug>/index.html with any page around an
article-body div (copy an existing post), add its entry to POSTS, run
python3 i18n/build.py.

Authoring tooling only, like the rest of i18n/ (excluded from the deploy).
"""
import html
import json
import os
import re
import sys
from datetime import date
from email.utils import format_datetime
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_posts import GROUPS, POSTS  # noqa: E402

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITE = "https://www.veloworkspaces.com"
AUTHOR = "Gaoliang Luo"
APP_STORE = "https://apps.apple.com/app/apple-store/id6805509975?pt=129339260&amp;ct=homepage&amp;mt=8"
DEFAULT_OG = "/assets/og/default.jpg"

BODY_START = '<div class="container article-body">'
BODY_END = re.compile(r'\n    </div>\n  </section>\n</main>')

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def attr(text):
    return html.escape(text, quote=True)


def plain(fragment):
    """An HTML fragment as plain text, for structured data and alt text."""
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def long_date(iso):
    d = date.fromisoformat(iso)
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def og_image(slug):
    path = f"/assets/og/{slug}.jpg"
    return path if os.path.exists(os.path.join(REPO, path.lstrip("/"))) else DEFAULT_OG


HEADER = f'''<header class="site-header">
  <div class="container">
    <a class="brand" href="/">
      <img class="mark" src="/assets/icon.png" width="48" height="48" alt="Velo Workspaces">
      Velo Workspaces
    </a>
    <nav class="site-nav" aria-label="Primary">
      <span class="nav-links">
        <a href="/#personas">Who it's for</a>
        <a href="/#features">Features</a>
        <a href="/#pricing">Pricing</a>
        <a href="/support/">Support</a>
        <a href="/roadmap/">Roadmap</a>
        <a href="/blog/" aria-current="page">Blog</a>
      </span>
      <a class="btn btn-primary" data-app-store-link href="{APP_STORE}">Download</a>
    </nav>
  </div>
</header>'''


def footer(trademarks=""):
    extra = f" {trademarks}" if trademarks else ""
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <a class="brand" href="/">
        <img class="mark" src="/assets/icon.png" width="28" height="28" alt="Velo Workspaces">
        Velo Workspaces
      </a>
      <nav class="footer-links" aria-label="Footer">
        <a href="/blog/">Blog</a>
        <a href="/roadmap/">Roadmap</a>
        <a href="/support/">Support</a>
        <a href="/privacy/">Privacy</a>
        <a href="mailto:support@veloworkspaces.com">support@veloworkspaces.com</a>
      </nav>
    </div>
    <p class="footer-fine">© 2026 Velo Workspaces. Apple, the Apple logo, Mac, macOS, and App Store are trademarks of Apple Inc., registered in the U.S. and other countries. Velo Workspaces is an independent app and is not affiliated with or endorsed by Apple Inc.{extra}</p>
  </div>
</footer>

<script src="/assets/app-store.js?v=3"></script>
</body>
</html>
'''


def head(*, title, description, url, og_type, image, image_alt, extra_meta="", ld):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{attr(title)}</title>
<meta name="description" content="{attr(description)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/assets/icon.png">
<link rel="stylesheet" href="/assets/style.css?v=6">
<link rel="alternate" type="application/rss+xml" title="Velo Workspaces Blog" href="{SITE}/blog/feed.xml">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Velo Workspaces">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{attr(image_alt)}">
<meta name="twitter:card" content="summary_large_image">
{extra_meta}<script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

'''


def post_page(post, body):
    slug = post["slug"]
    url = f"{SITE}/blog/{slug}/"
    image = og_image(slug)
    h1_text = plain(post["h1"])
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "headline": post["title"][:110],
                "name": h1_text,
                "description": post["description"],
                "image": f"{SITE}{image}",
                "datePublished": post["published"],
                "dateModified": post["modified"],
                "author": {"@type": "Person", "name": AUTHOR, "url": f"{SITE}/"},
                "publisher": {
                    "@type": "Organization",
                    "name": "Velo Workspaces",
                    "url": f"{SITE}/",
                    "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icon.png"},
                },
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                "inLanguage": "en",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
                    {"@type": "ListItem", "position": 3, "name": h1_text, "item": url},
                ],
            },
        ],
    }
    extra = (f'<meta property="article:published_time" content="{post["published"]}">\n'
             f'<meta property="article:modified_time" content="{post["modified"]}">\n'
             f'<meta property="article:author" content="{AUTHOR}">\n')
    byline = f'By {AUTHOR} · Published <time datetime="{post["published"]}">{long_date(post["published"])}</time>'
    if post["modified"] != post["published"]:
        byline += f' · Updated <time datetime="{post["modified"]}">{long_date(post["modified"])}</time>'
    return (
        head(title=post["title"], description=post["description"], url=url, og_type="article",
             image=image, image_alt=h1_text, extra_meta=extra, ld=ld)
        + HEADER
        + f'''

<main id="main">
  <section class="section" style="padding-bottom:0;">
    <div class="container">
      <a class="article-back-link" href="/blog/">← Back to Blog</a>
      <div class="article-header">
        <span class="eyebrow">{post["eyebrow"]}</span>
        <h1>{post["h1"]}</h1>
        <p class="article-lede">{post["lede"]}</p>
        <p class="article-meta">{byline}</p>
      </div>
    </div>
  </section>

  <section class="section">
    {BODY_START}
{body}
    </div>
  </section>
</main>

'''
        + footer(post.get("trademarks", ""))
    )


def read_body(slug):
    path = os.path.join(REPO, "blog", slug, "index.html")
    text = open(path, encoding="utf-8").read()
    start = text.index(BODY_START) + len(BODY_START)
    end = BODY_END.search(text, start)
    if end is None:
        raise SystemExit(f"{path}: no end of the article body found")
    return text[start:end.start()].strip("\n")


INDEX_TITLE = "Velo Workspaces Blog: Linux VMs, AI Agents and Apple Silicon"
INDEX_DESCRIPTION = ("Guides to running Linux VMs on Apple silicon Macs: cloud images, automatic installs, "
                     "local AI agents, Rosetta, benchmarks and honest comparisons.")


def index_page():
    url = f"{SITE}/blog/"
    by_group = {g["name"]: [p for p in POSTS if p["group"] == g["name"]] for g in GROUPS}
    ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Velo Workspaces Blog",
        "description": INDEX_DESCRIPTION,
        "url": url,
        "publisher": {"@type": "Organization", "name": "Velo Workspaces", "url": f"{SITE}/"},
        "blogPost": [
            {"@type": "BlogPosting", "headline": p["title"][:110], "url": f"{SITE}/blog/{p['slug']}/",
             "datePublished": p["published"], "dateModified": p["modified"]}
            for p in POSTS
        ],
    }
    groups_html = []
    for g in GROUPS:
        cards = []
        for p in by_group[g["name"]]:
            cards.append(f'''            <a class="blog-index-card" href="/blog/{p["slug"]}/">
              <span class="eyebrow">{p["eyebrow"]}</span>
              <h3>{p["card_title"]}</h3>
              <p>{p["card_summary"]}</p>
            </a>''')
        cards_html = "\n\n".join(cards)
        groups_html.append(f'''        <div class="blog-index-group">
          <h2>{g["name"]}</h2>
          <p class="blog-index-group-desc">{g["description"]}</p>
          <div class="blog-index-cards">
{cards_html}
          </div>
        </div>''')
    return (
        head(title=INDEX_TITLE, description=INDEX_DESCRIPTION, url=url, og_type="website",
             image=DEFAULT_OG, image_alt="Velo Workspaces Blog", ld=ld)
        + HEADER
        + f'''

<main id="main">
  <section class="section" style="padding-bottom:0;">
    <div class="container">
      <div class="article-header">
        <span class="eyebrow">Blog</span>
        <h1>Linux VMs, AI agents and Apple silicon, explained.</h1>
        <p class="article-lede">Step-by-step guides, measured benchmarks and plain-English explainers for running Linux, macOS and AI agents in virtual machines on your Mac.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="blog-index-list">

{chr(10).join(groups_html)}

      </div>
    </div>
  </section>
</main>

'''
        + footer()
    )


def feed():
    items = []
    for p in sorted(POSTS, key=lambda p: (p["published"], p["modified"]), reverse=True):
        when = datetime.fromisoformat(p["published"]).replace(hour=12, tzinfo=timezone.utc)
        items.append(f'''  <item>
    <title>{html.escape(p["title"])}</title>
    <link>{SITE}/blog/{p["slug"]}/</link>
    <guid isPermaLink="true">{SITE}/blog/{p["slug"]}/</guid>
    <pubDate>{format_datetime(when)}</pubDate>
    <description>{html.escape(p["description"])}</description>
  </item>''')
    newest = max(p["modified"] for p in POSTS)
    built = datetime.fromisoformat(newest).replace(hour=12, tzinfo=timezone.utc)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Velo Workspaces Blog</title>
  <link>{SITE}/blog/</link>
  <atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>
  <description>{html.escape(INDEX_DESCRIPTION)}</description>
  <language>en</language>
  <lastBuildDate>{format_datetime(built)}</lastBuildDate>
{chr(10).join(items)}
</channel>
</rss>
'''


def check():
    slugs = [p["slug"] for p in POSTS]
    dirs = sorted(d for d in os.listdir(os.path.join(REPO, "blog"))
                  if os.path.isdir(os.path.join(REPO, "blog", d)))
    missing = sorted(set(dirs) - set(slugs))
    unknown = sorted(set(slugs) - set(dirs))
    dupes = sorted({s for s in slugs if slugs.count(s) > 1})
    names = {g["name"] for g in GROUPS}
    ungrouped = [p["slug"] for p in POSTS if p["group"] not in names]
    if missing or unknown or dupes or ungrouped:
        raise SystemExit(f"blog_posts.py is out of step: not listed {missing}, no page {unknown}, "
                         f"duplicated {dupes}, unknown group {ungrouped}")


def main():
    check()
    for p in POSTS:
        body = read_body(p["slug"])
        path = os.path.join(REPO, "blog", p["slug"], "index.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(post_page(p, body))
    with open(os.path.join(REPO, "blog", "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page())
    with open(os.path.join(REPO, "blog", "feed.xml"), "w", encoding="utf-8") as f:
        f.write(feed())
    print(f"wrote {len(POSTS)} posts, blog/index.html and blog/feed.xml")


if __name__ == "__main__":
    main()
