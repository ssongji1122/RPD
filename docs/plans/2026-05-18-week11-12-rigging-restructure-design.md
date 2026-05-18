# Week 11-12 Rigging 시리즈 재설계 (기초 + AI 활용)

> 생성일: 2026-05-18 | Blender 5.0 기준 | 대상: 인하대 RPD 완전 초보 대학생

---

## 1. 배경 / 문제

### 현재 구조
- **W10 (done)**: 키프레임 애니메이션 (Dope Sheet, Graph Editor, 루프)
- **W11 (active)**: 리깅 기초 — Armature + Skinning + Pose + Weight Paint (100% 수동)
- **W12 (upcoming)**: AI 활용 리깅 (Mixamo + NLA)

### 문제점
1. W11 4개 step 모두 수동 작업 → 3시간 안에 완료 불가능. Weight Paint 추상도 높아 초보 좌절
2. W12에서 "Mixamo로 1분이면 됐던 작업" 발견 시 W11 학습 의미 손상
3. Weight Paint가 W11에 고립되어 "왜 배우는지" 맥락 부재
4. 2026.05 기준 AI 리깅 생태계 다양화(AccuRIG 2.0, Meshy 등) 반영 안 됨

---

## 2. 설계 원칙

- **본질 → 자동화 흐름**: "리깅이 뭔지 → 수동 본 얹기 체험 → AI 도구 인지 → AI 본격 활용 → 결과 보정"
- **정보 전달 중심**: 동기·메타 설명 없이 개념과 도구만
- **무료 우선**: AI 도구 카탈로그는 무료/유료 명확히 분리, 무료 우선 학습
- **2026.05 검증**: 공홈 직접 확인된 최신 정보만 사용
- **Weight Paint 재배치**: W11 → W12로 이동, "AI 결과 보정" 맥락에서 등장

---

## 3. W11 재설계: 리깅 본질 + 수동 본 얹기 + AI 도구 인지

**제목**: "Rigging 기초"
**부제**: "Armature 개념 · 수동 본 얹기 · AI 리깅 도구 소개"
**예상 시간**: ~3시간

### Step 1. Armature 개념
**copy**: 메쉬 안에 뼈대(Armature)를 넣어서 뼈를 움직이면 메쉬가 따라오게 만드는 거예요. 인형 안의 철사 골격과 같아요.

**goal**:
- Bone, Parent, Rest Pose 개념을 안다
- 메쉬와 Armature의 관계를 안다

**done**:
- Armature가 무엇이고 왜 필요한지 설명할 수 있다

**tasks**:
- Armature/Bone/Parent 슬라이드 보기
- 본 하나 = Head + Tail + Roll 구조 이해

---

### Step 2. 수동 본 만들기
**copy**: Shift+A로 Armature를 추가하고, Edit Mode에서 E로 본을 확장해서 척추-팔-다리 체인을 만들어요. 이름을 .L/.R로 붙이면 나중에 미러 작업이 쉬워져요.

**goal**:
- Armature를 추가하고 본 체인을 만든다
- 본 이름 규칙을 적용한다

**done**:
- 척추 + 양팔 + 양다리 구조의 본이 있다
- 본 이름이 spine, arm.L, arm.R, leg.L, leg.R 형식이다

**tasks**:
- Shift+A → Armature → Single Bone (몸통)
- Edit Mode 진입, E로 어깨·팔·다리 방향 확장
- Properties → Bone → 이름 입력
- Viewport Display → Names 켜기

**shortcuts**: Shift+A, E, Shift+D, Ctrl+N (Roll 재계산)

---

### Step 3. 메쉬에 얹기 (Skinning)
**copy**: W3-4에서 만든 로봇이나 캐릭터 메쉬에 본을 연결해요. 메쉬를 먼저 선택하고 Armature를 Shift+클릭으로 추가 선택한 뒤 Ctrl+P → With Automatic Weights를 누르면 Blender가 자동으로 영향 범위를 계산해줘요.

