---
name: git-commit
description: Use when executing git workflows such as status, diff, log, add, commit, push, branch checks, or repo-scoped git commands. Also use when the user asks to follow the team commit message convention.
allowed-tools: Read, Grep, Glob, Bash(git -C * status *), Bash(git -C * diff *), Bash(git -C * add *), Bash(git -C * commit *), Bash(git -C * branch *), Bash(git -C * log *)




---

# git-commit

Use this skill to run git operations safely and consistently.


 
step1 具体项目名字，项目路径，请根据如下文件查看：
/Users/kqy/Documents/kqyCode/Workspace/.claude/skills/repo-dir-list/SKILL.md

step2 确定项目名称之后，使用如下git命令提交代码


## Scope

Handle common git tasks:
- `git status`, `git diff`, `git log`
- `git add`, `git commit`, `git push`
- branch inspection and repository-scoped commands like `git -C <path> ...`

## Standard Workflow

1. Identify repository context.
- Run `git -C <repo> branch --show-current`.
- Run `git -C <repo> status --short`.

2. Inspect changes before committing.
- Use `git -C <repo> diff -- <file>` for targeted review.
- Use `git -C <repo> diff --stat` for summary.

3. Stage only required files.
- Prefer explicit paths in `git add`.
- Avoid staging unrelated changes.

4. Commit with required format when user asks to commit.

## Commit Message Convention

Format:
`[branch][type：summary]`

Rules:
- Use the current branch name exactly as shown by `git branch --show-current`.
- Keep `summary` short and action-oriented.
- Keep the full-width colon `：` after `type`.

Recommended `type` values:
- `feat`
- `fixbug`
- `refactor`
- `docs`
- `chore`

Examples:
- On `main`, summary is `unify localization with modular xcstrings and generated L10n`
  - `[main][feat：unify localization with modular xcstrings and generated L10n]`
- On `feature/advertise`, summary is `fix error of toast`
  - `[feature/advertise][fixbug：fix error of toast]`

## Safety Rules

- Do not run destructive git commands (for example reset/rebase/force push) unless explicitly requested.
- Do not push unless the user explicitly asks to push.
- If the worktree is dirty, preserve unrelated local changes.
