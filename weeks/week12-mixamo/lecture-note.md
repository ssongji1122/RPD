# Week 12: AI 활용 리깅 (Mixamo)

## 🔗 이전 주차 복습

> **Week 11에서 수동 리깅(Manual Rigging)을 직접 경험했습니다.**
> Bone을 하나하나 배치하고, Weight Painting을 수동으로 조정하는 과정이 얼마나 시간이 걸리는지 체감했을 것입니다.
> 이번 주에는 **AI 자동 리깅(Mixamo)**을 사용하여 같은 작업을 몇 분 만에 처리하는 방법을 배웁니다.
>
> **비교해보세요:**
> | 항목 | Week 11 수동 리깅 | Week 12 Mixamo 자동 리깅 |
> |------|------------------|------------------------|
> | Bone 배치 | 직접 하나씩 추가/정렬 | AI가 자동 배치 (마커 5개만 지정) |
> | Weight Painting | 수동 조정 필요 | 자동 처리 |
> | 소요 시간 | 1~3시간 | 5~10분 |
> | 커스터마이징 | 자유도 높음 | 제한적 (표준 스켈레톤) |
> | 애니메이션 | 직접 제작 필요 | 2000개+ 라이브러리 즉시 활용 |

## 학습 목표

- [ ] Mixamo 자동 리깅의 원리와 사용법을 이해한다
- [ ] Mixamo 애니메이션 라이브러리를 탐색하고 적용할 수 있다
- [ ] FBX 포맷으로 Blender와 Mixamo 간 데이터를 주고받을 수 있다
- [ ] NLA Editor를 사용하여 여러 애니메이션을 조합할 수 있다

## 이론 (30분)

### Mixamo란?

- **Adobe에서 제공하는 무료 웹 서비스** (Adobe 계정만 있으면 사용 가능)
- 두 가지 핵심 기능:
  1. **자동 리깅 (Auto-Rigging):** 3D 캐릭터를 업로드하면 AI가 자동으로 Bone 배치
  2. **애니메이션 라이브러리:** 2000개 이상의 모션 캡처 기반 애니메이션 무료 제공
- 웹 주소: https://www.mixamo.com
- 상업적 사용 가능 (Adobe 이용 약관 참조)

### Mixamo 계정 준비

- Adobe 계정 필요 (무료 가입 가능)
- https://www.mixamo.com 접속 > Sign Up 또는 Log In
- 별도의 소프트웨어 설치 불필요 (웹 브라우저에서 모든 작업 가능)

### 자동 리깅 원리

- AI가 업로드된 3D 모델의 **인체 구조를 인식**하여 Bone을 자동 배치
- 약 65개의 Bone으로 구성된 표준 인체 스켈레톤 생성
- 사용자가 주요 관절 위치를 마커로 지정하면 AI가 나머지를 자동 추론
- 마커 위치: Chin (턱), Wrists (손목), Elbows (팔꿈치), Knees (무릎), Groin (사타구니)
- Weight Painting도 자동으로 처리

### Mixamo 모델 요구사항

업로드할 모델이 아래 조건을 만족해야 자동 리깅이 성공한다:

- **T-Pose:** 팔을 양옆으로 벌린 T자 자세 (가장 중요)
- **사지 분리:** 팔, 다리, 머리가 몸통에서 명확히 분리
- **Mesh 깨끗:** 구멍, 겹침, 비정상 면(Non-Manifold)이 없어야 함
- **단일 Mesh:** 여러 파츠가 있으면 하나로 합치는 것을 권장 (Join: Ctrl+J)
- **적절한 Polygon 수:** 너무 많으면 처리가 느리고 실패할 수 있음 (10만 폴리곤 이하 권장)
- **기존 Armature 제거:** Armature가 있으면 삭제 후 업로드

> **로봇의 경우:** 인체형 로봇은 Mixamo가 잘 작동하지만, 비인체형(4족, 다리 없음 등)은 자동 리깅이 어려울 수 있음

### FBX 포맷

- **FBX (Filmbox):** 3D 데이터 교환 표준 포맷
- Autodesk에서 개발, 업계에서 가장 널리 사용되는 교환 포맷
- 포함 가능한 데이터: Mesh, Material, Armature, Animation, Camera, Light
- Mixamo는 FBX 포맷으로 입출력
- Blender에서 FBX 내보내기/가져오기 모두 지원

### Blender에서 FBX 내보내기 설정

Mixamo에 업로드하기 위한 FBX Export 설정:

