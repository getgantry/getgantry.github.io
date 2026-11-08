---

description: "Task list for the Gantry 0.27.0 landing update"
---

<!-- STE deviation: spec-kit template headings, task format, product names, page titles and paths stay verbatim. -->
# Tasks: Landing Update for Gantry 0.27.0

**Input**: Design documents from `/specs/001-landing-027/`

**Prerequisites**: plan.md, spec.md

**Tests**: Required as build checks. The constitution asks for a check that every page builds and that all internal links resolve.

**Organization**: Tasks are grouped by user story.

**Status note**: The implementation started before this list. All tasks are open, because nobody checked the result against this list yet. Tick a task only after you check its result on branch `feat/landing-027`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: The user story of the task (US1 to US4)

## Phase 1: Setup (Facts and Sources)

- [x] T001 Read build_pages.py, build_docs.py, templates/ and i18n/en.json. Write down how hreflang, the sitemap, llms.txt, JSON-LD and Open Graph tags are built.
- [x] T002 [P] Collect the 0.27.0 facts from ~/PycharmProjects/docker-watch/CHANGELOG.md, PRs #47 to #55 and /Volumes/SanDisk2Tb/builds/gantry-027/*/REPORT.md into a claims list with a source for each claim
- [x] T003 [P] Collect the current facts of Docker Desktop, OrbStack and Podman Desktop from their own pages, with links

---

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T004 Write the link checker with checks for unique titles, unique descriptions, sitemap entries and hreflang in scripts/check_links.py
- [x] T005 Decide if the comparison and Kubernetes guides update the existing pages or are new pages (open question in spec.md)

---

## Phase 3: User Story 1 - What Gantry 0.27.0 does (Priority: P1) (MVP)

**Goal**: Exact 0.27.0 claims on the home page and the two product pages.

- [x] T006 [US1] Update the feature sections in templates/home.html and the `home` keys in i18n/en.json
- [x] T007 [P] [US1] Update templates/apple-container.html and the `guide` keys in i18n/en.json for 1.7.1 support
- [x] T008 [P] [US1] Update templates/apple-container-kubernetes.html and the `k8s` keys in i18n/en.json for the native client, workers and the shared image store
- [x] T009 [US1] Add `TODO-SCREENSHOT` markers with section and file name for each new feature in the templates
- [x] T010 [US1] Check each claim against the claims list from T002

---

## Phase 4: User Story 2 - How-to guides (Priority: P1)

**Goal**: Five guides that teach a real task.

- [x] T011 [US2] Add the five guide slugs to `PAGES` in build_pages.py
- [x] T012 [P] [US2] Write the English guide "Run Kubernetes on a Mac with Apple container" in i18n/en.json and its template in templates/
- [x] T013 [P] [US2] Write the English guide "Move from Docker Desktop to Apple container" in i18n/en.json
- [x] T014 [P] [US2] Write the English guide "Gantry vs Docker Desktop vs OrbStack vs Podman Desktop" with cited facts in i18n/en.json and templates/compare.html
- [x] T015 [P] [US2] Write the English guide "Store containers and volumes on an external drive on a Mac" in i18n/en.json
- [x] T016 [P] [US2] Write the English guide "Create a container from a docker run command" in i18n/en.json
- [x] T017 [US2] Add a FAQ in JSON-LD and internal links to each guide in build_pages.py

---

## Phase 5: User Story 3 - Every language (Priority: P2)

**Goal**: All new and changed strings in 26 more languages.

- [x] T018 [US3] Translate the new and changed keys into each i18n/<lang>.json with /Volumes/SanDisk2Tb/builds/l10n/reviewed/<lang>.glossary.md and /Volumes/SanDisk2Tb/builds/l10n-027*/out/<lang>.glossary-add.md
- [x] T019 [US3] Check that Serbian Latin comes from i18n/sr.json through the transliteration
- [x] T020 [US3] Run the key check of build_pages.py and fix missing or extra keys in each language

---

## Phase 6: User Story 4 - Search and AI search (Priority: P2)

- [x] T021 [US4] Add the new features and guides to the llms output in build_pages.py
- [x] T022 [US4] Run build_docs.py and build_pages.py
- [x] T023 [US4] Run scripts/check_links.py and fix every failure

---

## Phase 7: Polish & Cross-Cutting Concerns

- [x] T024 Check the pages without JavaScript, in light and dark mode, and at phone width
- [x] T025 Commit on `feat/landing-027` with Conventional Commits and push the branch. Keep the branch unmerged. Send no IndexNow request.
- [x] T026 Write /Volumes/SanDisk2Tb/builds/gantry-027/landing/REPORT.md
- [x] T027 Before the merge, remove the claims of any app branch that is not in the 0.27.0 release, and add the real screenshots

---

## Dependencies & Execution Order

- Phase 1 comes first. T002 blocks T006 to T010. T003 blocks T014.
- T005 blocks T012 and T014.
- US2 needs T011 before the build.
- US3 comes after the English text of US1 and US2 is final.
- US4 comes after US3.
- T027 waits for the app release.

## Parallel Example: User Story 2

```bash
Task: "Write the Kubernetes guide"
Task: "Write the migration guide"
Task: "Write the external drive guide"
Task: "Write the docker run guide"
```

## Implementation Strategy

1. MVP: Phases 1 and 2, then User Story 1.
2. Add User Story 2 in English.
3. Translate (User Story 3), then build and check (User Story 4).
4. Phase 7. The merge waits for the release.
