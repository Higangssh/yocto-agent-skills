# BitBake and Yocto Tasks Reference

Use this reference for task-level troubleshooting. Verify exact behavior in the official Reference Manual task section for the user's release:
https://docs.yoctoproject.org/ref-manual/tasks.html

## Normal Recipe Build Tasks

- `do_fetch`: fetch sources from `SRC_URI`.
- `do_unpack`: unpack sources into the work directory.
- `do_patch`: apply patches from `SRC_URI`.
- `do_prepare_recipe_sysroot`: prepare recipe-specific sysroots from `DEPENDS`.
- `do_configure`: configure source using class-specific behavior.
- `do_compile`: compile source.
- `do_install`: install files into `${D}`.
- `do_package`: split installed files into packages.
- `do_packagedata`: write package metadata for later lookup.
- `do_package_qa`: run package QA checks.
- `do_populate_sysroot`: stage files for dependent recipes.
- `do_populate_lic`: collect license metadata.
- `do_build`: aggregate task for recipe build completion.

## Image and Rootfs Tasks

- `do_rootfs`: construct root filesystem by installing packages.
- `do_image`: generate image-specific tasks after rootfs.
- `do_image_complete`: finalize image generation and post-processing.
- `do_bootimg`: boot image generation where applicable.
- `do_testimage`: run image tests when configured.

## Package Backend Tasks

- `do_package_write_ipk`: write IPK packages.
- `do_package_write_rpm`: write RPM packages.
- `do_package_write_deb`: write DEB packages.
- `do_package_index`: generate package indexes for feeds.

## Manual and Debug Tasks

- `do_listtasks`: list recipe tasks.
- `do_devshell`: open a shell in the recipe build environment.
- `do_pydevshell`: Python development shell.
- `do_checkuri`: validate `SRC_URI`.
- `do_clean`: remove recipe work output.
- `do_cleansstate`: remove work output and shared state for a recipe.
- `do_cleanall`: also remove downloaded source; avoid unless source cache is the issue.

## Kernel Tasks

- `do_kernel_checkout`: prepare kernel source.
- `do_kernel_metadata`: process kernel metadata.
- `do_kernel_configme`: generate kernel configuration.
- `do_kernel_configcheck`: validate requested kernel configuration.
- `do_menuconfig`: interactive configuration.
- `do_diffconfig`: show config differences.
- `do_savedefconfig`: save minimal defconfig.
- `do_compile_kernelmodules`: build kernel modules.
- `do_shared_workdir`: stage kernel work for dependent recipes.

## Debug Rule

Always map an error to the first failing task and inspect:

```text
tmp/work/.../temp/log.do_<task>
tmp/work/.../temp/run.do_<task>
```

Then choose the focused skill:

- fetch/patch/configure/compile/package/rootfs: `bitbake-debug`
- image/rootfs/package selection: `yocto-image-rootfs`
- kernel/BSP tasks: `yocto-bsp-kernel`
