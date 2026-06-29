---
name: yocto-recipe-review
description: Review and improve Yocto/OpenEmbedded recipes, bbappends, bbclasses, package splits, dependencies, licensing, source fetching, patch handling, install logic, systemd/init integration, PACKAGECONFIG, and modern BitBake override syntax. Use for .bb, .bbappend, .bbclass, recipe diffs, recipe modernization, packaging errors, or metadata code review.
---

# Yocto Recipe Review

Use this skill for `.bb`, `.bbappend`, and `.bbclass` review. Optimize for release-aware, reproducible, package-correct metadata.

## Review Checklist

Inspect:

```bitbake
SUMMARY
DESCRIPTION
HOMEPAGE
LICENSE
LIC_FILES_CHKSUM
SRC_URI
SRCREV
S
inherit
DEPENDS
PACKAGECONFIG
do_configure
do_compile
do_install
FILES:${PN}
RDEPENDS:${PN}
SYSTEMD_SERVICE:${PN}
```

## Findings to Prioritize

- old override syntax in a modern layer without a release reason
- missing or vague `LICENSE` and `LIC_FILES_CHKSUM`
- `${AUTOREV}` in production metadata
- missing `DEPENDS` for headers, libraries, generated code tools, or `-native` tools
- runtime dependency added to `DEPENDS` instead of `RDEPENDS:<package>`
- installed files not covered by `FILES:*`
- installing outside `${D}`
- host path or host tool contamination
- unnecessary `INSANE_SKIP`
- patch entries with missing upstream status or fuzz
- bbappend that is too version-specific or too broad for the intended target

## Modern Syntax

Prefer:

```bitbake
FILES:${PN} += "${bindir}/tool"
RDEPENDS:${PN} += "bash"
PACKAGECONFIG:append = " feature"
do_install:append() {
    install -d ${D}${bindir}
}
```

Avoid `_append`, `_prepend`, `_remove`, and old package override syntax unless the target release requires it.

## References

- Read [../../references/bitbake/variables-core.md](../../references/bitbake/variables-core.md) for variable semantics.
- Read [../../references/bitbake/classes-core.md](../../references/bitbake/classes-core.md) for class-specific review.
- Read [../../references/yocto/qa-errors.md](../../references/yocto/qa-errors.md) for package QA risks.
- Use [../../references/shared/official-doc-map.md](../../references/shared/official-doc-map.md) to route official docs.

## Output

Lead with code-review findings:

```text
Findings:
- [severity] file:line issue and Yocto impact

Suggested metadata:
...

Validation:
- bitbake -e <recipe>
- bitbake -c patch <recipe>
- bitbake <recipe>
- bitbake <image>
```
