# Yocto Agent Skills

Official-doc-first Yocto Project and BitBake skills for AI coding agents.

Yocto is release-sensitive, deeply configurable, and easy for general LLMs to hallucinate. These skills force agents to inspect the target release, route questions to official Yocto/BitBake documentation, and reason from real metadata and build logs before suggesting fixes.

Korean documentation: [README.ko.md](README.ko.md)

## What It Helps With

- Debugging BitBake task failures: `do_fetch`, `do_unpack`, `do_patch`, `do_configure`, `do_compile`, `do_install`, `do_package`, `do_package_qa`, `do_rootfs`, `do_image`
- Writing and reviewing `.bb`, `.bbappend`, `.bbclass`, image recipes, machine config, distro config, and `layer.conf`
- Modernizing BitBake override syntax: `VAR:append`, `FILES:${PN}`, `RDEPENDS:${PN}`, task overrides, and package overrides
- Reviewing layers, bbappends, provider selection, package splitting, rootfs failures, QA messages, kernel/BSP metadata, and image composition
- Reducing common AI mistakes around `DEPENDS` vs `RDEPENDS`, recipe names vs package names, `SRCREV`, `LIC_FILES_CHKSUM`, `INSANE_SKIP`, host contamination, and sstate cleanup

## Installation

Install it as a skill by copying or symlinking this repository folder into your agent's skills directory.

Examples:

```bash
# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)" "${CODEX_HOME:-$HOME/.codex}/skills/yocto-agent-skills"

# Claude Code / other SKILL.md-compatible agents
# Copy or symlink this folder into the tool's configured skills directory.
```

After installation, ask your agent to use the Yocto Agent Skills when working on Yocto Project or BitBake issues.

## Example Prompts

```text
Use the Yocto Agent Skills to debug this do_rootfs failure.
```

```text
Use the Yocto Agent Skills to review this recipe and modernize the override syntax.
```

```text
Use the Yocto Agent Skills to explain why this bbappend is not being applied.
```

## Contents

- `SKILL.md`: trigger metadata and core agent workflow
- `references/official-doc-map.md`: official Yocto/BitBake documentation routing by problem type
- `references/yocto-field-guide.md`: compact field guide for recipes, layers, tasks, QA, images, providers, and BSP/kernel work
- `agents/openai.yaml`: UI metadata for compatible skill hosts

## License

MIT
