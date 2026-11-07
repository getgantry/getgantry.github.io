<!-- STE deviation: product names, file names, paths, PR numbers and quoted UI labels stay verbatim. -->
# Research: Landing Update for Gantry 0.27.0

This file holds the results of T001 (how the site is built), T002 and T010 (the claims list with sources) and T003
(facts about other products).

## T001: How the generators build the site

- `build_pages.py` reads `i18n/languages.json` and `i18n/<lang>.json`. `sr-Latn` is transliterated from `sr` in
  `load_strings()`. `check()` compares each language with `en.json`: keys, list lengths, HTML tags, `<code>`
  contents, placeholders, and the fixed values (`id`, `code`, `table`, `shot`, `when`, `unless`).
- `resolve()` selects the text for `FLAGS`. A key `x_native` (flag `k8s_native`) or `x_shipped` (flag
  `external_storage`) replaces `x` when its flag is on. List items with `when` or `unless` are left out when their
  flag says so.
- `PAGES` (home, `apple-container`, `apple-container-kubernetes`, `compare`) render with `templates/<slug>.html`
  inside `templates/page.html`. `GUIDES` render from structured strings with `guide_body()` and `sections_html()`.
  The terminal walk-through of the Kubernetes page (`k8s.terminal`) uses the same renderer.
- hreflang: `chrome()` writes one `<link rel="alternate">` for each language and `x-default`.
- Open Graph and Twitter tags are in `templates/page.html` and `templates/home.html`.
- JSON-LD:
  - The home page has Organization, WebSite, WebPage, SoftwareApplication, HowTo and FAQPage.
  - The other pages have TechArticle, BreadcrumbList and FAQPage.
  - The guides and the Kubernetes walk-through also have HowTo (`howto_ld()`).
- `sitemap()` writes one `<url>` for each page and language, with all alternates.
- `llms_txt()` replaces the languages section of the hand-written `llms.txt`. `llms_full()` writes `llms-full.txt`
  from the English strings: the command table, cluster options, the comparison, every guide with its commands, all
  FAQs and the page list.
- `shot()` writes a `TODO-SCREENSHOT` comment until `assets/shots/0.27.0/<file>` exists. When the file exists, it
  writes a figure with the size of the PNG.
- `build_docs.py` writes the English docs in `docs/`.

## T002 and T010: Claims and their sources

The app repository is `getgantry/gantry` (local clone `~/PycharmProjects/docker-watch`). The reports are in
`/Volumes/SanDisk2Tb/builds/gantry-027/*/REPORT.md`.

