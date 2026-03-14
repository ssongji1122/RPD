# RPD 2026 Spring 수업자료 구현 계획

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Blender 5.0 + AI 도구 기반 15주 강의자료 (Markdown 강의노트 + Marp 슬라이드 + 과제안내)를 제작하고, 기존 Notion 자료와 통합한다.

**Architecture:** 프로젝트 루트에 주차별 폴더(weeks/)를 두고, 각 폴더에 lecture-note.md / slides.md / assignment.md 3파일을 배치한다. 공통 리소스(AI 도구 가이드, 단축키, MCP 설정)는 resources/에 분리한다. Marp 테마는 templates/에 둔다.

**Tech Stack:** Markdown, Marp (슬라이드), Blender 5.0, Notion API (기존 자료 참조)

---

## Phase 1: 프로젝트 기반 구조 (Foundation)

### Task 1: README.md 작성

**Files:**
- Create: `README.md`

**Step 1: README 작성**

과목 개요, 평가 기준, 주차별 링크, 사용 소프트웨어 목록을 포함하는 README를 작성한다.

내용:
- 과목명, 교수, 학기 정보
- 강의 목표 3가지
- 평가 기준 표
- 주차별 강의 링크 (weeks/ 폴더)
- 필수 소프트웨어: Blender 5.0
- AI 도구 목록 (무료 도구만)
- Discord 채널 안내

**Step 2: 커밋**

```bash
git add README.md && git commit -m "docs: add course README with overview and links"
```

---

### Task 2: syllabus.md 작성

**Files:**
- Create: `syllabus.md`

**Step 1: 마스터 실라버스 작성**

15주 커리큘럼을 표 형태로 정리한다. 각 주차의 주제, 내용, 과제, 사용 도구를 포함한다.

설계 문서의 Section 4 (주차별 커리큘럼)를 표 형태로 변환한다.

**Step 2: 커밋**

```bash
git add syllabus.md && git commit -m "docs: add 15-week syllabus"
```

---

### Task 3: Marp 테마 + 과제 템플릿

**Files:**
- Create: `templates/marp-theme.css`
- Create: `templates/assignment-template.md`

**Step 1: Marp CSS 테마 작성**

RPD 브랜딩 테마:
- 다크 모드 기반 (3D 작업 시 눈 피로 감소)
- 타이틀 슬라이드: 과목명 + 주차 + 날짜
- 코드 블록: 단축키 표시에 최적화
- 이미지: 전체 화면 이미지 슬라이드 지원
- 폰트: Pretendard (한국어) + JetBrains Mono (코드)

**Step 2: 과제 템플릿 작성**

공통 과제 양식:
- 주차/제목
- 제출 방법 (Discord 채널)
- 제출 형식
- 평가 기준
- 참고 자료

**Step 3: 커밋**

```bash
git add templates/ && git commit -m "feat: add Marp theme and assignment template"
```

---

## Phase 2: 공통 리소스 (Resources)

### Task 4: AI 도구 종합 가이드

**Files:**
- Create: `resources/ai-tools-guide.md`

**Step 1: AI 도구 가이드 작성**

설계 문서의 AI 도구 표를 확장하여 각 도구별로:
- 개요 (1~2문장)
- 가입/접속 방법
- 무료 티어 범위
- 수업 활용 방법
- 주의사항

영역별로 구분: 이미지 생성, 3D 생성, 텍스처, HDRI, 영상, BGM, 자동 리깅, AI 자동화(MCP)

**Step 2: 커밋**

```bash
git add resources/ai-tools-guide.md && git commit -m "docs: add comprehensive AI tools guide"
```

---

### Task 5: Blender 5.0 단축키 치트시트

**Files:**
- Create: `resources/blender-shortcuts.md`

**Step 1: 단축키 치트시트 작성**

Blender 5.0 기준 주요 단축키를 영역별로 정리:
- Navigation (뷰 조작)
- Selection (선택)
- Transform (이동/회전/스케일)
- Edit Mode
- Sculpt Mode
- Object Mode
- Animation
- Rendering

5.0에서 변경된 단축키 별도 표시.

**Step 2: 커밋**

```bash
git add resources/blender-shortcuts.md && git commit -m "docs: add Blender 5.0 shortcuts cheatsheet"
```

---

### Task 6: Blender MCP + Claude 설치 가이드

