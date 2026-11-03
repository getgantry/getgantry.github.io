#!/usr/bin/env python3
"""Generate the standalone pages: the apple/container guide, Kubernetes and compare.

Run from the repo root after build_docs.py (it writes the shared docs.css).
"""
import html
import json
import os
import re

from build_docs import GITHUB, callout, code

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://getgantry.github.io"
UPDATED = "2026-11-03"


def plain(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


def faq_block(items):
    rows = "\n".join(
        f'<details class="faq-item"><summary>{html.escape(q)}</summary><p>{a}</p></details>'
        for q, a in items)
    return f'<div class="faq-list">\n{rows}\n</div>'


def faq_ld(url, items):
    return {
        "@type": "FAQPage",
        "@id": f"{url}#faq",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                       for q, a in items],
    }


def page_html(slug, title, desc, crumb, body, faq=None, about=None):
    url = f"{SITE}/{slug}/"
    graph = [
        {
            "@type": "TechArticle",
            "@id": f"{url}#article",
            "headline": title,
            "description": desc,
            "url": url,
            "inLanguage": "en",
            "dateModified": UPDATED,
            "image": f"{SITE}/assets/dashboard.png",
            "author": {"@type": "Organization", "name": "Gantry", "url": f"{SITE}/"},
            "publisher": {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Gantry",
                          "logo": f"{SITE}/assets/icon.png"},
            "about": about or [],
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumbs",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Gantry", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": crumb, "item": url},
            ],
        },
    ]
    if faq:
        graph.append(faq_ld(url, faq))
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    faq_html = ""
    if faq:
        faq_html = f'\n<h2 id="faq">Questions and answers</h2>\n{faq_block(faq)}\n'
    t = html.escape(title)
    d = html.escape(desc)

    def active(s):
        return ' class="active"' if slug == s else ''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-3JR87M6TNM"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-3JR87M6TNM');</script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{t}</title>
  <meta name="description" content="{d}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Gantry">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{t}">
  <meta property="og:description" content="{d}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/dashboard.png">
  <meta property="og:image:width" content="3364">
  <meta property="og:image:height" content="2116">
  <meta property="og:image:alt" content="Gantry fleet dashboard with Docker and apple/container hosts">
  <meta property="article:modified_time" content="{UPDATED}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t}">
  <meta name="twitter:description" content="{d}">
  <meta name="twitter:image" content="{SITE}/assets/dashboard.png">
  <meta name="theme-color" content="#060a10">
  <link rel="icon" type="image/png" href="../assets/icon.png">
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="../docs/docs.css">
  <script type="application/ld+json">
{ld}
  </script>
</head>
<body class="docs-body">
  <div class="bg-field"></div>
  <div class="bg-grid"></div>
  <div class="bg-grain"></div>
  <header class="nav" id="nav">
    <div class="nav-inner">
      <a class="brand" href="../"><img src="../assets/icon.png" alt="Gantry icon" width="30" height="30"><span>Gantry</span></a>
      <nav class="nav-links">
        <a href="../#features">Features</a>
        <a href="../apple-container/"{active("apple-container")}>apple/container</a>
        <a href="../apple-container-kubernetes/"{active("apple-container-kubernetes")}>Kubernetes</a>
        <a href="../compare/"{active("compare")}>Compare</a>
        <a href="../docs/index.html">Docs</a>
        <a href="{GITHUB}">GitHub</a>
      </nav>
    </div>
  </header>

  <main class="page-shell">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Gantry</a><span aria-hidden="true">/</span><span aria-current="page">{html.escape(crumb)}</span></nav>
    <article class="docs-article page-article">
{body.strip()}
{faq_html}
<p class="updated">Last updated {UPDATED}.</p>
    </article>
    <footer class="docs-foot">
      <a href="../">Home</a>
      <span>·</span>
      <a href="../apple-container/">apple/container guide</a>
      <span>·</span>
      <a href="../apple-container-kubernetes/">Kubernetes</a>
      <span>·</span>
      <a href="../compare/">Compare</a>
      <span>·</span>
      <a href="../docs/index.html">Docs</a>
      <span>·</span>
      <a href="{GITHUB}">MIT licensed · GitHub</a>
    </footer>
  </main>

  <script>
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


def table(head, rows):
    th = "".join(f'<th scope="col">{h}</th>' for h in head)
    body = "\n".join(
        "<tr>" + f'<th scope="row">{r[0]}</th>' + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>"
        for r in rows)
    return f'<div class="table-wrap"><table>\n<thead><tr>{th}</tr></thead>\n<tbody>\n{body}\n</tbody>\n</table></div>'


