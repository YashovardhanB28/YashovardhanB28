#!/usr/bin/env python3
"""
Generates assets/research_chart.svg — a small horizontal bar chart of key
metrics from the three research projects, normalized to 0-1 for visual
comparison. This is static (metrics don't change often), so it's run once
manually or re-run when docs/RESEARCH.md numbers are updated — not on a
schedule, unlike scripts/update_stats.py.

Usage: python scripts/generate_research_chart.py
"""

import os

METRICS = [
    ("Hound ML — AMR AUROC", 0.99, "0.99"),
    ("Hound ML — Accuracy", 0.98, "~98%"),
    ("NETRS — External ROC AUC", 0.697, "0.697"),
    ("Deepfake — Benchmark Acc.", 0.97, "97%"),
    ("Deepfake — Real-world Acc. (fixed)", 0.80, ">80%"),
]

WIDTH = 640
BAR_HEIGHT = 22
BAR_GAP = 14
LABEL_WIDTH = 260
CHART_WIDTH = WIDTH - LABEL_WIDTH - 70
TOP_PAD = 20
HEIGHT = TOP_PAD * 2 + len(METRICS) * (BAR_HEIGHT + BAR_GAP)

COLOR_BG = "#0a1628"
COLOR_BAR = "#14b8a6"
COLOR_TEXT = "#f4f6f8"
COLOR_LABEL = "#8fa3b8"


def build_svg():
    bars = []
    for i, (label, value, display) in enumerate(METRICS):
        y = TOP_PAD + i * (BAR_HEIGHT + BAR_GAP)
        bar_w = max(2, CHART_WIDTH * value)
        bars.append(
            f'<text x="0" y="{y + BAR_HEIGHT - 6}" font-family="Segoe UI, sans-serif" '
            f'font-size="13" fill="{COLOR_LABEL}">{label}</text>'
        )
        bars.append(
            f'<rect x="{LABEL_WIDTH}" y="{y}" width="{CHART_WIDTH}" height="{BAR_HEIGHT}" '
            f'rx="4" fill="#132538"/>'
        )
        bars.append(
            f'<rect x="{LABEL_WIDTH}" y="{y}" width="{bar_w:.1f}" height="{BAR_HEIGHT}" '
            f'rx="4" fill="{COLOR_BAR}"/>'
        )
        bars.append(
            f'<text x="{LABEL_WIDTH + CHART_WIDTH + 10}" y="{y + BAR_HEIGHT - 6}" '
            f'font-family="Segoe UI, sans-serif" font-size="13" fill="{COLOR_TEXT}">{display}</text>'
        )

    svg = f'''<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{WIDTH}" height="{HEIGHT}" rx="8" fill="{COLOR_BG}"/>
  {''.join(bars)}
</svg>'''
    return svg


def main():
    out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "research_chart.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(build_svg())
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
