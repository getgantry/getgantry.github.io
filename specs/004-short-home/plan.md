<!-- STE deviation: spec-kit template headings, product names, file names and paths stay verbatim. -->
# Implementation Plan: Short Home Page and a Features Page

**Branch**: `feat/short-home` | **Date**: 2026-11-16 | **Spec**: [spec.md](./spec.md)

## Summary <!-- slop: spec-kit template heading -->

1. Make `templates/features.html` from the area sections of the spec 003 home page. Fix the relative links for one level deeper.
2. Make `templates/home.html` short: area rows (`.areas`), a row of three figures, a short apple/container section, 8 questions.
3. In `build_pages.py`, add the page `features` to `PAGES`, add `render_features()` and `figures()`, and add `HOME_FAQ`. The home FAQ JSON-LD lists the 8 questions that the page shows.
4. Add 8 English strings and translate them into 25 languages.

## Constitution Check

| Principle | Check | Result |
|---|---|---|
| I. Generated Pages, One Source | Templates, generator and i18n only. | Pass |
| II. True Claims Only | No new claims. | Pass |
| III. Every Page in Every Site Language | `/features/` in 27 languages. | Pass |
| IV. Search and AI Search | New page has title, description, hreflang, sitemap, JSON-LD. FAQ JSON-LD matches the visible questions. | Pass |
| V. Fast and Accessible | Home page is shorter. | Pass |
