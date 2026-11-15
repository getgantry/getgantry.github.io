---

description: "Task list for the Gantry 0.29.0 landing update"
---

<!-- STE deviation: spec-kit template headings, task format, product names, page titles and paths stay verbatim. -->
# Tasks: Landing Update for Gantry 0.29.0

**Input**: Design documents from `/specs/002-landing-029/`

**Tests**: Build checks and a browser check, as the constitution tells.

## Phase 1: Release check, Debug build and claims

- [x] T001 Check the release with `gh release view v0.29.0 -R getgantry/gantry`
- [x] T002 Build the Debug app from `origin/main` into `/Volumes/SanDisk2Tb/builds/gantry/landing-029/DerivedData`
- [x] T003 [P] Write the claims of specs 006 to 013 and PRs #66 to #73 in research.md

## Phase 2: Screenshots (US3)

- [x] T004 [US3] Make the demo containers and a test host list
- [x] T005 [US3] Capture `assets/shots/0.29.0/fleet-activity.png`
- [x] T006 [US3] Capture `assets/shots/0.29.0/menu-bar-progress.png`
- [x] T007 [US3] Replace `assets/fleet.png` with the new dashboard
- [ ] T008 [US3] Capture `assets/shots/0.29.0/paste-command.png`. Blocked: the sheet needs a click (see research.md).
- [ ] T009 [US3] Capture the sheets of image scan, Export as Compose, Explain Failure and a Keychain secret row. Blocked for the same reason as T008.
- [x] T010 [US3] Quit the Debug app. Remove the demo containers, the socket forward and `/tmp/landing-*` on a remote Docker test host.

## Phase 3: English content (US1, US2)

- [x] T011 [US1] Add the section `#latest` to `templates/home.html` and `home.latest` to `i18n/en.json`
- [x] T012 [US1] Add the eight features to `home.ld.features`
- [x] T013 [US1] Set `APP_VERSION` and `UPDATED` in `build_pages.py`
- [x] T014 [US1] Update the text and the size of the fleet screenshot
- [x] T015 [US2] Extend the rows of `guide.table`
- [x] T016 [US2] Add the sections `#compose` and `#secrets` to the guide `docker-run-to-container`
- [x] T017 [US2] Add the Compose export note to the guide `docker-desktop-to-apple-container`
- [x] T018 [US2] Update the docs in `build_docs.py`: menu bar, containers, images and Compose, index
- [x] T019 [US4] Update `llms.txt`

## Phase 4: Languages (US1)

- [x] T020 [US1] Translate the new and changed strings into 25 languages with `build/i18n/<lang>.ui.json` and the glossaries
- [x] T021 [US1] Merge each language with `scripts/i18n_delta.py apply`
- [x] T022 [US1] Run `python3 build_pages.py --check`

## Phase 5: Build and check (US4)

- [x] T023 [US4] Run `build_docs.py` and `build_pages.py`
- [x] T024 [US4] Run `scripts/check_links.py`. Result: 0 problems. One marker stays for `paste-command.png` (T008).
- [x] T025 Open the pages in the Orca browser at desktop width and phone width. Make sure that all images load. Result: 9 pages at 390 px, no broken image, no horizontal scroll.
- [x] T026 Compare the text length of each page with `main`. Make sure that no page lost text. Result: 201 pages, 0 shorter.

## Phase 6: Pull request

- [ ] T027 Commit with Conventional Commits and open the pull request. Keep it unmerged. Send no IndexNow request.
