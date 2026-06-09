# 정효린 3D/AI 포트폴리오 — 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (권장) 또는 superpowers:executing-plans 로 태스크별 실행. 스텝은 체크박스(`- [ ]`)로 추적.

**Goal:** 정효린 학생의 Blender 수업 15주 결과물을, '보물이' 캐릭터를 관통선으로 하는 밝은 멀티컬러 베이토 + 스크롤 스토리 단일 포트폴리오 페이지로 제작·배포한다.

**Architecture:** 바닐라 HTML/CSS/JS 단일 페이지. Notion에서 자산을 다운로드해 로컬 호스팅. 베이토 히어로(About·통계·대표영상) → W1~W13 6개 스크롤 챕터 → 클로징 CTA. RPD repo 서브패스 `portfolio/hyorin/`로 GitHub Pages 배포.

**Tech Stack:** Vanilla HTML/CSS/JS (no build), Space Grotesk(영문 헤드)+Pretendard(한글) CDN, IntersectionObserver(스크롤 reveal), 기존 Playwright + Claude Preview tools(QA).

**설계 문서(SoT):** [docs/superpowers/specs/2026-06-09-hyorin-portfolio-design.md](../specs/2026-06-09-hyorin-portfolio-design.md) — 콘텐츠 매핑·팔레트·카피는 이 문서 참조.

---

## 파일 구조

```
portfolio/hyorin/
  index.html                  # 단일 페이지 마크업
  styles/
    tokens.css                # 디자인 토큰(색·타이포·스페이싱·라디우스)
    base.css                  # reset, 폰트, body, 그리드 셸
    components.css            # BentoCard, StatTile, MediaCard, CornerBracket, SealBadge, SideNav
    sections.css              # hero, chapter, closing 레이아웃
    responsive.css            # 3 브레이크포인트
  app.js                      # scroll reveal, 영상 클릭재생
  assets/
    raw/                      # Notion 원본 다운로드(커밋 제외 후보)
    curated/                  # 페이지에 실제 쓰는 선별 자산
tools/
  fetch_hyorin_assets.sh      # Notion URL 추출 + 일괄 다운로드 스크립트
```

**파일 책임 분리 원칙:** 토큰/컴포넌트/섹션/반응형을 CSS 파일로 분리(한 파일 한 책임). `index.html`은 마크업만, 스타일은 CSS, 동작은 `app.js`.

---

## Task 1: 스캐폴딩 + 자산 확보 게이트 (최우선 리스크)

> 이 Task가 통과해야 나머지가 의미 있다. Notion S3 URL은 만료되므로 **fresh re-fetch → 즉시 다운로드**가 핵심.

**Files:**
- Create: `portfolio/hyorin/` 디렉토리 트리, `tools/fetch_hyorin_assets.sh`

- [ ] **Step 1: 디렉토리 스캐폴드**

```bash
mkdir -p portfolio/hyorin/styles portfolio/hyorin/assets/raw portfolio/hyorin/assets/curated
```

- [ ] **Step 2: Notion 페이지 fresh re-fetch (MCP)**

`notion-fetch` 툴로 페이지 `12224245-31354d6549718179965fe34bf266d874`를 **다시** 호출한다(이전 fetch의 S3 URL은 이미 403 만료). 결과는 tool-results 파일로 저장됨 — 그 파일 경로를 `$FRESH`로 기록.

- [ ] **Step 3: URL 추출 스크립트 작성**

`tools/fetch_hyorin_assets.sh`:
```bash
#!/usr/bin/env bash
# usage: ./tools/fetch_hyorin_assets.sh <fresh_notion_fetch.txt> <out_dir>
set -euo pipefail
SRC="$1"; OUT="${2:-portfolio/hyorin/assets/raw}"
mkdir -p "$OUT"
# S3 이미지 + 첨부 URL 추출
# 문서 순서 보존(= 주차 순서, 큐레이션 키). sort 금지. URL 중복만 awk로 제거.
grep -oE 'https://prod-files-secure[^])"<> ]+' "$SRC" | awk '!seen[$0]++' > "$OUT/_urls.txt"
echo "추출된 URL: $(wc -l < "$OUT/_urls.txt")개"
i=0
: > "$OUT/_manifest.tsv"
while IFS= read -r u; do
  # URL 경로의 원본 파일명 디코드 → 의미 보존(shot1_studio.png 등). 순번 prefix로 순서 보존 + 충돌(image.png 중복) 방지
  base="$(python3 -c "import sys,os,urllib.parse as p; print(os.path.basename(p.urlparse(p.unquote(sys.argv[1])).path) or 'asset.bin')" "$u")"
  out="$(printf '%03d_%s' "$i" "$base")"
  printf '%03d\t%s\n' "$i" "$base" >> "$OUT/_manifest.tsv"
  curl -fsS --max-time 90 -o "$OUT/$out" "$u" || echo "  FAIL $i $base"
  i=$((i+1))
done < "$OUT/_urls.txt"
echo "다운로드 완료 ($i개). _manifest.tsv = 순번→원본파일명(주차 큐레이션 lookup 키)."
ls -lhS "$OUT" | head
```

