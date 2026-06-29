# Core Yocto Classes for Agents

Use this reference to pick the right class and review class-specific variables. Verify exact class behavior in the official Reference Manual for the target release:
https://docs.yoctoproject.org/ref-manual/classes.html

## Build System Classes

- `autotools`: GNU Autotools projects. Review `EXTRA_OECONF`, generated configure scripts, `PACKAGECONFIG`, and whether autoreconf is needed.
- `cmake`: CMake projects. Review `EXTRA_OECMAKE`, install paths, toolchain behavior, and package config options.
- `cmake-qemu`: CMake projects that need target binaries executed under QEMU during build checks.
- `meson`: Meson projects. Review `EXTRA_OEMESON`, feature options, cross files, and `PACKAGECONFIG`.
- `scons`: SCons projects. Check whether cross variables and install destinations are explicit.
- `qmake*` or framework-specific classes may be release/layer dependent; verify before recommending.

## Language and Ecosystem Classes

- `cargo`, `cargo_c`, `cargo_common`: Rust crates. Check vendoring, lockfiles, crate checksums, and network policy.
- `cargo-update-recipe-crates`: helper for updating Rust crate metadata when available.
- `go`, `go-mod`, `go-vendor`: Go builds. Check module mode, vendoring, import path, and reproducible fetching.
- `npm`: Node package builds. Check lockfiles, offline cache behavior, and network policy.
- `setuptools3`, `setuptools3-base`, `setuptools3_legacy`: Python setuptools flows.
- `python_pep517`, `python_flit_core`, `python_poetry_core`, `python_maturin`, `python_mesonpy`, `python_pdm`: PEP517 Python build backends.
- `python3native`, `python3targetconfig`: Python available for build-time or target configuration use.

## Runtime Integration Classes

- `systemd`: systemd unit packaging. Review `SYSTEMD_PACKAGES`, `SYSTEMD_SERVICE:<package>`, `SYSTEMD_AUTO_ENABLE:<package>`, and unit install path.
- `update-rc.d`: SysV init scripts. Review init script package variables.
- `update-alternatives`: alternatives registration. Ensure alternatives variables are package-specific.
- `useradd`: users and groups created by packages. Ensure packages that need users inherit/use it correctly.
- `mime`, `mime-xdg`, `gtk-icon-cache`, `fontcache`, `gsettings`: desktop/runtime cache integration.

## Kernel, BSP, Boot, and Device Tree

- `kernel`: base kernel recipe behavior.
- `kernel-yocto`: Yocto kernel metadata, features, config fragments, and validation.
- `kernel-devicetree`: devicetree build and packaging support.
- `devicetree`: standalone device tree compilation workflows.
- `kernel-fit-image`: FIT image generation.
- `kernel-module-split`: kernel module package splitting.
- `uboot-config`: U-Boot configuration variants.
- `uboot-sign`: U-Boot signing flows.

## Image, Packaging, QA, and Output

- `image`: image recipes and image construction.
- `image_types`: image type implementation.
- `image-live`, `image-container`, `image-buildinfo`: specialized image outputs.
- `rootfs*`: root filesystem construction behavior.
- `package`: packaging pipeline.
- `package_deb`, `package_ipk`, `package_rpm`: package backend specifics.
- `insane`: QA checks. Avoid `INSANE_SKIP` until the cause is understood.
- `buildhistory`: records package/image output changes.
- `rm_work`: removes work directories after build to save disk.

## License, Security, SBOM, and Source Archiving

- `license`: license collection and validation.
- `create-spdx`: SPDX/SBOM generation for releases using this class.
- `archiver`: source/archive collection.
- `copyleft_compliance`, `copyleft_filter`: copyleft source compliance flows where available.
- `cve-check` or newer SBOM/CVE classes: release-dependent; verify current release docs before naming a class.

## Testing and SDK

- `ptest`: package test support.
- `ptest-cargo`, `ptest-gnome`, `ptest-python-pytest`: ecosystem-specific ptest helpers.
- `testimage`: image runtime testing.
- `testsdk`: SDK testing.
- `populate_sdk`, `populate_sdk_ext`: SDK/eSDK generation.

## Review Rules

- Prefer inheriting the right class over hand-rolling configure/compile/install logic.
- Do not add class-specific variables unless the recipe inherits the class that consumes them.
- For build-system classes, map feature toggles through `PACKAGECONFIG` where possible.
- For runtime integration, verify files are installed and assigned to the package that declares service/init/alternative metadata.
- For language ecosystems, check lockfiles, vendoring, and network restrictions.
- For kernel/BSP classes, verify machine config, provider selection, and deploy artifacts.
