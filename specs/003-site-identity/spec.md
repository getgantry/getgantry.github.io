<!-- STE deviation: spec-kit template headings, the quoted user input, Given-When-Then scenarios, product names, font names, commands and paths stay verbatim. -->
# Feature Specification: Site Identity ("Command and Control")

**Feature Branch**: `feat/rebrand` (stacked on `feat/landing-0-29`)

**Created**: 2026-11-15

**Status**: In Progress

**Input**: User description: "Site identity rebrand. Replace the dark premium SaaS look of getgantry.github.io with Concept A, Command and Control: an operator's manual where each apple/container or Docker command sits next to its Gantry control. Light and dark mode. Self-hosted IBM Plex Sans and JetBrains Mono. Remove the decoration and the mock UI. Fix the untrue details. New home structure in the order of the app sidebar. Keep the name, the icon, all content, the search metadata. Stacked PRs. No merge, no IndexNow ping."

## Context

The design brief is in `research.md`. It lists 24 tells that make the site look like a 2024-2026 AI-startup template, with file and line. Some of them are defects, not style:

- The home page shows a mock interface with random data next to the claim "Real screenshots, no mockups".
- The mock fleet shows 4 hosts under the label "5 hosts". The mock host names look like the real hosts of the maintainer.
- The site has no light mode. Principle V of the constitution requires light and dark mode.
- The `og:image` size in the metadata is wrong. The star count is hardcoded.

The owner chose the direction on 2026-11-15: "decide yourself and do what is best for 2026-2027". The brief recommends Concept A, and this spec uses it.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - See an honest product page (Priority: P1)

A developer opens the home page. The developer sees what Gantry is, a real screenshot of the app and the download, without scrolling at 1440 x 900. All images are real screenshots. No number or name on the page is invented.

**Why this priority**: The mock interface is a false claim (Principle II). It must go first.

**Independent Test**: Open the home page. Find every image and every number. Each image is a file in `assets/`. Each number has a source in the app or the release.

**Acceptance Scenarios**:

1. **Given** the home page, **When** a visitor looks at it, **Then** no element shows data that JavaScript invents.
2. **Given** the hero, **When** the page loads at 1440 x 900, **Then** the dashboard screenshot is visible without scrolling.
3. **Given** a command on the page such as `gantry exec`, **When** the app does not install that command, **Then** the page does not show it.

---

### User Story 2 - Read the site in light or dark mode (Priority: P1)

A visitor with a light system appearance sees a light site. A visitor with a dark appearance sees a dark site. Text contrast is 4.5:1 or more in both.

**Why this priority**: Principle V requires it, and the site does not meet it today.

**Independent Test**: Open five page types with `prefers-color-scheme: light` and `dark`. Measure the contrast of the text tokens.

**Acceptance Scenarios**:

1. **Given** a light system appearance, **When** a visitor opens any page, **Then** the page uses the light tokens.
2. **Given** a dark system appearance, **When** a visitor opens any page, **Then** the page uses the dark tokens, and the screenshots stay as they are.

---

### User Story 3 - Map a command to a control (Priority: P2)

A developer who knows `container` or `docker` commands reads the home page. Next to each area of the app, the developer sees the commands that the area replaces.

**Why this priority**: It is the identity of the new site, and it tells the truth about the product: Gantry is a window for a command-line tool.

**Independent Test**: Each command in the rail is a real command of `container`, `docker` or `kubectl`. Each command has a matching control in the text next to it.

**Acceptance Scenarios**:

1. **Given** an area such as Logs, **When** a visitor reads it, **Then** the rail shows the command, for example `container logs -f`, and the text names the Gantry control.
2. **Given** a phone at 390 px, **When** a visitor reads an area, **Then** the rail shows above the text and the page has no horizontal scroll.

---

### User Story 4 - Read the site in each language (Priority: P2)

A visitor reads the site in any of the 27 languages. All characters show in the site fonts. All new text is translated with the app terms.

**Independent Test**: A script checks each character of `i18n/*.json` against the fonts. The build check passes for all languages.

**Acceptance Scenarios**:

1. **Given** Greek, Cyrillic or Baltic text, **When** the page loads, **Then** no character falls back to a different font.
2. **Given** a new English string, **When** the site builds, **Then** the string exists in all 27 languages.

### Edge Cases

- JavaScript is off: the page shows all content, the language menu works as a link list, and nothing waits for a scroll animation.
- Fonts do not load: the system font stack shows the text with the same layout.
- A long German, Finnish or Hungarian word in a heading: the heading breaks with `hyphens` and does not overflow at 390 px.
- A screenshot already contains the real window frame: the page shows no second frame around it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: All pages MUST use one token set with light and dark values, selected by the system appearance. No manual switch.
- **FR-002**: Text MUST use IBM Plex Sans; commands, keys and table data MUST use JetBrains Mono. Both are SIL OFL 1.1, self-hosted, with a system font fallback.
- **FR-003**: A check MUST fail when a character of a site language is missing from the fonts.
- **FR-004**: The pages MUST NOT have colour glows, a grid or grain backdrop, glass panels, card walls with icon tiles, uppercase kickers, reveal-on-scroll, parallax or CSS window frames.
- **FR-005**: The home page MUST NOT show a mock interface or invented data. Every image MUST be a real screenshot.
- **FR-006**: The home page MUST be ordered by the areas of the app, with a command rail beside each area. Releases MUST be a short list of links into the areas.
- **FR-007**: The site MUST keep all current content facts, the name Gantry, the app icon, `home.title`, `home.desc`, `home.keywords`, JSON-LD, hreflang, the sitemap and the llms files.
- **FR-008**: New and changed text MUST follow the voice rules in `research.md`: one fact per sentence, no metaphor, no em-dash, no "No X. No Y. No Z.", no adjective that a test cannot check.
- **FR-009**: The `og:image` size MUST match the file. The star count MUST NOT be hardcoded in the HTML.
- **FR-010**: The work MUST be split into stacked pull requests in the order given in `plan.md`, each with its own checks.

### Key Entities

- **Area**: one part of the app (for example Containers or Logs) with a name, a short text, feature items, the rail commands and an optional figure.
- **Rail command**: a real `container`, `docker` or `kubectl` command. It is not translated.
- **Token**: a named colour with a light value and a dark value.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0 elements on the home page show invented data.
- **SC-002**: Text contrast is 4.5:1 or more for each text token in light and dark mode.
- **SC-003**: The home page at 1440 px is 15,000 px tall or less (before: 17,895 px), and no content fact is lost. The brief estimated 10,000 px; with all 70 feature items kept, the measured height is about 14,600 px.
- **SC-004**: 0 characters of the 27 languages are missing from the fonts.
- **SC-005**: At 390 px, 0 pages have a horizontal scroll.
- **SC-006**: The build check and the link check show 0 problems after each pull request.

## Assumptions

- PR #5 (`feat/landing-0-29`) merges first. This stack sits on top of it.
- The app icon and the name stay. A change of the app icon or the accent colour is a separate spec in `getgantry/gantry`.
- The screenshots stay light in both schemes. Dark screenshots come with a later release update.
- The language menu needs no JavaScript to work.
- IndexNow waits until the stack is on `main`.