- [ ] **Step 4: 실행 + 검증 (게이트)**

Run:
```bash
chmod +x tools/fetch_hyorin_assets.sh
./tools/fetch_hyorin_assets.sh "$FRESH" portfolio/hyorin/assets/raw
ls portfolio/hyorin/assets/raw | grep -vc '^_'         # 다운로드 파일 수
file portfolio/hyorin/assets/raw/000_* | head          # 실제 이미지인지 확인
```
Expected: 51개 파일이 받아지고 `file`이 PNG로 인식.
> **사전 검증 완료 (2026-06-09):** fresh fetch 51 URL 전부 HTTP 200, basename 의미보존 확인. 파이프라인 작동 입증됨. **만약 실행 시점에 fetch가 만료(403)되면** 다시 fresh `notion-fetch` 후 즉시 재실행(URL 수명 ~1시간). 그래도 0개면 경로 B(사용자 Notion Export)로 전환.

- [ ] **Step 5: 첨부 영상(.mp4) 처리 판단**

```bash
ls -lhS portfolio/hyorin/assets/raw | head    # 큰 파일(영상) 용량 확인
```
10MB 미만이면 self-host 유지. 초과 시 `ffmpeg -i in.mp4 -vcodec libx264 -crf 28 out.mp4` 압축 또는 별도 처리. `.blend`는 받았더라도 페이지 임베드하지 않음(링크용으로만 보관).

- [ ] **Step 6: 큐레이션 (수동 판단)**

`_manifest.tsv`(순번→원본파일명)를 lookup해서 마일스톤당 베스트 2~3컷을 `assets/curated/`로 의미있는 이름으로 복사. 추측 불필요 — 순번이 곧 주차 순서다. **검증된 매핑 힌트**(2026-06-09):
```
000 1._장면_스크린샷.png        → Ch2 기초(W2)
008 (image.png)                → Ch2 모델링
009 Exact_Goldfish_Bot_3_4_View → Ch3 AI 3D(W5)
019 week06_junghyorin.png      → Ch4 재질(W6)
035-038 sunset_/noir_/product_ → Ch6 렌더(W13)
039-043 rigging1~3/pose3_curtsy → Ch5 리깅(W11)
046-050 shot1_studio/shot2_sunset/shot3_cyberpunk/ballet1/noir → Ch6 완성(W13 5컷)
```
```bash
cp portfolio/hyorin/assets/raw/046_shot1_studio.png portfolio/hyorin/assets/curated/ch6-render-studio.png
cp portfolio/hyorin/assets/raw/048_shot3_cyberpunk.png portfolio/hyorin/assets/curated/ch6-render-cyberpunk.png
# ... 매핑 힌트대로 챕터별 2~3컷
```
> 영상/오디오(W10·W13 Kling·Suno)는 S3 URL이 아닌 Notion 첨부(`attachment:`)일 수 있음 — fetch 본문에서 `attachment:` 또는 별도 file 블록 확인 후 동일하게 다운로드. 못 받으면 사용자 Notion Export로 보완.
선별 최종 목록을 `assets/curated/_manifest.md`(챕터→파일)에 기록.

- [ ] **Step 7: Commit**

```bash
git add portfolio/hyorin/assets/curated tools/fetch_hyorin_assets.sh portfolio/hyorin/assets/curated/_manifest.md
# raw는 용량 크면 .gitignore에 추가하고 curated만 커밋
git commit -m "feat(portfolio): 정효린 포트폴리오 자산 확보 및 큐레이션"
```

---

## Task 2: 디자인 토큰 + 폰트

