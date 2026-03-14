# RPD (Robot Product Design) 2026 Spring - 커리큘럼 & 수업자료 설계

> 인하대학교 디자인테크놀로지학과 | 송지희 교수
> 작성일: 2026-02-26

## 1. 과목 개요

- **과목명:** 로봇프러덕트 디자인 (Robot Product Design)
- **학점:** 3.0 / 절대평가
- **시간:** 화 10~15교시 (60주년-908)
- **목표:** Blender 5.0 + AI 도구를 활용한 3D 캐릭터/로봇 제품 디자인
- **진행방식:** 이론 30% + 실습 70%
- **평가:** 중간 35% / 기말 35% / 과제 20% / 출석 10%

## 2. 소프트웨어 기준

### Blender 5.0 (2025.11 릴리즈)
- 현재 안정 버전 5.0.1 기준으로 모든 자료 작성
- 5.0 주요 변경사항 반영:
  - HDR/Wide-gamut 네이티브 색상 관리 (ACES 1.3/2.0 뷰)
  - UI 변경 (pill 탭, 아이콘 플립, 300+ 테마 설정 통합)
  - 단축키 이동 (Collection 가시성 → Outliner)
  - Compositor modifier in Sequencer
  - Thin Film Iridescence (Principled BSDF)
  - Compositing/Rendering Workspace 제거 → General 통합

### AI 도구 (모두 무료/무료티어)

| 영역 | 도구 | 무료 조건 |
|------|------|---------|
| 무드보드 | Mixboard (Google Labs) | 완전 무료 |
| 컨셉 이미지 | 나노바나나 (Gemini 2.5 Flash) | 무료 사용 가능 |
| 보조 이미지 | ChatGPT (DALL-E) | 무료 계정 |
| AI 3D 생성 | Meshy AI | 무료 크레딧 |
| AI 3D 보조 | Tripo AI | 넉넉한 무료 크레딧 |
| AI 3D 보조 | Luma Genie | 무료 티어 |
| PBR 텍스처 | Poly Haven | 완전 무료 (CC0) |
| PBR 텍스처 | ambientCG | 완전 무료 (CC0) |
| AI HDRI | Blockade Labs Skybox | 무료 티어 |
| HDRI 라이브러리 | Poly Haven HDRI | 완전 무료 |
| AI 영상 | Kling AI | 매일 로그인 크레딧 |
| AI 영상 | Veo (Gemini 무료) | 기본 제공 |
| AI BGM | Suno AI | 하루 몇 곡 무료 |
| AI BGM 보조 | ElevenLabs Music | 무료 티어 |
| 자동 리깅 | Mixamo | 완전 무료 (Adobe 계정) |
| AI 자동화 | Blender MCP + Claude | 무료 (Claude 무료 계정) |

## 3. 프로젝트 구조

```
RPD/
├── README.md                    # 과목 개요, 평가기준
├── syllabus.md                  # 주차별 커리큘럼 마스터 문서
├── weeks/
│   ├── week01-orientation/
│   │   ├── lecture-note.md      # 상세 강의노트 (한국어 + 영어 용어)
│   │   ├── slides.md            # Marp 슬라이드 (수업 프레젠테이션용)
│   │   └── assignment.md        # 과제 안내
│   ├── week02-blender-basics/
│   │   └── ...
│   └── ... (week03 ~ week15)
├── resources/
│   ├── ai-tools-guide.md        # AI 도구 종합 가이드
│   ├── blender-shortcuts.md     # Blender 5.0 단축키 치트시트
│   ├── blender-mcp-setup.md     # Blender MCP + Claude 설치 가이드
│   └── references.md            # 참고 링크 모음
├── templates/
│   ├── marp-theme.css           # 커스텀 슬라이드 테마 (RPD 브랜딩)
│   └── assignment-template.md   # 과제 템플릿
└── docs/plans/                  # 설계 문서
```

## 4. 주차별 커리큘럼

### Week 01: 오리엔테이션, Blender 설치, 컨셉 설정
- **이론:** 수업 목표/평가/일정, 2026 캐릭터 프로덕트 트렌드
- **실습:** Blender 5.0 설치, Mixboard+나노바나나로 무드보드 제작
- **과제:** 무드보드 Discord 제출
- **기존 Notion 자료:** 없음 (신규 제작)

