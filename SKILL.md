---
name: yocto-agent-skills
description: Official-doc-first Yocto Project and BitBake agent skills for creating or reviewing recipes, layers, images, machine/distro config, bbappends, build logs, QA errors, fetch/patch/package/rootfs failures, and modern BitBake override syntax. Use when working with Yocto/OpenEmbedded files such as .bb, .bbappend, .bbclass, layer.conf, local.conf, bblayers.conf, machine config, distro config, image recipes, kernel recipes, or BitBake command output.
---

# Yocto Agent Skills

Use this skill to keep Yocto Project help grounded in current official documentation, real BitBake metadata, and build logs. Treat Yocto as release-sensitive: syntax, variables, classes, supported hosts, and QA checks can change by release.

## Ground Rules

1. Identify the user's Yocto release or branch first. If unknown, inspect `LAYERSERIES_COMPAT`, `conf/layer.conf`, `poky` branch, `oe-core` branch, or the build output. If still unknown, state the assumption and prefer current docs.
2. Prefer official docs and local metadata over memory. Use [references/official-doc-map.md](references/official-doc-map.md) to route questions to the right manual before giving precise guidance.
3. Ask for or inspect the smallest useful evidence: the failing task, the first fatal error, the relevant recipe or bbappend, `conf/bblayers.conf`, `conf/local.conf`, and `tmp/work/.../temp/log.do_*`.
4. Do not present generic Linux fixes as Yocto fixes until you map them to BitBake variables, tasks, classes, packages, or layer configuration.
5. Prefer modern override style (`VAR:override`, `:append`, `:prepend`, `:remove`) unless the target release requires old syntax.
6. Never recommend deleting `tmp/`, `downloads/`, or `sstate-cache/` as a first fix. Use targeted clean commands and explain rebuild impact.

## Workflow

### 1. Classify the Request

- **Build failure**: identify failing task (`do_fetch`, `do_unpack`, `do_patch`, `do_configure`, `do_compile`, `do_install`, `do_package`, `do_package_qa`, `do_rootfs`, `do_image`, kernel tasks).
- **Recipe work**: inspect `SUMMARY`, `LICENSE`, `LIC_FILES_CHKSUM`, `SRC_URI`, `SRCREV`, `S`, `inherit`, `DEPENDS`, `RDEPENDS:${PN}`, `FILES:${PN}`, `PACKAGECONFIG`, and custom tasks.
- **Layer work**: inspect `conf/layer.conf`, `BBFILE_COLLECTIONS`, `BBFILES`, `BBFILE_PATTERN_*`, `BBFILE_PRIORITY_*`, `LAYERSERIES_COMPAT_*`, `LAYERDEPENDS_*`, and bbappend coverage.
- **Image work**: inspect image recipe, `IMAGE_INSTALL`, `IMAGE_FEATURES`, `EXTRA_IMAGE_FEATURES`, package manager, rootfs logs, and package availability.
- **Machine or distro work**: inspect `MACHINE`, `DISTRO`, `MACHINE_FEATURES`, `DISTRO_FEATURES`, tune, kernel provider, bootloader, and BSP layer dependencies.
- **Syntax or modernization**: inspect override syntax, assignment operators, anonymous Python, variable flags, task ordering, and class inheritance.

### 2. Gather Evidence

Run or request these commands when available:

```bash
bitbake-layers show-layers
bitbake-layers show-recipes <name>
bitbake-layers show-appends
bitbake -e <recipe> | less
bitbake -c listtasks <recipe>
bitbake -c devshell <recipe>
bitbake -c cleansstate <recipe>
bitbake -k <target>
bitbake -g <target>
oe-pkgdata-util list-pkgs
oe-pkgdata-util find-path '*/path/or/file'
```

For failures, inspect:

```text
tmp/work/<machine-or-arch>/<recipe>/<version>/temp/log.do_<task>
tmp/work/<machine-or-arch>/<recipe>/<version>/temp/run.do_<task>
tmp/work/<machine-or-arch>/<recipe>/<version>/recipe-sysroot*
tmp/deploy/images/<machine>/
tmp/deploy/licenses/
tmp/log/
```

### 3. Diagnose by Task

- `do_fetch`: verify `SRC_URI`, protocol, branch, `SRCREV`, checksums, mirrors, credentials, network policy, and `DL_DIR`.
- `do_unpack`: verify archive format, `S`, subdirectory layout, and multi-source unpack paths.
- `do_patch`: verify patch paths in `SRC_URI`, strip level, patch order, fuzz, upstream status, and whether `apply=yes/no` is needed.
- `do_configure`: verify inherited build class (`autotools`, `cmake`, `meson`, `setuptools3`, etc.), `EXTRA_OECONF`, `EXTRA_OECMAKE`, `PACKAGECONFIG`, sysroot dependencies, and host contamination.
- `do_compile`: verify build-time tools in `DEPENDS`, cross-compile variables, generated headers, parallel build safety, and class-specific compile hooks.
- `do_install`: verify install destination under `${D}`, permissions, ownership, systemd/init files, and installed-vs-shipped packaging coverage.
- `do_package` / `do_package_qa`: verify `FILES:*`, split packages, runtime dependency variables, debug/dev/static package rules, and QA messages.
- `do_rootfs`: verify package names, runtime providers, `IMAGE_INSTALL`, package conflicts, license policy, postinstall scripts, and package feed data.
- `do_image`: verify rootfs completion, `IMAGE_FSTYPES`, image features, boot artifacts, WIC kickstart files, and deploy output.

### 4. Review Changes

When reviewing a Yocto patch, produce findings first:

- release compatibility risk
- syntax or override errors
- missing license/source integrity fields
- missing build or runtime dependencies
- layer priority or bbappend risk
- packaging gaps, especially installed files not shipped
- QA suppressions that hide real defects
- host contamination or non-reproducible behavior
- excessive cleans, global config changes, or build directory assumptions

### 5. Use References

- For official documentation routing, read [references/official-doc-map.md](references/official-doc-map.md).
- For compact domain guidance, task debugging, metadata syntax, variables, QA checks, and review checklists, read [references/yocto-field-guide.md](references/yocto-field-guide.md).

## Output Style

For troubleshooting, answer with:

1. most likely cause
2. evidence needed or observed
3. exact Yocto/BitBake command or metadata change
4. why it works in Yocto terms
5. official doc section to verify

For code changes, keep edits minimal and release-aware. Show the changed `.bb`, `.bbappend`, `.conf`, or `.bbclass` snippet and mention the validation command.
