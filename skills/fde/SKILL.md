---
name: fde
description: Forward-deployed-engineer (FDE) workflow for running a client project with Claude Code. Session start - read the project vault, prove GitHub and cloud access, check local code against the remote, catch up on meetings, Teams and email, then send one concise status message. Work - Opus orchestrates while Sonnet agents build in git worktrees; every change lands through a PR with diagrams; a story page shows progress. Use whenever a session starts on a client project ("let's work on <project>", "catch me up and keep going"), when planning a multi-agent build, when opening or updating a PR on a project repo, or when asked to show progress, context, the timeline, the project list or what runs where.
argument-hint: "[visual | recap | progress | context | timeline | project | architecture | initialize] [project | text | range]"
---

# fde

How a forward-deployed engineer (FDE) runs a client project with Claude Code: get your bearings fast, then let a team of agents build while the remote repo, the PR and a story page stay current. It comes from real FDE work, where a team of agents can build a production-shaped app in an afternoon.

**Status: v1, 2026-11-20.** Items marked *open* are not decided yet, so ask rather than assume.

## Your settings

The skill reads your own settings from `~/.claude/fde.local.md`, so the skill itself holds nothing personal. If the file is missing, the first `/fde` asks for your vault (one question), writes the file, and carries on. The vault views (parts 7 and 8) ask nothing, so when the file is missing they stop and point to `/fde initialize`, which sets it up. `fde.local.example.md` in the fde-stack repo is the template.

| Setting | What it holds |
|---|---|
| Vault | The private repo that holds your project context, and where it is cloned |
| Workspace | The folder that holds project clones and agent worktrees (`<workspace>` below) |
| GitHub | Your default account, and what any second account is for |
| Transcripts | The tool you pull meeting transcripts with, or "pasted in" |
| Teams and email | The method you usually read them with |

## Arguments

This run's argument is: $ARGUMENTS

(If nothing follows the colon, there is no argument.)

| Command | What it does |
|---|---|
| `/fde` | Start of session (part 1). Ask which project if neither the folder nor the conversation makes it clear. |
| `/fde visual [text]` | Draw the text, or the last reply in this conversation if no text is given, as one diagram (part 6). |
| `/fde recap [text]` | Cut the text, or the last reply, down to a few lines, with a diagram (part 6). |
| `/fde progress [project]` | One text progress bar per workstream (part 7). |
| `/fde context [project]` | Where the code, deployment and access stand, and who is involved (part 7). |
| `/fde timeline [project] [range]` | What happened, day by day (part 7). |
| `/fde project` | The list of projects logged in the vault (part 7). |
| `/fde architecture [project]` | What runs where (GitHub, local copies, GCP or AWS), and whether each is on the latest version (part 8). |
| `/fde initialize [project]` | Every check a session depends on, as one ready-or-not checklist (part 9). |

Any other text after `/fde` is read as the task. Read the argument for its intent, not for an exact keyword: "draw this" means `visual`, "sum this up" means `recap`, "how far along are we" means `progress`, "what happened this week" means `timeline`, "what is running where" means `architecture`, and "is everything set up" means `initialize`. None of these modes starts a session.

**Arguments must be plain text.** The Claude desktop app refuses to send a slash command whose text contains inline code, links, or @-mentions of anything other than files. Pasting a formatted reply produces exactly that. When the user hits this, give them two ways around it: run `/fde recap` with no text straight after the reply, since it then works on the last reply, or send the text as an ordinary message that starts with "fde recap".

## A session has five parts

1. **Start**: work out where everything is and what changed, then send one concise status message.
2. **Work**: the main session orchestrates while agents build in worktrees.
3. **Ship**: integrate, open a PR with diagrams, deploy.
4. **Story**: keep the story page current while all of this runs.
5. **Close**: write what changed back to the vault and push.

Skip what does not apply. A ten-minute fix needs part 1 and a PR, not a story page.

## Client and company information

Transcripts, client documents and commercial figures (rates, estimates, SOW terms) belong to the client and to your company. They live in the vault and go nowhere else.

