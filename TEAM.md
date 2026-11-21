# Team guide: HackNation 2026 (Bydgoszcz, 21–22.11)

This repo is our project **and** our AI toolkit. `house/` ("AI Software House") runs Claude Code as a small
software house: one coordinator session plans, agents code in parallel git worktrees, a judge scores the build
against the jury's criteria, and guard hooks stop agents from cheating (editing acceptance tests, committing
secrets, force-pushing `main`). Full docs (in Polish): [`house/README.md`](house/README.md).

We work on **two tasks**, one repo each:

| Task | Repo | Where it lives locally |
|---|---|---|
| ODWOŁANIA2JSON (UZP) | this repo, `Eterphis/hacknation-2026-odwolania2json` | the clone root (contest name `odwolania2json`) |
| Radar Innowacji (PCI) | `Eterphis/hacknation-2026-innovation-radar` | `house/contests/radar-innowacji` (contest name `radar-innowacji`) |

After the setup below, get the Radar repo with `house sync` and `house adapt radar-innowacji`, then open Claude
Code in `house/contests/radar-innowacji`. Each repo has its own `.house/`, coordinator and submission.

## Key times

| When | What |
|---|---|
| Sat 11:00 | Full task briefs + **scoring criteria** published → coding starts |
| Sun 11:00 | **Coding ends.** Submit on Hacktribe before this; nothing changed later counts |
| Sun 14:45 | Top 5 per task announced (Stage I = jury scores the Hacktribe submission) |
| Sun 15:15 | Stage II: **5 min pitch + 5 min Q&A** live |

Rules: max 6 per team; the jury may award nothing if no solution reaches 50% of the points.

## How we work

- **Coordinator** (one person, one Claude Code session at the repo root) drives the `/house-*` commands and
  is the only one who merges to `main` (through `house merge`, which runs the frozen checks).
- **Everyone else** takes tasks from `.house/tasks/`. Use your own Claude Code / Codex / editor, on your own
  branch `task/T###-slug`. When the task's checks pass, set `status: review` and tell the coordinator.
