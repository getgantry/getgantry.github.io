<!-- STE deviation: product names, UI names, paths and code references stay verbatim. -->
# Research: Landing Update for Gantry 0.29.0

## Sources

- App source at `origin/main`, which is `v0.29.0` (commit 93efa79). The export is in `/Volumes/SanDisk2Tb/builds/gantry/landing-029/src`.
- Specs 006 to 013 and their task lists. All tasks are ticked, except T028 of spec 013.
- Pull requests #66 to #73 and #80 in `getgantry/gantry`.
- `gh release view v0.29.0 -R getgantry/gantry` shows the release. It was published at 2026-11-15T13:49:39Z. Thus the version change to 0.29.0 can go in now.

## Claims list

| Feature | Claim on the site | Source |
|---|---|---|
| Resource Usage (006, 0.28.0) | One table of the running containers of all hosts. Columns: host, name, image, CPU, memory, network I/O, disk I/O, uptime. Sort by each column. Filter by name, image or host. Uses the 5-second samples. Double-click opens the container. MCP tool `fleet_activity`. | `App/Views/Usage/FleetActivityView.swift:97-130`, `GantryTools+Activity.swift:14-28` |
| Log export (007, 0.29.0) | Export Logs… (⇧⌘E) saves the visible lines as a .log or .txt file. Copy Visible Lines copies them. Timestamps and a time range work on Docker hosts only. | `LogExportControls.swift:117-158`, `LogExport.swift:48-51` |
| Export as Compose (008, 0.28.0) | In the context menu, the More menu and the menu for many containers. One service for each container. Secret-like values become `${NAME}`. A file with a secret value gets mode 0600. Apple hosts show warnings for flags such as `--kernel`. | `ComposeExportSheet.swift`, PR #68 |
| Explain images (009, 0.28.0) | Up to 3 images, 20 MB each, reduced to 1024 px. Needs macOS 27 and the on-device model. Images go only to the on-device model. | PR #67, `ExplainPanel.swift` |
| Build history (010, 0.29.0) | A Builds section on each host. Gantry keeps 100 builds for each host and the names of build arguments. Docker hosts also show `docker buildx history` (buildx 0.23.0 or later). `apple/container` hosts show the Gantry builds only. | `BuildxHistory.swift:67`, `ContentView.swift:62-70` |
| Image scan (011, 0.29.0) | Scan for Vulnerabilities… runs Trivy 0.50.0 or later, or Grype 0.74.0 or later. The user installs the scanner. Export SBOM writes CycloneDX, or SPDX with Trivy. Works on Apple, local Docker and SSH hosts. | `ImageScanner.swift:33-34,107-130`, `ImageScanPlan.swift` |
| Keychain secrets (012, 0.28.0) | Settings → Secrets. A key menu on each environment row. The row shows `keychain:NAME`. Gantry reads the value when it creates the container. Copy as Command, recipes and Compose export write the name. | `KeychainSecretStore.swift:9`, `EnvSecretField.swift:18,78-100` |
| Menu bar progress (013, 0.29.0) | An Activity section with title, host, progress bar, layers or services, bytes, time and Cancel. The icon shows the count. Compose projects get Pull Images and Compose Down. | `OperationProgress.swift:32-34`, PR #70 |

These items are not on the site:

- Kubernetes pods in Resource Usage, and a sort order that stays.
- Export of pod logs.
- The Apple Intelligence comment in a Compose export.
- Secrets in the MCP tool `create_container`.
- Values that `docker inspect` shows outside Gantry. The site tells the reader that the engine keeps the value.
- Live Activities, and the Stop or Keep Running question of task T028 in spec 013.

## Screenshots

- The 0.27.0 set comes from `screencapture -l<CGWindowID>` of the real window. It has light mode only.
- In this session, `screencapture` stops with the error "could not create image from window". The Orca shell has no Screen Recording permission.
- Orca Computer Use also has no Accessibility access. Thus clicks in the app are blocked.
- On 2026-11-15 the maintainer chose "routes only". We captured the screens that a `gantry://` route opens, with `gantry-ctl snapshot`.
- That snapshot draws the sidebar empty. Thus we cut each image to the content area.
- Made: `assets/shots/0.29.0/fleet-activity.png`, `assets/shots/0.29.0/menu-bar-progress.png` and `assets/fleet.png`.
- Open: `paste-command.png` and the sheets of image scan, Compose export, Explain Failure and Keychain secrets. Each sheet needs a click.
- We did not use the Builds list. The buildx records of the demo daemon show as `default/default/<id>`. Also, a route cannot select a record.

Demo data:

- On this Mac: `apple/container` containers web, api, postgres, redis and worker.
- On a remote Docker test host: a Docker-in-Docker daemon `landing-dind` with the Compose project `shop`.
- Gantry reached that daemon through a socket that SSH forwards. The host name in Gantry is "Build Server".
- The images show no real host name, network address, user path or secret.
- We removed all demo containers, the socket forward and `/tmp/landing-*` on a remote Docker test host.

## Translations

UI names come from the two app catalogs, `App/Localizable.xcstrings` and `Packages/AppCore/Sources/AppCore/Resources/Localizable.xcstrings`. We extracted them to `build/i18n/<lang>.ui.json`. Other terms come from the glossaries in `/Volumes/SanDisk2Tb/builds/l10n/reviewed/`.
