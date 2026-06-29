# Official Yocto Documentation Map

Use this map before giving precise Yocto or BitBake guidance. Prefer the release-specific URL that matches the user's branch. If the release is unknown, use the current docs and say so.

## Start Here

- Yocto Project Documentation index: https://docs.yoctoproject.org/
- Supported and outdated release manuals: https://docs.yoctoproject.org/releases.html
- "What I wish I'd known about Yocto Project": https://docs.yoctoproject.org/what-i-wish-id-known.html
- Quick Build: https://docs.yoctoproject.org/brief-yoctoprojectqs/
- Overview and Concepts Manual: https://docs.yoctoproject.org/overview-manual/
- Development Tasks Manual: https://docs.yoctoproject.org/dev-manual/
- Reference Manual: https://docs.yoctoproject.org/ref-manual/
- BitBake User Manual: https://docs.yoctoproject.org/bitbake/
- Board Support Package Developer's Guide: https://docs.yoctoproject.org/bsp-guide/
- Kernel Development Manual: https://docs.yoctoproject.org/kernel-dev/
- Security Manual: https://docs.yoctoproject.org/security-manual/
- Profile and Tracing Manual: https://docs.yoctoproject.org/profile-manual/
- SDK Manual: https://docs.yoctoproject.org/sdk-manual/
- Test Environment Manual: https://docs.yoctoproject.org/test-manual/
- Migration Guides: https://docs.yoctoproject.org/migration-guides/

## Route by User Problem

### New build or environment setup

Read:

- Quick Build for host setup and minimal build flow.
- Development Tasks Manual for day-to-day build setup.
- Reference Manual source directory structure for `build/`, `downloads/`, `sstate-cache/`, `tmp/`, `deploy/`, and `work/`.
- BitBake environment setup if the user asks about `bitbake-setup`.

Check:

- Supported host distro for the target release.
- `oe-init-build-env` or setup command used.
- `conf/local.conf`, `conf/bblayers.conf`, `MACHINE`, `DISTRO`, `DL_DIR`, `SSTATE_DIR`.

### BitBake syntax, overrides, assignments, functions, and tasks

Read:

- BitBake User Manual > Syntax and Operators.
- BitBake User Manual > Conditional Syntax (Overrides).
- BitBake User Manual > Functions and Tasks.
- BitBake User Manual > Dependencies.
- BitBake User Manual > Task Checksums and Setscene.

Use modern examples:

```bitbake
VAR:append = " value"
VAR:prepend = "value "
VAR:remove = "value"
FILES:${PN} += "${bindir}/tool"
RDEPENDS:${PN} += "bash"
do_install:append() {
    install -d ${D}${bindir}
}
```

Avoid old `_append`, `_prepend`, and package override syntax unless the user's release requires it.

### Recipe creation or update

Read:

- Development Tasks Manual > Writing a New Recipe.
- Reference Manual > Variables Glossary.
- Reference Manual > Classes.
- Reference Manual > Tasks.
- BitBake User Manual > File Download Support.

Check:

- `SUMMARY`, `DESCRIPTION`, `HOMEPAGE`, `LICENSE`, `LIC_FILES_CHKSUM`.
- `SRC_URI`, checksums, `SRCREV`, branch, protocol, `S`.
- inherited class: `autotools`, `cmake`, `meson`, `cargo`, `go`, `setuptools3`, `python_pep517`, `kernel`, `systemd`, etc.
- `DEPENDS` for build-time dependencies.
- `RDEPENDS:${PN}` for runtime packages.
- `FILES:${PN}` and split package variables for installed files.

### Fetch, source, patch, or license failure

Read:

- BitBake User Manual > File Download Support.
- Reference Manual > `do_fetch`, `do_unpack`, `do_patch`, `do_populate_lic`.
- Reference Manual > Variables Glossary for `SRC_URI`, `SRCREV`, `S`, `LIC_FILES_CHKSUM`.
- Reference Manual > QA Error and Warning Messages for `src-uri-bad`, `patch-fuzz`, `patch-status`, `unlisted-pkg-lics`, and license errors.

