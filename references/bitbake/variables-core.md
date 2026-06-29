# BitBake and Yocto Core Variables

Use this starter reference for variables agents frequently confuse. Verify exact behavior in the official Reference Manual or BitBake User Manual for the user's release.

## Source and Fetch

- `SRC_URI`: source locations and patches. Supports parameters such as protocol, branch, subdir, name, apply, and checksums depending on fetcher.
- `SRCREV`: fixed source revision for SCM fetchers. Prefer fixed commits for reproducible builds.
- `AUTOREV`: resolves to latest revision. Useful during active development, risky in production metadata.
- `S`: source directory used by configure/compile tasks. Common Git value: `${WORKDIR}/git`.
- `DL_DIR`: shared download directory.
- `PREMIRRORS` / `MIRRORS`: source mirror policy.

## Build and Runtime Dependencies

- `DEPENDS`: build-time recipe dependencies; makes sysroot contents available before configure/compile.
- `RDEPENDS:<package>`: runtime package dependencies installed with a package.
- `RRECOMMENDS:<package>`: weaker runtime recommendations.
- `PROVIDES`: build-time names a recipe can provide.
- `RPROVIDES:<package>`: runtime package names a package can provide.
- `PREFERRED_PROVIDER_virtual/*`: selects build-time virtual provider, commonly kernel or bootloader.
- `PREFERRED_VERSION:<recipe>`: selects recipe version.

## Packaging

- `PACKAGES`: packages emitted by a recipe.
- `FILES:<package>`: file globs assigned to a package.
- `CONFFILES:<package>`: config files preserved by the package manager.
- `ALLOW_EMPTY:<package>`: allow empty output package.
- `INSANE_SKIP:<package>`: skip QA checks only with a documented root cause.

## Images and Features

- `IMAGE_INSTALL`: packages installed in an image.
- `IMAGE_FEATURES`: image-level features.
- `EXTRA_IMAGE_FEATURES`: often used in local configuration for extra features.
- `IMAGE_FSTYPES`: image artifact formats.
- `DISTRO_FEATURES`: distro-wide feature policy.
- `MACHINE_FEATURES`: hardware/machine capabilities.
- `PACKAGECONFIG`: recipe feature toggles, often mapped to configure flags and dependencies.

## Layers

- `BBFILE_COLLECTIONS`: configured layer collection names.
- `BBFILES`: recipe and append file globs.
- `BBFILE_PATTERN_<collection>`: regex matching files in a collection.
- `BBFILE_PRIORITY_<collection>`: layer priority.
- `BBFILES_DYNAMIC`: optional append activation when other collections are present.
- `BBMASK`: hide recipes or appends from parsing.
- `LAYERSERIES_COMPAT_<collection>`: compatible Yocto release series.
- `LAYERDEPENDS_<collection>`: layer dependencies.

## Override Syntax

Prefer modern syntax:

```bitbake
VAR:append = " value"
VAR:prepend = "value "
VAR:remove = "value"
FILES:${PN} += "${bindir}/tool"
RDEPENDS:${PN} += "bash"
```

Only use old syntax when the user's release requires it.