INSTALL = "brew install --cask getgantry/tap/gantry"
APPLE_REPO = "https://github.com/apple/container"
APPLE_ABOUT = [{"@type": "SoftwareApplication", "name": "container (apple/container)",
                "url": APPLE_REPO, "operatingSystem": "macOS",
                "applicationCategory": "DeveloperApplication"}]

PAGES = {}

# ------------------------------------------------------------------ guide
GUIDE_MAP = [
    ("<code>container run</code>, <code>container create</code>", "New Container sheet and Quick Run: image, name, command, ports, environment, volumes, DNS domain, custom kernel and boot arguments", "Any"),
    ("<code>container list --all</code>", "Containers list, grouped by Compose project, with state filters and search", "Any"),
    ("<code>container start</code>, <code>stop</code>, <code>kill</code>, <code>delete</code>, <code>prune</code>", "Toolbar, right-click menu and the menu bar panel", "Any"),
    ("<code>container logs</code>", "Logs tab: live follow, regex search, level filter, ANSI color", "Any"),
    ("<code>container stats</code>", "Stats tab and fleet dashboard sparklines", "Any"),
    ("<code>container exec</code>", "Terminal tab (interactive shell) and Processes tab", "Any"),
    ("<code>container inspect</code>", "Overview and Inspect tabs", "Any"),
    ("<code>container export</code>", "Export Filesystem (tar)", "Any"),
    ("<code>container commit</code>", "Commit to Image", "1.6"),
    ("<code>container copy</code>", "Files tab: download and drag out to Finder (the container must be started)", "Any; tested on 1.6.1"),
    ("<code>container exec</code> with <code>tar</code>", "Files tab: upload files and drop whole folders from Finder", "Any"),
    ("<code>container clean</code>", "Trim Disk on a running container, and a row in Reclaim Space", "1.4"),
    ("<code>container image pull</code>, <code>tag</code>, <code>delete</code>, <code>prune</code>, <code>inspect</code>", "Images: pull with progress, tag, remove, prune, inspect", "Any"),
    ("<code>container build</code>", "Builds the <code>build:</code> services of a Compose file", "Any"),
    ("<code>container volume create</code>, <code>delete</code>, <code>inspect</code>, <code>prune</code>", "Volumes", "Any"),
    ("<code>container network create</code>, <code>delete</code>, <code>inspect</code>, <code>prune</code>", "Networks", "Any"),
    ("<code>--network &lt;name&gt;,alias=…</code>", "Network DNS aliases, subtree aliases (<code>.gateway</code>) and Compose service names", "Any; tested on 1.6.1"),
    ("<code>container system start</code>, <code>stop</code>", "System section: start, stop and restart the services; also in the menu bar and Settings", "Any"),
    ("<code>container system status</code>, <code>version</code>", "System section: status, client and server versions, host facts", "Any"),
    ("<code>container system logs</code>", "System section: Service Logs, live or over 5 minutes to 1 day, filtered by level, service and text", "Any"),
    ("<code>container system property list</code>", "System section: System Properties editor, saved to <code>~/.config/container/config.toml</code>", "Any; tested on 1.6.1"),
    ("<code>container system dns create</code>, <code>delete</code>, <code>list</code>", "Settings ▸ Apple: local DNS domains and a default domain", "Any"),
    ("<code>container system kernel set</code>", "System section: install the recommended kernel, a kernel file or a tar archive", "Any"),
    ("<code>container system df</code>", "Host overview disk usage and Reclaim Space", "Any"),
    ("<code>container builder start</code>, <code>stop</code>, <code>delete</code>, <code>status</code>", "System section: Image Builder with CPU, memory and DNS options", "Any"),
    ("<code>container registry login</code>, <code>logout</code>, <code>list</code>", "System section: Registry Logins (password on stdin only)", "Any"),
    ("<code>container machine create</code>, <code>run</code>, <code>stop</code>, <code>delete</code>, <code>set-default</code>, <code>set</code>, <code>inspect</code>", "Machines: create, start, stop, delete, default machine, CPUs and memory, shell, inspect, Open in VS Code", "Any; nested virtualization and kernels 1.1"),
    ("<code>container cluster create</code>, <code>list</code>, <code>delete</code>, <code>write-config</code>, <code>load-image</code>", "Clusters: Kubernetes clusters, nodes, kubeconfig, kubectl context, Load into Cluster", "1.5 (<code>k8s</code>), 1.6.1 (<code>cluster</code>)"),
    ("No <code>compose</code> command", "Compose runner: bring up a <code>docker-compose.yml</code> from Finder, the File menu or drag and drop", "Any"),
]

