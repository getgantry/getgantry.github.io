# Gantry Website Constitution

The site getgantry.github.io presents Gantry, the native Mac app for Apple's `container`
tool. These rules bind every change to the site.

## Core Principles

### I. Generated Pages, One Source

- Edit the templates (`templates/`), the strings (`i18n/<lang>.json`) and the generators
  (`build_pages.py`, `build_docs.py`). Do not edit generated HTML by hand.
- Run the generators before each commit. The committed output must match the sources.

### II. True Claims Only

- The site describes only what a published Gantry release does. Features in branches or
  in progress stay off the live site until their release ships.
- Facts about other products cite their own pages, and the comparison is fair.

### III. Every Page in Every Site Language

- Each page exists in all 27 site languages, with hreflang links and a sitemap entry.
- Translations use the app glossaries (`/Volumes/SanDisk2Tb/builds/l10n/reviewed/`) so
  that the site and the app use the same terms. Serbian Latin comes from Serbian Cyrillic.

### IV. Search and AI Search

- Each page has its own title and description in each language, Open Graph tags and
  JSON-LD where it applies (SoftwareApplication, FAQ, HowTo).
- `llms.txt` and `llms-full.txt` list the features and guides. After a release goes live,
  send the changed URLs to IndexNow.
- Guides teach a real task. They are not advertisements.

### V. Fast and Accessible

- Plain static HTML and CSS with little JavaScript. Images have alt text and fixed sizes.
- The pages work without JavaScript, in light and dark mode, and on a phone.

## Workflow

- Every change goes through spec-kit: `/speckit-specify`, `/speckit-plan`, `/speckit-tasks`,
  then `/speckit-implement`. A task is ticked only when its result exists and was checked.
- Work happens on a branch. The site goes live when the branch merges to `main`, together
  with the Gantry release that it describes.
- Before a merge, check that every page builds and that all internal links resolve.
- Commits follow Conventional Commits in lowercase imperative English, with no AI attribution.

## Governance

This constitution overrides other practice documents for the site. A change to it is a
pull request that states the version bump and its reason. Versions follow semantic
versioning: MAJOR for a removed or redefined principle, MINOR for a new principle or
section, PATCH for wording.

**Version**: 1.0.0 | **Ratified**: 2026-11-07 | **Last Amended**: 2026-11-07
