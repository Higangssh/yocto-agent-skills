# Example: bbappend Not Applied

## User Prompt

```text
Use yocto-layer-review to explain why my .bbappend is not being applied.
```

## Evidence to Request

- bbappend filename and path
- target recipe filename and version
- `conf/layer.conf`
- `conf/bblayers.conf`
- `bitbake-layers show-appends`
- `bitbake-layers show-recipes <recipe>`

## Bad Answer Pattern

- Telling the user to raise `BBFILE_PRIORITY` first.
- Assuming the layer is enabled because it exists on disk.

## Expected Answer Pattern

- Verify the layer is in `bblayers.conf`.
- Verify `BBFILES` includes the append path.
- Verify the append filename matches recipe name/version or intentionally uses `%`.
- Verify collection name and optional dynamic layer handling.

## Validation

```bash
bitbake-layers show-layers
bitbake-layers show-appends | rg '<recipe>'
bitbake -e <recipe> | rg '<expected variable>'
```
