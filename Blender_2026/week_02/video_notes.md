# Week 02: Blender 인터페이스 및 기초 — 영상 콘텐츠 노트

> 영상 제작 참고용. 각 클립의 핵심 내용, 다루는 기능, 추가 제작 아이디어를 정리합니다.

---

## A. 설치 & 시작 (클립 01–03)

### 01. Blender 다운로드
- **핵심**: blender.org 접속 → 운영체제별 설치 파일 다운로드
- **다루는 내용**:
  - blender.org 메인 페이지 구성
  - Windows / macOS / Linux 버전 선택
  - LTS(장기 지원) 버전 vs 최신 버전 차이
  - Steam 설치 vs 공식 다운로드 비교
- **추가 영상 아이디어**:
  - [ ] Blender 버전 업데이트 방법 (기존 설정 유지)
  - [ ] Portable 버전 사용법 (USB에 담아 사용)

### 02. Blender 설치하기
- **핵심**: 다운로드한 파일 실행 → 설치 과정
- **다루는 내용**:
  - macOS: DMG 마운트 → Applications 폴더로 드래그
  - Windows: MSI 설치 마법사 진행
  - 설치 경로 확인
- **추가 영상 아이디어**:
  - [ ] GPU 드라이버 설정 (NVIDIA/AMD 최적화)
  - [ ] 처음 실행 시 보안 경고 해결 (macOS Gatekeeper)

### 03. Blender 첫 실행
- **핵심**: Splash Screen, 기본 씬 구성, 초기 화면 파악
- **다루는 내용**:
  - Splash Screen 구성 요소 (최근 파일, Quick Setup)
  - Quick Setup: 언어, 단축키 프리셋, 테마 선택
  - 기본 씬: Camera, Cube, Light 3개 오브젝트
  - 3D Viewport 레이아웃 첫인상
- **추가 영상 아이디어**:
  - [ ] Preferences 초기 설정 가이드 (Undo Steps, Auto Save 등)
  - [ ] Startup File 커스텀 저장 (File > Defaults > Save Startup File)

---

## B. 인터페이스 & 도구 (클립 04–06)

### 04. 인터페이스 소개
- **핵심**: Blender UI의 4가지 주요 영역
- **다루는 내용**:
  - 3D Viewport — 메인 작업 공간
  - Outliner — 씬 오브젝트 목록 (레이어 패널)
  - Properties — 선택 오브젝트의 세부 설정
  - Timeline — 애니메이션 시간축
  - 각 영역의 에디터 타입 변경 방법 (좌상단 아이콘)
- **추가 영상 아이디어**:
  - [ ] 커스텀 Workspace 만들기 (Modeling, Sculpting, UV Editing 등)
  - [ ] 영역 분할/합치기 (드래그로 에디터 추가/제거)
  - [ ] Outliner 필터링 & 검색 기능

### 05. 인터페이스 심화
- **핵심**: 뷰포트 Header 핵심 컨트롤 + N 패널 + 네비게이션 기즈모
- **다루는 내용**:
  - Transform Orientation (Global, Local, Normal, View 등)
  - Pivot Point (Median, Individual Origins, 3D Cursor 등)
  - Snap (격자, Vertex, Edge, Face 스냅)
  - Proportional Editing (비례 편집, 감쇠 커브)
  - N 패널: Item/View/Tool 탭
  - 네비게이션 기즈모: 축 클릭, 원근/직교 전환
- **추가 영상 아이디어**:
  - [ ] Transform Orientation 실전 활용 (경사면 Extrude)
  - [ ] 3D Cursor 활용법 심화 (Shift+RightClick, Shift+S)
  - [ ] Custom Orientation 만들기

### 06. 도구상자 (Toolbox)
- **핵심**: T 패널 도구 팔레트와 주요 도구
- **다루는 내용**:
  - `T` 키로 Tool Shelf 열기/닫기
  - Select Box (W), Move (G), Rotate (R), Scale (S)
  - Transform 통합 도구
  - 단축키 vs 도구 팔레트 사용 차이
- **추가 영상 아이디어**:
  - [ ] Annotate 도구 (스케치 메모)
  - [ ] Measure 도구 (거리 측정)
  - [ ] 도구별 상단 옵션 바 설정

---

## C. 오브젝트 기본 조작 (클립 07–09)

### 07. 오브젝트 추가 (Add Object)
- **핵심**: Shift+A로 Primitive 오브젝트 추가
- **다루는 내용**:
  - Shift+A → Mesh 메뉴
  - Cube, UV Sphere, Ico Sphere, Cylinder, Cone, Torus
  - F9로 생성 직후 옵션 조절 (Segments, Rings, Size)
  - 추가 시 3D Cursor 위치에 생성되는 점 주의