GUIDE_FAQ = [
    ("What is the best GUI for Apple container?",
     'Gantry is a free, open-source native macOS GUI made for apple/container. It maps the <code>container</code> CLI to a desktop app: containers, logs, stats and exec, plus Kubernetes clusters, machines, the image builder, registry logins, kernels, service logs and system properties. The table on this page lists each command and the Gantry feature that uses it.'),
    ("Does Apple container have a GUI?",
     'Apple ships <code>container</code> as a command-line tool only. Gantry is a separate open-source app that gives it a GUI, next to your Docker hosts.'),
    ("Can I use docker compose with Apple container?",
     'apple/container has no <code>compose</code> command. Gantry reads a <code>docker-compose.yml</code>, builds <code>build:</code> services, creates the network and named volumes, and starts the services in <code>depends_on</code> order. Service names resolve through network DNS aliases.'),
    ("How do I open a container machine in VS Code?",
     'Start the machine in Gantry and click <b>Open in VS Code</b>. Gantry opens it over Remote-SSH, as in Apple\'s <code>container-machine-vscode</code> example. The machine image must run <code>sshd</code>.'),
    ("Does Apple container work on Intel Macs?",
     'No. apple/container needs a Mac with Apple silicon. Gantry runs on Intel Macs too, but there it manages Docker hosts only.'),
    ("Which container CLI version should I install?",
     'Gantry needs 1.0 or later and is tested with 1.6.1. Install it with the signed installer package from the <a href="https://github.com/apple/container/releases">apple/container releases page</a>. The Homebrew build does not include the machine backend, so <code>container machine</code> does not work with it.'),
]

