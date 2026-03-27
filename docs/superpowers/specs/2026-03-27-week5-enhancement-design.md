# Week 5 Enhancement: AI 러프 디자인 + Sculpt 교육

> Created: 2026-03-27
> Status: Approved (brainstorming complete)

## 목표

5주차를 "Sculpt 기술 교육 → 본인 프로젝트 AI 러프 생성"으로 재구성한다.
1~4주차 로봇 기초 모델링을 마무리하고, 학생 개인 프로젝트로 전환하는 분기점.

## 배경

- 1주차에 Mixboard로 무드보드/아이디에이션 완료 (Notion 개인폴더에 링크+이미지 저장)
- 학생 프로젝트 방향: 혼합 (캐릭터, 기계, 하이브리드 등 제각각)
- 하드서피스 분기 불필요 — Sculpt는 새 도구 교육, AI 생성은 러프 확인 목적

## 현재 5주차 스텝 순서

1. AI 3D 생성 체험 (Meshy/Tripo)
2. AI 메쉬 정리 (Decimate)
3. Sculpt Mode 기초 (Draw/Grab/Smooth)
4. Sculpt 브러시 심화 (Clay/Crease/Inflate)
5. Remesh와 마무리

## 변경 후 스텝 순서

1. **Sculpt Mode 기초** — Draw/Grab/Smooth 3대 브러시 (기존 Step 3 → 앞으로 이동)
2. **Sculpt 브러시 심화** — Clay Strips/Crease/Inflate/Snake Hook (기존 Step 4 확장)
3. **Remesh + Decimate + 메쉬 정리** — 기존 Step 2+5 합치기 + 애드온 추가
4. **무드보드 → AI 프롬프트 설계** — 신규
5. **본인 프로젝트 AI 러프 생성** — 기존 Step 1 수정
6. **AI 메쉬 정리 실전** — Step 3에서 배운 도구로 AI 메쉬 직접 정리

### 변경 근거

- Sculpt를 먼저 가르치면, AI 생성 메쉬를 다듬는 맥락이 자연스러움
- 무드보드 분석 스텝을 AI 생성 직전에 넣어 "내 아이디어 → 프롬프트 → 3D" 연결
- Remesh/Decimate를 Sculpt 파트에 묶되, AI 메쉬 정리에서 재활용

---

## Step 3: 메쉬 정리 애드온 (신규 추가)

### Mesh Cleaner 2 (무료)

- Gumroad에서 pay-what-you-want ($0 가능)
- one-click 메쉬 전처리: 중복 버텍스, 플리핑 노멀, 빈 구멍, 미사용 Material 제거
- Blender 4.3+ 호환, 5.0.1 작동 확인
- URL: https://decoded.gumroad.com/l/meshcleaner

### QRemeshify (무료)

- 트라이앵글 → 쿼드 토폴로지 변환 (QuadWild 기반 Bi-MDF solver)
- Gumroad에서 pay-what-you-want ($0 가능)
- Blender 4.2+ 호환, 5.0 확인
- URL: https://ksami.gumroad.com/l/QRemeshify

---

## Step 4: 무드보드 → AI 프롬프트 설계 (신규)

### copy
"1주차에 만든 무드보드, 기억하죠? 오늘 그걸 3D로 만들기 시작해요.
AI한테 잘 설명하려면 이미지 느낌을 단어로 번역하는 과정이 필요해요."

### tasks
- `w5-t-mood1`: Notion에서 내 무드보드 열기
- `w5-t-mood2`: 핵심 키워드 5개 이내 추출 (형태/스타일/재질감 각 1~2개)
- `w5-t-mood3`: Meshy용 프롬프트 초안 작성 — `[형태] + [스타일] + [재질감] + 3D model` 패턴

### goal
- 무드보드 이미지를 텍스트 키워드로 변환할 수 있다
- AI 3D 생성용 프롬프트를 작성할 수 있다

### done
- 프롬프트 초안이 노션에 기록되었다

---