**Files:**
- Create: `portfolio/hyorin/styles/tokens.css`, `portfolio/hyorin/index.html`(head 골격)

- [ ] **Step 1: tokens.css 작성**

```css
/* portfolio/hyorin/styles/tokens.css — design doc §6 */
:root {
  /* 팔레트 */
  --pf-bg: #ececec;
  --pf-card: #ffffff;
  --pf-violet: #7b6ef6;
  --pf-mint: #a8e0d8;
  --pf-yellow: #fbc95e;
  --pf-ink: #111111;
  --pf-pink: #eba6e0;
  --pf-sky: #7ec8e3;            /* 보물이 시그니처 */
  --pf-text: #1a1a1a;
  --pf-muted: #6b6b6b;
  --pf-on-violet: #ffffff;
  --pf-on-ink: #ffffff;

  /* 타이포 */
  --pf-font-head: "Space Grotesk", "Pretendard", sans-serif;
  --pf-font-body: "Pretendard", -apple-system, BlinkMacSystemFont, sans-serif;
  --pf-fs-hero: clamp(3rem, 9vw, 7.5rem);
  --pf-fs-h2:   clamp(1.6rem, 3.6vw, 2.75rem);
  --pf-fs-h3:   clamp(1.15rem, 1.8vw, 1.5rem);
  --pf-fs-stat: clamp(2rem, 4.5vw, 3.5rem);
  --pf-fs-body: clamp(0.95rem, 1.1vw, 1.05rem);
  --pf-fs-cap:  0.8rem;

  /* 스페이싱 (4px 베이스) */
  --pf-sp-2: 8px;  --pf-sp-3: 12px; --pf-sp-4: 16px;
  --pf-sp-6: 24px; --pf-sp-8: 32px; --pf-sp-12: 48px; --pf-sp-16: 64px;

  /* 라디우스 */
  --pf-r-card: 24px;
  --pf-r-md: 16px;
  --pf-r-pill: 999px;

  /* 베이토 */
  --pf-gap: 20px;
  --pf-maxw: 1240px;
}
```

- [ ] **Step 2: index.html head + 폰트 로드**

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>정효린 — 3D/AI 포트폴리오</title>
  <meta name="description" content="Blender와 AI로 캐릭터 '보물이'를 만든 15주. 정효린 포트폴리오." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
  <link rel="stylesheet" href="styles/tokens.css" />
  <link rel="stylesheet" href="styles/base.css" />
  <link rel="stylesheet" href="styles/components.css" />
  <link rel="stylesheet" href="styles/sections.css" />
  <link rel="stylesheet" href="styles/responsive.css" />
</head>
<body>
  <main id="app"><!-- sections --></main>
  <script src="app.js" defer></script>
</body>
</html>
```

- [ ] **Step 3: 검증** — Claude Preview로 페이지를 띄워 폰트가 로드되는지(콘솔 404 없음), 배경색 적용 확인.
Run: `preview_start` → `preview_console_logs`(에러 0) → `preview_screenshot`.

- [ ] **Step 4: Commit**
```bash
git add portfolio/hyorin/styles/tokens.css portfolio/hyorin/index.html
git commit -m "feat(portfolio): 디자인 토큰 + 폰트 로드"
```

---

## Task 3: 베이스 + 컴포넌트 CSS

**Files:**
- Create: `portfolio/hyorin/styles/base.css`, `portfolio/hyorin/styles/components.css`

- [ ] **Step 1: base.css (reset + 셸)**

```css
/* base.css */
*, *::before, *::after { box-sizing: border-box; margin: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--pf-bg);
  color: var(--pf-text);
  font-family: var(--pf-font-body);
  font-size: var(--pf-fs-body);
  line-height: 1.6;
  word-break: keep-all;
  overflow-wrap: break-word;
  -webkit-font-smoothing: antialiased;
}
img, video { display: block; max-width: 100%; height: auto; }
#app { max-width: var(--pf-maxw); margin: 0 auto; padding: var(--pf-sp-8) var(--pf-sp-6); }
.pf-head { font-family: var(--pf-font-head); font-weight: 700; letter-spacing: -0.02em; }
h2.pf-section { font-family: var(--pf-font-head); font-size: var(--pf-fs-h2); font-weight: 700; }
```

- [ ] **Step 2: components.css — BentoCard / CornerBracket**

```css
/* components.css */
.bento { border-radius: var(--pf-r-card); padding: var(--pf-sp-6); position: relative; overflow: clip; background: var(--pf-card); }
.bento--violet { background: var(--pf-violet); color: var(--pf-on-violet); }
.bento--mint   { background: var(--pf-mint); }
.bento--yellow { background: var(--pf-yellow); }
.bento--ink    { background: var(--pf-ink); color: var(--pf-on-ink); }

