---
name: yocto-bsp-kernel
description: Review and debug Yocto BSP, MACHINE configuration, kernel provider selection, kernel recipes, kernel config fragments, defconfig, devicetree, U-Boot, FIT images, deploy artifacts, and kernel module installation. Use for machine/BSP/kernel/devicetree/bootloader issues or when kernel artifacts are missing from deploy output.
---

# Yocto BSP Kernel

Use this skill for machine, BSP, kernel, devicetree, and bootloader work. Verify the selected machine, enabled BSP layers, kernel provider, and deploy artifacts before changing recipes.

## Evidence

Ask for or inspect:

```text
MACHINE
conf/machine/*.conf
enabled BSP layers
PREFERRED_PROVIDER_virtual/kernel
kernel recipe and bbappends
KERNEL_DEVICETREE
defconfig or config fragments
U-Boot variables
tmp/deploy/images/<machine>/
```

Useful commands:

```bash
bitbake-layers show-layers
bitbake-layers show-recipes virtual/kernel
bitbake-layers show-appends | rg 'linux|kernel|u-boot'
bitbake -e virtual/kernel | rg '^(MACHINE|PREFERRED_PROVIDER|KERNEL|UBOOT|SRC_URI|S)='
bitbake -c kernel_configme virtual/kernel
bitbake -c kernel_configcheck virtual/kernel
bitbake -c menuconfig virtual/kernel
bitbake -c diffconfig virtual/kernel
bitbake -c savedefconfig virtual/kernel
```

## Review Rules

- Machine config should express hardware policy; distro config should express product policy.
- Select kernel through `PREFERRED_PROVIDER_virtual/kernel` in machine or distro policy.
- Keep devicetree names aligned with kernel source and machine config.
- Use kernel config fragments or defconfig intentionally; validate with kernel config tasks.
- Verify deploy artifacts before debugging bootloader or flashing.
- Check vendor BSP branch compatibility before modernizing syntax.

## References

- Read [../../references/yocto/bsp-kernel.md](../../references/yocto/bsp-kernel.md).
- Read [../../references/bitbake/classes-core.md](../../references/bitbake/classes-core.md) for kernel and U-Boot classes.
- Read [../../references/yocto/migration.md](../../references/yocto/migration.md) for release compatibility risks.

## Output

Answer with:

1. selected machine and kernel provider
2. BSP/layer compatibility risk
3. kernel/devicetree/bootloader metadata issue
4. command to validate config or deploy artifacts
5. minimal metadata change
