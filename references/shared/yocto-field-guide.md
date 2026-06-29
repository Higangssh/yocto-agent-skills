# Yocto Field Guide for Agents

This guide compresses the official Yocto Project and BitBake documentation into practical agent behavior. It is not a replacement for the official manuals; use it to decide what to inspect and which official section to verify.

## Mental Model

- Yocto Project is a distribution construction system built on OpenEmbedded metadata and BitBake execution.
- BitBake parses configuration, layers, classes, recipes, and appends, then executes tasks with a datastore of expanded variables.
- Recipes produce packages; images install packages. Do not confuse recipe names, package names, and image targets.
- Layers organize metadata. Layer ordering, collection names, dependencies, priorities, and append matching affect which metadata wins.
- Tasks run in isolated work directories. The most useful truth is usually in `tmp/work/.../temp/log.do_<task>` and `run.do_<task>`.
- Shared state can hide or reveal changes. If behavior is surprising, distinguish parse-time metadata from task execution and sstate reuse.

## Core File Types

- `.bb`: recipe.
- `.bbappend`: append to an existing recipe from another layer.
- `.bbclass`: reusable class inherited by recipes.
- `.inc`: include file shared by recipes.
- `conf/layer.conf`: layer collection, file patterns, compatibility, dependencies, priority.
- `conf/local.conf`: local build configuration, not usually committed.
- `conf/bblayers.conf`: enabled layer list, not usually committed to product metadata.
- `conf/machine/*.conf`: machine/BSP configuration.
- `conf/distro/*.conf`: distro policy.
- image recipe: recipe that inherits image behavior and defines installed packages/features.

## Assignment and Override Rules

Prefer current BitBake override syntax:

```bitbake
VAR = "value"
VAR ?= "default if unset"
VAR ??= "weak default"
VAR := "${IMMEDIATE_EXPANSION}"
VAR += " value-with-leading-space-usually-needed"
VAR =+ "value-with-trailing-space-usually-needed "
VAR .= "suffix-no-space"
VAR =. "prefix-no-space"
VAR:append = " suffix"
VAR:prepend = "prefix "
VAR:remove = "token"
VAR:machine = "machine-specific"
FILES:${PN} += "${bindir}/mytool"
RDEPENDS:${PN} += "bash"
```

Agent cautions:

- Spacing matters for `+=`, `=+`, `.=` and `=.`.
- Override-style `:append`, `:prepend`, and `:remove` are applied at expansion time.
- Package-specific variables usually need package overrides such as `${PN}`, `${PN}-dev`, or `${PN}-ptest`.
- `DEPENDS` takes recipe-level build dependencies. `RDEPENDS:${PN}` takes runtime package dependencies.
- `PN` collisions with entries in `OVERRIDES` can cause surprising override behavior; check QA `pn-overrides`.

## Recipe Checklist

Minimum recipe review:

```bitbake
SUMMARY = "Short package summary"
DESCRIPTION = "Longer description if needed"
HOMEPAGE = "https://example.org"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=<md5>"
SRC_URI = "git://example.org/project.git;protocol=https;branch=main"
SRCREV = "<fixed revision>"
S = "${WORKDIR}/git"
inherit cmake
DEPENDS += "openssl"
PACKAGECONFIG ??= ""
FILES:${PN} += "${systemd_system_unitdir}/foo.service"
RDEPENDS:${PN} += "bash"
```

Check:

- Use fixed `SRCREV` for reproducible builds; avoid `${AUTOREV}` outside active development.
- Use checksums for archive downloads.
- Match `S` to unpacked source layout.
- Use the build-system class instead of hand-running generic commands when possible.
- Add build tools and libraries to `DEPENDS`, not host assumptions.
- Install only under `${D}` in `do_install`.
- Package installed files through `FILES:*`.
- Do not silence QA with `INSANE_SKIP` until the real cause is understood.

## Layer Checklist

