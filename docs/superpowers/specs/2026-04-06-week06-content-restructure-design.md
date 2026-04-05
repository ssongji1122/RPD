# Week 06 콘텐츠 재구성 설계 — 공통구조 4-Part 적용 + Week 7 브릿지

**날짜**: 2026-04-06
**범위**: RPD 6주차 (Material & Shader Node + AI PBR Texture)
**SSOT**: Notion 페이지 `Week 06: Material & Shader Node` (id: `31354d65-4971-818c-8cb5-e7814445e3eb`)
**관련 결정**: `memory/decision_log.md` — "주차별 수업 페이지 공통 구조 표준화" (2026-04-06)

---

## 배경

Week 6가 공통구조(`Part 0 오리엔테이션 / Part 1 이론 / Part 2 실습 / Part 3 정리 / Part 4 학생 리소스`)를 **처음 구현**하는 주차. 동시에 Week 7(UV+AI Texture)과의 브릿지에 3가지 갭 존재:

1. Week 7은 학생이 **Image Texture를 Base Color에 연결**할 줄 안다고 전제 — 현재 Week 6엔 Noise Texture만 있음
2. Week 7은 **PBR 맵 용어**(Diffuse/Roughness/Normal)를 전제 — 현재 Week 6에 없음
3. Week 7은 **로봇 UV 작업**을 전제 — 현재 Week 6 과제는 "구 5개 재질 샘플러"로 로봇과 무관

추가로 현재 과제가 드래그드랍 수준이라 학습밀도가 낮다는 피드백. AI 커리큘럼 취지에 맞게 **AI 텍스처 생성 워크플로우**로 재설계.

---

## 설계 원칙

- **SoT = Notion**. repo 쪽 `lecture-note.md`는 건드리지 않음 (decision log 2026-04-06)
- 공통구조 4-Part 골격 고정. 주차별 자유도는 Part 2 Step 수·내용에만 허용
- **기존 블록 내용 보존하며 재배치**. 파괴적 재작성은 신규 섹션에만
- `done` 필드 추가 안 함
- MCP는 **맛보기 수준**만 Week 6 도입, 본격 수업은 Week 9 유지

---

## 학습 목표 (이번 주차)

학생이 수업 후 다음을 할 수 있어야 함:

- Material 슬롯 구조 이해 + 오브젝트에 재질 할당
- Principled BSDF 4파라미터(Metallic / Roughness / Transmission / Emission)로 재질 표현
- Shader Editor에서 Color Ramp · Noise Texture · Image Texture 노드 연결
- Poly AI 도구로 PBR 3종 맵 생성 후 Shader Editor 연결
- PBR 맵 용어 3종(Diffuse / Roughness / Normal) 인지 — Week 7 브릿지

**수준**: 재질 감상자 + 노드 이해 (고급 재질 설계는 Week 7+ 이후)

---

## 전체 구조 맵

```
Week 06: Material & Shader Node + AI PBR Texture

🔗 이전 주차 복습      Week 5 AI 로봇을 이번 주에 완성체로
✅ 수업 시작 체크리스트  .blend 파일 / Blender 5.0 / Poly 가입
🎯 학습 목표           불릿 5~6개 (현재 6 heading_3 → 요약화)

═══ Part 1: 이론 ═══
  1.1 Material이란              → ShowMe: material-basics
  1.2 Principled BSDF 4파라미터  → ShowMe: principled-bsdf
  1.3 Shader Node란             → ShowMe: shader-editor
  1.4 Procedural vs Image      → ShowMe: texture-types (신규)
  1.5 PBR 맵 3종 용어           → Week 7 브릿지, 카드 없음

═══ Part 2: 실습 (7 Steps) ═══
  Step 1: Remesh로 작업 준비
  Step 2: Material 할당 + BSDF 탐색
  Step 3: Shader Editor + Color Ramp
  Step 4: Procedural Texture (Noise)
  Step 5: Image Texture + Poly PBR 4종 맵  ← 신규
  Step 6: 로봇 3개 복제 & 재질 적용          ← 신규
  Step 7 (선택): MCP로 Material 자동 생성 맛보기  ← 신규

═══ Part 3: 정리 ═══
  ⚠️ 흔한 실수 (개념 오해) 5개
  ✨ 핵심 정리 5줄
  📝 과제: 로봇 3종 재질 챌린지

═══ Part 4: 학생 리소스 ═══
  ⌨️  단축키 퀵 레퍼런스
  🔧 자주 막히는 지점 (실무 트러블슈팅) 7개
  🎥 공식 영상 / 📖 공식 문서
  🔗 참고자료 (Poly, Poly Haven, AmbientCG 등)
  ☑️  Week 6 완료 체크리스트

💡 Week 7 예고 callout
```

