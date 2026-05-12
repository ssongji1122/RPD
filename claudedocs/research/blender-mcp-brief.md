# 리서치 브리프: Blender MCP (Model Context Protocol)
> 생성일: 2026-05-12 | 조사 기준: 2026-05 현재

---

## 1. 개요

Claude AI와 Blender를 연결하여 **자연어로 3D 장면을 제어**하는 기술.
두 가지 경로가 존재하며 성격이 다름:

| 구분 | 공식 Blender Lab MCP | 커뮤니티 blender-mcp (ahujasid) |
|------|---------------------|-------------------------------|
| 제작 | Blender Foundation | ahujasid (개인, 오픈소스) |
| 공식 여부 | ✅ Blender 공식 | ⚠️ Anthropic과 Blender가 공식 파트너십 후 사실상 인정 |
| 문서 | [blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/) | [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) |
| 지원 클라이언트 | .mcpb 파일 지원 신규 클라이언트 | Claude Desktop, Claude Code, Cursor, VSCode |
| Blender 요구 버전 | 3.6+ | 3.0+ |
| Python | - | 3.10+ |

### 배경 타임라인

- **2025-03** ahujasid/blender-mcp 공개 → 커뮤니티에서 폭발적 반응
- **2026-04-28** Anthropic "Claude for Creative Work" 발표 — Blender Foundation과 공식 파트너십, Anthropic이 Blender Python API 개발 기부
- **2026-05 현재** Blender Lab에서 공식 MCP 서버 페이지 운영 중

---

## 2. 핵심 기능 (ahujasid/blender-mcp 기준)

| 기능 | 설명 |
|------|------|
| 오브젝트 생성/수정/삭제 | 자연어로 메시 생성, 위치/크기/회전 변경 |
| 재질 적용 | 색상, 재질 노드 제어 |
| 장면 분석 | 장면 전체 구조 읽기 및 디버깅 |
| Python 코드 실행 | `execute_blender_code` 툴 — Blender Python API 직접 실행 |
| Poly Haven 에셋 | 무료 HDRI/텍스처/모델 자동 다운로드 |
| Hyper3D Rodin | AI 생성 3D 모델 가져오기 |
| 뷰포트 스크린샷 | Claude가 현재 Blender 화면을 봄 |

---

## 3. 아키텍처

```
Claude (클라이언트) ←→ MCP Server (Python, 포트 9876) ←→ Blender Addon (addon.py, Socket Server)
```

- **Blender Addon**: Blender 안에서 소켓 서버 실행
- **MCP Server**: MCP 프로토콜을 소켓으로 번역
- 환경변수: `BLENDER_HOST` (기본 localhost), `BLENDER_PORT` (기본 9876)

---

## 4. 설치 방법 (ahujasid/blender-mcp, Claude Desktop 기준)

