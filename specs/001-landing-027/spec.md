<!-- STE deviation: spec-kit template headings, the quoted user input, Given-When-Then scenarios, product names, page titles and paths stay verbatim. -->
# Feature Specification: Landing Update for Gantry 0.27.0

**Feature Branch**: `feat/landing-027`

**Created**: 2026-11-07

**Status**: In Progress (implementation started before spec-kit adoption on 2026-11-07)

**Input**: User description: "Update the site for Gantry 0.27.0. Position Gantry as the best native Mac app for Apple's container tool and a free open-source alternative to Docker Desktop and OrbStack. Add how-to guides in all site languages, update llms.txt, and check every page and link. The site goes live together with the 0.27.0 release." Source brief: `/Volumes/SanDisk2Tb/builds/gantry-027/landing.md`.

## Context

Gantry 0.27.0 adds many features. The main ones are support for Apple container 1.7.1, a Kubernetes browser with no kubectl, and Explain Failure with Apple Intelligence. Others are macOS integration, the command palette, bulk actions, create from a pasted run command, and recipes. The release also adds external drives, a new design, and 28 UI languages. Some of these features are still in open branches (`feat/apple-container-1-7-1`, `feat/kubernetes-native`, `feat/hig-design-pass`, `feat/external-storage`). The site must describe only what the release contains.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Learn what Gantry 0.27.0 does (Priority: P1)

A visitor opens the home page, the Apple container page or the Apple container Kubernetes page in any site language. The visitor sees the features of 0.27.0 with exact claims.

**Why this priority**: These pages get the most visits. They must be correct on release day.

**Independent Test**: Read the home page and the two product pages in English and in two other languages. Compare each claim with the CHANGELOG and the branch reports.

**Acceptance Scenarios**:

1. **Given** the 0.27.0 release, **When** a visitor opens the home page, **Then** the feature sections describe the 0.27.0 features.
2. **Given** a branch report says a part is missing, **When** the site describes that feature, **Then** the site does not claim the missing part.
3. **Given** the Kubernetes page, **When** a visitor reads it, **Then** it says that Gantry browses an Apple container cluster with no kubectl.
4. **Given** a new feature has no 0.27.0 screenshot yet, **When** the page is built, **Then** the page has a `TODO-SCREENSHOT` marker with the section and the file name, not an old screenshot.

---

### User Story 2 - Follow a how-to guide (Priority: P1)

A visitor finds a guide through search and does the task. The guides are:

- "Run Kubernetes on a Mac with Apple container"
- "Move from Docker Desktop to Apple container"
- "Gantry vs Docker Desktop vs OrbStack vs Podman Desktop"
- "Store containers and volumes on an external drive on a Mac"
- "Create a container from a docker run command"

**Why this priority**: Guides bring visitors from search. They must teach a real task.

**Independent Test**: Follow each English guide on a Mac with Apple container 1.7.1 and Gantry 0.27.0.

**Acceptance Scenarios**:

1. **Given** the Kubernetes guide, **When** a visitor follows it, **Then** the visitor creates a cluster with workers and a shared image store, and browses it in Gantry.
2. **Given** the migration guide, **When** a visitor reads it, **Then** the guide maps Docker Desktop concepts to Apple container and lists what is missing.
3. **Given** the comparison guide, **When** a visitor reads the table, **Then** each fact about another product cites a page of that product.
4. **Given** any guide, **When** a search engine reads it, **Then** the page has a FAQ in JSON-LD and links to related pages.

---

### User Story 3 - Read the site in the visitor's language (Priority: P2)

A visitor reads every page in one of the 27 site languages. The terms match the terms in the app.

**Why this priority**: The site sells "28 languages". English-only pages break that promise.

**Independent Test**: Open every page in each language. Compare the main terms with the app glossaries.

**Acceptance Scenarios**:

