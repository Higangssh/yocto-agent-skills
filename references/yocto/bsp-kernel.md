# Yocto BSP and Kernel Reference

Use this reference for machine, BSP, kernel, devicetree, and bootloader issues. Verify exact behavior in:

- BSP Developer's Guide
- Linux Kernel Development Manual
- Reference Manual classes: `kernel`, `kernel-yocto`, `devicetree`, `uboot-config`, `uboot-sign`, `kernel-fit-image`
- Reference Manual variables: `MACHINE`, `KERNEL_DEVICETREE`, `PREFERRED_PROVIDER_virtual/kernel`, `UBOOT_CONFIG`

## BSP Mental Model

- `MACHINE` selects hardware configuration.
- BSP layers provide machine configs, kernel recipes/appends, bootloader metadata, and hardware-specific files.
- Kernel provider selection is policy, often in machine or distro configuration.
- Deploy artifacts under `tmp/deploy/images/${MACHINE}` prove what was built.

## Key Variables

- `MACHINE`: selected machine.
- `MACHINE_FEATURES`: hardware capabilities.
- `PREFERRED_PROVIDER_virtual/kernel`: selected kernel provider.
- `KERNEL_DEVICETREE`: devicetree files to build/deploy.
- `KERNEL_FEATURES`: Yocto kernel metadata features.
- `SRC_URI`: patches, config fragments, defconfig, kernel features.
- `UBOOT_CONFIG`: U-Boot configuration variants.
- `UBOOT_BINARY`: expected U-Boot binary.
- `IMAGE_BOOT_FILES`: files copied into boot partitions for some image flows.

## Kernel Debug Flow

1. Confirm `MACHINE`.
2. Confirm BSP layer is enabled and compatible.
3. Confirm `virtual/kernel` provider.
4. Inspect kernel recipe and bbappends.
5. Inspect `SRC_URI` for patches, fragments, features, and defconfig.
6. Run kernel config tasks.
7. Inspect deploy artifacts.

## Useful Commands

```bash
bitbake-layers show-recipes virtual/kernel
bitbake-layers show-appends | rg 'linux|kernel|u-boot'
bitbake -e virtual/kernel | rg '^(MACHINE|PREFERRED_PROVIDER|KERNEL|UBOOT|SRC_URI|S)='
bitbake -c kernel_configme virtual/kernel
bitbake -c kernel_configcheck virtual/kernel
bitbake -c menuconfig virtual/kernel
bitbake -c diffconfig virtual/kernel
bitbake -c savedefconfig virtual/kernel
ls tmp/deploy/images/${MACHINE}
```

## Common Problems

- Wrong `MACHINE` selected.
- BSP layer enabled but not compatible with target release.
- Kernel bbappend does not match selected kernel recipe version.
- `KERNEL_DEVICETREE` names do not match kernel tree paths.
- Config fragment requested symbols but dependencies disable them.
- U-Boot config variant does not produce expected binary.
- Deploy artifact is missing because the wrong provider or image type is being built.
