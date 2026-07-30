My recipe fails `do_package_qa` with this:

```text
ERROR: libfoo-1.2.0-r0 do_package_qa: QA Issue: libfoo: Files/directories were installed but not shipped in any package:
  /usr/lib/libfoo.so
  /usr/include/foo.h
Please set FILES such that these items are packaged. Alternatively if they are unneeded, avoid installing them or delete them within do_install.
[installed-vs-shipped]
ERROR: libfoo-1.2.0-r0 do_package_qa: QA Issue: libfoo: non -dev/-dbg/nativesdk- package contains symlink .so: libfoo path '/usr/lib/libfoo.so' [dev-so]
```

The recipe:

```bitbake
SUMMARY = "Foo library"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=abc123..."

SRC_URI = "git://example.com/foo.git;branch=main;protocol=https"
SRCREV = "deadbeef"

S = "${WORKDIR}/git"

inherit cmake

FILES:${PN} += "${libdir}/libfoo.so ${includedir}/foo.h"
```

How do I fix this?
