# fde: my settings

`/fde initialize` writes this file for you at `~/.claude/fde.local.md`; this is what it looks like. Edit it by hand only to change a value. The `fde` skill reads it at the start of every run; until it exists, the vault views show the sample vault bundled with the skill. It holds no secrets: never put a token, key or password here.

Each line is a bare value. The notes at the end explain them and are not part of the file.

```markdown
# fde: my settings

## Vault
- Repo: <account>/<account>-vault
- Clone: ~/code/<account>-vault
- Pushes: straight to main

## Workspace
- Folder: ~/code

## GitHub
- Default account: <login>
- Second account: none

## Transcripts
- Tool: pasted in

## Teams and email
- Usual method: screenshots
```

## Notes

- **Repo:** private, in an account or org approved for client data. An internal or public repo fails the vault's safe-place check. For a local vault, write `Repo: none (local folder)` and `Pushes: none (local folder)`.
- **Clone:** keep it out of iCloud, Dropbox and other cloud-synced folders. On a Mac that syncs Desktop and Documents, that includes `~/Documents`.
- **Pushes:** the vault is a private notebook, not a project repo, so it is pushed straight to `main`.
- **Workspace:** project clones go in `<workspace>/<project>/`, agent worktrees in `<workspace>/<project>/wt/<agent>`. The same cloud-sync caution applies.
- **Second account:** `<login>, only for <what>` when there is one.
- **Transcripts:** `pasted in`, or the name of your transcript tool.
- **Teams and email:** `screenshots`, `browser`, `desktop app` or `skip`.
