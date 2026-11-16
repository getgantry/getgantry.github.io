<!-- STE deviation: spec-kit template headings, the quoted user input, Given-When-Then scenarios, product names, page titles and paths stay verbatim. -->
# Feature Specification: Landing Update for Gantry 0.29.0

**Feature Branch**: `feat/landing-0-29`

**Created**: 2026-11-15

**Status**: In Progress

**Input**: User description: "Update the Gantry landing site for 0.29.0. Releases 0.28.0 and 0.29.0 added eight features: fleet activity table (spec 006), log export (spec 007), export as Compose (spec 008), screenshots in Explain (spec 009), build history (spec 010), image scan and SBOM with Trivy or Grype (spec 011), Keychain secrets in the container environment (spec 012), pull, build and compose progress in the menu bar (spec 013). Describe only what the code does. New screenshots from the Debug app with demo data, the missing paste-command.png and a new fleet.png. All languages. Keep hreflang, sitemap.xml, llms.txt and JSON-LD correct. Open a pull request, do not merge, no IndexNow ping."

## Context

The site describes Gantry 0.27.0. Release 0.28.0 (2026-11-14) and release 0.29.0 (2026-11-15) are published. The specs of the eight features are in the app repository (`specs/006-*` to `specs/013-*`), and the pull requests are #66 to #73. The screenshot `paste-command.png` of the guide "Create a container from a docker run command" was never made, so that guide has a `TODO-SCREENSHOT` marker. The image `assets/fleet.png` shows the old design and real host names of the maintainer.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Learn what 0.28.0 and 0.29.0 add (Priority: P1)

A visitor opens the home page in any site language and sees the eight new features, each with a short exact description. The main ones have a real screenshot.

**Why this priority**: The home page gets the most visits and must match the published release.

**Independent Test**: Read the home page in English and in two other languages. Compare each claim with the claims list (research.md), which cites the app code and the pull requests.

**Acceptance Scenarios**:

1. **Given** release 0.29.0, **When** a visitor opens the home page, **Then** a section lists the eight features of 0.28.0 and 0.29.0.
2. **Given** a spec item that the code does not do (a deferred task), **When** the site describes that feature, **Then** the site does not claim that item.
3. **Given** the 0.27.0 feature cards, **When** the page is rebuilt, **Then** they stay on the page (no content is lost).

---

### User Story 2 - Use a new feature from a guide (Priority: P2)

A visitor reads a guide or a docs page and finds the steps for a new feature where the task fits: export as Compose in the docker run and Docker Desktop guides, Keychain secrets in the New Container steps, image scan, build history and log export in the docs.

**Independent Test**: Follow each new step in the Debug build of 0.29.0. Each named button and menu item exists.

**Acceptance Scenarios**:

1. **Given** the guide "Create a container from a docker run command", **When** a visitor opens it, **Then** it shows `paste-command.png` and no `TODO-SCREENSHOT` marker.
2. **Given** a guide step names a UI control, **When** the visitor looks in the app, **Then** the control has that name in the visitor's language (app catalog `App/Localizable.xcstrings`).

---

### User Story 3 - Real screenshots with demo data (Priority: P1)

The new screenshots come from the Debug build of 0.29.0 with demo containers (web, api, postgres, redis). They show no real host name, IP address, path or secret of the maintainer.

**Independent Test**: Look at each PNG in `assets/shots/0.29.0` and at `assets/fleet.png`.

**Acceptance Scenarios**:

1. **Given** the Keychain secrets screenshot, **When** a visitor looks at it, **Then** it shows a masked field and a dummy secret name.
2. **Given** a screenshot PNG, **When** its size is compared with the 0.27.0 set, **Then** it is of the same order (about 1 MB or less).

---

### User Story 4 - Search and AI search stay correct (Priority: P2)

**Acceptance Scenarios**:

1. **Given** the build, **When** `scripts/check_links.py` runs, **Then** all internal links resolve, titles and descriptions are unique, and every page has hreflang links and a sitemap entry.
2. **Given** `llms.txt`, `llms-full.txt` and the JSON-LD `featureList`, **When** a crawler reads them, **Then** they list the new features and version 0.29.0.

### Edge Cases

- A feature works only on Docker hosts or only on Apple container hosts: the text says which.
- A feature needs an external tool (Trivy or Grype): the text says so.
- A language has no app translation for a feature name: use the glossary term and the English name.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The home page MUST describe the eight features of 0.28.0 and 0.29.0 in every site language.
- **FR-002**: Each claim MUST match the app code at tag `v0.29.0`. Deferred spec items MUST NOT be claimed.
- **FR-003**: UI names on the site MUST be the names of the app catalog in each language.
- **FR-004**: Screenshots MUST come from the real app window with demo data only, and MUST go to `assets/shots/0.29.0`. `paste-command.png` and a new `assets/fleet.png` MUST exist.
- **FR-005**: The version on the site (JSON-LD `softwareVersion`, text) MUST be 0.29.0, because release `v0.29.0` exists.
- **FR-006**: hreflang links, `sitemap.xml`, `llms.txt`, `llms-full.txt` and JSON-LD MUST stay correct for all pages.
- **FR-007**: No page MUST lose content, except text that is no longer true.
- **FR-008**: The pages MUST work at phone width, and all images MUST load.

### Key Entities

- **Claims list**: one row for each claim, with its source (spec, pull request, code path).
- **Screenshot**: file, page and section, content, demo data used.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 8 of 8 features appear on the home page in 27 of 27 languages.
- **SC-002**: 0 `TODO-SCREENSHOT` markers in the built pages.
- **SC-003**: The site checker reports 0 failures.
- **SC-004**: 0 real host names, IP addresses, user paths or secret values in the new images.
- **SC-005**: No built page has less text than before, except where a claim was corrected.

## Assumptions

- The 0.27.0 screenshots are light mode only, so the new set is light mode only.
- The 0.27.0 feature cards stay on the home page in a section with a new heading.
- A Docker host for the Docker-only screenshots is a remote Docker test host, with containers named `landing-*` that are removed at the end. The host name does not appear in an image.
- The docs (`docs/`, English only) get the new features too.
- Merge and IndexNow are the decision of the maintainer and are out of scope.
