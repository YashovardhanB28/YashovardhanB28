#!/usr/bin/env python3
"""
generate_skyline.py — builds assets/skyline.svg: an isometric "city" where
each building is one of the user's real public repos.

- Building height  = log-scaled (stars * 3 + forks * 2 + size_kb/50 + 1)
  i.e. a rough "activity/impact" score, not a single vanity metric.
- Building width    = fixed, buildings sorted by height (skyline silhouette)
- Building color    = mapped from the repo's primary language
- Windows           = lit/unlit pattern seeded from repo name (deterministic,
                       so it doesn't flicker differently every run — but still
                       looks organic, not a grid).

This is bespoke code, not a wrapper around an existing badge/stats service.
Run manually or via .github/workflows/refresh-profile.yml.

Usage:
    GITHUB_USER=YashovardhanB28 python scripts/generate_skyline.py
"""

import math
import os
import random

import requests

USERNAME = os.environ.get("GITHUB_USER", "YashovardhanB28")
TOKEN = os.environ.get("GITHUB_TOKEN")
API = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

LANGUAGE_COLORS = {
    "Python": "#3776ab",
    "TypeScript": "#3178c6",
    "JavaScript": "#f0db4f",
    "C++": "#00599c",
    "R": "#276dc3",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Jupyter Notebook": "#da5b0b",
    "Shell": "#89e051",
    None: "#5c6b7a",
}
DEFAULT_COLOR = "#5c6b7a"

WIDTH = 900
HEIGHT = 320
GROUND_Y = 280
BUILDING_W = 46
GAP = 14
BG = "#0a1628"
SKY_GLOW = "#0f2438"
MAX_BUILDING_H = 190
MIN_BUILDING_H = 40
MAX_REPOS = 14


def fetch_repos():
    repos, page = [], 1
    while True:
        batch = requests.get(
            f"{API}/users/{USERNAME}/repos",
            headers=HEADERS,
            params={"per_page": 100, "page": page, "type": "owner"},
            timeout=15,
        ).json()
        if not isinstance(batch, list) or not batch:
            break
        repos.extend(batch)
        page += 1
    return [r for r in repos if not r.get("fork")]


def activity_score(repo):
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    size = repo.get("size", 0)  # KB
    raw = stars * 3 + forks * 2 + size / 50 + 1
    return math.log(raw + 1, 1.6)  # log-scale so one big repo doesn't dwarf the rest


def isometric_building(x, base_y, w, h, color, seed_name):
    """Return SVG markup for one flat-front building with a lit-window pattern
    seeded deterministically from the repo name."""
    rng = random.Random(seed_name)
    top_y = base_y - h

    # subtle side-shading for depth without true 3D
    body = (
        f'<rect x="{x}" y="{top_y}" width="{w}" height="{h}" fill="{color}" opacity="0.92"/>'
        f'<rect x="{x}" y="{top_y}" width="{w}" height="{h}" fill="url(#buildingShade)"/>'
    )

    windows = []
    win_w, win_h, pad = 6, 8, 6
    cols = max(1, (w - pad) // (win_w + pad))
    rows = max(1, int((h - pad) // (win_h + pad)))
    for r in range(rows):
        for c in range(cols):
            if rng.random() < 0.35:
                continue  # unlit window
            wx = x + pad + c * (win_w + pad)
            wy = top_y + pad + r * (win_h + pad)
            windows.append(
                f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{win_w}" height="{win_h}" '
                f'fill="#ffd166" opacity="0.85"/>'
            )

    return body + "".join(windows)


def build_svg(repos):
    repos = sorted(repos, key=activity_score, reverse=True)[:MAX_REPOS]
    scores = [activity_score(r) for r in repos]
    max_score = max(scores) if scores else 1

    total_w = len(repos) * (BUILDING_W + GAP) - GAP
    start_x = (WIDTH - total_w) / 2 if total_w < WIDTH else 20

    buildings = []
    labels = []
    for i, repo in enumerate(repos):
        score = activity_score(repo)
        h = MIN_BUILDING_H + (score / max_score) * (MAX_BUILDING_H - MIN_BUILDING_H)
        x = start_x + i * (BUILDING_W + GAP)
        lang = repo.get("language")
        color = LANGUAGE_COLORS.get(lang, DEFAULT_COLOR)
        buildings.append(
            isometric_building(x, GROUND_Y, BUILDING_W, h, color, repo["name"])
        )
        labels.append(
            f'<text x="{x + BUILDING_W/2:.1f}" y="{GROUND_Y + 18}" font-family="Segoe UI, sans-serif" '
            f'font-size="9" fill="#8fa3b8" text-anchor="middle">{repo["name"][:10]}</text>'
        )

    stars = sum(r.get("stargazers_count", 0) for r in repos)

    svg = f'''<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="{SKY_GLOW}"/>
    </linearGradient>
    <linearGradient id="buildingShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.25"/>
      <stop offset="50%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.25"/>
    </linearGradient>
  </defs>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#sky)"/>
  <line x1="0" y1="{GROUND_Y}" x2="{WIDTH}" y2="{GROUND_Y}" stroke="#14b8a6" stroke-width="1.5" opacity="0.5"/>
  {''.join(buildings)}
  {''.join(labels)}
  <text x="20" y="30" font-family="Segoe UI, sans-serif" font-size="14" fill="#f4f6f8" font-weight="600">Commit Skyline</text>
  <text x="20" y="48" font-family="Segoe UI, sans-serif" font-size="11" fill="#8fa3b8">Each building = a real repo. Height = stars + forks + size. {stars} total stars across skyline.</text>
</svg>'''
    return svg


def main():
    repos = fetch_repos()
    svg = build_svg(repos) if repos else build_svg([])
    out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "skyline.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {out_path} from {len(repos)} repos")


if __name__ == "__main__":
    main()