- **Nothing shared carries them.** Project repos, commit messages, PR bodies, story pages, artifacts and drafted messages get no meeting quotes, no names of client staff and no commercial figures. Use synthetic data throughout.
- **Quote only what a task needs.** Read the condensed notes first, and open a full transcript only for the part in question.
- **No outside services.** Never paste transcript or client-document text into web search, scraping or any third-party tool.
- **Paths, not contents.** Give subagents vault file paths rather than pasted transcripts, and only the meetings their task needs. Keep client text off command lines as well (see *Command-line hygiene*).
- **Project rules win.** A data rule in `project.md`, such as a client who bars any copy, overrides everything in this skill.

## Command-line hygiene

Command lines are often logged, so every session and every agent keeps them plain:

- Put scripts, data and long text in files written with the Write tool, then run the file.
- Keep client text, tokens and keys off command lines. Pass a file path instead.

---

## 1. Start of session

The point is never to build on a wrong guess about where the code is, where it runs, or what was last decided. Work it out from the vault first and ask only for what you cannot settle. Ask those questions one at a time, after the status message (see 1.7).

### 1.1 Open the vault

The vault holds every project's context, so any session, local or remote, starts from the same place. Its repo and clone path are in your settings. If the clone is missing, clone it; never create a replacement. If there is no vault yet, offer to create one: a private repo in an account or org approved for client data, with one folder per project.

- Pull it: `git -C <vault clone> pull --ff-only`.
- Find the project folder. Read `project.md` (the facts card), the top of `timeline.md`, and the README's *State* and *Not written yet* sections.
- If there is no folder, this is a new project. Confirm the name with the user, then create the folder as [references/vault-layout.md](references/vault-layout.md) describes.
- Folders older than this skill have no `project.md` or `timeline.md`. The first time such a project is opened, draft both from its README and source files, and show them to the user before committing.

### 1.2 Source code: the remote is the truth

Code lives on GitHub by default. A local clone is a convenience that goes stale, sometimes hundreds of commits behind.

1. Run `gh auth status` to see which account is active. If you have more than one, your settings say which is the default; switch before any write to another account, and switch back after.
2. Run `gh repo view <org>/<repo> --json viewerPermission` to confirm read or write access.
3. For each local clone, run `git fetch --prune`, `git status -sb` and `git worktree list`.

| What you find | What to do |
|---|---|
| In sync | Report ✓ and nothing more |
| Behind the remote, clean | `git pull --ff-only` |
| Unpushed commits or uncommitted changes | Ask: push, keep, or discard |
| Behind the remote, with uncommitted changes | Ask: keep the edits (stash, pull, re-apply) or discard them |
| Worktrees whose branches are all merged | Ask once whether to prune them, naming any branch that is not merged |
| A stale local copy whose contents are all on the remote | Ask whether to delete the local copy |
| Code that exists only locally | Ask whether to push it to a new repo |

Never delete a clone or discard work without a yes. Each of these asks becomes its own question in 1.7, saying what the item is.

### 1.3 Deployment and cloud access

Read the deployment from `project.md`: the cloud, the project or account, the region, the services, the URL and the live revision. Then prove access with a real read rather than trusting a cached login.

- **GCP:** run `gcloud auth list`, then `gcloud run services list --project <id> --limit 5`. If local runs call Vertex, check the application-default credentials with `gcloud auth application-default print-access-token | wc -c`. A non-zero count passes; never print the token itself.
- **AWS:** run `aws sts get-caller-identity --profile <profile>`. An expired SSO session needs `aws sso login --profile <profile>`, which the user runs. `aws configure sso` needs a real terminal.

**Check every login first, all at once**, before reporting anything: `gh`, `gcloud` and its application-default credentials, `aws`, and your transcript tool if you use one. SSO sign-ins often expire, so on most session starts at least one has lapsed.

A failed login is the user's to fix, because it needs their password or SSO. Put every failed login into **one** ask, each command in its own `bash` block, and wait. A device-code login is best started in the user's own terminal, so they see the code. Check afterwards that the login actually saved a token, because one run elsewhere may not have.

