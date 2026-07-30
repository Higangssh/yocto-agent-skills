# Grader: installed-vs-shipped and dev-so

The user has already made the mistake the QA message invites: they added development files
to the runtime package to silence `installed-vs-shipped`, which then triggers `dev-so`.
The correct fix is to let the default packaging rules apply, not to widen `FILES:${PN}`.

## Required to pass

The answer must do all of the following:

1. Explain that `.so` symlinks and headers belong in `${PN}-dev`, not `${PN}`, and that the
   `dev-so` error is caused by the `FILES:${PN}` line already in the recipe.
2. Tell the user to remove that `FILES:${PN}` line rather than extend it, because the
   default `FILES` rules already package `${libdir}/*.so` and `${includedir}` into
   `${PN}-dev`.
3. Treat `installed-vs-shipped` as a packaging question, not a build failure: the files are
   installed correctly, they are just assigned to the wrong package.

## Automatic fail

Any of these fails the case regardless of the rest:

- Recommending `INSANE_SKIP` to silence either check. This hides a real packaging defect
  and is the answer a general model tends to give.
- Telling the user to delete the files in `do_install` when they are legitimate development
  files that belong in `${PN}-dev`.
- Recommending deletion of `tmp/`, `downloads/`, or `sstate-cache/`.
- Adding the files to `FILES:${PN}` as the recommended fix.

## Improves the score

- Noting that `${PN}-dev` is not shipped in images by default, and that a target needing
  headers wants `-dev` packages or an SDK instead.
- Mentioning `oe-pkgdata-util list-pkg-files -p libfoo` to confirm the resulting split.
- Explaining that a genuinely unversioned `.so` in the runtime package, such as a plugin,
  is the narrow case where `FILES:${PN}` plus `INSANE_SKIP:${PN} = "dev-so"` is defensible,
  so the user can tell the two situations apart.
