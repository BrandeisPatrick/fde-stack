# /fde stack

A Claude Code skill for running a client project as a forward-deployed engineer. Click a command to see an example reply (Contoso is a placeholder company).

<details>
<summary><code>/fde</code> · catch up on a project in one message</summary>

![Claude Code reply to /fde: a one-line priority, then status, what changed, progress bars and the user's actions.](docs/assets/screens/fde.svg)

</details>

<details>
<summary><code>/fde initialize</code> · set up, then check everything is ready</summary>

![Claude Code reply to /fde initialize: a ten-row checklist and the login command to run.](docs/assets/screens/fde-initialize.svg)

</details>

<details>
<summary><code>/fde architecture</code> · see what runs where, and what is out of date</summary>

![Claude Code reply to /fde architecture: local copies, GitHub and the live deployment, each with its version.](docs/assets/screens/fde-architecture.svg)

</details>

<details>
<summary><code>/fde progress</code> · one bar per workstream</summary>

![Claude Code reply to /fde progress: four workstreams with ten-cell bars.](docs/assets/screens/fde-progress.svg)

</details>

<details>
<summary><code>/fde timeline</code> · what happened, day by day</summary>

![Claude Code reply to /fde timeline: four dated rows with linked sources.](docs/assets/screens/fde-timeline.svg)

</details>

<details>
<summary><code>/fde context</code> · the project's facts</summary>

![Claude Code reply to /fde context: a six-row facts card.](docs/assets/screens/fde-context.svg)

</details>

<details>
<summary><code>/fde project</code> · every project in your vault</summary>

![Claude Code reply to /fde project: three projects with stage and last entry.](docs/assets/screens/fde-project.svg)

</details>

<details>
<summary><code>/fde visual</code> · redraw a reply as a diagram</summary>

![Claude Code reply to /fde visual: two flows, today ending in Blocked and proposed ending in Delivered.](docs/assets/screens/fde-visual.svg)

</details>

<details>
<summary><code>/fde recap</code> · cut a reply to a few lines</summary>

![Claude Code reply to /fde recap: a verdict, a short table, a diagram and a proposal.](docs/assets/screens/fde-recap.svg)

</details>

<details>
<summary>In a session · build with a team of agents</summary>

- Opus plans and reviews; Sonnet agents build, each in its own worktree.
- Every change ships as a PR with a diagram.
- A private story page shows progress as it happens.

</details>

## Install

```bash
git clone https://github.com/BrandeisPatrick/fde-stack ~/code/fde-stack
```

```bash
mkdir -p ~/.claude/skills && ln -s ~/code/fde-stack/skills/fde ~/.claude/skills/fde
```

Then run `/fde initialize` in Claude Code. It finds your private [vault](skills/fde/references/vault-layout.md) (or offers to create one), writes your settings, and checks that everything is ready.

v1 · [How it works](skills/fde/SKILL.md)