**goal**:
- 메쉬-Armature 부모 관계를 만든다
- Automatic Weights를 적용한다

**done**:
- 본을 움직이면 메쉬가 따라온다

**tasks**:
- 메쉬 먼저 선택 → Shift+클릭으로 Armature 추가
- Ctrl+P → With Automatic Weights
- Armature Modifier가 메쉬에 추가된 것 확인

**mistakes**:
- 메쉬 안 움직임 → 선택 순서 확인 (Armature가 Active여야 함)
- 본 안 보임 → Properties → Object Data → Viewport Display → In Front 체크
- 위치 어긋남 → 리깅 전 Ctrl+A → All Transforms

---

### Step 4. Pose Mode 동작 확인
**copy**: Ctrl+Tab으로 Pose Mode에 들어가서 본을 R/G로 움직여요. 본을 회전시키면 연결된 메쉬도 같이 변형돼요. Alt+R로 회전을 초기화할 수 있어요.

**goal**:
- Pose Mode로 전환하고 본을 조작한다
- 포즈를 만들고 리셋한다

**done**:
- 캐릭터가 팔을 들거나 인사하는 포즈가 잡힌다

**tasks**:
- Armature 선택 → Ctrl+Tab → Pose Mode
- 본 선택 → R로 회전, G로 이동
- 여러 본 조합으로 인사 포즈
- Alt+R로 회전 리셋

**shortcuts**: Ctrl+Tab, R, G, Alt+R, Alt+G

---

### Step 5. AI 자동 리깅 도구 인지
**copy**: 수동 리깅만 있는 게 아니에요. 2026년에는 AccuRIG, Mixamo 같은 무료 AI 도구가 캐릭터를 1분 만에 리깅해줘요. 다음 주에 직접 써볼 거예요.

**goal**:
- AI 리깅 도구의 존재와 종류를 안다

**done**:
- AccuRIG, Mixamo가 뭔지 한 줄로 설명 가능

**tasks**:
- AccuRIG 90초 데모 영상 보기
- Mixamo 무료 라이브러리 미리보기

---

### Step 6. AI 학습 보조 활용
**copy**: 막혔을 때 스크린샷을 찍어서 ChatGPT나 Claude에게 보여주면 답을 알려줘요. "본을 회전시켰는데 메쉬가 안 움직여요" 같은 질문에 디버깅 도움을 받아요.

**goal**:
- 멀티모달 AI에 Blender 화면을 보내서 막힘을 푸는 방법을 안다

**done**:
- 본인이 겪은 문제 1개를 AI에게 질문해서 답을 받았다

**tasks**:
- 화면 캡처 (Shift+Cmd+4, Win+Shift+S)
- ChatGPT/Claude 웹에 이미지 + 질문 입력
- 답변 적용해보기

---

### W11 과제
- W3-4 로봇/캐릭터에 본 체인 얹기
- 포즈 2가지 스크린샷
- AI에게 디버깅 질문 1번 시도 + 답변 메모

### W11 explore
- 본인 캐릭터에 손가락 본 추가
- Bone Constraint(IK) 한 번 추가해보기
- 대칭 리깅 (.L/.R 이름 + Symmetrize)

---

## 4. W12 재설계: AI 리깅 도구 + Weight Paint 보정 + NLA 시퀀스

**제목**: "AI 리깅과 애니메이션 시퀀스"
**부제**: "AI 리깅 카탈로그 · AccuRIG/Mixamo · Weight Paint 보정 · NLA"
**예상 시간**: ~3시간

### Step 1. 2026 AI 리깅 도구 카탈로그
**copy**: AI 리깅 도구는 무료부터 유료까지 다양해요. 무료 도구로 시작해서 필요할 때 유료를 검토하세요. 인체형이면 AccuRIG, 무료 애니메이션이 필요하면 Mixamo가 기본이에요.

**goal**:
- 무료/유료 AI 리깅 도구를 분류한다
- 상황별 도구 선택 기준을 안다

**done**:
- 본인 프로젝트에 어떤 도구를 쓸지 정할 수 있다

