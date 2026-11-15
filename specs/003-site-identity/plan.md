<!-- STE deviation: spec-kit template headings, product names, font names, file names and paths stay verbatim. -->
# Implementation Plan: Site Identity ("Command and Control")

**Branch**: `feat/rebrand` and the stacked branches below | **Date**: 2026-11-15 | **Spec**: [spec.md](./spec.md)

## Summary <!-- slop: spec-kit template heading -->

Section 4 of `research.md` has the detailed plan. This file records the decisions and the order.

Decisions on the open questions of `research.md` (owner: "decide yourself"):

1. Concept A, with the beam and the single orange from B, and unframed screenshots from C.
2. The h1 changes. `home.title`, `home.desc` and `home.keywords` stay.
3. Self-hosted fonts with the system stack as fallback.
4. No manual theme switch. Light screenshots in both schemes.

## Technical Context

**Language and version**: Python 3 generators, HTML, CSS

**Primary dependencies**: `build_pages.py`, `build_docs.py`, `scripts/i18n_delta.py`, `scripts/check_links.py`, new `scripts/check_fonts.py`

**Fonts**: IBM Plex Sans 400 and 600, JetBrains Mono 400, WOFF2 subsets from `@fontsource` (SIL OFL 1.1), in `assets/fonts/` with `OFL.txt`

**Testing**: `python3 build_pages.py --check`, `scripts/check_links.py`, `scripts/check_fonts.py`, Playwright with Chrome at 1440 px and 390 px in light and dark mode

**Constraints**: Edit only the sources of generated HTML. Keep each PR unmerged. Send no IndexNow request.

## Stacked pull requests

| # | Branch | Base | Content |
|---|--------|------|---------|
| 1 | `feat/rebrand` | `feat/landing-0-29` | Tokens, fonts, light mode, backdrop removed, `og:image` size. No i18n change. |
| 2 | `refactor/rebrand-strip` | 1 | Decoration and mock UI removed, about 30 keys deleted. |
| 3 | `feat/rebrand-home` | 2 | Command rail, areas, new copy, 26 translations. |
| 4 | `perf/rebrand-images` | 3 | Sized WebP images, inner pages, new `og:image`. |
| 5 | `docs/rebrand-voice` | 4 | Optional voice pass on older strings. |

## Constitution Check

| Principle | Check | Result |
|---|---|---|
| I. Generated Pages, One Source | Changes are in templates, CSS, i18n and generators. Output is generated in its own commit. | Pass |
| II. True Claims Only | The mock UI and the unverified command go. Rail commands are real commands. | Pass |
| III. Every Page in Every Site Language | New strings go to all 27 languages in PR 3. Fonts are checked for all characters. | Pass |
| IV. Search and AI Search | Title, description, keywords, JSON-LD, hreflang, sitemap and llms files stay. | Pass |
| V. Fast and Accessible | Light mode is added. Less JavaScript. Fixed image sizes. Contrast 4.5:1. | Pass (fixes a gap) |

## Complexity Tracking

No violations.
