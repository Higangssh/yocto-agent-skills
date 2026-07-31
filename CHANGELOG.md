# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-07-31

Yocto Agent Skills now installs as a Claude Code plugin, and every skill folder is
self-contained.

Example:

```text
/plugin marketplace add Higangssh/yocto-agent-skills
/plugin install yocto-agent-skills@yocto-skills
```

### Added

- Add Claude Code plugin and marketplace manifests under `.claude-plugin/`.
- Add `tools/sync_references.py` to generate per-skill reference copies from the
  canonical files in `references/`.
- Add `tools/validate_skills.py` for frontmatter, link, reference drift, README catalog,
  manifest, and public-repo disclosure checks, and run it in CI.
- Add project rules in `.claude/CLAUDE.md`, including the security rules for a public
  repository.
- Add eval cases and graders under `evals/cases/`. These are not yet runnable:
  `claude plugin eval` is in early access.
- Add `.gitattributes` and `.gitignore`.

### Changed

- Each skill now carries the references it links to, so a skill keeps working when its
  folder is installed on its own. Previously every skill linked through
  `../../references/`, which broke under the documented per-skill install.
- Correct the release matrix. Guidance had stopped at `walnascar` (5.2), EOL since
  November 2025; the supported series are now 6.0 (`wrynose`) and 5.0 (`scarthgap`).
  Release lists now carry the date they were checked and link the official releases page.
- Expand eval prompts from 7 to 16, covering every skill, each with pass criteria.
- Replace the `quick_validate.py` step in `CONTRIBUTING.md`, which referenced a script
  that was never in the repository.

## [0.2.0] - 2026-06-29

Yocto Agent Skills is now a broader skill collection covering build debugging, recipes, layers, image/rootfs, BSP/kernel, and security/SBOM workflows.

Example:

```text
Use yocto-image-rootfs to find why my package is not in the final image.
```

### Added

- Add `yocto-image-rootfs`, `yocto-bsp-kernel`, and `yocto-security-sbom` skills.
- Add image/rootfs, BSP/kernel, security/SBOM, and tasks references.
- Add examples and manual eval prompts.
- Add issue templates, PR template, and contributing guide.

### Changed

- Expand README skill catalog and installation instructions.
- Update root compatibility router to include advanced skills.

## [0.1.0] - 2026-06-29

Initial public release of official-doc-first Yocto Project and BitBake skills.

### Added

- Add root compatibility skill.
- Add focused skills for doc routing, BitBake debugging, recipe review, and layer review.
- Add starter references for official docs, variables, classes, QA errors, migration, and field guidance.
