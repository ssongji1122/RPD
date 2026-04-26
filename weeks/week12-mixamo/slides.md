---
marp: true
theme: rpd
paginate: true
---

# Week 12: AI 활용 리깅 (Mixamo)

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## Mixamo란?

- **Adobe에서 제공하는 무료 웹 서비스**
- 핵심 기능:
  1. **자동 리깅:** AI가 3D 캐릭터에 Bone을 자동 배치
  2. **애니메이션 라이브러리:** 2000+ 모션 캡처 기반 무료 애니메이션
- 웹 브라우저에서 작업 (소프트웨어 설치 불필요)
- 상업적 사용 가능

**https://www.mixamo.com** (Adobe 계정 필요, 무료 가입)

---

## 자동 리깅 원리

**AI가 인체 구조를 인식하여 Bone 자동 배치**

1. 3D 모델을 FBX로 업로드
2. 5개 마커를 주요 관절에 배치:
   - Chin (턱), Wrists (손목), Elbows (팔꿈치)
   - Knees (무릎), Groin (사타구니)
3. AI가 나머지 Bone 위치를 자동 추론
4. 약 65개 Bone의 표준 스켈레톤 생성
5. Weight Painting도 자동 처리

---

## Mixamo 모델 요구사항

| 조건 | 설명 |
|------|------|
| **T-Pose** | 팔을 양옆으로 벌린 T자 자세 (가장 중요) |
| **사지 분리** | 팔, 다리, 머리가 명확히 분리 |
| **깨끗한 Mesh** | 구멍, 겹침, Non-Manifold 없을 것 |
| **단일 Mesh** | 여러 파츠는 Ctrl+J로 합치기 |
| **폴리곤 수** | 10만 이하 권장 |
| **기존 Armature** | 삭제 후 업로드 |

**주의:** 비인체형 로봇(4족 등)은 자동 리깅이 어려울 수 있음

---

## FBX 포맷과 내보내기

**FBX:** 3D 데이터 교환 표준 포맷 (Mesh + Armature + Animation)

**Blender 내보내기 설정:**
1. File > Export > FBX (.fbx)
2. Apply Scalings: **All Local**
3. Apply Modifiers: **체크**
4. Forward: **-Z Forward** / Up: **Y Up**
5. Ctrl+A > All Transforms 적용 후 Export

---

## Mixamo 업로드 및 리깅

**업로드:**
1. mixamo.com > Upload Character
2. FBX 파일 드래그 앤 드롭

**마커 배치:**
- Chin, Wrists, Elbows, Knees, Groin
- 정확한 배치 = 높은 리깅 품질

**스켈레톤 옵션:**
- **Use No Fingers:** 간단한 모델
- **Use Fingers:** 손가락이 있는 모델

프리뷰에서 결과 확인 후 문제 있으면 마커 재조정

---

## 애니메이션 라이브러리

**검색 키워드로 원하는 애니메이션 탐색:**

| 키워드 | 동작 |
|--------|------|
| Walking | 걷기 |
| Running | 뛰기 |
| Dancing | 춤추기 |
| Waving | 인사 |
| Idle | 대기 자세 |
| Fighting | 전투 |
| Jumping | 점프 |

**설정 조정:** Character Arm-Space, Trim, Speed, In Place

---

## FBX 다운로드 및 Blender 임포트

**Mixamo 다운로드 설정:**
- Format: **FBX**
- Skin: **With Skin** (첫 번째) / **Without Skin** (두 번째부터)
- FPS: **30**

**Blender 임포트:**
1. File > Import > FBX
2. Automatic Bone Orientation: **체크**
3. Scale 조정 (필요 시)
4. Space로 애니메이션 재생 확인

---

## NLA Editor 개념

**NLA (Non-Linear Animation) Editor:**
여러 애니메이션을 **블렌딩/시퀀싱**하는 도구

**핵심 개념:**
- **Action:** 하나의 애니메이션 데이터 (걷기, 뛰기, 인사...)
- **NLA Strip:** Action을 타임라인에 배치한 클립
- **Push Down:** Action을 NLA Strip으로 변환
- **Blend In/Out:** Strip 간 부드러운 전환

**열기:** Editor Type > NLA Editor

---

## NLA Editor 실습

**여러 애니메이션 이어 붙이기:**

1. 첫 번째 Animation Action > **Push Down**으로 Strip 변환
2. 두 번째 Animation FBX 임포트
3. 새 Action도 **Push Down**
4. Strip을 드래그하여 순서 배치

**전환 설정:**
- 두 Strip을 약간 겹치게 배치
- N 패널 > Strip > **Blend In/Out** 값 조정
- Extrapolation: Nothing / Hold / Hold Forward

---

## 실습 전체 워크플로우

```
Blender에서 FBX 내보내기
        ↓
Mixamo 업로드 → 마커 배치 → 자동 리깅
        ↓
애니메이션 선택 → 설정 조정
        ↓
FBX 다운로드 (With Skin + Without Skin)
        ↓
Blender에서 FBX 임포트
        ↓
NLA Editor에서 애니메이션 조합
        ↓
최종 결과물 확인
```

---

## 과제 안내

- **제출처:** 본인 학생 페이지
- **내용:**
  - Mixamo 자동 리깅 + 2가지 이상 애니메이션 적용
  - 애니메이션 GIF 또는 영상 2개
  - Mixamo 리깅 스크린샷 1장
- **평가:** Mixamo 리깅 30% / 애니메이션 선택 35% / NLA 편집 35%

---

## 다음 주 예고: 렌더링 + AI 영상/사운드

**Week 13: 렌더링 + AI 영상/사운드**

- Cycles / EEVEE 렌더 엔진 비교 및 설정
- AI 영상 생성 도구 활용
- AI 사운드/음악 생성 도구 활용
- 최종 프로젝트를 위한 영상 제작 기초
