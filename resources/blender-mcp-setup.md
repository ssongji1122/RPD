# Blender MCP + AI 연동 가이드
> Blender 5.1 / 4.x 기준 | 최종 업데이트: 2026-05-12

Blender를 AI(Claude, Gemini, Cursor 등)로 **자연어 제어**하기 위한 설치 가이드.

---

## 두 가지 설치 방법 비교

| 항목 | 방법 A: 공식 애드온 | 방법 B: 서드파티 애드온 (권장) |
|------|-------------------|-------------------------------|
| 제작자 | Blender Foundation | ahujasid (커뮤니티) |
| 지원 버전 | **5.1 이상만** | **4.x ~ 5.0 호환** |
| 설치 파일 | `mcp-0.3.0.zip` | `addon.py` |
| 다운로드 | [blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/) | [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) |
| 인터넷 허용 설정 | 필요 | 불필요 |
| 안정성 | 공식 지원 (출시 초기) | 커뮤니티 유지보수, 검증됨 |

> ✅ **방법 B 권장** — 공식 애드온이 나온 지 얼마 안 돼서 호환성이 아직 불안정해요.
> 두 방법 모두 `uvx blender-mcp` 브릿지와 포트 9876을 공유합니다.

---

## 0. MCP란?

**MCP(Model Context Protocol)** = AI가 외부 프로그램을 직접 제어할 수 있게 해주는 표준 규격

```
AI (Claude / Gemini / Cursor)
        ↕ MCP JSON-RPC
[uvx blender-mcp]  ← 브릿지
        ↕ TCP 소켓 (localhost:9876)
[Blender 애드온]
        ↕ bpy API
[Blender 씬]
```

한 번 설정하면 어떤 MCP 지원 AI에서든 Blender를 자연어로 제어할 수 있어요.

---

## 1. uv 설치 (공통)

**uv** = Python 프로그램을 빠르게 실행해주는 패키지 매니저. `blender-mcp` 실행에 필요해요.

