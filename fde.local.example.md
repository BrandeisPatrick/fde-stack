# fde: my settings

`/fde initialize` writes this file for you at `~/.claude/fde.local.md`; this is what it looks like. Edit it by hand only to change a value. The `fde` skill reads it at the start of every run; until it exists, the vault views show the sample vault bundled with the skill. It holds no secrets: never put a token, key or password here.

## Vault
- Repo: <owner>/<your-name>-vault, private, in an account or org approved for client data. An internal or public repo fails the vault's safe-place check. If you don't have one yet, `/fde` offers to create it.
- Clone: ~/code/<your-name>-vault. Keep it out of iCloud, Dropbox or other cloud-synced folders; on a Mac that syncs Desktop and Documents, that includes ~/Documents.
- Pushes: straight to main (it is a private notebook, not a project repo)

## Workspace
- Folder: ~/code. Project clones go in `<workspace>/<project>/`, agent worktrees in `<workspace>/<project>/wt/<agent>`. The same cloud-sync caution as the vault applies.

## GitHub
- Default account: <your work login>
- Second account: none (or: <login>, only for <what>)

## Transcripts
- Tool: pasted in (or: the name of your transcript tool)

## Teams and email
- Usual method: screenshots (or: browser, desktop app, skip)