**Files:**
- Create: `resources/blender-mcp-setup.md`

**Step 1: MCP 설치 가이드 작성**

기존 Notion "Blender MCP 사용법" 페이지를 기반으로 Markdown으로 재작성.
Blender 5.0 호환성 확인 내용 추가.

Windows/Mac 양쪽 설치 절차:
1. 사전 준비물
2. uv/uvx 설치
3. Blender MCP 애드온 설치
4. Claude Desktop 설정
5. 연결 확인
6. 사용 예시
7. 트러블슈팅

**Step 2: 커밋**

```bash
git add resources/blender-mcp-setup.md && git commit -m "docs: add Blender MCP + Claude setup guide"
```

---

### Task 7: 참고 링크 모음

**Files:**
- Create: `resources/references.md`

**Step 1: 참고 링크 정리**

영역별 참고 링크:
- Blender 공식 문서/튜토리얼
- Poly Haven / ambientCG
- AI 도구 공식 사이트
- 기존 Notion 페이지 링크
- YouTube 튜토리얼 (기존 tutorial/ 폴더 영상 목록)

**Step 2: 커밋**

```bash
git add resources/references.md && git commit -m "docs: add reference links collection"
```

---

## Phase 3: 주차별 강의자료 - 전반부 (Week 1~7)

> 각 주차는 3개 파일(lecture-note.md, slides.md, assignment.md)을 포함한다.
> 아래는 각 주차의 핵심 내용만 기술한다. 모든 주차는 동일한 패턴을 따른다.

### Task 8: Week 01 - 오리엔테이션

**Files:**
- Create: `weeks/week01-orientation/lecture-note.md`
- Create: `weeks/week01-orientation/slides.md`
- Create: `weeks/week01-orientation/assignment.md`

**강의노트 내용:**
- 수업 소개: 목표, 평가, 일정, Discord 안내
- 2026 캐릭터 프로덕트 트렌드 소개
- Blender 5.0 설치 가이드 (Windows/Mac)
- AI 도구 소개: Mixboard, 나노바나나
- 실습: Mixboard로 무드보드 제작, 나노바나나로 캐릭터 컨셉 이미지 생성

**슬라이드:** 12장 (과목소개 4 + 트렌드 3 + 설치 2 + AI무드보드 3)

**과제:** 무드보드 Discord 제출 (이미지 2장 + 컨셉 한줄 설명)

**Step: 커밋**
```bash
git add weeks/week01-orientation/ && git commit -m "content: add Week 01 orientation materials"
```

---

### Task 9: Week 02 - Blender 인터페이스 + MCP

**Files:**
- Create: `weeks/week02-blender-basics/lecture-note.md`
- Create: `weeks/week02-blender-basics/slides.md`
- Create: `weeks/week02-blender-basics/assignment.md`

**강의노트 내용:**
- Blender 5.0 UI 구조 (Viewport, Outliner, Properties, Timeline)
- 5.0 UI 변경사항: pill 탭, 아이콘 변경, Workspace 변경
- 뷰 조작: 마우스 미들버튼, Numpad
- Transform: G(이동), R(회전), S(스케일) + 축 제한(X/Y/Z)
- Apply Transform (Ctrl+A) - 왜 중요한지
- Origin 설정 (Right-click > Set Origin)
- Pivot Point
- Blender MCP + Claude 설치 및 연결 (resources/blender-mcp-setup.md 참조)
- MCP 간단 테스트: "Create a cube and move it to (2, 0, 0)"

**기존 Notion 참조:** Blender 기초 튜토리얼, Transform/Origin, Blender MCP 사용법

**슬라이드:** 15장
**과제:** 기본 도형 5개 배치 스크린샷 + MCP 테스트 스크린샷

**Step: 커밋**
```bash
git add weeks/week02-blender-basics/ && git commit -m "content: add Week 02 Blender basics + MCP setup"
```

---

### Task 10: Week 03 - 기초 모델링 1

**Files:**
- Create: `weeks/week03-modeling-1/lecture-note.md`
- Create: `weeks/week03-modeling-1/slides.md`
- Create: `weeks/week03-modeling-1/assignment.md`

**강의노트 내용:**
- Primitive 종류 (Cube, Sphere, Cylinder, Cone, Torus 등)
- Object Mode vs Edit Mode (Tab)
- 선택 모드: Vertex(1) / Edge(2) / Face(3)
- 필수 도구: Extrude(E), Loop Cut(Ctrl+R), Inset(I), Bevel(Ctrl+B)
- 실습: 간단한 로봇 머리 형태 만들기 (Cube → Extrude → Loop Cut)

