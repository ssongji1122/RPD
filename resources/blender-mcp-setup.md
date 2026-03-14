# Blender MCP + Claude 설치 및 연결 가이드

## 개요

Blender MCP는 Claude AI가 Blender를 직접 제어할 수 있게 해주는 도구입니다. 텍스트 프롬프트로 3D 모델 생성, 씬 구성, 조명 설정, 렌더링 등을 자동화할 수 있습니다.

## 사전 준비물

- Blender 5.0 이상
- Claude Desktop 앱
- Python 3.10 이상
- uv 또는 uvx 패키지

## Windows 설치

### Step 1: Python 설치

- python.org에서 Python 3.10+ 다운로드
- 설치 시 "Add Python to PATH" 체크 필수

### Step 2: uv 설치

```
pip install uv
```

### Step 3: Blender MCP 애드온 설치

1. GitHub에서 addon.py 다운로드 (https://github.com/ahujasid/blender-mcp)
2. Blender > Edit > Preferences > Add-ons > Install
3. addon.py 선택 후 체크박스 활성화

### Step 4: Claude Desktop 설정

1. Claude Desktop > File > Settings > Developer > Edit Config
2. `%APPDATA%\Claude\claude_desktop_config.json` 파일에 추가:

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

### Step 5: 연결 확인

1. Blender에서 N키 > BlenderMCP 탭 > Start MCP Server
2. Claude Desktop 재시작
3. Claude 우측 하단에 망치 아이콘 확인

## Mac 설치

### Step 1: uv 설치

```
brew install uv
```

또는

```
pip install uv
```

### Step 2: Blender MCP 애드온 설치

(Windows와 동일)

### Step 3: Claude Desktop 설정

1. Claude Desktop > File > Settings > Developer > Edit Config
2. `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

### Step 4: 연결 확인

(Windows와 동일)

## 사용 예시

### 기본 오브젝트 생성

> "Create a red cube at position (2, 0, 0) with size 1"

### 씬 구성

> "Create a simple studio setup with a floor plane, 3-point lighting, and a camera pointing at the origin"

### 조명 연출

> "Add warm sunset HDRI lighting to the scene and set the camera angle to 45 degrees"

### 렌더링

> "Render the current scene at 1920x1080 using Eevee with 64 samples"

## 수업 활용 가이드

| 주차 | MCP 활용 내용 |
|------|------------|
| Week 02 | 설치 및 연결, 간단한 오브젝트 생성 테스트 |
| Week 05 | 기본 씬 자동 구성 (바닥, 조명, 카메라) |
| Week 09 | 다양한 조명 분위기 자동 연출 (스튜디오, 일몰, 야간 등) |
| Week 13 | 카메라/렌더 설정 자동화 |

## 트러블슈팅

### 연결이 안 될 때

1. Blender에서 MCP Server가 Started 상태인지 확인
2. Claude Desktop을 완전히 종료 후 재시작
3. config.json 파일 경로와 JSON 형식 확인
4. uv/uvx가 정상 설치되었는지 터미널에서 `uvx --version` 실행

### Claude에서 Blender 도구가 보이지 않을 때

1. Claude 앱 우측 하단 망치 아이콘 확인
2. 없으면 Claude Desktop 재시작
3. config.json에 오타가 없는지 확인

### Blender 5.0 호환성

- Blender MCP 애드온은 Blender 3.0+ 호환
- Blender 5.0에서도 정상 작동 확인됨
- 5.0에서 UI가 변경되었지만 MCP 탭 위치(N키 사이드바)는 동일

## 참고 링크

- Blender MCP GitHub: https://github.com/ahujasid/blender-mcp
- Claude Desktop: https://claude.ai/download
