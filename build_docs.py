#!/usr/bin/env python3
"""Generate the Gantry docs section (static HTML) with shared chrome.

Run from the repo root: `python3 build_docs.py`. Emits docs/*.html and
docs/docs.css. The output is plain static HTML — no build step at serve time.
"""
import os
import html

OUT = os.path.join(os.path.dirname(__file__), "docs")

# (group title, [(page title, slug)])
SIDEBAR = [
    ("Getting started", [
        ("Introduction", "index"),
        ("Install", "install"),
        ("The menu bar", "menu-bar"),
    ]),
    ("Hosts & engines", [
        ("Hosts", "hosts"),
        ("apple/container", "apple-container"),
    ]),
    ("Working with containers", [
        ("Containers", "containers"),
        ("Ports & browser access", "ports"),
        ("Local DNS names", "dns"),
        ("Images & Compose", "images-compose"),
        ("Networks, volumes & machines", "resources"),
    ]),
    ("Automation", [
        ("AI agents & MCP", "mcp"),
    ]),
    ("Help", [
        ("Troubleshooting", "troubleshooting"),
    ]),
]

GITHUB = "https://github.com/getgantry/gantry"


def code(lang, body, copy=None):
    copy = copy if copy is not None else body
    return f'''<div class="code-block">
  <div class="code-head"><span>{html.escape(lang)}</span><button class="copy" data-copy="{html.escape(copy, quote=True)}">Copy</button></div>
  <pre><code>{html.escape(body)}</code></pre>
</div>'''


def callout(kind, body):
    label = {"tip": "Tip", "note": "Note", "warn": "Heads up"}[kind]
    return f'<div class="callout callout-{kind}"><span class="callout-tag">{label}</span><div>{body}</div></div>'


# ---------------------------------------------------------------- page bodies

PAGES = {}

PAGES["index"] = ("Introduction",
  "Gantry is a free, open-source native macOS app for managing Docker — locally and over SSH — and Apple's container runtime.",
  f"""
<h1>Gantry documentation</h1>
<p class="page-lead">Gantry is a native macOS app for managing and monitoring containers across every engine you use — local Docker, Docker over SSH, and Apple's <code>container</code> runtime — from one clean, fast interface. It is free, open source, and has no limits.</p>

{callout("tip", 'New here? Install Gantry, then jump to <a href="containers.html">Containers</a> or set up <a href="dns.html">local DNS names</a> so every container is reachable by name.')}

<h2>What you can do</h2>
<ul>
  <li><strong>See everything at a glance</strong> — a fleet dashboard with live CPU/memory sparklines and health issues that jump straight to the culprit, plus a <a href="menu-bar.html">menu-bar panel</a> of running containers.</li>
  <li><strong>Manage every resource</strong> — containers, images, volumes, networks, and (on apple/container) machines, with live logs, stats, an interactive terminal, file browsing and process lists.</li>
  <li><strong>Reach services instantly</strong> — open a container in your browser or copy its <code>ip:port</code> in one click, and give containers real <a href="dns.html">DNS names</a> on apple/container.</li>
  <li><strong>Work across hosts</strong> — add remote Docker daemons over SSH with first-class key handling, an SFTP file browser and a host terminal.</li>
  <li><strong>Drive it from agents</strong> — a built-in <a href="mcp.html">MCP server</a> and macOS App Intents make Gantry scriptable and AI-ready.</li>
</ul>

<h2>Requirements</h2>
<ul>
  <li>macOS 26 or later, Apple Silicon or Intel.</li>
  <li>For local Docker: Docker Desktop, Colima, OrbStack, or any daemon exposing the Docker socket.</li>
  <li>For Apple's runtime: the <a href="https://github.com/apple/container">apple/container</a> CLI 1.0+ (Gantry can guide you through installing it).</li>
</ul>

<h2>Open source</h2>
<p>Gantry is MIT-licensed and built with SwiftUI. The source, issues and releases live on <a href="{GITHUB}">GitHub</a>.</p>
""")