**tasks**:
- 무료 5종(AccuRIG, Mixamo, Rigify, BlenRig, Cascadeur) 비교표 학습
- 유료 5종(Auto-Rig Pro, Meshy, Rodin, Everything Universe, iClone) 인지
- 선택 가이드 차트 학습

**참고**: docs/plans/2026-05-18-week11-12-rigging-restructure-design.md §6 카탈로그 표

---

### Step 2. AccuRIG 자동 리깅
**copy**: AccuRIG는 Reallusion의 무료 standalone 도구예요. FBX로 캐릭터를 내보내서 AccuRIG에 올리고 관절 마커를 맞추면 1분 만에 리깅이 끝나요. 결과를 다시 Blender로 임포트해요.

**goal**:
- AccuRIG로 캐릭터를 자동 리깅한다

**done**:
- 리깅된 캐릭터가 Blender에 임포트됐다

**tasks**:
- Blender → File → Export → FBX
- AccuRIG에 FBX 업로드
- 관절 마커(턱·손목·팔꿈치·무릎·사타구니) 맞추기
- Auto Rig 실행
- FBX export → Blender Import

**mistakes**:
- 업로드 실패 → 메쉬 단일화(Ctrl+J), 법선 정리(Shift+N)
- 스케일 어긋남 → Ctrl+A → All Transforms 미적용

---

### Step 3. Mixamo 애니메이션 적용
**copy**: Mixamo는 2500개 넘는 무료 애니메이션 라이브러리예요. 리깅된 캐릭터에 걷기·달리기·춤 같은 동작을 적용해서 다운로드해요.

**goal**:
- Mixamo에서 애니메이션을 골라 캐릭터에 적용한다

**done**:
- 캐릭터가 걷거나 뛰는 애니메이션이 재생된다

**tasks**:
- Mixamo.com에 캐릭터 FBX 업로드 (또는 AccuRIG 결과 사용)
- Animations 탭에서 동작 선택
- Download FBX (With Skin, Keyframe Reduction: None)
- Blender → File → Import → FBX
- Space로 재생

**mistakes**:
- 회전됨 → Import 설정 Manual Orientation, Forward: -Z, Up: Y
- 슬로우 모션 → Frame Rate 24fps 맞추기

---

### Step 4. Weight Paint 개념
**copy**: AI가 만든 결과가 완벽하지 않을 때가 있어요. 팔을 올렸는데 몸통이 같이 늘어난다면 Weight Paint로 영향 범위를 수정해요. 빨강은 강한 영향, 파랑은 영향 없음이에요.

**goal**:
- Vertex Group과 Weight 의미를 안다
- 빨강/파랑 색 코드를 안다

**done**:
- AI 리깅 결과에서 어색한 부위 1군데를 찾았다

**tasks**:
- Ctrl+Tab → Weight Paint Mode
- Properties → Vertex Groups에서 본별 그룹 확인
- Pose Mode로 가서 팔/다리 돌려보며 어색한 곳 체크

---

### Step 5. Weight Paint 부분 보정
**copy**: 문제 있는 부위 본의 Vertex Group을 선택하고 브러시로 칠해요. 빼고 싶으면 Ctrl+클릭으로 Subtract, 부드럽게 섞고 싶으면 Shift+클릭으로 Blur를 써요. Front Faces Only를 켜야 반대쪽이 같이 칠해지지 않아요.

**goal**:
- 특정 부위의 Weight를 수동 조정한다

**done**:
- 어색하던 부위가 자연스럽게 움직인다

**tasks**:
- Ctrl+Shift+클릭으로 본 선택 (Blender 4.0+ 단축키)
- Front Faces Only 켜기
- 브러시 Weight·Radius·Strength 조절
- 칠하기 → Pose Mode 확인 반복

**shortcuts**: Ctrl+Tab, Ctrl+Shift+LMB, F (Radius), Shift+F (Strength), Ctrl+LMB (Subtract), Shift+LMB (Blur)

