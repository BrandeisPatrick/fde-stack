# Working on fde-stack

One skill, `skills/fde/`, shipped as a Claude Code plugin. The repo root is the plugin root.

## Rules

- **Made-up data only.** Examples, images and the sample vault use fictional companies (Contoso, Fabrikam, Northwind) and `example.com`. Never a real client, person or URL.
- **The images are generated.** Edit `EXAMPLES` in `docs/tools/render_replies.py`, then run it. Never edit an SVG by hand.
- **The sample vault and the images must agree.** A number changed in one is changed in the other.
- **The description says when to use the skill**, not how it works, and stays under 1,024 characters.
- **The plugin name `fde` never changes.** Installed copies are keyed on it.
- Keep `SKILL.md` under 700 lines. Move detail into `skills/fde/references/`.

## Before a commit

```bash
python3 -I docs/tools/render_replies.py && git diff --exit-code -- docs/assets
```

```bash
python3 -I docs/tools/check_repo.py
```

```bash
claude plugin validate .
```

Add a line to `CHANGELOG.md` under *Unreleased* for anything a user would notice.