PAGES["install"] = ("Install",
  "Install Gantry with Homebrew or download the latest release. No App Store, no account.",
  f"""
<h1>Install</h1>
<p class="page-lead">No App Store and no account — download and drag, or use Homebrew.</p>

<h2>Homebrew</h2>
{code("Homebrew", "brew install --cask getgantry/tap/gantry\nxattr -dr com.apple.quarantine /Applications/Gantry.app")}

<h2>Manual download</h2>
<ol>
  <li>Grab the latest <code>.zip</code> from <a href="{GITHUB}/releases/latest">Releases</a> and unzip it.</li>
  <li>Move <code>Gantry.app</code> into <code>/Applications</code>.</li>
  <li>Gantry isn't notarized yet, so right-click the app and choose <em>Open</em> the first time, or clear the quarantine flag:</li>
</ol>
{code("Clear the quarantine flag", "xattr -dr com.apple.quarantine /Applications/Gantry.app")}

<h2>Updates</h2>
<p>Gantry checks for updates automatically (via Sparkle) and can install them in place. You can also re-run the Homebrew command above.</p>

{callout("note", 'Gantry runs as both a normal window app and a menu-bar item. You can hide the Dock icon and keep just the menu bar from <strong>Settings → General</strong>.')}
""")

PAGES["menu-bar"] = ("The menu bar",
  "The Gantry menu-bar panel lists running containers and lets you open them in a browser or copy their address.",
  f"""
<h1>The menu bar</h1>
<p class="page-lead">Click the Gantry icon in the menu bar for a compact panel of every connected host and its running containers — without opening the main window.</p>

<h2>What's in the panel</h2>
<ul>
  <li><strong>Per-host sections</strong> with a live status dot and a running/total count.</li>
  <li><strong>Each running container</strong> shows a state dot, its name, and its reachable port.</li>
  <li><strong>Open in browser</strong> — the Safari button opens the container's service directly.</li>
  <li><strong>Copy address</strong> — tap the <code>:port</code> chip to copy the container's <code>ip:port</code> (or <code>dns:port</code>).</li>
  <li><strong>Quick actions</strong> — stop and restart inline; right-click for Kill, Copy DNS Name, Copy ID, and <a href="mcp.html">Copy as Prompt</a>.</li>
  <li><strong>Recently exited</strong> containers with a one-tap start.</li>
</ul>

<p>Clicking a container name opens the main window focused on that container's detail view. On apple/container hosts, the panel also has a strip to start or stop the background services.</p>

{callout("tip", 'For SSH hosts, the menu opens the container through a local port forward; for local Docker and apple/container it opens the published port or routable IP directly.')}
""")

PAGES["hosts"] = ("Hosts",
  "Add and manage Docker hosts — local, over SSH, and Apple's container runtime.",
  f"""
<h1>Hosts</h1>
<p class="page-lead">A host is one container engine Gantry talks to. Add as many as you like; they all share one sidebar and dashboard.</p>

<h2>Host types</h2>
<ul>
  <li><strong>Local Docker</strong> — the daemon on your Mac (Docker Desktop, Colima, OrbStack, …). Gantry auto-adds a Local host on first launch; override the socket path in <strong>Settings → General</strong> if needed.</li>
  <li><strong>Docker over SSH</strong> — a remote daemon reached through SSH. Gantry tunnels the Docker socket; nothing needs to be exposed publicly.</li>
  <li><strong>apple/container</strong> — Apple's native runtime. See <a href="apple-container.html">apple/container</a>.</li>
</ul>

<h2>Adding an SSH host</h2>
<p>Click <strong>Add Host…</strong> at the bottom of the sidebar and choose <em>SSH Docker Host</em>. You can import an entry straight from your <code>~/.ssh/config</code>, or fill in host, port and user manually. Authentication can be:</p>
<ul>
  <li><strong>Automatic</strong> — your SSH agent and default keys.</li>
  <li><strong>Key file</strong> — a specific private key (with an optional passphrase).</li>
  <li><strong>Password</strong> — stored in your login Keychain if you opt in.</li>
</ul>
<p>On first connection Gantry shows the server's host-key fingerprint for you to trust (trust-on-first-use), the same model as OpenSSH.</p>

<h2>Per-host tools</h2>
<ul>
  <li><strong>Overview</strong> — CPU/memory gauges, disk usage, and host facts (OS, architecture, Docker version).</li>
  <li><strong>Host terminal</strong> — an interactive SSH shell in its own window.</li>
  <li><strong>Host files</strong> — an SFTP browser to download files from the remote host (SSH only).</li>
  <li><strong>Reconnect, reorder, remove</strong> — from the host's hover menu in the sidebar.</li>
</ul>

{callout("note", 'Removing a host never deletes stored credentials from your Keychain — only the host entry in Gantry.')}
""")

