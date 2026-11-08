#!/usr/bin/env python3
"""Check the built site: local links and anchors, hreflang, sitemap, unique titles and descriptions, JSON-LD.

Run from the repo root after the generators. `--external` also requests every external link once.
Exit code 1 when a problem is found. TODO-SCREENSHOT markers are listed but are not problems.
"""
import collections
import html.parser
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://getgantry.github.io"
SKIP_DIRS = {"templates", "build", "scripts", ".git", "node_modules"}


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.alternates, self.ld = [], set(), {}, []
        self.title, self.desc, self.lang = "", "", ""
        self._in_title = self._in_ld = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "a" and "name" in a:
            self.ids.add(a["name"])
        for key in ("href", "src"):
            if key in a and not (tag == "link" and a.get("rel") == "alternate"):
                self.links.append(a[key])
        if tag == "link" and a.get("rel") == "alternate" and "hreflang" in a:
            self.alternates[a["hreflang"]] = a["href"]
        if tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        self._in_title = tag == "title"
        self._in_ld = tag == "script" and a.get("type") == "application/ld+json"

    def handle_endtag(self, tag):
        self._in_title = self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self.ld.append(data)


def html_files():
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                yield os.path.relpath(os.path.join(dirpath, f), ROOT)


def target(rel_file, link):
    """Map a link to (local file, fragment), or None when it is not on this site."""
    if link.startswith(SITE):
        link = link[len(SITE):]
        base = "/"
    elif re.match(r"^[a-z]+:", link) or link.startswith("//"):
        return None
    else:
        base = "/" + os.path.dirname(rel_file) + "/"
    parts = urllib.parse.urlsplit(link)
    path = urllib.parse.unquote(parts.path)
    full = os.path.normpath(os.path.join(base, path)) if path else "/" + rel_file
    if path.endswith("/") or (not path and rel_file.endswith("index.html") and not parts.fragment):
        full = full.rstrip("/") + "/index.html"
    elif not os.path.splitext(full)[1] and path:
        full = full + "/index.html"
    return full.lstrip("/"), parts.fragment


def main():
    pages = {}
    for rel in html_files():
        p = Page()
        with open(os.path.join(ROOT, rel)) as f:
            text = f.read()
        p.feed(text)
        p.todo = re.findall(r"<!-- TODO-SCREENSHOT (.*?) -->", text)
        pages[rel] = p
    problems, external = [], collections.defaultdict(set)
    for rel, p in pages.items():
        for link in p.links:
            if link.startswith(("mailto:", "javascript:", "data:")):
                continue
            t = target(rel, link)
            if t is None:
                if link.startswith("http"):
                    external[link.split("#")[0]].add(rel)
                continue
            path, frag = t
            if not os.path.exists(os.path.join(ROOT, path)):
                problems.append(f"{rel}: broken link {link} -> {path}")
            elif frag and path in pages and frag not in pages[path].ids:
                problems.append(f"{rel}: missing anchor {link}")
        for lang, href in p.alternates.items():
            t = target(rel, href)
            if t is None or not os.path.exists(os.path.join(ROOT, t[0])):
                problems.append(f"{rel}: hreflang {lang} -> {href} does not exist")
        for block in p.ld:
            try:
                json.loads(block)
            except ValueError as e:
                problems.append(f"{rel}: JSON-LD does not parse: {e}")
        if not rel.startswith("docs/") and p.ld and '"FAQPage"' not in "".join(p.ld):
            problems.append(f"{rel}: no FAQPage JSON-LD")
    # Unique title and description in each language.
    by_lang = collections.defaultdict(list)
    for rel, p in pages.items():
        if not rel.startswith("docs/"):
            by_lang[p.lang].append((rel, p))
    for lang, items in by_lang.items():
        for field in ("title", "desc"):
            seen = collections.defaultdict(list)
            for rel, p in items:
                seen[getattr(p, field).strip()].append(rel)
            for value, rels in seen.items():
                if not value:
                    problems.extend(f"{r}: empty {field}" for r in rels)
                elif len(rels) > 1:
                    problems.append(f"{lang}: same {field} on {rels}: {value[:70]}")
    # Sitemap lists every page, and every listed page exists.
    sm = open(os.path.join(ROOT, "sitemap.xml")).read()
    locs = set(re.findall(r"<loc>(.*?)</loc>", sm))
    for loc in locs:
        t = target("index.html", loc)
        if not os.path.exists(os.path.join(ROOT, t[0])):
            problems.append(f"sitemap: {loc} does not exist")
    for rel in pages:
        url = SITE + "/" + (rel[:-len("index.html")] if rel.endswith("index.html") and not rel.startswith("docs/") else rel)
        if url not in locs:
            problems.append(f"sitemap: {url} is not listed")
    if "--external" in sys.argv:
        for url in sorted(external):
            try:
                req = urllib.request.Request(url, method="GET", headers={"User-Agent": "gantry-site-check"})
                with urllib.request.urlopen(req, timeout=20) as r:
                    status = r.status
            except urllib.error.HTTPError as e:
                status = e.code
            except Exception as e:  # noqa: BLE001 - report any network failure
                status = type(e).__name__
            if status != 200:
                print(f"external {status}: {url} (on {len(external[url])} pages, e.g. {sorted(external[url])[0]})")
    todos = sorted({t for p in pages.values() for t in p.todo})
    print(f"{len(pages)} pages, {sum(len(p.links) for p in pages.values())} links, {len(locs)} sitemap URLs, "
          f"{len(external)} external URLs")
    print(f"TODO-SCREENSHOT markers ({len(todos)} distinct):")
    for t in todos:
        print("  " + t)
    for prob in problems:
        print("PROBLEM " + prob)
    print(f"{len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
