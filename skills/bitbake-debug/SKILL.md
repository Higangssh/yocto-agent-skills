---
name: bitbake-debug
description: Debug BitBake and Yocto build failures from task logs, run scripts, metadata expansion, packages, providers, rootfs errors, fetch/patch/configure/compile/install/package/image failures, and common QA messages. Use when the user provides BitBake output, tmp/work logs, do_* task failures, package/rootfs errors, or asks how to diagnose a Yocto build.
---

# BitBake Debug

Use this skill to diagnose Yocto/BitBake failures from concrete evidence. Prefer `log.do_*`, `run.do_*`, `bitbake -e`, `bitbake-layers`, and pkgdata over guesses.

## Evidence First

Ask for or inspect:

```text
failing target and task
first fatal error, not only the final summary
tmp/work/.../temp/log.do_<task>
tmp/work/.../temp/run.do_<task>
conf/local.conf
conf/bblayers.conf
affected recipe or bbappend
```

Useful commands:

```bash
bitbake-layers show-layers
bitbake-layers show-recipes <recipe>
bitbake-layers show-appends
bitbake -e <recipe>
bitbake -c listtasks <recipe>
bitbake -c devshell <recipe>
bitbake -g <target>
oe-pkgdata-util list-pkgs
oe-pkgdata-util find-path '*/path/or/file'
```

## Task Playbook

- `do_fetch`: verify `SRC_URI`, protocol, branch, `SRCREV`, checksums, network policy, mirrors, `DL_DIR`, and credentials only when the source is private.
- `do_unpack`: verify archive layout, `S`, multi-source unpack paths, and subdirectories.
- `do_patch`: verify patch path, strip level, order, fuzz, upstream status, and `apply=yes/no` only when automatic patch handling is wrong.
- `do_configure`: verify inherited class, `PACKAGECONFIG`, `EXTRA_OECONF`, `EXTRA_OECMAKE`, `EXTRA_OEMESON`, `DEPENDS`, and `recipe-sysroot`.
- `do_compile`: verify compiler command, generated files, missing `-native` tools, cross variables, and parallel race signs.
- `do_install`: verify installation under `${D}`, permissions, ownership, and paths using `${bindir}`, `${libdir}`, `${sysconfdir}`, etc.
- `do_package` / `do_package_qa`: verify package splits, `FILES:*`, runtime dependencies, and QA tags.
- `do_rootfs`: verify package names, providers, `IMAGE_INSTALL`, license policy, package conflicts, and postinstall scripts.
- `do_image`: verify rootfs completion, `IMAGE_FSTYPES`, WIC kickstart, boot artifacts, and deploy output.

## References

- Read [../../references/shared/yocto-field-guide.md](../../references/shared/yocto-field-guide.md) for the broader task playbook.
- Read [../../references/yocto/qa-errors.md](../../references/yocto/qa-errors.md) for common QA failures.
- Read [../../references/bitbake/variables-core.md](../../references/bitbake/variables-core.md) when the fix depends on variable semantics.

## Output

For every diagnosis, provide:

1. most likely cause
2. evidence that supports it
3. exact next command or metadata change
4. why this is the Yocto/BitBake fix
5. validation command
