# Example: Old Override Modernization

## User Prompt

```text
Use yocto-recipe-review to modernize this recipe's old BitBake override syntax.
```

## Evidence to Request

- target Yocto release
- recipe or bbappend diff
- vendor BSP branch if relevant
- current parse error, if any

## Bad Answer Pattern

- Blindly converting syntax without checking target release.
- Changing behavior by altering spacing around `:append` or `+=`.

## Expected Answer Pattern

- Confirm release supports modern override syntax.
- Convert package overrides such as `FILES_${PN}` to `FILES:${PN}`.
- Convert `_append`, `_prepend`, `_remove` to `:append`, `:prepend`, `:remove`.
- Preserve spacing semantics.

## Validation

```bash
bitbake -p
bitbake -e <recipe> | rg '^(FILES|RDEPENDS|PACKAGECONFIG)'
```
