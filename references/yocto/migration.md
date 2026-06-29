# Yocto Migration Reference

Use this reference when a fix may depend on Yocto release series. Always verify exact changes in the official migration guide for the source and target releases:
https://docs.yoctoproject.org/migration-guides/

## Release-Aware Checks

1. Identify source release, target release, and vendor fork if present.
2. Inspect every custom layer's `LAYERSERIES_COMPAT_*`.
3. Check vendor BSP layers for pinned branches and old syntax.
4. Review release notes and migration guides before changing class names, variables, or override syntax.
5. Validate by parsing metadata before running long builds.

Useful commands:

```bash
bitbake-layers show-layers
bitbake-layers show-appends
bitbake-layers show-overlayed
bitbake -p
bitbake -e <recipe>
bitbake -k <image>
```

## Common Migration Risk Areas

### Override Syntax

- Old `_append`, `_prepend`, `_remove`, and package override forms may fail or behave differently on newer releases.
- Prefer `VAR:append`, `VAR:prepend`, `VAR:remove`, `FILES:${PN}`, `RDEPENDS:${PN}`, and task overrides such as `do_install:append()`.
- Vendor BSP layers may still carry old syntax; check target release support before mass conversion.

### Layers

- `LAYERSERIES_COMPAT_*` must include the target release series.
- `.bbappend` files may stop matching when recipe versions change.
- Layer priority may expose different providers after an upgrade.
- Optional appends should use `BBFILES_DYNAMIC` when dependent layers may be absent.

### Classes and Variables

- Build-system class behavior can change across releases.
- Python packaging classes evolve as projects move to PEP517 backends.
- Security, CVE, and SBOM class names and output paths can change.
- QA checks may become stricter, turning warnings into failures in product workflows.

### Host and Toolchain

- Supported host distributions change by release.
- Compiler, binutils, Python, and buildtools versions may affect recipes.
- Host contamination bugs often surface during migration because newer QA detects more issues.

### Package and Image Behavior

- Package names, default providers, and feature defaults can shift.
- `IMAGE_INSTALL` issues often appear when package splits change.
- `DISTRO_FEATURES` and `MACHINE_FEATURES` interactions may change package configuration.

### Kernel and BSP

- Kernel provider, devicetree names, defconfig handling, and boot artifacts may differ.
- BSP layers may lag OE-Core and require branch-specific fixes.
- U-Boot and FIT image flows are especially release and vendor dependent.

## Migration Review Output

For migration reviews, answer with:

1. detected source and target release
2. layer compatibility risks
3. syntax changes required
4. class/variable behavior that needs official migration guide confirmation
5. build commands to validate parse, recipe, and image behavior

## Minimal Validation Ladder

Run the cheapest checks first:

```bash
bitbake -p
bitbake-layers show-appends
bitbake -e <critical-recipe>
bitbake -c package_qa <critical-recipe>
bitbake -k <image>
```