### Step 1 — Blender Addon 설치
1. [GitHub Release](https://github.com/ahujasid/blender-mcp/releases)에서 `addon.py` 다운로드
2. Blender → Edit > Preferences > Add-ons > Install → `addon.py` 선택 → 활성화
3. 사이드바(N 키) > BlenderMCP 탭 > "Start MCP Server" 클릭

### Step 2 — Claude Desktop 설정
`~/Library/Application Support/Claude/claude_desktop_config.json` 편집:

```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

Claude Desktop 재시작 → 연결 확인.

### Claude Code CLI 사용 시
```bash
claude mcp add blender -- uvx blender-mcp
```

### 요구사항
- `uv` 패키지 매니저 설치 필수 (`brew install uv` 또는 [astral.sh/uv](https://astral.sh/uv))

---

## 5. 주의사항 🔴

| 항목 | 내용 |
|------|------|
| 코드 실행 위험 | `execute_blender_code`는 가드 없이 Python 실행 → **작업 전 저장 필수** |
| 보안 | Blender 공식 MCP: "민감한 정보 없는 환경에서 사용 권장" |
| 텔레메트리 | ahujasid/blender-mcp: 익명화된 텔레메트리 수집, `DISABLE_TELEMETRY=1`로 비활성화 가능 |
| 비공식 사이트 | blender-mcp.com, blendermcp.org 등은 공식 아님 — **ahujasid GitHub이 원본** |

---

## 6. 공식 소스

| 소스 | URL | 설명 |
|------|-----|------|
| Blender Lab 공식 MCP 페이지 | [blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/) | Blender Foundation 공식 |
| Anthropic 발표 | [anthropic.com/news/claude-for-creative-work](https://www.anthropic.com/news/claude-for-creative-work) | 2026-04-28 파트너십 공식 발표 |
| ahujasid GitHub | [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) | 가장 널리 쓰이는 구현체 (v1.5.5) |
| MCP 공식 프로토콜 문서 | [modelcontextprotocol.io](https://modelcontextprotocol.io/) | MCP 표준 스펙 |
| Blender Artists 커뮤니티 | [blenderartists.org/t/from-blender-mcp-to-3d-agent…](https://blenderartists.org/t/from-blender-mcp-to-3d-agent-anthropic-partners-with-blender-claude-ai-connector-now-official/1639106) | 파트너십 커뮤니티 반응 |

---

## 7. 추천 영상

| 영상 | 링크 | 내용 |
|------|------|------|
| Blender MCP Full Tutorial | [youtube.com/watch?v=UdsC3fqBz6Q](https://www.youtube.com/watch?v=UdsC3fqBz6Q) | Claude로 3D 장면 생성 전체 과정 (2025-03-20) |
| Step-by-Step Setup Guide | [youtube.com/watch?v=8CiU6Bjxps8](https://www.youtube.com/watch?v=8CiU6Bjxps8) | Claude Desktop + Blender 자동화 설치 (2025-03-16) |
| Claude Code + Blender MCP | [youtube.com/watch?v=fsLkJNEtsTw](https://www.youtube.com/watch?v=fsLkJNEtsTw) | Claude Code CLI로 Blender 제어 |
| ChatGPT Blender MCP | [youtube.com/watch?v=mnQrG_diYmw](https://www.youtube.com/watch?v=mnQrG_diYmw) | ChatGPT 연동 (참고용) |
| MCP Tutorial 플레이리스트 | [youtube.com/playlist?list=PLXBVh4y1Y6E3…](https://www.youtube.com/playlist?list=PLXBVh4y1Y6E3sxwqRH-BE0_UaUJhfVgao) | MCP 전반 튜토리얼 시리즈 |

---

## 8. 한국어 리소스

| 소스 | URL |
|------|-----|
| 설치 방법 단계별 가이드 | [onedollarvps.com/blogs/how-to-install-blender-mcp](https://onedollarvps.com/blogs/how-to-install-blender-mcp) |
| Claude MCP 추천 7종 가이드 | [goldenrabbit.co.kr/articles/ugC8rmSLpFfoJPnnRVUZ](https://goldenrabbit.co.kr/articles/ugC8rmSLpFfoJPnnRVUZ) |
| AI 엔지니어를 위한 완벽 가이드 | [skywork.ai (한국어)](https://skywork.ai/skypage/ko/MCP-Server-Blender-AI-%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A5%BC-%EC%9C%84%ED%95%9C-%EC%99%84%EB%B2%BD-%EA%B0%80%EC%9D%B4%EB%93%9C/1971402775242076160) |
| Vagon 설정 가이드 | [vagon.io/blog/how-to-use-blender-mcp-with-anthropic-claude-ai](https://vagon.io/blog/how-to-use-blender-mcp-with-anthropic-claude-ai) |

---

## 9. RPD 교육 활용 메모

- MCP 연동은 **Blender Python API 기초 이해 후**에 소개하면 효과적
- "Claude가 실제로 bpy 코드를 생성해서 실행한다"는 원리 설명 필요
- `execute_blender_code` 위험성 → 학생에게 **항상 저장 후 실행** 습관 강조
- 교안에서 소개할 경우: 공식 Blender Lab MCP + ahujasid/blender-mcp 둘 다 언급
