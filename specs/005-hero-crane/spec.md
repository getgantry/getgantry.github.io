<!-- STE deviation: spec-kit template headings, the quoted user input, product names, commands and paths stay verbatim. -->
# Feature Specification: Crane Animation in the Title Block

**Feature Branch**: `feat/hero-crane`

**Created**: 2026-11-16

**Status**: Done

**Input**: User description: "The animation on the old site was nice. Rewrite it for the new concept and put it on the site."

## Context

The old site had a crane animation that hid the dashboard screenshot for 3 seconds (`research.md` of spec 003, tell 15). Spec 003 removed it. The new animation tells the concept of the site: a command goes in, a running container comes out.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - See the idea in 3 seconds (Priority: P1)

A visitor opens the home page. Next to the headline, a flat crane in the colours of the icon draws itself. The trolley brings an orange container with the text `$ container run` and lowers it. On the ground the text changes to `web :8080` with a green dot.

**Acceptance Scenarios**:

1. **Given** a system that allows motion, **When** the page loads, **Then** the animation plays once in about 3.4 seconds.
2. **Given** reduced motion or no CSS animation, **When** the page loads, **Then** the last frame shows at once.
3. **Given** the page loads, **When** the animation plays, **Then** the dashboard screenshot is visible at the same time.

## Requirements *(mandatory)*

- **FR-001**: The animation MUST use CSS only. It MUST NOT need JavaScript.
- **FR-002**: The base styles MUST be the last frame, so that a browser without animation shows the result.
- **FR-003**: Colours MUST come from the site tokens, so that dark mode works.
- **FR-004**: The text in the animation MUST be commands and names only, so that it needs no translation.
- **FR-005**: The SVG MUST be `aria-hidden`, because the headline and the lead already say the same.

## Success Criteria *(mandatory)*

- **SC-001**: 0 new strings. 0 link problems. No horizontal scroll at 390 px in 27 languages.
- **SC-002**: The English home page stays under 6,000 px at 1440 px.
