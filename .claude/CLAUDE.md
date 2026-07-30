# Project Rules

Yocto Agent Skills is a **public repository**. Everything committed here is published:
commit messages, file contents, branch names, and issue/PR text.

## Security

Treat every commit as a publication.

- Never commit personal or machine-specific details: email addresses, real usernames,
  absolute local paths (`C:\Users\<name>\...`, `/home/<name>/...`), internal hostnames,
  company-internal layer or project names, or private Git URLs.
- Never commit credentials of any kind: tokens, API keys, SSH or GPG private keys,
  `.netrc` contents, or build-server passwords. This includes examples that merely
  look real.
- Use placeholders in documentation: `/home/user`, `meta-company`, `example.com`,
  `<recipe>`, `<machine>`.
- Keep the same rule in commit messages. A path or address pasted into a commit
  message is as public as one in a file, and rewriting history after a push is not a
  reliable fix.
- Real build logs are the most common leak source. Before pasting one into an example,
  strip host paths, usernames, and internal URLs.
- `tools/validate_skills.py` enforces these mechanically and runs in CI. Fix what it
  reports rather than adding exceptions. If a finding is a genuine false positive,
  widen `PLACEHOLDER_USERS` instead of removing the check.

Run before every commit:

```bash
python tools/validate_skills.py
```

## Content

- Prefer official Yocto Project, OpenEmbedded, and BitBake documentation over memory.
  This repository exists to stop hallucinated Yocto advice, so do not guess release
  codenames, variable names, class names, or QA message text — verify them.
- Yocto is release-sensitive. Note release applicability when syntax, classes,
  variables, or tooling differ between releases.
- Do not copy full official manuals. Link and summarize.

## Structure

- `references/` is the source of truth. `skills/*/references/` are **generated copies**
  produced by `tools/sync_references.py`. Edit the source, then re-run the script.
- Each skill folder must stay self-contained: a skill has to work when its folder alone
  is installed, so `SKILL.md` may only link files inside its own directory.
- The repository doubles as a Claude Code plugin. Skills live in `skills/<name>/SKILL.md`
  at the repository root, and `.claude-plugin/` holds only `plugin.json` and
  `marketplace.json`. This file lives in `.claude/` rather than the repository root
  because a root `CLAUDE.md` makes `claude plugin validate --strict` fail: it is
  contributor context, not something the plugin ships to users.
- Keep the frontmatter `name` equal to the skill's folder name. In a plugin skill the
  frontmatter name determines the command's last segment, so a mismatch silently
  renames the skill.