Check:

- `tmp/work/.../temp/log.do_fetch`, `log.do_unpack`, `log.do_patch`, or `log.do_populate_lic`.
- exact upstream URL, branch, revision, checksum, and patch path.
- whether the patch should apply from `SRC_URI` automatically or needs `apply=yes/no`.

### Compile, configure, install, package, or rootfs failure

Read:

- Reference Manual > Tasks.
- Reference Manual > Classes for the build system class.
- Reference Manual > QA Error and Warning Messages.
- Variables Glossary for `DEPENDS`, `EXTRA_OECONF`, `EXTRA_OECMAKE`, `PACKAGECONFIG`, `FILES`, `RDEPENDS`, `IMAGE_INSTALL`, and `IMAGE_FEATURES`.

Check:

- `log.do_configure`, `log.do_compile`, `log.do_install`, `log.do_package`, `log.do_package_qa`, `log.do_rootfs`.
- `recipe-sysroot` and `recipe-sysroot-native` for missing build tools or headers.
- installed files under `${D}` versus package file lists.
- available packages with `oe-pkgdata-util`.

### Layer, bbappend, collection, or priority problem

Read:

- Development Tasks Manual > Layers.
- Reference Manual > Variables Glossary for `BBFILE_COLLECTIONS`, `BBFILES`, `BBFILE_PATTERN`, `BBFILE_PRIORITY`, `BBMASK`, `LAYERSERIES_COMPAT`, `LAYERDEPENDS`.
- BitBake User Manual > Layers and Append Files.

Check:

- `bitbake-layers show-layers`.
- `bitbake-layers show-appends`.
- `bitbake-layers show-recipes <recipe>`.
- `conf/layer.conf`.
- whether a `.bbappend` matches an existing recipe version.

### Image, package selection, or root filesystem problem

Read:

- Development Tasks Manual image sections.
- Reference Manual > Image-related tasks.
- Reference Manual > Variables Glossary for `IMAGE_INSTALL`, `IMAGE_FEATURES`, `EXTRA_IMAGE_FEATURES`, `PACKAGE_CLASSES`, `PACKAGECONFIG`, `DISTRO_FEATURES`, `MACHINE_FEATURES`.

Check:

- whether the requested name is a recipe name or package name.
- `oe-pkgdata-util list-pkgs` and `oe-pkgdata-util find-path`.
- `log.do_rootfs`.
- package conflicts and postinstall failures.

### BSP, machine, bootloader, or kernel problem

Read:

- BSP Developer's Guide.
- Kernel Development Manual.
- Reference Manual classes: `kernel`, `kernel-yocto`, `uboot-config`, `uboot-sign`, `devicetree`, `kernel-fit-image`.
- Variables Glossary for `MACHINE`, `MACHINE_FEATURES`, `KERNEL_DEVICETREE`, `PREFERRED_PROVIDER_virtual/kernel`, `UBOOT_CONFIG`.

Check:

- machine `.conf`, tune include, BSP layer dependencies.
- kernel recipe and bbappends.
- deploy artifacts under `tmp/deploy/images/${MACHINE}`.

### Security, SBOM, CVE, or license compliance

Read:

- Security Manual.
- Yocto Project Security Reference.
- Reference Manual classes: `create-spdx`, `cve-check` or current SBOM/CVE classes, `archiver`, `copyleft_compliance`, `license`.
- Variables Glossary for license inclusion/exclusion policy.

Check:

- whether the user's release uses old or new SBOM/CVE class names.
- generated SPDX, license, and CVE output paths for that release.

## Release Awareness Checklist

- Confirm branch or release: `kirkstone`, `langdale`, `mickledore`, `nanbield`, `scarthgap`, `styhead`, `walnascar`, `next`, or vendor fork.
- Match docs to that release when possible.
- Check migration guides before changing override syntax, class names, Python version assumptions, host distro support, or security/SBOM tooling.
- Be careful with vendor BSP layers: they may lag OE-Core syntax or pin old branches.