### Week 02: Blender 인터페이스 및 기초 + MCP 설정
- **이론:** Blender 5.0 UI (Viewport, Outliner, Properties), 뷰 조작
- **실습:** Transform, Apply Transform, Origin, Pivot Point
- **추가:** Blender MCP + Claude 설치 및 연결 (Windows/Mac)
- **과제:** 기본 도형 배치 + MCP 간단 테스트
- **기존 Notion 자료:** Blender 기초 튜토리얼, Transform/Origin (5.0 업데이트 필요)
- **기존 Notion 자료:** Blender MCP 사용법 (그대로 활용)

### Week 03: 기초 모델링 1 - Edit Mode
- **이론:** Primitive, Edit Mode, 선택 모드 (Vertex/Edge/Face)
- **실습:** Extrude, Loop Cut, Inset, Bevel로 로봇 기본 형태
- **과제:** 로봇/캐릭터 기본 형태 스크린샷
- **기존 Notion 자료:** Blender 기초 튜토리얼 일부 (로봇 특화로 재작성)

### Week 04: 기초 모델링 2 - Modifier
- **이론:** Subdivision Surface, Mirror, Solidify, Array, Boolean
- **실습:** Non-destructive 워크플로우로 로봇 형태 다듬기
- **과제:** 로봇/캐릭터 형태 다듬기 실습
- **기존 Notion 자료:** 없음 (신규 제작)

### Week 05: AI 3D 생성 + Sculpting + MCP 활용
- **이론:** AI 3D 생성 원리, Sculpt Mode 기초
- **실습:** Meshy AI/Tripo AI로 3D 생성 → Blender 임포트 → Sculpt 수정
- **추가:** MCP로 기본 씬 자동 생성 실습
- **과제:** AI 3D + Blender 작업 적용 이미지
- **기존 Notion 자료:** Sculpting Tutorial (5.0 업데이트 필요)

### Week 06: Material & Shader Node
- **이론:** Material 생성, Principled BSDF, Shader Node Editor
- **실습:** Poly Haven/BlenderKit 텍스처 활용, Thin Film Iridescence(5.0 신기능)
- **과제:** 로봇/캐릭터 재질 적용 이미지
- **기존 Notion 자료:** Material Basic, Material Delete, Material Node (5.0 업데이트)

### Week 07: UV Unwrapping + AI Texture
- **이론:** UV 개념, Seam, Unwrap 방법, UV Editor
- **실습:** Texture 이미지 적용, AI 텍스처 생성 및 적용
- **과제:** 텍스처 적용된 로봇 렌더
- **기존 Notion 자료:** UV Unwrapping, Texture Painting, Texture Save/Export (5.0 업데이트)

### Week 08: 중간고사 - 중간 프로젝트 발표
- **제출:** 로봇/캐릭터 모델링 + 텍스처 완성본, 이미지 3장+, .blend 파일
- **배점:** 35%
- **신규 제작:** 루브릭, 제출 가이드, 발표 템플릿

### Week 09: Lighting 기초 + MCP 조명 연출
- **이론:** Point/Sun/Spot/Area, 3-Point Lighting, HDRI
- **실습:** Poly Haven HDRI, Blockade Labs AI HDRI 생성
- **추가:** Claude MCP로 다양한 조명 분위기 자동 연출
- **과제:** 3가지 조명 환경 렌더 이미지
- **기존 Notion 자료:** Lighting (5.0 업데이트 + HDRI 가이드 추가)

### Week 10: Animation 기초
- **이론:** Timeline, Keyframe(I), 오브젝트 애니메이션
- **실습:** 이동/회전/스케일 애니메이션, 프레임 범위 설정
- **과제:** 3~5초 간단한 움직임 애니메이션
- **기존 Notion 자료:** Animation (5.0 업데이트)