**mistakes**:
- 반대쪽 같이 칠해짐 → Front Faces Only 체크
- Auto Normalize 끔 → 합 1 보장 안 됨, 다른 그룹 같이 확인
- Lock 무시됨 → Normalize All 사용 시 주의

---

### Step 6. NLA 시퀀스
**copy**: NLA(Non-Linear Animation)는 영상 편집 타임라인과 같아요. 키프레임 묶음 하나를 Action이라고 부르고, 여러 Action을 스트립으로 만들어 시간순으로 이어붙여 한 캐릭터의 긴 시퀀스를 만들어요. Mixamo에서 받은 걷기·인사·정지 클립을 연결할 때 써요.

**goal**:
- NLA의 개념을 안다
- 2개 이상 Action을 스트립으로 만들어 이어붙인다

**done**:
- 걷기 → 정지 → 인사 순서로 재생되는 시퀀스가 있다

**tasks**:
- Editor Type → Nonlinear Animation
- Action을 Push Down으로 스트립화
- 스트립 드래그로 시간 위치 이동
- 다음 Action을 새 스트립으로 추가
- Space로 시퀀스 재생

**shortcuts**: Push Down(NLA 헤더 버튼), G(스트립 이동), S(스트립 길이)

---

### W12 과제
- AccuRIG 또는 Mixamo로 리깅된 캐릭터
- Weight Paint 보정 전/후 비교 1군데
- 2개 이상 애니메이션 클립 NLA로 연결
- .blend 파일

### W12 explore
- 본인 캐릭터에 AccuRIG + Mixamo 워크플로우 한 번 더
- Meshy 무료 100 크레딧으로 모델→리깅 체험
- AI 리깅 결과 vs W11 수동 리깅 비교 메모

---

## 5. 흐름 검증

```
W10 키프레임 (오브젝트 단위)
   ↓
W11 Step1 Armature 개념 → 캐릭터는 본이 필요
   ↓
W11 Step2-4 수동 본 얹기 → 본질 체험
   ↓
W11 Step5-6 AI 도구 인지 + AI 학습 보조
   ↓
W12 Step1 AI 도구 카탈로그 → 선택 기준
   ↓
W12 Step2-3 AccuRIG + Mixamo → 본격 자동화
   ↓
W12 Step4-5 Weight Paint 보정 → AI 결과 다듬기
   ↓
W12 Step6 NLA 시퀀스 → 완성된 애니메이션
   ↓
W13 렌더링
```

W11 ↔ W12 연결점:
- W11에서 수동으로 본 만든 경험 → W12 AccuRIG 결과 본 구조 이해 가능
- W11에서 Pose Mode로 본 회전 → W12 NLA에서 Action 단위 조작 가능
- W11에서 AI 도구 인지 → W12 카탈로그 선택 가이드 자연 진입
- W12 Weight Paint는 "AI 결과 보정" 구체적 맥락 → 추상도 해소

---

## 6. AI 리깅 도구 카탈로그 (2026.05 검증)

### 무료

| 도구 | 검증 출처 | 장점 | 단점 |
|------|----------|------|------|
| **Reallusion AccuRIG 2.0** | actorcore.reallusion.com, CG Channel 2025.07 | 1분 자동 리깅. 전신+손가락+얼굴. 인체형+사족(beastmen·새). FBX/USD export. Blender Rigify 변환 무료 애드온. ActorCore 모션 라이브러리 통합(2025.07~) | Reallusion 계정 필요. 비유기체(차량·식물) 불가 |
| **Mixamo (Adobe)** | status.adobe.com 정상, 커뮤니티 보고 | 완전 무료·무한. 2500+ 애니메이션 라이브러리 | 2021년 이후 신규 기능 추가 없음(유지보수 모드). T-pose 단일 메쉬 강제. 인체형만. 손가락 없음 |
| **Blender Rigify (내장)** | docs.blender.org, CG Channel 2026.05 | Blender 5.0 내장. 메타리그 커스터마이즈. FK/IK + Bendy Bones. MetaHuman 호환 애드온(2026.05) 등장 | AI 아닌 휴리스틱. 메타리그 수동 배치 필수 |
| **BlenRig 6** | github.com/jpbouza/BlenRig | Interactive Rigging Assistant 50%+ 자동화. 사전 웨이트 메쉬. Blender Open Movies에서 검증 | 학습곡선. 한국어 자료 적음 |
| **Cascadeur Free** | cascadeur.com | AutoPosing 신경망 AI. FBX로 Blender 연동. 연수익 $100K↓ 무료 | 리깅 아닌 애니메이션 보조. 별도 앱. 상업 사용 시 유료 |

