# Vault layout for an FDE project

The vault is a private Git repo that holds your project context: one folder per piece of work, each with its own README. Its location is in your settings (`~/.claude/fde.local.md`). This file says what an FDE project folder needs on top of that.

```text
<vault>/
├── README.md               index table, one row per folder
├── platforms/              defaults shared by every project (starts as a one-line README.md)
│   ├── gcp.md
│   ├── aws.md
│   └── dependencies.md
└── <project>/
    ├── README.md           what it is, state, files, not written yet
    ├── project.md          the facts card
    ├── timeline.md         meetings and decisions, newest first
    ├── meetings/           condensed notes, one file per meeting
    ├── story/              story page source and run log (when there is one)
    └── source/             files exactly as received
```

## platforms/

These are the settings most projects share, kept in one place so each project records only how it differs. Write them the first time the user approves, from what they already know about their clouds.

- **`gcp.md`**: the orgs and sandbox projects, default region, how access works (IAP, Domain Restricted Sharing), which models are available where, and what agents cannot do (DNS, certificates, Secret Manager writes).
- **`aws.md`**: the SSO path, accounts and roles, regions, and org rules (for example, which services may be public).
- **`dependencies.md`**: the shared services a build may need, such as a model gateway, model providers and MCP servers. For each one, record its base URL, where its key lives and its known traps.

Never write a key, token or password into the vault. Record where it lives, such as a Secret Manager name, an env var or a password-manager item, and who can grant it.

## project.md

```markdown
# <Project>: facts

Updated YYYY-MM-DD.

## Workstreams
The progress bars in the status message read from this table and write back to it. Keep the same rows from session to session, and add a row only when new work starts.
| Workstream | Done when | Estimate | As of | Basis |
|---|---|---|---|---|

## Code
| Repo | Default branch | Local clone | Merge owner |
|---|---|---|---|

## Deployment
| Env | Cloud | Project or account | Region | Services | URL | Live revision |
|---|---|---|---|---|---|---|

## Platform overrides
Only where this project differs from ../platforms/<cloud>.md.

## Dependencies
| What | Where the key lives | Notes |
|---|---|---|

## Access
| Source | Method last used | Notes |
|---|---|---|
| Teams | browser / app / screenshots / skipped | |
| Email | browser / app / screenshots / skipped | |
| Transcripts | your transcript tool / pasted in | |

## People
| Name | Role | Side |
|---|---|---|

## Data rules
What the client's or your company's terms say about copies, retention and sharing. Write "None beyond the defaults" when there are none.

## Story
Pages URL, artifact URL, and the run-log path.
```

Keep it to facts that a session needs to start. Reasoning and history belong in the README or the timeline.

## timeline.md

The newest entry goes first. Each entry covers one meeting, or one message that changed a decision.

```markdown
# <Project> timeline

## 2026-03-09 · Internal kickoff
- **Decided:** …
- **Asked of us:** …
- **Open:** …
- Transcript: [Teams recording](<link>) · [notes](meetings/2026-03-09-internal-kickoff.md) · [full](meetings/2026-03-09-internal-kickoff.transcript.txt)

## 2026-03-06 · Teams, project core chat
- **Decided:** …
- Source: Teams, <chat name>, 2026-03-06
```

- A meeting with no transcript gets `Transcript: missing (asked YYYY-MM-DD)` until the user supplies one.
- Entries stay short. The decision and who made it matter; the discussion does not.
- When a newer entry reverses an older one, say so in the new entry ("reverses 3/6"), so a reader does not act on the old decision.

## meetings/

Each meeting gets two files:
- **`YYYY-MM-DD-<slug>.md`** holds the condensed notes: decisions, commitments, dates and open questions, plus a link to the source recording. Sessions read this file.
- **`YYYY-MM-DD-<slug>.transcript.txt`** is the full transcript, as your tool returned it or as the user supplied it. Open it only when the notes are not enough, and read only the part a task needs.

The full transcript is stored only when the vault passes the check below.

## Is the vault a safe place?

Full transcripts and client documents go into the vault only when it is a safe place. Run this check once per session, before storing anything.

**A remote vault** passes when all four of these hold.

```bash
gh repo view <org>/<vault> --json visibility,owner
```

- `visibility` is `PRIVATE`. `INTERNAL` fails, because every enterprise member can read it, and `PUBLIC` fails too.
- The owner is an account or org approved for client data.

```bash
gh api 'repos/<org>/<vault>/collaborators?affiliation=direct' --jq '.[].login'
```

- Only the user is listed. The plain collaborator list also shows the org owners as admins. That is expected, since owners are admins on every repo in the org.

```bash
gh api 'repos/<org>/<vault>/collaborators?affiliation=outside' --jq '.[].login'
```

- The list is empty.

Quote the URL, because zsh treats the `?` as a glob.

**A local vault** passes when it is a folder on this laptop that is not inside a personal cloud-sync folder, such as iCloud Drive, Dropbox or a personal Google Drive.

**When the vault fails**, keep the link and the condensed notes only, and tell the user why.

A data rule in `project.md` overrides this check. A client whose terms bar any copy gets none, wherever the vault is.

## story/

The story page source, `run-log.json` and the build script. Keep the run log here from the start, not in a session scratchpad: scratchpads get cleared, and a build script that points at one stops working.