| Claim on the site | Source | State |
|---|---|---|
| Supports `container` CLI 1.0 to 1.7.1, 1.7.1 recommended | PR #50; `ac17/REPORT.md` (`recommendedVersion = 1.7.1`) | merged |
| Worker CPUs and memory, shared image store ("Use local images"), cluster list for 1.7, Kubernetes version and image store in the overview | PR #50; `ac17/REPORT.md` | merged |
| Cluster nodes are locked against start, stop, remove and rename; Start All and Stop All skip nodes | PR #50; `ac17/REPORT.md` | merged |
| "Load into Cluster" only on CLI 1.5 and 1.6 | PR #50; `ac17/REPORT.md` | merged |
| Clusters made with 1.6 or earlier do not show in the 1.7 list | `ac17/REPORT.md`, known gaps; apple/container `docs/cluster.md` | merged |
| Hint when the cluster services do not answer: Homebrew build gets "Download Installer…", others get "Restart Services…" | `feat/apple-container-1-7-1`; `ac171/REPORT.md` item 1 | listed branch |
| `[container.dns]` list editor on CLI 1.7 | `feat/apple-container-1-7-1`; `ac171/REPORT.md` item 2 | listed branch |
| Outdated builder image card with "Recreate Builder…" | `feat/apple-container-1-7-1`; `ac171/REPORT.md` item 5 | listed branch |
| Kubernetes browser: kinds, logs, shell, port forward, scale, rollout restart, delete, Apply YAML, masked secrets; runs `kubectl`, Homebrew install | PR #54; `k8s/REPORT.md` | merged |
| Browse Resources on a cluster; the toolbar has Browse Resources and a More menu | PR #54; `hig/REPORT.md` (Clusters detail) | merged / listed branch |
| Kubernetes browser with no `kubectl` | `feat/kubernetes-native` has no commits and no report | **not claimed** (flag `k8s_native` off) |
| Explain Failure: logs and details with environment values and secret-like text removed; on-device model; Private Cloud Compute for long logs (macOS 27); shows what was sent; prompt for another assistant | PR #48 | merged |
| Notification actions, Spotlight, App Intents and Siri, fleet widget, two Control Center controls | PR #49 | merged |
| `gantry://` links | PR #55 | merged |
| Command palette (⌘K) and its search scope | PR #51; `palette/REPORT.md` | merged |
| Bulk actions with progress and a report for each item | PR #52; `bulk/REPORT.md` | merged |
| Paste Command, the flags it reads, warnings for each host type, Copy as Command, recipes in `recipes.json` | PR #53; `recipe/REPORT.md` | merged |
| New design: live charts, icon toolbars, Liquid Glass only on floating controls | `feat/hig-design-pass`; `hig/REPORT.md` | listed branch |
| External drives in Gantry: move the data root, volumes on a disk, warning when the disk is not connected | `feat/external-storage` has no commits and no report | **not claimed** (flag `external_storage` off) |
| 28 UI languages | PR #42 (0.26.0); PRs #48 and #49 ("translated into all 28 languages") | merged |
| Gantry starts the services without `--app-root` | `AppleContainerControl.swift` and `AppleContainerTransport.swift` on `main`: `system start --disable-kernel-install` | merged |
| `--app-root` does not persist; volumes are sparse ext4 images; `--opt` only takes `size` and `journal` | apple/container 1.7.1 source: `SystemStart.swift`, `ApplicationRoot.swift`, `VolumesService.swift`, `docs/volumes.md` | upstream |
| `cp -Rp` keeps sparse volume images sparse, `ditto` does not | Test on this Mac, 2026-11-07, macOS 27, APFS to APFS over USB | tested |
| `cluster create` flags, the shared image store and its security note, default node image `kindest/node:v1.35.5` | apple/container 1.7.1 `docs/cluster.md` and `container cluster create --help` | upstream |

## T003: Other products (checked 2026-11-07)

The comparison page cites each fact. The sources are in `i18n/en.json` under `compare.body.sources.items`.

- **Docker Desktop:** free for personal use, education, non-commercial open source, and organizations with fewer
  than 250 employees and less than $10M revenue. Pro costs $11, Team $16 and Business $24 per user per month. It is
  closed source and Electron. Its Kubernetes is kubeadm (single node) or kind (multi-node). It has a disk image
  location setting, the MCP Toolkit and Gordon. Version 4.98.0 (2026-11-03). It does not manage apple/container.
- **OrbStack:** free for personal, non-commercial use; Pro costs $8 per user per month. It is closed source with some
  open components, and a native Swift app for macOS 14+. Its Kubernetes has a single node. It has Linux machines and,
  since 0.13.0, a data location. Version 2.2.5 (2026-10-23). The maintainer has no plans for apple/container
  (issue 2451).
- **Podman Desktop:** Apache 2.0, Electron. Kubernetes through the Kind and Minikube extensions. Remote Podman over
  SSH. The AI Lab extension has MCP. Version 1.30.5 (2026-10-13). **It manages apple/container through the official
  Apple container extension (Socktainer).** For this reason, the site does not say "the only GUI".
- **apple/container:** 1.7.1 (2026-11-06). There is no `compose`. `cluster` runs kubeadm on `kindest/node` and
  supports several nodes.
- About 10 other open-source GUIs for apple/container exist, for example Orchard and AppleContainerGUI.

## Decisions

- **T005:** the maintainer decided on 2026-11-07 (spec, Assumptions) that the comparison and Kubernetes guides
  update the existing pages. `/compare/` is the comparison guide. The walk-through "Run Kubernetes on a Mac with
  Apple container" is the section `#terminal` of `/apple-container-kubernetes/`. The separate page
  `/kubernetes-on-mac/` was removed before it went live.
- **Constitution II:** in the default build (both flags off), the site does not mention unreleased features, not
  even as "in development". The text for each flag is ready in all languages.
