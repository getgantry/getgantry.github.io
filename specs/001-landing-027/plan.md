<!-- STE deviation: spec-kit template headings, product names, file names and paths stay verbatim. -->
# Implementation Plan: Landing Update for Gantry 0.27.0

**Branch**: `feat/landing-027` | **Date**: 2026-11-07 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-landing-027/spec.md`

**Note**: The implementation started before this plan. The plan describes the approach of the brief.

## Summary <!-- slop: spec-kit template heading -->

Collect the 0.27.0 facts from the app repository (CHANGELOG, PRs #47 to #55, branch reports). Update the strings and templates of the home page and the two product pages. Add five guide pages to the `PAGES` table of `build_pages.py`, with their templates and strings.

Translate the new strings into all site languages with the app glossaries. Update `llms.txt` and `llms-full.txt` through the generator. Run the generators. Write a link checker and a check for unique titles and descriptions. Commit and push the branch. Do not merge it.

## Technical Context

**Language/Version**: Python 3 (generators), HTML, CSS, a small amount of JavaScript

**Primary Dependencies**: `build_pages.py` and `build_docs.py` (own template engine), no external packages

**Storage**: `i18n/<lang>.json` strings, `templates/*.html`, generated HTML in the repository

**Testing**: A new link checker script. Checks for unique titles and descriptions, sitemap entries and hreflang. The `check()` function of `build_pages.py` compares the keys of each language with English.

**Target Platform**: GitHub Pages, static site

**Project Type**: Static web site with generators

**Performance Goals**: Pages stay plain HTML and CSS. Images have fixed sizes.

**Constraints**: No hand edits of generated HTML. No merge to `main`. No IndexNow request before the release.

**Scale/Scope**: 4 existing pages and 5 new pages in 27 languages, so about 240 generated pages. 2 llms files and the sitemap.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Result |
|---|---|---|
| I. Generated Pages, One Source | All changes go into `templates/`, `i18n/` and the generators. The output is generated before each commit. | Pass |
| II. True Claims Only | The branch describes 0.27.0 features, and some are in open branches. The branch merges only together with the release. Claims follow the branch reports. Competitor facts cite their pages. | Pass with a condition: before the merge, remove the claims of any branch that is not in the release |
| III. Every Page in Every Site Language | The five guides and the changed pages exist in all 27 languages with hreflang and sitemap entries. Glossaries are used. Serbian Latin is transliterated. | Pass |
| IV. Search and AI Search | Unique titles and descriptions, Open Graph, FAQ JSON-LD, `llms.txt` and `llms-full.txt`. IndexNow waits for the release. | Pass |
| V. Fast and Accessible | No new scripts. Screenshot placeholders get alt text and fixed sizes when the real images arrive. | Pass |

Post-design re-check: no change.

## Project Structure

### Documentation (this feature)

```text
specs/001-landing-027/
├── spec.md
├── plan.md
└── tasks.md
```

### Source Code (repository root)

```text
build_pages.py                 # PAGES: five new guide slugs, llms output
build_docs.py                  # only if a docs page links to a guide
templates/
├── home.html                  # 0.27.0 feature sections
├── apple-container.html       # 0.27.0 changes
├── apple-container-kubernetes.html   # native client, workers, shared image store
├── compare.html               # see the open question in spec.md
├── page.html                  # shared guide layout
└── <guide>.html               # new templates if page.html is not enough
i18n/
├── en.json                    # new keys for the guides and the features
├── <lang>.json                # the same keys in 26 more languages
└── languages.json
scripts/check_links.py         # new: link checker, unique titles and descriptions, sitemap check
llms.txt, llms-full.txt, sitemap.xml   # generated
<lang>/<slug>/index.html       # generated
```

**Structure Decision**: The guides use the existing `PAGES` mechanism. This gives them all languages, hreflang and the sitemap.

## Complexity Tracking

No violations.
