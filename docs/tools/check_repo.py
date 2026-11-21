#!/usr/bin/env python3
"""Check the repo for drift. Standard library only.

Run from anywhere: python3 -I docs/tools/check_repo.py
Fails (exit 1) unless:
- the SKILL.md frontmatter description is at most 1,024 characters;
- both .claude-plugin/*.json files parse, and the marketplace's plugin entry
  has the same name as plugin.json;
- every relative markdown link in the README, SKILL.md, the references and
  the sample vault points at a file that exists;
- the sample vault's Contoso workstream estimates match PROGRESS_ROWS in
  render_replies.py, which draws the README images.
"""
import ast
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SKILL = os.path.join(ROOT, "skills", "fde")
errors = []


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def rel(path):
    return os.path.relpath(path, ROOT)


def check_description():
    text = read(os.path.join(SKILL, "SKILL.md"))
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append("SKILL.md: no frontmatter")
        return
    desc = re.search(r"^description:\s*(.*)$", m.group(1), re.M)
    if not desc:
        errors.append("SKILL.md: no description in the frontmatter")
        return
    value = desc.group(1).strip().strip('"').strip("'")
    if len(value) > 1024:
        errors.append(f"SKILL.md: description is {len(value)} characters, over 1,024")


def check_plugin():
    try:
        plugin = json.loads(read(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
        market = json.loads(read(os.path.join(ROOT, ".claude-plugin", "marketplace.json")))
    except (OSError, ValueError) as e:
        errors.append(f".claude-plugin: {e}")
        return
    names = [p.get("name") for p in market.get("plugins", [])]
    if plugin.get("name") not in names:
        errors.append(f".claude-plugin: plugin.json name {plugin.get('name')!r} not in marketplace plugins {names}")


LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def check_links():
    files = [os.path.join(ROOT, "README.md"), os.path.join(SKILL, "SKILL.md")]
    files += glob.glob(os.path.join(SKILL, "references", "*.md"))
    files += glob.glob(os.path.join(SKILL, "sample-vault", "**", "*.md"), recursive=True)
    for path in sorted(files):
        in_fence = False
        for n, line in enumerate(read(path).splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            targets = LINK.findall(line) + re.findall(r'<img[^>]*\ssrc="([^"]+)"', line)
            for target in targets:
                if "<" in target or target.startswith("#") or re.match(r"[a-z]+:", target):
                    continue
                target = target.split("#", 1)[0]
                full = os.path.normpath(os.path.join(os.path.dirname(path), target))
                if not os.path.exists(full):
                    errors.append(f"{rel(path)}:{n}: broken link {target}")


def progress_rows():
    tree = ast.parse(read(os.path.join(ROOT, "docs", "tools", "render_replies.py")))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "PROGRESS_ROWS" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit("render_replies.py: PROGRESS_ROWS not found")


def check_progress():
    text = read(os.path.join(SKILL, "sample-vault", "contoso-retail", "project.md"))
    section = text.split("## Workstreams", 1)[1].split("\n## ", 1)[0]
    vault = {}
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[2].endswith("%"):
            vault[cells[0]] = (cells[2], cells[4])
    images = {r[0]: (r[2], r[3]) for r in progress_rows()}
    if vault != images:
        errors.append(f"contoso-retail/project.md workstreams {vault} differ from PROGRESS_ROWS {images}")
    for name, bar, pct, _ in progress_rows():
        filled = bar.strip("`").count("█")
        if filled * 10 != int(pct.rstrip("%")) or len(bar.strip("`")) != 10:
            errors.append(f"PROGRESS_ROWS: bar for {name} does not match {pct}")


def main():
    check_description()
    check_plugin()
    check_links()
    check_progress()
    for e in errors:
        print("✗", e)
    if errors:
        return 1
    print("✓ all checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