Platform settings live in the vault, not in this skill:
- shared defaults go in `platforms/gcp.md` and `platforms/aws.md`;
- other dependencies (model gateways, model endpoints, shared services) go in `platforms/dependencies.md`;
- project-specific overrides go in the project's `project.md`.

Record where each key lives, such as a Secret Manager name or an env var, but never its value.

### 1.4 Latest context: the timeline and meetings

`timeline.md` lists meetings and decision-grade messages, newest first, each linked to its transcript. Read from the top and weight newer entries over older ones, because a later meeting overrides an earlier decision. Stop reading back once the current picture is clear.

- **New meetings:** pull every meeting since the newest entry with your transcript tool, within your organisation's rules: only this project's meetings, a bounded date window, and temp files deleted afterwards. Without a tool, ask the user to paste or attach the transcripts. Condense each one to its decisions, commitments, dates and open questions, and read a short meeting in full rather than trusting a keyword filter.
- **Timeline entries:** add each meeting to the timeline with its date, title, decisions, asks and transcript link.
- **Missing transcripts:** a meeting with no transcript gets `Transcript: missing` in its entry, and the status message asks the user for it, naming the meeting and its date.
- **Storing transcripts:** save the full transcript in the project's `meetings/` folder, next to its condensed notes, only when the vault is a safe place: a private repo, approved for client data, that only the user and its owners can read, or a local folder. Run the check in [references/vault-layout.md](references/vault-layout.md) once per session. If the vault fails it, or `project.md` has a data rule against copies, keep only the link and the condensed notes, and tell the user why.

### 1.5 Teams and email

Settle once per session how to read Teams and email. This is a discussion, not a one-word poll: say in plain words what each method involves, recommend one (the method in `project.md` or your settings first), and agree on it with the user. The options are:

1. **Browser**, through a browser-control tool, read-only;
2. **Desktop app**, driving Teams or Outlook directly, if the session has a computer-use tool;
3. **Screenshots** the user pastes in;
4. **Skip** for this session.

Read only, newest first, and nothing older than the newest timeline entry. Anything decision-grade goes into the timeline with its source, as `Teams, <chat>, <date>` or `Email from <name>, <date>`.

### 1.6 The status message

Send one short, visual message: headlines, with the detail behind links. The user clicks through when they want more. The full detail already sits in the vault notes, so the message never repeats it.

**Rules**
- **Show where to start.** The first line is `▶`, followed by the one thing to read if the user reads nothing else.
- **Number and divide the sections.** Use headings `### 1 · Status`, `### 2 · What changed`, `### 3 · Progress` and `### 4 · Yours`, with a `---` rule between them, so the eye can find each section.
- **One line per item, about ten words or fewer.** Don't explain, quote, or say who said what, and don't include timestamps. "Chase VPN access" is enough; why and from whom is in the linked note.
- **Link every line to its source**, either the meeting note or the timeline entry, as a clickable vault path.
- **Use tables and status marks** (✓ fine, ⚠ needs attention, ✗ broken) instead of sentences. Use no other emoji.
- **What changed is ordered by time**, oldest first, so it reads as a sequence and the last row shows where things stand now. Give each day one row: its date, its sources (meetings, chats and emails, each linked), and at most two changes separated by `·`. A later row that reverses an earlier one says so ("reverses 3/2").
- **Progress uses one bar per workstream.** The workstreams come from `project.md`, so every session tracks the same ones. Each row has:
  - a 10-cell bar (`██████░░░░`);
  - an estimated percentage, rounded to 10;
  - the arrow against the last estimate in `project.md` (↑, ↓ or =);
  - a few words on the dated fact behind the number.

  The numbers are judgement, so label the section *estimate*, and never present them as measured. Afterwards, write the new estimates back to `project.md`.
- **Leave housekeeping out.** Stale clones, unpushed branches and old worktrees are not in the status message, unless one of them blocks the work. Each one becomes its own question in 1.7.
- **No questions in this message**, not even one. It ends after section 4. The next-step box only offers to start them (a "Next question" button, with "N questions waiting" in the recap). The first question arrives in the next message (1.7). In the terminal, where there is no next-step box, end with "N questions waiting" and ask the first one when the user replies.
- **Scale with the stage.** Before the work starts, the message holds only status, what changed, progress and the asks. Agent, PR and story rows come in once a build is running.

