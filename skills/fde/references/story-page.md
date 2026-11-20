# Story page

The story page is one static page that shows what is being built and how the agents are building it. The FDE watches it while agents run, and shares the link with coworkers or the client. The story agent keeps it current, and the orchestrator feeds it through the run log.

## How the page is built

No template ships with this skill yet (an open item), so build to this shape:

- **`index.html`** is the page. All of its data sits in one block, `<script type="application/json" id="build-data">`, and the page renders from that block.
- **`build_story.py`** (or any script) reads `run-log.json` and the git history of the agent branches, then rewrites that JSON block. Keep every path in it relative to the story folder, never a session scratchpad.
- **`run-log.json`** is the build log (format below).
- **`console_links.json`** holds the links in *Live services*.

Keep the look plain and consistent from one project to the next: monochrome, one accent colour, tables over prose.

## Sections

Use the ones the build has reached.

| Section | What it shows | When it is useful |
|---|---|---|
| What we built | The product, in a paragraph and a few headline numbers | From the first deploy |
| Live services | Links to the running app and the cloud console pages | Once something is deployed |
| What's covered | The feature list against what was built | Mid-build onward |
| How we built it | A Gantt chart of agents by phase and group, the sandboxes, and the human decisions | From the first wave |
| How we know it works | Tests, QA, the red team and review findings | After QA |
| Conclusions | What worked, what did not, and what is not done | At the end |
| Reference figures | Every number on the page, with where it came from | Always |

Early in a build, the page is mostly the plan and who is doing what. Weight it toward whatever the user would show next.

## run-log.json

The orchestrator writes it as the build goes. The story agent never invents entries.

```json
{
  "build": "<name>",
  "goal": "<one sentence>",
  "story_goal": "<what the page should convince a reader of>",
  "time_note": "<time zone; which clock each time comes from>",
  "orchestrator": {"role": "plans, briefs, reviews, tracks; writes no product code", "model": "claude-opus-…"},
  "phases": [{"id": "P1", "name": "Build wave 1", "started": "10:00", "ended": "10:30"}],
  "agents": [{
    "name": "infra", "group": "platform", "phase": "P1",
    "role": "<one line>", "type": "general-purpose", "model": "sonnet",
    "sandbox": "worktree <build>/infra + <cloud project>",
    "started": "10:02", "finished": "10:20",
    "blocked": [{"at": "10:05", "what": "<what blocked it>"}],
    "commits": 1, "tokens": 100000, "tool_uses": 40, "duration_s": 600
  }],
  "human_decisions": [{"at": "09:55", "q": "<question asked>", "a": "<answer>"}],
  "events": [{"at": "10:02", "what": "<what happened>"}],
  "deploys": [{"n": 1, "at": "11:00", "revision": "<rev>", "image": "<sha>", "what": "<what shipped>", "checks": "<how it was checked>"}],
  "review": {"model": "opus", "at": "10:45", "verdict": "<verdict>", "must_fix": ["…"]},
  "known_issues": [{"from": "<agent>", "what": "<issue>"}],
  "categories": [{"id": "platform", "name": "Platform and data", "what": "<one line>", "agents": ["infra"]}]
}
```

Add blocks such as per-wave QA or red-team results when the page needs them.

These rules come from running real builds:
- **Times:** launch times come from the orchestrator's clock, and finish times come from each branch's last commit. The agents' self-reported times were unreliable.
- **Tokens and duration:** copy them from each agent's task notification as it arrives. They are not stored anywhere else.
- **Human decisions:** log each one with the time it was made. The decisions show where a person steered, and clients want to see that.
- **Location:** keep the log in the vault's `<project>/story/` from the start, and commit it at each milestone.

## Content rules

- Every number on the page comes from the JSON block that the build script regenerates. Never hand-edit a figure into the HTML.
- Use synthetic data only. Show no credentials, test-account passwords, client PII or internal-only notes. Keep anything internal in a separate block that the page never renders.
- Check before showing a client's brand marks; their use may need approval.

## Publishing to GitHub Pages

The `gh-pages` branch is an orphan that holds only the built site: `index.html`, any extra pages, images, `.nojekyll`, and a three-line README saying the branch is generated and must not be edited by hand. The source stays in the vault.

**First time.** Ask the user before enabling Pages, because it publishes the page to everyone with read access to the repo.

```bash
git -C <repo> worktree add --detach <workspace>/<project>/wt/gh-pages
```

```bash
git -C <workspace>/<project>/wt/gh-pages switch --orphan gh-pages
```

Then copy the built site in, commit, and push with `git push -u origin gh-pages`. Enable Pages and check it came up private:

```bash
gh api -X POST repos/<org>/<repo>/pages -f 'source[branch]=gh-pages' -f 'source[path]=/'
```

```bash
gh api repos/<org>/<repo>/pages --jq '.html_url, .public'
```

`public` should be `false`. A private repo's Pages URL is a random subdomain such as `<words>-<code>.pages.github.io`, not `<org>.github.io/<repo>`. Take the URL from this call, and record it in `project.md` and the repo README.

**Each update:**
1. Rebuild with the build script.
2. Copy the output into the `gh-pages` worktree.
3. Commit with a message like `story: <what changed>`, then push.

Pages redeploys in about a minute. This branch is pushed directly rather than through a PR, because it holds published output, not source.

**An artifact copy** can be published as well, through the desktop app's Artifact tool, for a quick look or for viewers outside the repo.