## Step 5: 본인 프로젝트 AI 러프 생성 (수정)

### copy 변경
기존: "텍스트 몇 글자 입력하면 3D 메쉬가 뚝딱 나와요..."
변경: "내 아이디어의 초벌을 AI가 잡아줘요. 완벽하지 않아도 괜찮아요 — 오늘은 방향을 확인하는 게 목적이에요."

### task 변경
- `w5-t1` 수정: "Meshy에서 **내 프롬프트**로 생성" (기존: 일반 프롬프트)
- `w5-t2` 수정: "키워드 하나 바꿔서 재생성 — 어느 쪽이 내 의도에 더 가까운지 선택"
- `w5-t3` 유지: .glb Import

---

## Step 6: AI 메쉬 정리 실전 (수정)

Step 3에서 배운 Mesh Cleaner 2 + Decimate + QRemeshify를 AI 생성 메쉬에 직접 적용.
별도 기술 교육 없이 "이미 아는 도구를 새 맥락에 써보는" 실전 단계.

---

## Assignment 교체

### 기존
> "AI 생성 메쉬를 Sculpt로 다듬은 결과물"

### 변경
> **"내 프로젝트 첫 3D 러프"**
> - 내 무드보드에서 추출한 프롬프트 키워드 (텍스트)
> - AI 생성 원본 스크린샷
> - 메쉬 정리 후 스크린샷
> - 한 문장: "나는 앞으로 ___을 만들 예정이에요"

---

## Showme 카드

### 기존 카드 활용

| 카드 ID | 배치 스텝 | 상태 |
|---------|----------|------|
| `sculpt-basics` | Step 1 | 있음 |
| `remesh-modifier` | Step 3 | 있음 |
| `decimate-modifier` | Step 3 | 있음 |
| `mask-modifier` | Step 3 widget | 있음 |
| `multiresolution-modifier` | Step 3 widget | 있음 |

### 신규 카드 3장

#### 1. `sculpt-brushes` (Sculpting 카테고리)

**audienceNeed:** "기본 3개는 써봤는데 다른 브러시들은 뭐가 다른 건지 감이 안 올 때"

**탭 5개:**

| 탭 | 내용 |
|----|------|
| 브러시 도감 | 8종 브러시 카드 — Draw, Clay Strips, Clay, Inflate, Crease, Grab, Snake Hook, Smooth. 각 카드에 비유/용도/단축키/Ctrl반전 설명 |
| 직접 해보기 | **2D Canvas 하이트맵 스컬프트 샌드박스**. 200x200 그리드, 높이→그라데이션 컬러 시각화. 브러시 선택 버튼 8개, 드래그로 실시간 적용. F=크기조절, Ctrl=반전, Shift=Smooth 시뮬레이션. Reset 버튼. 하단 힌트: "브러시를 바꿔가며 구를 얼굴 형태로 만들어 보세요" |
| 비교 | 같은 구에 다른 브러시 적용 → Canvas before-after (sculpt-basics와 동일 패턴) |
| 레시피 | 브러시 조합 워크플로우 카드 — "얼굴 만들기" = Grab 턱 → Clay 광대 → Crease 눈/코 → Smooth 정리 |
| 퀴즈 | 브러시 선택 판단 문제 5~6개 |

**인터랙티브 "직접 해보기" 브러시 알고리즘:**
- Draw: 반경 내 높이 += strength
- Clay Strips: 일정 높이까지만 올림 (평탄+약간 볼록)
- Clay: Draw와 유사하되 평탄화 경향
- Inflate: 반경 내 높이를 바깥으로 퍼트림
- Crease: 중앙만 깊게 파임 (날카로운 감쇠 곡선)
- Grab: 반경 전체를 드래그 방향으로 이동
- Snake Hook: 끝점만 따라오는 드래그
- Smooth: 인접 셀 평균값으로 수렴

**visualPattern:** `interactive-canvas`

#### 2. `ai-prompt-design` (기타 카테고리)