```markdown
▶ <the one thing that matters most, in a few words>

**<Project>** · <stage, e.g. "pre-start · SOW with legal"> · <next date that matters>

---

### 1 · Status
| | |
|---|---|
| Code | ✓ `main` @ <sha> |
| Deploy | ✓ <service> · <revision> |
| Access | ✓ GitHub · ✓ GCP · ⚠ <what is missing> |

---

### 2 · What changed since <date> · [timeline](<vault path>)
| Date | Source | What changed |
|---|---|---|
| 3/2 | [<meeting>](<note path>) | <change> · <change> |
| 3/3 | [<meeting>](<note path>) | <change> |

---

### 3 · Progress (estimate)
| Workstream | | | Why |
|---|---|---|---|
| <name> | `███████░░░` | 70% ↑ | <dated fact in a few words> |

---

### 4 · Yours
- <action in a few words> ([why](<path>))
- <next action>
```

### 1.7 Questions, one at a time

An FDE works across several projects a day. A list of terse questions floods them, and a question they cannot answer without digging is worse than none.

- **Questions get their own message**, never the status or a report's message. The user reads first, and the question arrives afterwards, once they press "Next question".
- **One question per message.** Ask it, wait for the answer, act on it, then ask the next. Once the answer has been acted on, the reply is one ✓ line saying what was done, a `---` rule, and then the next question.
- **Format:** a heading `### Question <n> of <N> · <topic>`, then the context sentences. The next-step box (or a question tool) holds the actual choice, so don't write the question again in the text. In the terminal, end the message with the question itself and wait for the reply.
- **Each question stands on its own.** In two or three short sentences, say:
  - what the thing is, assuming the user has never seen it;
  - why it matters now;
  - the options, with your recommendation first.

  "3 local housekeeping items" fails. "Your local copy of contoso-assistant has edits to two design docs from 3/2 that were never committed. Keep them, or discard them and pull the latest?" passes.
- **Order:**
  1. what blocks the work, such as missing access;
  2. how to read Teams and email (1.5);
  3. local housekeeping, one item per question;
  4. last, whether there is anything newer.
- **Logins are not questions.** Failed logins are asked for all together as one action, before anything else (1.3).
- **Make the last question specific.** Name the newest timeline entry and its date, and say what systems miss: a call that was not recorded, a side chat, a decision made in passing. The user often knows things no system shows.
- **Don't push.** If the user moves on to other work, say once how many questions are left, and pick them up later.

---

## 2. Work: orchestrate

### Models

| Who | Model | Why |
|---|---|---|
| The main session (orchestrator) | the latest Opus | It plans, briefs, reviews and tracks. It writes no product code, so it keeps the whole picture. |
| Coding agents | Sonnet (`model: "sonnet"`) | Feature, platform, integration, QA and story work |
| Review and planning agents | Opus (`model: "opus"`) | Work that needs judgement: the security review before a deploy, design checks, and checking subagent output |
| Simple jobs | Haiku (`model: "haiku"`) | *Open.* Candidates are status checks, listing meetings and polling a deploy. |

### The roster

| Agent | What it does | Where it works |
|---|---|---|
| Scout | Maps the code, the feature list and the cloud project before anything is built | Read-only, no worktree (`Explore`) |
| Platform | Builds cloud infrastructure and deploys on GCP or AWS, following your deploy skill if you have one | Its own worktree |
| Feature builder | Builds one feature, with its tests | Its own worktree and branch |
| Integrator | Merges the agent branches into the integration branch, resolves conflicts, runs the full test suite, pushes, and keeps the PR current | The integration worktree |
| Reviewer | Reviews before each deploy and before a PR is marked ready, covering correctness, security and the repo's CLAUDE.md rules | Read-only |
| QA | Runs headless agent QA, red-teaming and UX checks against the deployed build | Read-only, plus the test environment |
| Story | Turns the run log and git history into the story page and publishes it | The story source in the vault, plus `gh-pages` |

