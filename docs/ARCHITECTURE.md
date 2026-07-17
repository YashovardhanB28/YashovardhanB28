# Architecture & Roadmap Specification

This document separates what's actually implemented in this repo from the larger interactive
site concept, so the README never overstates what exists.

## Implemented today

| Component | File | Status |
|---|---|---|
| Profile README | `README.md` | ✅ Live |
| Research write-ups | `docs/RESEARCH.md` | ✅ Live |
| Stats auto-refresh | `scripts/update_stats.py` + `.github/workflows/refresh-profile.yml` | ✅ Live — runs weekly, needs no extra setup beyond default `GITHUB_TOKEN` |
| Broken-link checking | `.github/workflows/link-check.yml` | ✅ Live — uses `lychee-action`, no keys needed |
| Issue/PR templates | `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md` | ✅ Live |

## Planned: Interactive Site (not yet built)

The longer-term idea is a small Next.js site (deployed via GitHub Pages or Cloudflare Pages)
that goes beyond the flat README. This section specifies it so it can be built incrementally
rather than all at once — each item below is genuinely useful on its own, so partial completion
still ships value.

### Recommended stack

| Layer | Choice | Why |
|---|---|---|
| Framework | Next.js (static export) | Free hosting via Pages, no server needed |
| Styling | Tailwind CSS | Fast iteration, consistent with DealMatch stack already known |
| Diagrams | Mermaid (pre-rendered at build time) | No client JS cost, renders in plain Markdown too |
| Skill graph | D3.js (force-directed, 2D) | Three.js/R3F adds real maintenance and accessibility cost for marginal benefit over a well-designed 2D graph — recommend starting here and only moving to 3D if the 2D version proves the concept |
| Search | Static keyword/tag search over `docs/RESEARCH.md` sections | Embedding-based search needs a vector DB and ongoing indexing cost that isn't justified until there's enough content to search |
| Data source | GitHub REST/GraphQL API, fetched at build time | Avoids client-side rate limits |

### Phase 1 — Static site shell
- Port `README.md` + `docs/RESEARCH.md` content into a Next.js static site with proper typography
  and the same content, no new features yet. Validates the pipeline before adding complexity.

### Phase 2 — Real skill graph
- A D3 force-directed graph of skills → projects (e.g. "PyTorch" node connects to "Deepfake
  Forensics" and "Hound ML"). Data source: a single hand-maintained `data/skills.json`, not
  auto-generated — auto-extraction from commits is unreliable and not worth the complexity here.

### Phase 3 — Auto-generated architecture diagrams
- A GitHub Action that runs on push to any linked project repo, regenerates a Mermaid diagram of
  that repo's folder structure via a simple script, and commits it to `docs/diagrams/`.

### Deliberately deferred / not recommended as-is
- **3D "commit galaxy" / "project universe" visualizations** — high build and maintenance cost,
  accessibility concerns (motion, WebGL fallback), and limited signal for a hiring audience beyond
  novelty. Worth revisiting only if Phase 2's 2D graph gets real engagement and a 3D version would
  add clarity, not just spectacle.
- **AI interview simulator, ARG-style puzzle, procedural achievement system** — fun but orthogonal
  to job-search and research-collaboration goals; skipping these keeps the repo's scope honest
  about what it's for.
- **Daily fully-autonomous AI rewrites of README content** — risk of the README drifting from
  what's actually true about current work. The weekly stats refresh (numbers only, not prose) is
  the safer version of "living README" — factual fields update automatically, but the narrative
  stays human-written and accurate.

## Guiding principle

Every automated or interactive feature here should either (a) save real maintenance time, or
(b) communicate something about the underlying research/engineering work more clearly than plain
text. Features that exist mainly to look impressive are cut, since the actual research write-ups
in `docs/RESEARCH.md` are stronger signal than any visualization would be.