### Week 11: Rigging 기초
- **이론:** Armature, Bone 구조, IK/FK, Weight Painting, Pose Mode
- **실습:** 로봇/캐릭터에 기초 리깅 적용
- **과제:** 기초 리깅 적용 실습
- **기존 Notion 자료:** Basic Rigging (Character + Mechanical), Weight Painting (5.0 업데이트)

### Week 12: AI 활용 리깅 (Mixamo)
- **이론:** Mixamo 자동 리깅 원리, 애니메이션 라이브러리
- **실습:** Mixamo 리깅 → Blender 임포트 → 적용
- **과제:** Mixamo 리깅/애니메이션 적용
- **기존 Notion 자료:** Retargetting_Mixamo (5.0 업데이트)

### Week 13: AI 영상/사운드 + 렌더링 + MCP
- **이론:** Camera (Focal Length, DOF), Eevee vs Cycles, 5.0 색상 관리
- **실습:** Kling AI(이미지→비디오), Suno AI(BGM), 렌더링
- **추가:** MCP로 카메라/렌더 설정 자동화
- **과제:** 렌더링 + AI 영상/사운드 테스트
- **기존 Notion 자료:** Rendering, Camera Setting, Render & Export, Eevee 문제해결 (5.0 업데이트)

### Week 14: 최종 프로젝트 제작
- **활동:** 기말 프로젝트 본격 제작, 개별 피드백
- **과제:** 최종 프로젝트 진행 중간 체크
- **신규 제작:** 프로젝트 체크리스트, 피드백 가이드

### Week 15: 기말고사 - 최종 프로젝트 발표
- **제출:** 최종 프로덕트 완성본, 렌더 이미지, .blend, 영상
- **배점:** 35%
- **신규 제작:** 루브릭, 발표 가이드

### Week 16: 보강 (어린이날 보강)

## 5. Notion 기존 자료 업데이트 목록

Blender 5.0 기준으로 업데이트가 필요한 기존 Notion 페이지:

| Notion 페이지 | 업데이트 내용 |
|--------------|------------|
| Blender 기초 튜토리얼 | 5.0 UI 스크린샷, pill 탭, 단축키 변경 |
| Transform/Origin | 5.0 UI 반영 |
| Sculpting Tutorial | 5.0 변경사항 확인 및 반영 |
| Material Basic / Node | Thin Film Iridescence 추가, 5.0 UI |
| UV Unwrapping | 5.0 UI 반영 |
| Texture Painting / Save | 5.0 UI 반영 |
| Lighting | 5.0 HDR 색상 관리 추가 |
| Rendering | ACES 뷰, HDR 출력, Compositor 변경 |
| Animation | 5.0 변경사항 확인 |
| Basic Rigging (Character/Mechanical) | 5.0 변경사항 확인 |
| Weight Painting | 5.0 변경사항 확인 |
| Retargetting_Mixamo | 5.0 임포트 확인 |
| Camera Setting | 5.0 UI 반영 |
| Render & Export | 5.0 HDR/Wide-gamut 출력 옵션 추가 |
| Blender MCP 사용법 | 5.0 호환성 확인 |
| Instancing | 5.0 변경사항 확인 |
| Eevee 렌더링 문제해결 | 5.0 Eevee 변경사항 반영 |

## 6. 자료 제작 템플릿

### 강의노트 (lecture-note.md)
- 학습 목표 (체크리스트)
- 이론 섹션 (30분 분량)
- 실습 섹션 (90분 분량, step-by-step)
- 과제 안내
- 참고 자료 링크

### 슬라이드 (slides.md - Marp)
- 10~15장 분량
- 커스텀 테마 (RPD 브랜딩)
- 수업 중 화면 공유용
- 핵심 개념 + 단축키 + 실습 절차

### 과제 안내 (assignment.md)
- 제출 방법 (Discord 채널)
- 형식 (이미지 1~2장 + 한줄 코멘트)
- 평가 기준

## 7. 자료 언어 규칙

- 설명/해설: 한국어
- Blender 메뉴/도구명: 영어 그대로 (예: Edit Mode, Extrude, Principled BSDF)
- 단축키: 영어 표기 (예: Tab, I, G/R/S)
- AI 도구명: 영문 그대로 (예: Meshy AI, Suno AI)