PAGES["apple-container"] = ("apple/container",
  "Use Apple's native container runtime in Gantry: services, machines, and local DNS.",
  f"""
<h1>apple/container</h1>
<p class="page-lead">Gantry is a first-class UI for Apple's <a href="https://github.com/apple/container">container</a> runtime — manage its background services, machines, and local DNS without dropping to a terminal.</p>

<h2>Setup</h2>
<p>Install the <code>container</code> CLI 1.0+ from Apple's official signed installer. Gantry detects it automatically and, if it's missing or outdated, offers a guided setup. Then add an <em>Apple Container</em> host from <strong>Add Host…</strong>.</p>

{callout("warn", 'Use the official signed installer rather than the Homebrew bottle — the bottle omits the machine API server, so <code>container machine</code> cannot run.')}

<h2>Background services</h2>
<p>apple/container relies on background services that must be running for any container to work. Start or stop them from the menu-bar strip or <strong>Settings → Apple</strong>.</p>

<h2>What's different from Docker</h2>
<ul>
  <li>Every container gets its own <strong>routable IP</strong> on your Mac — no port publishing needed to reach it.</li>
  <li>Containers can resolve by name through <a href="dns.html">local DNS domains</a>.</li>
  <li><strong>Machines</strong> are long-lived Linux VMs (comparable to OrbStack machines) — see <a href="resources.html">Machines</a>.</li>
  <li><strong>Compose</strong> files can be brought up directly on an apple host.</li>
</ul>
""")

PAGES["containers"] = ("Containers",
  "Create, run, inspect and operate containers — logs, stats, terminal, files and more.",
  f"""
<h1>Containers</h1>
<p class="page-lead">The container list groups by Compose project, filters by state, and searches by name, image or ID. Everything you can do to a container is reachable here.</p>

<h2>Creating a container</h2>
<p>Two paths, both from the Containers toolbar:</p>
<ul>
  <li><strong>New Container</strong> — the full <code>docker run</code> surface: image, name, command, port mappings, environment, volume binds, restart policy, TTY and auto-remove. On apple hosts it also offers a <a href="dns.html">DNS domain</a>. If the image is missing locally it offers to pull and retry.</li>
  <li><strong>Quick Run</strong> — an OrbStack-style fast path: pick a local image, optionally share a Mac folder, map a port, choose a DNS domain, and open it in the browser when ready.</li>
</ul>

<h2>The detail view</h2>
<p>Select a container to open its detail tabs:</p>
<ul>
  <li><strong>Overview</strong> — state, address, ports, mounts, networks, config and environment.</li>
  <li><strong>Logs</strong> — live streaming with search, follow toggle and export.</li>
  <li><strong>Stats</strong> — live CPU, memory, network and I/O charts.</li>
  <li><strong>Terminal</strong> — an interactive shell into the running container.</li>
  <li><strong>Files</strong> — browse, download and upload files.</li>
  <li><strong>Processes</strong> — a live <code>top</code> table.</li>
  <li><strong>Inspect</strong> — the raw JSON.</li>
</ul>

<h2>Actions</h2>
<p>Start, stop, restart and kill from the toolbar; the overflow menu adds Rename, Commit to Image, Export Filesystem, Restart Policy, Copy ID and <a href="mcp.html">Copy as Prompt</a>. Most actions are also on the right-click menu in the list and the <a href="menu-bar.html">menu bar</a>.</p>
""")

PAGES["ports"] = ("Ports & browser access",
  "Open container services in your browser and copy their address, including SSH port forwarding.",
  f"""
<h1>Ports & browser access</h1>
<p class="page-lead">Gantry makes a container's service one click away, whichever engine it runs on.</p>

<h2>Local Docker</h2>
<p>Published ports open directly on <code>localhost</code>. Use the open-in-browser button on a port in the container's <strong>Overview → Ports</strong> section, or the <a href="menu-bar.html">menu bar</a>.</p>

<h2>apple/container</h2>
<p>Each container has a routable IP, so its ports are reachable directly at <code>http://&lt;ip&gt;:&lt;port&gt;</code> — no publishing required. The <strong>Address</strong> section shows the IP (and DNS name, if any) with one-click open chips. Gantry uses the IP for the primary open action because it always resolves; see <a href="dns.html">Local DNS names</a> to also reach it by name.</p>

<h2>Docker over SSH</h2>
<p>Remote ports aren't reachable from your Mac directly, so Gantry creates a local <strong>SSH port forward</strong> on demand and opens <code>localhost:&lt;local-port&gt;</code>. Active forwards are listed in the Ports section, where you can change the local port, copy the URL, or tear the forward down.</p>

{callout("tip", 'The copy button puts a paste-ready <code>host:port</code> on your clipboard — handy for database clients and tools that are not browsers.')}
""")

