# Example: Missing Package in do_rootfs

## User Prompt

```text
Use yocto-image-rootfs to debug this do_rootfs failure. I added `foo` to IMAGE_INSTALL but rootfs says nothing provides foo.
```

## Evidence to Request

- image recipe or `local.conf` change
- `tmp/work/.../<image>/.../temp/log.do_rootfs`
- `bitbake -e <image>` output for `IMAGE_INSTALL`
- `oe-pkgdata-util list-pkgs | rg foo`
- `bitbake-layers show-recipes foo`

## Bad Answer Pattern

- Telling the user to add `DEPENDS += "foo"` to the image.
- Assuming recipe name and package name are identical.
- Recommending a full `tmp/` deletion.

## Expected Answer Pattern

- Verify whether `foo` is a runtime package name.
- Use `oe-pkgdata-util lookup-recipe <package>` or `list-pkgs`.
- If the recipe emits `foo-bin` or `${PN}-utils`, add that package to `IMAGE_INSTALL`.
- If no package exists, review the recipe's `PACKAGES` and `FILES:*`.

## Validation

```bash
oe-pkgdata-util list-pkgs | rg foo
bitbake -c rootfs <image>
```
