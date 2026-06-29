# Yocto Agent Skills

공식 문서 우선 방식의 Yocto Project / BitBake 전용 AI agent skills입니다.

Yocto는 릴리즈별 차이가 크고 설정 계층이 깊어서 일반 LLM이 쉽게 틀립니다. 이 저장소는 agent가 공식 문서를 올바르게 찾고, BitBake 실패를 디버깅하고, recipe와 layer를 리뷰하고, image/rootfs, BSP/kernel, security/SBOM 문제까지 다루도록 돕는 focused skills를 제공합니다.

English documentation: [README.md](README.md)

## Skills

- `skills/yocto-doc-router`: Yocto, OpenEmbedded, BitBake 공식 문서를 릴리즈 기준으로 라우팅합니다.
- `skills/bitbake-debug`: BitBake task/log/rootfs/package/provider 실패를 디버깅합니다.
- `skills/yocto-recipe-review`: recipe, bbappend, bbclass, dependency, packaging, licensing, override syntax를 리뷰합니다.
- `skills/yocto-layer-review`: layer.conf, layer compatibility, priority, dependency, provider, bbappend matching을 리뷰합니다.
- `skills/yocto-image-rootfs`: image recipe, package name, `IMAGE_INSTALL`, `IMAGE_FEATURES`, `do_rootfs`, pkgdata, package manager 문제를 다룹니다.
- `skills/yocto-bsp-kernel`: machine config, BSP layer, kernel provider, devicetree, defconfig, U-Boot, deploy artifact를 다룹니다.
- `skills/yocto-security-sbom`: license metadata, CVE, SPDX/SBOM, archiver/copyleft, compliance artifact를 다룹니다.

root `SKILL.md`는 repo 전체를 하나의 skill로 설치하는 host를 위한 호환 router로 남겨뒀습니다.

## 도와주는 작업

- BitBake task 실패 디버깅: `do_fetch`, `do_unpack`, `do_patch`, `do_configure`, `do_compile`, `do_install`, `do_package`, `do_package_qa`, `do_rootfs`, `do_image`
- `.bb`, `.bbappend`, `.bbclass`, image recipe, machine config, distro config, `layer.conf` 작성과 리뷰
- 최신 BitBake override 문법 정리: `VAR:append`, `FILES:${PN}`, `RDEPENDS:${PN}`, task override, package override
- layer, bbappend, provider 선택, package split, rootfs 실패, QA 메시지, kernel/BSP metadata, image 구성 리뷰
- `DEPENDS`와 `RDEPENDS`, recipe name과 package name, `SRCREV`, `LIC_FILES_CHKSUM`, `INSANE_SKIP`, host contamination, sstate cleanup 관련 흔한 AI 실수 줄이기

## 설치

collection-aware agent에서는 `skills/` 아래의 개별 skill 폴더를 설치하는 방식을 권장합니다.

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
for skill in yocto-doc-router bitbake-debug yocto-recipe-review yocto-layer-review yocto-image-rootfs yocto-bsp-kernel yocto-security-sbom; do
  ln -s "$(pwd)/skills/$skill" "${CODEX_HOME:-$HOME/.codex}/skills/$skill"
done
```

repo 전체를 하나의 skill로 설치하는 host에서는 root를 설치하면 됩니다.

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)" "${CODEX_HOME:-$HOME/.codex}/skills/yocto-agent-skills"
```

## 예시 프롬프트

```text
Use bitbake-debug to diagnose this do_rootfs failure.
```

```text
Use yocto-recipe-review to review this recipe and modernize the override syntax.
```

```text
Use yocto-layer-review to explain why this bbappend is not being applied.
```

```text
Use yocto-image-rootfs to find why my package is not in the final image.
```

```text
Use yocto-bsp-kernel to debug why my devicetree is missing from deploy/images.
```

```text
Use yocto-security-sbom to review this license checksum and SBOM setup.
```

## 구성

- `SKILL.md`: root 호환 router
- `skills/*/SKILL.md`: focused installable skills
- `references/shared/official-doc-map.md`: 문제 유형별 공식 Yocto/BitBake 문서 라우팅
- `references/shared/yocto-field-guide.md`: recipe, layer, task, QA, image, provider, BSP/kernel 작업용 압축 가이드
- `references/bitbake/variables-core.md`: agent가 자주 헷갈리는 핵심 변수
- `references/bitbake/classes-core.md`: 자주 쓰는 class와 리뷰 규칙
- `references/bitbake/tasks-reference.md`: task 단위 디버깅 reference
- `references/yocto/qa-errors.md`: 흔한 QA error 패턴
- `references/yocto/migration.md`: 릴리즈별 migration 체크
- `references/yocto/image-rootfs.md`: image/rootfs 문제 해결
- `references/yocto/bsp-kernel.md`: BSP/kernel 문제 해결
- `references/yocto/security-sbom.md`: security, license, CVE, SBOM 흐름
- `examples/`: 현실적인 실패 예시와 기대 답변 패턴
- `evals/prompts.md`: 수동 forward-test 프롬프트
- `agents/openai.yaml`: 호환 skill host용 UI metadata

## 라이선스

MIT