DNS_CLI = '''# 1. create the domain (asks for admin)
sudo container system dns create test

# 2. make it the default domain
mkdir -p ~/.config/container
printf '[dns]\\ndomain = "test"\\n' > ~/.config/container/config.toml

# 3. restart services, then run a container
container system stop && container system start
container run -d --name web docker.io/library/nginx:alpine

# 4. resolve it
dscacheutil -flushcache
curl http://web.test/'''

PAGES["dns"] = ("Local DNS names",
  "Give apple/container containers real DNS names like web.test that resolve across your Mac.",
  f"""
<h1>Local DNS names</h1>
<p class="page-lead">On apple/container, Gantry can make every container reachable by name — <code>name.domain</code> — across your whole Mac, OrbStack-style. This page explains how it works and how to set it up.</p>

<h2>How it works</h2>
<p>apple/container ships a local DNS server (on <code>127.0.0.1:2053</code>). When you create a <em>local domain</em>, macOS is told to route that domain's lookups to it (via a file in <code>/etc/resolver</code>). A container started under that domain then resolves as <code>&lt;name&gt;.&lt;domain&gt;</code> to its routable IP.</p>
<p>Two things are required for names to resolve from the host:</p>
<ol>
  <li>The domain must exist (<code>container system dns create &lt;domain&gt;</code>).</li>
  <li>It must be the <strong>default DNS domain</strong>, set in <code>~/.config/container/config.toml</code>, and the services restarted.</li>
</ol>
<p>Gantry does both for you.</p>

<h2>Set it up in Gantry</h2>
<ol>
  <li>Open <strong>Settings → Apple</strong>.</li>
  <li>Under <strong>Local DNS Domains</strong>, add a domain (for example <code>test</code>). Creating a domain needs administrator approval — macOS will prompt once. The first domain you add becomes the default automatically.</li>
  <li>Click the <strong>star</strong> to mark a domain as the default. Gantry writes it into apple/container's config and shows a <strong>Restart Services</strong> button — click it.</li>
</ol>
<p>From now on, containers you create in Gantry are assigned the default domain automatically, with a unique name derived from the image (e.g. <code>nginx</code>, then <code>nginx-2</code>). They resolve immediately — Gantry flushes the DNS cache for you.</p>

{callout("tip", 'You can also set the domain per container in <strong>New Container</strong> and <strong>Quick Run</strong>, under Networking.')}

<h2>Naming an existing container</h2>
<p>A container's DNS domain is fixed when it's created, so apple/container can't change it on a running container. In the container's <strong>Overview → Address</strong> section, use <strong>Assign / Change DNS Name…</strong> — Gantry recreates the container with the new domain, preserving its image, command, environment, published ports, volume binds, restart policy and labels. Named volumes and bind mounts are kept; only the container's writable layer is reset (exactly like <code>docker rm</code> + <code>docker run</code>).</p>

<h2>Doing it by hand</h2>
<p>If you prefer the CLI:</p>
{code("Terminal", DNS_CLI)}

<h2>Caveats</h2>
<ul>
  <li>Only containers created <em>after</em> the default domain is set are registered — recreate older ones (Gantry's Assign DNS Name does this).</li>
  <li>macOS caches negative lookups: if you tried a name before it existed, flush with <code>dscacheutil -flushcache</code>. Gantry flushes automatically after a recreate or services restart.</li>
  <li>The container's IP always works even when a name doesn't — Gantry's open-in-browser uses the IP for reliability.</li>
</ul>
""")