- File > Export > FBX (.fbx)
- **Path Mode:** Copy (텍스처 포함 시)
- **Include:** Selected Objects (선택한 오브젝트만) 또는 전체
- **Transform:**
  - Scale: 1.0 (또는 모델 크기에 따라 조정)
  - Apply Scalings: All Local
  - Forward: -Z Forward
  - Up: Y Up
- **Geometry:**
  - Apply Modifiers: 체크 (Mirror, Subdivision 등 적용)
- **Armature:** 기존 Armature가 있으면 제외하거나 삭제 후 Export

### NLA (Non-Linear Animation) Editor

- **NLA Editor:** 여러 애니메이션(Action)을 블렌딩하고 시퀀싱하는 도구
- Timeline 위의 상위 레이어에서 애니메이션 클립을 관리
- 비선형(Non-Linear): 순서를 자유롭게 바꾸고, 반복하고, 겹칠 수 있음

**핵심 개념:**

- **Action:** 하나의 애니메이션 데이터 (예: 걷기, 뛰기, 인사)
- **NLA Strip:** Action을 NLA Editor에 배치한 클립
- **Stash:** 현재 Action을 NLA에 저장하고 새 Action을 시작
- **Blend In/Out:** 두 Strip이 겹치는 구간에서 부드럽게 전환

**NLA Editor 열기:**
- Editor Type > NLA Editor (또는 Shift+F12, 설정에 따라 다름)
- Timeline 영역 좌측 상단의 Editor Type 드롭다운에서 선택

## 실습 (90분)

### Blender에서 로봇 모델 FBX 내보내기 (15분)

#### 모델 준비

1. 자신의 로봇/캐릭터 모델 파일 열기
2. 모델 상태 점검:
   - T-Pose인지 확인 (아니면 Pose Mode에서 T-Pose로 조정)
   - 여러 파츠가 있으면 Ctrl+J로 하나의 Mesh로 합치기
   - 기존 Armature가 있으면 선택 후 X로 삭제
3. 모델 크기 확인: N 패널 > Dimensions가 적절한지 확인 (너무 크거나 작으면 조정)
4. Apply All Transforms: Ctrl+A > All Transforms (위치, 회전, 스케일 적용)

#### FBX 내보내기

1. File > Export > FBX (.fbx) 선택
2. 파일 이름 지정 (예: my_robot_for_mixamo.fbx)
3. 설정 확인:
   - Include: Selected Objects 또는 전체
   - Transform > Apply Scalings: All Local
   - Geometry > Apply Modifiers: 체크
4. Export FBX 클릭

> **💡 프로 팁: FBX Export 전 필수 체크**
> - 반드시 `Ctrl+A > All Transforms`를 적용한 후 Export하세요. Apply Transform을 하지 않으면 Mixamo에서 모델 크기나 방향이 틀어집니다.
> - 여러 파츠로 나뉜 모델은 반드시 `Ctrl+J`로 Join 후 Export하세요. Mixamo는 단일 Mesh를 기대합니다.

### Mixamo 업로드 및 자동 리깅 (15분)

#### Mixamo 접속 및 업로드

1. 웹 브라우저에서 https://www.mixamo.com 접속
2. Adobe 계정으로 로그인
3. 우측 상단 **Upload Character** 버튼 클릭
4. 내보낸 FBX 파일을 드래그 앤 드롭 또는 파일 선택으로 업로드
5. 업로드 완료까지 대기 (모델 크기에 따라 1~5분)

#### 마커 배치

1. 업로드가 완료되면 마커 배치 화면이 나타남
2. 5개의 마커를 올바른 위치에 배치:
   - **Chin:** 턱 위치
   - **Wrists:** 양쪽 손목 위치 (2개)
   - **Elbows:** 양쪽 팔꿈치 위치 (2개)
   - **Knees:** 양쪽 무릎 위치 (2개)
   - **Groin:** 사타구니 (다리 사이 중심점)
3. 마커를 정확하게 배치해야 리깅 품질이 높아짐
4. **Next** 클릭

#### 리깅 설정

1. Skeleton 옵션 확인:
   - **Use No Fingers:** 손가락 Bone 제외 (간단한 모델에 적합)
   - **Use Fingers:** 손가락 Bone 포함 (손가락이 있는 모델)
2. 프리뷰에서 자동 리깅 결과 확인
3. 모델이 올바르게 움직이는지 확인
4. 문제가 있으면 마커 위치를 수정하고 다시 시도

### 애니메이션 적용 (15분)

