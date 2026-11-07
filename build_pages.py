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
UPDATED = "2026-11-03"
APP_VERSION = "0.25.0"
APP_UI_LANGUAGES = ["en", "zh-Hans"]
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
        if not t.strip() and en.strip():
            errors.append(f"{path}: empty")
        for name, a, b in zip(("tags", "code", "placeholders"), signature(en), signature(t)):
            if a != b:
                errors.append(f"{path}: {name} differ: {sorted(set(a) ^ set(b))[:4]}")
    return errors


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
        "updated": UPDATED,
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
    fleet = t["home"]["features"]["fleet"]
    ctx["hostlist_attrs"] = "" if lang["code"] == "en" else (
        f' data-running="{html.escape(fleet["running"], quote=True)}"'
        f' data-unhealthy="{html.escape(fleet["unhealthy"], quote=True)}"')
    return render(template("home.html"), ctx)


# ------------------------------------------------------------------ guide, kubernetes, compare
def blocks_for(key, p, t):
    copy_label = t["chrome"]["copy"]
    b = {"table": table(p["table_head"], p["table"])}
    if "code_mcp" in p:
        b["code_mcp"] = code_block(p["code_mcp"], MCP_CMD, copy_label)
    if key == "guide":
        b["callout"] = callout_warn(p["callout"], t["chrome"]["callout_warn"])
    if key == "k8s":
        for n, cmd in (("code_create", "container cluster create --name dev --workers 2 --cpus 2 --memory 4G"),
                       ("code_kubectl", "kubectl --context dev get nodes"),
                       ("code_load", "container cluster load-image --name dev myapp:dev")):
            b[n] = code_block(p["code_shell"], cmd, copy_label)
    return b


def about_for(key):
    if key == "guide":
        return APPLE_ABOUT
    if key == "k8s":
        return APPLE_ABOUT + [{"@type": "SoftwareApplication", "name": "Kubernetes", "url": "https://kubernetes.io/"}]
    return [{"@type": "SoftwareApplication", "name": n}
            for n in ("Gantry", "Docker Desktop", "OrbStack", "Podman Desktop", "container (apple/container)")]


def render_page(langs, lang, t, slug, key):
    p = t[key]
    root = "../" if lang["code"] == "en" else "../../"
    ctx = base_ctx(langs, lang, t, slug, root, 6)
    url = ctx["url"]
    home = SITE + page_path(lang["code"], "")
    faq = [(f["q"], f["a"]) for f in p["faq"]]
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
            "about": about_for(key),
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
    rows = "\n".join(
        f'<details class="faq-item"><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q, a in faq)
    ctx.update({
        "p": p,
        "blocks": blocks_for(key, p, t),
        "ld": ld_dump(graph, ""),
        "active": {k: (' class="active"' if k == key else "") for k in ("guide", "k8s", "compare")},
        "faq": f'\n<h2 id="faq">{t["chrome"]["faq_heading"]}</h2>\n<div class="faq-list">\n{rows}\n</div>\n',
        "updated_line": t["chrome"]["updated"].replace("{date}", UPDATED),
    })
    ctx["body"] = render(template(f"{slug}.html"), ctx).strip()
    return render(template("page.html"), ctx)


# ------------------------------------------------------------------ site files
def sitemap(langs):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for slug, (_, freq, prio) in PAGES.items():
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
           "The home page, the apple/container guide, the Kubernetes page and the comparison are also available "
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
    for row in en["compare"]["table"]:
        out.append(f"- {plain(row[0])}: " + "; ".join(f"{n}: {plain(c)}" for n, c in zip(names, row[1:])))
    out += ["", "## Questions and answers", ""]
    seen = set()
    faqs = en["home"]["faq"]["items"] + en["guide"]["faq"] + en["k8s"]["faq"] + en["compare"]["faq"]
    for item in faqs:
        q = plain(item["q"])
        if q in seen:
            continue
        seen.add(q)
        out += [f"Q: {q}", f"A: {' '.join(plain(item['a']).split())}", ""]
    out += ["## Pages", ""]
    out += [f"- {SITE}/{slug}/ : {en[key]['title']}" for slug, (key, _, _) in PAGES.items() if slug]
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
        t = copy.deepcopy(strings[lang["code"]])
        for slug, (key, _, _) in PAGES.items():
            out = render_home(langs, lang, t) if key == "home" else render_page(langs, lang, t, slug, key)
            path = os.path.join(ROOT, page_path(lang["code"], slug).strip("/"), "index.html")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(out)
            count += 1
    sitemap(langs)
    llms_txt(langs)
    llms_full(langs, en)
    lang_js(langs, strings)
    print(f"Wrote {count} pages in {len(langs)} languages")


if __name__ == "__main__":
    main()
