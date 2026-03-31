# Week 05 Sculpt/Remesh 도구 상세 설명 + ShowMe 카드 링크 구현 플랜

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Week 05 노션 페이지의 빨간색 도구 이름 10개에 상세 설명 + 캡처 이미지 + YouTube + ShowMe 카드 링크를 추가한다.

**Architecture:** Playwright로 Blender 공식 문서 7페이지 캡처 → GitHub 푸시로 raw URL 확보 → YouTube 리서치 → Notion API로 3개 섹션 업데이트

**Tech Stack:** Playwright (Python capture script), Notion MCP, Git, WebSearch

---

## File Structure

| 파일 | 역할 | 변경 |
|------|------|------|
| `tools/capture_screenshots.py` | 캡처 스크립트 STEP_MAP | Modify: Week 5 sculpt brush 매핑 7개 추가 |
| `course-site/assets/images/week05/sculpt-*.png` | 브러시별 캡처 이미지 7장 | Create |
| Notion page `31354d65-4971-811e-85fe-ed7681421e37` | Week 05 페이지 본문 | Modify: 3개 섹션에 details 토글 추가 |

---

### Task 1: capture_screenshots.py에 Week 5 브러시 매핑 추가

**Files:**
- Modify: `tools/capture_screenshots.py:50-52`

- [ ] **Step 1: STEP_MAP에 7개 브러시 엔트리 추가**

`tools/capture_screenshots.py`의 `STEP_MAP` 딕셔너리, Week 5 섹션(`(5, 0)`, `(5, 1)` 아래)에 추가:

```python
    # Week 5: Sculpt brushes (개별 공식 문서 캡처)
    (5, 10): ("sculpt-draw",         "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/draw.html"),
    (5, 11): ("sculpt-grab",         "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/grab.html"),
    (5, 12): ("sculpt-smooth",       "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/smooth.html"),
    (5, 13): ("sculpt-clay-strips",  "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/clay_strips.html"),
    (5, 14): ("sculpt-crease",       "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/crease.html"),
    (5, 15): ("sculpt-inflate",      "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/inflate.html"),
    (5, 16): ("sculpt-snake-hook",   "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/snake_hook.html"),
```

step_index 10~16을 사용 (기존 Week 3의 패턴과 동일 — 도구 개별 캡처는 10번대).

- [ ] **Step 2: dry-run으로 매핑 확인**

Run: `cd /Users/ssongji/Developer/Workspace/RPD/.claude/worktrees/dazzling-nash && python3 tools/capture_screenshots.py --week 5 --dry-run`

Expected: 9개 항목 출력 (기존 2개 + 신규 7개), 각각 파일명과 URL 표시

- [ ] **Step 3: Commit**

```bash
git add tools/capture_screenshots.py
git commit -m "feat(capture): add Week 5 sculpt brush doc URLs to STEP_MAP"
```

---

### Task 2: 7개 브러시 공식 문서 스크린샷 캡처

**Files:**
- Create: `course-site/assets/images/week05/sculpt-draw.png`
- Create: `course-site/assets/images/week05/sculpt-grab.png`
- Create: `course-site/assets/images/week05/sculpt-smooth.png`
- Create: `course-site/assets/images/week05/sculpt-clay-strips.png`
- Create: `course-site/assets/images/week05/sculpt-crease.png`
- Create: `course-site/assets/images/week05/sculpt-inflate.png`
- Create: `course-site/assets/images/week05/sculpt-snake-hook.png`

- [ ] **Step 1: 캡처 스크립트 실행**

Run: `cd /Users/ssongji/Developer/Workspace/RPD/.claude/worktrees/dazzling-nash && python3 tools/capture_screenshots.py --week 5 --skip-curriculum`

`--skip-curriculum` 플래그 사용 — curriculum.js 자동 수정 불필요 (step_index 10+ 매핑은 curriculum.js에 없음).

Expected: `완료: 8/9 성공` 또는 `9/9 성공` (`ai-3d-import`은 URL None이라 스킵됨, 실제 대상 8개)

- [ ] **Step 2: 생성된 이미지 확인**

Run: `ls -la course-site/assets/images/week05/sculpt-*.png`

Expected: 7개 파일 + 기존 `sculpt-mode.png` = 8개 sculpt-*.png 파일

- [ ] **Step 3: Commit + Push**

```bash
git add course-site/assets/images/week05/sculpt-*.png
git commit -m "feat(week05): capture 7 sculpt brush official doc screenshots"
git push origin claude/dazzling-nash
```

Push 후 GitHub raw URL 패턴 확인:
`https://raw.githubusercontent.com/ssongji1122/RPD/claude/dazzling-nash/course-site/assets/images/week05/sculpt-draw.png`

---

### Task 3: YouTube 영상 리서치

**Files:** 없음 (리서치만)

- [ ] **Step 1: 각 브러시별 YouTube 영상 검색**

WebSearch로 아래 7개 도구 + Remesh + Decimate = 9개 검색:

| 도구 | 검색어 |
|------|--------|
| Draw brush | `blender sculpt draw brush tutorial short` |
| Grab brush | `blender sculpt grab brush tutorial short` |
| Smooth brush | `blender sculpt smooth brush tutorial short` |
| Clay Strips | `blender sculpt clay strips brush tutorial` |
| Crease brush | `blender sculpt crease brush tutorial` |
| Inflate brush | `blender sculpt inflate brush tutorial` |
| Snake Hook | `blender sculpt snake hook brush tutorial` |
| Remesh | `blender voxel remesh tutorial short` |
| Decimate | `blender decimate modifier tutorial short` |

선정 기준: Blender 공식/Grant Abbitt/Blender Guru 채널 우선, 5분 이내, 해당 도구에 집중하는 영상.

- [ ] **Step 2: 결과를 메모**

각 도구별 YouTube URL을 기록. 형식: `https://www.youtube.com/watch?v=XXXXXXXXXXX`

노션에서는 YouTube URL만 넣으면 자동 임베드됨.

---

### Task 4: 노션 Sculpt Mode 기초 섹션 업데이트

**Files:**
- Modify: Notion page `31354d65-4971-811e-85fe-ed7681421e37`

- [ ] **Step 1: 현재 페이지 내용 조회**

`notion-fetch` 로 페이지 ID `31354d65-4971-811e-85fe-ed7681421e37` 조회.

Sculpt Mode 기초 섹션의 마지막 체크리스트 항목을 찾아 `old_str`로 사용할 정확한 문자열 확인.

- [ ] **Step 2: Draw/Grab/Smooth 상세 + ShowMe 링크 추가**

`notion-update-page` (command: `update_content`)로 Sculpt Mode 기초 섹션의 마지막 체크리스트 뒤에 삽입.

`old_str`: Sculpt 기초 섹션의 마지막 체크리스트 항목 (Smooth 관련)
`new_str`: 기존 체크리스트 + 아래 내용 추가

```markdown
<details>
<summary>🖌️ Draw 브러시 상세</summary>
Sculpt Mode의 기본 브러시예요. 표면을 올리거나(기본) 파낼 수(Ctrl) 있어요.
Radius와 Strength로 브러시 크기/강도를 조절하고, Automasking으로 인접 면만 영향받게 제한할 수 있어요.
큰 형태를 먼저 잡을 때 가장 많이 쓰이고, Grab과 번갈아 쓰면 효율적이에요.

![Draw 브러시 공식 문서](https://raw.githubusercontent.com/ssongji1122/RPD/claude/dazzling-nash/course-site/assets/images/week05/sculpt-draw.png)

> [Draw — Blender 공식 문서](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/draw.html)

{Task 3에서 찾은 Draw YouTube URL}

</details>
<details>
<summary>✊ Grab 브러시 상세</summary>
메쉬를 잡아서 끌어당기는 브러시예요. 형태의 큰 실루엣을 조정할 때 핵심이에요.
다른 브러시와 달리 표면을 추가/제거하지 않고 기존 점을 이동시켜요.
큰 브러시 크기로 전체 비율을 잡고, 작은 크기로 세부 위치를 조정하세요.

![Grab 브러시 공식 문서](https://raw.githubusercontent.com/ssongji1122/RPD/claude/dazzling-nash/course-site/assets/images/week05/sculpt-grab.png)

> [Grab — Blender 공식 문서](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/grab.html)

{Task 3에서 찾은 Grab YouTube URL}

</details>
<details>
<summary>🧹 Smooth 브러시 상세</summary>
울퉁불퉁한 표면을 부드럽게 정리하는 브러시예요. Shift를 누른 채로 다른 브러시 사용 중 임시 전환도 가능해요.
Strength를 0.3~0.5로 낮게 시작하면 형태를 무너뜨리지 않으면서 정리할 수 있어요.
스컬프팅 마무리 단계에서 전체를 한 번 쓸어주면 깔끔해져요.

![Smooth 브러시 공식 문서](https://raw.githubusercontent.com/ssongji1122/RPD/claude/dazzling-nash/course-site/assets/images/week05/sculpt-smooth.png)

> [Smooth — Blender 공식 문서](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/smooth.html)

{Task 3에서 찾은 Smooth YouTube URL}

</details>
> 📘 [ShowMe 카드에서 인터랙티브 학습 → Sculpt Mode 기초](https://ssongji1122.github.io/RPD/course-site/week.html?week=5&showme=sculpt-basics)
```

주의: `{Task 3에서 찾은 ... URL}` 부분은 Task 3 결과로 실제 YouTube URL 대체.

---

### Task 5: 노션 Sculpt 브러시 심화 섹션 업데이트

**Files:**
- Modify: Notion page `31354d65-4971-811e-85fe-ed7681421e37`

- [ ] **Step 1: 심화 섹션 마지막 체크리스트 확인**

Task 4에서 조회한 페이지 내용에서 Snake Hook 체크리스트 항목의 정확한 문자열 확인.

- [ ] **Step 2: Clay Strips/Crease/Inflate/Snake Hook 상세 + ShowMe 링크 추가**

`notion-update-page`로 심화 섹션 마지막 체크리스트 뒤에 삽입:

```markdown
<details>
<summary>🧱 Clay Strips 상세</summary>
점토를 덧붙이듯 형태를 쌓아올리는 브러시예요. Draw보다 넓고 평평한 스트로크를 만들어요.
근육이나 갑옷 같은 넓은 면의 볼륨을 쌓을 때 최적이에요.
Strength를 높이면 한 번에 많이 쌓이고, Normal Radius로 방향을 조정할 수 있어요.

![Clay Strips 공식 문서](https://raw.githubusercontent.com/ssongji1122/RPD/claude/dazzling-nash/course-site/assets/images/week05/sculpt-clay-strips.png)

> [Clay Strips — Blender 공식 문서](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/clay_strips.html)

{YouTube URL}

</details>
<details>
<summary>〰️ Crease 상세</summary>
날카로운 홈이나 주름 선을 파는 브러시예요. Pinch 효과가 같이 들어가서 선이 또렷해져요.
관절 접히는 곳, 눈/입 라인, 갑옷 이음새 등 선형 디테일에 적합해요.
Ctrl로 반전하면 돌출된 능선을 만들 수 있어요.

![Crease 공식 문서](https://raw.githubusercontent.com/ssongji1122/RPD/claude/dazzling-nash/course-site/assets/images/week05/sculpt-crease.png)

> [Crease — Blender 공식 문서](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/crease.html)

{YouTube URL}

</details>
<details>
<summary>🎈 Inflate 상세</summary>
표면을 노멀 방향으로 부풀리는 브러시예요. Draw와 달리 모든 방향으로 균일하게 팽창해요.
볼살, 근육 강조, 둥근 보석 같은 볼록한 형태를 만들 때 유용해요.
Ctrl로 반전하면 수축 효과 — 눈구멍이나 움푹 들어간 곳에 활용하세요.

![Inflate 공식 문서](https://raw.githubusercontent.com/ssongji1122/RPD/claude/dazzling-nash/course-site/assets/images/week05/sculpt-inflate.png)

> [Inflate — Blender 공식 문서](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/inflate.html)

{YouTube URL}

</details>
<details>
<summary>🐍 Snake Hook 상세</summary>
끝점이 따라오면서 메쉬를 길게 늘어나게 끌어내는 브러시예요.
뿔, 촉수, 머리카락, 나뭇가지처럼 가늘고 긴 형태를 빼낼 때 핵심이에요.
DynTopo를 켜고 쓰면 늘어나는 부분에 폴리곤이 자동 추가되어 더 자연스러워요.

![Snake Hook 공식 문서](https://raw.githubusercontent.com/ssongji1122/RPD/claude/dazzling-nash/course-site/assets/images/week05/sculpt-snake-hook.png)

> [Snake Hook — Blender 공식 문서](https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/snake_hook.html)

{YouTube URL}

</details>
> 📘 [ShowMe 카드에서 인터랙티브 학습 → Sculpt 브러시 선택 기준](https://ssongji1122.github.io/RPD/course-site/week.html?week=5&showme=sculpt-brushes)
```

---

### Task 6: 노션 Remesh + Decimate 섹션에 ShowMe 카드 링크 추가

**Files:**
- Modify: Notion page `31354d65-4971-811e-85fe-ed7681421e37`

- [ ] **Step 1: Remesh 섹션 끝 위치 확인**

이전 세션에서 추가된 "Blender Remesh 완전 가이드" 인라인 콘텐츠의 마지막 부분 (`AI 생성 (.glb) → Import → ...` 코드 블록) 찾기.

- [ ] **Step 2: Remesh/Decimate YouTube + ShowMe 카드 링크 추가**

`notion-update-page`로 Remesh 인라인 가이드 마지막 뒤에 삽입:

```markdown
{Remesh YouTube URL}

{Decimate YouTube URL}

> 📘 [ShowMe 카드 → Remesh 이해](https://ssongji1122.github.io/RPD/course-site/week.html?week=5&showme=remesh-modifier) · [Decimate 이해](https://ssongji1122.github.io/RPD/course-site/week.html?week=5&showme=decimate-modifier)
```

---

### Task 7: 검증

**Files:** 없음 (검증만)

- [ ] **Step 1: 노션 페이지 재조회**

`notion-fetch`로 page ID `31354d65-4971-811e-85fe-ed7681421e37` 재조회.

확인 항목:
- Sculpt 기초 섹션: Draw/Grab/Smooth `<details>` 3개 + sculpt-basics ShowMe 링크
- Sculpt 심화 섹션: Clay Strips/Crease/Inflate/Snake Hook `<details>` 4개 + sculpt-brushes ShowMe 링크
- Remesh 섹션: remesh-modifier + decimate-modifier ShowMe 링크
- 이미지 URL이 GitHub raw URL로 올바르게 렌더링되는지
- YouTube URL이 임베드로 표시되는지

- [ ] **Step 2: Commit showme.md 스킬 수정**

```bash
git add .claude/commands/showme.md
git commit -m "docs(showme): add card granularity decision guide"
```

- [ ] **Step 3: 최종 Push**

```bash
git push origin claude/dazzling-nash
```