#### 애니메이션 탐색

1. 리깅이 완료되면 좌측에 **Animations** 패널이 표시됨
2. 검색창에 키워드 입력으로 원하는 애니메이션 찾기:
   - **Walking:** 걷기
   - **Running:** 뛰기
   - **Dancing:** 춤추기
   - **Waving:** 인사 (손 흔들기)
   - **Idle:** 대기 자세
   - **Fighting:** 전투 동작
   - **Jumping:** 점프
3. 애니메이션을 클릭하면 즉시 프리뷰에서 확인 가능

#### 애니메이션 설정 조정

1. 마음에 드는 애니메이션 선택
2. 우측 설정 패널에서 조정:
   - **Character Arm-Space:** 팔의 기본 각도 조정 (T-Pose와 모델의 팔 각도 차이 보정)
   - **Trim:** 애니메이션의 시작/끝 구간 자르기
   - **Speed:** 재생 속도 조절
   - **Overdrive:** 동작의 과장 정도
   - **In Place:** 제자리 애니메이션 (이동 없이 동작만)
3. 최소 2개의 서로 다른 애니메이션을 선택하여 적용해 볼 것

> **💡 프로 팁: "In Place" 옵션 활용**
> - Mixamo 애니메이션 설정에서 **"In Place"** 체크박스를 켜면 캐릭터가 제자리에서 동작합니다.
> - 나중에 Blender에서 직접 이동 경로를 제어하고 싶을 때 유용합니다.
> - Root Motion이 포함된 애니메이션은 NLA에서 위치가 겹쳐서 충돌할 수 있으므로, 처음에는 "In Place"로 다운로드하는 것을 권장합니다.

### FBX 다운로드 및 Blender 임포트 (15분)

#### Mixamo에서 다운로드

1. 원하는 애니메이션이 적용된 상태에서 **Download** 버튼 클릭
2. Download Settings:
   - **Format:** FBX
   - **Skin:** With Skin (메쉬 포함)
   - **Frames per Second:** 30
   - **Keyframe Reduction:** Uniform (기본값)
3. Download 클릭하여 FBX 파일 저장
4. 다른 애니메이션도 같은 방법으로 다운로드
   - 두 번째 애니메이션부터는 **Skin: Without Skin**으로 다운로드 (메쉬 중복 방지)

#### Blender에서 임포트

1. Blender에서 새 파일 또는 기존 파일 열기
2. File > Import > FBX (.fbx) 선택
3. 다운로드한 FBX 파일 선택
4. Import 설정:
   - Automatic Bone Orientation: 체크 권장
   - Scale: 필요에 따라 조정 (Mixamo 모델이 너무 크거나 작을 수 있음)
5. Import FBX 클릭
6. 임포트된 모델과 Armature 확인
7. Space로 애니메이션 재생하여 동작 확인

> **💡 프로 팁: FBX Import 설정**
> - **Automatic Bone Orientation** 옵션을 반드시 체크하세요. Mixamo의 Bone 방향이 Blender 기본값과 다르기 때문에, 이 옵션 없이 임포트하면 Bone 방향이 뒤틀릴 수 있습니다.
> - 두 번째 애니메이션부터는 **Without Skin**으로 다운로드했으므로, 기존 Armature에 Action만 추가됩니다.

### NLA Editor에서 애니메이션 관리 (20분)

#### Action 확인

1. 임포트된 Armature 선택
2. Dope Sheet Editor 열기 > 모드를 Action Editor로 변경
3. 현재 할당된 Action 확인 (예: "mixamo.com" 또는 애니메이션 이름)
4. Action 이름을 알아보기 쉽게 변경 (예: "Walk", "Dance")

#### NLA Strip으로 변환

1. Editor Type을 **NLA Editor**로 변경
2. 현재 Action 옆의 **Push Down** 버튼(아래 화살표 아이콘) 클릭
   - Action이 NLA Strip으로 변환됨
   - Strip이 NLA Editor의 트랙에 나타남
3. 두 번째 애니메이션 FBX를 추가로 임포트
4. Action Editor에서 새로운 Action 확인 > Push Down

#### 여러 애니메이션 이어 붙이기

1. NLA Editor에서 두 개의 Strip이 보이는지 확인
2. Strip을 드래그하여 순서 배치:
   - 첫 번째 Strip: 걷기 (예: Frame 1~60)
   - 두 번째 Strip: 인사 (예: Frame 61~120)
