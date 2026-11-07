#!/usr/bin/env python3
"""Generate the home page and the marketing pages in every language, plus sitemap.xml and lang.js.

Run from the repo root after build_docs.py. Strings: i18n/<lang>.json. Templates: templates/.
`python3 build_pages.py --check` only validates the string files.
"""
import copy
import html
import json
import os
import posixpath
import re
import sys

from build_docs import GITHUB

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://getgantry.github.io"
UPDATED = "2026-11-07"
APP_VERSION = "0.27.0"
# Features that are built on a branch but not merged yet. The pages show the text for the shipped state only when
# the flag is True; flip a flag when its branch merges and rebuild.
FLAGS = {
    "k8s_native": False,        # feat/kubernetes-native: Kubernetes browser without kubectl
    "external_storage": False,  # feat/external-storage: move the data root, volumes on a disk, unplug safety
}
VARIANTS = {"_native": "k8s_native", "_shipped": "external_storage"}
FIXED_KEYS = {"id", "code", "table", "shot", "when", "unless"}
APP_UI_LANGUAGES = ["en", "zh-Hans", "de", "fr", "es", "it", "pt-PT", "nl", "sv", "da", "nb", "fi", "pl", "cs", "sk", "hu", "ro", "bg", "el", "hr", "sl", "sr", "sr-Latn", "lt", "lv", "et", "uk", "ru"]
INSTALL = "brew install --cask getgantry/tap/gantry"
MCP_CMD = "claude mcp add gantry -- /Applications/Gantry.app/Contents/Resources/gantry-mcp"
APPLE_REPO = "https://github.com/apple/container"
APPLE_ABOUT = [{"@type": "SoftwareApplication", "name": "container (apple/container)",
                "url": APPLE_REPO, "operatingSystem": "macOS",
                "applicationCategory": "DeveloperApplication"}]

# slug -> (strings key, sitemap changefreq, sitemap priority)
PAGES = {
    "": ("home", "weekly", "1.0"),
    "apple-container": ("guide", "weekly", "0.9"),
    "apple-container-kubernetes": ("k8s", "weekly", "0.9"),
    "compare": ("compare", "monthly", "0.8"),
}
# How-to guides: slug -> (sitemap changefreq, priority). Strings: guides.<slug>.
GUIDES = {
    "docker-desktop-to-apple-container": ("monthly", "0.8"),
    "containers-on-external-drive": ("monthly", "0.7"),
    "docker-run-to-container": ("monthly", "0.7"),
}
# Commands in the guides and in the terminal walk-through of the Kubernetes page (key "k8s"). Not translated.
GUIDE_CODE = {
    "k8s": {
        "start": "container system start",
        "create": "container cluster create --name dev --cpus 2 --memory 2g \\\n"
                  "  --workers count=2,cpus=2,memory=2g --shared-image-store",
        "list": "container cluster list --nodes\nkubectl --context dev get nodes",
        "build": "printf 'FROM nginx:alpine\\n' > Dockerfile\ncontainer build -t hello:dev .\n"
                 "kubectl --context dev create deployment hello --image=hello:dev\nkubectl --context dev get pods",
        "forward": "kubectl --context dev port-forward deployment/hello 8080:80",
        "delete": "container cluster delete --name dev",
    },
    "docker-desktop-to-apple-container": {
        "images": "docker save -o app.tar app:dev\ncontainer image load -i app.tar\ncontainer image pull nginx:alpine",
        "volumes": "docker run --rm -v data:/from -v \"$PWD\":/to alpine tar -C /from -cf /to/data.tar .\n"
                   "container volume create data\n"
                   "container run --rm -v data:/to -v \"$PWD\":/from alpine tar -C /to -xf /from/data.tar",
    },
    "containers-on-external-drive": {
        "status": "container system status | grep appRoot\ncontainer system df",
        "bind": "mkdir -p /Volumes/Fast/site\n"
                "container run -d --name web -p 8080:80 \\\n  -v /Volumes/Fast/site:/usr/share/nginx/html:ro nginx:alpine",
        "move": "container system stop\n"
                "cp -Rp ~/Library/Application\\ Support/com.apple.container /Volumes/Fast/container\n"
                "container system start --app-root /Volumes/Fast/container\n"
                "container system status | grep appRoot\n"
                "container ls -a && container image ls && container volume ls",
        "save": "mkdir -p /Volumes/Fast/images\n"
                "container image save -o /Volumes/Fast/images/myapp.tar myapp:dev\n"
                "container image delete myapp:dev\n"
                "container image load -i /Volumes/Fast/images/myapp.tar",
    },
    "docker-run-to-container": {
        "docker": "docker run -d --name cache --restart unless-stopped -p 6379:6379 \\\n"
                  "  -v redisdata:/data redis:7 redis-server --appendonly yes",
        "container": "container volume create redisdata\n"
                     "container run -d --name cache -p 6379:6379 \\\n"
                     "  -v redisdata:/data redis:7 redis-server --appendonly yes",
    },
}
# Screenshots of 0.27.0 features. Until the file exists, the page has a TODO-SCREENSHOT comment in its place.
SHOT_DIR = "assets/shots/0.27.0"
SHOTS = {
    "home-dashboard": ("home, section #new (new design)", "dashboard.png"),
    "home-kube": ("home, section #new (Kubernetes browser)", "kubernetes-browser.png"),
    "home-explain": ("home, section #new (Explain Failure)", "explain-failure.png"),
    "k8s-browser": ("page apple-container-kubernetes, section #browser", "kubernetes-browser-dev.png"),
    "paste-command": ("guide docker-run-to-container, section #paste", "paste-command.png"),
    "storage-pane": ("guide containers-on-external-drive, section #gantry", "storage-pane.png"),
    "cluster-overview": ("page apple-container-kubernetes, section #nodes", "cluster-overview.png"),
}
DOCS = [("index", "weekly", "0.8"), ("install", "monthly", "0.7"), ("apple-container", "monthly", "0.8"),
        ("menu-bar", "monthly", "0.5"), ("hosts", "monthly", "0.6"), ("containers", "monthly", "0.6"),
        ("ports", "monthly", "0.5"), ("dns", "monthly", "0.6"), ("images-compose", "monthly", "0.6"),
        ("resources", "monthly", "0.6"), ("mcp", "monthly", "0.7"), ("troubleshooting", "monthly", "0.4")]


