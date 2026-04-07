# ShowMe Template & References

## HTML 기본 구조

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{한글 제목}</title>
  <style>
    /* ── 전체 CSS 인라인 (mirror-modifier.html에서 복사) ── */
  </style>
</head>
<body>
  <nav class="tabs" role="tablist">
    <button class="tab is-active" data-tab="concept" role="tab" aria-selected="true">개념 이해</button>
    <button class="tab" data-tab="visual" role="tab" aria-selected="false">interaction</button>
    <button class="tab" data-tab="when" role="tab" aria-selected="false">언제 쓰나요?</button>
    <button class="tab" data-tab="quiz" role="tab" aria-selected="false">퀴즈</button>
  </nav>

  <section class="panel is-active" id="panel-concept" role="tabpanel">...</section>
  <section class="panel" id="panel-visual" role="tabpanel">...</section>
  <section class="panel" id="panel-when" role="tabpanel">...</section>
  <section class="panel" id="panel-quiz" role="tabpanel">...</section>

  <script>
    /* 탭 전환 + initQuiz + postMessage */
  </script>
</body>
</html>
```

## Blender 공식 문서 URL 패턴

| 카테고리 | URL 패턴 |
|----------|----------|
| Generate 모디파이어 | `https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/{name}.html` |
| Mesh 도구 | `https://docs.blender.org/manual/en/latest/modeling/meshes/tools/{tool}.html` |
| Edge 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/{tool}.html` |
| Mesh 편집 | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/{tool}.html` |

## 참조 파일

| 파일 | 역할 |
|------|------|
| `course-site/assets/showme/_template.html` | 전체 CSS 원본 |
| `course-site/assets/showme/_registry.js` | 위젯 메타데이터 |
| `course-site/assets/showme/mirror-modifier.html` | 표준 참조 카드 (단일 기능) |
| `course-site/assets/showme/edit-mode-tools.html` | 복합 참조 카드 (다중 도구) |
| `course-site/week.html` | 모달 시스템, iframe 임베드 |
| `course-site/data/curriculum.js` | 주차별 showme 필드 |
| `course-site/assets/showme/_supplements.js` | 보충 설명 데이터 (프론트엔드 accordion) |
| `course-site/assets/showme/_supplements.json` | 보충 설명 데이터 (Notion sync용) |

> 보충 설명 생성은 `/brainstormC` 스킬 사용