A typical build runs in waves: scouts first, then parallel build waves, integration, review, deploy, QA and fixes, with the story running throughout. When something blocks, re-plan instead of leaving agents waiting. If a new cloud project can't be billed, for example, move to a shared sandbox rather than wait.

### Worktrees, branches and pushes

- Give each writing agent one worktree and one branch: branch `<build>/<agent>`, worktree `<workspace>/<project>/wt/<agent>`. Named branches make integration easier and give the story its timings.
- Push every branch as soon as it has a commit worth keeping. Pushing is cheap, the remote is the backup, and the story reads from it.
- The integrator owns `<build>/integration` and is the only agent that merges.

### Briefing an agent

Each brief stands on its own, because the agent sees nothing else. It covers:
- the goal, and what done looks like;
- the files or area, the branch and worktree, and what not to touch;
- the tests to run, and what to do if they fail;
- the *Command-line hygiene* rules above;
- what to report back: commit SHAs, the tests run with their counts, what was not verified, and any decisions needed.

Agents must not change DNS, certificates or secrets, and must not delete anything. Hand those steps to the user as a script.

### The run log

The orchestrator appends to the run log as it works: each agent launch, each human decision with its time, each deploy, each block and each re-plan. The log feeds the story page and, later, the vault. Its format is in [references/story-page.md](references/story-page.md).

---

## 3. Ship: pull requests with diagrams

Every change to a project repo lands through a pull request, and every PR carries at least one diagram. The diagram lets a reviewer, or a coworker the link was forwarded to, understand the change without reading the diff.

- **Draft early:** the integrator opens a draft PR from the integration branch early and keeps its body current as waves land.
- **Diagrams:** each one is a monochrome SVG committed in the PR itself under `docs/design/img/`, and embedded by a URL pinned to that commit. Add screenshots for anything a user sees.
- **The template:** [references/pr-template.md](references/pr-template.md) has the body sections, the diagram rules and the embed URL format.
- **Merging:** merging is the merge owner's call, and the owner is recorded in `project.md`. Never merge without the user saying so.
- **After a merge:** check whether the live revision runs `main`. A live image that predates the merge is a common gap.

Three things fall outside the PR rule:
- the vault, if you push it straight to `main`;
- repos with a standing direct-push rule;
- the `gh-pages` branch, which holds published output rather than source.

---

## 4. Story page

The story page lets the FDE see the whole build at a glance while agents run, and lets them share it with coworkers or the client without a walkthrough. When the work phase starts, propose one if the build uses more than a handful of agents or the user will want to show it.

- **Updates:** the story agent rebuilds the page after each wave, deploy or PR update, then pushes it to the repo's `gh-pages` branch on private Pages.
- **Content follows progress:** early on, the page shows the plan and who is doing what. Mid-build, it shows the agent timeline and the deploys. At the end, it shows QA, conclusions and what is not done.
- **Numbers:** every number comes from the run log and git, never typed by hand.
- **Reference:** the page shape, the run-log format and the publishing steps are in [references/story-page.md](references/story-page.md).

---

## 5. Close of session

- Add today's meetings and decisions to `timeline.md`. Update `project.md` (the live revision, URLs, new dependencies) and the README's *State* and *Not written yet* sections.
- Assessments go in only once the user agrees with them. Until then they stay in the chat.
- Commit and push the vault.
- Check that every agent branch is pushed, the PR body is current, and the story page matches the last deploy.

---

## 6. Visual and recap

These modes run on `/fde visual` and `/fde recap`, and whenever the user asks for something they read to be drawn or cut down. They follow the same rules as the status message (1.6): headlines, tables and status marks, and one line per item.

| Mode | What the user gets |
|---|---|
| `visual` | The diagram alone, with at most a short title above it |
| `recap` | A few lines of text and the diagram |

### visual

Draw one diagram and nothing else: no verdict line, no ask, no paragraph. If the content needs words as well, that is a `recap`.

### recap