**슬라이드:** 12장
**과제:** 로봇/캐릭터 기본 형태 스크린샷

**Step: 커밋**
```bash
git add weeks/week03-modeling-1/ && git commit -m "content: add Week 03 basic modeling 1"
```

---

### Task 11: Week 04 - 기초 모델링 2

**Files:**
- Create: `weeks/week04-modeling-2/lecture-note.md`
- Create: `weeks/week04-modeling-2/slides.md`
- Create: `weeks/week04-modeling-2/assignment.md`

**강의노트 내용:**
- Modifier 개념: Non-destructive 워크플로우
- 핵심 Modifier: Subdivision Surface, Mirror, Solidify, Array
- Boolean 연산: Union, Difference, Intersect
- 실습: Mirror + Subdivision으로 대칭 로봇 바디 만들기

**슬라이드:** 12장
**과제:** Modifier 적용된 로봇/캐릭터 형태 스크린샷

**Step: 커밋**
```bash
git add weeks/week04-modeling-2/ && git commit -m "content: add Week 04 basic modeling 2 (Modifier)"
```

---

### Task 12: Week 05 - AI 3D 생성 + Sculpting + MCP

**Files:**
- Create: `weeks/week05-ai3d-sculpting/lecture-note.md`
- Create: `weeks/week05-ai3d-sculpting/slides.md`
- Create: `weeks/week05-ai3d-sculpting/assignment.md`

**강의노트 내용:**
- AI 3D 생성 도구 비교: Meshy AI vs Tripo AI vs Luma Genie
- 텍스트→3D / 이미지→3D 워크플로우
- Blender 임포트: 스케일 조정, 원점 설정, 메쉬 정리
- Sculpt Mode 기초: Draw, Clay Strips, Smooth, Grab, Mask
- MCP 활용: Claude에게 기본 씬(바닥, 조명) 자동 생성 요청
- 실습: Meshy로 로봇 3D 생성 → Blender 임포트 → Sculpt로 디테일 추가

**기존 Notion 참조:** Sculpting Tutorial

**슬라이드:** 15장
**과제:** AI 3D + Blender Sculpt 작업 이미지

**Step: 커밋**
```bash
git add weeks/week05-ai3d-sculpting/ && git commit -m "content: add Week 05 AI 3D + Sculpting + MCP"
```

---

### Task 13: Week 06 - Material & Shader Node

**Files:**
- Create: `weeks/week06-material/lecture-note.md`
- Create: `weeks/week06-material/slides.md`
- Create: `weeks/week06-material/assignment.md`

**강의노트 내용:**
- Material 생성 및 할당
- Principled BSDF: Base Color, Metallic, Roughness, Specular
- Thin Film Iridescence (Blender 5.0 신기능) - 로봇 금속 표면에 활용
- Shader Node Editor 기초
- Poly Haven / BlenderKit에서 텍스처 가져오기
- 실습: 로봇에 다양한 재질 적용 (금속, 플라스틱, 유리)

**기존 Notion 참조:** Material Basic, Material Delete, Material Node

**슬라이드:** 13장
**과제:** 로봇/캐릭터 재질 적용 이미지

**Step: 커밋**
```bash
git add weeks/week06-material/ && git commit -m "content: add Week 06 Material & Shader Node"
```

---

### Task 14: Week 07 - UV Unwrapping + AI Texture

**Files:**
- Create: `weeks/week07-uv-texture/lecture-note.md`
- Create: `weeks/week07-uv-texture/slides.md`
- Create: `weeks/week07-uv-texture/assignment.md`

**강의노트 내용:**
- UV 개념: 3D → 2D 전개
- Seam 설정 (Mark Seam) 전략
- Unwrap 방법들: Unwrap, Smart UV Project, Cube Projection
- UV Editor 사용법
- Texture 이미지 적용
- AI 텍스처 생성: Meshy AI Texture / 나노바나나로 패턴 생성
- Texture Painting 기초
- 실습: 로봇에 UV 적용 → AI 텍스처 + 수동 페인팅

**기존 Notion 참조:** UV Unwrapping, Texture Painting, Texture Save/Export

