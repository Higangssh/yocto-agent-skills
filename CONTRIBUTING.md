# Contributing

Thanks for improving Yocto Agent Skills.

## Principles

- Prefer official Yocto Project, OpenEmbedded, and BitBake documentation.
- Keep skills concise and procedural.
- Put deeper reusable material in `references/`.
- Do not copy full official manuals.
- Include release awareness when syntax, classes, variables, or tooling can differ.
- Prefer real build evidence: `log.do_*`, `run.do_*`, `bitbake -e`, `bitbake-layers`, and `oe-pkgdata-util`.

## Adding or Updating a Skill

1. Add or update `skills/<skill-name>/SKILL.md`.
2. Link only the references the skill needs, and keep the frontmatter `name` equal to
   the folder name.
3. If the skill needs a shared reference, add it to `SKILL_REFERENCES` in
   `tools/sync_references.py` and run the script. Never hand-edit
   `skills/*/references/` — those files are generated.
4. Add an example in `examples/` if the behavior is easy to misunderstand.
5. Add or update eval prompts in `evals/prompts.md`.
6. Update the skill catalog in both `README.md` and `README.ko.md`.
7. Run validation.

## Validation

```bash
python tools/sync_references.py     # regenerate skill-local reference copies
python tools/validate_skills.py     # frontmatter, links, drift, disclosure scan
claude plugin validate . --strict   # Claude Code plugin manifest
```

Validation must pass before opening a PR. CI runs the same checks.

## Security

This is a public repository, so every commit is a publication.

`tools/validate_skills.py` scans for email addresses, real usernames, absolute local
paths, and credential patterns, but it cannot catch everything. Before opening a PR,
review your changes -- including commit messages -- for internal hostnames,
company-internal layer names, private Git URLs, and anything else pasted in from a real
build machine. Build logs are the most common leak source: strip host paths, usernames,
and internal URLs before using one as an example.

See [.claude/CLAUDE.md](.claude/CLAUDE.md) for the full project rules.
