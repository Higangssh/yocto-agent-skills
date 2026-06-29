# Example: installed-vs-shipped QA Error

## User Prompt

```text
Use yocto-recipe-review to fix an installed-vs-shipped QA error in my recipe.
```

## Evidence to Request

- exact QA message
- affected recipe
- `log.do_package_qa`
- `do_install` function
- installed path under `${D}`
- `bitbake -e <recipe>` output for `PACKAGES` and `FILES:*`

## Bad Answer Pattern

- Adding broad `INSANE_SKIP:${PN} += "installed-vs-shipped"`.
- Adding random paths to `FILES:${PN}` without checking package split intent.

## Expected Answer Pattern

- Identify which installed file has no owning package.
- Decide whether the file should be packaged or removed.
- Add the narrow path to the correct `FILES:<package>` if it should ship.
- Validate with `bitbake -c package_qa <recipe>`.

## Validation

```bash
bitbake -e <recipe> | rg '^(PACKAGES|FILES)[:=]'
bitbake -c package_qa <recipe>
```