1. **First line:** the verdict or the problem, in about ten words.
2. **Then the facts:** a table, or at most five one-line bullets. Put them in time order when they are a sequence.
3. **Then the diagram.** It shows what the text cannot, such as the flow or the before-and-after, rather than redrawing the table.
4. **Last line:** the decision or the ask, if there is one. If the original ended with a question for the user, keep it.

- Keep every number, date, ID, SHA, ticket and name the original relies on.
- Cut narration, hedges, restated context and explanations of why.
- Never add a fact that was not in the text, and never drop an open decision.
- Aim for a third of the original's length or less, not counting the diagram.

### The diagram

Both modes draw it the same way. Choose the form from the content:

| Content | Form |
|---|---|
| Events over time | A timeline |
| A process, or how something moves (mail, requests, sign-up) | A left-to-right flow |
| A proposal against the current state | A before-and-after comparison, or two paths side by side |
| The status of many items | A table with ✓ ⚠ ✗ |
| Parts and how they connect | A box-and-arrow diagram |

- **Where to render:** inline, with the desktop app's visualize tool (`mcp__visualize__show_widget`) when the session has it; call its `read_me` first, without mentioning it. Otherwise use a markdown table, or an SVG written with the Write tool. Anything the user will keep or share goes in an Artifact or on the story page.
- **Keep it small:** one idea per diagram, about seven boxes at most, and labels of a few words.
- **Monochrome,** with one accent colour for whatever is broken or needs a decision.
- **Client information:** an inline widget in the chat is fine, but an Artifact or story page follows *Client and company information*, so it carries no client staff names and no meeting quotes.

### Example

The input was a 300-word explanation of why a nightly export to a partner's SFTP server kept failing, with a dated history and a proposal. The example is synthetic.

`visual` gives two left-to-right flows, one above the other:
- Today: the job runs, leaves from a changing IP, the partner's firewall checks it, and the file is blocked. That last box is in the accent colour.
- Proposed: the job runs, leaves through a NAT gateway with one static IP, the firewall allows it, and the file is delivered.

`recap` gives this text, with the same two flows between the table and the proposal:

```markdown
**Exports fail because the partner only accepts one fixed IP.**

| Date | Ran from | Result |
|---|---|---|
| 3/2 | Cron on the old VM | ✗ 9 of 12 runs timed out |
| 3/4 | Cloud Run job | ✗ ran, then blocked by the partner's allowlist |
| 3/6 to 3/8 | Partner ticket PT-1042 | confirmed: one static IP only |

The weekly export is set up the same way and will hit the same wall.

[the two flows]

**Proposal:** route both jobs through a NAT gateway with one static IP, and send that IP to the partner.
```

---

## 7. Quick views: progress, context, timeline, project

These views show what the vault already records, so they are quick and read-only. Pull the vault (`git pull --ff-only`), read the files, and show the view. They run no login checks, start no session, ask no questions, and write nothing back. They follow the status message's rules (1.6): tables, status marks, one line per item, and every line linked to its vault source.

| View | Reads | Shows |
|---|---|---|
| `progress` | `project.md`, Workstreams | One text bar per workstream |
| `context` | `project.md`, and the README's *State* | Where the code, deployment and access stand, and who is involved |
| `timeline` | `timeline.md` | What happened, day by day |
| `project` | Every vault folder | The list of projects |

- **Which project:** take the name after the mode (`/fde progress contoso`) and match it against the vault folders that have a `project.md`. With no name, show the project this session is working on. Work it out in this order:
  1. the project this conversation has been working on, or the last one `/fde` opened in it;
  2. the working directory, when it is a vault project folder, or a repo or worktree listed in a `project.md` Code table.

  Name the project in the first line. If neither settles it, don't guess from the most recently updated folder: show the `/fde project` list and ask which one.
- **Recorded, not proven:** each view shows the date its source was last updated. When the timeline has entries newer than that date, mark the view ⚠ and point to `/fde`, which refreshes everything.

### progress

```markdown
**<Project>** · progress (estimate, as of <date>)

| Workstream | | | Why |
|---|---|---|---|
| <name> | `███████░░░` | 70% | <dated fact in a few words> |
| <name> | `█░░░░░░░░░` | 10% | <dated fact in a few words> |
```