**슬라이드:** 14장
**과제:** 텍스처 적용된 로봇 렌더

**Step: 커밋**
```bash
git add weeks/week07-uv-texture/ && git commit -m "content: add Week 07 UV Unwrapping + AI Texture"
```

---

## Phase 4: 중간고사 + 후반부 (Week 8~15)

### Task 15: Week 08 - 중간고사

**Files:**
- Create: `weeks/week08-midterm/lecture-note.md`
- Create: `weeks/week08-midterm/assignment.md`

**내용:**
- 중간 프로젝트 제출 가이드
- 평가 루브릭 (모델링 완성도, 텍스처 품질, 창의성, 기술 활용)
- 발표 가이드 (시간, 형식, 발표 순서)
- 제출 체크리스트

(슬라이드 없음 - 발표 수업)

**Step: 커밋**
```bash
git add weeks/week08-midterm/ && git commit -m "content: add Week 08 midterm project guide + rubric"
```

---

### Task 16: Week 09 - Lighting + MCP 조명 연출

**Files:**
- Create: `weeks/week09-lighting/lecture-note.md`
- Create: `weeks/week09-lighting/slides.md`
- Create: `weeks/week09-lighting/assignment.md`

**강의노트 내용:**
- 조명 종류: Point, Sun, Spot, Area
- 3-Point Lighting: Key, Fill, Back
- HDRI 환경 조명 (World > Environment Texture)
- Poly Haven HDRI 활용
- Blockade Labs Skybox: 텍스트→360 HDRI 생성
- Blender 5.0 HDR 색상 관리: AgX vs ACES 비교
- Claude MCP 활용: 다양한 조명 분위기 자동 연출

**기존 Notion 참조:** Lighting

**슬라이드:** 13장
**과제:** 3가지 조명 환경 렌더 이미지

**Step: 커밋**
```bash
git add weeks/week09-lighting/ && git commit -m "content: add Week 09 Lighting + HDRI + MCP"
```

---

### Task 17: Week 10 - Animation 기초

**Files:**
- Create: `weeks/week10-animation/lecture-note.md`
- Create: `weeks/week10-animation/slides.md`
- Create: `weeks/week10-animation/assignment.md`

**강의노트 내용:**
- Timeline 사용법
- Keyframe 삽입 (I) / 삭제 (Alt+I)
- 오브젝트 애니메이션: Location, Rotation, Scale
- Graph Editor 기초: 이징 커브
- 재생 및 프레임 범위 설정
- 실습: 로봇이 3~5초간 걸어가거나 손 흔드는 간단한 애니메이션

**기존 Notion 참조:** Animation

**슬라이드:** 12장
**과제:** 3~5초 간단한 움직임 애니메이션

**Step: 커밋**
```bash
git add weeks/week10-animation/ && git commit -m "content: add Week 10 Animation basics"
```

---

### Task 18: Week 11 - Rigging 기초

**Files:**
- Create: `weeks/week11-rigging/lecture-note.md`
- Create: `weeks/week11-rigging/slides.md`
- Create: `weeks/week11-rigging/assignment.md`

**강의노트 내용:**
- Armature 생성 (Shift+A > Armature)
- Bone 구조: Parent-Child 관계
- IK (Inverse Kinematics) vs FK (Forward Kinematics)
- 캐릭터 리깅 vs 기계 오브젝트 리깅 차이
- Weight Painting 기초
- Pose Mode
- 실습: 간단한 로봇 팔/다리 리깅

**기존 Notion 참조:** Basic Rigging (Character + Mechanical), Weight Painting

**슬라이드:** 14장
**과제:** 기초 리깅 적용 실습

**Step: 커밋**
```bash
git add weeks/week11-rigging/ && git commit -m "content: add Week 11 Rigging basics"
```

---

### Task 19: Week 12 - AI 활용 리깅 (Mixamo)

**Files:**
- Create: `weeks/week12-mixamo/lecture-note.md`
- Create: `weeks/week12-mixamo/slides.md`
- Create: `weeks/week12-mixamo/assignment.md`

**강의노트 내용:**
- Mixamo 소개 및 가입 (Adobe 무료 계정)
- 모델 업로드 및 자동 리깅
- 애니메이션 라이브러리 탐색 및 적용
- FBX 내보내기 → Blender 임포트
- Blender에서 Mixamo 애니메이션 편집
- NLA Editor 기초: 애니메이션 블렌딩