PAGES["images-compose"] = ("Images & Compose",
  "Pull, build, tag and prune images, and bring up Compose files.",
  f"""
<h1>Images & Compose</h1>

<h2>Images</h2>
<ul>
  <li><strong>Pull</strong> with optional registry authentication and per-layer progress.</li>
  <li><strong>Build</strong> from a Dockerfile — pick the context, tag, target stage, build args and cache option, and watch the log stream live. You can also drag a Dockerfile onto the window, or use <strong>Open With → Gantry</strong>.</li>
  <li><strong>Tag</strong> and <strong>remove</strong> images; <strong>prune</strong> dangling or all unused.</li>
  <li>Inspect an image's layers/history and raw JSON, and see which containers use it.</li>
</ul>

<h2>Compose</h2>
<p>On apple/container hosts, open a <code>docker-compose.yml</code> from <strong>Docker → Open Compose File…</strong>, Finder's <em>Open With</em>, or by dropping it on the window. Choose the host, toggle recreate / no-cache, and bring the project up with a live, colorized log stream. When it's up, Gantry jumps to the host's Containers grouped by the Compose project.</p>
""")

PAGES["resources"] = ("Networks, volumes & machines",
  "Manage networks, volumes, and apple/container machines.",
  f"""
<h1>Networks, volumes & machines</h1>

<h2>Networks</h2>
<p>Create networks (bridge, overlay, macvlan) with labels, inspect their IPAM config and connected containers, attach a running container, and prune unused ones. Built-in networks (<code>bridge</code>, <code>host</code>, <code>none</code>) are protected from removal.</p>

<h2>Volumes</h2>
<p>Create and remove volumes, see their driver, labels and mount point, inspect the raw JSON, and prune unused volumes.</p>

<h2>Machines (apple/container)</h2>
<p>Machines are long-lived Linux VMs managed by <code>container machine</code>. From the <strong>Machines</strong> section you can create one (name + image), start and stop it, open a shell, set it as default, and delete it.</p>

{callout("note", '<code>container machine</code> requires the official signed apple/container installer — the Homebrew bottle omits the machine API server.')}
""")

PAGES["mcp"] = ("AI agents & MCP",
  "Drive Gantry from Claude and other agents with the built-in MCP server, App Intents and Copy as Prompt.",
  f"""
<h1>AI agents & MCP</h1>
<p class="page-lead">Gantry is built to be driven by agents — it ships a Model Context Protocol server and macOS App Intents.</p>

<h2>The MCP server</h2>
<p>Gantry bundles a <code>gantry-mcp</code> binary. Register it with Claude in one command:</p>
{code("Add the Gantry MCP server", "claude mcp add gantry -- /Applications/Gantry.app/Contents/Resources/gantry-mcp")}
<p>The agent can then list hosts and containers, read logs, run commands and operate the fleet through Gantry's tools.</p>

<h2>Copy as Prompt</h2>
<p>On any container, <strong>Copy as Prompt</strong> (⌥⌘P) puts a paste-ready prompt on your clipboard: the host and how to reach it, the MCP <code>host_id</code> and the tools to call, the container's current state, and a task matched to the symptom. An unhealthy container asks the agent to fix the failing health check; a crash-looping one, to find the crash. Paste it into Claude Code and let it dig in.</p>

<h2>Shortcuts & Spotlight</h2>
<p>Gantry exposes App Intents, so you can build Shortcuts and trigger common actions from Siri and Spotlight. See <strong>Settings → Agents</strong> for examples.</p>
""")

PAGES["troubleshooting"] = ("Troubleshooting",
  "Fixes for common issues: DNS names, the menu bar, SSH, and apple/container services.",
  f"""
<h1>Troubleshooting</h1>

<h2>A DNS name won't open (NXDOMAIN / "can't find server")</h2>
<ul>
  <li>Make sure a <strong>default DNS domain</strong> is set and starred in <strong>Settings → Apple</strong>, and that you clicked <strong>Restart Services</strong>.</li>
  <li>Only containers created <em>after</em> that resolve — recreate older ones with <strong>Assign / Change DNS Name…</strong> on the container.</li>
  <li>macOS may have cached the old negative result. Flush it:</li>
</ul>
{code("Terminal", "dscacheutil -flushcache")}
<p>The container's IP always works regardless — Gantry's open-in-browser uses it. See <a href="dns.html">Local DNS names</a>.</p>

<h2>apple/container containers don't appear</h2>
<p>The background services must be running. Start them from the menu-bar strip or <strong>Settings → Apple</strong>. If the CLI is missing or outdated, Gantry's setup prompt links to the official installer.</p>

<h2>The menu-bar panel is empty</h2>
<p>It only lists <em>connected</em> hosts. Check the host's status dot in the sidebar; if it failed, open the host and retry the connection.</p>

<h2>An SSH host won't connect</h2>
<ul>
  <li>Confirm you can <code>ssh</code> to it from Terminal with the same credentials.</li>
  <li>If the key has a passphrase, choose <em>Key file</em> auth and let Gantry store it in the Keychain.</li>
  <li>Use the host's <strong>Reconnect</strong> action after fixing credentials.</li>
</ul>

<h2>"Gantry is damaged" or won't open</h2>
<p>The build isn't notarized yet. Clear the quarantine flag:</p>
{code("Terminal", "xattr -dr com.apple.quarantine /Applications/Gantry.app")}

<p>Still stuck? Open an issue on <a href="{GITHUB}/issues">GitHub</a>.</p>
""")


