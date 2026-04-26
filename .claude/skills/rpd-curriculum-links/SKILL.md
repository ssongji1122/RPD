---
name: rpd-curriculum-links
description: >
  커리큘럼 task에 외부 링크 추가/점검. 수업 단계에서 외부 사이트 접속이나 파일 다운로드가 필요한
  task에 url 필드를 넣어서 수강생이 바로 이동할 수 있게 함.
  Use when: 새 주차 추가, 새 외부 서비스 연동, "링크 없는데요" 피드백.
---

# RPD Curriculum Links

## 역할
`data/curriculum.js`의 각 주차 step → task 항목에 `"url"` 필드를 관리한다.

링크가 있는 task는 week.html에서 아래처럼 렌더링됨:
```html
<a class="task-link" href="..." target="_blank" rel="noopener noreferrer">
  <svg><!-- external-link icon --></svg>
  www.blender.org/download
</a>
```
CSS: `tokens.css` → `.task-link`

---

## 데이터 스키마

```jsonc
// curriculum.js task 오브젝트
{
  "id": "w1-t1",
  "label": "blender.org 에서 다운로드 완료",
  "detail": "최신 LTS 버전 권장",   // optional: 토글 펼치면 보이는 보조 설명
  "url": "https://www.blender.org/download/"  // optional: 외부 링크
}
```

- `url`은 선택 필드 — 없으면 링크 미표시
- 링크는 task 레이블 바로 아래, detail 토글 위에 항상 노출됨 (숨겨진 detail 안에 넣지 않음)

---

## 현재 등록된 링크 목록

| task id | label | url |
|---------|-------|-----|
| w1-t1 | blender.org 에서 다운로드 완료 | https://www.blender.org/download/ |
| w5-t1 | Meshy 또는 Tripo에서 프롬프트 입력 후 생성 | https://www.meshy.ai/ |
| w6-bk4 | ambientcg.com 접속 → 'Concrete' 검색 → 1K PNG 다운로드 | https://ambientcg.com/ |
| w6-poly1 | withpoly.com 접속 → 텍스트 입력 | https://withpoly.com/browse/textures |
| w9-t5 | Poly Haven에서 HDRI 파일 다운로드 | https://polyhaven.com/hdris |
| w12-t4 | Mixamo.com 접속 후 FBX 파일 업로드 | https://www.mixamo.com/ |
| w12-t7 | Mixamo Animations 탭에서 걷기/달리기/춤 골라보기 | https://www.mixamo.com/#/?page=1&type=Animation |
| w12-t8 | FBX로 다운로드 (With Skin 옵션) | https://www.mixamo.com/ |

---

## 링크 추가 기준

링크가 **필요한** task:
- 외부 사이트 이름이 label에 등장 (`blender.org`, `Mixamo`, `Poly Haven`, `Meshy`, `Tripo`)
- "다운로드"가 포함되고 외부 소스에서 받는 경우
- "접속", "가입", "업로드" 등 사이트 방문이 전제된 경우

링크가 **불필요한** task:
- Blender 내부 UI 조작 (`Shader Editor 열기`, `Dope Sheet 열기` 등)
- 파일 시스템 작업 (`파일 저장`, `폴더에 넣기`)
- 순수 연습 동작 (`G로 이동`, `Tab으로 전환`)

---

## 알려진 외부 서비스 URL

| 서비스 | URL | 용도 |
|--------|-----|------|
| Blender 다운로드 | https://www.blender.org/download/ | 설치 파일 |
| Blender 공식 문서 | https://docs.blender.org/manual/en/latest/ | 레퍼런스 |
| Blender Studio | https://studio.blender.org/training/ | 튜토리얼 영상 |
| Poly Haven | https://polyhaven.com/hdris | HDRI 무료 다운로드 |
| Poly Haven (텍스처) | https://polyhaven.com/textures | 텍스처 무료 다운로드 |
| Mixamo | https://www.mixamo.com/ | 리깅 + 애니메이션 |
| Mixamo 애니메이션 탭 | https://www.mixamo.com/#/?page=1&type=Animation | 애니메이션 검색 |
| Meshy AI | https://www.meshy.ai/ | AI 3D 생성 |
| Tripo AI | https://www.tripo3d.ai/ | AI 3D 생성 (대안) |
| Sketchfab | https://sketchfab.com/ | 3D 에셋 다운로드 |
| AmbientCG | https://ambientcg.com/ | CC0 PBR 텍스처 무료 다운로드 |
| WithPoly | https://withpoly.com/browse/textures | AI 생성 PBR 텍스처 (무료 2K~8K) |

---

## 작업 절차

### 새 주차 추가 시
1. 새로 추가된 주차의 task label을 스캔
2. 위 "링크 필요 기준" 대조
3. 알려진 서비스이면 "알려진 외부 서비스 URL" 표에서 URL 가져와 추가
4. 모르는 서비스면 공식 사이트 URL 확인 후 추가
5. 이 스킬의 "현재 등록된 링크 목록" 표 업데이트

### 링크 추가 방법
```jsonc
// Before
{ "id": "w9-t5", "label": "Poly Haven에서 HDRI 파일 다운로드", "detail": "polyhaven.com → HDRIs" }

// After
{ "id": "w9-t5", "label": "Poly Haven에서 HDRI 파일 다운로드", "detail": "polyhaven.com → HDRIs",
  "url": "https://polyhaven.com/hdris" }
```

### 링크 검증
```bash
# 모든 task url 추출해서 확인
grep -n '"url"' course-site/data/curriculum.js | grep -v "assets/images\|docs.blender\|studio.blender\|youtu"
```

---

## 렌더링 코드 위치

- **템플릿**: `course-site/week.html` → `taskItems = tasks.map(...)` 내부
- **스타일**: `course-site/assets/tokens.css` → `.task-link` 섹션

렌더링 로직 변경이 필요하면 week.html의 `taskLinkHtml` 변수 수정.