1. **Given** a new page, **When** the site is built, **Then** the page exists in all 27 languages with hreflang links.
2. **Given** a translated page, **When** a native speaker reads it, **Then** the text reads naturally and uses the glossary terms.
3. **Given** the Serbian page, **When** the site is built, **Then** the Serbian Latin page comes from the Serbian Cyrillic text.

---

### User Story 4 - Be cited by search and AI search (Priority: P2)

A search engine or an AI assistant reads the site. It finds the new features and guides in `llms.txt`, `llms-full.txt` and the sitemap. Each page has its own title and description in each language.

**Why this priority**: The guides only help if search finds them.

**Independent Test**: Run the checks for titles, descriptions, sitemap and links.

**Acceptance Scenarios**:

1. **Given** the build is complete, **When** the checker runs, **Then** each page has a unique title and description in each language.
2. **Given** the build is complete, **When** the checker runs, **Then** the sitemap lists every page and every internal link resolves.
3. **Given** the build is complete, **When** an AI crawler reads `llms.txt`, **Then** it finds the new features and guides.

---

### Edge Cases

- A feature branch does not merge before the release. Its claims must leave the site.
- A competitor changes its prices or features before the release.
- A translated title is longer than the space in the page header.
- A guide slug must be the same in all languages.
- The existing `compare` and `apple-container-kubernetes` pages cover the same topics as two of the new guides.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The home page, the Apple container page and the Apple container Kubernetes page MUST describe the 0.27.0 features.
- **FR-002**: Each claim MUST match merged code or a listed branch. The site MUST NOT claim a part that a branch report calls missing.
- **FR-003**: The site MUST have the five guides, each in all 27 site languages.
- **FR-004**: Each guide MUST have hreflang links, a sitemap entry, a FAQ in JSON-LD, Open Graph tags and internal links.
- **FR-005**: Facts about other products MUST cite the pages of those products. The comparison MUST be fair.
- **FR-006**: Translations MUST use the reviewed app glossaries and the 0.27 glossary additions. Serbian Latin MUST come from Serbian Cyrillic.
- **FR-007**: New features with no 0.27.0 screenshot MUST have a `TODO-SCREENSHOT` marker with the section and the file name.
- **FR-008**: `llms.txt` and `llms-full.txt` MUST list the new features and guides.
- **FR-009**: All pages MUST come from the generators. No generated page is edited by hand.
- **FR-010**: A link checker MUST confirm that every internal link resolves.
- **FR-011**: Each page MUST have a unique title and description in each language.
- **FR-012**: The site MUST NOT go live and MUST NOT notify IndexNow before the 0.27.0 release.
- **FR-013**: The pages MUST work without JavaScript, in light and dark mode, and on a phone.

### Key Entities

- **Page**: slug, strings key, sitemap frequency and priority, title and description per language.
- **Guide**: a page that teaches a task, with steps, a FAQ and links.
- **Claim**: a statement about a feature, with its source (CHANGELOG, PR or branch report).
- **Screenshot placeholder**: section, file name and intended content.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100 % of the pages build in all 27 languages.
- **SC-002**: 0 internal links fail in the link checker.
- **SC-003**: 0 duplicate titles or descriptions in each language.
- **SC-004**: 100 % of the claims about 0.27.0 trace to a merged PR or a listed branch report.
- **SC-005**: A visitor can follow each English guide to the end with no other source.

## Assumptions

- The release 0.27.0 ships the four open branches. If a branch does not merge, its claims are removed before the site goes live.
- The new comparison guide and the new Kubernetes guide update or extend the existing `compare` and `apple-container-kubernetes` pages. Decision (maintainer, 2026-11-07): update the existing `compare` and `apple-container-kubernetes` pages. Do not add duplicate pages, because two pages for one search query compete.
- Real screenshots come from the maintainer after the design pass merges.
- The guides are in the `PAGES` generator (all languages). The English-only docs in `docs/` stay as they are.
