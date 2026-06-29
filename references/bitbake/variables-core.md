# BitBake and Yocto Core Variables

Use this reference for variables agents frequently confuse. Verify exact behavior in the official manuals for the user's release:

- Yocto variables: https://docs.yoctoproject.org/ref-manual/variables.html
- BitBake variables: https://docs.yoctoproject.org/bitbake/bitbake-user-manual/bitbake-user-manual-ref-variables.html

## Source and Fetch

- `SRC_URI`: source locations and patches. Check fetcher parameters such as `protocol`, `branch`, `rev`, `name`, `subdir`, `destsuffix`, `apply`, and checksums.
- `SRCREV`: fixed SCM revision. Prefer immutable commits for reproducible builds.
- `SRCREV_FORMAT`: combines multiple named revisions when a recipe fetches multiple SCMs.
- `AUTOREV`: resolves latest revision. Useful for active development, risky for production metadata.
- `S`: source directory used by tasks. Git recipes often use `S = "${WORKDIR}/git"`.
- `B`: build directory. Out-of-tree builds often use a separate `${B}`.
- `DL_DIR`: shared downloads directory.
- `PREMIRRORS` / `MIRRORS`: source mirror policy.
- `BB_NO_NETWORK`: blocks network access during builds when enabled.

## License and Compliance

- `LICENSE`: recipe or package license expression.
- `LIC_FILES_CHKSUM`: checksum of license text inside the source tree.
- `LICENSE_FLAGS`: marks packages requiring explicit acceptance.
- `LICENSE_FLAGS_ACCEPTED`: distro/user policy for accepted restricted licenses.
- `INCOMPATIBLE_LICENSE`: excludes packages by license policy.
- `COPYLEFT_LICENSE_INCLUDE` / `COPYLEFT_LICENSE_EXCLUDE`: source archiving policy for copyleft flows.

## Build Dependencies and Providers

- `DEPENDS`: build-time recipe dependencies. Makes dependency sysroot content available before configure/compile.
- `PROVIDES`: build-time names a recipe can satisfy.
- `PREFERRED_PROVIDER:<item>` or `PREFERRED_PROVIDER_virtual/*`: selects a provider when multiple recipes satisfy a name.
- `PREFERRED_VERSION:<recipe>`: selects recipe version.
- `BBCLASSEXTEND`: creates variants such as `native` and `nativesdk`.
- `ASSUME_PROVIDED`: declares host-provided tools that BitBake should not build.

## Runtime Dependencies and Package Relationships

- `RDEPENDS:<package>`: runtime dependencies.
- `RRECOMMENDS:<package>`: weak runtime recommendations.
- `RPROVIDES:<package>`: runtime names a package can satisfy.
- `RCONFLICTS:<package>`: packages that cannot be installed together.
- `RREPLACES:<package>`: packages this package replaces.
- `RSUGGESTS:<package>`: optional runtime suggestions.

Rule: `DEPENDS` affects build sysroots; `RDEPENDS` affects installed runtime packages. Do not use `DEPENDS` to put software into an image.

## Packaging

- `PACKAGES`: output package list and split order.
- `FILES:<package>`: paths assigned to a package.
- `CONFFILES:<package>`: config files preserved by the package manager.
- `ALLOW_EMPTY:<package>`: allow an empty package.
- `INSANE_SKIP:<package>`: skip QA checks narrowly and only with a documented reason.
- `PACKAGE_ARCH`: package architecture.
- `PACKAGE_BEFORE_PN`: package split ordering helper.
- `PACKAGES_DYNAMIC`: declares dynamic package names.
- `SOLIBS` / `SOLIBSDEV` / `FILES_SOLIBSDEV`: shared library split behavior.

## Images, Rootfs, and Features

- `IMAGE_INSTALL`: packages installed into an image.
- `CORE_IMAGE_EXTRA_INSTALL`: extra install list for core-image based images.
- `IMAGE_FEATURES`: image features such as debug tools or package management.
- `EXTRA_IMAGE_FEATURES`: local extra image features.
- `IMAGE_FSTYPES`: output image formats.
- `IMAGE_ROOTFS`: rootfs directory for image construction.
- `ROOTFS_POSTPROCESS_COMMAND`: rootfs post-processing hooks.
- `PACKAGE_CLASSES`: package backend selection.
- `DISTRO_FEATURES`: distro-wide feature policy.
- `MACHINE_FEATURES`: hardware/machine capabilities.
- `COMBINED_FEATURES`: intersection of distro and machine feature policy.
- `PACKAGECONFIG`: recipe feature toggles, usually mapping to configure flags and dependencies.

## Layers and Metadata Visibility

- `BBFILE_COLLECTIONS`: configured layer collection names.
- `BBFILES`: recipe and append file globs.
- `BBFILE_PATTERN_<collection>`: regex matching files in a collection.
- `BBFILE_PRIORITY_<collection>`: layer priority.
- `BBFILES_DYNAMIC`: optional append activation when another collection is present.
- `BBMASK`: hides recipes or appends from parsing.
- `BBPATH`: search path for classes and includes.
- `LAYERSERIES_COMPAT_<collection>`: compatible Yocto release series.
- `LAYERDEPENDS_<collection>`: layer dependencies.

## Machine, Distro, Kernel, and Boot

- `MACHINE`: selected hardware/machine config.
- `DISTRO`: selected distribution policy.
- `MACHINEOVERRIDES` / `DISTROOVERRIDES`: override dimensions from machine/distro policy.
- `TUNE_FEATURES`: CPU/tune features.
- `PREFERRED_PROVIDER_virtual/kernel`: selected kernel provider.
- `KERNEL_DEVICETREE`: devicetree files to build/deploy.
- `KERNEL_FEATURES`: kernel metadata features.
- `KERNEL_MODULE_AUTOLOAD`: modules loaded at boot.
- `UBOOT_CONFIG`: U-Boot configuration variants.
- `UBOOT_BINARY`: U-Boot binary output.

## Systemd and Runtime Integration

- `SYSTEMD_PACKAGES`: packages containing systemd units.
- `SYSTEMD_SERVICE:<package>`: unit files for a package.
- `SYSTEMD_AUTO_ENABLE:<package>`: enable/disable service by default.
- `INITSCRIPT_PACKAGES`, `INITSCRIPT_NAME`, `INITSCRIPT_PARAMS`: SysV init integration.
- `ALTERNATIVE:<package>` and related variables: update-alternatives integration.

## Override and Assignment Syntax

Prefer modern syntax:

```bitbake
VAR:append = " value"
VAR:prepend = "value "
VAR:remove = "value"
FILES:${PN} += "${bindir}/tool"
RDEPENDS:${PN} += "bash"
SYSTEMD_SERVICE:${PN} = "example.service"
```

Assignment reminders:

- `=` deferred expansion.
- `:=` immediate expansion.
- `?=` default if unset.
- `??=` weak default.
- `+=` and `=+` add with spacing behavior.
- `.=` and `=.` concatenate without spaces.

Only use old `_append`, `_prepend`, `_remove`, or old package override syntax when the user's release requires it.