### 유료

| 도구 | 2026.05 가격 | 장점 | 단점 |
|------|------|------|------|
| **Auto-Rig Pro** | $40 일회성 (superhivemarket.com) | Blender 내부 작동. Mixamo 본 호환. 프로 워크플로우 표준 | 학생 부담. 영어 자료 |
| **Meshy** | Free 100크레딧/월, Pro 1000, Studio 4000 | 텍스트→3D + 자동 리깅 + 20~500개 애니메이션 라이브러리 | 100크레딧 ≈ 10개 모델. 캐릭터 품질 제한 |
| **Hyper3D Rodin** | Free $1.5/크레딧, Education $15/월, Creator $20-30/월, 7일 무료 체험 | Gen 2 T/A-pose 강제. 고품질 텍스처 | 정적 모델만 생성. 리깅·애니메이션 외부 도구 필요 |
| **Everything Universe (구 Anything World)** | 가격 비공개 B2B | 비인체형(동물·사물) AI 리깅. Blender 애드온 | 정보 부족. 2025 리브랜드 |
| **Reallusion iClone 8** | $599 일회성 | AccuRIG·ActorCore 생태계 통합. 얼굴/립싱크 | 학습 부담. Blender 별도 |

### 학생용 선택 가이드

| 상황 | 추천 |
|------|------|
| 인체형 캐릭터 처음 | AccuRIG 2.0 |
| 무료 애니메이션 풍부히 | Mixamo |
| Blender 안에서만 | Rigify 또는 BlenRig |
| 동물·로봇·식물 | 수동 + Rigify 메타리그 수정 |
| AI로 모델까지 생성 | Meshy (Free 100크레딧) |
| 졸업 후 실무 | Auto-Rig Pro $40 검토 |

---

## 7. 수정 위치

| 대상 | 위치 | 방법 |
|------|------|------|
| W11 step copy/tasks/goal/done | Notion (Week 11 페이지) | Notion MCP append/edit |
| W12 step copy/tasks/goal/done | Notion (Week 12 페이지) | Notion MCP append/edit |
| W11/W12 shortcuts, mistakes | Notion | Notion MCP |
| W12 status: upcoming → 새 구조 적용 | Notion | Notion MCP |
| showme 카드 ID 매핑 | overrides.json | Edit tool |
| 동기화 | `python3 tools/notion-sync.py --fetch-only` | Bash |

---

## 8. 검증 체크리스트

- [ ] W11 6개 step이 3시간 안에 소화 가능
- [ ] W12 6개 step이 3시간 안에 소화 가능
- [ ] W11 → W12 흐름이 끊김 없음
- [ ] Weight Paint 등장 맥락이 "AI 결과 보정"으로 자명
- [ ] AI 도구 카탈로그 무료/유료 분리 명확
- [ ] 2026.05 기준 가격·기능 검증 완료
- [ ] Blender 5.0 단축키와 일치
- [ ] CONTENT_GUIDE 톤(~해요/~이에요) 준수

---

## 9. 후속 단계

1. 이 design doc 사용자 리뷰
2. 승인 시 → writing-plans 스킬로 구체적 구현 계획 수립
3. 구현 계획에서 Notion 페이지별 수정 명세 작성
4. Notion MCP로 W11/W12 페이지 update
5. notion-sync로 curriculum.json 재생성
6. `/rpd-check week 11 week 12`로 검증