# ------------------------------------------------------------------ template engine
TOKEN = re.compile(r"{{\s*(.+?)\s*}}|{%\s*(.+?)\s*%}")
BLOCK_LINE = re.compile(r"^[ \t]*({%.+?%})[ \t]*\n", re.M)
FILTERS = {
    "attr": lambda s: html.escape(s, quote=True),
    "text": lambda s: html.escape(s, quote=False),
    "js": lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'",
}


def parse(src):
    src = BLOCK_LINE.sub(r"\1", src)
    root = []
    stack = [(None, root)]
    pos = 0
    for m in TOKEN.finditer(src):
        stack[-1][1].append(src[pos:m.start()])
        pos = m.end()
        if m.group(1):
            stack[-1][1].append(("var", m.group(1)))
            continue
        words = m.group(2).split()
        if words[0] == "for":
            node = ("for", words[1], words[3], [])
            stack[-1][1].append(node)
            stack.append((node, node[3]))
        elif words[0] == "if":
            node = ("if", words[1], [], [])
            stack[-1][1].append(node)
            stack.append((node, node[2]))
        elif words[0] == "else":
            stack[-1] = (stack[-1][0], stack[-1][0][3])
        elif words[0] in ("endfor", "endif"):
            stack.pop()
        else:
            raise ValueError(f"unknown tag {m.group(0)}")
    stack[-1][1].append(src[pos:])
    if len(stack) != 1:
        raise ValueError("unclosed block")
    return root


def lookup(ctx, path):
    val = ctx
    for part in path.split("."):
        val = val[int(part)] if isinstance(val, list) else val[part]
    return val


def render(nodes, ctx):
    out = []
    for n in nodes:
        if isinstance(n, str):
            out.append(n)
        elif n[0] == "var":
            path, *filters = [x.strip() for x in n[1].split("|")]
            v = lookup(ctx, path).replace("{root}", ctx["root"])
            for f in filters:
                v = FILTERS[f](v)
            out.append(v)
        elif n[0] == "for":
            out += [render(n[3], {**ctx, n[1]: item}) for item in lookup(ctx, n[2])]
        else:
            out.append(render(n[2] if lookup(ctx, n[1]) else n[3], ctx))
    return "".join(out)


_templates = {}


def template(name):
    if name not in _templates:
        with open(os.path.join(ROOT, "templates", name)) as f:
            _templates[name] = parse(f.read())
    return _templates[name]


# ------------------------------------------------------------------ strings
SR_LATN = dict(zip(
    "АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШабвгдђежзијклљмнњопрстћуфхцчџш",
    ["A", "B", "V", "G", "D", "Đ", "E", "Ž", "Z", "I", "J", "K", "L", "Lj", "M", "N", "Nj", "O", "P", "R",
     "S", "T", "Ć", "U", "F", "H", "C", "Č", "Dž", "Š",
     "a", "b", "v", "g", "d", "đ", "e", "ž", "z", "i", "j", "k", "l", "lj", "m", "n", "nj", "o", "p", "r",
     "s", "t", "ć", "u", "f", "h", "c", "č", "dž", "š"]))


