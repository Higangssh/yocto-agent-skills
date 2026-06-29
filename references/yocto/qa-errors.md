# Yocto QA Errors Reference

Use this reference for common QA messages. Verify exact QA names and behavior in the official Reference Manual for the user's release:
https://docs.yoctoproject.org/ref-manual/qa-checks.html

## Debug Flow

1. Capture the exact QA tag and package name from `log.do_package_qa`.
2. Inspect files under `${D}` and the recipe's package split variables.
3. Inspect expanded metadata with `bitbake -e <recipe>`.
4. Fix metadata, install behavior, dependencies, or source content first.
5. Use `INSANE_SKIP:<package>` only with a documented reason and narrow scope.

Useful commands:

```bash
bitbake -e <recipe> | rg '^(PACKAGES|FILES|RDEPENDS|INSANE_SKIP|LICENSE|LIC_FILES_CHKSUM)[:=]'
oe-pkgdata-util list-pkgs
oe-pkgdata-util find-path '*/path/or/file'
```

## Packaging and File Layout

- `installed-vs-shipped`: files were installed into `${D}` but no output package owns them. Add the path to the right `FILES:<package>` or stop installing the file.
- `files-invalid`: `FILES:*` contains an invalid path expression. Use valid absolute target paths or package globs.
- `empty-dirs`: package contains directories expected to be empty. Remove the files or adjust install paths.
- `debug-files`: debug files are in a non-debug package. Fix `FILES:*` splits.
- `dev-so`: unversioned `.so` is in a non-dev package. Keep development symlinks in `-dev`; plugin `.so` files may need intentional packaging.
- `staticdev`: static archives are in a non-staticdev package. Move `.a` files to `${PN}-staticdev` or equivalent.
- `libdir` / `libexec`: files installed into wrong library paths. Use `${libdir}`, `${base_libdir}`, and `${libexecdir}` correctly.
- `usrmerge`: package violates usrmerge layout policy. Check install destinations against distro policy.

## Dependencies

- `file-rdeps`: package has a file-level runtime requirement that metadata does not satisfy. Add the right `RDEPENDS:<package>` or fix interpreters/linkage.
- `build-deps`: runtime dependency appears without corresponding build dependency path. Check `DEPENDS`, automatic shlibdeps, and package split.
- `dev-deps` / `debug-deps`: non-dev or non-debug packages depend on dev/debug packages. Fix package split or runtime deps.
- `dep-cmp`: dependency version comparison is invalid. Fix versioned dependency syntax.
- `shlib-provider`: shared library provider is missing or ambiguous. Check `PROVIDES`, package names, and library packaging.

## Source, Patch, and Reproducibility

- `src-uri-bad`: source URI violates policy or recommended form. Check protocol, checksums, mirrors, branch, and release policy.
- `patch-fuzz`: patch applied with fuzz. Refresh the patch against the target source.
- `patch-status`: patch metadata lacks acceptable upstream status. Add or fix `Upstream-Status` according to project policy.
- `buildpaths`: build directory paths leaked into output. Fix generated files, debug info, flags, or reproducibility settings.
- `already-stripped`: binary was stripped before Yocto debug splitting. Stop upstream build/install from stripping.
- `host-user-contaminated`: installed files preserve host uid/gid. Fix install commands and ownership.

## Configuration and Build System

- `configure-unsafe`: configure step looked at unsafe host paths. Add missing sysroot dependencies or fix configure flags.
- `configure-gettext`: gettext handling is incomplete. Check inherited classes and native gettext dependencies.
- `unknown-configure-option`: configure option is not accepted. Check `EXTRA_OECONF`, `PACKAGECONFIG`, and upstream version.
- `invalid-packageconfig`: `PACKAGECONFIG` contains an unknown option. Define option flags or remove the option.
- `pkgconfig`: `.pc` files contain bad paths or sysroot leakage. Fix installation or pkg-config variables.
- `la`: libtool archive contains problematic paths. Remove `.la` files when appropriate or fix libtool metadata.

## License and Policy

- `incompatible-license`: package is blocked by license policy. Check `LICENSE`, package license overrides, and accepted flags.
- `unlisted-pkg-lics`: package license metadata references packages not listed as expected. Check `LICENSE:<package>` and `PACKAGES`.
- `license`: generic license metadata or checksum problem. Verify `LICENSE` and `LIC_FILES_CHKSUM`.

## Naming, Syntax, and Metadata

- `pkgname`: package name is invalid. Check package naming rules and overrides.
- `packages-list`: `PACKAGES` has duplicate or invalid entries.
- `pkgvarcheck`: package-specific variable is missing a package override. Use `RDEPENDS:${PN}`, `FILES:${PN}`, etc.
- `pn-overrides`: recipe `PN` collides with active overrides. Rename or adjust metadata to avoid override confusion.
- `space-around-equal`: metadata assignment has invalid spacing. Use valid BitBake assignment syntax.
- `invalid-chars`: metadata contains invalid characters. Check variable values and package names.
- `recipe-naming`: recipe filename/version naming does not match expected policy.

## Runtime Integration

- `mime` / `mime-xdg`: MIME integration metadata is incomplete. Check inherited classes and installed MIME files.
- `desktop`: desktop file failed validation. Fix `.desktop` fields and install paths.
- `missing-update-alternatives`: alternatives metadata is incomplete. Check `ALTERNATIVE:*` variables.
- `shebang-size`: interpreter line is too long. Use shorter paths or wrapper strategy.
- `perms`, `perm-config`, `perm-line`, `perm-link`: filesystem permission metadata is invalid. Check fs-perms tables and installed mode/owner.

## Architecture and Binary Issues

- `arch`: binary architecture does not match package architecture. Check compiler, prebuilt binaries, and package arch.
- `textrel`: binary contains text relocations. Fix build flags or upstream code.
- `rpaths` / `useless-rpaths`: binary contains bad or unnecessary RPATH. Fix build system install/link flags.
- `ldflags`: binary did not use expected linker flags. Check build system and class integration.
- `xorg-driver-abi`: X.Org driver ABI dependency issue. Check driver packaging and server ABI.

## Output Rule

When explaining a QA fix, name the package-specific variable and validation command:

```text
Fix `installed-vs-shipped` by adding the installed path to `FILES:${PN}`.
Validate with `bitbake -c package_qa <recipe>` or a full recipe build.
```