3. Strip 간 겹치는 구간 만들기:
   - 두 번째 Strip을 첫 번째 Strip 끝 부분과 약간 겹치게 배치
   - 겹치는 구간에서 **Blend In/Out**이 자동으로 적용되어 부드러운 전환

#### Blend In/Out 설정

1. Strip 선택 > N 패널 > Strip 탭
2. **Blend In:** 전환 시작 프레임 수 (0에서 서서히 시작)
3. **Blend Out:** 전환 끝 프레임 수 (서서히 사라짐)
4. 값을 조정하여 전환 부드러움 정도 제어
5. **Extrapolation:** Strip 끝난 후 동작
   - **Nothing:** 정지
   - **Hold:** 마지막 프레임 유지
   - **Hold Forward:** 다음 Strip까지 유지

### 완성된 애니메이션 재생 및 조정 (10분)

1. Timeline에서 전체 프레임 범위 설정 (Start: 1, End: 최종 프레임)
2. Space로 전체 애니메이션 재생
3. 확인 사항:
   - 애니메이션 간 전환이 자연스러운지
   - 메쉬가 깨지거나 이상한 변형이 없는지
   - 속도와 타이밍이 적절한지
4. 필요 시 Strip 위치, 길이, Blend 값 조정
5. 결과물 확인 후 Viewport에서 스크린샷 또는 렌더

## ⚠️ 흔한 실수와 해결법

### 실수 1: FBX Export 시 Apply Transform 미적용

- **증상:** Mixamo에 업로드한 모델이 매우 작거나, 방향이 틀어져 있음
- **원인:** Blender에서 `Ctrl+A > All Transforms`를 적용하지 않고 Export
- **해결:** Export 전 반드시 오브젝트를 선택하고 `Ctrl+A > All Transforms` 실행. Scale이 (1, 1, 1)인지 확인

### 실수 2: Mixamo에서 캐릭터 인식 실패

- **증상:** "We couldn't rig your character" 오류 메시지, 또는 마커 배치 화면이 나오지 않음
- **원인:** 모델이 T-Pose가 아니거나, 여러 Mesh로 분리되어 있거나, Polygon 수가 너무 많음
- **해결:**
  - T-Pose 확인: 팔을 양옆으로 뻗은 자세인지 확인
  - 단일 Mesh: 모든 파츠를 선택하고 `Ctrl+J`로 Join
  - Polygon 수 줄이기: Decimate Modifier로 10만 폴리곤 이하로 줄이기
  - 기존 Armature가 있으면 반드시 삭제 후 업로드

### 실수 3: NLA Editor에서 Strip 겹침으로 애니메이션 충돌

- **증상:** 두 애니메이션이 동시에 재생되어 모델이 이상하게 뒤틀림
- **원인:** NLA Strip이 같은 프레임 범위에 겹쳐 있어 블렌딩이 의도치 않게 발생
- **해결:**
  - NLA Editor에서 Strip이 겹치지 않도록 타임라인상 순서대로 배치
  - 의도적으로 겹치는 경우에만 Blend In/Out 값을 설정
  - Strip 선택 > N 패널에서 Extrapolation을 "Nothing"으로 설정하여 Strip 종료 후 영향 제거

### 실수 4: Mixamo 애니메이션의 Root Motion 처리 문제

- **증상:** 캐릭터가 걷기 애니메이션에서 한 방향으로 계속 이동하여 씬 밖으로 나감
- **원인:** Mixamo 애니메이션에 Root Motion(위치 이동 데이터)이 포함되어 있음
- **해결:**
  - Mixamo에서 다운로드 시 **"In Place"** 옵션 활성화
  - 이미 다운로드한 경우: Blender에서 Graph Editor를 열고 Root Bone의 Location 키프레임을 삭제

### 실수 5: 임포트 후 모델 크기가 맞지 않음

- **증상:** Mixamo에서 돌아온 모델이 기존 씬과 크기가 다름
- **원인:** Mixamo는 자체적으로 모델 크기를 정규화하며, FBX Import 시 Scale 설정이 다를 수 있음
- **해결:** Import 시 Scale 값을 조정하거나, Import 후 `S` 키로 크기를 맞추고 `Ctrl+A > Scale` 적용

## 핵심 정리