**기존 Notion 참조:** Retargetting_Mixamo

**슬라이드:** 12장
**과제:** Mixamo 리깅/애니메이션 적용

**Step: 커밋**
```bash
git add weeks/week12-mixamo/ && git commit -m "content: add Week 12 Mixamo rigging"
```

---

### Task 20: Week 13 - AI 영상/사운드 + 렌더링 + MCP

**Files:**
- Create: `weeks/week13-rendering-ai/lecture-note.md`
- Create: `weeks/week13-rendering-ai/slides.md`
- Create: `weeks/week13-rendering-ai/assignment.md`

**강의노트 내용:**
- Camera 설정: Focal Length, Depth of Field, 카메라 애니메이션
- Eevee vs Cycles 렌더러 비교
- Blender 5.0 색상 관리: AgX, ACES 1.3/2.0
- 렌더 설정: 해상도, 샘플링, 출력 포맷
- AI 영상 생성: Kling AI / Veo (렌더 이미지→비디오)
- AI BGM 생성: Suno AI / ElevenLabs Music
- MCP 활용: Claude로 카메라/렌더 설정 자동화
- Compositor: 기본 포스트 프로세싱

**기존 Notion 참조:** Rendering, Camera Setting, Render & Export, Eevee 문제해결

**슬라이드:** 15장
**과제:** 렌더링 이미지 + AI 영상/사운드 테스트

**Step: 커밋**
```bash
git add weeks/week13-rendering-ai/ && git commit -m "content: add Week 13 Rendering + AI video/sound"
```

---

### Task 21: Week 14 - 최종 프로젝트 제작

**Files:**
- Create: `weeks/week14-final-project/lecture-note.md`
- Create: `weeks/week14-final-project/assignment.md`

**내용:**
- 최종 프로젝트 요구사항 정리
- 프로젝트 체크리스트 (모델링→텍스처→리깅→애니메이션→렌더링→영상)
- 피드백 가이드 (자가 체크리스트)
- 개별 피드백 시간 운영 방법

(슬라이드 없음 - 작업 시간)

**Step: 커밋**
```bash
git add weeks/week14-final-project/ && git commit -m "content: add Week 14 final project guide"
```

---

### Task 22: Week 15 - 기말고사

**Files:**
- Create: `weeks/week15-final/lecture-note.md`
- Create: `weeks/week15-final/assignment.md`

**내용:**
- 최종 프로젝트 제출 가이드
- 기말 평가 루브릭 (모델링, 텍스처, 리깅, 애니메이션, 렌더링, AI 활용, 창의성, 발표)
- 발표 가이드 (시간, 형식)
- 포트폴리오 정리 팁

(슬라이드 없음 - 발표 수업)

**Step: 커밋**
```bash
git add weeks/week15-final/ && git commit -m "content: add Week 15 final presentation guide + rubric"
```

---

## Phase 5: Notion 연동

### Task 23: Notion 주차별 구조 재편성

기존 Notion RPD 페이지를 주차별로 재구성한다.
Notion API를 통해 주차별 하위 페이지를 만들고, 기존 페이지를 해당 주차 아래로 이동한다.

**작업 내용:**
1. Notion RPD 페이지 아래에 "2026 Spring" 섹션 추가
2. 주차별 하위 페이지 생성 (Week 01 ~ Week 15)
3. 기존 튜토리얼 페이지들을 해당 주차 아래로 링크
4. 각 주차 페이지에 Git 강의노트 링크 포함

**Step: 확인**
Notion 페이지 구조가 올바르게 반영되었는지 확인한다.

---

## 실행 순서 요약

| Phase | Tasks | 예상 분량 | 우선순위 |
|-------|-------|---------|---------|
| 1. Foundation | Task 1~3 (README, syllabus, templates) | 3개 파일 | 최우선 |
| 2. Resources | Task 4~7 (AI가이드, 단축키, MCP, 참고링크) | 4개 파일 | 높음 |
| 3. 전반부 | Task 8~14 (Week 1~7) | 21개 파일 | 높음 |
| 4. 후반부 | Task 15~22 (Week 8~15) | 19개 파일 | 중간 |
| 5. Notion | Task 23 (Notion 재구성) | Notion API | 낮음 |

**총 산출물:** ~47개 Markdown 파일 + 1 CSS + Notion 구조 재편성
