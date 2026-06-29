# Example: Missing Kernel Devicetree Artifact

## User Prompt

```text
Use yocto-bsp-kernel to debug why my devicetree is not in tmp/deploy/images.
```

## Evidence to Request

- `MACHINE`
- machine `.conf`
- `KERNEL_DEVICETREE`
- kernel recipe and bbappends
- `bitbake -e virtual/kernel` relevant output
- deploy directory listing

## Bad Answer Pattern

- Editing the image recipe before proving the kernel built the devicetree.
- Assuming the devicetree filename without checking kernel source paths.

## Expected Answer Pattern

- Confirm selected machine and kernel provider.
- Check whether `KERNEL_DEVICETREE` names match source tree paths.
- Validate kernel config/build tasks.
- Inspect deploy artifacts.

## Validation

```bash
bitbake -e virtual/kernel | rg '^(MACHINE|KERNEL_DEVICETREE|PREFERRED_PROVIDER)'
bitbake -c kernel_configcheck virtual/kernel
bitbake virtual/kernel
ls tmp/deploy/images/${MACHINE}
```
