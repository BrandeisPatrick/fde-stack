# PR template

Every change to a project repo lands through a PR, and every PR has at least one diagram. The template below comes from a PR that a reviewer who was not in the build could approve on its own: it shows how the pieces are wired, how a request flows, what was and was not checked, and what must be decided before merge.

## Body

Use the sections that apply, in this order. A small fix may need only the summary, one diagram, the checks and the commits.

````markdown
<One paragraph: what this adds or replaces, and why. Link the design doc if there is one.>

> [!IMPORTANT]
> **Not ready to merge until <condition>.** <One line on why.> See *Decide before merge*.

## How <the pieces> are wired

![<A full sentence saying what the diagram shows>](https://github.com/<org>/<repo>/blob/<sha>/docs/design/img/<name>.svg?raw=true)

- **<Point>.** What changed in this picture, and why it matters.

## How <a request / a card / a turn> flows

![<alt text>](https://github.com/<org>/<repo>/blob/<sha>/docs/design/img/<flow>.svg?raw=true)

<One paragraph walking the path.>

## What it looks like

All synthetic data.

| <Screen A> | <Screen B> |
|---|---|
| ![<alt>](<pinned screenshot URL>) | ![<alt>](<pinned screenshot URL>) |
| <What to notice, and where the figures come from> | <…> |

## What was verified, and what was not

| Checked | How |
|---|---|
| Unit tests | <n> passed, <n> skipped |
| Live turns | <what ran, against what> |

| **Not** checked | Why |
|---|---|
| <thing> | <reason> |

## Decide before merge

1. **<Decision>.** The facts, the options, and whose call it is.

## Known rough edges

- **<Edge>.** One or two sentences.

## Run it locally

```bash
<commands>
```

## Commits

- `<sha>` **<area>:** <what>
- `<sha>` **docs:** the diagrams and screenshots above

## Provenance

<Only when code came from another repo: the source repo, commit, and what was left out.>
````

The *Not checked* table and *Decide before merge* are what make a PR reviewable by someone who was not there. Never drop them to make the PR look finished.

## Diagrams

- **At least one per PR.** For an architecture change, show how the pieces are wired. For a behaviour change, show the path the change touches. Add screenshots for anything a user sees.
- **Monochrome SVG**, one ink colour with tints of it, and never ASCII art. Keep one idea per diagram, and write the SVG with the Write tool. For a diagram headed for a client artifact, a diagram tool such as Lucid is fine; commit its export.
- **Commit diagrams in the PR itself**, under `docs/design/img/`, usually as a final `docs:` commit.
- **Embed them by a commit-pinned URL**: `https://github.com/<org>/<repo>/blob/<sha>/<path>?raw=true`. A relative path does not render in a PR body, and a branch URL breaks once the branch is deleted. The pinned form renders for anyone who can read the private repo.
- **Alt text is a full sentence** that says what the diagram shows, so the PR still reads when the image does not load.

## Mechanics

- **Body in a file:** write the body to a scratch file with the Write tool, then run `gh pr create --draft --body-file <file>` or `gh pr edit <n> --body-file <file>`. This keeps long payloads off the command line (see *Command-line hygiene* in SKILL.md).
- **Draft early:** open the PR as a draft as soon as the integration branch exists, and update its body as waves land.
- **Keep it current:** refresh the pinned URLs when a diagram changes, because they point at a specific commit.
- **Marking ready:** `gh pr ready <n>` only after the reviewer agent has passed it and the *Not checked* table is honest.
- **Bind it:** in the Claude desktop app, bind the PR to the session (the `ccd_pr` tools) so CI and review comments come back to it.
- **Merging:** this is the merge owner's call, as recorded in `project.md`. Never merge, or enable auto-merge, without the user saying so.
