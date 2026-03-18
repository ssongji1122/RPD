# Blender Show Me Integration

## Current icon mapping

- `edit-mode` -> `ops.generic.select_box`
- `edit-mode-tools` -> `ops.mesh.polybuild_hover`
- `extrude` -> `ops.mesh.extrude_region_move`
- `loop-cut` -> `ops.mesh.loopcut_slide`
- `inset` -> `ops.mesh.inset`
- `bevel-tool` -> `ops.mesh.bevel`
- `poly-circle` -> `ops.mesh.spin`

## Archive paths

- Registry metadata: `course-site/assets/showme/_registry.js`
- Icon assets: `course-site/assets/showme/icons/`
- Week page renderer: `course-site/week.html`

## Capture command

```bash
SHOWME_ICON_GALLERY_OUTPUT="$PWD/output/blender-showme-icons-gallery.png" \
"/Applications/Blender.app/Contents/MacOS/Blender" \
  --factory-startup \
  --python "$PWD/.claude/skills/blender-showme-icons/scripts/capture_showme_icon_gallery.py"
```

## Extraction command

```bash
python3 "$PWD/.claude/skills/blender-showme-icons/scripts/extract_showme_icons.py" \
  --gallery "$PWD/output/blender-showme-icons-gallery.png" \
  --output-dir "$PWD/course-site/assets/showme/icons"
```

## Browser verification pattern

1. `course-site/` 에서 로컬 서버 실행
2. `week.html?week=3` 열기
3. 모델링 Show Me 카드가 들어 있는 step 펼치기
4. Show Me 카드 묶음 스크린샷 찍기
5. `Extrude` 같은 대표 카드 열기
6. 모달 컨테이너 스크린샷 찍기

## Notes

- extractor는 `capture_showme_icon_gallery.py` 가 만드는 갤러리 레이아웃에 맞춰져 있습니다.
- Blender 버전이나 popup 레이아웃이 크게 바뀌면 `scripts/extract_showme_icons.py` 의 crop box를 다시 맞춥니다.
- 렌더러가 이미 PNG 자산을 지원하면, 카드 전체를 다시 디자인하기보다 badge 안 이미지 크기부터 조정합니다.
