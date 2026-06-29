# Evaluation Prompts

Use these prompts to manually forward-test whether the skills route to the right evidence and avoid common hallucinations.

## Image and Rootfs

```text
Use yocto-image-rootfs. I added openssh to DEPENDS in my image recipe but it is not in the final image. What should I check?
```

```text
Use yocto-image-rootfs. do_rootfs says nothing provides my-tool, but I have a recipe named my-tool.bb.
```

## Recipe and QA

```text
Use yocto-recipe-review. This recipe installs /usr/lib/libfoo.so and gets dev-so plus installed-vs-shipped.
```

```text
Use yocto-recipe-review. Convert this old syntax: FILES_${PN} += "${bindir}/foo"; do_install_append() { ... }
```

## Layer

```text
Use yocto-layer-review. My meta-company bbappend exists but bitbake does not apply it.
```

## BSP and Kernel

```text
Use yocto-bsp-kernel. My custom machine builds an image but no DTB appears in deploy/images.
```

## Security and SBOM

```text
Use yocto-security-sbom. LIC_FILES_CHKSUM changed after an upstream upgrade. Is it safe to update the checksum?
```