PAGES["apple-container"] = dict(
    title="Apple container GUI for Mac: the complete apple/container guide",
    crumb="apple/container guide",
    desc="What Apple's container tool is, how to install it, and how Gantry manages it: a table of each container CLI command and its Gantry feature, from compose to Kubernetes.",
    about=APPLE_ABOUT,
    faq=GUIDE_FAQ,
    body=f"""
<h1>Apple container on Mac: the complete guide and GUI</h1>
<p class="page-lead">apple/container runs Linux containers on your Mac, each in its own lightweight virtual machine. It ships as a command-line tool. Gantry is a native macOS GUI for it. This guide explains the tool, how to set it up, and which Gantry feature covers each <code>container</code> command.</p>

<div class="tldr">
<p><strong>In short.</strong> Gantry is a free, open-source (MIT) macOS app that manages Apple's <code>container</code> tool and Docker from one window. It supports <code>container</code> CLI 1.0 to 1.6.1 (recommended) and shows only the features your CLI version supports. Install it with <code>{INSTALL}</code>.</p>
</div>

<h2 id="what-is">What is apple/container?</h2>
<p><a href="{APPLE_REPO}">apple/container</a> is an open-source tool from Apple, written in Swift, that creates and runs Linux containers on a Mac. Docker Desktop runs all containers in one shared Linux VM; apple/container runs each container in its own lightweight virtual machine, built on Apple's Virtualization framework. It uses standard OCI images, so it pulls from and pushes to the same registries as Docker.</p>
<ul>
  <li><strong>Hardware:</strong> a Mac with Apple silicon.</li>
  <li><strong>macOS:</strong> Apple supports it on macOS 26.</li>
  <li><strong>Interface:</strong> the <code>container</code> CLI only. There is no desktop app and no <code>compose</code> command.</li>
  <li><strong>Networking:</strong> each container gets its own IP address on your Mac, and local DNS domains give containers names such as <code>web.test</code>.</li>
</ul>

<h2 id="why-gui">Why use a GUI for apple/container?</h2>
<p>The CLI is complete, but daily work means many commands: <code>container list</code>, <code>logs</code>, <code>stats</code>, <code>exec</code>, then <code>system</code>, <code>builder</code>, <code>registry</code>, <code>machine</code> and <code>cluster</code> for the rest. Gantry puts them in one window with live updates, so you see the state instead of polling for it. It also adds what the CLI does not have: Compose files, failure notifications, a fleet view with your Docker hosts, and an MCP server for AI agents.</p>

<h2 id="setup">Set up apple/container with Gantry</h2>
<ol>
  <li>Install Gantry: <code>{INSTALL}</code>, then clear the quarantine flag (see <a href="../docs/install.html">Install</a>).</li>
  <li>Install the <code>container</code> CLI from the signed <code>.pkg</code> on the <a href="{APPLE_REPO}/releases">apple/container releases page</a>. If it is missing or older than 1.0, Gantry shows a setup sheet with the steps.</li>
  <li>In Gantry, choose <strong>Add Host…</strong> and add an <em>Apple Container</em> host. Connecting starts the <code>container</code> services if they are stopped.</li>
  <li>If no default kernel is installed, the host overview shows a banner. Click it to install the recommended kernel.</li>
</ol>
{callout("warn", 'Use the signed installer package, not the Homebrew build. The Homebrew build does not include the machine backend, so <code>container machine</code> cannot run.')}

<h2 id="command-map">Each container command and its Gantry feature</h2>
<p>This table maps the <code>container</code> CLI to Gantry. The last column shows the CLI version that Gantry needs for the feature. <em>Any</em> means any supported CLI, 1.0 or later. Gantry reads your installed version and hides the features that it does not support.</p>
{table(["CLI command", "Gantry feature", "CLI version Gantry needs"], GUIDE_MAP)}

<h2 id="features">What Gantry adds on apple/container</h2>

<h3 id="kubernetes">Kubernetes clusters</h3>
<p>Create multi-worker Kubernetes clusters with <code>container cluster</code>, choose the CNI, see each node, write the kubeconfig and load local images into the cluster. See <a href="../apple-container-kubernetes/">Kubernetes on apple/container</a>.</p>

<h3 id="machines">Container machines and VS Code</h3>
<p>Machines are long-lived Linux environments from <code>container machine</code>. Gantry creates, starts, stops and deletes them, sets the default machine, edits CPUs and memory, and opens a shell. On CLI 1.1 or later, a machine can boot with nested virtualization (Apple silicon M3 or newer) and a custom kernel. <strong>Open in VS Code</strong> connects to a running machine over Remote-SSH; the machine image must run <code>sshd</code>.</p>

<h3 id="compose">Docker Compose on apple/container</h3>
<p>Open a <code>docker-compose.yml</code> from Finder (<em>Open With ▸ Gantry</em> or <em>Quick Actions ▸ Compose Up in apple/container</em>), from <strong>File ▸ Open Compose File…</strong>, or by dropping it on the window. Gantry builds <code>build:</code> services, creates the project network and named volumes, and starts each service in <code>depends_on</code> order with the standard <code>com.docker.compose.*</code> labels. With a default DNS domain set, services reach each other by service name through network aliases.</p>

<h3 id="dns">Network DNS aliases and local domains</h3>
<p>Gantry passes network aliases to <code>container</code> as <code>--network &lt;name&gt;,alias=…</code>. Without a default DNS domain, only fully qualified names pass, and a subtree alias (a leading dot, such as <code>.gateway</code>) passes only as its exact alias. With a default domain, short names work too. Gantry creates and deletes local DNS domains, sets the default domain, and gives new containers a <code>name.domain</code> hostname. See <a href="../docs/dns.html">Local DNS names</a>.</p>

<h3 id="system">System: services, builder, registries, kernel, logs, properties</h3>
<p>Each apple/container host has a <strong>System</strong> section. It works while the host is disconnected, so you can start stopped services from there.</p>
<ul>
  <li><strong>Status and version:</strong> client and server versions, with a warning when they differ; start, stop and restart the services; host facts and paths.</li>
  <li><strong>Image Builder:</strong> state, image, CPUs, memory and IP; start with CPU, memory and DNS options; stop; delete.</li>
  <li><strong>Registry Logins:</strong> list, log in and log out. The password goes to the CLI on stdin (<code>--password-stdin</code>) only, and Gantry keeps no copy.</li>
  <li><strong>Kernel:</strong> install the recommended kernel, a kernel file or a tar archive, with streamed progress.</li>
  <li><strong>Service Logs:</strong> live or one-shot, over 5 minutes to 1 day, filtered by level, service and text.</li>
  <li><strong>System Properties:</strong> edits go to <code>~/.config/container/config.toml</code>, with a pending-restart flag and a <strong>Restart Services</strong> button.</li>
</ul>

<h3 id="disk">Commit, Trim Disk and files</h3>
<p><strong>Commit to Image</strong> uses <code>container commit</code> (CLI 1.6). <strong>Trim Disk</strong> uses <code>container clean</code> (CLI 1.4) and also shows as a row in Reclaim Space. The Files tab downloads files and lets you drag them out to Finder with <code>container copy</code> (the container must be started), and uploads files and folders.</p>

<h3 id="labels">Labels that contain <code>=</code></h3>
<p><code>container create</code> rejects a label value that contains <code>=</code>, also on CLI 1.6.1. Gantry encodes such values when it creates the container and decodes them when it reads it back, so the labels you set are the labels you see.</p>

<h3 id="agents">MCP server and Shortcuts</h3>
<p>The bundled <code>gantry-mcp</code> server gives AI agents the same reach on apple/container hosts: containers, images, volumes, networks, Compose, machines (<code>list_machines</code>, <code>create_machine</code> and more), clusters (<code>list_clusters</code>, <code>create_cluster</code>, <code>delete_cluster</code>) and <code>apple_*</code> system tools for services, builder, registries (no login tool), properties, logs and kernel install. App Intents add Shortcuts and Siri actions. See <a href="../docs/mcp.html">AI agents &amp; MCP</a>.</p>
{code("Add the Gantry MCP server", "claude mcp add gantry -- /Applications/Gantry.app/Contents/Resources/gantry-mcp")}

<h2 id="vs-docker">apple/container next to Docker</h2>
<p>Gantry manages apple/container hosts, the local Docker daemon (Docker Desktop, OrbStack, Colima) and remote Docker hosts over SSH in one sidebar and one fleet dashboard. You do not have to choose one runtime. For a feature-by-feature view of the tools, see <a href="../compare/">Gantry vs Docker Desktop, OrbStack and Podman Desktop</a>.</p>
""")

