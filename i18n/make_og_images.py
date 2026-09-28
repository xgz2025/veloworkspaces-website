#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renders the share images in assets/og/: default.jpg for the home page, the
blog index and anything without its own, and <slug>.jpg for every blog post,
with the post's card title on it. Run after adding a post or changing a
title, then python3 i18n/build.py so the pages point at them.

    python3 i18n/make_og_images.py            # every image
    python3 i18n/make_og_images.py <slug> ... # just these posts

Needs Node with Playwright (npm i -g playwright). Authoring tooling only.
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from blog_posts import POSTS  # noqa: E402


def plain(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def main():
    wanted = set(sys.argv[1:])
    cards = []
    if not wanted:
        cards.append(dict(out="assets/og/default.jpg", eyebrow="For Apple silicon Macs",
                          title="Linux in about a minute. Disposable VMs and AI sandboxes on your Mac.",
                          footer="Free on the Mac App Store"))
    for p in POSTS:
        if wanted and p["slug"] not in wanted:
            continue
        cards.append(dict(out=f"assets/og/{p['slug']}.jpg", eyebrow=plain(p["eyebrow"]),
                          title=plain(p["card_title"]), footer="Velo Workspaces Blog"))
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(cards, f)
    env = dict(os.environ)
    root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env["NODE_PATH"] = root + os.pathsep + env.get("NODE_PATH", "")
    subprocess.run(["node", os.path.join(HERE, "og_images.cjs"), f.name, REPO], check=True, env=env)
    os.unlink(f.name)


if __name__ == "__main__":
    main()