- **추가 영상 아이디어**:
  - [ ] Curve, Text, Empty 등 비메시 오브젝트 추가
  - [ ] Add-on으로 커스텀 Primitive 추가 (Extra Objects)
  - [ ] 오브젝트 복제 (Shift+D) vs 링크 복제 (Alt+D) 차이

### 08. 오브젝트 편집 (Object Edit)
- **핵심**: Object Mode에서 G/R/S 기본 Transform
- **다루는 내용**:
  - G (이동), R (회전), S (스케일) 기본 조작
  - 축 제한: G+X, R+Z, S+Y 등
  - 숫자 입력으로 정밀 조작: R+Z+45+Enter
  - Shift+축키로 축 제외 이동
  - 우클릭/ESC로 취소, Enter/좌클릭으로 확정
- **추가 영상 아이디어**:
  - [ ] Apply Transform (Ctrl+A) 상세 설명
  - [ ] Origin 설정과 Pivot Point 활용
  - [ ] 정밀 이동: 숫자 입력 + N 패널 직접 입력

### 09. Tab 키로 모드 전환
- **핵심**: Object Mode ↔ Edit Mode 전환
- **다루는 내용**:
  - Tab 키 토글
  - Object Mode: 오브젝트 단위 조작
  - Edit Mode: 점(Vertex)/선(Edge)/면(Face) 편집
  - 1/2/3 키로 선택 모드 전환
  - 흔한 실수: 모드 혼동으로 오브젝트 전체가 이동
- **추가 영상 아이디어**:
  - [ ] Sculpt Mode 소개
  - [ ] Weight Paint / Texture Paint 모드 미리보기
  - [ ] 다중 오브젝트 Edit Mode (Ctrl+Tab으로 빠른 전환)

---

## D. Extrude & Bevel (클립 10–11)

### 10. Extrude & Inset
- **핵심**: E 키로 면 돌출, I 키로 면 내부에 새 면 생성
- **다루는 내용**:
  - Face 모드(3)에서 면 선택 → E로 Extrude
  - Region Extrude vs Extrude Individual Faces 차이
  - I 키로 Inset (면 안쪽에 패널 만들기)
  - ⚠️ Extrude 취소 시 중복 Vertex 문제 (ESC 대신 Ctrl+Z)
  - Extrude 후 방향 고정: E → Z (Z축으로만 돌출)
- **추가 영상 아이디어**:
  - [ ] Extrude Along Normals (면 법선 방향 돌출)
  - [ ] Inset Individual vs Region 차이
  - [ ] Extrude + Inset 조합으로 로봇 얼굴 디테일

### 11. Bevel 도구
- **핵심**: Ctrl+B로 모서리 깎기 (부드러운 모서리)
- **다루는 내용**:
  - Edge 선택 → Ctrl+B → 마우스로 Bevel 크기 조절
  - 마우스 스크롤로 Segment(분할) 수 조절
  - Segment 수에 따른 부드러움 변화
  - Vertex Bevel: Ctrl+Shift+B (꼭짓점 깎기)
  - Bevel Weight로 선택적 Bevel 적용
- **추가 영상 아이디어**:
  - [ ] Bevel Modifier vs 수동 Bevel 비교
  - [ ] Subdivision Surface와 Bevel 조합
  - [ ] Hard Surface 모델링에서 Bevel 활용법

---

## E. LoopCut & Knife (클립 12–14)

### 12. Loop Cut 기초
- **핵심**: Ctrl+R로 Edge Loop 추가
- **다루는 내용**:
  - Ctrl+R → 마우스 위치에 노란색 미리보기
  - 마우스 이동으로 Loop Cut 방향 결정
  - Left Click으로 위치 확정
  - Right Click으로 정확히 중앙에 고정
  - Loop Cut이 메시 형태에 따라 어떻게 흐르는지
- **추가 영상 아이디어**:
  - [ ] Edge Loop 선택 (Alt+Click)
  - [ ] Edge Ring 선택 (Ctrl+Alt+Click)
  - [ ] Loop Cut으로 관절 만들기 실전

### 13. Loop Cut 활용
- **핵심**: Loop Cut 개수 조절과 실전 활용
- **다루는 내용**:
  - 마우스 스크롤로 Loop Cut 개수 늘리기/줄이기
  - 복수 Loop Cut 간격 균등 배치
  - Loop Cut 위치 미세 조정 (슬라이드)
  - 실전: 로봇 팔/다리 관절 부분에 Edge Loop 추가
  - Loop Cut + Extrude 조합으로 디테일 추가