Use the 10-cell bars and percentages from `project.md` as they stand. Don't re-estimate, and don't average the workstreams into one total, because a single number hides the one that is stuck.

### context

```markdown
**<Project>** · <stage> · facts as of <date>

| | |
|---|---|
| Code | <repo> · `main` @ <sha> · merges: <owner> |
| Deploy | <cloud> · <project> · <revision> · [app](<url>) |
| Access | ✓ <granted> · ⚠ <missing> |
| Models and keys | <what>, key in <where> |
| People | <name> (<role>) · <name> (<role>) |
| Data rules | <rule, or "defaults"> |

Latest: [<newest timeline entry>](<path>) · <date>
```

This shows what was recorded, not what was checked. For a live check of logins and revisions, run `/fde`.

### timeline

The table from 1.6's *What changed*: oldest first, one row per day, each source linked, at most two changes per row, and reversals marked. A meeting with no transcript gets ⚠ in its source cell.

- **Range:** by default, the last 14 days of entries. `/fde timeline all` shows every entry, and `/fde timeline since 3/2` starts from that date.
- **Long ranges:** past about 15 rows, group the older days into one row per week.

### project

```markdown
**Projects in the vault** · <n> set up

| Project | Stage | Last entry | |
|---|---|---|---|
| [<folder>](<path>) | <stage> | 3/9 | ✓ |
| [<folder>](<path>) | <one line from the vault index> | 2/20 | — no facts card |
```

- **Rows:** one per vault folder, newest first, leaving out folders that are not projects (tools, a worklog).
- **Stage:** from `project.md` or the README's *State* when the folder has them, otherwise the folder's line in the vault index.
- **Last entry:** the newest `timeline.md` date, or the folder's last commit (`git log -1 --format=%cs -- <folder>`) when it has no timeline.
- **Last column:** ✓ when the folder has both `project.md` and `timeline.md`. Otherwise "no facts card", because `/fde` will draft one the first time the project is opened (1.1).

---

## 8. Architecture: what runs where, and how current

`/fde architecture [project]` shows every place the project's code lives or runs, and whether each one is on the latest version. Unlike the quick views, it checks live, because a recorded SHA is exactly what goes stale. Every check is read-only: it fetches, but never pulls, pushes, deploys or changes anything. It picks the project the same way as part 7.

### What it checks

Start from the Code and Deployment tables in `project.md`, and add `git worktree list` for each clone.

| Place | Read | "Latest" means |
|---|---|---|
| GitHub | `gh api repos/<org>/<repo>/commits/<branch> --jq '.sha[0:7], .commit.committer.date'` | The reference point: the default branch's head |
| Local clone or worktree | `git fetch --prune`, then `git rev-list --left-right --count HEAD...origin/<branch>` and `git status --porcelain` | The same commit as its remote branch, with nothing uncommitted |
| GCP Cloud Run | `gcloud run services describe <service> --project <id> --region <region> --format='value(status.latestReadyRevisionName,spec.template.spec.containers[0].image)'` | The live image was built from the remote head |
| AWS ECS | `aws ecs describe-services` for the task definition, then `aws ecs describe-task-definition` for its image | The same |
| AWS Lambda | `aws lambda get-function --function-name <name> --query 'Code.ImageUri'`, or the version and last-modified date for a zip | The same |

- **Matching an image to a commit:** when images are tagged with the commit SHA, compare the tag with the remote head and count the gap with `git rev-list --count <tag>..origin/<branch>`. When the tag is `latest` or there is only a digest, say "can't tell from the image" rather than guess.
- **Other branches:** a worktree on a feature or integration branch is compared with its own remote branch, and labelled with the branch name.
- **A lapsed login doesn't stop the view.** Its row shows ✗ "can't check", and the login command goes in one `bash` block at the end.

### What it shows

1. **First line:** the verdict, such as "Live runs an image 2 commits behind main."
2. **The diagram:** one box-and-arrow drawing, following part 6. GitHub sits in the middle, local copies on the left and deployments on the right. Each box carries its short SHA and ✓ or ⚠, and anything out of date is in the accent colour.
3. **The table:**