/* 코너 브래킷(Dribbble 시그니처) — 우상단 ㄱ자 */
.bento--bracket::after {
  content: ""; position: absolute; top: 14px; right: 14px;
  width: 18px; height: 18px;
  border-top: 2px solid currentColor; border-right: 2px solid currentColor;
  opacity: .5;
}
```

- [ ] **Step 3: components.css — StatTile / MediaCard / SealBadge / SideNav**

```css
.stat { display: flex; flex-direction: column; justify-content: center; gap: 4px; }
.stat__num { font-family: var(--pf-font-head); font-weight: 700; font-size: var(--pf-fs-stat); font-variant-numeric: tabular-nums; line-height: 1; }
.stat__label { font-size: var(--pf-fs-cap); text-transform: uppercase; letter-spacing: .08em; opacity: .75; }

.media { position: relative; border-radius: var(--pf-r-card); overflow: clip; background: var(--pf-ink); }
.media img, .media video { width: 100%; height: 100%; object-fit: cover; }
.media__play { position: absolute; inset: 0; margin: auto; width: 64px; height: 64px; border: 0; border-radius: var(--pf-r-pill); background: rgba(255,255,255,.92); cursor: pointer; display: grid; place-items: center; }
.media__play::before { content: ""; width: 0; height: 0; border-left: 16px solid var(--pf-ink); border-top: 10px solid transparent; border-bottom: 10px solid transparent; margin-left: 4px; }