# ------------------------------------------------------------------ kubernetes
K8S_FAQ = [
    ("Does Apple container support Kubernetes?",
     'Yes. The <code>container</code> CLI creates Kubernetes clusters whose nodes run as containers: <code>container cluster</code> in CLI 1.6.1, <code>container k8s</code> in CLI 1.5.0 to 1.6.0. Gantry gives this a GUI.'),
    ("Does Gantry support container cluster?",
     'Yes. Gantry lists, creates and deletes clusters on apple/container hosts, shows their nodes, writes the kubeconfig, copies the <code>kubectl</code> context command and loads local images into a cluster. It uses <code>cluster</code> or <code>k8s</code> to match your CLI version.'),
    ("How do I use kubectl with an apple/container cluster?",
     'When the CLI creates a cluster, it adds a kubeconfig context named after the cluster to <code>~/.kube/config</code>. Run <code>kubectl --context &lt;name&gt; get nodes</code>. To keep a separate file, use <b>Write Kubeconfig</b> in Gantry; the default path is <code>~/.kube/&lt;name&gt;.kubeconfig</code>.'),
    ("How do I get a local image into the cluster without a registry?",
     'In Gantry, right-click the image in Images and choose <b>Load into Cluster</b>. Gantry runs <code>container cluster load-image</code>, which copies the image into the containerd of each node.'),
    ("Can I create a multi-node cluster?",
     'Yes. Set the number of workers in the create sheet. Workers need CLI 1.6.0 or later.'),
    ("Can I use my own CNI such as Calico or Cilium?",
     'Yes. Choose <b>Custom manifest</b> and select the manifest file, or choose <b>None</b> and apply a CNI yourself after the cluster starts. Nodes stay NotReady until a CNI runs. <b>None</b> needs CLI 1.6.0 or later. The default CNI is the bundled kindnet manifest.'),
]

K8S_OPTIONS = [
    ("Name", "<code>--name</code>", "Also the kubeconfig context name"),
    ("Workers", "<code>--workers</code>", "Number of worker nodes. CLI 1.6.0+"),
    ("CPUs", "<code>--cpus</code>", "Per node"),
    ("Memory", "<code>--memory</code>", "Per node, for example <code>4G</code>"),
    ("Node image", "<code>--node-image</code>", "Empty keeps the CLI default"),
    ("CNI", "<code>--cni</code>", "Default (bundled kindnet), None (<code>NONE</code>, CLI 1.6.0+) or a custom manifest path"),
]

