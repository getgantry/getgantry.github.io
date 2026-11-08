#!/usr/bin/env python3
"""List the strings a translation needs after en.json changed, and merge the translations back.

`todo LANG [--base REV]` writes build/i18n/LANG.todo.json ({path: English}) against en.json at REV (default HEAD).
`apply LANG FILE` merges FILE into i18n/LANG.json in the key order of en.json and runs the build_pages.py check.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "i18n")
MISSING = object()
FIXED = {"id", "code", "table", "shot", "when", "unless"}


def at_rev(rev, rel):
    return json.loads(subprocess.check_output(["git", "-C", ROOT, "show", f"{rev}:{rel}"]))


def ident(item):
    """The question, heading or first cell that names a list item."""
    if isinstance(item, dict):
        return item.get("q") or item.get("h")
    if isinstance(item, list) and item and isinstance(item[0], str):
        return item[0]
    return None


def align(old_en, old_t, new_en, path, todo):
    """Return new_en's shape filled with the old translations; record the leaves to translate in todo."""
    if isinstance(new_en, dict):
        return {k: align(old_en.get(k, MISSING) if isinstance(old_en, dict) else MISSING,
                         old_t.get(k, MISSING) if isinstance(old_t, dict) else MISSING,
                         v, f"{path}.{k}" if path else k, todo)
                for k, v in new_en.items()}
    if isinstance(new_en, list):
        old_en_l = old_en if isinstance(old_en, list) else []
        old_t_l = old_t if isinstance(old_t, list) and len(old_t) == len(old_en_l) else []
        out, used = [], set()
        for i, v in enumerate(new_en):
            # Match by content first, so an inserted item does not shift the old translations.
            j = next((j for j, o in enumerate(old_en_l) if j not in used and o == v and old_t_l), None)
            if j is None and old_t_l:
                j = next((j for j, o in enumerate(old_en_l) if j not in used and ident(o) and ident(o) == ident(v)),
                         None)
            if j is None and len(old_en_l) == len(new_en) and old_t_l:
                j = i
            if j is None:
                out.append(align(MISSING, MISSING, v, f"{path}[{i}]", todo))
            else:
                used.add(j)
                out.append(align(old_en_l[j], old_t_l[j], v, f"{path}[{i}]", todo))
        return out
    if old_en is not MISSING and old_en == new_en and isinstance(old_t, str):
        return old_t
    if path.rsplit(".", 1)[-1] in FIXED:
        return new_en
    todo[path] = new_en
    return new_en


def set_path(tree, path, value):
    parts = re.findall(r"[^.\[\]]+|\[\d+\]", path)
    node = tree
    for p in parts[:-1]:
        node = node[int(p[1:-1])] if p.startswith("[") else node[p]
    last = parts[-1]
    if last.startswith("["):
        node[int(last[1:-1])] = value
    else:
        node[last] = value


def main():
    cmd, lang = sys.argv[1], sys.argv[2]
    rev = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "HEAD"
    new_en = json.load(open(os.path.join(ROOT, "i18n", "en.json")))
    todo = {}
    base = align(at_rev(rev, "i18n/en.json"), at_rev(rev, f"i18n/{lang}.json"), new_en, "", todo)
    if cmd == "todo":
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, f"{lang}.todo.json"), "w") as f:
            json.dump(todo, f, ensure_ascii=False, indent=1)
        print(f"{lang}: {len(todo)} strings, {sum(len(v) for v in todo.values())} characters")
    elif cmd == "apply":
        done = json.load(open(sys.argv[3]))
        missing, extra = sorted(set(todo) - set(done)), sorted(set(done) - set(todo))
        if missing or extra:
            sys.exit(f"{lang}: missing {missing[:5]} ({len(missing)}), unknown {extra[:5]} ({len(extra)})")
        for p, v in done.items():
            set_path(base, p, v)
        sys.path.insert(0, ROOT)
        from build_pages import check
        errors = check(new_en, base)
        if errors:
            sys.exit(f"{lang}:\n" + "\n".join(errors[:30]))
        with open(os.path.join(ROOT, "i18n", f"{lang}.json"), "w") as f:
            json.dump(base, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"{lang}: merged {len(done)} strings")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
