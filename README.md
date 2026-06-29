# Yocto Agent Skills

Official-doc-first Yocto Project and BitBake skills for AI coding agents.

Yocto is release-sensitive, deeply configurable, and easy for general LLMs to hallucinate. This repository gives agents focused skills for routing to official documentation, debugging BitBake failures, reviewing recipes, reviewing layers, diagnosing image/rootfs problems, working through BSP/kernel issues, and handling security/SBOM workflows.

Korean documentation: [README.ko.md](README.ko.md)

## Skills

- `skills/yocto-doc-router`: release-aware routing to the right Yocto, OpenEmbedded, and BitBake official documentation.
- `skills/bitbake-debug`: task/log/rootfs/package/provider debugging for BitBake build failures.
- `skills/yocto-recipe-review`: recipe, bbappend, bbclass, dependency, packaging, licensing, and override syntax review.
- `skills/yocto-layer-review`: layer.conf, layer compatibility, priority, dependency, provider, and bbappend matching review.
- `skills/yocto-image-rootfs`: image recipes, package names, `IMAGE_INSTALL`, `IMAGE_FEATURES`, `do_rootfs`, pkgdata, and package manager issues.
- `skills/yocto-bsp-kernel`: machine config, BSP layers, kernel providers, devicetree, defconfig, U-Boot, and deploy artifacts.
- `skills/yocto-security-sbom`: license metadata, CVE checks, SPDX/SBOM, archiver/copyleft flows, and compliance artifacts.

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
for skill in yocto-doc-router bitbake-debug yocto-recipe-review yocto-layer-review yocto-image-rootfs yocto-bsp-kernel yocto-security-sbom; do
  ln -s "$(pwd)/skills/$skill" "${CODEX_HOME:-$HOME/.codex}/skills/$skill"
done
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
Use yocto-image-rootfs to find why my package is not in the final image.
```

```text
Use yocto-bsp-kernel to debug why my devicetree is missing from deploy/images.
```

```text
Use yocto-security-sbom to review this license checksum and SBOM setup.
```

## Contents

- `SKILL.md`: root compatibility router
- `skills/*/SKILL.md`: focused installable skills
- `references/shared/official-doc-map.md`: official Yocto/BitBake documentation routing by problem type
- `references/shared/yocto-field-guide.md`: compact field guide for recipes, layers, tasks, QA, images, providers, and BSP/kernel work
- `references/bitbake/variables-core.md`: variables agents often confuse
- `references/bitbake/classes-core.md`: common classes and review rules
- `references/bitbake/tasks-reference.md`: task-level debugging reference
- `references/yocto/qa-errors.md`: common QA error patterns
- `references/yocto/migration.md`: release-aware migration checks
- `references/yocto/image-rootfs.md`: image and rootfs troubleshooting
- `references/yocto/bsp-kernel.md`: BSP and kernel troubleshooting
- `references/yocto/security-sbom.md`: security, license, CVE, and SBOM workflows
- `examples/`: realistic failure examples and expected answer patterns
- `evals/prompts.md`: manual forward-test prompts
- `agents/openai.yaml`: UI metadata for compatible skill hosts

## License

MIT
