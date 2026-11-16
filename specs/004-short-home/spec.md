<!-- STE deviation: spec-kit template headings, the quoted user input, Given-When-Then scenarios, product names and paths stay verbatim. -->
# Feature Specification: Short Home Page and a Features Page

**Feature Branch**: `feat/short-home`

**Created**: 2026-11-16

**Status**: Done

**Input**: User description: "Is such a long landing page OK? What is the concept?" Answer: no. Make the home page short and move the full feature list to a new page.

## Context

Spec 003 made the home page an operator's manual with all 70 feature items, 8 figures and 19 apple/container items. The English home page is 14,724 px tall at 1440 px and 21,141 px at 390 px. A home page is the cover of the manual, not the full manual. The Product Hunt launch starts on 2026-11-17, and its visitors come to the home page.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Understand Gantry from a short page (Priority: P1)

A visitor reads the home page and sees the idea, the download, the command table, the areas of the app, three figures, the releases, the install steps and the main questions.

**Independent Test**: Measure the home page height in all 27 languages.

**Acceptance Scenarios**:

1. **Given** the home page at 1440 px, **When** a visitor scrolls, **Then** the page ends before 6,000 px.
2. **Given** an area row on the home page, **When** a visitor clicks it, **Then** the features page opens at that area.

### User Story 2 - Read all features on one page (Priority: P1)

A visitor who wants details opens `/features/` and finds each feature item, figure and question that the home page had before.

**Independent Test**: Each `home.*` feature string that spec 003 put on the home page is on the home page or on `/features/`.

### Edge Cases

- JavaScript is off: both pages show all content.
- The home page shows 8 questions. Its FAQ JSON-LD lists only these 8. The features page shows and lists all 21.

## Requirements *(mandatory)*

- **FR-001**: The home page MUST show the title block, the command table (8 rows), one row for each area with a link to `/features/#area`, three figures, apple/container links, releases, install and 8 questions.
- **FR-002**: `/features/` MUST exist in all 27 languages with hreflang, a sitemap entry, its own title and description, BreadcrumbList and FAQ JSON-LD.
- **FR-003**: No feature string, figure or question MUST be lost: each one is on the home page or on `/features/`.
- **FR-004**: The nav item "Features" MUST open `/features/`.
- **FR-005**: The GitHub link MUST show the live star count from the GitHub API. Without JavaScript, or when the API does not answer, the link shows "GitHub" with no number. The HTML has no fixed count.

## Success Criteria *(mandatory)*

- **SC-001**: The English home page is 6,000 px tall or less at 1440 px (before: 14,724 px).
- **SC-002**: 0 strings of spec 003 are lost.
- **SC-003**: The build check and the link check show 0 problems. No page has a horizontal scroll at 390 px.

## Assumptions

- The features page reuses the strings of spec 003. Only 8 strings are new.