- **추가 영상 아이디어**:
  - [ ] Offset Edge Slide (간격 유지 슬라이드)
  - [ ] Edge Slide (G+G)로 기존 Loop 위치 조정
  - [ ] Loop Cut으로 Topology 개선

### 14. Knife 도구 ⚠️ (미업로드 — 쿼터 초과, 재시도 필요)
- **핵심**: K 키로 자유롭게 메시 분할
- **다루는 내용**:
  - K 키 → 좌클릭으로 절단 경로 지정 → Enter로 확정
  - 직선 절단 vs 자유곡선 절단
  - C 키: 각도 제한 (수직/수평/45도)
  - Z 키: 관통 절단 (뒤쪽 면까지)
  - Knife vs Loop Cut 사용 시기 비교
- **추가 영상 아이디어**:
  - [ ] Bisect 도구 (평면으로 반분할)
  - [ ] Knife Project (다른 오브젝트 형태로 절단)

---

## F. Join / Separate / Bridge (클립 15–17)

### 15. Join & Separate
- **핵심**: Ctrl+J로 오브젝트 합치기, P로 분리하기
- **다루는 내용**:
  - Object Mode에서 여러 오브젝트 선택 → Ctrl+J로 Join
  - Active Object 개념 (마지막 선택 = 이름/Origin 기준)
  - Edit Mode에서 P → Selection / By Material / By Loose Parts
  - Join ↔ Separate(By Loose Parts) 역연산 관계
  - Join 후 Origin 재설정 (Set Origin to Geometry)
- **추가 영상 아이디어**:
  - [ ] Boolean Union vs Join 차이 비교 (내부 면 유무)
  - [ ] 대량 오브젝트 정리: Select All → Join → Separate By Loose Parts

### 16. Bridge Edge Loops 기초
- **핵심**: 두 Edge Loop를 면으로 연결하기
- **다루는 내용**:
  - 두 파트를 같은 오브젝트로 합치기 (Ctrl+J)
  - 연결 부위의 면 삭제 (X → Faces)
  - Alt+클릭으로 Edge Loop 선택 → Shift+Alt+클릭으로 두 번째 선택
  - Edge 메뉴 → Bridge Edge Loops
  - Segments, Twist 옵션 조절
  - 버텍스 수가 다를 때 대처법
- **추가 영상 아이디어**:
  - [ ] Bridge로 터널/파이프 형태 만들기
  - [ ] Bridge vs Fill(F) 차이 비교
  - [ ] Grid Fill로 N-gon 면 정리

### 17. 실전: 로봇 팔-몸통 연결
- **핵심**: Join → Bridge → Loop Cut 실전 워크플로우
- **다루는 내용**:
  - 몸통과 팔을 각각 모델링 후 Ctrl+J로 합치기
  - 연결 부위 면 삭제 후 Bridge Edge Loops
  - Loop Cut으로 관절 디테일 추가
  - 완성 후 필요에 따라 Separate로 다시 분리
- **추가 영상 아이디어**:
  - [ ] 목-머리 연결, 다리-골반 연결 활용
  - [ ] Subdivision Surface 적용 시 Bridge 부위 형태 변화

---

## 추가 영상 제작 아이디어 (Week 02 보충)

### 단독 영상 후보
- [ ] **뷰 조작 마스터**: MMB 회전, Shift+MMB 이동, 스크롤 줌, Numpad 뷰 전환 집중 연습
- [ ] **Apply Transform 완전 정복**: Scale (1,1,1)이 아닌 경우의 문제점 실제 시연
- [ ] **3D Cursor 활용법**: Shift+RightClick 배치, Shift+S 스냅 메뉴, Cursor to World Origin
- [ ] **Emulate 설정 가이드**: 노트북 사용자를 위한 Numpad/3Button Mouse 에뮬레이트
- [ ] **선택 기법 총정리**: Box(B), Circle(C), Lasso(L), Linked(L), Select All(A) 등
- [ ] **Merge & Clean Up**: 중복 Vertex 제거, Dissolve, Fill, Grid Fill
- [ ] **Normal 방향 이해**: Face Normal 시각화, Recalculate Outside (Shift+N)

### 시리즈 확장 후보
- [ ] Object Mode 심화: 복제(Shift+D), 링크복제(Alt+D), Join(Ctrl+J), Separate(P)
- [ ] Edit Mode 심화: Vertex/Edge/Face 메뉴 주요 기능
- [ ] Modifier 기초: Subdivision Surface, Mirror, Array
- [ ] Material 기초: Principled BSDF, 색상 지정, 간단한 재질