PAGES["apple-container-kubernetes"] = dict(
    title="Kubernetes on Apple container: a GUI for container cluster on Mac",
    crumb="Kubernetes on apple/container",
    desc="Run Kubernetes on Apple's container tool with Gantry: create multi-worker clusters with container cluster, pick a CNI, view nodes, write the kubeconfig and load local images.",
    about=APPLE_ABOUT + [{"@type": "SoftwareApplication", "name": "Kubernetes", "url": "https://kubernetes.io/"}],
    faq=K8S_FAQ,
    body=f"""
<h1>Kubernetes on Apple container</h1>
<p class="page-lead">apple/container can run a Kubernetes cluster whose nodes are containers on your Mac. Gantry is a GUI for it: create a cluster, watch its nodes come up, connect <code>kubectl</code> and load your local images, without long <code>container cluster</code> command lines.</p>

<div class="tldr">
<p><strong>In short.</strong> On an apple/container host, the Gantry <strong>Clusters</strong> section creates and deletes Kubernetes clusters with <code>container cluster</code> (CLI 1.6.1) or <code>container k8s</code> (CLI 1.5.0 to 1.6.0). It supports multiple workers, a custom CNI, a nodes view, kubeconfig and <code>kubectl</code> context, and <strong>Load into Cluster</strong> for local images.</p>
</div>

<h2 id="requirements">Requirements</h2>
<ul>
  <li>A Mac with Apple silicon, macOS 26, and Gantry (<code>{INSTALL}</code>).</li>
  <li>The <code>container</code> CLI 1.5.0 or later; 1.6.1 is recommended. Workers and the <em>None</em> CNI need 1.6.0 or later.</li>
  <li><code>kubectl</code>, if you want to use the cluster from the terminal.</li>
</ul>

<h2 id="create">Create a cluster</h2>
<ol>
  <li>Select your apple/container host and open <strong>Clusters</strong> in the sidebar.</li>
  <li>Start a new cluster and fill in the options below.</li>
  <li>Create it. The list shows the new cluster with streamed progress. <strong>Cancel</strong> stops the creation and deletes the nodes that were already made.</li>
</ol>
{table(["Option", "CLI flag", "Notes"], K8S_OPTIONS)}
<p>The same command on the CLI:</p>
{code("Shell", "container cluster create --name dev --workers 2 --cpus 2 --memory 4G")}

<h2 id="nodes">Nodes and cluster details</h2>
<p>The cluster list shows each cluster with its nodes: role, state and address. The detail view has an <strong>Overview</strong> (kubectl context, API server, workers, node network), a <strong>Nodes</strong> table, <strong>Inspect</strong> for the raw node data, and the actions <strong>Write Kubeconfig</strong>, <strong>Copy kubectl Context Command</strong> and <strong>Delete</strong>.</p>

<h2 id="kubectl">Connect kubectl</h2>
<p>The CLI adds a context named after the cluster to <code>~/.kube/config</code> when it creates the cluster. Use <strong>Copy kubectl Context Command</strong> in Gantry, or type it:</p>
{code("Shell", "kubectl --context dev get nodes")}
<p>To keep the cluster in its own file, use <strong>Write Kubeconfig</strong>. Gantry runs <code>container cluster write-config</code>; the default path is <code>~/.kube/&lt;name&gt;.kubeconfig</code>.</p>

<h2 id="images">Load local images into the cluster</h2>
<p>Build or pull an image on the apple/container host, then right-click it in <strong>Images</strong> and choose <strong>Load into Cluster</strong>. Gantry runs <code>container cluster load-image</code>, which copies the image into the containerd of each node. You do not need a registry for local development.</p>
{code("Shell", "container cluster load-image --name dev myapp:dev")}

<h2 id="cni">Choose a CNI</h2>
<p>The default is the bundled kindnet manifest. Choose <strong>Custom manifest</strong> to install your own CNI, for example Calico or Cilium, from a file. Choose <strong>None</strong> to install a CNI yourself later; until then, the nodes stay NotReady.</p>

<h2 id="agents">Clusters from AI agents</h2>
<p>The Gantry MCP server has <code>list_clusters</code>, <code>create_cluster</code> and <code>delete_cluster</code>, so an agent such as Claude Code can make a temporary cluster for a test and remove it after.</p>
{code("Add the Gantry MCP server", "claude mcp add gantry -- /Applications/Gantry.app/Contents/Resources/gantry-mcp")}

<h2 id="more">More on apple/container</h2>
<p>Read the <a href="../apple-container/">apple/container guide</a> for each <code>container</code> command and its Gantry feature, or see how Gantry compares with <a href="../compare/">Docker Desktop, OrbStack and Podman Desktop</a>.</p>
""")

