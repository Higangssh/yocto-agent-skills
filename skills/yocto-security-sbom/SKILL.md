---
name: yocto-security-sbom
description: Review and debug Yocto license metadata, LIC_FILES_CHKSUM, LICENSE_FLAGS, incompatible licenses, license manifests, SPDX/SBOM generation, CVE checking, archiver/copyleft source compliance, and security policy. Use for compliance, CVE, SBOM, license, commercial license, source archiving, or security review questions.
---

# Yocto Security SBOM

Use this skill for security, license, CVE, SBOM, and compliance workflows. Treat class names and output paths as release-sensitive.

## Evidence

Ask for or inspect:

```text
target Yocto release
recipe LICENSE and LIC_FILES_CHKSUM
license QA error
image/license manifest output
SPDX/SBOM configuration and output
CVE check configuration and reports
archiver/copyleft configuration
commercial license policy
```

Useful commands:

```bash
bitbake -e <recipe> | rg '^(LICENSE|LIC_FILES_CHKSUM|LICENSE_FLAGS|LICENSE_FLAGS_ACCEPTED|INCOMPATIBLE_LICENSE|CVE|SPDX|ARCHIVER)[:=]'
bitbake -c populate_lic <recipe>
bitbake <image>
find tmp/deploy -maxdepth 4 -iname '*spdx*' -o -path '*licenses*'
```

## Review Rules

- `LIC_FILES_CHKSUM` is mandatory unless `LICENSE = "CLOSED"`.
- License checksum mismatch means upstream license text changed; inspect before updating the checksum.
- Keep commercial license acceptance explicit and narrow.
- Verify current release SBOM/CVE class names before recommending `create-spdx`, CVE classes, or output paths.
- Use archiver/copyleft flows when source offer obligations matter.
- Do not confuse build-time `DEPENDS` with packages included in final image license manifests.

## References

- Read [../../references/yocto/security-sbom.md](../../references/yocto/security-sbom.md).
- Read [../../references/bitbake/classes-core.md](../../references/bitbake/classes-core.md) for `license`, `archiver`, `create-spdx`, and release-sensitive security classes.
- Read [../../references/yocto/migration.md](../../references/yocto/migration.md) for SBOM/CVE release changes.

## Output

Answer with:

1. license/security artifact being debugged
2. release-sensitive class or variable to verify
3. exact metadata or policy fix
4. validation command and expected artifact
5. compliance caveat if legal interpretation is required
