# Yocto Agent Skills

Official-doc-first Yocto Project and BitBake skills for AI coding agents.

Yocto is release-sensitive, deeply configurable, and easy for general LLMs to hallucinate. This repository gives agents focused skills for routing to official documentation, debugging BitBake failures, reviewing recipes, and reviewing layers.

Korean documentation: [README.ko.md](README.ko.md)

## Skills

- `skills/yocto-doc-router`: release-aware routing to the right Yocto, OpenEmbedded, and BitBake official documentation.
- `skills/bitbake-debug`: task/log/rootfs/package/provider debugging for BitBake build failures.
- `skills/yocto-recipe-review`: recipe, bbappend, bbclass, dependency, packaging, licensing, and override syntax review.
- `skills/yocto-layer-review`: layer.conf, layer compatibility, priority, dependency, provider, and bbappend matching review.

The root `SKILL.md` remains as a compatibility router for hosts that install a repository as a single skill.

## What It Helps With

- Debugging BitBake task failures: `do_fetch`, `do_unpack`, `do_patch`, `do_configure`, `do_compile`, `do_install`, `do_package`, `do_package_qa`, `do_rootfs`, `do_image`
- Writing and reviewing `.bb`, `.bbappend`, `.bbclass`, image recipes, machine config, distro config, and `layer.conf`
- Modernizing BitBake override syntax: `VAR:append`, `FILES:${PN}`, `RDEPENDS:${PN}`, task overrides, and package overrides
- Reviewing layers, bbappends, provider selection, package splitting, rootfs failures, QA messages, kernel/BSP metadata, and image composition
- Reducing common AI mistakes around `DEPENDS` vs `RDEPENDS`, recipe names vs package names, `SRCREV`, `LIC_FILES_CHKSUM`, `INSANE_SKIP`, host contamination, and sstate cleanup

## Installation

For collection-aware agents, install the individual folders under `skills/`.

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)/skills/yocto-doc-router" "${CODEX_HOME:-$HOME/.codex}/skills/yocto-doc-router"
ln -s "$(pwd)/skills/bitbake-debug" "${CODEX_HOME:-$HOME/.codex}/skills/bitbake-debug"
ln -s "$(pwd)/skills/yocto-recipe-review" "${CODEX_HOME:-$HOME/.codex}/skills/yocto-recipe-review"
ln -s "$(pwd)/skills/yocto-layer-review" "${CODEX_HOME:-$HOME/.codex}/skills/yocto-layer-review"
```

For hosts that install one folder as one skill, install the repository root:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)" "${CODEX_HOME:-$HOME/.codex}/skills/yocto-agent-skills"
```

## Example Prompts

```text
Use bitbake-debug to diagnose this do_rootfs failure.
```

```text
Use yocto-recipe-review to review this recipe and modernize the override syntax.
```

```text
Use yocto-layer-review to explain why this bbappend is not being applied.
```

```text
Use yocto-doc-router to find the official documentation path for this Yocto migration question.
```

## Contents

- `SKILL.md`: root compatibility router
- `skills/*/SKILL.md`: focused installable skills
- `references/shared/official-doc-map.md`: official Yocto/BitBake documentation routing by problem type
- `references/shared/yocto-field-guide.md`: compact field guide for recipes, layers, tasks, QA, images, providers, and BSP/kernel work
- `references/bitbake/variables-core.md`: variables agents often confuse
- `references/bitbake/classes-core.md`: common classes and review rules
- `references/yocto/qa-errors.md`: common QA error patterns
- `references/yocto/migration.md`: release-aware migration checks
- `agents/openai.yaml`: UI metadata for compatible skill hosts

## License

MIT
