# 포트폴리오 웹페이지 만들기 — 통합 가이드 (초안)

> **이 초안의 목적**: `Portfolio page 만들기`(Week 14 하위)에 들어갈 **단일 가이드(SSoT)**. Week 14 본문에 흩어져 있던 "웹페이지 제작 참고 자료"(도구표·프롬프트·레퍼런스·배포)를 여기로 흡수해 중복·불일치를 없앴습니다.
> **적용 후 Week 14 본문**에는 「선택 가산점: 포트폴리오 웹페이지」 안내 + 발표 섹션 구조 + **이 페이지 링크**만 남깁니다 (아래 §8 참고).
> 무료 한도는 **2026-06-08 기준** — 수업 당일 각 사이트에서 재확인.

---

## 0. 먼저 샘플부터 만져보기

- **사다리타기 샘플**: https://ssongji1122.github.io/RPD/ladder-sample.html — "프롬프트 → 작동 페이지"가 뭔지 1분이면 감이 와요.
- **학생 데이터로 만든 포트폴리오 샘플**: https://hyorin.vercel.app — Claude Code로 학생 노션 페이지 데이터 + 레퍼런스 이미지를 주고 생성.

---

## 1. 어떤 툴로 만들까

> 프롬프트만으로 웹페이지를 만드는 "바이브코딩" 도구. 다 "말로 설명하면 만들어주는" 빌더예요. 보여줄 작품은 이미 배운 툴(Blender·Meshy·Kling·Suno·Mixamo 등)로 만든 걸 올립니다. 정답은 하나가 아니니 두세 개 찍어보고 손에 맞는 걸 고르세요.

### 바로 무료로 시작 (계정·카드 기준)

| 도구 | 유형 | 무료 한도 (2026-06-08) | 강점 |
|------|------|----------------------|------|
| Google AI Studio | 프롬프트 → 앱 | 완전 무료, 카드 불필요 | 진입장벽 최저. Cloud Run 원클릭 배포 |
| Google Stitch | UI 디자인 시안 | 무료(Google Labs), 하루 약 400 크레딧 | 비주얼·레이아웃 먼저 잡기. React 코드 export |
| bolt.new | 프롬프트 → 풀스택 | 무료 월 100만 토큰(하루 30만) | 브라우저에서 앱~호스팅까지(Bolt 배지) |
| Lovable | 프롬프트 → 웹앱 | 무료 하루 5크레딧(월 최대 30) | 가장 쉬운 대화형. 한도 작아 큰 골격 위주 |
| Replit | 앱+호스팅 올인원 | Starter: Agent 크레딧 제한, 앱 1개 게시 | 코드·DB·배포를 한 곳에서 |
| v0 (Vercel) | UI/컴포넌트 생성 | 월 $5 크레딧 + 하루 7메시지 | React/Next UI, Vercel 배포 |
| Claude Artifacts | 대화 → HTML 즉석 | claude.ai 무료 티어 | 채팅 중 랜딩·위젯 즉석 렌더 |
| Google Antigravity | 에이전트 IDE | 개인 public preview 무료 | 파일·코드 직접 다루는 IDE(중급+) |

### 유료 구독 필요 (무료 체험 제한적)

| 도구 | 무료 체험 | 강점 / 비고 |
|------|----------|------------|
| Figma Make | Starter 월 500크레딧(하루 150) | Figma 디자인을 앱으로. 본격 사용은 유료 |
| Claude Code | Claude Pro 월 $20 포함 | 터미널 에이전트, 파일 수정·배포까지. 제어·품질 최상 |
| Codex (OpenAI) | ChatGPT Plus 월 $20 포함 | 터미널·클라우드 에이전트 코딩 |
| Claude Design | Claude Pro/Max research preview | 대화형 디자인(시안·슬라이드·목업), 2026-04 출시 |

> OpenDesign (Claude Design 오픈소스 대안, 무료): https://github.com/opendesigntool/opendesign

**처음이라면 추천 흐름**: ① 디자인 감 잡기 → Google Stitch · ② 프롬프트로 한 번에 → Google AI Studio 또는 bolt.new · ③ 코드까지 다듬기 → Claude Code 또는 Antigravity · ④ 배포 → Netlify Drop/툴 내장 → 공개 URL을 학생 페이지에 연결.

