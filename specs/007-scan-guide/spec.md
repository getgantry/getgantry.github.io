<!-- STE deviation: spec-kit template headings, the quoted user input, product names, commands and paths stay verbatim. -->
# Feature Specification: Image Scan Guide and Guide Heading Fix

**Feature Branch**: `feat/scan-guide`

**Created**: 2026-11-23

**Status**: Done

**Input**: User description: "Update the site for Gantry 0.29.0." Spec 002 put the 0.29.0 features on the site. A local branch made the same update and also had two items that the site does not have. This feature adds only these two items.

## Context

- Gantry 0.29.0 can scan an image with Trivy or Grype (getgantry/gantry#72). No page of the site tells how to scan an image on a Mac.
- In `sections_html` of `build_pages.py`, the list variable replaced the heading tag. Thus each section heading after a list became `<ul id=…>` or `<ol id=…>`. This occurred on 108 generated pages.

## Requirements *(mandatory)*

- **FR-001**: The site MUST have the guide `scan-container-images-mac` in all 27 languages, with HowTo and FAQ JSON-LD, hreflang links and a sitemap entry.
- **FR-002**: The commands of the guide MUST have been run on Apple container 1.7.1 with Trivy 0.76.2 and Grype 0.121.3.
- **FR-003**: Each section heading of a guide MUST be a heading element, also after a list.
- **FR-004**: `llms.txt` MUST list the new guide.

## Success Criteria *(mandatory)*

- **SC-001**: The key check shows `27 languages ok`.
- **SC-002**: The link check shows 0 problems.
- **SC-003**: 0 generated pages have `<ul id=` or `<ol id=`.

## Assumptions

- The screenshot of the scan sheet does not exist yet. The guide has a `TODO-SCREENSHOT` marker in its place.
- The command checks are in `specs/002-landing-029` of the branch `feat/landing-029`: the tar of `container image save` starts with `./`. Trivy and Grype refuse this tar, and they scan the unpacked folder.
