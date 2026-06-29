# Core Yocto Classes for Agents

Use this starter reference to pick the right class and review class-specific variables. Verify exact class behavior in the official Reference Manual for the target release.

## Build System Classes

- `autotools`: GNU Autotools projects. Review `EXTRA_OECONF`, `PACKAGECONFIG`, and generated configure scripts.
- `cmake`: CMake projects. Review `EXTRA_OECMAKE`, toolchain behavior, install paths, and `PACKAGECONFIG`.
- `meson`: Meson projects. Review `EXTRA_OEMESON`, cross files, feature options, and `PACKAGECONFIG`.
- `scons`: SCons projects; often needs explicit cross variables.
- `make`: no universal class; recipes often override compile/install tasks or rely on base behavior.

## Language and Ecosystem Classes

- `cargo`, `cargo_c`, `cargo_common`: Rust crates and vendoring flows.
- `go`, `go-mod`, `go-vendor`: Go builds, module fetching, and vendoring.
- `setuptools3`, `python_pep517`, `python_flit_core`, `python_poetry_core`, `python_maturin`: Python packaging variants.
- `npm`: Node package builds; pay attention to lockfiles and network policy.

## Runtime Integration

- `systemd`: systemd units. Review `SYSTEMD_SERVICE:<package>` and package split.
- `update-rc.d`: SysV init scripts.
- `useradd`: users and groups created by packages.
- `update-alternatives`: alternatives registration.

## Kernel, BSP, and Boot

- `kernel`: kernel recipes.
- `kernel-yocto`: Yocto kernel tooling, config fragments, features, and metadata.
- `devicetree`: devicetree compilation and packaging.
- `uboot-config`, `uboot-sign`: U-Boot configuration and signing.
- `kernel-fit-image`: FIT image generation.

## Packaging, QA, and Output

- `image`: image recipes.
- `rootfs*`: root filesystem construction behavior.
- `package`: packaging pipeline.
- `insane`: QA checks.
- `license`: license collection and validation.
- `create-spdx`: SPDX/SBOM generation on releases that use it.
- `archiver`: source/archive collection.
- `buildhistory`: track package and image output changes.

## Review Rules

- Prefer inheriting the right class over hand-rolling configure/compile/install logic.
- Do not add class-specific variables without verifying the inherited class uses them.
- For systemd/init integration, ensure service files are installed and assigned to the correct package.
- For language ecosystems, check network access and vendoring expectations for reproducibility.