Review `conf/layer.conf` for:

```bitbake
BBPATH .= ":${LAYERDIR}"
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend"
BBFILE_COLLECTIONS += "mylayer"
BBFILE_PATTERN_mylayer = "^${LAYERDIR}/"
BBFILE_PRIORITY_mylayer = "6"
LAYERSERIES_COMPAT_mylayer = "scarthgap walnascar"
LAYERDEPENDS_mylayer = "core"
```

Check:

- collection name is stable and unique.
- `LAYERSERIES_COMPAT_*` matches the target release.
- `LAYERDEPENDS_*` lists required layers.
- `.bbappend` files match existing recipes; verify with `bitbake-layers show-appends`.
- Dynamic appends should use `BBFILES_DYNAMIC` when optional layers may be absent.
- Avoid raising layer priority to mask dependency or provider problems.

## Task Failure Playbook

### `do_fetch`

Evidence:

- `SRC_URI`, `SRCREV`, branch, protocol, checksums.
- `log.do_fetch`.
- mirror settings and network policy.

Fix patterns:

- use `protocol=https` for Git when needed.
- pin `SRCREV` to a real commit on the selected branch.
- update archive checksums after verifying upstream source intentionally changed.
- use mirrors or premirrors for controlled environments.

### `do_unpack`

Evidence:

- source archive layout under `${WORKDIR}`.
- value of `S`.
- multi-source `SRC_URI` entries.

Fix patterns:

- set `S = "${WORKDIR}/git"` for Git fetches when needed.
- set subdirectories on `SRC_URI` entries when multiple sources collide.

### `do_patch`

Evidence:

- `SRC_URI` patch entries.
- `log.do_patch`.
- patch strip level, context, fuzz, and upstream status.

Fix patterns:

- refresh patches against the release source.
- add `Upstream-Status` where project policy requires it.
- use `apply=yes` or `apply=no` only when automatic patch handling is wrong.

### `do_configure`

Evidence:

- inherited class.
- `PACKAGECONFIG`, `EXTRA_OECONF`, `EXTRA_OECMAKE`, `EXTRA_OEMESON`.
- `recipe-sysroot` and `recipe-sysroot-native`.

Fix patterns:

- add missing build dependencies to `DEPENDS`.
- move feature toggles to `PACKAGECONFIG`.
- avoid host paths and host tools; add native tools as `foo-native` dependencies.

### `do_compile`

Evidence:

- compiler command in `log.do_compile`.
- generated files expected by build.
- parallel build race signs.

Fix patterns:

- fix upstream build system variables through the right class.
- add missing generated-code tools to `DEPENDS`.
- only disable parallel make for a proven race, and do it locally.

### `do_install`

Evidence:

- install commands in `run.do_install`.
- contents under `${D}`.
- permissions and ownership.

Fix patterns:

- use `install -d` and `install -m`.
- never install to host `/usr`, `/etc`, or source tree paths.
- use `${bindir}`, `${sbindir}`, `${libdir}`, `${sysconfdir}`, `${systemd_system_unitdir}`.

### `do_package` and `do_package_qa`

Evidence:

- QA message tag.
- files under `${D}`.
- package split variables.

Fix patterns:

- `installed-vs-shipped`: add correct files to `FILES:${PN}` or remove unwanted installed files.
- `file-rdeps`: add runtime package dependency to the right `RDEPENDS:<package>`.
- `dev-so`: move unversioned `.so` only if it is truly a development symlink.
- `already-stripped`: stop upstream install from stripping binaries.
- `host-user-contaminated`: fix install ownership; do not preserve host uid/gid.
- `patch-fuzz`: refresh patch.
- `buildpaths`: remove absolute build paths from outputs.

### `do_rootfs`

Evidence:

- `log.do_rootfs`.
- image recipe and `IMAGE_INSTALL`.
- package names from pkgdata.

Fix patterns:

- use package names, not always recipe names.
- verify package availability with `oe-pkgdata-util list-pkgs`.
- check `RPROVIDES`, `RCONFLICTS`, `RREPLACES`, and selected package manager.
- resolve license or incompatible package policy before forcing install.

## Image and Package Debugging

Useful commands:

```bash
oe-pkgdata-util list-pkgs
oe-pkgdata-util find-path '*/usr/bin/foo'
oe-pkgdata-util lookup-recipe <package>
bitbake -e <image> | rg '^(IMAGE_INSTALL|IMAGE_FEATURES|PACKAGE_CLASSES|DISTRO_FEATURES|MACHINE_FEATURES)='
```

Common mistakes:

- adding a recipe name to `IMAGE_INSTALL` when the produced package has another name.
- using `IMAGE_INSTALL +=` in `local.conf` without understanding parse ordering.
- enabling a feature in `DISTRO_FEATURES` but missing required layer or package config.
- expecting `DEPENDS` to install something into the final image.

## Provider and Dependency Debugging

Check:

```bash
bitbake-layers show-recipes <name>
bitbake-layers show-overlayed
bitbake -e <recipe> | rg '^(PREFERRED_PROVIDER|PREFERRED_VERSION|PROVIDES|RPROVIDES|DEPENDS|RDEPENDS)'
```

Rules:

- `PROVIDES` and `PREFERRED_PROVIDER_*` affect build-time provider selection.
- `RPROVIDES` affects runtime package provider selection.
- `PREFERRED_VERSION_*` selects recipe versions where multiple versions exist.
- `virtual/kernel`, `virtual/bootloader`, and similar virtual providers are policy decisions usually made by machine or distro config.

## Kernel and BSP Checklist

Check:

- `MACHINE` and machine `.conf`.
- BSP layer enabled and compatible.
- `PREFERRED_PROVIDER_virtual/kernel`.
- kernel recipe and bbappends.
- `KERNEL_DEVICETREE`, kernel fragments, defconfig, and config check logs.
- deploy artifacts under `tmp/deploy/images/${MACHINE}`.

Useful tasks:

```bash
bitbake -c menuconfig virtual/kernel
bitbake -c diffconfig virtual/kernel
bitbake -c savedefconfig virtual/kernel
bitbake -c kernel_configme virtual/kernel
bitbake -c kernel_configcheck virtual/kernel
```

## Clean Commands

Use targeted cleans:

```bash
bitbake -c clean <recipe>
bitbake -c cleansstate <recipe>
bitbake -c cleanall <recipe>
```

Guidance:

- `clean` removes work output for the recipe.
- `cleansstate` also removes shared state for that recipe.
- `cleanall` also removes downloads; avoid unless source download state is the problem.
- Prefer explaining rebuild impact before recommending cleans.

## Review Red Flags

- old override syntax used in a modern layer without release reason.
- `INSANE_SKIP` added without a linked QA root cause.
- `SRCREV = "${AUTOREV}"` in production metadata.
- missing `LIC_FILES_CHKSUM` or vague `LICENSE`.
- host tools assumed instead of `-native` dependencies.
- installing outside `${D}`.
- global changes in `local.conf` used as product metadata.
- `.bbappend` tied to an exact version when a wildcard append is intended, or wildcard append used when release behavior must be pinned.
- layer priority used to override another layer without explicit provider/version policy.
- image changes that confuse recipe names and runtime package names.
- deleting `tmp`/`sstate-cache` as a routine fix.

## Response Templates

Build failure:

```text
Most likely cause: ...
Evidence: ...
Check next: ...
Fix: ...
Why this is the Yocto fix: ...
Official docs: ...
Validation: bitbake -c <task> <recipe> or bitbake <target>
```

Recipe review:

```text
Findings:
- ...

Suggested metadata:
...

Validation:
- bitbake -e <recipe>
- bitbake -c patch <recipe>
- bitbake <recipe>
- bitbake <image>
```