.seal { width: 84px; height: 84px; border-radius: var(--pf-r-pill); background: var(--pf-ink); color: #fff; display: grid; place-items: center; }
.seal__dot { width: 12px; height: 12px; border-radius: 50%; background: #fff; }

.sidenav { position: fixed; left: 18px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: var(--pf-sp-6); writing-mode: vertical-rl; font-size: var(--pf-fs-cap); letter-spacing: .12em; text-transform: uppercase; color: var(--pf-muted); }
.sidenav a { color: inherit; text-decoration: none; }
.sidenav a:hover, .sidenav a:focus-visible { color: var(--pf-text); }
```

- [ ] **Step 4: 검증** — 임시 테스트 마크업(각 컴포넌트 1개씩)을 index.html에 잠깐 넣고 `preview_screenshot`으로 카드·코너브래킷·통계·플레이버튼이 렌더되는지 확인 후 제거.

- [ ] **Step 5: Commit**
```bash
git add portfolio/hyorin/styles/base.css portfolio/hyorin/styles/components.css
git commit -m "feat(portfolio): 베이스 + 베이토 컴포넌트 CSS"
```

---

## Task 4: 히어로 베이토 섹션

**Files:**
- Modify: `portfolio/hyorin/index.html` (#app 내부), `portfolio/hyorin/styles/sections.css`(Create)

- [ ] **Step 1: 히어로 마크업** (design doc §4·§5)

`#app` 안에 삽입 — 좌측 About 세로카드 + 우측(헤드라인·통계 3타일·대표영상):
```html
<section class="hero" id="intro">
  <article class="bento bento--violet hero__about">
    <p class="hero__kicker">About Me</p>
    <div class="hero__avatar"><img src="assets/curated/key-bomul.png" alt="캐릭터 보물이 키비주얼" /></div>
    <h1 class="hero__name pf-head">Im,<br><strong>정효린</strong></h1>
    <p class="hero__intro">3D와 AI로 캐릭터를 만드는 미디어커뮤니케이션 전공. 다음은 기업 홍보실.</p>
    <a class="hero__mail" href="mailto:REPLACE_EMAIL">이메일 보내기</a>
    <div class="seal hero__seal"><span class="seal__dot"></span></div>
  </article>

  <div class="hero__right">
    <h2 class="hero__display pf-head">Portfolio</h2>
    <div class="media bento--bracket hero__video">
      <video src="assets/curated/hero-w13-kling.mp4" poster="assets/curated/hero-w13-poster.png" preload="none"></video>
      <button class="media__play" aria-label="대표 영상 재생"></button>
    </div>
    <ul class="hero__stats">
      <li class="bento bento--mint stat bento--bracket"><span class="stat__num">15</span><span class="stat__label">Weeks</span></li>
      <li class="bento bento--violet stat"><span class="stat__num">7</span><span class="stat__label">AI · 3D Tools</span></li>
      <li class="bento bento--yellow stat bento--bracket"><span class="stat__num">5</span><span class="stat__label">Cinematic Renders</span></li>
      <li class="bento bento--ink stat"><span class="stat__num">1</span><span class="stat__label">Character · 보물이</span></li>
    </ul>
  </div>
</section>
```
> `REPLACE_EMAIL`과 키비주얼/영상 파일명은 Task 1 `_manifest.md` 실제 파일로 치환. 이메일은 정효린 확인 필요(없으면 클로징 CTA로 대체).

- [ ] **Step 2: sections.css — hero 그리드**

```css
.hero { display: grid; grid-template-columns: minmax(280px, 1fr) 1.8fr; gap: var(--pf-gap); align-items: stretch; }
.hero__about { display: flex; flex-direction: column; gap: var(--pf-sp-4); }
.hero__kicker { font-size: var(--pf-fs-cap); text-transform: uppercase; letter-spacing: .1em; opacity: .8; }
.hero__avatar { width: 100%; aspect-ratio: 1; border-radius: var(--pf-r-pill); overflow: clip; background: var(--pf-pink); }
.hero__avatar img { width: 100%; height: 100%; object-fit: cover; }
.hero__name { font-size: var(--pf-fs-h2); line-height: 1.05; }
.hero__intro { font-size: var(--pf-fs-body); opacity: .95; }
.hero__mail { margin-top: auto; align-self: start; background: #fff; color: var(--pf-ink); padding: 10px 18px; border-radius: var(--pf-r-pill); text-decoration: none; font-weight: 600; }
.hero__seal { position: absolute; right: 20px; bottom: 20px; }
.hero__right { display: grid; grid-template-rows: auto 1fr auto; gap: var(--pf-gap); min-width: 0; }
.hero__display { font-size: var(--pf-fs-hero); line-height: .9; }
.hero__video { min-height: 280px; }
.hero__stats { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--pf-gap); }
```

- [ ] **Step 3: 검증** — `preview_screenshot` 데스크톱. About 카드 좌측, 거대 "Portfolio" 헤드라인, 영상 카드, 통계 4타일 멀티컬러 확인. `preview_console_logs` 에러 0. 자산 누락 시 placeholder 회색박스로 보이는지.

- [ ] **Step 4: Commit**
```bash
git add portfolio/hyorin/index.html portfolio/hyorin/styles/sections.css
git commit -m "feat(portfolio): 히어로 베이토 섹션"
```

---

## Task 5: W1~W13 스크롤 챕터

**Files:**
- Modify: `portfolio/hyorin/index.html`, `portfolio/hyorin/styles/sections.css`

- [ ] **Step 1: 챕터 공통 마크업 패턴** — 6개 챕터를 같은 구조로. Ch1 예시(나머지는 design doc §5 콘텐츠로 동일 패턴 반복):

```html
<section class="chapter" id="works">
  <article class="chap" data-reveal>
    <header class="chap__head">
      <span class="chap__no pf-head">01</span>
      <h2 class="chap__title pf-head">컨셉 — 보물이</h2>
      <p class="chap__lead">보험처럼 나를 지켜주는 수호천사. 삼성화재 ‘보험 선물하기’를 위한 캐릭터 ‘보물이’를 기획했습니다.</p>
    </header>
    <div class="chap__grid">
      <figure class="media bento--bracket chap__hero"><img src="assets/curated/ch1-concept-mixboard.png" alt="보물이 컨셉 무드보드" /></figure>
      <figure class="media chap__side"><img src="assets/curated/ch1-concept-2.png" alt="보물이 컨셉 탐색" /></figure>
      <div class="bento bento--mint chap__note"><p>Google Mixboard로 아이데이션 → 삼성화재 키컬러(하늘색) 적용</p></div>
    </div>
  </article>
  <!-- Ch2~Ch6 동일 패턴, 콘텐츠는 design doc §5 표 -->
</section>
```
> 챕터별 색상 강조 토큰을 번갈아(mint→violet→yellow→sky→pink→ink) 적용해 리듬을 만든다. Ch6(완성)은 W13 렌더 5컷 갤러리 + Kling 영상 + Suno 음악(`<audio controls>`).

- [ ] **Step 2: sections.css — chapter 레이아웃**

```css
.chapter { margin-top: var(--pf-sp-16); display: flex; flex-direction: column; gap: var(--pf-sp-16); }
.chap__head { display: grid; gap: var(--pf-sp-2); margin-bottom: var(--pf-sp-6); }
.chap__no { font-size: var(--pf-fs-hero); line-height: .8; color: var(--pf-violet); opacity: .25; }
.chap__title { font-size: var(--pf-fs-h2); }
.chap__lead { max-width: 60ch; color: var(--pf-muted); }
.chap__grid { display: grid; grid-template-columns: 2fr 1fr; grid-auto-rows: minmax(120px, auto); gap: var(--pf-gap); }
.chap__hero { grid-row: span 2; min-height: 320px; }
.chap__note { display: grid; align-content: center; }
```

- [ ] **Step 3: 콘텐츠 채우기** — design doc §5 표의 6개 챕터 카피·자산을 모두 입력. 기술용어 1줄 풀이 포함(예: 리깅). 미제출 주차(W7/14/15)는 스킵.

- [ ] **Step 4: 검증** — `preview_screenshot` 전체 스크롤 캡처(또는 구간별). 6개 챕터 흐름·색 리듬·이미지 로드 확인. `preview_console_logs` 에러 0. 영상/오디오 컨트롤 동작.

- [ ] **Step 5: Commit**
```bash
git add portfolio/hyorin/index.html portfolio/hyorin/styles/sections.css
git commit -m "feat(portfolio): W1~W13 스크롤 챕터"
```

---

## Task 6: 클로징 + 사이드네비 + 반응형

**Files:**
- Modify: `portfolio/hyorin/index.html`, Create: `portfolio/hyorin/styles/responsive.css`

- [ ] **Step 1: 클로징 CTA + 사이드네비 마크업**

```html
<section class="closing" id="contact">
  <div class="bento bento--ink closing__card">
    <h2 class="pf-head">보물이를 만든 과정처럼,<br>다음 캐릭터도 만들 준비가 되어 있습니다.</h2>
    <a class="hero__mail" href="mailto:REPLACE_EMAIL">함께 일하기</a>
  </div>
  <p class="closing__credit">Made with Blender · Hyper3D · Kling AI · Suno AI · Mixamo</p>
</section>
<nav class="sidenav" aria-label="섹션 이동">
  <a href="#intro">Intro</a><a href="#works">Works</a><a href="#contact">Contact</a>
</nav>
```

- [ ] **Step 2: responsive.css — 3 브레이크포인트**

```css
@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; }
  .hero__stats { grid-template-columns: repeat(2, 1fr); }
  .chap__grid { grid-template-columns: 1fr; }
  .chap__hero { grid-row: auto; }
  .sidenav { display: none; }
}
@media (max-width: 600px) {
  #app { padding: var(--pf-sp-6) var(--pf-sp-4); }
  .hero__stats { grid-template-columns: 1fr 1fr; }
  .hero__display { font-size: clamp(2.5rem, 16vw, 4rem); }
}
```

- [ ] **Step 3: 검증** — `preview_resize` 1280 / 834 / 390 폭에서 각각 `preview_screenshot`. 모바일 1열 스택·통계 2열·사이드네비 숨김 확인. 가로 overflow 없는지.

- [ ] **Step 4: Commit**
```bash
git add portfolio/hyorin/index.html portfolio/hyorin/styles/responsive.css
git commit -m "feat(portfolio): 클로징 CTA + 사이드네비 + 반응형"
```

---

## Task 7: 모션 + 영상 인터랙션

**Files:**
- Create: `portfolio/hyorin/app.js`

- [ ] **Step 1: app.js — scroll reveal + 영상 클릭재생**

```javascript
// app.js
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// 스크롤 인뷰 reveal
if (!reduce && "IntersectionObserver" in window) {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
    }
  }, { threshold: 0.15 });
  document.querySelectorAll("[data-reveal]").forEach((el) => io.observe(el));
} else {
  document.querySelectorAll("[data-reveal]").forEach((el) => el.classList.add("is-in"));
}

// 영상 클릭 재생(자동재생 금지)
document.querySelectorAll(".media__play").forEach((btn) => {
  btn.addEventListener("click", () => {
    const video = btn.parentElement.querySelector("video");
    if (!video) return;
    video.setAttribute("controls", "");
    btn.remove();
    video.play();
  });
});
```

- [ ] **Step 2: reveal CSS 추가** (sections.css)
```css
[data-reveal] { opacity: 0; transform: translateY(16px); transition: opacity .5s ease, transform .5s ease; }
[data-reveal].is-in { opacity: 1; transform: none; }
@media (prefers-reduced-motion: reduce) { [data-reveal] { opacity: 1; transform: none; transition: none; } }
.bento { transition: transform .14s ease; }
.bento:hover { transform: translateY(-2px); }
```

- [ ] **Step 3: 검증** — preview에서 스크롤 시 챕터 fade-up, 영상 플레이버튼 클릭→재생, hover lift. `prefers-reduced-motion` 강제 시 애니메이션 꺼지는지(`preview_eval`로 매치미디어 확인).

- [ ] **Step 4: Commit**
```bash
git add portfolio/hyorin/app.js portfolio/hyorin/styles/sections.css
git commit -m "feat(portfolio): 스크롤 reveal + 영상 클릭재생"
```

---

## Task 8: 접근성 + QA

**Files:** 전체 점검, 필요 시 마크업/CSS 수정

- [ ] **Step 1: 접근성 점검** — 모든 `img` alt 채움, 버튼 `aria-label`, 색대비(멀티컬러 카드 위 텍스트 WCAG AA), 키보드 포커스 링, heading 순서(h1→h2). RPD `rpd-a11y-audit` 스킬 실행.

- [ ] **Step 2: 콘솔/네트워크 QA** — `preview_console_logs`(에러 0), `preview_network`(404 자산 0, 만료 링크 0).

- [ ] **Step 3: 최종 시각 회귀** — 데스크톱/태블릿/모바일 `preview_screenshot` 3장 사용자에게 공유.

- [ ] **Step 4: Commit**(수정 있었으면)
```bash
git add -A portfolio/hyorin
git commit -m "fix(portfolio): 접근성 · QA 보정"
```

---

## Task 9: 동의 게이트 + 배포

**Files:** `.gitignore`(raw 제외 시), GitHub Pages 설정

- [ ] **Step 1: 발행 전 동의 게이트** — 사용자(→정효린)에게 (a) 공개 동의 (b) 이미지·인용 사용 동의 확인. 학번 노출 0 재확인. 미동의 시 배포 보류.

- [ ] **Step 2: 삼성화재 표기 확인** — 페이지에 "학생 수업 과제 / 비공식 컨셉" 문구 존재, 실제 로고·자산 미사용 확인.

- [ ] **Step 3: 배포** — `portfolio/hyorin/`가 GitHub Pages 경로로 서빙되는지 확인(RPD는 main 배포). 공개 URL 접속 테스트(자산 로드·반응형).

- [ ] **Step 4: 최종 Commit + PR**
```bash
git add -A
git commit -m "feat(portfolio): 정효린 3D/AI 포트폴리오 페이지 완성"
```
PR 생성은 사용자 승인 후.

---

## Self-Review 체크 (작성자 수행)

- **스펙 커버리지:** design doc §1~§15 → Task 1~9로 매핑됨(자산=T1, 토큰=T2, 컴포넌트=T3, 히어로=T4, 챕터=T5, 반응형=T6, 모션=T7, 접근성=T8, 동의·배포=T9). 누락 없음.
- **플레이스홀더:** `REPLACE_EMAIL`·자산 파일명은 Task 1 manifest로 치환하도록 명시(의도된 변수, T4/T6 노트에 처리법 기재). 그 외 TBD 없음.
- **타입 일관성:** 클래스명(`.bento`, `.media__play`, `[data-reveal]`, `.stat__num`)이 컴포넌트 정의(T3)와 사용(T4~T7)에서 일치.

## 리스크 & 의존성

- **T1이 게이트.** 자산 다운로드 실패 시 경로 B(Notion Export)로 전환, 그 전까지 T4~T8 비주얼 검증 불가(placeholder로 진행 가능).
- 이메일·본인 사진 부재는 design doc에서 확정(사진 미사용/보물이 키비주얼). 이메일 미확인 시 mailto만 placeholder.