def walk(node, fn):
    if isinstance(node, str):
        return fn(node)
    if isinstance(node, list):
        return [walk(x, fn) for x in node]
    return {k: walk(v, fn) for k, v in node.items()}


def load_languages():
    with open(os.path.join(ROOT, "i18n", "languages.json")) as f:
        return json.load(f)


def load_strings(lang):
    if lang.get("transliterate_from"):
        base = load_strings({"code": lang["transliterate_from"]})
        t = walk(base, lambda s: "".join(SR_LATN.get(ch, ch) for ch in s))
    else:
        with open(os.path.join(ROOT, "i18n", f"{lang['code']}.json")) as f:
            t = json.load(f)
    for key, val in lang.get("overrides", {}).items():
        parts = key.split(".")
        lookup(t, ".".join(parts[:-1]))[parts[-1]] = val
    return t


def signature(s):
    tags = sorted(re.findall(r"<[^>]+>", s))
    codes = sorted(re.findall(r"<code>(.*?)</code>", s, re.S))
    holes = sorted(re.findall(r"\{(?:root|date|n)\}", s))
    return tags, codes, holes


def check(en, t, path="", errors=None):
    errors = [] if errors is None else errors
    if type(en) is not type(t):
        errors.append(f"{path}: type differs")
    elif isinstance(en, dict):
        for k in en.keys() | t.keys():
            if k not in t:
                errors.append(f"{path}.{k}: missing")
            elif k not in en:
                errors.append(f"{path}.{k}: not in en.json")
            else:
                check(en[k], t[k], f"{path}.{k}", errors)
    elif isinstance(en, list):
        if len(en) != len(t):
            errors.append(f"{path}: {len(t)} items, en has {len(en)}")
        for i, (a, b) in enumerate(zip(en, t)):
            check(a, b, f"{path}[{i}]", errors)
    else:
        if path.rsplit(".", 1)[-1] in FIXED_KEYS and en != t:
            errors.append(f"{path}: must stay {en!r}")
        if not t.strip() and en.strip():
            errors.append(f"{path}: empty")
        for name, a, b in zip(("tags", "code", "placeholders"), signature(en), signature(t)):
            if a != b:
                errors.append(f"{path}: {name} differ: {sorted(set(a) ^ set(b))[:4]}")
    return errors


def resolve(node, flags=None):
    """Pick the text for the current FLAGS: `x_native` replaces `x` when its flag is on, and list items with
    `when` / `unless` drop out when their flag says so. Variant keys and conditions are removed."""
    flags = FLAGS if flags is None else flags
    if isinstance(node, list):
        keep = [x for x in node if not isinstance(x, dict)
                or (flags[x["when"]] if isinstance(x.get("when"), str) and x["when"] in flags else True)
                and (not flags[x["unless"]] if isinstance(x.get("unless"), str) and x["unless"] in flags else True)]
        return [resolve(x, flags) for x in keep]
    if not isinstance(node, dict):
        return node
    out = {}
    for k, v in node.items():
        if (k in ("when", "unless") and isinstance(v, str) and v in flags) or any(k.endswith(suf) for suf in VARIANTS):
            continue
        for suf, flag in VARIANTS.items():
            if flags[flag] and k + suf in node:
                v = node[k + suf]
        out[k] = resolve(v, flags)
    return out


