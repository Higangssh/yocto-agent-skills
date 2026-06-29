# Yocto Agent Skills

공식 문서 우선 방식의 Yocto Project / BitBake 전용 AI agent skills입니다.

Yocto는 릴리즈별 차이가 크고 설정 계층이 깊어서 일반 LLM이 쉽게 틀립니다. 이 skills는 agent가 먼저 대상 릴리즈를 확인하고, 공식 Yocto/BitBake 문서로 질문을 라우팅하고, 실제 metadata와 build log를 근거로 수정안을 내도록 강제합니다.

English documentation: [README.md](README.md)

## 도와주는 작업

- BitBake task 실패 디버깅: `do_fetch`, `do_unpack`, `do_patch`, `do_configure`, `do_compile`, `do_install`, `do_package`, `do_package_qa`, `do_rootfs`, `do_image`
- `.bb`, `.bbappend`, `.bbclass`, image recipe, machine config, distro config, `layer.conf` 작성과 리뷰
- 최신 BitBake override 문법 정리: `VAR:append`, `FILES:${PN}`, `RDEPENDS:${PN}`, task override, package override
- layer, bbappend, provider 선택, package split, rootfs 실패, QA 메시지, kernel/BSP metadata, image 구성 리뷰
- `DEPENDS`와 `RDEPENDS`, recipe name과 package name, `SRCREV`, `LIC_FILES_CHKSUM`, `INSANE_SKIP`, host contamination, sstate cleanup 관련 흔한 AI 실수 줄이기

## 설치

이 repo 폴더를 사용하는 agent의 skills 디렉토리에 복사하거나 symlink로 연결하면 됩니다.

예시:

```bash
# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)" "${CODEX_HOME:-$HOME/.codex}/skills/yocto-agent-skills"

# Claude Code / 다른 SKILL.md 호환 agent
# 이 폴더를 해당 도구의 skills 디렉토리에 복사하거나 symlink로 연결하세요.
```

설치 후 Yocto Project나 BitBake 작업에서 Yocto Agent Skills를 사용하라고 요청하면 됩니다.

## 예시 프롬프트

```text
Use the Yocto Agent Skills to debug this do_rootfs failure.
```

```text
Use the Yocto Agent Skills to review this recipe and modernize the override syntax.
```

```text
Use the Yocto Agent Skills to explain why this bbappend is not being applied.
```

## 구성

- `SKILL.md`: trigger metadata와 핵심 agent workflow
- `references/official-doc-map.md`: 문제 유형별 공식 Yocto/BitBake 문서 라우팅
- `references/yocto-field-guide.md`: recipe, layer, task, QA, image, provider, BSP/kernel 작업용 압축 가이드
- `agents/openai.yaml`: 호환 skill host용 UI metadata

## 라이선스

MIT
