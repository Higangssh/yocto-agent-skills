# Yocto Migration Starter Reference

Use this starter reference when a fix may depend on Yocto release series. Always verify exact changes in the official migration guide for the source and target releases.

## Release-Aware Checks

- Identify both source and target releases when reviewing migration work.
- Check `LAYERSERIES_COMPAT_*` in every custom layer.
- Check vendor BSP layers for pinned branches and old syntax.
- Review deprecated override syntax and class/variable behavior changes.
- Check Python, host distro, compiler, and security tooling changes.

## Common Migration Risk Areas

- Old override syntax: `_append`, `_prepend`, `_remove`, and old package overrides.
- Class names or class behavior changing across releases.
- CVE/SBOM/SPDX class and output behavior.
- QA checks becoming stricter.
- Host distro support changing.
- Package naming or provider defaults changing.
- Kernel, bootloader, and BSP layer compatibility.
- Python packaging class changes for PEP517/flit/poetry/maturin.

## Migration Review Output

For migration reviews, answer with:

1. source and target release
2. layer compatibility risks
3. syntax changes required
4. class/variable behavior that needs official migration guide confirmation
5. validation build commands

## Validation Commands

```bash
bitbake-layers show-layers
bitbake-layers show-appends
bitbake -p
bitbake -e <recipe>
bitbake -k <image>
```
