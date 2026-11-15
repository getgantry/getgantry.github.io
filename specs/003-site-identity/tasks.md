---

description: "Task list for the site identity rebrand"
---

<!-- STE deviation: spec-kit template headings, task format, product names, font names and paths stay verbatim. -->
# Tasks: Site Identity ("Command and Control")

**Input**: Design documents from `/specs/003-site-identity/`

**Tests**: Build checks, a font check and a browser check in light and dark mode.

## Phase 1: Spec and facts

- [x] T001 Write spec.md, plan.md and research.md (design brief)
- [ ] T002 Check the app source for a shipped `gantry` command. Record the result in research.md

## Phase 2: PR 1, tokens, fonts and light mode (US2, US4)

- [ ] T003 [US4] Add IBM Plex Sans 400 and 600 and JetBrains Mono 400 WOFF2 subsets and `OFL.txt` to `assets/fonts/`
- [ ] T004 [US4] Add `scripts/check_fonts.py` and run it on all 27 languages
- [ ] T005 [US2] Replace the `:root` tokens in `styles.css` with the light and dark tokens. Add `color-scheme` and `@font-face`
- [ ] T006 [US2] Remove the backdrop layers from `styles.css`, `templates/home.html`, `templates/page.html` and `build_docs.py`
- [ ] T007 [US2] Replace hardcoded colours in `styles.css` and `DOCS_CSS` with tokens. Restyle the nav with the beam, the footer and the language menu
- [ ] T008 [US2] Add two `theme-color` metas. Fix the `og:image` size
- [ ] T009 Build, run the checks, look at 1440 px and 390 px in light and dark mode. Open PR 1

## Phase 3: PR 2, remove the decoration and the mock UI (US1)

- [ ] T010 [US1] Remove the crane stage, trust strip, reveal classes, icon tiles, mini mock UIs, CSS window frames, kickers and the star pill from `templates/home.html`
- [ ] T011 [US1] Reduce `app.js` to the copy handler. Remove the unused CSS
- [ ] T012 [US1] Delete the unused keys from all 27 `i18n/*.json` files with a script
- [ ] T013 Build, run the checks, open PR 2

## Phase 4: PR 3, command rail, areas and copy (US3, US4)

- [ ] T014 [US3] Write the new home outline in `templates/home.html` and the data in `build_pages.py`
- [ ] T015 [US3] Write the new English strings
- [ ] T016 [US4] Translate the new and changed strings into 25 languages. Make Serbian Latin from Serbian Cyrillic
- [ ] T017 Build, run the checks, compare the content facts with `main`, open PR 3

## Phase 5: PR 4, images and inner pages

- [ ] T018 Add `scripts/make_images.py` and `picture` with `srcset` in `shot()`
- [ ] T019 Restyle the guides, the compare page and the docs. Make a 1200 x 630 `og:image`
- [ ] T020 Build, run the checks, open PR 4

## Phase 6: PR 5, voice pass (optional)

- [ ] T021 Rewrite the older feature strings in the voice of research.md and translate them