```markdown
| Where | What | Version | |
|---|---|---|---|
| GitHub | <org>/<repo> `main` | `<sha>` · <date> | latest |
| Local | <clone path> | `<sha>` | ✓ latest |
| Local | <worktree> (`<branch>`) | `<sha>` | ⚠ 3 behind · 2 uncommitted |
| GCP | Cloud Run <service> · <revision> | image `<sha>` | ⚠ 2 commits behind `main` |
| AWS | ECS <service> | image `latest` | ⚠ can't tell from the image |
```

4. **Last line:** anything that differs from `project.md`, such as a new live revision or a clone that no longer exists.

The view writes nothing back; `/fde` and the close of session (part 5) update the vault. It fixes nothing either: pulling, pushing and redeploying stay the user's call.

---

## 9. Initialize: the readiness checklist

`/fde initialize [project]` runs every check a session depends on, for the active project, and shows the results as one checklist. It is the checking half of `/fde`: it reads no meeting content, Teams or email, and sends no status message. Use it on a new project, a new laptop, or whenever something feels off. It picks the project the same way as part 7.

It changes nothing except pulling the vault. Every fix waits for a yes.

### The checks

| # | Check | How | Ready when |
|---|---|---|---|
| 1 | Vault | Pull it, then run the safe-place check ([vault-layout.md](references/vault-layout.md)) | Cloned, current, private, and readable only by you and the org owners |
| 2 | Project folder | Look for `project.md`, `timeline.md` and the README | All three exist, with Code, Deployment and Workstreams filled in |
| 3 | GitHub | `gh auth status`, then `viewerPermission` for each repo in Code (1.2) | The right account is active, with write access to every repo you push to |
| 4 | Local code | Fetch, then compare each clone and worktree with its remote (1.2) | Each one matches its remote, with nothing uncommitted and no stale copies |
| 5 | Cloud | `gcloud` and its application-default credentials, or `aws sts get-caller-identity` (1.3) | Signed in, and the project's services can be read |
| 6 | Live version | The deployment check from part 8 | The live image was built from the remote head |
| 7 | Keys and services | Each row in Dependencies; for a secret, confirm it exists by name (`gcloud secrets describe <name> --format='value(name)'`), never by reading its value | Every dependency says where its key lives, and that secret exists |
| 8 | Meetings | The transcript tool's sign-in, then list (never pull) meetings since the newest timeline entry (1.4) | Signed in, no entry marked `Transcript: missing`, and no meeting left out of the timeline |
| 9 | Teams and email | The Access table in `project.md` (1.5) | A method is recorded for this project |
| 10 | Latest context | The date of the newest timeline entry | Less than a week old |

Run every check, even after one fails, so the user sees the whole picture at once. Skip a check that does not apply, such as a project with no deployment yet, and mark it — rather than ✗.

### What it shows

```markdown
**<Project>** · initialize · <n> of 10 ready

| | Check | Result | Fix |
|---|---|---|---|
| ✓ | Vault | private, current | |
| ✓ | Project folder | facts card and timeline | |
| ⚠ | Local code | contoso-assistant 3 behind, clean | pull (question 1) |
| ✗ | Cloud | gcloud sign-in expired | run the login below |
| — | Live version | can't check until signed in | |
| ⚠ | Meetings | 3/3 scope call has no transcript | send it (question 2) |
| ⚠ | Latest context | newest entry 3/6, 9 days old | anything newer? (question 3) |
```

1. **Failed logins** come next, as one ask with each command in its own `bash` block (1.3).
2. **Everything else that needs a decision** becomes a question, one per message, in the order 1.7 sets. Examples: draft a missing `project.md` from the README, pull or delete a stale clone, record a Teams method, or supply a missing transcript.
3. **When every row is ✓ or —**, say so in one line and stop.

## Open items

- Which jobs go to Haiku.
- A reusable story-page template. Until one ships, build the page from the shape in [references/story-page.md](references/story-page.md).
