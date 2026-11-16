<!-- STE deviation: this whole file is an internal design brief, not site text. Quoted site copy, sample copy, product names (apple/container), CSS values, table cells and dense specification lines stay verbatim and are not held to ASD-STE100 sentence rules. -->
# Gantry site rebrand: diagnosis, three concepts, plan

Scope: the site's visual identity, layout and voice. The name Gantry, the app icon and the app stay.
Read from branch `feat/landing-0-29` (PR #5). Paths are relative to the repo root.
Rendered check: Playwright, 1440 px and 390 px (screenshots not committed).

Measured facts used below:

- Home page height: 17,895 px at 1440 px wide, 27,268 px at 390 px wide.
- `templates/home.html` has 57 `reveal` elements and 31 icon tiles (`class="ico"`).
- `i18n/en.json`: 1,063 strings in total, 299 under `home`. The `home` strings contain 27 em-dashes.
- `styles.css` and `docs/docs.css` contain no `prefers-color-scheme` rule. The site is dark only.

---

## 1. Diagnosis: why the site reads as AI-made

The page is the 2024-2026 "dark premium SaaS" template, complete to the last part. A visitor who has seen
twenty such pages recognises it in one second, before reading a word. The parts:

### 1.1 Visual template

| # | Tell | Evidence |
|---|------|----------|
| 1 | The stylesheet names its own genre: "dark, premium". | `styles.css:2` |
| 2 | Three fixed backdrop layers: radial colour glows, a 64 px grid with a radial mask, SVG noise grain. On every page, the docs too. | `styles.css:63-94`; `templates/home.html:51-53`; `templates/page.html:38-40`; `build_docs.py:484-486` |
| 3 | Gradient-clipped word in the headline (white to blue to orange). | `styles.css:201-204`; `i18n/en.json:288` (`<span class="grad">`) |
| 4 | Pill "eyebrow" with a gradient badge above a centred 5.2 rem headline with -0.035em tracking. | `styles.css:177-200`; `templates/home.html:92-95` |
| 5 | Glass: translucent white panels at 3.5 to 9 % alpha, `backdrop-filter` blur on the nav, the ghost button and the replay button. | `styles.css:10-14`, `108-112`, `170`, `357` |
| 6 | Bento grid of 24 px-radius cards, each with a gradient icon tile, a hover lift and a cursor-following radial spotlight. Used three times in a row for 31 cards. | `styles.css:395-423`; `app.js:83-90`; `templates/home.html:179`, `234`, `293` |
| 7 | Uppercase orange "kicker" over every H2, 8 times. | `styles.css:382-386`; `templates/home.html:174`, `229`, `288`, `460`, `488`, `527`, `567`, `584` |
| 8 | Reveal-on-scroll with staggered delays on 57 elements, plus scroll parallax on screenshots. | `styles.css:626-628`; `app.js:71-81`, `92-111` |
| 9 | Glowing gradient CTA with an inset highlight and a coloured shadow; a blurred orange "glow floor" under the hero. | `styles.css:160-165`, `364-369` |
| 10 | Two "glow panels" with 32 px radius and corner radial gradients (apple/container and install). | `styles.css:483-493`, `557-567` |
| 11 | Fake macOS window chrome (three traffic-light dots) drawn in CSS around images, 5 times. | `styles.css:313-333`; `templates/home.html:134-143`, `494-498`, `534-555` |
| 12 | Blinking terminal cursor and a self-scrolling log. | `styles.css:479-480`; `app.js:183-218` |
| 13 | Generic 24 px stroke icons, one per card. They carry no information; a different icon would fit as well. | `templates/home.html:181-447` |
| 14 | "Trust strip": an uppercase line plus six invented glyphs for Docker, OrbStack, Colima, Kubernetes. These are not the products' marks. | `templates/home.html:156-168`; `styles.css:372-376` |
| 15 | The crane animation is the one original idea, but it is executed as a product-launch stunt: a 3-second hoist, a "container skin" that fades, a Replay button. It delays the screenshot, which is the real argument. | `templates/home.html:111-150`; `styles.css:239-362`; `app.js:17-31` |

### 1.2 Things that are worse than a style problem

| # | Problem | Evidence |
|---|---------|----------|
| 16 | **Mock UI with invented data, next to the claim "Real screenshots, no mockups".** The fleet card is built in JavaScript with `Math.random()` sparklines; the stats card shows a fixed `6.7%` and `1.42 GB`; the log lines are a script. | `app.js:136-145`, `148-181`, `184-195`; `templates/home.html:351`, `355`; claim at `i18n/en.json:397` |
| 17 | The mock fleet list shows 4 hosts under a label that says "5 hosts" and "5 need attention". | `app.js:148-153`; `i18n/en.json:305-306` |
| 18 | The mock host names (`Nettop`, `dedic`, `SuperSet`) look like the maintainer's real hosts. Spec 002 replaced `assets/fleet.png` for this reason; the JavaScript list stayed. | `app.js:149-152`; `specs/002-landing-029/spec.md` (Context) |
| 19 | The mock terminal runs `gantry exec clickhouse-server-1`. If the app ships no `gantry` command, this is an untrue claim (Principle II). | `templates/home.html:371` |
| 20 | Double window chrome: `assets/dashboard.png` already contains the real window with its traffic lights and shadow. The hero puts it inside the CSS fake window with a second title bar. | `templates/home.html:134-142`; `assets/dashboard.png` |
| 21 | No light mode. Principle V requires light and dark. `theme-color` is fixed to `#060a10`. The app screenshots are light, so they sit in a dark page as white slabs. | `.specify/memory/constitution.md` (V); `templates/home.html:40`; `styles.css` (no `prefers-color-scheme`) |
| 22 | `og:image` declares 3364 x 2116; the file is 3104 x 1986. | `templates/home.html:32-33` |
| 23 | Hardcoded star count `★ 16` (live value was 90 on 2026-11-15) and an untranslated `Copy` button. Without JavaScript the page shows the stale number. | `templates/home.html:76`, `497` |
| 24 | Weight: six PNG files of about 1 MB each at 3104 px wide, shown at 1080 px or less. | `assets/`, `assets/shots/0.27.0/` |

### 1.3 Copy template

The English text has two authors. Text added in 0.27 to 0.29 is dry, exact and translatable (for example
`home.latest.*`, `i18n/en.json:428` onward). The older text is launch-page boilerplate. The seam between them
is itself a tell.

| Pattern | Evidence (`i18n/en.json`) |
|---------|---------------------------|
| Triple fragment "No X. No Y. No Z." | `:289` "No Electron. No subscription. No limits."; `:410` "No web wrappers. No daemons of our own." |
| Three-chip status line | `:287` "Supports apple/container 1.7.1. Open source. Agent-ready." |
| Em-dash plus metaphor headline | `:288` "... and Docker — your whole fleet on one deck." |
| Hype idiom | `:315` "Logs on steroids"; `:409` "Built different"; `:413` "sips memory"; `:351` "perfect for" |
| Category words with no content | `:301` "The control plane"; `:303` "A complete, focused command center ... fast to the point of feeling local even when it isn't" |
| "Built to be X" / "Designed to feel like Y" | `:380` "Built to be driven by AI"; `:396` "Designed to feel like it shipped with the OS" |
| Drama headline | `:325` "Know the moment it breaks" |
| Section labels from the template | `:395` "A closer look"; `:379` "Agent-ready"; `:422` "Install in a minute"; `:297` "Works with everything you already run" |
| Superlatives that nobody can check | `:413` "Launches instantly"; `:303` "live by default" |

### 1.4 Structure

- The page is ordered by the history of the project, not by the reader's question: "New in 0.28 and 0.29",
  then "New in 0.27.0", then "Features". Three card walls describe one product three times
  (`templates/home.html:171`, `226`, `285`). Explain Failure and Compose each appear in two walls.
- The strongest fact about the product is not shown as an idea anywhere: Apple's `container` is a command-line
  tool, and Gantry gives each command a control. The data for this exists and is translated
  (`guide.table` in `i18n/en.json`, used only on `/apple-container/`).
- The 19 apple/container items (`home.apple.items`) are the most concrete content on the page. They sit
  inside a glow panel at 0.92 rem.

**Summary.** The page hides a precise, honest, deeply technical product behind the costume of a funded
startup. The fix is not a new palette. Remove the costume and let the precision be the identity.

---

## 2. Three concept directions

Common to all three: static HTML and CSS, tokens for light and dark through `prefers-color-scheme`, no
decoration that needs JavaScript, real screenshots only, no fake chrome, no mock UI, the 27 languages.

Font coverage was checked against the Google Fonts subset lists on 2026-11-15:

| Font | Licence | latin-ext | cyrillic | greek |
|------|---------|-----------|----------|-------|
| IBM Plex Sans | SIL OFL 1.1 | yes | yes | yes |
| IBM Plex Mono | SIL OFL 1.1 | yes | yes | **no** |
| IBM Plex Sans Condensed | SIL OFL 1.1 | yes | partial | **no** |
| JetBrains Mono | SIL OFL 1.1 | yes | yes | yes |
| Sofia Sans, Sofia Sans Condensed, Sofia Sans Extra Condensed | SIL OFL 1.1 | yes | yes | yes |
| Source Serif 4 | SIL OFL 1.1 | yes | yes | yes |

Before a font ships, a script must check its `cmap` against every character in the 27 string files.

---

### Concept A: "Command and Control" (the operator's manual)

**Idea.** `container` is a command-line tool, and Gantry is the control panel for it; so the site is the
operator's manual that puts each command next to its control.

**Positioning line.** "Every `container` command has a control in Gantry."

**Voice.** Simplified Technical English, the voice that the 0.27 to 0.29 text already has. Short declarative
sentences. One fact per sentence. Version numbers, key names and command names are the persuasion.

| Do | Don't |
|----|-------|
| "Gantry reads `docker buildx history` on Docker hosts (buildx 0.23.0 or later)." | "Powerful build insights at your fingertips." |
| "Not notarized yet. Right-click the app and choose Open." | "Install in a minute." |
| "apple/container has no `compose` command. Gantry runs your `docker-compose.yml`." | "Compose, anywhere." |

Rules: no em-dash, no metaphor, no "No X. No Y. No Z.", no adjective that a test cannot check. A heading names
a thing ("Logs"), not a feeling.

**Typography.**

- Text and headings: **IBM Plex Sans** (SIL OFL 1.1), weights 400 and 600, self-hosted WOFF2 with
  `unicode-range` subsets (latin, latin-ext, cyrillic, greek). A visitor loads 1 or 2 files of about 20 to 40 kB.
- Commands, keys, table data: **JetBrains Mono** (SIL OFL 1.1), weight 400. It has Greek; IBM Plex Mono does not.
- Scale (rem): 0.8125 mono and captions, 1.0 body with 1.55 line height, 1.25 lead, 1.0625 h3 (600), 1.75 h2
  (600), `clamp(2rem, 4.2vw, 3.25rem)` h1 (600, tracking -0.01em, line height 1.1). Left-aligned everywhere.
  No uppercase labels; section numbers do that job.

**Colour tokens.**

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `--paper` | `#FFFFFF` | `#0E1318` | page |
| `--panel` | `#F2F4F6` | `#151C23` | code, table head, title block |
| `--ink` | `#0B2942` | `#E8EDF2` | text, headings, the beam (icon navy) |
| `--ink-2` | `#4A525C` | `#9AA7B4` | secondary text |
| `--rule` | `#D5D9DE` | `#2A333D` | hairlines |
| `--signal` | `#C2500A` | `#FF9D52` | links, section numbers (4.7:1 on white) |
| `--crane` | `#F6863A` | `#F6863A` | filled marks only, never text (icon orange) |

No gradient, no shadow except the shadow inside the screenshots, radius 4 px at most.

**Layout and grid.** 12 columns, 1120 px maximum, 8 px baseline. Columns 1 to 3 are the **rail**; columns 4 to
12 are the text. Sections are separated by a 2 px ink rule and a number (`01`, `02`). Features are definition
lists and tables, not cards. Below 800 px the rail becomes one mono line above its text.

**Signature element: the command rail.** The left rail shows, in mono, the command or commands that the
feature on its right replaces: `container cluster create` next to Clusters, `docker -H ssh://` next to SSH
hosts, `kubectl get pods` next to the Kubernetes browser. Commands are not translated, so the rail costs no
translation. The page frame repeats the app icon without drawing a crane: a 6 px ink bar under the nav is the
beam, and the rail's vertical hairline is the cable.

**Screenshots.** Unframed, because the PNG files already contain the real window. Numbered figures
("Fig. 3") with a caption in the rail. Static, no parallax. In dark mode they stay as they are.

**Home outline.**

0. Beam nav: icon, Gantry, 5 links, language menu, Download.
1. Title block: h1, lead, the `brew` line and the Download button; beside it a fact table (version 0.29.0,
   release date, macOS 26 or later, MIT, apple/container CLI 1.0 to 1.7.1, 28 UI languages). Fig. 1: the dashboard.
2. `01` What it manages: three rows (apple/container on this Mac, Docker on this Mac, Docker over SSH).
3. `02` Command to control: 8 to 10 rows from `guide.table`, with a link to the full table.
4. `03` to `09` The app by area, in the order of the app sidebar: Containers; Images and builds; Compose;
   Kubernetes; Hosts and fleet; Logs; Menu bar and macOS. Each area: rail, one paragraph, a definition list of
   the existing feature items, one figure where a screenshot exists.
5. `10` apple/container coverage: the 19 items as a two-column definition list.
6. `11` Agents: the `claude mcp add` block, the tool list, Copy as Prompt.
7. `12` Releases: 0.29.0, 0.28.0, 0.27.0 as three lines of links into the areas. This replaces both "New" walls.
8. `13` How it is built: four facts as a table.
9. `14` Install: three numbered steps; the "not notarized yet" note as a plain callout.
10. `15` Questions: the 21 `details` items. FAQ JSON-LD unchanged.
11. Colophon: licence, font credits, links, the language list.

**Sample copy.**

- H1: "The Mac app for Apple container and Docker"
- Subhead: "Apple's `container` tool runs Linux containers on Apple silicon, and it has no window. Gantry is
  the window: containers, images, Compose projects, Kubernetes clusters and logs, next to your Docker hosts.
  Free, open source, MIT licence."
- Headings: "Command to control" · "Hosts and fleet" · "What Gantry does not do yet"
- Feature paragraph (Logs): "Follow the log of a container or of a whole Compose project. Search with text or
  a regular expression, and filter by level from Error to Trace. The buffer holds 50,000 lines. **Export
  Logs…** (⇧⌘E) saves the lines that you see, with the filter and the time range, as a `.log` or `.txt` file."

**Risks.** It can look like documentation, so a first-time visitor may not see a product: Fig. 1 must be above
the fold at 1440 x 900. IBM Plex is well known; the structure must carry the identity, not the typeface. The
rail needs care at 390 px. A dry voice needs one warm, plain sentence in the lead, or it reads as cold.

---

### Concept B: "Yard" (terminal signage)

**Idea.** A gantry crane works in a container yard, where everything is labelled to be read from 50 metres;
the site borrows that marking system, and each feature is a marked box in a stowage plan.

**Positioning line.** "The crane for the containers on your Mac."

**Voice.** Signage: a verb and an object. Loud headings, quiet body text.

| Do | Don't |
|----|-------|
| "Run. Stop. Inspect." as a heading over three exact paragraphs | "Unleash your containers" |
| "Bay 04: Kubernetes" | "Next-gen orchestration" |
| "Load a compose file. Gantry starts the services in `depends_on` order." | "Smooth sailing for your stack" (a pun does not survive 26 translations) |

**Typography.** Display: **Sofia Sans Extra Condensed** 800, uppercase, `clamp(3.5rem, 11vw, 9rem)`, line
height 0.9. Text: **Sofia Sans** 400 and 600, 1.0625 rem. Marking plates and commands: **JetBrains Mono**. All
SIL OFL 1.1 with Latin Extended, Cyrillic and Greek.

**Colour tokens.**

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `--ground` | `#ECEAE4` | `#16181A` | page (concrete, asphalt) |
| `--slab` | `#FFFFFF` | `#202326` | blocks |
| `--ink` | `#16181A` | `#F2F0EA` | text |
| `--ink-2` | `#55595E` | `#A3A7AB` | secondary text |
| `--crane` | `#F26A1B` | `#FF7A2B` | large fills, display type |
| `--navy` | `#0B2942` | `#7FB2E5` | second container colour, links |
| `--mark` | `#FFD400` | `#FFD400` | one hazard stripe per page, at Install |

**Layout and grid.** A strict grid of 2:1 modules with container proportions. Blocks are flat colour slabs
with square corners and 2 px gaps, stacked like a yard seen from above. Full-bleed colour bands.

**Signature element: the marking plate and the bay plan.** Each block has a plate in the style of ISO 6346
markings: `GNTU 029 · APPLE/CONTAINER · CLI 1.7`. The feature index is a stowage plan: a grid of slots, one
per feature, filled orange for apple/container, navy for Docker, split for both. It is a true capability matrix.

**Screenshots.** Full-bleed on an orange or navy slab, no shadow, a plate as the caption.

**Home outline.** (1) Slab hero: giant "GANTRY", one line, Download, the dashboard screenshot cropping into
the next band. (2) Bay plan. (3) Bays 01 to 07, one per app area, alternating slab colours. (4) apple/container
manifest: the 19 items as a tally table. (5) Agents bay. (6) Install, with the hazard stripe. (7) Questions.
(8) Footer as a large marking plate.

**Sample copy.**

- H1: "GANTRY" with the line "Lifts Apple container and Docker on your Mac."
- Subhead: "A free, open-source Mac app for Apple's `container` tool and for Docker hosts, local or over SSH."
- Headings: "Bay 01: Containers" · "Stowage plan" · "Lift it onto your Mac"
- Feature paragraph: "Bay 03: Compose. apple/container has no `compose` command. Gantry reads your
  `docker-compose.yml`, builds the images, creates the network and the volumes, and starts each service in
  `depends_on` order."

**Risks.** The highest risk of the three. It can become a theme park. Condensed uppercase breaks with long
German, Finnish and Hungarian words, and Greek capitals drop their accents. The loud page fights the quiet,
Apple-native screenshots, so the site and the app look like two brands. The metaphors ("bay", "lift") need 26
careful translations. Brutalist slabs are a recognisable 2025 trend of their own.

---

### Concept C: "Same Window" (the site is laid out like the app)

**Idea.** The site has no visual brand of its own: it uses the app's information architecture and the
system's own type and colours, so that the site feels like the first screen of the app.

**Positioning line.** "A Mac app that looks like one."

**Voice.** Apple Human Interface Guidelines style: name the control and say what it does.

| Do | Don't |
|----|-------|
| "Choose **Export as Compose…** on one or more containers." | "Effortlessly export" |
| "Containers" as a heading | "Container management, reimagined" |
| "Requires macOS 26 or later." | "Built for the future of macOS" |

**Typography.** System fonts only: `-apple-system, system-ui` and `ui-monospace`. No font files. Scale: 1.0625
rem body, 1.375 h2, 2.5 h1, weight 600 at most. Coverage of all 27 languages comes from the operating system.

**Colour tokens.** macOS semantic colours.

| Token | Light | Dark |
|-------|-------|------|
| `--window` | `#FFFFFF` | `#1E1E1E` |
| `--sidebar` | `#F5F5F7` | `#2A2A2C` |
| `--label` | `#1D1D1F` | `#F5F5F7` |
| `--label-2` | `#6E6E73` | `#A1A1A6` |
| `--separator` | `#D2D2D7` | `#3A3A3C` |
| `--accent` | `#C2500A` | `#FF9D52` |

**Layout and grid.** Two panes. A sticky sidebar of 240 px lists the items of the app sidebar: Dashboard,
Kubernetes, Overview, Containers, Images, Volumes, Networks, Machines, Clusters, System. The content pane
(720 px text, 960 px figures) has one section per item. On a phone the sidebar is a `details` menu.

**Signature element.** The sidebar. To read the site is to walk through the app in its own order.

**Screenshots.** One per section at the top, unframed, at half of the pixel size so that the interface text is
close to its real size. A `picture` element can swap in dark screenshots later.

**Home outline.** (1) Dashboard: h1, lead, Download, the dashboard screenshot. (2) to (10) One section per
sidebar item. (11) Agents. (12) Install. (13) Questions.

**Sample copy.**

- H1: "Gantry"; line: "The Mac app for Apple container and Docker."
- Subhead: "Free and open source. Requires macOS 26 or later."
- Headings: "Containers" · "Machines" · "Clusters"
- Feature paragraph: "Machines. Create, start and stop `container machine` Linux environments. Set the CPUs
  and the memory, open a shell, or open the machine in VS Code over Remote-SSH."

**Risks.** It is the least memorable: it reads as a documentation site or as an imitation of apple.com. The
signature disappears on a phone. Fleet, SSH, Compose and MCP are the selling points and have no sidebar item.
The site order breaks when the app sidebar changes.

---

## 3. Recommendation

**Build Concept A, "Command and Control".**

1. It is the only concept whose idea is a true statement about the product: Gantry is a GUI for a CLI. The
   signature (the command rail) is evidence, not ornament, so it also satisfies Principle II.
2. It matches the voice that the owner already writes in. The 0.27 to 0.29 strings stay; only the old hype
   strings change.
3. It has the lowest translation cost. The rail is untranslated commands. The command table reuses
   `guide.table`, which already exists in 27 languages. The feature items reuse the existing `h3` and `p` strings.
4. It works without JavaScript by construction: tables, lists, `details`. Light and dark are a token swap.
5. It is the furthest from the AI-landing genre. That genre has no tables, no numbers and no margins.
6. The home page falls from about 17,900 px to an estimated 8,000 to 9,000 px at 1440 px, with no content
   lost (FR of spec 002: "no content is lost").

**Steal from B (Yard):**

- One signal colour taken from the icon (crane orange), used rarely and flat.
- The beam: a thick ink bar under the nav and one vertical hairline. A crane without a drawing of a crane.
- The capability matrix idea, as a plain table in section `01` (apple/container, Docker, Docker over SSH).
- The marking plate, once: the title block of facts in the hero.

**Steal from C (Same Window):**

- Unframed screenshots near real size; no CSS window chrome anywhere.
- The order of the feature areas follows the app sidebar.
- `ui-monospace` and `system-ui` as the fallback stack, so text is correct before the fonts load.

**Do not take:** the uppercase condensed display type (B), the bay metaphors in the copy (B), the two-pane
sidebar layout (C).

---

## 4. Implementation plan for Concept A

**Spec-kit.** Create `specs/003-site-identity/` (`spec.md`, `plan.md`, `tasks.md`) and point
`.specify/feature.json` at it. Spec 002 is complete work for a release; do not reopen it. The constitution
needs no amendment: the rebrand makes the site meet Principle V (light mode), which it does not meet today.

**Base.** PR #5 (`feat/landing-0-29`) merges first, or the stack starts on top of it. Each PR below regenerates
216 pages or more; put the generated output in its own commit (`build: regenerate the pages`) so that a
reviewer reads only the source commits.

### PR 1: `feat(style): add the token system, the fonts and light mode`

No i18n change. No change to the home page structure. All inner pages (compare, guides, Kubernetes, docs) get
the new look through CSS only.

- `specs/003-site-identity/*`, `.specify/feature.json`.
- `assets/fonts/`: IBM Plex Sans 400 and 600, JetBrains Mono 400, WOFF2, four subsets each, with `OFL.txt`.
- `styles.css`: replace `:root` (`:5-45`) with the Concept A tokens and a `prefers-color-scheme: dark` block;
  add `color-scheme: light dark`; add `@font-face`. Delete `.bg-field`, `.bg-grid`, `.bg-grain` (`:62-94`).
  Rewrite Nav (`:100-173`, no blur, the 6 px beam), Languages (`:660-738`), Footer (`:614-622`), the code and
  copy styles. Replace every hardcoded `rgba(255,255,255,…)`, `#cfe0ef`, `#eaf2fa` with tokens. Add a
  temporary block that renders the old home sections flat (cards without radius, glow or hover).
- `build_docs.py`: `DOCS_CSS` (`:541` onward) to tokens; remove the three backdrop `div`s (`:484-486`).
- `templates/home.html:51-53`, `templates/page.html:38-40`: remove the backdrop `div`s. Both templates: two
  `theme-color` metas with `media`. Fix `og:image` size to 3104 x 1986 (`home.html:32-33`, `page.html:20-21`).
- New `scripts/check_fonts.py`: fail when a character of any `i18n/*.json` is missing from the fonts.

### PR 2: `refactor(home): remove the decoration and the mock interface`

No new strings. Removed keys are deleted from all 27 files by a script, which is a mechanical diff.

- `templates/home.html`: remove the crane stage (`:111-152`), the trust strip icons (`:156-168`), all `reveal`
  and `d1` to `d3` classes, all `.ico` tiles, the mini mock UIs (`:297-300`, `:310-313`, `:323-338`,
  `:348-359`, `:369-375`), the CSS window chrome (`:134-143`, `:534-555`), the kickers, the star pill
  (`:74-77`), the inline `style` attributes. Bento cells become `dl` entries; screenshots become plain `figure`s.
- `app.js`: delete all but the copy handler (about 12 lines), or inline it as in `page.html:81-90` and delete
  the file. `templates/home.html:4`: remove the `js` class script.
- `styles.css`: delete Hero stage (`:239-369`), Bento and mini UI (`:394-480`), the glow panels, Reveal
  (`:624-638`), `.window` and `.dot`. Expected size: about 740 lines down to about 350.
- `build_pages.py`: drop `hostlist_attrs` (`:458-461`).
- `i18n/*.json`, about 30 keys removed: the 8 `kicker`s, `home.hero.eyebrow`, `window_title`, `replay`,
  `replay_label`, `home.features.fleet.lbl`, `pill`, `running`, `unhealthy`, `home.features.logs.lbl`, `pill`,
  `home.features.notify.n1_*` and `n2_*`, `home.features.stats.mem`, `home.shots.*_title`, `chrome.star`.
- The h1 string keeps its `<span class="grad">` and `<br>` until PR 3; CSS neutralises both.

### PR 3: `feat(home): add the command rail, the areas and the new copy`

The only PR with translation work. Commits: template and generator; English; 26 languages; generated output.

- `templates/home.html`: the Concept A outline (title block, `01` to `15`, colophon).
- `build_pages.py`: `HOME_COMMANDS` (indexes into `guide.table`, so the rows are reused, not copied);
  `HOME_AREAS` (area to feature keys and rail commands); `HOME_RELEASES` (version to feature keys); the title
  block context from `APP_VERSION` and `UPDATED`; figure numbers in `shot()` (`:312-322`). Keep `home_ld()`
  (`:389-442`) unchanged, and check that `home.ld.features` still matches the page.
- `styles.css`: rail grid, title block, definition lists, tables, figures.
- English strings, estimate:
  - **New, about 55:** h1, lead, 6 title block labels, 15 section headings, about 12 one-line section intros,
    7 area names (take them from the app glossaries), 9 cells of the `01` table, 3 table headers, "Fig.",
    2 colophon lines.
  - **Changed, about 22:** `home.hero.tagline`, `note`; `home.features.h2`, `p`, `logs.h3`, `notify.h3`,
    `compose.h3`, `tunnel.p`; `home.agents.h2`, `p`; `home.shots.h2`, `p`; `home.built.h2`, `p`, `swiftui_p`,
    `swift6_p`, `updates_p`; `home.install.h2`, `sub`; `home.trust.title`; `home.title` and `home.desc` only
    if the owner wants (see question 2).
  - **Translation load:** about 77 strings x 26 languages, about 2,000 strings. Serbian Latin is generated.
    Use `scripts/i18n_delta.py` for the delta and the app glossaries for the terms (Principle III).
- `llms.txt`, `llms-full.txt`: regenerate; check that the feature list did not change in meaning.

### PR 4: `perf(assets): add sized images and finish the inner pages`

- New `scripts/make_images.py`: write 1600 px and 800 px WebP files next to each PNG. `shot()` emits
  `picture` with `srcset`, and keeps `width`, `height` and `alt`.
- `templates/page.html`, guide and docs styles: figure numbers, the rail for the "In short" block, table style
  equal to the home tables. New `og:image` at 1200 x 630 made from Fig. 1.
- Remove the temporary CSS block of PR 1. Delete unused assets after a `grep`.

### PR 5 (optional): `docs(i18n): rewrite the older feature text in the same voice`

About 20 changed strings (`home.features.*.p`, the remaining em-dashes), x 26 languages, about 520 strings.
No layout change. It can wait for the next release update.

### Checks for every PR

- `python3 build_pages.py --check`, then `python3 build_pages.py && python3 build_docs.py`, then
  `git status --porcelain` must be empty after a second build.
- `python3 scripts/check_links.py` (links, anchors, hreflang, sitemap, unique titles, JSON-LD).
- `python3 scripts/check_fonts.py` (from PR 1).
- Playwright with Chrome: `/`, `/compare/`, one guide, `/docs/index.html` at 1440 px and 390 px, light and
  dark, in `en`, `de`, `ru`, `el`, `fi`. At 390 px: `scrollWidth <= 390`. One run with JavaScript off.
- Text contrast 4.5:1 or more for `--ink`, `--ink-2`, `--signal` on `--paper` and `--panel`, both schemes.
- Fig. 1 visible without scrolling at 1440 x 900.
- Every `img` has `alt`, `width`, `height`. FAQ, SoftwareApplication and HowTo JSON-LD still validate.
- No IndexNow ping until the stack is on `main`.

---

## 5. Open questions for the owner

1. **Is the idea right: "every command has a control"?** It makes the site look like a manual, not like a
   product launch. Default: yes, Concept A.
2. **May the h1 and the `<title>` change?** The current h1 holds the search phrase "native macOS GUI for Apple
   container and Docker". Default: h1 becomes "The Mac app for Apple container and Docker"; `home.title`,
   `home.desc` and `home.keywords` stay unchanged, so search snippets do not move.
3. **Self-hosted fonts or system fonts only?** IBM Plex Sans and JetBrains Mono add about 60 to 100 kB for a
   visitor and give the site its own face. System fonts add nothing and look like the current site. Default:
   self-hosted, with the system stack as the fallback.
4. **A manual light/dark switch, and dark screenshots?** A switch needs JavaScript and storage. Dark
   screenshots double the capture work. Default: no switch (follow the system), light screenshots in both
   schemes; add dark screenshots with the next release update.

Also needs an answer, outside the four: does the app install a `gantry` command? If not, the mock terminal
line (`templates/home.html:371`) is untrue today and must go at once, not in PR 2.