**audienceNeed:** "AI한테 뭘 어떻게 써야 내가 원하는 모양이 나오는지 모르겠을 때"

**탭 4개:**
| 탭 | 내용 |
|----|------|
| 개념 이해 | 프롬프트 공식: `[형태] + [스타일] + [재질감] + [색상] + 3D model`. 각 슬롯별 예시 단어 |
| 시각적 비교 | Good vs Bad 프롬프트 → 결과 비교 (Canvas 일러스트) |
| 언제 쓰나요? | 무드보드 → 키워드 추출 → 프롬프트 변환 워크플로우 |
| 퀴즈 | 프롬프트 개선 문제 3~4개 |

**visualPattern:** `comparison`

#### 3. `ai-3d-generation` (기타 카테고리)

**audienceNeed:** "Meshy/Tripo에서 만들고 Blender로 가져오는 흐름이 안 잡힐 때"

**탭 4개:**
| 탭 | 내용 |
|----|------|
| 개념 이해 | AI 3D 생성 원리 간략 설명 + Meshy/Tripo 비교 |
| 시각적 비교 | 생성 → 다운로드 → Import → 정리 4단계 워크플로우 다이어그램 |
| 언제 쓰나요? | Import 후 체크리스트 (크기/원점/폴리곤 수), Mesh Cleaner 2 + QRemeshify 사용법 |
| 퀴즈 | Import 관련 문제 3~4개 |

**visualPattern:** `workflow`

---

## curriculum.js 기타 변경

### title/subtitle 유지
"AI 3D 생성 + Sculpting" → 그대로 (Sculpt가 먼저 오지만 제목은 현행 유지)

### topics 순서 재배치
```
"Sculpt Mode 기초 브러시",
"Sculpt 브러시 심화 (Clay/Crease/Inflate/Snake Hook)",
"Remesh·Decimate·메쉬 정리 애드온",
"무드보드 → AI 프롬프트 설계",
"AI 3D 생성 (Meshy/Tripo)",
"AI 메쉬 Import 및 실전 정리"
```

### shortcuts 유지 (기존 그대로)

### explore 유지 (기존 그대로)

### mistakes 추가
- "프롬프트가 너무 짧음 → 형태+스타일+재질 키워드를 넣어야 원하는 결과가 나와요"
- "AI 메쉬를 정리 없이 바로 Sculpt → Mesh Cleaner 먼저 돌리고 시작하기"

### videos 유지

### docs 추가
- Mesh Cleaner 2: https://decoded.gumroad.com/l/meshcleaner
- QRemeshify: https://ksami.gumroad.com/l/QRemeshify

---

## _catalog.json 변경

### manualSectionMap 추가
```json
"sculpt-brushes": "sculpting-painting",
"ai-prompt-design": "sculpting-painting",
"ai-3d-generation": "sculpting-painting"
```

### categoryMap 추가
```json
"sculpt-brushes": "Sculpting",
"ai-prompt-design": "기타",
"ai-3d-generation": "기타"
```

### cardOverrides 추가
```json
"sculpt-brushes": {
  "officialVideos": [
    { "label": "Blender Studio - Sculpting Brushes", "url": "https://studio.blender.org/training/sculpting-in-blender/brushes/" }
  ],
  "keywords": ["clay strips", "crease", "inflate", "snake hook", "brush comparison"],
  "prerequisites": ["sculpt-basics"],
  "audienceNeed": "기본 3개는 써봤는데 다른 브러시들은 뭐가 다른 건지 감이 안 올 때"
},
"ai-prompt-design": {
  "keywords": ["prompt", "AI", "keyword", "moodboard", "text to 3d"],
  "audienceNeed": "AI한테 뭘 어떻게 써야 내가 원하는 모양이 나오는지 모르겠을 때"
},
"ai-3d-generation": {
  "keywords": ["meshy", "tripo", "AI 3D", "glb", "import", "mesh cleaner"],
  "audienceNeed": "Meshy/Tripo에서 만들고 Blender로 가져오는 흐름이 안 잡힐 때"
}
```
