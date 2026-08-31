#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerates every localized static page from the content_*.py dictionaries
in this directory. Run this after editing any content_*.py file, or after
changing English copy in the root index.html / privacy/index.html /
support/index.html by hand (update the matching "en" entry first, then run
this — don't let the English source and the generated English page drift).

    python3 i18n/build.py

This script is authoring tooling only — it is not part of the deployed
site (see .assetsignore) and the site itself has no build step.
"""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = [
    "render_home.py",
    "render_privacy.py",
    "render_support.py",
    "render_404.py",
    "gen_sitemap.py",
]

def main():
    for script in SCRIPTS:
        path = os.path.join(HERE, script)
        print(f"--- running {script} ---")
        result = subprocess.run([sys.executable, path], cwd=HERE)
        if result.returncode != 0:
            print(f"FAILED: {script}", file=sys.stderr)
            sys.exit(result.returncode)
    print("\nAll locales regenerated.")

if __name__ == "__main__":
    main()
