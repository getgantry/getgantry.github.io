<!-- STE deviation: spec-kit template headings, the quoted user input and paths stay verbatim. -->
# Feature Specification: Phone Layout of the Home Page

**Feature Branch**: `fix/mobile-home`

**Created**: 2026-11-16

**Status**: Done

**Input**: User description: "The mobile version is not good."

## Context

At 390 px the home page was 8,113 px tall. The command table took about 1,700 px in two narrow columns. The command rails wrapped into a block that repeated the table and the Homebrew line. Three figures stood one under the other. The gaps between sections were large.

## Requirements *(mandatory)*

- **FR-001**: At 800 px or less, each row of the command table MUST show as one card: the command, then the control. The home page shows 5 rows, and the link opens the full table.
- **FR-002**: At 800 px or less, the rails of the sections "Command to control" and "Install" MUST be hidden, because the content next to them shows the same commands.
- **FR-003**: At 800 px or less, the three figures MUST scroll sideways in one row, with the next figure partly visible.
- **FR-004**: Smaller gaps and type on phones. The desktop layout MUST not change.

## Success Criteria *(mandatory)*

- **SC-001**: The English home page at 390 px is 6,500 px tall or less (before: 8,113 px). Result: 6,421 px.
- **SC-002**: At 390 px, each home page and each features page of the 27 languages fits the screen width. Result: 0 pages too wide.
- **SC-003**: The link check shows 0 problems.
