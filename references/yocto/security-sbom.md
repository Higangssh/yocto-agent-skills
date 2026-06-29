# Yocto Security, License, and SBOM Reference

Use this reference for license, CVE, SPDX/SBOM, source archiving, and compliance questions. Verify exact behavior in:

- Security Manual
- Development Tasks Manual > Working With Licenses
- Development Tasks Manual > Creating a Software Bill of Materials
- Reference Manual classes: `license`, `archiver`, `create-spdx`, CVE/SBOM classes for the user's release

## License Basics

- `LICENSE` describes recipe/package license.
- `LIC_FILES_CHKSUM` tracks license text and is mandatory unless `LICENSE = "CLOSED"`.
- License checksum mismatch means upstream license text changed; inspect the diff before updating.
- `LICENSE_FLAGS` marks packages needing explicit acceptance.
- `LICENSE_FLAGS_ACCEPTED` controls accepted restricted/commercial licenses.
- `INCOMPATIBLE_LICENSE` blocks licenses by policy.

## Artifacts

- License manifests are generated during image creation.
- SPDX/SBOM outputs are release-sensitive; verify the class and output paths.
- Source archiving can support source-offer obligations.
- CVE reports depend on product/version mappings and the release's CVE tooling.

## Debug Flow

1. Identify target release and enabled security/SBOM classes.
2. Inspect recipe `LICENSE`, `LIC_FILES_CHKSUM`, `LICENSE_FLAGS`.
3. Inspect image policy: accepted flags and incompatible licenses.
4. Build the recipe or image target that generates the artifact.
5. Inspect `tmp/deploy/licenses`, SPDX/SBOM output, or CVE report.

## Useful Commands

```bash
bitbake -e <recipe> | rg '^(LICENSE|LIC_FILES_CHKSUM|LICENSE_FLAGS|LICENSE_FLAGS_ACCEPTED|INCOMPATIBLE_LICENSE|CVE|SPDX|ARCHIVER)[:=]'
bitbake -c populate_lic <recipe>
bitbake <image>
find tmp/deploy -maxdepth 4 -iname '*spdx*' -o -path '*licenses*'
```

## Common Problems

- License checksum updated without reviewing upstream license changes.
- Commercial license accepted too broadly.
- Package blocked by `INCOMPATIBLE_LICENSE`.
- SBOM class name or output path from a different release is recommended incorrectly.
- CVE product name/version mapping creates false positives or false negatives.
- Source archiving is assumed to satisfy all legal obligations without reviewing the actual license.

## Output Rule

Do not give legal advice. Provide Yocto metadata guidance, generated artifacts, and the checks needed for counsel or compliance review.