**Mac**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# 또는 Homebrew: brew install uv
```

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**설치 확인** (터미널 닫았다가 다시 열고)
```bash
uv --version
```
`uv 0.x.x` 같은 버전 번호가 나오면 성공.

---

## 2. Blender 애드온 설치

### 방법 B: 서드파티 애드온 (권장, Blender 4.x ~ 5.0)

**B-1. addon.py 다운로드**
- [github.com/ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) 접속
- 초록색 **Code** 버튼 → **Download ZIP** → 압축 해제 → `addon.py` 파일 확인
- 또는 직접 다운로드: [addon.py raw 파일](https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py)

**B-2. Blender에 설치**
1. Blender 상단 메뉴 → **Edit** → **Preferences** → **Add-ons**
2. 우측 상단 **Install** 버튼 (Blender 4.x) 또는 **드롭다운 ▾ → Install from Disk** (Blender 5.0)
3. `addon.py` 선택 → 설치
4. 검색창에 `blender mcp` 입력 → **Interface: Blender MCP** 체크박스 켜기

**B-3. MCP 서버 시작**
1. 3D 뷰포트에서 **N** 키 → 우측 사이드바 표시
2. **BlenderMCP** 탭 클릭
3. **Start MCP Server** 버튼 클릭
4. 포트 9876에서 서버 시작 확인

---

### 방법 A: 공식 애드온 (Blender 5.1 이상)

**A-1. 파일 다운로드**
[blender.org/lab/mcp-server](https://www.blender.org/lab/mcp-server/) 에서 `mcp-0.3.0.zip` 다운로드

> drag & drop으로 설치할 경우 두 번 드래그 필요:
> 첫 번째 = Blender Lab repository 세팅, 두 번째 = MCP 애드온 설치

**A-2. Blender 5.1 실행 후 애드온 설치**
1. **Edit** → **Preferences** → **Add-ons**
2. 드롭다운 **▾** → **Install from Disk...** → `mcp-0.3.0.zip` 선택
3. 검색창에 `mcp` 입력 → **MCP** 체크박스 켜기

**A-3. 인터넷 허용 (필수)**
1. Preferences → **System** 탭
2. 하단 **Network** → **Allow Online Access** 체크
3. **Save Preferences**

> 이 설정 없으면 `"Online access must be enabled"` 오류 발생

**A-4. 서버 확인**
Add-ons 탭에서 MCP 항목 펼치기:
- Host: `localhost`, Port: `9876`, Auto Start: 체크
- Blender 하단 상태바에 `MCP server running on localhost:9876` 표시 → 성공

---

## 3. AI 클라이언트 연결 (공통)

방법 A/B 모두 동일한 방식으로 연결.

### Claude Code (터미널)
```bash
claude mcp add blender -s user -- uvx blender-mcp
```
`Added stdio MCP server blender` 메시지 → 성공

### Claude Desktop
`~/Library/Application Support/Claude/claude_desktop_config.json` (Mac)
`%APPDATA%\Claude\claude_desktop_config.json` (Windows)

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
Claude Desktop 재시작 → 우측 하단 망치 아이콘 확인

### Cursor / VS Code
`.cursor/mcp.json` 또는 `.vscode/mcp.json`:
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

### Gemini CLI
`~/.gemini/settings.json`:
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

---

## 4. 동작 확인

Blender가 켜져 있고 서버가 시작된 상태에서 AI에게:

```
"Blender에 빨간 구체를 하나 만들어줘"
"현재 씬에 있는 오브젝트 목록을 알려줘"
"카메라 위치를 x=5, y=-5, z=3으로 이동해줘"
```

AI가 Blender 화면을 직접 조작하면 성공 🎉

---

## AI 클라이언트별 지원 현황

| AI | MCP 지원 | 비고 |
|----|----------|------|
| Claude Code | ✅ 완전 지원 | 가장 안정적 |
| Cursor | ✅ 완전 지원 | VS Code 기반 |
| VS Code Copilot | ✅ 지원 | GitHub Copilot 필요 |
| Gemini CLI | ✅ 지원 | 무료 |
| ChatGPT (웹) | ❌ 미지원 | — |

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `Connection refused` | Blender 꺼짐 또는 서버 미시작 | Blender 실행 + 서버 시작 확인 |
| `Online access must be enabled` | 방법 A의 인터넷 허용 누락 | Preferences > System > Allow Online Access |
| AI에서 툴이 안 보임 | AI 클라이언트 재시작 필요 | 새 세션 열기 |
| `uvx` 명령 없음 | uv 미설치 또는 터미널 미재시작 | 터미널 닫았다가 다시 열기 |
| `command not found: claude` | Claude Code 미설치 | [claude.ai/code](https://claude.ai/code) |
| BlenderMCP 사이드바 탭 안 보임 | 애드온 활성화 안 됨 | Preferences > Add-ons 체크박스 확인 |

---

## 수업 활용 가이드

| 주차 | MCP 활용 내용 |
|------|--------------|
| Week 09 | MCP 설치 + 조명 자동 세팅 |
| Week 13 | 카메라·렌더 설정 자동화 |

---

## 참고 링크

- [Blender 공식 다운로드](https://www.blender.org/download/)
- [Blender MCP Server 공식 페이지](https://www.blender.org/lab/mcp-server/)
- [서드파티 blender-mcp (ahujasid)](https://github.com/ahujasid/blender-mcp)
- [uv 공식 문서](https://docs.astral.sh/uv/)
- [Model Context Protocol 공식](https://modelcontextprotocol.io/)
- [Claude Code](https://claude.com/code)
- [Claude 설치 + Blender MCP 설치 영상](https://www.youtube.com/watch?v=Xg20g0JgzsA)
- [Blender MCP로 레퍼런스 이미지 재현하기 (심화 가이드)](https://www.notion.so/35e54d6549718192b2abe6e1570df3f5)