---

## Part 0: 오리엔테이션 (신규)

### 🔗 이전 주차 복습
- Week 5에서 AI(Meshy/Tripo)로 생성한 로봇 모델 준비 완료 확인
- Week 5 Step 6에서 저장한 `.blend` 파일이 이번 주차의 재료
- Remesh 정리까지 된 상태여야 Material이 자연스럽게 먹힘

### ✅ 수업 시작 체크리스트
- [ ] Week 5 .blend 파일 열려있다
- [ ] Blender 5.0.1 이상
- [ ] [Poly (withpoly.com)](https://withpoly.com) 가입 완료
- [ ] Material Preview 모드로 현재 로봇 상태 확인

### 🎯 학습 목표
- Material 슬롯 + Principled BSDF로 재질 표현
- Shader Editor 노드 기본 연결
- Procedural vs Image Texture 구분
- Poly로 AI PBR 텍스처 생성 → Shader 연결
- PBR 맵 3종 용어 인지 (Week 7 브릿지)

---

## Part 1: 이론

각 토픽 = **본문 서술 3~5줄 + ShowMe 카드 링크 1개** (하이브리드 방식)

### 1.1 Material이란 무엇인가
> 오브젝트의 "옷"이에요. 같은 메쉬여도 Material을 바꾸면 금속 로봇도 되고, 유리 로봇도 돼요. 하나의 오브젝트에 여러 Material을 쓸 수도 있어요 — 로봇 몸체는 금속, 눈은 발광처럼요. Material은 **Material Properties 패널**에서 관리하고, **Material 슬롯**에 담겨요.

**ShowMe**: `material-basics` (기존)

### 1.2 Principled BSDF — 재질 4파라미터
> Blender의 **디폴트 쉐이더**. 이 노드 하나의 슬라이더 4개로 웬만한 재질을 다 만들 수 있어요.
> - **Metallic** (0→1): 플라스틱 ↔ 금속
> - **Roughness** (0→1): 거울 ↔ 까끌까끌
> - **Transmission** (0→1): 불투명 ↔ 유리
> - **Emission**: 스스로 빛남 (램프, LED)

**ShowMe**: `principled-bsdf` (기존 — Emission 내용 보강 필요)

### 1.3 Shader Node란 — 레고 블록
> Shader Editor에서 **노드 = 레고 블록**, **연결선 = 데이터 흐름**이에요. 왼쪽 노드 출력을 오른쪽 노드 입력에 꽂으면, 앞 단계 결과가 뒤로 흘러가요. 마지막엔 항상 **Material Output**으로 들어가야 화면에 보여요.

**ShowMe**: `shader-editor` (기존 — 레고 비유 + 소켓 색 매칭 보강 필요)

### 1.4 Procedural vs Image Texture — 핵심 구분 (신규)
> 텍스처는 두 종류예요.
> - **Procedural (절차적)**: Noise·Musgrave처럼 **수식으로 만드는** 패턴. 해상도 무한, 파일 없음. 자연스러운 잡음·노이즈에 강함.
> - **Image Texture**: 사진·그림 파일을 불러와 씀. 구체적 디테일(벽돌, 나무결, 녹) 표현에 강함. **UV가 있어야 정확히 매핑**(→ Week 7).
> 이번 주는 **둘 다** 써봐요.

**ShowMe**: `texture-types` (🔴 신규 필수)

### 1.5 PBR 맵 3종 용어 — Week 7 브릿지 (신규)
> 진짜 같은 재질은 **맵 3종**으로 만들어요.
> - **Diffuse (Base Color)**: 색 정보
> - **Roughness**: 표면 거칠기 (흑백)
> - **Normal**: 표면 요철 (파란 이미지)
> 이번 주는 **Poly**에서 이 3종을 AI로 한 번에 생성해서 Principled BSDF에 연결해봐요. 다음 주엔 이 맵들이 **어떻게 메쉬에 매핑되는지**(UV)를 배워요.

**ShowMe**: 없음 (용어 소개 수준, Week 7에서 depth 보강)

---

## Part 2: 실습 — 7 Steps

### Step 1: Remesh로 작업 준비
**목표**: Week 5 AI 로봇 파일을 Material 적용 가능한 상태로 만들기

- [ ] Week 5 .blend 파일 열기
- [ ] Voxel Remesh · Decimate · Mesh Cleanup 차이 확인
- [ ] 적절한 도구 선택 → 폴리곤 정리
- [ ] Material Preview로 상태 확인

**ShowMe**: `remesh-modifier`, `decimate-modifier` (기존)

### Step 2: Material 할당 + Principled BSDF 탐색
**목표**: 재질 슬롯 구조 이해 + BSDF 4파라미터 직접 조작

- [ ] Material Properties에서 + New → 첫 재질 생성
- [ ] Base Color 변경
- [ ] Metallic 1.0 → 금속 재질
- [ ] Transmission 1.0 → 유리 재질
- [ ] Roughness 0 vs 0.5 vs 1 비교
- [ ] Emission으로 발광 재질
- [ ] Edit Mode에서 면 선택 → 두 번째 Material Assign

### Step 3: Shader Editor + Color Ramp
**목표**: 노드 그래프 편집 기초 + 색상 그라데이션

- [ ] Shader Editor 열기 (워크스페이스 Shading)
- [ ] Shift+A → Color → Color Ramp 추가
- [ ] Color Ramp 출력 → Base Color 입력 연결
- [ ] 색상 두 개 바꿔서 그라데이션 확인

**ShowMe**: `color-ramp` (🟡 신규 권장)

### Step 4: Procedural Texture (Noise)
**목표**: 이미지 없이 수식으로 재질감 만들기

- [ ] Shift+A → Texture → Noise Texture 추가
- [ ] Noise → Color Ramp → Base Color 연결
- [ ] Noise Fac 출력을 Principled BSDF Roughness에 연결
- [ ] Scale 값 바꿔가며 무늬 크기 조절

**ShowMe**: `noise-texture` (🟡 신규 권장)

### Step 5: Image Texture + Poly PBR 4종 맵 (신규, Week 7 브릿지)
**목표**: AI로 텍스처 생성 → Shader Editor에서 PBR 맵 연결

- [ ] [withpoly.com](https://withpoly.com) 가입 + 로그인
- [ ] 프롬프트 작성 (예: "rusty painted metal, worn industrial surface")
- [ ] PBR 4종 맵 다운로드 (Color / Normal / Roughness / AO)
- [ ] Shader Editor에 Image Texture 노드 3개 추가
- [ ] Color → Base Color
- [ ] Roughness → Roughness (Color Space: Non-Color)
- [ ] Normal → Normal Map 노드 → Normal (Color Space: Non-Color)
- [ ] 렌더 결과 확인

**Callout**: *"이미지가 로봇에 이상하게 늘어나 보이나요? 정상이에요 — UV가 없어서 그래요. 다음 주에 배워요."*

**ShowMe**: `image-texture-pbr` (🔴 신규 필수)

### Step 6: 로봇 3개 복제 & 과제 재질 적용
**목표**: 과제 소재 준비 + 3가지 재질 방식 실전 비교

- [ ] Week 5 로봇 Shift+D로 2번 복제 → 나란히 배치 (총 3개)
- [ ] 로봇 A: 수동 BSDF — 금속 또는 유리
- [ ] 로봇 B: 수동 BSDF — 발광 (Emission)
- [ ] 로봇 C: Poly AI PBR 텍스처 (Step 5 재활용)
- [ ] Z 키로 Material Preview ↔ Rendered 비교

### Step 7 (선택): MCP로 Material 자동 생성 맛보기
**목표**: MCP 첫 만남 — 프롬프트로 재질 만들어지는 경험 (Week 9 prereq 셋업 겸)

- [ ] Blender MCP addon 설치
- [ ] Claude에 MCP 연결 (포트 9876)
- [ ] 프롬프트로 재질 요청 (예: "빈티지 플라스틱")
- [ ] MCP가 만든 노드 그래프 **읽어보기**
- [ ] 수동 설정한 로봇과 비교

**Callout**: *"MCP는 Week 9에서 조명 연출로 본격 다뤄요. 이번 주는 맛보기."*

**ShowMe**: 없음 (Week 9에서 본격 카드)

---

## Part 3: 정리

### ⚠️ 흔한 실수 (개념 오해) — 5개

1. **Emission 1.0인데 빛이 안 나요** → Rendered 모드에서만 보여요
2. **유리가 검게 보여요** → 환경이 반사돼야 유리. HDRI 환경광 추가
3. **Color Ramp 바꿔도 색이 안 변해요** → Material Output 연결 확인
4. **소켓끼리 연결이 안 돼요** → 색깔이 다르면 타입 불일치
5. **Image Texture가 이상하게 늘어나요** → UV가 없어서. Week 7에서 해결

### ✨ 핵심 정리 — 5줄 요약

```
1. Material = 오브젝트의 옷. 슬롯 구조로 여러 개 가능.
2. Principled BSDF 4파라미터(Metallic/Roughness/Transmission/Emission)로
   대부분의 재질 표현 OK.
3. Shader Editor = 노드 그래프. 왼→오 연결, 마지막은 Material Output.
4. Texture 2종 = Procedural(수식) / Image(파일). 목적에 따라 선택.
5. AI PBR 텍스처는 Poly에서 프롬프트 한 줄로 3종 맵 획득 가능.
   → 단, UV가 없으면 왜곡 (Week 7 해결).
```

### 📝 과제 — "로봇 3종 재질 챌린지"

**필수 (3개):**
- 로봇 A: 수동 BSDF — 금속 또는 유리
- 로봇 B: 수동 BSDF — 발광 (Emission)
- 로봇 C: Poly AI PBR — PBR 3종 맵 생성 + Shader Editor 연결

**도전 (선택):**
- 로봇 D: MCP 자동 생성 + 노드 그래프 읽기

**제출물:**
- [ ] 로봇 3개(+도전) 나란히 배치한 **렌더 이미지 1장** (1920×1080)
- [ ] 각 로봇의 **Shader Editor 스크린샷** 1장씩
- [ ] **1줄 메모**: 어떤 방식이 가장 빠르고/자연스러웠는지
- [ ] .blend 파일 저장 (Week 7에서 사용)

**평가 포인트:**
- 3파라미터 이상 수동 조정 흔적
- Image Texture 노드 3종 실제 연결
- 렌더 모드에서 HDRI 사용

---

## Part 4: 학생 리소스

### ⌨️ 단축키 퀵 레퍼런스

```
─── 뷰포트 ───
Z                       Shading 모드 전환 파이 메뉴
Shift + ` (백틱)        Material Preview 빠른 토글
F12                     최종 렌더
Ctrl + F3               뷰포트 스크린샷 저장

─── Shader Editor ───
Shift + A               노드 추가 메뉴
Ctrl + Shift + Click    Viewer 노드 연결 (미리보기)
Ctrl + T                Image Texture에 자동 Mapping+Coordinate 추가
G / R / S               노드 이동 / 회전 / 크기
M                       노드 Mute (연결 임시 해제)
F                       선택된 두 노드 자동 연결

─── Edit Mode 재질 ───
Tab                     Edit Mode 토글
3                       면 선택 모드
Ctrl + L → Materials    연결된 오브젝트에 재질 복사
```

### 🔧 자주 막히는 지점 (실무 트러블슈팅) — 7개

1. **뷰포트가 검게만 나와요** → Shading 모드(Z) 확인. Solid면 재질 안 보임
2. **Poly PBR 맵 어디에 꽂는지 모르겠어요** → Color→Base Color / Rough→Roughness / Normal→Normal Map 노드 경유 / AO→선택
3. **Normal 맵 효과가 너무 약/강해요** → Normal Map 노드 Strength 조절 (0.3~1.5)
4. **Image Texture 색이 바랬어요** → Color 맵은 sRGB, Rough/Normal은 Non-Color
5. **Shader Editor에 노드가 안 보여요** → 상단 토글이 World로 되어있을 수 있음. Object 탭으로
6. **렌더하면 재질이 다르게 보여요** → Material Preview는 고정 HDRI, Rendered는 Scene 조명
7. **MCP 연결이 안 돼요 (Step 7)** → Blender MCP addon 활성화 + 포트 9876 확인

### 🎥 공식 영상 / 📖 공식 문서

**공식 영상:**
- Blender Studio — [Materials and Shading](https://studio.blender.org)
- Blender YouTube — Shader Editor Introduction

**공식 문서:**
- [Blender Manual — Materials](https://docs.blender.org/manual/en/latest/render/materials/index.html)
- [Blender Manual — Principled BSDF](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html)
- [Blender Manual — Shader Editor](https://docs.blender.org/manual/en/latest/editors/shader_editor.html)
- [Blender Manual — Texture Nodes](https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/index.html)
- [Blender Manual — Color Ramp](https://docs.blender.org/manual/en/latest/render/shader_nodes/converter/color_ramp.html)

### 🔗 참고자료

**AI 텍스처 도구:**
- [Poly (withpoly.com)](https://withpoly.com) — 이번 주 사용
- [Polycam AI Texture](https://poly.cam/tools/ai-texture) — 대안
- [Adobe Substance 3D Sampler](https://www.adobe.com/products/substance3d-sampler.html) — 프로용

**무료 PBR 텍스처 라이브러리:**
- [Poly Haven](https://polyhaven.com/textures)
- [AmbientCG](https://ambientcg.com)
- [Textures.com](https://www.textures.com)

**HDRI (환경 조명):**
- [Poly Haven HDRIs](https://polyhaven.com/hdris)

### ☑️ Week 6 완료 체크리스트

- [ ] Week 5 로봇을 Remesh로 정리했다
- [ ] Principled BSDF 4파라미터 각각 바꿔봤다
- [ ] Shader Editor에서 Color Ramp + Noise 연결했다
- [ ] Poly에서 PBR 3종 맵 생성해서 로봇에 연결했다
- [ ] 과제: 로봇 3개에 서로 다른 재질 적용 완료
- [ ] 렌더 이미지 + Shader 스크린샷 제출 준비 완료
- [ ] .blend 파일 저장 — Week 7 UV 작업에서 씀

### 💡 Week 7 예고

> "Image Texture가 이상하게 늘어난다"는 이슈, 기억나요? 다음 주 **UV Unwrapping**에서 해결합니다. 로봇에 펠트지 뜨듯 "평면 전개도"를 펴서 텍스처를 정확히 매핑하는 법을 배워요. Week 6 .blend 파일 꼭 저장해두세요.

---

## ShowMe 카드 작성 계획

### 신규 필요 (4개) — β 범위

| 카드 ID | 우선순위 | 내용 | 사용처 |
|---|---|---|---|
| `texture-types` | 🔴 필수 | Procedural vs Image Texture 비교 | Part 1.4, Step 4~5 |
| `image-texture-pbr` | 🔴 필수 | Poly 워크플로우 + PBR 3종 맵 연결 | Step 5 |
| `noise-texture` | 🟡 권장 | Noise Scale/Detail 활용법 | Step 4 |
| `color-ramp` | 🟡 권장 | 단색/그라데이션 만들기 | Step 3 |

### 기존 카드 보강

| 카드 | 보강 내용 |
|---|---|
| `shader-editor` | "레고 블록" 비유 + 소켓 색 매칭 confusion 추가 |
| `principled-bsdf` | Emission 4번째 파라미터 내용 포함 확인 |
| `viewport-shading` | `_registry.js`에 `week: 6` 태그 추가 |

**제외:**
- `mcp-material-intro` (Week 9 본격 수업에서 더 풍부하게 만들 예정)

---

## Notion 실행 전략

### 작업 방식: **구조 재배치 + 신규 섹션 추가**, 기존 블록 내용 보존

Notion API는 블록 이동을 직접 지원하지 않으므로:

1. **기존 Week 6 페이지 → 백업용 복사본 생성** (archive/Week 06 backup 2026-04-06)
2. **신규 구조로 페이지 재구성**:
   - 기존 블록 중 보존할 것: 학습목표 하위 6 heading_3의 체크리스트 내용, 단축키, 공식 문서 링크, 흔한 실수 5개, 과제 구조
   - 기존 블록 중 재배치할 것: Remesh(→Step 1), Material 할당(→Step 2), BSDF(→Step 2 통합), Shader Node(→Step 3), Texture(→Step 4), Viewport Shading(→Part 1.3 추가 or 생략)
   - 삭제할 것: 기존 "구 5개 재질 샘플러" 과제 (새 과제로 교체)
3. **신규 블록 작성**: Part 0 전체, Part 1 이론 5개 토픽, Step 5/6/7, Part 3 핵심 정리, Part 4 자주 막히는 지점 / 참고자료 / 완료 체크리스트 / Week 7 예고
4. **ShowMe 카드 링크** 각 섹션에 삽입 (카드 먼저 작성 or placeholder 링크)

### 후속 작업

**Week 9 페이지 업데이트 필요**:
- "MCP 첫 만남" 톤 → "이미 Week 6에서 만났고, 조명 맥락으로 재활용" 톤 변경
- MCP addon 설치 prereq를 "Week 6 Step 7에서 셋업 완료" 문구로

**Week 5 페이지**:
- 현재 미적용 공통구조, 차후 재정렬 (우선순위 낮음)

---

## 변경하지 않는 것

- repo `course-site/` 내 `lecture-note.md`, `slides.md`, `assignment.md` (Notion이 SoT)
- 기존 Week 6의 단축키 리스트 내용 (보존하며 재배치만)
- 기존 흔한 실수 5개 항목 (보존 + 신규 2개 추가 검토)
- 다른 주차(Week 1~5, 7~15) 구조 (Week 6 검증 후 순차 적용)

---

## 구현 의존성 순서

1. **ShowMe 카드 4개 작성** (`/showme` 활용)
2. **Notion Week 6 페이지 재구성** (백업 후 구조 재배치)
3. **Notion Week 9 페이지 prereq 문구 업데이트**
4. (선택) repo 쪽 `curriculum.js` Week 6 동기화

## Open Questions / 후속 결정 필요

- HDRI 설정 실습을 Step 5/6 어디에 끼울지 (유리/금속 반사 확인용) — 현재는 학생 자율에 맡김
- Step 7 MCP 도전과제의 시연/셋업 시간이 수업 중 충분한지 — 선택 섹션이므로 부담 없음
- ShowMe 카드 `principled-bsdf` 기존 내용 감사 필요 (Emission 4파라미터 포함 여부)