# ------------------------------------------------------------------ helpers
def plain(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


def page_path(code, slug):
    parts = ([] if code == "en" else [code]) + ([slug] if slug else [])
    return "/" + "".join(p + "/" for p in parts)


def rel(src, dst):
    r = posixpath.relpath(dst, src)
    return "./" if r == "." else r + "/"


def table(head, rows):
    th = "".join(f'<th scope="col">{h}</th>' for h in head)
    body = "\n".join(
        "<tr>" + f'<th scope="row">{r[0]}</th>' + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>"
        for r in rows)
    return f'<div class="table-wrap"><table>\n<thead><tr>{th}</tr></thead>\n<tbody>\n{body}\n</tbody>\n</table></div>'


def code_block(title, body, copy_label):
    return f'''<div class="code-block">
  <div class="code-head"><span>{html.escape(title)}</span><button class="copy" data-copy="{html.escape(body, quote=True)}">{copy_label}</button></div>
  <pre><code>{html.escape(body)}</code></pre>
</div>'''


def callout_warn(body, label):
    return f'<div class="callout callout-warn"><span class="callout-tag">{label}</span><div>{body}</div></div>'


def shot(key, alt, caption, root, indent=""):
    section, name = SHOTS[key]
    rel_path = f"{SHOT_DIR}/{name}"
    if not os.path.exists(os.path.join(ROOT, rel_path)):
        return f'{indent}<!-- TODO-SCREENSHOT section="{section}" file="{rel_path}" -->'
    with open(os.path.join(ROOT, rel_path), "rb") as f:
        head = f.read(24)
    width, height = int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")  # PNG IHDR
    return (f'{indent}<figure class="guide-shot"><img src="{root}{rel_path}" alt="{html.escape(alt, quote=True)}" '
            f'width="{width}" height="{height}" loading="lazy" decoding="async"><figcaption>{caption}</figcaption>'
            f'</figure>')


def callout_note(body, label):
    return f'<div class="callout callout-note"><span class="callout-tag">{label}</span><div>{body}</div></div>'


def faq_ld(url, items):
    return {
        "@type": "FAQPage",
        "@id": f"{url}#faq",
        "mainEntity": [{"@type": "Question", "name": plain(q),
                        "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                       for q, a in items],
    }


GLOBE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'
         '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>')


def lang_links(langs, lang, slug, cls):
    here = page_path(lang["code"], slug)
    out = []
    for o in langs:
        cur = ' aria-current="page"' if o["code"] == lang["code"] else ""
        href = rel(here, page_path(o["code"], slug))
        out.append(f'<a href="{href}" hreflang="{o["code"]}" lang="{o["code"]}"{cur}>{o["name"]}</a>')
    return out


def chrome(langs, lang, t, slug, indent):
    pad = " " * indent
    code = lang["code"]
    alternates = [f'  <link rel="alternate" hreflang="{o["code"]}" href="{SITE}{page_path(o["code"], slug)}">'
                  for o in langs]
    alternates.append(f'  <link rel="alternate" hreflang="x-default" href="{SITE}{page_path("en", slug)}">')
    items = "\n".join(f"{pad}    <li>{a}</li>" for a in lang_links(langs, lang, slug, "menu"))
    label = html.escape(f'{t["chrome"]["language"]}: {lang["name"]}', quote=True)
    switcher = (f'{pad}<details class="lang-menu">\n'
                f'{pad}  <summary aria-label="{label}" title="{html.escape(t["chrome"]["language"], quote=True)}">'
                f'{GLOBE}<span class="lang-name">{lang["name"]}</span><span class="lang-code">{code.upper()}</span></summary>\n'
                f'{pad}  <ul>\n{items}\n{pad}  </ul>\n{pad}</details>\n')
    foot_pad = pad[:-2]
    footer = (f'{foot_pad}<nav class="lang-foot" aria-label="{html.escape(t["chrome"]["languages"], quote=True)}">\n'
              + "\n".join(f"{foot_pad}  {a}" for a in lang_links(langs, lang, slug, "foot"))
              + f"\n{foot_pad}</nav>\n")
    return "\n".join(alternates), switcher, footer


def base_ctx(langs, lang, t, slug, root, indent):
    alternates, switcher, footer = chrome(langs, lang, t, slug, indent)
    code = lang["code"]
    attrs = "" if code == "en" else f' data-copied="{html.escape(t["chrome"]["copied"], quote=True)}"'
    return {
        "t": t, "lang": code, "root": root, "og_locale": lang["og"], "html_attrs": attrs,
        "url": SITE + page_path(code, slug), "alternates": alternates, "switcher": switcher,
        "footer_langs": footer, "hint_script": f'  <script src="{root}lang.js" defer></script>\n',
        "updated": UPDATED, "flags": FLAGS,
    }


def ld_dump(graph, indent):
    text = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    return "\n".join(indent + line for line in text.split("\n"))


# ------------------------------------------------------------------ home
def home_ld(langs, code, t, url):
    h = t["home"]
    ld = h["ld"]
    app = {
        "@type": "SoftwareApplication",
        "@id": f"{SITE}/#app",
        "name": "Gantry",
        "alternateName": ld["app_alt_name"],
        "applicationCategory": "DeveloperApplication",
        "applicationSubCategory": ld["app_subcategory"],
        "operatingSystem": "macOS 26",
        "processorRequirements": ld["app_processor"],
        "softwareVersion": APP_VERSION,
        "inLanguage": APP_UI_LANGUAGES,
        "keywords": ld["app_keywords"],
        "url": url,
        "downloadUrl": f"{GITHUB}/releases/latest",
        "installUrl": f"{SITE}/docs/install.html",
        "releaseNotes": f"{GITHUB}/blob/main/CHANGELOG.md",
        "softwareHelp": {"@type": "CreativeWork", "url": f"{SITE}/docs/"},
        "screenshot": f"{SITE}/assets/dashboard.png",
        "license": f"{GITHUB}/blob/main/LICENSE",
        "codeRepository": GITHUB,
        "isAccessibleForFree": True,
        "description": ld["app_desc"],
        "featureList": ld["features"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "publisher": {"@id": f"{SITE}/#organization"},
    }
    step_urls = [f"{url}#install", f"{url}#install", f"{SITE}/docs/install.html", f"{SITE}/docs/mcp.html"]
    howto = {
        "@type": "HowTo",
        "@id": f"{url}#install-howto",
        "name": ld["howto_name"],
        "description": ld["howto_desc"],
        "tool": [{"@type": "HowToTool", "name": "Homebrew"}],
        "supply": [{"@type": "HowToSupply", "name": ld["howto_supply"]}],
        "step": [{"@type": "HowToStep", "position": i + 1, "name": s["name"], "text": s["text"], "url": u}
                 for i, (s, u) in enumerate(zip(ld["howto_steps"], step_urls))],
    }
    graph = [
        {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Gantry", "url": f"{SITE}/",
         "logo": f"{SITE}/assets/icon.png", "sameAs": [GITHUB]},
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Gantry",
         "description": ld["website_desc"], "publisher": {"@id": f"{SITE}/#organization"},
         "inLanguage": [o["code"] for o in langs]},
        {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": h["title"], "description": h["desc"],
         "inLanguage": code, "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#app"}},
        app,
        howto,
        faq_ld(url, [(f["q"], f["a"]) for f in h["faq"]["items"]]),
    ]
    return ld_dump(graph, "  ")


def render_home(langs, lang, t):
    root = "" if lang["code"] == "en" else "../"
    ctx = base_ctx(langs, lang, t, "", root, 8)
    ctx["ld"] = home_ld(langs, lang["code"], t, ctx["url"])
    n = t["home"]["new"]
    ctx["shots"] = {
        "home_dashboard": shot("home-dashboard", n["shot_dash_alt"], n["shot_dash_caption"], root, "        "),
        "home_kube": shot("home-kube", n["shot_kube_alt"], n["shot_kube_caption"], root, "            "),
        "home_explain": shot("home-explain", n["shot_explain_alt"], n["shot_explain_caption"], root, "            "),
    }
    fleet = t["home"]["features"]["fleet"]
    ctx["hostlist_attrs"] = "" if lang["code"] == "en" else (
        f' data-running="{html.escape(fleet["running"], quote=True)}"'
        f' data-unhealthy="{html.escape(fleet["unhealthy"], quote=True)}"')
    return render(template("home.html"), ctx)


# ------------------------------------------------------------------ guide, kubernetes, compare
def blocks_for(key, p, t):
    copy_label = t["chrome"]["copy"]
    rows = list(p["table"])
    if key == "compare":
        rows[8:8] = [p["table_kube"]]
        rows.append(p["table_storage"])
    b = {"table": table(p["table_head"], rows)}
    if "code_mcp" in p:
        b["code_mcp"] = code_block(p["code_mcp"], MCP_CMD, copy_label)
    if key == "guide":
        b["callout"] = callout_warn(p["callout"], t["chrome"]["callout_warn"])
    if key == "k8s":
        for n, cmd in (("code_create", "container cluster create --name dev --cpus 2 --memory 4G \\\n"
                                       "  --workers count=2,cpus=2,memory=4G --shared-image-store"),
                       ("code_kubectl", "kubectl --context dev get nodes"),
                       ("code_shared", "container build -t myapp:dev .\n"
                                       "kubectl --context dev create deployment myapp --image=myapp:dev"),
                       ("code_load", "container cluster load-image --name dev myapp:dev")):
            b[n] = code_block(p["code_shell"], cmd, copy_label)
        b["shot_cluster"] = shot("cluster-overview", p["shot_alt"], p["shot_caption"], "{root}")  # render() fills {root}
        term = p["terminal"]
        gantry = next(sec for sec in term["sections"] if sec["id"] == "gantry")
        b["shot_browser"] = "\n".join(shot(x["shot"], x["alt"], x["caption"], "{root}")
                                      for x in gantry["blocks"] if "shot" in x)
        walk = [sec for sec in term["sections"] if sec["id"] != "gantry"]
        b["terminal"] = "\n".join([f'<h2 id="terminal">{term["h1"]}</h2>', f'<p>{term["lead"]}</p>',
                                   sections_html("k8s", walk, term.get("tables", {}), t, "{root}", "h3", "terminal-")])
    return b


def about_for(key):
    if key in GUIDES:
        return APPLE_ABOUT + [{"@type": "SoftwareApplication", "name": "Gantry", "url": f"{SITE}/"}]
    if key == "guide":
        return APPLE_ABOUT
    if key == "k8s":
        return APPLE_ABOUT + [{"@type": "SoftwareApplication", "name": "Kubernetes", "url": "https://kubernetes.io/"}]
    return [{"@type": "SoftwareApplication", "name": n}
            for n in ("Gantry", "Docker Desktop", "OrbStack", "Podman Desktop", "container (apple/container)")]


def sections_html(code_key, sections, tables, t, root, tag="h2", id_prefix=""):
    chrome = t["chrome"]
    out = []
    for sec in sections:
        out += ["", f'<{tag} id="{id_prefix}{sec["id"]}">{sec["h"]}</{tag}>']
        for b in sec["blocks"]:
            if "p" in b:
                out.append(f'<p>{b["p"]}</p>')
            elif "ul" in b or "ol" in b:
                tag = "ul" if "ul" in b else "ol"
                out.append(f"<{tag}>\n" + "\n".join(f"  <li>{li}</li>" for li in b[tag]) + f"\n</{tag}>")
            elif "code" in b:
                if b.get("after"):
                    out.append(f'<p>{b["after"]}</p>')
                out.append(code_block(chrome["terminal"], GUIDE_CODE[code_key][b["code"]], chrome["copy"]))
            elif "table" in b:
                tb = tables[b["table"]]
                out.append(table(tb["head"], tb["rows"]))
            elif "note" in b:
                out.append(callout_note(b["note"], chrome["note"]))
            elif "warn" in b:
                out.append(callout_warn(b["warn"], chrome["callout_warn"]))
            elif "shot" in b:
                out.append(shot(b["shot"], b["alt"], b["caption"], root))
            else:
                raise ValueError(f"{code_key}: unknown block {sorted(b)}")
    return "\n".join(out)


def howto_ld(url, name, sections, anchor_prefix=""):
    """HowTo steps: one per section, with the text of its first paragraph or list."""
    steps = []
    for sec in sections:
        first = next((b for b in sec["blocks"] if "p" in b or "ul" in b or "ol" in b), None)
        if first is None:
            continue
        text = first.get("p") or " ".join(first.get("ul") or first.get("ol"))
        steps.append({"@type": "HowToStep", "position": len(steps) + 1, "name": plain(sec["h"]),
                      "text": " ".join(plain(text).split()), "url": f"{url}#{anchor_prefix}{sec['id']}"})
    return {"@type": "HowTo", "@id": f"{url}#howto", "name": plain(name), "step": steps}


def guide_body(slug, p, t, root):
    chrome = t["chrome"]
    out = [f'<h1>{p["h1"]}</h1>', f'<p class="page-lead">{p["lead"]}</p>', "",
           f'<div class="tldr">\n<p>{p["tldr"]}</p>\n</div>',
           sections_html(slug, p["sections"], p.get("tables", {}), t, root)]
    links = [f'  <li><a href="../{g}/">{t["guides"][g]["title"]}</a></li>' for g in GUIDES if g != slug]
    links += [f'  <li><a href="../apple-container/">{t["guide"]["title"]}</a></li>',
              f'  <li><a href="../apple-container-kubernetes/">{t["k8s"]["title"]}</a></li>',
              f'  <li><a href="../compare/">{t["compare"]["title"]}</a></li>']
    out += ["", f'<h2 id="related">{chrome["related"]}</h2>', "<ul>", *links, "</ul>"]
    return "\n".join(out)


def render_page(langs, lang, t, slug, key):
    p = t["guides"][slug] if key == "guides" else t[key]
    root = "../" if lang["code"] == "en" else "../../"
    ctx = base_ctx(langs, lang, t, slug, root, 6)
    url = ctx["url"]
    home = SITE + page_path(lang["code"], "")
    faq = [(f["q"], f["a"]) for f in p["faq"]]
    if key == "k8s":
        # The terminal walk-through brings its own questions; skip the two that the page FAQ already answers.
        faq += [(f["q"], f["a"]) for i, f in enumerate(p["terminal"]["faq"]) if i in (0, 1, 3)]
    graph = [
        {
            "@type": "TechArticle",
            "@id": f"{url}#article",
            "headline": p["title"],
            "description": p["desc"],
            "url": url,
            "inLanguage": lang["code"],
            "dateModified": UPDATED,
            "image": f"{SITE}/assets/dashboard.png",
            "author": {"@type": "Organization", "name": "Gantry", "url": f"{SITE}/"},
            "publisher": {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Gantry",
                          "logo": f"{SITE}/assets/icon.png"},
            "about": about_for(slug if key == "guides" else key),
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumbs",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Gantry", "item": home},
                {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url},
            ],
        },
        faq_ld(url, faq),
    ]
    if key == "guides":
        graph.append(howto_ld(url, p["h1"], p["sections"]))
    elif key == "k8s":
        walk = [sec for sec in p["terminal"]["sections"] if sec["id"] != "gantry"]
        graph.append(howto_ld(url, p["terminal"]["h1"], walk, "terminal-"))
    rows = "\n".join(
        f'<details class="faq-item"><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q, a in faq)
    ctx.update({
        "p": p,
        "blocks": {} if key == "guides" else blocks_for(key, p, t),
        "ld": ld_dump(graph, ""),
        "active": {k: (' class="active"' if k == key else "") for k in ("guide", "k8s", "compare")},
        "faq": f'\n<h2 id="faq">{t["chrome"]["faq_heading"]}</h2>\n<div class="faq-list">\n{rows}\n</div>\n',
        "updated_line": t["chrome"]["updated"].replace("{date}", UPDATED),
    })
    if key == "guides":
        ctx["body"] = guide_body(slug, p, t, root)
    else:
        ctx["body"] = render(template(f"{slug}.html"), ctx).strip()
    return render(template("page.html"), ctx)


# ------------------------------------------------------------------ site files
def sitemap(langs):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    entries = [(slug, freq, prio) for slug, (_, freq, prio) in PAGES.items()]
    entries += [(slug, freq, prio) for slug, (freq, prio) in GUIDES.items()]
    for slug, freq, prio in entries:
        alts = [f'    <xhtml:link rel="alternate" hreflang="{o["code"]}" href="{SITE}{page_path(o["code"], slug)}"/>'
                for o in langs]
        alts.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{page_path("en", slug)}"/>')
        for o in langs:
            lines += ["  <url>", f"    <loc>{SITE}{page_path(o['code'], slug)}</loc>", f"    <lastmod>{UPDATED}</lastmod>",
                      f"    <changefreq>{freq}</changefreq>", f"    <priority>{prio}</priority>", *alts, "  </url>"]
    for name, freq, prio in DOCS:
        lines += ["  <url>", f"    <loc>{SITE}/docs/{name}.html</loc>", f"    <lastmod>{UPDATED}</lastmod>",
                  f"    <changefreq>{freq}</changefreq>", f"    <priority>{prio}</priority>", "  </url>"]
    lines.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write("\n".join(lines) + "\n")


def languages_section(langs):
    out = ["## Languages", "",
           "The home page, the apple/container guide, the Kubernetes page (with the Kubernetes on a Mac walk-through), "
           "the comparison and the how-to guides (moving from Docker Desktop, external drives, docker run) are also "
           "available "
           "in these languages. Each language uses the same paths under its prefix, for example "
           f"{SITE}/de/apple-container/. The documentation is in English only.", ""]
    out += [f"- {o['name']} ({o['code']}): {SITE}{page_path(o['code'], '')}" for o in langs if o["code"] != "en"]
    return out


def llms_txt(langs):
    path = os.path.join(ROOT, "llms.txt")
    with open(path) as f:
        text = f.read()
    block = "\n".join(languages_section(langs)) + "\n\n"
    text = re.sub(r"## Languages\n.*?\n\n(?=## )", "", text, flags=re.S)
    text = text.replace("## Source\n", block + "## Source\n", 1)
    with open(path, "w") as f:
        f.write(text)


def llms_full(langs, en):
    with open(os.path.join(ROOT, "llms.txt")) as f:
        intro = f.read().split("\n## ")[0].rstrip()
    out = [intro, "", f"Last updated: {UPDATED}", ""]
    out += ["## container CLI command to Gantry feature", ""]
    out += [f"- {plain(c)}: {plain(g)} (CLI version: {plain(v)})" for c, g, v in en["guide"]["table"]]
    out += ["", "## Kubernetes cluster create options", ""]
    out += [f"- {plain(o)} ({plain(fl)}): {plain(n)}" for o, fl, n in en["k8s"]["table"]]
    out += ["", f"## Comparison (facts as of {UPDATED}; Unknown means not found in vendor docs)", ""]
    names = ["Gantry", "Docker Desktop", "OrbStack", "Podman Desktop", "container CLI"]
    crow = list(en["compare"]["table"])
    crow[8:8] = [en["compare"]["table_kube"]]
    crow.append(en["compare"]["table_storage"])
    for row in crow:
        out.append(f"- {plain(row[0])}: " + "; ".join(f"{n}: {plain(c)}" for n, c in zip(names, row[1:])))
    walks = [("k8s", f"{SITE}/apple-container-kubernetes/#terminal", en["k8s"]["terminal"])]
    walks += [(slug, f"{SITE}/{slug}/", en["guides"][slug]) for slug in GUIDES]
    for slug, url, g in walks:
        out += ["", f"## Guide: {plain(g['h1'])}", "", f"URL: {url}", "", " ".join(plain(g["tldr"]).split())]
        for sec in g["sections"]:
            out += ["", f"### {plain(sec['h'])}", ""]
            for b in sec["blocks"]:
                if "p" in b or "note" in b or "warn" in b:
                    out.append(" ".join(plain(b.get("p") or b.get("note") or b.get("warn")).split()))
                elif "ul" in b or "ol" in b:
                    out += [f"- {' '.join(plain(li).split())}" for li in b.get("ul") or b.get("ol")]
                elif "code" in b:
                    if b.get("after"):
                        out.append(plain(b["after"]))
                    out += ["```sh", GUIDE_CODE[slug][b["code"]], "```"]
                elif "table" in b:
                    tb = g["tables"][b["table"]]
                    out += [f"- {plain(r[0])} -> " + "; ".join(plain(c) for c in r[1:] if c) for r in tb["rows"]]
    out += ["", "## Questions and answers", ""]
    seen = set()
    faqs = en["home"]["faq"]["items"] + en["guide"]["faq"] + en["k8s"]["faq"] + en["compare"]["faq"]
    faqs += en["k8s"]["terminal"]["faq"] + [f for slug in GUIDES for f in en["guides"][slug]["faq"]]
    for item in faqs:
        q = plain(item["q"])
        if q in seen:
            continue
        seen.add(q)
        out += [f"Q: {q}", f"A: {' '.join(plain(item['a']).split())}", ""]
    out += ["## Pages", ""]
    out += [f"- {SITE}/{slug}/ : {en[key]['title']}" for slug, (key, _, _) in PAGES.items() if slug]
    out += [f"- {SITE}/{slug}/ : {en['guides'][slug]['title']}" for slug in GUIDES]
    out += [f"- {SITE}/ : Home", f"- {SITE}/docs/index.html : Documentation", f"- {GITHUB} : Source code", ""]
    out += languages_section(langs) + [""]
    with open(os.path.join(ROOT, "llms-full.txt"), "w") as f:
        f.write("\n".join(out))


def lang_js(langs, strings):
    data = {o["code"]: {k: strings[o["code"]]["chrome"][k] for k in ("hint_text", "hint_link", "hint_close")}
            for o in langs}
    with open(os.path.join(ROOT, "templates", "lang.js")) as f:
        js = f.read()
    with open(os.path.join(ROOT, "lang.js"), "w") as f:
        f.write(js.replace("/*HINTS*/{}", json.dumps(data, ensure_ascii=False, separators=(",", ":"))))


def main():
    langs = load_languages()
    if "--partial" in sys.argv:
        have = {o["code"] for o in langs if os.path.exists(os.path.join(ROOT, "i18n", f"{o['code']}.json"))}
        langs = [o for o in langs if o["code"] in have or o.get("transliterate_from") in have]
    if "--only" in sys.argv:
        only = {"en", *sys.argv[sys.argv.index("--only") + 1].split(",")}
        langs = [o for o in langs if o["code"] in only]
    strings = {o["code"]: load_strings(o) for o in langs}
    en = strings["en"]
    errors = [f"{code}{e}" for code, t in strings.items() for e in check(en, t)]
    if errors:
        print("\n".join(errors))
        sys.exit(f"{len(errors)} problems in i18n/*.json")
    if "--check" in sys.argv:
        print(f"{len(langs)} languages ok")
        return
    count = 0
    for lang in langs:
        t = resolve(copy.deepcopy(strings[lang["code"]]))
        pages = [(slug, key) for slug, (key, _, _) in PAGES.items()] + [(slug, "guides") for slug in GUIDES]
        for slug, key in pages:
            out = render_home(langs, lang, t) if key == "home" else render_page(langs, lang, t, slug, key)
            path = os.path.join(ROOT, page_path(lang["code"], slug).strip("/"), "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(out)
            count += 1
    sitemap(langs)
    llms_txt(langs)
    llms_full(langs, resolve(en))
    lang_js(langs, strings)
    print(f"Wrote {count} pages in {len(langs)} languages")


if __name__ == "__main__":
    main()
