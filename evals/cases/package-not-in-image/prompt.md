I am building a custom image with Yocto. I want openssh on the device, so I added it
to DEPENDS in my image recipe:

```bitbake
SUMMARY = "My product image"
LICENSE = "MIT"

inherit core-image

DEPENDS += "openssh"
```

The build succeeds, but openssh is not on the device. What is wrong?
