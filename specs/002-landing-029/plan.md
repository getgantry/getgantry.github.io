<!-- STE deviation: spec-kit template headings, product names, file names and paths stay verbatim. -->
# Implementation Plan: Landing Update for Gantry 0.29.0

**Branch**: `feat/landing-0-29` | **Date**: 2026-11-15 | **Spec**: [spec.md](./spec.md)

## Summary <!-- slop: spec-kit template heading -->

1. Build the Debug app at `v0.29.0`.
2. Make the screenshots with demo data. Write the claims list in research.md.
3. Add the section `#latest` to the home page, above the 0.27.0 section. It has eight feature cards and two screenshots.
4. Add the features to the JSON-LD `featureList` and to the command table of the `apple/container` guide.
5. Add the sections `#compose` and `#secrets` to the guide "Create a container from a docker run command".
6. Add a Compose export note to the guide "Move from Docker Desktop to Apple container".
7. Update the docs and `llms.txt`. Set the version to 0.29.0.
8. Translate the new strings into 25 languages with the UI names of the app catalog. Serbian Latin comes from Serbian Cyrillic.
9. Build and check the site. Open a pull request.

## Technical Context

**Language and version**: Python 3 generators, HTML, CSS

**Primary dependencies**: `build_pages.py`, `build_docs.py`, `scripts/i18n_delta.py`, `scripts/check_links.py`

**Testing**: `python3 build_pages.py --check`, `scripts/check_links.py`, and the Orca embedded browser at desktop width and phone width

**Constraints**: Edit only the sources of generated HTML. Keep the branch unmerged. Send no IndexNow request.

## Constitution Check

| Principle | Check | Result |
|---|---|---|
| I. Generated Pages, One Source | Changes are in `templates/`, `i18n/`, `build_pages.py` and `build_docs.py`. The output is generated again. | Pass |
| II. True Claims Only | Release v0.29.0 is published. Each claim has a source in research.md. | Pass |
| III. Every Page in Every Site Language | New strings are in all 27 languages. UI names come from the app catalog. | Pass |
| IV. Search and AI Search | JSON-LD `featureList` and version, llms files and sitemap are generated again. IndexNow waits. | Pass |
| V. Fast and Accessible | Screenshots have alt text and fixed sizes. Each PNG is smaller than 200 KB. | Pass |

## Project Structure

```text
build_pages.py          # APP_VERSION, UPDATED, SHOTS with one folder per release, home shots
build_docs.py           # menu bar, containers, images & compose docs
templates/home.html     # section #latest, fleet.png size
i18n/<lang>.json        # home.latest, ld features, shots.fleet_*, guide table, guides
llms.txt                # intro, new features, page notes
assets/shots/0.29.0/    # fleet-activity.png, menu-bar-progress.png
assets/fleet.png        # new dashboard screenshot
```

## Complexity Tracking

No violations.
