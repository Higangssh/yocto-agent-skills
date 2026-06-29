# Yocto Image and Rootfs Reference

Use this reference for image composition, package installation, and root filesystem failures. Verify exact behavior in:

- Development Tasks Manual > Customizing Images
- Development Tasks Manual > Working with Packages
- Reference Manual > Tasks: `do_rootfs`, `do_image`, `do_image_complete`
- Reference Manual > Variables: `IMAGE_INSTALL`, `IMAGE_FEATURES`, `EXTRA_IMAGE_FEATURES`, `PACKAGE_CLASSES`

## Mental Model

- Recipes build packages.
- Images install runtime packages.
- Package groups are recipes that produce packages whose runtime dependencies pull other packages.
- `DEPENDS` affects build sysroots; it does not install software into an image.
- `IMAGE_INSTALL` wants package names, which may differ from recipe names.

## Image Variables

- `IMAGE_INSTALL`: runtime packages included in an image.
- `IMAGE_FEATURES`: image features set by the image recipe.
- `EXTRA_IMAGE_FEATURES`: local/config-level extra features.
- `CORE_IMAGE_EXTRA_INSTALL`: add packages to core-image based images.
- `IMAGE_FSTYPES`: output formats.
- `PACKAGE_CLASSES`: package backend.
- `BAD_RECOMMENDATIONS`, `NO_RECOMMENDATIONS`, `PACKAGE_EXCLUDE`: exclude packages, with backend limitations.

## Rootfs Debug Flow

1. Inspect `log.do_rootfs`.
2. Confirm whether the requested name is a package or recipe.
3. Use `oe-pkgdata-util list-pkgs` and `lookup-recipe`.
4. Check `RPROVIDES`, `RDEPENDS`, conflicts, replaces, and package backend.
5. Check license policy and postinstall script failures.
6. Rebuild rootfs with `bitbake -c rootfs <image>`.

## Common Problems

- Package added to `IMAGE_INSTALL` does not exist because the recipe emits a differently named package.
- Feature added to `IMAGE_FEATURES` maps to package groups or configuration, not a literal package.
- `IMAGE_INSTALL +=` in the wrong context behaves unexpectedly; prefer clear image recipe changes for product images.
- Package is only recommended and excluded by recommendation policy.
- Postinstall script fails during rootfs construction.
- Runtime provider conflict blocks package manager resolution.
- License policy excludes a package during image construction.

## Validation Commands

```bash
bitbake -e <image> | rg '^(IMAGE_INSTALL|IMAGE_FEATURES|EXTRA_IMAGE_FEATURES|PACKAGE_CLASSES)='
oe-pkgdata-util list-pkgs | rg '<package>'
oe-pkgdata-util lookup-recipe <package>
oe-pkgdata-util find-path '*/usr/bin/<tool>'
bitbake -c rootfs <image>
```
