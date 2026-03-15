# week.html 리디자인 구현 계획

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** `week.html`을 사이드바 + 인포그래픽 스텝 카드 형태로 리디자인

**Architecture:** 단일 HTML 파일(`week.html`) 수정. 사이드바 toggle은 JS classList + IntersectionObserver. 단계 잠금 제거. 스텝 카드는 번호+툴명+설명+체크리스트만 유지.

**Tech Stack:** Vanilla HTML/CSS/JS, `curriculum.js` 데이터(개발자 제어 신뢰 데이터), `tokens.css` 디자인 토큰

**보안 참고:** innerHTML에 삽입되는 데이터는 `curriculum.js` (개발자가 직접 편집하는 정적 파일)에서만 옵니다. 외부 사용자 입력은 없습니다. 기존 코드와 동일한 패턴.

---

## 전제 조건

- 수정 파일: `course-site/week.html` 하나
- `curriculum.js` 데이터 구조 변경 없음
- `tokens.css` 변경 없음
- 로컬 확인: 브라우저에서 `course-site/week.html?week=2` 열기

---

## Task 1: 단계 잠금 로직 제거

**Files:**
- Modify: `course-site/week.html` - JS `initProgress()` 함수, `updateStep()` 함수

**Step 1: `updateStep()` 함수에서 잠금 로직 제거**

`updateStep()` 함수 전체를 아래로 교체:

```javascript
function updateStep(step) {
  const pill     = step.querySelector("[data-step-status]");
  const complete = isComplete(step);
  step.classList.toggle("is-complete", complete);
  step.classList.remove("is-locked");
  getTasks(step).forEach(t => { t.disabled = false; });
  if (complete) { pill.textContent = "완료"; pill.className = "status-pill complete"; }
  else          { pill.textContent = "진행 중"; pill.className = "status-pill active"; }
}
```

**Step 2: `sync()` 함수에서 순차 잠금 블록 제거**

`sync()` 안의 `let prevOk = true;` 와 그 이하 블록을 아래로 교체:

```javascript
steps.forEach(step => updateStep(step));
```

**Step 3: 브라우저에서 확인**

`week.html?week=2` 열어서 Step 1 미완료 상태에서도 Step 2 체크박스가 활성화되는지 확인.

**Step 4: Commit**

```bash
git add course-site/week.html
git commit -m "fix: remove sequential step locking — students can skip freely"
```

---

## Task 2: Hero 섹션 컴팩트하게

**Files:**
- Modify: `course-site/week.html` - `.hero` CSS

**Step 1: Hero 높이 줄이기**

`.hero` 스타일 교체:

```css
.hero {
  padding: 100px 0 28px; text-align: center;
}
```

(`min-height: 72vh; display: grid; place-items: center;` 제거)

**Step 2: 브라우저에서 확인**

1080p 풀스크린에서 Hero 아래 첫 번째 섹션이 스크롤 없이 보이는지 확인.

**Step 3: Commit**

```bash
git add course-site/week.html
git commit -m "style: compact hero section"
```

---

## Task 3: 스텝 카드 구조 단순화

**Files:**
- Modify: `course-site/week.html` - `stepsHtml` 생성 JS, 관련 CSS

**Step 1: `stepsHtml` 생성 코드 교체**

`buildPage()` 안의 `stepsHtml` 변수 생성 전체를 아래로 교체.

각 article에 `id="step-${idx}"` 추가, goal/done 제거, `step.copy`를 `<p class="step-copy">` 로 표시:

```
번호 + step.title + status-pill
(선택) step.image
step.copy 텍스트
task 체크박스 목록
```

**Step 2: `.step-title-group` CSS 업데이트**

```css
.step-title-group {
  display: flex; align-items: center; gap: 14px;
}
.step-title-text {
  font-size: 1.05rem; color: var(--text);
}
.step-copy {
  margin: 12px 0 16px;
  color: var(--muted-strong);
  font-size: .9rem;
  line-height: 1.72;
}
```

**Step 3: 불필요 CSS 제거**

`.step-info-grid`, `.step-info-card` 블록 삭제.

**Step 4: 브라우저에서 확인**

`week.html?week=2` - 각 스텝 카드에 목표/완료기준 없이 번호+툴명+설명+체크리스트만 보이는지 확인.