# ------------------------------------------------------------------ compare
COMPARE = [
    ("What it is", "Native GUI client. Uses the engine you already have", "Docker engine in a Linux VM, plus a GUI", "Docker and Linux engine, plus a GUI", "GUI for Podman (and other engines)", "Apple's CLI and runtime"),
    ("License and price", "MIT, free for all use", "Proprietary. Free for personal use, education, non-commercial open source and small businesses (fewer than 250 employees and less than $10M annual revenue); paid subscription otherwise", "Proprietary. Free for personal, non-commercial use; paid license for commercial use", "Apache 2.0, free", "Apache 2.0, free"),
    ("Source code", "Open", "Closed", "Closed", "Open", "Open"),
    ("UI technology", "SwiftUI (native)", "Electron", "Native macOS app", "Electron", "No GUI"),
    ("Platforms", "macOS 26+, Apple silicon and Intel", "macOS, Windows, Linux", "macOS", "macOS, Windows, Linux", "macOS on Apple silicon"),
    ("Manages apple/container", "Yes, CLI 1.0 to 1.6.1", "No", "No", "Not in vendor docs (checked 2026-11-03)", "It is apple/container"),
    ("Kubernetes", "On apple/container, through <code>container cluster</code>: multi-worker, custom CNI", "Built-in Kubernetes", "Built-in Kubernetes", "Through Kind and other providers", "<code>container cluster</code> (1.6.1), <code>container k8s</code> (1.5.0 to 1.6.0)"),
    ("Docker Compose", "On Docker hosts and on apple/container (Gantry runs the file)", "Yes", "Yes", "Yes, through a Compose provider", "No <code>compose</code> command"),
    ("Long-lived Linux machines", "<code>container machine</code>, with Open in VS Code", "No", "Yes (Linux machines)", "No (Podman machine is the engine VM)", "<code>container machine</code>"),
    ("Remote Docker hosts over SSH in the GUI", "Yes, with ProxyJump and Keychain secrets", "Unknown", "Unknown", "Unknown", "Not applicable"),
    ("Bundled MCP server that manages your containers", "Yes (<code>gantry-mcp</code>)", "Unknown", "Unknown", "Unknown", "No"),
]

COMPARE_FAQ = [
    ("Is Gantry a Docker Desktop alternative?",
     'For the GUI, yes. Gantry manages containers, images, volumes, networks, logs, stats and Compose. It does not include a Docker engine: on a Mac, use OrbStack, Colima or Docker Desktop for that, or use Apple\'s <code>container</code> tool, which Gantry also manages. Gantry is MIT licensed and free for commercial use.'),
    ("Is Gantry an OrbStack alternative?",
     'Partly. OrbStack is an engine and a GUI; Gantry is a GUI only. You can use Gantry as the GUI on top of the OrbStack Docker engine, or use Gantry with apple/container, which gives you containers, Linux machines and Kubernetes from Apple\'s own tool.'),
    ("Which is the best GUI for Apple container?",
     'Of the tools on this page, Gantry is the only one that manages apple/container (checked 2026-11-03). It covers the whole <code>container</code> CLI, including clusters, machines, builder, registries and system properties.'),
    ("Can I use Gantry and Docker Desktop together?",
     'Yes. Gantry connects to the Docker Desktop engine over its socket, so you can use Gantry as the GUI and keep Docker Desktop as the engine.'),
]