# ---------------------------------------------------------------- templating

THEME_SVGS = '''<svg class="ico-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        <svg class="ico-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'''


def sidebar_html(active):
    out = ['<nav class="docs-nav" aria-label="Docs">']
    for group, items in SIDEBAR:
        out.append(f'<div class="docs-nav-group"><span class="docs-nav-title">{html.escape(group)}</span><ul>')
        for title, slug in items:
            cls = ' class="active"' if slug == active else ''
            out.append(f'<li><a href="{slug}.html"{cls}>{html.escape(title)}</a></li>')
        out.append('</ul></div>')
    out.append('</nav>')
    return "\n".join(out)


def page_html(slug, title, desc, body):
    full_title = "Gantry Docs — " + title if slug != "index" else "Gantry Documentation"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-3JR87M6TNM"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-3JR87M6TNM');</script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(full_title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta property="og:title" content="{html.escape(full_title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="https://getgantry.github.io/docs/{slug}.html">
  <meta property="og:image" content="https://getgantry.github.io/assets/dashboard.png">
  <meta name="theme-color" content="#0B2942">
  <link rel="icon" type="image/png" href="../assets/icon.png">
  <link rel="stylesheet" href="../style.css">
  <link rel="stylesheet" href="docs.css">
</head>
<body class="docs-body">
  <header class="nav">
    <div class="nav-inner">
      <a class="brand" href="../index.html"><img src="../assets/icon.png" alt="Gantry icon" width="28" height="28"><span>Gantry</span></a>
      <nav class="nav-links">
        <a href="../index.html#features">Features</a>
        <a href="index.html" class="active">Docs</a>
        <a href="../index.html#install">Install</a>
        <a href="{GITHUB}">GitHub</a>
      </nav>
      <button id="theme-toggle" class="theme-toggle" aria-label="Toggle color theme" title="Toggle theme">
        {THEME_SVGS}
      </button>
      <button id="docs-menu-btn" class="docs-menu-btn" aria-label="Toggle docs menu" title="Menu">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </header>

  <div class="docs-shell">
    <aside class="docs-sidebar" id="docs-sidebar">
      {sidebar_html(slug)}
    </aside>
    <main class="docs-content">
      <article class="docs-article">
        {body.strip()}
      </article>
      <footer class="docs-foot">
        <a href="{GITHUB}/blob/main/CHANGELOG.md">Changelog</a>
        <span>·</span>
        <a href="{GITHUB}/issues">Report an issue</a>
        <span>·</span>
        <a href="{GITHUB}">MIT licensed · GitHub</a>
      </footer>
    </main>
  </div>

  <script>
    (function () {{
      var root = document.documentElement;
      var saved = localStorage.getItem('gantry-theme');
      if (saved) root.setAttribute('data-theme', saved);
      var btn = document.getElementById('theme-toggle');
      btn.addEventListener('click', function () {{
        var current = root.getAttribute('data-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        var next = current === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        localStorage.setItem('gantry-theme', next);
      }});
      var mb = document.getElementById('docs-menu-btn');
      var sb = document.getElementById('docs-sidebar');
      mb.addEventListener('click', function () {{ sb.classList.toggle('open'); }});
      sb.addEventListener('click', function (e) {{ if (e.target.tagName === 'A') sb.classList.remove('open'); }});
    }})();
    document.querySelectorAll('.copy').forEach(function (b) {{
      b.addEventListener('click', function () {{
        navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function () {{
          var t = b.textContent; b.textContent = 'Copied';
          setTimeout(function () {{ b.textContent = t; }}, 1400);
        }});
      }});
    }});
  </script>
</body>
</html>
'''


DOCS_CSS = '''/* Docs layout — builds on style.css tokens. */
.docs-shell {
  max-width: 1180px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 256px minmax(0, 1fr);
  gap: 0;
  align-items: start;
}
.docs-sidebar {
  position: sticky;
  top: 61px;
  align-self: start;
  height: calc(100vh - 61px);
  overflow-y: auto;
  padding: 30px 18px 60px;
  border-right: 1px solid var(--border);
}
.docs-nav-group { margin-bottom: 22px; }
.docs-nav-title {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--text-dim);
  margin: 0 10px 8px;
}
.docs-nav ul { list-style: none; margin: 0; padding: 0; }
.docs-nav li a {
  display: block;
  padding: 6px 10px;
  border-radius: 8px;
  color: var(--text-dim);
  font-size: 0.92rem;
  font-weight: 500;
}
.docs-nav li a:hover { background: var(--bg-elev); color: var(--text); text-decoration: none; }
.docs-nav li a.active {
  background: linear-gradient(135deg, rgba(43,108,176,0.16), rgba(246,134,58,0.12));
  color: var(--text);
  font-weight: 600;
}

.docs-content { padding: 40px clamp(20px, 4vw, 56px) 90px; min-width: 0; }
.docs-article { max-width: 760px; }
.docs-article h1 { font-size: clamp(2rem, 4vw, 2.7rem); margin: 0 0 14px; }
.docs-article h2 {
  font-size: 1.4rem;
  margin: 40px 0 12px;
  padding-top: 14px;
  border-top: 1px solid var(--border);
}
.docs-article h3 { font-size: 1.1rem; margin: 26px 0 8px; }
.docs-article p, .docs-article li { color: var(--text); }
.docs-article .page-lead { font-size: 1.15rem; color: var(--text-dim); margin: 0 0 8px; }
.docs-article ul, .docs-article ol { padding-left: 22px; }
.docs-article li { margin: 6px 0; }
.docs-article a { font-weight: 500; }
.docs-article code {
  background: var(--border);
  padding: 1.5px 6px;
  border-radius: 5px;
  font-size: 0.86em;
}
.docs-article .code-block code { background: none; padding: 0; }
.docs-article .code-block { margin: 16px 0; }

/* Callouts */
.callout {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  margin: 18px 0;
  padding: 14px 16px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: var(--bg-elev);
  font-size: 0.95rem;
}
.callout div { min-width: 0; }
.callout-tag {
  flex: none;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 3px 9px;
  border-radius: 999px;
  color: #fff;
}
.callout-tip { border-color: rgba(40,170,90,0.35); }
.callout-tip .callout-tag { background: linear-gradient(135deg, #2b9d5a, #1f8f7a); }
.callout-note { border-color: rgba(43,108,176,0.35); }
.callout-note .callout-tag { background: linear-gradient(135deg, var(--steel), var(--navy)); }
.callout-warn { border-color: rgba(246,134,58,0.45); }
.callout-warn .callout-tag { background: linear-gradient(135deg, var(--crane), #d2641f); }

.docs-foot {
  max-width: 760px;
  margin-top: 56px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
  color: var(--text-dim);
  font-size: 0.9rem;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.docs-menu-btn {
  display: none;
  align-items: center;
  justify-content: center;
  width: 36px; height: 36px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--bg-elev);
  color: var(--text);
  cursor: pointer;
}

@media (max-width: 860px) {
  .docs-shell { grid-template-columns: 1fr; }
  .docs-sidebar {
    position: fixed;
    top: 61px; left: 0;
    width: 280px;
    max-width: 84vw;
    background: var(--bg-solid);
    transform: translateX(-105%);
    transition: transform 0.22s ease;
    z-index: 40;
    box-shadow: var(--shadow);
  }
  .docs-sidebar.open { transform: none; }
  .docs-menu-btn { display: inline-flex; }
  .nav-links { display: none; }
}
'''


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "docs.css"), "w") as f:
        f.write(DOCS_CSS)
    for slug, (title, desc, body) in PAGES.items():
        with open(os.path.join(OUT, f"{slug}.html"), "w") as f:
            f.write(page_html(slug, title, desc, body))
    print(f"Wrote {len(PAGES)} pages + docs.css to {OUT}")


if __name__ == "__main__":
    main()
