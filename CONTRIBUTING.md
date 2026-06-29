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
2. Link only the references the skill needs.
3. Add an example in `examples/` if the behavior is easy to misunderstand.
4. Add or update eval prompts in `evals/prompts.md`.
5. Run validation on every changed skill.

## Validation

```bash
for d in skills/*; do
  quick_validate.py "$d"
done
```

Also scan changes for secrets, private paths, personal emails, and local-only environment details before opening a PR.
