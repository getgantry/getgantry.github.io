<!-- STE deviation: spec-kit template headings, product names, file names and paths stay verbatim. -->
# Implementation Plan: Image Scan Guide and Guide Heading Fix

**Branch**: `feat/scan-guide` | **Date**: 2026-11-23 | **Spec**: [spec.md](./spec.md)

## Summary <!-- slop: spec-kit template heading -->

Add `scan-container-images-mac` to `GUIDES`, its commands to `GUIDE_CODE` and the screenshot `scan-sheet` to `SHOTS`. Copy the strings `guides.scan-container-images-mac` of the 26 language files from the branch `feat/landing-029`. Rename the list variable in `sections_html`. Add the guide to `llms.txt`. Run the generators and the checks.

## Constitution Check

| Principle | Result |
|---|---|
| I. Generated Pages, One Source | Pass: changes are in `build_pages.py`, `i18n/` and `llms.txt` |
| II. True Claims Only | Pass: the scan is in the published release 0.29.0 (#72); the commands were run |
| III. Every Page in Every Site Language | Pass: 26 language files, Serbian Latin is transliterated |
| IV. Search and AI Search | Pass: HowTo and FAQ JSON-LD, sitemap, `llms.txt`; IndexNow after the merge |
| V. Fast and Accessible | Pass: no new scripts; correct heading elements |