| 개념 | 핵심 내용 |
|------|----------|
| Mixamo | Adobe 무료 자동 리깅 + 애니메이션 라이브러리 |
| 자동 리깅 | AI가 인체 구조 인식, 마커 5개 배치로 Bone 자동 생성 |
| 모델 요구사항 | T-Pose, 사지 분리, 깨끗한 Mesh, 단일 오브젝트 |
| FBX | 3D 데이터 교환 표준 포맷, Mesh + Armature + Animation 포함 |
| NLA Editor | 여러 애니메이션을 비선형으로 블렌딩/시퀀싱하는 도구 |
| Action | 하나의 애니메이션 데이터 단위 |
| NLA Strip | Action을 NLA Editor에 배치한 클립 |
| Blend In/Out | 두 Strip 간 부드러운 전환 |

### 핵심 단축키 / 조작

| 동작 | 방법 |
|------|------|
| FBX 내보내기 | File > Export > FBX |
| FBX 가져오기 | File > Import > FBX |
| Action Editor | Dope Sheet > Action Editor 모드 |
| NLA Editor 열기 | Editor Type > NLA Editor |
| Push Down | NLA Editor에서 Action을 Strip으로 변환 |
| Strip 이동 | NLA Editor에서 Strip 드래그 |
| 애니메이션 재생 | Space |

## 다음 주 예고

**Week 13: 렌더링 + AI 영상/사운드**
- Cycles / EEVEE 렌더 엔진 비교
- 카메라 설정 및 렌더 세팅
- AI 영상 생성 도구 활용
- AI 사운드/음악 생성 도구 활용
- 최종 프로젝트를 위한 영상 제작 기초

## 📋 프로젝트 진행 체크리스트

이번 주차 실습이 끝나면 아래 항목을 확인하세요:

- [ ] Blender에서 FBX Export가 정상적으로 완료되었는가
- [ ] Mixamo에서 자동 리깅이 성공적으로 완료되었는가
- [ ] 최소 2개 이상의 서로 다른 애니메이션을 적용해 보았는가
- [ ] FBX를 Blender로 다시 Import하여 애니메이션이 재생되는가
- [ ] NLA Editor에서 2개 이상의 애니메이션을 Strip으로 조합하였는가
- [ ] Strip 간 전환(Blend In/Out)이 자연스러운가
- [ ] 최종 결과물을 Viewport에서 확인하고 스크린샷 또는 영상으로 저장했는가
- [ ] (기말 프로젝트 대비) 자신의 로봇 모델에 Mixamo 리깅을 적용할 계획이 있는가

> **기말 프로젝트 연결:** 이번 주 Mixamo 리깅 결과물은 Week 14~15 최종 프로젝트의 핵심 요소가 됩니다. 자신의 로봇 모델로 반드시 실습해두세요.

<!-- AUTO:CURRICULUM-SYNC:START -->
## 커리큘럼 연동 요약

> 이 섹션은 `course-site/data/curriculum.js` 기준으로 자동 갱신됩니다.

- 핵심 키워드: Mixamo 자동 리깅 · 애니메이션 임포트
- 예상 시간: ~3시간

### 실습 단계

#### 1. Mixamo 업로드

AI가 파일을 불러와서 자동으로 뼈대를 넣어줘요. 수동으로 본을 하나하나 넣던 시간이 없어져요.

배울 것

- Mixamo 워크플로우를 안다

체크해볼 것

- Blender에서 .obj 또는 .fbx 익스포트
- Mixamo.com 에 파일 업로드
- 자동 리깅 후 확인

#### 2. 애니메이션 다운로드 및 임포트

Mixamo에서 걷기, 달리기, 춤추기 등 애니메이션을 골라서 Blender로 가져와요.

배울 것

- FBX 임포트 방식을 안다

체크해볼 것

- Mixamo에서 애니메이션 선택 후 FBX 다운로드
- Blender → File → Import → FBX
- Dope Sheet에서 애니메이션 재생 확인

### 과제 한눈에 보기

- 과제명: AI 리깅 캐릭터 애니메이션
- 설명: Mixamo로 리깅된 캐릭터의 애니메이션이 재생되는 Blender 파일과 렌더 영상.
- 제출 체크:
  - 애니메이션 재생 영상 or GIF
  - .blend 파일

### 자주 막히는 지점

- FBX 임포트가 회전됨 → Import 설정에서 Forward/Up 방향 확인
<!-- AUTO:CURRICULUM-SYNC:END -->

## 참고 자료

- [Mixamo](https://www.mixamo.com) - Adobe 자동 리깅 및 애니메이션
- [Blender Manual: NLA Editor](https://docs.blender.org/manual/en/latest/editors/nla/index.html)
- [Blender Manual: FBX Import/Export](https://docs.blender.org/manual/en/latest/files/import_export/fbx.html)
