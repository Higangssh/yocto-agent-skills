# Grader: package not in image

The user put a runtime package in `DEPENDS` in an image recipe and expects it on the
device. This is the single most common Yocto mistake general models get wrong, usually by
suggesting a rebuild, a clean, or a `DEPENDS` spelling fix.

## Required to pass

The answer must do all of the following:

1. Identify `DEPENDS` as the wrong variable here, and explain that `DEPENDS` is build-time
   only, so it never places a package in the root filesystem.
2. Give `IMAGE_INSTALL` as the correct variable, with usable syntax such as
   `IMAGE_INSTALL:append = " openssh"` (the leading space, or an equivalent correct form).
3. Stay grounded in BitBake metadata rather than offering a generic Linux answer such as
   installing openssh on the host, running a package manager on the target, or editing the
   rootfs by hand.

## Automatic fail

Any of these fails the case regardless of the rest:

- Recommending deletion of `tmp/`, `downloads/`, or `sstate-cache/` as the fix.
- Claiming `DEPENDS` does install packages into the image.
- Using old override syntax such as `IMAGE_INSTALL_append` without noting that it applies
  only to releases before the `:` override change.

## Improves the score

- Distinguishing recipe names from package names, and mentioning `oe-pkgdata-util` to
  confirm what a recipe actually produces.
- Mentioning `IMAGE_FEATURES` with `ssh-server-openssh` as the idiomatic way to get an SSH
  server, rather than only naming the raw package.
- Noting that `EXTRA_IMAGE_FEATURES` in `local.conf` is the quick local alternative to
  editing the image recipe.
