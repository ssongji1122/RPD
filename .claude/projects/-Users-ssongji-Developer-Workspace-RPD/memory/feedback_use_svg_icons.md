---
name: use-svg-icon-library
description: UI 아이콘에 이모지 대신 Lucide Icons SVG 세트를 사용할 것
type: feedback
---

UI 아이콘에 이모지(📦📊⚙ 등)를 쓰지 말 것. Lucide Icons 같은 SVG 아이콘 세트를 사용할 것.

**Why:** 이모지는 OS마다 다르게 렌더링되고, 디자인 통일감이 없으며, 테마 색상 적용이 불가능. SVG 아이콘은 `currentColor`로 테마 대응, stroke-width로 굵기 통일, 크기 자유 조절 가능.

**How to apply:** 사이드바, 탭, 버튼 등 모든 UI 아이콘에 Lucide Icons CDN(`unpkg.com/lucide-static`) 또는 인라인 SVG 사용. 이모지는 콘텐츠(카드 설명 등)에서만 허용.