---

## 2. 만들기 전에 — 이 한 줄을 꼭

브리핑(첫 지시) 끝에 이 문장을 붙이면 결과가 확 좋아져요.

> "만들기 전에, 명확히 하기 위한 질문을 먼저 해줘."

AI가 바로 안 만들고 이름·섹션·분위기를 먼저 물어봐요. 여기 답을 잘 할수록 나중에 고칠 게 줄어요.

---

## 3. 프롬프트 (복사해서 순서대로)

> 목표는 베끼기가 아니라 **자기 작품에 맞는 페이지**를 만드는 거예요. 아래 프롬프트로 구조부터 잡고, 색·폰트·분위기는 작품에 맞게 바꾸세요. (귀여운 캐릭터와 시네마틱 로봇은 어울리는 디자인이 다릅니다.)

### 압축 버전

① 기획/구조용
```
[작업 페이지 링크] 작업들을 흐름대로 보여주는 포트폴리오를 [레퍼런스 페이지 링크] 느낌으로 만들 거야. 내용 분석 후 섹션 구조와 카피 초안을 먼저 제안해줘. 섹션명·버튼·카피는 실제 포트폴리오 웹사이트에서 자주 쓰는 용어·표현으로 정리해줘.
```

② 코드 생성용
```
위 구조로 단일 index.html(인라인 CSS·JS)로 1페이지 포트폴리오를 만들어줘. sticky 네비, 스크롤 active 하이라이트, 이미지 클릭 모달, before/after 블록, 인쇄 모드 토글 포함.
```

### 세밀 버전

① 마스터 프롬프트 (분석 → 기획 → 구조)
```
[역할] 너는 시니어 포트폴리오 디자이너이자 프론트엔드 개발자야.
[목표] [작업 페이지 링크] 작업들을 '기획 → 과정 → 결과 → 회고' 흐름으로 보여주는 1페이지 포트폴리오.
[무드] 레퍼런스 페이지처럼. 넉넉한 여백, 큰 타이포.
[작업] 1) 작업 분석해 핵심 메시지 정리 2) 섹션 구조(Hero/Overview/Process/Final/Reflection) 제안 3) 각 섹션 카피 초안 4) 필요한 이미지 목록. 먼저 구조·카피만 제안하고 확정 후 코드를 만들자.
```

② Claude Code 프롬프트
```
[작업 페이지 링크] 작업 내용으로 단일 index.html(인라인 CSS·JS)을 만들어줘. 내 작품 톤에 맞는 색·폰트로. 먼저 구조·카피를 제안하고, 확정 후 코드.
```

③ Stitch 보조
```
다크·미니멀 1페이지 포트폴리오 UI. 섹션: Hero, Overview, Process(타임라인), Final, Reflection. 큰 타이포, 넉넉한 여백, accent #7c9cff.
```

④ Claude Design 보조
```
위 Stitch 시안을 반응형 컴포넌트로 정리해줘. 모바일에서 네비는 가로 스크롤, 이미지 그리드는 1열.
```

### 영문 HTML 프롬프트 (캐릭터 프로젝트용)
```
Create a one-page responsive HTML portfolio website for my final character project.
Show the full process: ideation, AI image generation, 3D modeling, material and texture,
rigging, animation, final renders, and reflection.
Style: cinematic dark tech portfolio, large visual sections, clean typography, responsive mobile.
Use placeholder areas for images and one MP4 animation video.
```

---

## 4. 레퍼런스 — 잘 만든 것 먼저 보기

> 만들기 전에 잘 만든 페이지를 먼저 보면 결과가 달라집니다. 레이아웃·여백·타이포를 눈에 익히고, 마음에 드는 섹션을 스크린샷으로 모아두세요.

**비주얼 레퍼런스 (빠르게 많이)**: Dribbble · Pinterest · Behance · Mobbin
**랜딩·웹 갤러리 (섹션 구조)**: Awwwards · Godly · Land-book · Lapa Ninja · One Page Love · SaaS Landing Page
**타이포·레이아웃 디테일**: Typewolf · Fonts In Use
**3D·캐릭터 포트폴리오 (수업 맥락)**: ArtStation · The Rookies · Bruno Simon · Sketchfab

