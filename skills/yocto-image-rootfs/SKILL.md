---
name: yocto-image-rootfs
description: Debug and review Yocto image recipes, IMAGE_INSTALL, IMAGE_FEATURES, package groups, do_rootfs failures, package manager errors, postinstall scripts, pkgdata lookups, package feeds, and missing packages in root filesystems. Use when packages do not appear in images, rootfs construction fails, image features behave unexpectedly, or the user needs image/rootfs guidance.
---

# Yocto Image Rootfs

Use this skill for image composition and root filesystem problems. Distinguish recipe names, package names, package groups, image features, and rootfs package manager behavior before suggesting fixes.

## Evidence

Ask for or inspect:

```text
image recipe or local.conf change
failing do_rootfs log
IMAGE_INSTALL / IMAGE_FEATURES / EXTRA_IMAGE_FEATURES
PACKAGE_CLASSES
DISTRO_FEATURES / MACHINE_FEATURES
package name being installed
oe-pkgdata-util output
```

Useful commands:

```bash
bitbake -e <image> | rg '^(IMAGE_INSTALL|IMAGE_FEATURES|EXTRA_IMAGE_FEATURES|PACKAGE_CLASSES|DISTRO_FEATURES|MACHINE_FEATURES)='
bitbake -c rootfs <image>
oe-pkgdata-util list-pkgs | rg '<name>'
oe-pkgdata-util lookup-recipe <package>
oe-pkgdata-util find-path '*/usr/bin/<tool>'
```

## Review Rules

- Use runtime package names in `IMAGE_INSTALL`, not assumed recipe names.
- Prefer image recipes or package groups for product images; keep `local.conf` changes local.
- Use `IMAGE_FEATURES` in image recipes and `EXTRA_IMAGE_FEATURES` in local configuration.
- Check package group recipes when adding groups of related packages.
- For `do_rootfs` failures, inspect package conflicts, missing providers, license policy, postinstall scripts, and package manager backend.
- Do not use `DEPENDS` to add software to an image.

## References

- Read [../../references/yocto/image-rootfs.md](../../references/yocto/image-rootfs.md).
- Read [../../references/bitbake/variables-core.md](../../references/bitbake/variables-core.md) for `IMAGE_INSTALL`, `IMAGE_FEATURES`, and package variables.
- Read [../../references/bitbake/tasks-reference.md](../../references/bitbake/tasks-reference.md) for `do_rootfs`, `do_image`, and package tasks.

## Output

Answer with:

1. recipe name vs package name status
2. exact variable or image recipe change
3. command to prove package availability
4. rootfs validation command
5. official-doc section to verify