- **Shared state lives in `.house/` and is committed.** Read `.house/PROGRESS.md` (what's done),
  `.house/DECISIONS.md` (why), `.house/QUESTIONS.md` (open questions). Pull often.

## One-time setup (≈10 min)

You need git, **Python 3.11+** (house uses only the standard library) and the
[Claude Code CLI](https://docs.claude.com/en/docs/claude-code). Codex CLI is optional; house uses it as a
second pool of usage limits and for cross-review.

### macOS / Linux

```bash
git clone git@github.com:Eterphis/hacknation-2026-odwolania2json.git   # keep the default folder name
cd hacknation-2026-odwolania2json
git config user.name "<your name>"; git config user.email "<your email>"   # local to this repo only
python3 --version                                # must be 3.11+
python3 house/bin/house doctor                   # what tools house sees on this machine
python3 house/bin/house adapt odwolania2json    # generates your agents, skills, hooks
claude                                           # start Claude Code at the repo root
```

### Windows

```powershell
winget install --id Python.Python.3.12 --scope user    # if `py -0` shows nothing 3.11+
git clone git@github.com:Eterphis/hacknation-2026-odwolania2json.git
cd hacknation-2026-odwolania2json
git config user.name "<your name>"; git config user.email "<your email>"
py -3.12 house\bin\house doctor
py -3.12 house\bin\house adapt odwolania2json
claude
```

Our copy of house has a small Windows patch: a file-lock fallback for `fcntl`, a re-launch under Python 3.11+
in UTF-8 mode, forward-slash paths, hooks that call the right Python, acceptance checks run through Git Bash
(not cmd.exe), and hashes of protected files that ignore CRLF vs LF. After `adapt`, `house/bin/house …` works
directly from Git Bash too. The build flow (`check`, `merge`, `guard`, `export`, the `/house-*` commands) is
tested on Windows. Not on Windows: `house exp` (optimize contests), Signal, `house night` / `house review` unless
the `claude` CLI is on PATH. Write acceptance criteria as bash commands that work on macOS, Linux and Git Bash.

### What `adapt` does

- Writes `AGENTS.md`, `CLAUDE.md`, `.claude/agents/`, `.claude/skills/house-*` and the hooks in
  `.claude/settings.local.json`.
- Installs git hooks in `.git/hooks/` (`pre-commit`, `pre-push`).

These files hold **absolute paths of your machine**, so they are gitignored and every person runs `adapt` on
their own machine. Re-run it after a `git pull` that changes `house/`. If you already have a `CLAUDE.md` habit,
put your notes somewhere else: `adapt` owns that file.

The contest name in commands (`odwolania2json`) can be any valid name: house is vendored inside this repo, so
every contest command points to this repo.

## Coordinator: the flow

In Claude Code at the repo root:

1. `/house-start`: paste the **full task text, the scoring criteria and the rules** (from 11:00). It fills in
   `.house/spec.yaml` (`kind: build`, the rubric, the timeline with Sun 11:00 as the end) and asks about gaps.
2. `/house-ideate`: ideas with a "what already exists" card each, scored by the judge against the rubric. You
   pick (we run in `copilot` mode).
3. `/house-plan`: the golden path (`.house/demo-flow.md`), then tasks `T###` with acceptance criteria written
   as commands. **Review the criteria before they freeze**; that's the cheapest moment to fix them.
4. `/house-run`: agents work in `.worktrees/`; finished tasks are merged through `house merge`.
5. `/house-judge` before each milestone: a 1–5 score per criterion and the single cheapest improvement.
6. `/house-ship`: deploy, pitch script and slides (`pitch/`), submission README, clean export.

Type **"jak tam"** at any time to get a briefing (what happened, decisions made without you), then open
questions one at a time.

## Teammates: taking a task by hand

```bash
git pull
# pick a task in .house/tasks/ with status: todo and owner: null, set owner: <you>, status: doing, commit + push
git worktree add .worktrees/T004-api -b task/T004-api      # or just: git switch -c task/T004-api
# ... work ...
python3 house/bin/house check odwolania2json T004 --worktree .worktrees/T004-api   # GREEN = done
# set status: review in the task file, push the branch, tell the coordinator
```

Don'ts (the hooks enforce most of these):
- Don't change a task's `acceptance` or `protected` files to make checks pass. Ask the coordinator
  (`house check … --refreeze --reason`).
- Don't commit `.env`. Keep keys in an ignored `.env` and commit `.env.example`.
- Don't push to `main` directly or force-push. `main` changes only through `house merge`.
- Don't edit the generated files (`AGENTS.md`, `CLAUDE.md`, `.claude/agents|skills`). Change `house/core/` and
  re-run `adapt`.

## Build rules that win hackathons (from house's playbook)

- **Golden path first:** the 3-sentence demo (who, does what, sees what), end-to-end and ugly, before any polish.
- **The jury runs it without our keys.** Set API keys server-side on the deployed demo, test it from another
  device on another network early, and keep a clearly labelled demo mode with seeded data in case a key fails.
- **Integrate early,** merge often, **feature freeze ~Sun 09:30**, then only bugs, the demo video and the pitch.
- Record a **fallback demo video** before the freeze.
- Write the README and pitch for the published criteria: name each criterion and how we meet it.

## Suggested split (5 people)

| Who | Focus |
|---|---|
| Coordinator | `/house-*` flow, merges, judge rounds, decisions |
| Backend / AI | data ingestion + LLM pipeline |
| Backend / data | external data sources, registers, evaluation set |
| Frontend | demo UI, golden path, deploy |
| Product / pitch | criteria mapping, demo data, slides, video, 5-min pitch + Q&A prep |

## Publishing

The repo stays private. Whatever we publish or submit comes from a clean export:
`python3 house/bin/house export odwolania2json ../hacknation-export`. Check the export and push **that**.
It leaves out `.house/`, agent configs and `.env*`.
