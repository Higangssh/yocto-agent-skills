---
name: yocto-doc-router
description: Release-aware official documentation routing for Yocto Project, OpenEmbedded, and BitBake questions. Use when the user asks where to find current Yocto docs, when a Yocto answer may depend on release/branch, or before giving precise guidance about variables, classes, tasks, QA errors, migration, BSP, kernel, SDK, security, SBOM, CVE, or build setup.
---

# Yocto Doc Router

Use this skill to route Yocto and BitBake questions to the correct official documentation before answering. Yocto is release-sensitive; do not rely on generic memory when syntax, variables, classes, host support, or QA behavior may differ by branch.

## Workflow

1. Identify the release or branch: inspect `LAYERSERIES_COMPAT_*`, `conf/layer.conf`, Poky/OE-Core branch names, build output, or vendor layer documentation.
2. If the release is unknown, state the assumption and prefer current official docs.
3. Read [../../references/shared/official-doc-map.md](../../references/shared/official-doc-map.md) to route by problem type.
4. For release changes, read [../../references/yocto/migration.md](../../references/yocto/migration.md).
5. Return the smallest useful doc path, the reason it matters, and the evidence needed from the user's tree.

## Routing Rules

- New build setup: Quick Build, Development Tasks Manual, source directory structure, supported host distro.
- Syntax and overrides: BitBake User Manual > Syntax and Operators, Conditional Syntax, Functions, Tasks.
- Variables: Reference Manual Variables Glossary plus [../../references/bitbake/variables-core.md](../../references/bitbake/variables-core.md).
- Classes: Reference Manual Classes plus [../../references/bitbake/classes-core.md](../../references/bitbake/classes-core.md).
- QA errors: Reference Manual QA messages plus [../../references/yocto/qa-errors.md](../../references/yocto/qa-errors.md).
- Layers: Development Tasks Manual > Layers, BitBake concepts for layers and appends.
- Recipes: Development Tasks Manual > Writing a New Recipe, Reference Manual Tasks and Classes.
- BSP/kernel: BSP Guide, Kernel Development Manual, relevant class and variable entries.
- Security/SBOM/CVE/license: Security Manual, Security Reference, Reference Manual classes and variables.
- Image/rootfs: Development Tasks Manual image customization, package management, and Reference Manual image/rootfs tasks.

## Output

Answer with:

1. assumed or detected release
2. official manual section to check
3. local file/log/command that confirms the issue
4. next focused skill to use, if any: `bitbake-debug`, `yocto-recipe-review`, `yocto-layer-review`, `yocto-image-rootfs`, `yocto-bsp-kernel`, or `yocto-security-sbom`