PAGES["compare"] = dict(
    title="Gantry vs Docker Desktop vs OrbStack vs Podman Desktop vs container CLI",
    crumb="Compare",
    desc="A factual comparison of Gantry, Docker Desktop, OrbStack, Podman Desktop and Apple's container CLI on macOS: license, price, UI, apple/container support, Kubernetes, Compose and machines.",
    about=[{"@type": "SoftwareApplication", "name": n} for n in ("Gantry", "Docker Desktop", "OrbStack", "Podman Desktop", "container (apple/container)")],
    faq=COMPARE_FAQ,
    body=f"""
<h1>Gantry vs Docker Desktop, OrbStack, Podman Desktop and the container CLI</h1>
<p class="page-lead">Five ways to run and manage containers on a Mac, compared on facts you can check. Gantry is a GUI client. The others include an engine, except the <code>container</code> CLI, which is an engine with no GUI.</p>

<div class="tldr">
<p><strong>In short.</strong> Pick <strong>Gantry</strong> if you want a free, native, open-source GUI for Apple's <code>container</code> tool and for Docker (local and over SSH) in one app. Gantry does not replace a Docker engine; it works with the one you have, or with apple/container.</p>
</div>

<h2 id="table">Comparison table</h2>
<p>Facts as of 2026-11-03, from each vendor's public pages (see <a href="#sources">sources</a>). "Unknown" means we did not find the fact in the vendor's documentation. It does not mean that the feature is missing.</p>
{table(["", "Gantry", "Docker Desktop", "OrbStack", "Podman Desktop", "<code>container</code> CLI"], COMPARE)}

<h2 id="when">When to choose which</h2>
<h3>Choose Gantry</h3>
<p>You use Apple's <code>container</code> tool and want a GUI for all of it, including Kubernetes clusters, machines and the image builder. Or you manage several Docker hosts, local and remote over SSH, and want one native window and failure notifications for all of them. Or you want an MCP server so AI agents can manage your containers.</p>
<h3>Choose Docker Desktop</h3>
<p>You need the Docker engine with the same app on macOS, Windows and Linux, Docker extensions and Docker support, and your company has a Docker subscription or qualifies for free use.</p>
<h3>Choose OrbStack</h3>
<p>You want a Docker engine and Linux machines on macOS in one product, and a paid license for commercial use is acceptable.</p>
<h3>Choose Podman Desktop</h3>
<p>You use Podman, want an open-source GUI on several operating systems, or work with Red Hat tools.</p>
<h3>Choose the container CLI only</h3>
<p>You script everything in the terminal and do not need a GUI. Gantry uses the same CLI, so you can add the GUI later.</p>

<h2 id="together">Use them together</h2>
<p>Gantry is a client, so it works next to the others. It connects to the Docker engine of Docker Desktop, OrbStack or Colima through the Docker socket, to remote Docker hosts over SSH, and to apple/container through the <code>container</code> CLI, all in one sidebar.</p>

<h2 id="sources">Sources</h2>
<ul>
  <li>Docker Desktop license terms: <a href="https://www.docker.com/pricing/faq/">Docker pricing FAQ</a>.</li>
  <li>OrbStack license terms: <a href="https://docs.orbstack.dev/licensing">OrbStack licensing</a>.</li>
  <li>Podman Desktop license and features: <a href="https://github.com/podman-desktop/podman-desktop">podman-desktop on GitHub</a> and <a href="https://podman-desktop.io/docs">Podman Desktop docs</a>.</li>
  <li>apple/container: <a href="{APPLE_REPO}">apple/container on GitHub</a>.</li>
  <li>Gantry: <a href="{GITHUB}">source code</a> and <a href="{GITHUB}/blob/main/CHANGELOG.md">changelog</a>.</li>
</ul>
<p>Found an error? <a href="https://github.com/getgantry/getgantry.github.io/issues">Open an issue</a> and we will fix the table.</p>
""")


def home_faq():
    with open(os.path.join(ROOT, "index.html")) as f:
        page = f.read()
    return re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", page, re.S)


def llms_full():
    """Plain-text copy of llms.txt plus the tables and answers of every page."""
    with open(os.path.join(ROOT, "llms.txt")) as f:
        intro = f.read().split("\n## ")[0].rstrip()
    out = [intro, "", f"Last updated: {UPDATED}", ""]
    out += ["## container CLI command to Gantry feature", ""]
    out += [f"- {plain(c)}: {plain(g)} (CLI version: {plain(v)})" for c, g, v in GUIDE_MAP]
    out += ["", "## Kubernetes cluster create options", ""]
    out += [f"- {plain(o)} ({plain(fl)}): {plain(n)}" for o, fl, n in K8S_OPTIONS]
    out += ["", f"## Comparison (facts as of {UPDATED}; Unknown means not found in vendor docs)", ""]
    names = ["Gantry", "Docker Desktop", "OrbStack", "Podman Desktop", "container CLI"]
    for row in COMPARE:
        out.append(f"- {plain(row[0])}: " + "; ".join(f"{n}: {plain(c)}" for n, c in zip(names, row[1:])))
    out += ["", "## Questions and answers", ""]
    seen = set()
    for q, a in home_faq() + GUIDE_FAQ + K8S_FAQ + COMPARE_FAQ:
        q = plain(q)
        if q in seen:
            continue
        seen.add(q)
        out += [f"Q: {q}", f"A: {' '.join(plain(a).split())}", ""]
    out += ["## Pages", ""]
    out += [f"- {SITE}/{slug}/ : {p['title']}" for slug, p in PAGES.items()]
    out += [f"- {SITE}/ : Home", f"- {SITE}/docs/index.html : Documentation", f"- {GITHUB} : Source code", ""]
    with open(os.path.join(ROOT, "llms-full.txt"), "w") as f:
        f.write("\n".join(out))


def main():
    llms_full()
    for slug, p in PAGES.items():
        out_dir = os.path.join(ROOT, slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w") as f:
            f.write(page_html(slug, p["title"], p["desc"], p["crumb"], p["body"], p.get("faq"), p.get("about")))
    print(f"Wrote {len(PAGES)} pages")


if __name__ == "__main__":
    main()
