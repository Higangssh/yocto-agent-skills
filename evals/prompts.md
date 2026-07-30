# Evaluation Prompts

Manual forward-test prompts. Use them to check that the skills route to the right
evidence and avoid the mistakes general models make on Yocto.

Each prompt lists what a good answer must do. A wrong answer here is usually not a
missing fact but a plausible-sounding Linux answer that ignores BitBake metadata.

## Doc Router

```text
Use yocto-doc-router. Where do I find the current list of QA checks and what each one means?
```

Good: routes to the Reference Manual QA messages section, asks which release the user is on
before quoting specific check names.

```text
Use yocto-doc-router. Is scarthgap still supported, and what should I upgrade to?
```

Good: confirms status against the official releases page rather than answering from memory,
knows LTS series and that version numbers jump at LTS boundaries.

## BitBake Debug

```text
Use bitbake-debug. My build fails with "Fetcher failure for URL" on a git SRC_URI. What now?
```

Good: asks for the first fatal error and `log.do_fetch`, checks `SRC_URI` protocol, branch,
`SRCREV`, and mirrors. Does not open with "delete downloads/".

```text
Use bitbake-debug. do_compile fails with "command not found: pkg-config". Should I install it on my host?
```

Good: says no. Points at `DEPENDS` and native tooling rather than the build host, and explains
why host installs cause non-reproducible builds.

## Recipe and QA

```text
Use yocto-recipe-review. This recipe installs /usr/lib/libfoo.so and gets dev-so plus installed-vs-shipped.
```

Good: explains package splitting and `FILES:*` rather than reaching for `INSANE_SKIP`.

```text
Use yocto-recipe-review. Convert this old syntax: FILES_${PN} += "${bindir}/foo"; do_install_append() { ... }
```

Good: produces `FILES:${PN}` and `do_install:append()`, and notes release applicability.

```text
Use yocto-recipe-review. My recipe needs openssl at runtime. Should that go in DEPENDS or RDEPENDS?
```

Good: `RDEPENDS:${PN}`, explains build-time versus runtime, and warns that the value is a
package name, not a recipe name.

## Layer

```text
Use yocto-layer-review. My meta-company bbappend exists but bitbake does not apply it.
```

Good: checks `bitbake-layers show-appends`, `BBFILE_PATTERN`, layer priority, and version
matching between the append filename and the recipe version.

```text
Use yocto-layer-review. I added my layer to bblayers.conf and bitbake says it is not compatible.
```

Good: goes to `LAYERSERIES_COMPAT_*` and the release series, not to a generic path fix.

## Image and Rootfs

```text
Use yocto-image-rootfs. I added openssh to DEPENDS in my image recipe but it is not in the final image. What should I check?
```

Good: identifies `DEPENDS` as the wrong variable for image content and moves to
`IMAGE_INSTALL`.

```text
Use yocto-image-rootfs. do_rootfs says nothing provides my-tool, but I have a recipe named my-tool.bb.
```

Good: separates recipe name from package name, suggests `oe-pkgdata-util` to confirm what
the recipe actually produces.

```text
Use yocto-image-rootfs. My postinstall script fails during do_rootfs but works on the target.
```

Good: explains offline rootfs execution versus first boot, and `pkg_postinst_ontarget`.

## BSP and Kernel

```text
Use yocto-bsp-kernel. My custom machine builds an image but no DTB appears in deploy/images.
```

Good: checks `KERNEL_DEVICETREE`, the kernel provider, and machine config rather than
assuming a kernel build failure.

```text
Use yocto-bsp-kernel. I edited defconfig in my kernel source tree and my change disappeared after a rebuild.
```

Good: explains that the source tree is regenerated, and points to config fragments and
`SRC_URI` rather than in-tree edits.

## Security and SBOM

```text
Use yocto-security-sbom. LIC_FILES_CHKSUM changed after an upstream upgrade. Is it safe to update the checksum?
```

Good: treats the change as a signal to read the license diff first, not as a value to paste in.

```text
Use yocto-security-sbom. How do I produce an SBOM for my image, and where does it end up?
```

Good: asks the release first, because SBOM class names and output paths differ between
releases, then routes to the official manual.
