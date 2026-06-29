---
name: yocto-layer-review
description: Review Yocto/OpenEmbedded layer structure, layer.conf, BBFILE collections and patterns, LAYERSERIES_COMPAT, LAYERDEPENDS, BBFILE_PRIORITY, BBFILES_DYNAMIC, bbappend matching, overlayed recipes, provider selection, and layer compatibility. Use for layer creation, layer migration, layer review, or when a bbappend/recipe is not being applied.
---

# Yocto Layer Review

Use this skill to review layers and diagnose metadata visibility problems. Layer issues often look like recipe, provider, or package failures; prove whether BitBake sees the metadata first.

## Required Evidence

Ask for or inspect:

```text
conf/layer.conf
conf/bblayers.conf
bitbake-layers show-layers
bitbake-layers show-recipes <recipe>
bitbake-layers show-appends
bitbake-layers show-overlayed
```

## Layer Checklist

Review:

```bitbake
BBPATH .= ":${LAYERDIR}"
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb ${LAYERDIR}/recipes-*/*/*.bbappend"
BBFILE_COLLECTIONS += "mylayer"
BBFILE_PATTERN_mylayer = "^${LAYERDIR}/"
BBFILE_PRIORITY_mylayer = "6"
LAYERSERIES_COMPAT_mylayer = "scarthgap walnascar"
LAYERDEPENDS_mylayer = "core"
```

Check:

- collection name is unique and stable
- `LAYERSERIES_COMPAT_*` matches the target release
- required layers are declared with `LAYERDEPENDS_*`
- recipe and append globs cover intended files
- `BBFILE_PRIORITY_*` is not used to hide provider/version policy problems
- optional bbappends use `BBFILES_DYNAMIC` when the target layer may be absent
- `.bbappend` filename matches an existing recipe version or intentionally uses `%`

## Common Problems

- layer is present in the tree but missing from `bblayers.conf`
- `.bbappend` silently not applied due to recipe version mismatch
- collection name in `BBFILES_DYNAMIC` does not match target layer collection
- layer priority causes a recipe to win unexpectedly
- vendor BSP layer pins an older release and rejects modern syntax
- dependency layer missing even though a recipe path exists locally

## References

- Read [../../references/shared/official-doc-map.md](../../references/shared/official-doc-map.md) for official layer docs.
- Read [../../references/shared/yocto-field-guide.md](../../references/shared/yocto-field-guide.md) for layer and provider basics.
- Read [../../references/yocto/migration.md](../../references/yocto/migration.md) for release compatibility checks.

## Output

Answer with:

1. whether BitBake sees the layer and append
2. exact layer.conf or filename issue
3. metadata visibility command to prove it
4. minimal fix
5. validation command