**Step 5: Commit**

```bash
git add course-site/week.html
git commit -m "style: simplify step card to title, description, tasks only"
```

---

## Task 4: 사이드바 HTML + CSS 추가

**Files:**
- Modify: `course-site/week.html` - body 구조, CSS

**Step 1: Topbar에 사이드바 토글 버튼 추가**

기존 `.topbar-inner` 안에서 `.brand` 앞에 `sidebar-toggle` 버튼 감싸는 `.brand-left` div 추가:

```html
<div class="brand-left">
  <button class="sidebar-toggle" id="sidebarToggle" aria-label="목차 열기" type="button">
    <!-- 햄버거 SVG (3선) -->
  </button>
  <div class="brand"> ... 기존 brand ... </div>
</div>
```

**Step 2: `#pageContent`를 `.content-layout` 안으로 이동**

기존 `<div id="pageContent"></div>` 를 아래 구조로 교체:

```html
<div class="content-layout">
  <nav class="sidebar" id="sidebar" aria-hidden="true">
    <ul class="sidebar-nav" id="sidebarNav"></ul>
  </nav>
  <div class="sidebar-overlay" id="sidebarOverlay"></div>
  <main class="main-content" id="pageContent"></main>
</div>
```

**Step 3: 사이드바 CSS 추가**

```css
.content-layout { display: flex; position: relative; }

.sidebar {
  position: fixed; top: 0; left: 0;
  width: 240px; height: 100vh;
  background: rgba(10,10,12,.96);
  border-right: 1px solid var(--line);
  backdrop-filter: blur(20px);
  z-index: 50;
  padding: 72px 0 24px;
  overflow-y: auto;
  transform: translateX(-100%);
  transition: transform .26s cubic-bezier(.4,0,.2,1);
}
.sidebar.is-open { transform: translateX(0); }

.sidebar-overlay {
  display: none; position: fixed; inset: 0;
  background: rgba(0,0,0,.5); z-index: 49;
}
.sidebar-overlay.is-visible { display: block; }

.sidebar-nav { list-style: none; margin: 0; padding: 8px 0; }
.sidebar-nav li a {
  display: block; padding: 8px 20px;
  font-size: .84rem; color: var(--muted);
  border-left: 2px solid transparent;
  transition: color .14s, border-color .14s, background .14s;
}
.sidebar-nav li a:hover {
  color: var(--text); background: rgba(255,255,255,.04);
}
.sidebar-nav li.is-active a {
  color: var(--key-soft); border-left-color: var(--key-soft);
  background: rgba(10,132,255,.08);
}
.sidebar-nav .nav-section-label {
  display: block; padding: 14px 20px 4px;
  font-size: .72rem; color: var(--muted);
  text-transform: uppercase; letter-spacing: .08em; font-weight: 600;
}

.sidebar-toggle {
  display: flex; align-items: center; justify-content: center;
  width: 36px; height: 36px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--line);
  background: rgba(255,255,255,.04);
  color: var(--muted-strong); cursor: pointer;
  transition: background .14s, color .14s; flex-shrink: 0;
}
.sidebar-toggle:hover { background: rgba(255,255,255,.09); color: var(--text); }
.brand-left { display: flex; align-items: center; gap: 10px; }
.main-content { flex: 1; min-width: 0; }
```

**Step 4: Commit**

```bash
git add course-site/week.html
git commit -m "feat: add sidebar HTML and CSS"
```

---

## Task 5: 사이드바 JS (토글 + IntersectionObserver)

**Files:**
- Modify: `course-site/week.html` - script 블록

**Step 1: `buildPage()` 안 마지막에 `initSidebar(w)` 호출 추가**

`initProgress(...)` 와 `initTopicChecks(...)` 아래에:

```javascript
initSidebar(w);
```

**Step 2: `initSidebar(w)` 함수 추가**

`</script>` 앞에 추가:

```javascript
function initSidebar(w) {
  const sidebar   = document.getElementById("sidebar");
  const overlay   = document.getElementById("sidebarOverlay");
  const toggleBtn = document.getElementById("sidebarToggle");
  const navList   = document.getElementById("sidebarNav");

  // 섹션 목록 구성
  const sections = [{ id: "hero-section", label: "개요", group: null }];
  w.steps.forEach((step, idx) => {
    sections.push({ id: "step-" + idx, label: step.title, group: idx === 0 ? "실습" : null });
  });
  if (w.shortcuts && w.shortcuts.length)  sections.push({ id: "section-shortcuts",  label: "단축키",     group: "참고" });
  if (w.explore   && w.explore.length)    sections.push({ id: "section-explore",    label: "더 해보기",  group: null });
  if (w.mistakes  && w.mistakes.length)   sections.push({ id: "section-mistakes",   label: "막히는 지점", group: null });
  if (w.assignment)                        sections.push({ id: "section-assignment", label: "과제",       group: null });

  // nav 렌더 (curriculum.js = 신뢰 데이터)
  navList.innerHTML = sections.map(s => {
    const g = s.group ? '<li><span class="nav-section-label">' + s.group + "</span></li>" : "";
    return g + '<li data-nav-id="' + s.id + '"><a href="#' + s.id + '">' + s.label + "</a></li>";
  }).join("");

  // 열기/닫기
  function open()  { sidebar.classList.add("is-open");    overlay.classList.add("is-visible");    sidebar.removeAttribute("aria-hidden"); }
  function close() { sidebar.classList.remove("is-open"); overlay.classList.remove("is-visible"); sidebar.setAttribute("aria-hidden","true"); }
  toggleBtn.addEventListener("click", () => sidebar.classList.contains("is-open") ? close() : open());
  overlay.addEventListener("click", close);
  document.addEventListener("keydown", e => { if (e.key === "Escape") close(); });

  // IntersectionObserver: 현재 섹션 하이라이트
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      navList.querySelectorAll("li[data-nav-id]").forEach(li => li.classList.remove("is-active"));
      const active = navList.querySelector('li[data-nav-id="' + entry.target.id + '"]');
      if (active) active.classList.add("is-active");
    });
  }, { rootMargin: "-20% 0px -70% 0px", threshold: 0 });

  sections.forEach(s => {
    const el = document.getElementById(s.id);
    if (el) observer.observe(el);
  });
}
```

**Step 3: Hero 섹션에 id 추가**

HTML 생성 코드에서 hero section 태그 교체:

```html
<section class="hero" id="hero-section">
```

**Step 4: 각 하위 섹션에 id 추가**

shortcutsHtml, exploreHtml, mistakesHtml, assignmentHtml 의 `<section class="content-block">` 태그에 각각:
- `id="section-shortcuts"`
- `id="section-explore"`
- `id="section-mistakes"`
- `id="section-assignment"`

**Step 5: 브라우저에서 확인**

1. `≡` 버튼 → 사이드바 열림/닫힘
2. 오버레이 클릭 / ESC → 닫힘
3. 스크롤 시 사이드바 현재 섹션 파란 하이라이트
4. 사이드바 링크 클릭 → 해당 섹션 스크롤

**Step 6: Commit**

```bash
git add course-site/week.html
git commit -m "feat: sidebar toggle and scroll-aware section highlight"
```

---

## Task 6: 모바일 반응형

**Files:**
- Modify: `course-site/week.html` - `@media (max-width: 720px)` 블록

**Step 1: 모바일 CSS 추가**

```css
@media (max-width: 720px) {
  .hero { padding-top: 88px; }
  .sidebar { width: 80vw; max-width: 300px; }
}
```

**Step 2: DevTools 375px에서 확인**

사이드바가 화면 80%만 덮고 뒤에 오버레이 보이는지 확인.

**Step 3: Commit**

```bash
git add course-site/week.html
git commit -m "style: mobile responsive sidebar overlay"
```

---

## 완료 체크리스트

- [ ] 단계 잠금 없음 - 모든 체크박스 활성화
- [ ] Hero 컴팩트 - 1080p 기준 첫 콘텐츠 스크롤 없이 보임
- [ ] 스텝 카드 - 번호/툴명/이미지/설명/체크리스트만
- [ ] 목표/완료기준 없음
- [ ] 사이드바 toggle 동작
- [ ] 스크롤 시 현재 섹션 자동 하이라이트
- [ ] 모바일 오버레이 드로어
- [ ] localStorage 진도 정상 작동
