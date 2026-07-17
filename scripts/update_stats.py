#!/usr/bin/env python3
"""
Regenerates the STATS block in README.md using the GitHub REST API.

Run in CI (see .github/workflows/refresh-profile.yml) with:
  GITHUB_TOKEN   - provided automatically by Actions
  GITHUB_USER    - your GitHub username (repo variable or hardcoded below)

No external dependencies beyond `requests` (installed in the workflow).
"""

import os
import re
import sys
from datetime import datetime, timezone

import requests

USERNAME = os.environ.get("GITHUB_USER", "YashovardhanB28")
TOKEN = os.environ.get("GITHUB_TOKEN")
README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")

API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def get(url, params=None):
    resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_public_repos():
    repos, page = [], 1
    while True:
        batch = get(
            f"{API}/users/{USERNAME}/repos",
            params={"per_page": 100, "page": page, "type": "owner"},
        )
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return [r for r in repos if not r.get("fork")]


def build_stats_block(repos):
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    languages = {}
    for r in repos:
        lang = r.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    top_langs = sorted(languages.items(), key=lambda kv: kv[1], reverse=True)[:5]
    lang_str = " · ".join(f"{lang} ({count})" for lang, count in top_langs) or "—"

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return (
        f"**{len(repos)}** public repos · **{total_stars}** stars total\n"
        f"Top languages: {lang_str}\n\n"
        f"<sub>Last updated {updated} UTC</sub>"
    )


def update_readme(stats_block):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        r"(<!--STATS-START-->)(.*?)(<!--STATS-END-->)", re.DOTALL
    )
    if not pattern.search(content):
        print("STATS markers not found in README.md; aborting.", file=sys.stderr)
        sys.exit(1)

    new_content = pattern.sub(
        lambda m: f"{m.group(1)}\n\n{stats_block}\n\n{m.group(3)}", content
    )

    if new_content != content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md stats block updated.")
        return True

    print("No changes to stats block.")
    return False


def main():
    repos = fetch_public_repos()
    stats_block = build_stats_block(repos)
    update_readme(stats_block)


if __name__ == "__main__":
    main()