---

## 5. 스스로 점검 — 8가지 기준

다 만들었으면 AI에게:
> "이 포트폴리오를 아래 8가지 기준으로 솔직하게 평가해줘. 각 항목이 강함/보통/부족 중 어디인지, 부족한 건 뭘 더 하면 좋은지 알려줘."

관점(누구에게) · 타이포그래피 · 색상 · 계층 구조(시선 순서) · 이미지 · 모션 · 모바일 · 로딩 속도

> 부족한 곳은 하나씩 말고 "좀 더 완성도 있어 보이게 5가지 정도 묶어서 제안해줘"처럼 의도만 전하면 묶음으로 고쳐줘요.

---

## 6. 공개하기 — 배포

미리보기 주소(localhost)는 내 컴퓨터에서만 열려요. 공개 URL 하나가 나오면 끝.

- **툴 내장 배포 (가장 쉬움)**: bolt.new·Lovable·v0는 "Publish/Deploy" 버튼만 누르면 공개 주소.
- **Netlify Drop**: 로컬 파일로 나온 경우(예: Claude Code). app.netlify.com/drop 에 **폴더 안의 파일들**을 드래그&드롭(폴더째 X). 첫 배포는 로그인도 불필요.
- **GitHub Pages**: 깃을 쓸 줄 알면. 무료 플랜은 public 레포만.

그다음 공개 URL을 본인 학생 페이지에 연결하면 제출 완료. 폴더 압축 시 **폴더 안의 파일들**을 압축(폴더째 압축하면 빈 페이지).

---

## 7. 자주 막히는 것

- **이미지가 안 떠요** → 만료되는 외부 링크 말고, 이미지 파일을 프로젝트 폴더에 직접 넣어요.
- **자꾸 깨져요** → 포기 말고 "뭐가 잘못됐고 뭘 기대했는지" 설명. AI에게 살펴볼 기회를 주면 대부분 고쳐져요.
- **AI 티가 나요** → 'Inter' 폰트가 보이면 다른 폰트로. 카피도 형용사 빼고 짧게.

---

## (선택) 막힐 때 — 베이스 코드

> **기본은 각자 스타일입니다.** 프롬프트로 자기 작품에 맞는 페이지를 만드는 게 목표예요. 아래 베이스는 *코딩이 막막하거나 시간이 없을 때만* 출발점으로 쓰세요. 쓰더라도 **색·폰트·섹션 구조는 꼭 자기 작품에 맞게** 바꿔야 합니다 — 안 그러면 다들 똑같아 보여서 포트폴리오의 의미가 없어요.

<details>
<summary>베이스 index.html 펼쳐보기 (다크·미니멀 · sticky 네비 + 이미지 모달 + 인쇄 모드)</summary>

기존 Portfolio page의 `index.html` 코드 블록을 그대로 유지합니다. (길어서 초안에선 표기만 — Notion 적용 시 실제 코드 포함)

</details>

---

## 8. (적용 메모) Week 14 본문에서 바꿀 것

**Week 14 본문 → 이렇게 축소** (중복 제거):
- 「선택 가산점: 포트폴리오 웹페이지 생성」 안내 + 제출 형태(공개 URL/HTML/캡처)는 **유지**
- "발표자료에 꼭 들어갈 섹션 8개"도 **유지** (발표·웹 공통)
- ❌ **제거(→ 이 가이드로 이동)**: "웹페이지 제작 참고 자료" 전체 — 도구표 12개, HTML 제작 프롬프트, 도구 링크/미리보기, 웹 디자인 참고 사이트 20곳, OpenDesign
- 제거한 자리에 한 줄: **"→ 도구·프롬프트·레퍼런스·배포 상세는 [Portfolio page 만들기] 참고"**

**남는 효과**: Week 14 = "무엇을 제출하나"(최종 프로젝트 전반·발표) · Portfolio page = "웹페이지를 어떻게 만드나"(단일 가이드). 도구표 불일치(12개 vs 6개)도 12개 기준 하나로 해소.
