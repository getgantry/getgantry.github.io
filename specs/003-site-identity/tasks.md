---

description: "Task list for the site identity rebrand"
---

<!-- STE deviation: spec-kit template headings, task format, product names, font names and paths stay verbatim. -->
# Tasks: Site Identity ("Command and Control")

**Input**: Design documents from `/specs/003-site-identity/`

**Tests**: Build checks, a font check and a browser check in light and dark mode.

## Phase 1: Spec and facts

- [x] T001 Write spec.md, plan.md and research.md (design brief)
- [x] T002 Remove the `gantry exec` line. The new home page has no mock terminal, so the claim is gone whatever the app ships

## Phase 2: PR 1, design system and new home page (US1, US2, US3, US4)

- [x] T003 [US4] Add IBM Plex Sans 400 and 600 and JetBrains Mono 400 WOFF2 subsets and the two OFL files to `assets/fonts/`
- [x] T004 [US4] Add `scripts/check_fonts.py`. Result: 27 languages, 0 missing letters. Six symbols use the system font
- [x] T005 [US2] Write `styles.css` with light and dark tokens, `@font-face`, the beam, the rail, tables, figures, FAQ and footer
- [x] T006 [US2] Remove the backdrop layers from `templates/home.html`, `templates/page.html` and `build_docs.py`
- [x] T007 [US2] Move `DOCS_CSS` to the tokens. Remove glass, gradients and hardcoded colours
- [x] T008 [US2] Add two `theme-color` metas. Set the `og:image` size to 3104 x 1986
- [x] T009 [US1] Remove the crane stage, trust strip, reveal classes, icon tiles, mock UIs, CSS window frames, kickers, star count and `app.js`
- [x] T010 [US3] Write the new home page: title block, command table from `guide.table`, areas with the command rail, releases, install, FAQ, colophon
- [x] T011 [US3] Write the new English strings (`home.ia`) and change the hype strings. Delete the unused keys
- [ ] T012 [US4] Translate 35 new or changed strings into 25 languages. Make Serbian Latin from Serbian Cyrillic
- [ ] T013 Build, run the checks, look at 1440 px and 390 px in light and dark mode in en, de, ru, el, fi. Open PR 1

## Phase 3: PR 2, images

- [ ] T014 Add `scripts/make_images.py` and `picture` with `srcset` in `shot()`
- [ ] T015 Make a 1200 x 630 `og:image`

## Phase 4: PR 3, voice pass (optional)

- [ ] T016 Rewrite the older strings of the docs and the guides in the voice of research.md and translate them
