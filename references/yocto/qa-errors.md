# Yocto QA Errors Starter Reference

Use this reference for common QA messages. Verify exact QA names and behavior in the official Reference Manual for the user's release.

## Common QA Checks

- `installed-vs-shipped`: files were installed into `${D}` but not assigned to any package. Fix `FILES:<package>` or stop installing unwanted files.
- `file-rdeps`: package has runtime file dependency not satisfied by package metadata. Add the right `RDEPENDS:<package>` or fix interpreter/shebang/library linkage.
- `dev-so`: unversioned `.so` is in a non-dev package. Usually assign development symlinks to `-dev`; real plugin `.so` files may need different packaging.
- `already-stripped`: binary was stripped before Yocto debug split. Stop upstream install/build from stripping.
- `host-user-contaminated`: installed files preserve host uid/gid. Fix install commands and ownership.
- `patch-fuzz`: patch applied with fuzz. Refresh patch against the target source.
- `patch-status`: patch metadata lacks acceptable upstream status where policy requires it.
- `buildpaths`: build directory paths leaked into output. Fix build flags, generated files, debug info, or reproducibility settings.
- `pn-overrides`: recipe `PN` collides with override names. Rename or adjust metadata to avoid override confusion.
- `src-uri-bad`: source URI policy or format issue. Check protocol, mirrors, checksums, and release policy.
- `invalid-packageconfig`: `PACKAGECONFIG` references unknown options. Define option flags or remove invalid entries.
- `license` / `unlisted-pkg-lics`: package license metadata does not match policy or package list.

## Debug Flow

1. Capture the exact QA tag and package name.
2. Inspect `log.do_package_qa`.
3. Inspect files under `${D}` and package split variables.
4. Inspect expanded metadata with `bitbake -e <recipe>`.
5. Fix metadata or install behavior first; use `INSANE_SKIP` only with a documented reason.

## Output Rule

When explaining a QA fix, name the package-specific variable. Prefer `FILES:${PN}`, `FILES:${PN}-dev`, `RDEPENDS:${PN}`, etc. over generic variable names.
