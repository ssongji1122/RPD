"""
showme_phase2_build.py — Phase 2 local build (8 cards, no Notion token required)
==================================================================================
Builds 8 Phase 2 cards from in-process Notion-shaped JSON. Writes:
- tests/fixtures/showme/cards/{card_id}.json (for snapshot tests)
- course-site/assets/showme/{card_id}.html
- course-site/assets/showme/_registry.js (merged with legacy)
- course-site/assets/showme/_catalog.json (merged with legacy)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from showme_lib.index import build_catalog_json_merged, build_registry_js_merged  # noqa: E402
from showme_lib.notion_cards import normalize_card_page  # noqa: E402
from showme_lib.renderer import render_card_html  # noqa: E402

TEMPLATE_PATH = ROOT / "course-site" / "assets" / "showme" / "_template.v2.html"
OUTPUT_DIR = ROOT / "course-site" / "assets" / "showme"
REGISTRY_PATH = OUTPUT_DIR / "_registry.js"
CATALOG_PATH = OUTPUT_DIR / "_catalog.json"
FIXTURES_DIR = ROOT / "tests" / "fixtures" / "showme" / "cards"


def _rt(text: str) -> dict:
    return {"rich_text": [{"plain_text": text}]} if text else {"rich_text": []}


def _title(text: str) -> dict:
    return {"title": [{"plain_text": text}]}


def _select(name: str) -> dict:
    return {"select": {"name": name}}


def _multi(names: list[str]) -> dict:
    return {"multi_select": [{"name": n} for n in names]}


def _url(u: str) -> dict:
    return {"url": u}


def _make_page(page_id: str, card_id: str, label: str, icon: str, category: str,
               weeks: list[str], priority: str, status: str, concept: str, usage: str,
               pitfall: str, steps_json_str: str, widget_id: str, official_docs: str) -> dict:
    return {
        "object": "page",
        "id": page_id,
        "properties": {
            "card_id": _title(card_id),
            "label": _rt(label),
            "icon": _rt(icon),
            "category": _select(category),
            "week": _multi(weeks),
            "priority": _select(priority),
            "status": _select(status),
            "concept_md": _rt(concept),
            "usage_md": _rt(usage),
            "pitfall_md": _rt(pitfall),
            "steps_json": _rt(steps_json_str),
            "widget_id": _rt(widget_id),
            "blender_version": _rt("5.0"),
            "official_docs": _url(official_docs),
            "prerequisites": {"relation": []},
            "related": {"relation": []},
            "videos_relation": {"relation": []},
        },
    }


CARDS = [
    _make_page(
        page_id="36454d65-4971-817e-a665-c900d9960073",
        card_id="collection-outliner",
        label="Collection 과 Outliner 이해",
        icon="🗂️",
        category="object",
        weeks=["3"],
        priority="P0",
        status="published",
        concept=(
            "Collection은 **폴더**처럼 오브젝트를 묶는 단위예요. Outliner는 그 폴더 구조를 보여주는 트리.\n\n"
            "로봇처럼 파츠가 많은 모델은 머리/몸통/팔/다리를 Collection으로 분리하면 가시성, 선택 잠금, "
            "일괄 조작이 한결 쉬워져요. 책상 위에 부품을 통 안에 나눠 담는 것과 같아요."
        ),
        usage="파츠 수가 많아질 때, 좌우 대칭 작업 중 한쪽만 숨기고 싶을 때, 렌더에서 일부만 제외하고 싶을 때.",
        pitfall=(
            "Outliner 옆 두 아이콘은 역할이 달라요. **눈 아이콘 = 뷰포트 가시성**, "
            "**모니터(카메라) 아이콘 = 렌더 가시성**. 렌더에서만 사라지는 파츠가 있다면 모니터 아이콘이 꺼져 있는 거예요."
        ),
        steps_json_str=json.dumps({
            "blender_version": "5.0",
            "platform_note": None,
            "steps": [
                {"n": 1, "action": "Outliner 빈 공간 우클릭 → New Collection", "hotkey": None, "menu": "Outliner > New Collection", "screenshot": None, "note": None},
                {"n": 2, "action": "오브젝트 선택 후 Collection으로 이동", "hotkey": "M", "menu": "Move to Collection", "screenshot": None, "note": None},
                {"n": 3, "action": "뷰포트에서 Collection 숨기기/보이기", "hotkey": None, "menu": "눈 아이콘 클릭", "screenshot": None, "note": "H로도 토글 가능"},
                {"n": 4, "action": "Collection 선택 잠금", "hotkey": None, "menu": "화살표(필터) 아이콘 클릭", "screenshot": None, "note": "실수로 움직이는 것 방지"},
            ],
        }, ensure_ascii=False),
        widget_id="",
        official_docs="https://docs.blender.org/manual/en/latest/scene_layout/collections/index.html",
    ),
    _make_page(
        page_id="36554d65-4971-81a6-9dda-c7f8402b36ed",
        card_id="modifier-stack-order",
        label="Modifier Stack 순서",
        icon="📚",
        category="modifier",
        weeks=["3"],
        priority="P0",
        status="draft",
        concept=(
            "Modifier는 **요리 레시피**처럼 위에서 아래로 순서대로 계산돼요. **같은 재료라도 넣는 순서가 다르면 결과가 달라져요.**\n\n"
            "가장 안전한 시작 순서는 **Mirror → Boolean → Subdivision Surface → Bevel → Weighted Normal**. "
            "Mirror로 좌우 대칭을 먼저 잡고, Boolean으로 구멍을 뚫고, 마지막에 Subdivision으로 부드럽게 만드는 흐름이에요."
        ),
        usage="여러 Modifier를 같이 쓸 때 결과가 의도와 다르게 보이면 가장 먼저 순서를 점검해요. Stack 핸들(::)을 드래그하거나 화살표 아이콘으로 위/아래로 옮길 수 있어요.",
        pitfall=(
            "**Subdivision Surface를 먼저 넣고 Boolean을 하면** 곡면이 깨져서 결과가 지저분해져요. "
            "Subdivision은 거의 항상 마지막 또는 끝에서 두 번째로 두는 게 안전해요. "
            "Weighted Normal은 Bevel 이후에 와야 음영 정리가 의도대로 됩니다."
        ),
        steps_json_str=json.dumps({
            "blender_version": "5.0",
            "platform_note": None,
            "steps": [
                {"n": 1, "action": "Properties 패널 > 렌치 아이콘(Modifier Properties) 열기", "hotkey": None, "menu": "Properties > 🔧", "screenshot": None, "note": None},
                {"n": 2, "action": "Modifier 항목 좌측의 핸들(::) 잡기", "hotkey": None, "menu": None, "screenshot": None, "note": "드래그해서 위/아래로 이동"},
                {"n": 3, "action": "메뉴에서 Move Up / Move Down 선택", "hotkey": None, "menu": "Modifier 우상단 ▾ > Move Up/Down", "screenshot": None, "note": None},
                {"n": 4, "action": "권장 순서: Mirror → Boolean → Subdivision → Bevel → Weighted Normal", "hotkey": None, "menu": None, "screenshot": None, "note": "Apply 타이밍은 가장 마지막"},
            ],
        }, ensure_ascii=False),
        widget_id="",
        official_docs="https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html#the-modifier-stack",
    ),
    _make_page(
        page_id="36554d65-4971-81a2-af13-c94666c69e98",
        card_id="shade-smooth-auto-smooth",
        label="Shade Smooth & Auto Smooth",
        icon="✨",
        category="modeling",
        weeks=["3", "4"],
        priority="P0",
        status="draft",
        concept=(
            "같은 메쉬도 **빛이 부드럽게 흐르는지 / 면마다 뚝뚝 끊기는지** 셰이딩 모드로 바뀌어요. "
            "**Flat**은 모든 면을 각진 그대로, **Shade Smooth**는 전체를 부드럽게 보간해요.\n\n"
            "**Auto Smooth by Angle**은 절충안 — 각도가 작은 모서리는 부드럽게, 큰 모서리(예: 30° 초과)는 날카롭게 유지해요. "
            "로봇처럼 모서리와 곡면이 섞인 모델에 가장 자주 써요."
        ),
        usage="원기둥·구·캐릭터 등 부드러워야 할 모델에는 Shade Smooth. 로봇·도구처럼 일부 모서리가 살아야 하는 모델에는 Auto Smooth by Angle (30~45°).",
        pitfall=(
            "Shade Smooth만 켜면 **모서리까지 다 뭉개져요.** Auto Smooth 각도가 너무 작으면(예: 10°) 부드러워야 할 곳도 끊겨 보이고, "
            "너무 크면(예: 80°) 뭉개져요. **30° 근처에서 시작**해서 모델 보면서 조정하세요. "
            "Blender 5.0에서는 Object Data Properties → Normals → Auto Smooth 토글로 들어가요."
        ),
        steps_json_str=json.dumps({
            "blender_version": "5.0",
            "platform_note": None,
            "steps": [
                {"n": 1, "action": "Object Mode에서 메쉬 우클릭", "hotkey": None, "menu": "Object Context Menu", "screenshot": None, "note": None},
                {"n": 2, "action": "Shade Smooth 선택", "hotkey": None, "menu": "Shade Smooth", "screenshot": None, "note": "전체 매끄럽게"},
                {"n": 3, "action": "Properties > Object Data (역삼각형) > Normals", "hotkey": None, "menu": "Object Data Properties", "screenshot": None, "note": "Blender 5.0 위치"},
                {"n": 4, "action": "Auto Smooth 토글 → Angle 입력", "hotkey": None, "menu": None, "screenshot": None, "note": "보통 30°로 시작"},
            ],
        }, ensure_ascii=False),
        widget_id="",
        official_docs="https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html#shade-smooth-flat",
    ),
    _make_page(
        page_id="36554d65-4971-8194-83a4-d665dfe663f8",
        card_id="merge-by-distance",
        label="Merge by Distance (겹친 버텍스 정리)",
        icon="🧹",
        category="edit-mode",
        weeks=["3", "4"],
        priority="P0",
        status="draft",
        concept=(
            "Boolean이나 Extrude를 잘못 누르면 **같은 자리에 버텍스가 두 개씩 쌓여요**. "
            "눈에는 멀쩡해 보여도 메쉬가 끊어진 상태라 Subdivision이 깨지거나 Smooth가 이상하게 적용돼요.\n\n"
            "**Merge by Distance**는 설정한 거리 안에 있는 버텍스를 하나로 합쳐주는 청소 도구예요. "
            "빨래 짤 때 물기 빼듯, 메쉬에서 중복 정보를 짜내는 작업."
        ),
        usage="Boolean 직후, Mirror에 Clipping 없이 작업한 직후, 외부 메쉬(AI 생성·STL import)를 받았을 때 가장 먼저 돌려요. Subdivision이 갑자기 이상해지면 십중팔구 중복 버텍스가 원인.",
        pitfall=(
            "거리가 너무 크면(예: 1m) **분리되어 있어야 할 버텍스까지 합쳐져** 메쉬가 뭉개져요. "
            "기본값 **0.0001m**부터 시작하고, 안 합쳐지면 단계적으로 키워요. "
            "작업 후에는 합쳐진 개수가 화면 하단에 표시돼요 — 'Removed 12 vertices' 같은 메시지."
        ),
        steps_json_str=json.dumps({
            "blender_version": "5.0",
            "platform_note": None,
            "steps": [
                {"n": 1, "action": "Edit Mode 진입", "hotkey": "Tab", "menu": None, "screenshot": None, "note": None},
                {"n": 2, "action": "전체 선택", "hotkey": "A", "menu": None, "screenshot": None, "note": None},
                {"n": 3, "action": "Merge 메뉴 열기", "hotkey": "M", "menu": "Mesh > Merge", "screenshot": None, "note": None},
                {"n": 4, "action": "By Distance 선택", "hotkey": None, "menu": "By Distance", "screenshot": None, "note": None},
                {"n": 5, "action": "좌하단 패널에서 거리 조정", "hotkey": None, "menu": "Merge Distance", "screenshot": None, "note": "0.0001m → 0.001m 순으로"},
            ],
        }, ensure_ascii=False),
        widget_id="",
        official_docs="https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/merge.html#by-distance",
    ),
    _make_page(
        page_id="36554d65-4971-8117-8aa6-f6297514e709",
        card_id="bridge-edge-loops",
        label="Bridge Edge Loops (열린 루프 연결)",
        icon="🌉",
        category="edit-mode",
        weeks=["4"],
        priority="P0",
        status="draft",
        concept=(
            "모자와 머리를 따로 만들었는데 둘이 안 붙어 있다면 **두 열린 루프를 다리(bridge)로 연결**해야 해요. "
            "Bridge Edge Loops는 두 Edge 루프 사이에 면을 자동으로 만들어줘요.\n\n"
            "휴지심 두 개를 마주 보게 놓고 사이에 종이를 감아 붙이는 것과 비슷해요. 빈 공간을 면으로 메워주는 도구."
        ),
        usage="파츠를 따로 만든 뒤 하나의 메쉬로 합쳐야 할 때, 구멍(Delete Face로 만든)을 다른 메쉬 루프와 연결할 때, 캐릭터 모자·후드·옷깃처럼 두 표면을 잇는 형태를 만들 때.",
        pitfall=(
            "**두 루프의 버텍스 개수가 다르면** 결과 토폴로지가 지저분해져요. "
            "비슷한 개수로 맞춘 뒤 Bridge 하거나, 한쪽을 Loop Cut으로 분할해 개수를 맞춰요. "
            "**두 루프가 같은 메쉬에 있어야** 동작해요 — 다른 오브젝트면 먼저 `Ctrl + J`로 Join."
        ),
        steps_json_str=json.dumps({
            "blender_version": "5.0",
            "platform_note": None,
            "steps": [
                {"n": 1, "action": "두 루프가 다른 오브젝트면 Join", "hotkey": "Ctrl + J", "menu": None, "screenshot": None, "note": "Object Mode에서"},
                {"n": 2, "action": "Edit Mode 진입 + Edge 모드", "hotkey": "Tab → 2", "menu": None, "screenshot": None, "note": None},
                {"n": 3, "action": "두 루프 선택 (Alt+클릭으로 루프 단위 선택, Shift+Alt+클릭으로 추가)", "hotkey": None, "menu": None, "screenshot": None, "note": None},
                {"n": 4, "action": "Bridge Edge Loops 실행", "hotkey": None, "menu": "Edge > Bridge Edge Loops", "screenshot": None, "note": None},
            ],
        }, ensure_ascii=False),
        widget_id="",
        official_docs="https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/bridge_edge_loops.html",
    ),
    _make_page(
        page_id="36554d65-4971-8197-945a-ccd77cc4e56e",
        card_id="duplicate-vs-linked-duplicate",
        label="Duplicate vs Linked Duplicate",
        icon="🔗",
        category="object",
        weeks=["4"],
        priority="P1",
        status="draft",
        concept=(
            "**Duplicate (Shift+D)**는 완전 복사 — 원본과 무관한 별개 오브젝트가 생겨요. 한쪽을 수정해도 다른 쪽엔 영향 없어요.\n\n"
            "**Linked Duplicate (Alt+D)**는 **같은 메쉬 데이터를 공유하는 인스턴스**. "
            "한쪽 Edit Mode에서 수정하면 모든 복제본이 동시에 변해요. 한 손가락을 만들면 다섯 손가락이 동시에 갱신되는 식."
        ),
        usage="같은 모양 부품을 여러 개 배치하면서 **나중에 한 번에 수정**하고 싶으면 Linked Duplicate. 복사 후 **개별적으로 다르게** 변형할 거면 일반 Duplicate.",
        pitfall=(
            "Linked Duplicate를 만든 뒤 한쪽을 따로 수정하고 싶어졌다면 `U > Object & Data`로 메쉬 데이터 연결을 끊을 수 있어요. "
            "거꾸로 Linked로 만들었는지 알려면 Outliner에서 오브젝트 아래 메쉬 아이콘 옆 숫자(예: `2`)를 확인하세요."
        ),
        steps_json_str=json.dumps({
            "blender_version": "5.0",
            "platform_note": None,
            "steps": [
                {"n": 1, "action": "오브젝트 선택", "hotkey": None, "menu": None, "screenshot": None, "note": None},
                {"n": 2, "action": "일반 복제 (독립)", "hotkey": "Shift + D", "menu": "Object > Duplicate Objects", "screenshot": None, "note": None},
                {"n": 3, "action": "연결 복제 (메쉬 공유)", "hotkey": "Alt + D", "menu": "Object > Duplicate Linked", "screenshot": None, "note": None},
                {"n": 4, "action": "연결 끊기 (필요 시)", "hotkey": "U", "menu": "Object > Make Single User > Object & Data", "screenshot": None, "note": None},
            ],
        }, ensure_ascii=False),
        widget_id="",
        official_docs="https://docs.blender.org/manual/en/latest/scene_layout/object/editing/duplicate.html",
    ),
    _make_page(
        page_id="36554d65-4971-81e7-969e-f783bac8aad7",
        card_id="face-orientation-normals",
        label="Face Orientation & Normals",
        icon="🧭",
        category="edit-mode",
        weeks=["3", "4", "6"],
        priority="P1",
        status="draft",
        concept=(
            "모든 면에는 **앞면/뒷면 방향(Normal)**이 있어요. Blender는 앞면을 파란색, 뒷면을 빨간색으로 표시할 수 있어요 — "
            "**Viewport Overlays > Face Orientation**.\n\n"
            "쿠키 모양 틀이 뒤집힌 채로 반죽을 누르면 모양이 거꾸로 나오죠? Normal이 뒤집힌 면도 마찬가지로 셰이딩·렌더·Boolean에서 이상한 결과를 만들어요."
        ),
        usage="Boolean 결과가 이상할 때, Auto Smooth가 한쪽만 어색할 때, 렌더에 검은 얼룩이 보일 때 가장 먼저 Face Orientation 오버레이를 켜고 확인.",
        pitfall=(
            "빨간 면을 발견하면 `Mesh > Normals > Recalculate Outside` (`Shift+N`)로 일괄 정리. "
            "일부만 뒤집고 싶으면 면 선택 후 `Alt+N > Flip`. "
            "**AI로 생성한 메쉬는 Normal이 일관성 없게 들어오는 경우가 많아** 항상 한 번 점검하세요."
        ),
        steps_json_str=json.dumps({
            "blender_version": "5.0",
            "platform_note": None,
            "steps": [
                {"n": 1, "action": "Viewport Overlays 메뉴 열기", "hotkey": None, "menu": "뷰포트 우상단 두 원 겹친 아이콘", "screenshot": None, "note": None},
                {"n": 2, "action": "Face Orientation 토글", "hotkey": None, "menu": "Geometry > Face Orientation", "screenshot": None, "note": "파랑=앞, 빨강=뒤"},
                {"n": 3, "action": "Edit Mode에서 일괄 재계산", "hotkey": "Shift + N", "menu": "Mesh > Normals > Recalculate Outside", "screenshot": None, "note": None},
                {"n": 4, "action": "특정 면만 뒤집기", "hotkey": "Alt + N", "menu": "Mesh > Normals > Flip", "screenshot": None, "note": "Flip 선택"},
            ],
        }, ensure_ascii=False),
        widget_id="",
        official_docs="https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html",
    ),
    _make_page(
        page_id="36554d65-4971-816e-90b6-fb5035e90b65",
        card_id="apply-modifier-vs-keep-procedural",
        label="Apply Modifier vs 비파괴 유지",
        icon="🔒",
        category="modifier",
        weeks=["3", "4"],
        priority="P1",
        status="draft",
        concept=(
            "Modifier는 **투명한 효과 필름**이에요. 값을 바꾸거나 끄거나 지우면 원본 메쉬는 그대로 남아요 — "
            "이게 **비파괴(Non-destructive)**.\n\n"
            "**Apply**는 그 필름을 원본에 도장 찍어버리는 작업. 한 번 Apply하면 더 이상 값을 못 바꿔요. "
            "사진 보정에서 RAW를 JPEG으로 굳히는 것과 비슷. 보정 정보가 사라지면 되돌릴 수 없죠."
        ),
        usage="**보통은 Apply 하지 마세요.** Apply가 필요한 시점은 (1) 다음 Modifier가 Apply된 결과를 입력으로 받아야 할 때, (2) 외부로 export할 때(FBX/GLTF), (3) Edit Mode에서 수동으로 다듬어야 할 때.",
        pitfall=(
            "**Apply Transform (`Ctrl+A`)과 Apply Modifier는 달라요.** Ctrl+A는 Object의 위치/회전/크기를 수치적으로 정리하는 거고, "
            "Modifier Apply는 효과를 메쉬에 굳히는 거예요. Modifier Apply는 거의 항상 **맨 마지막에만** 합니다. "
            "Mirror를 너무 일찍 Apply하면 좌우 비대칭으로 다듬기 어려워져요."
        ),
        steps_json_str=json.dumps({
            "blender_version": "5.0",
            "platform_note": None,
            "steps": [
                {"n": 1, "action": "Modifier 우상단 ▾ 메뉴 열기", "hotkey": None, "menu": "Modifier > ▾", "screenshot": None, "note": None},
                {"n": 2, "action": "Apply 선택", "hotkey": None, "menu": "Apply", "screenshot": None, "note": "되돌리기 어려움"},
                {"n": 3, "action": "Apply 대신 Visibility 토글로 임시 확인", "hotkey": None, "menu": "Modifier 패널 눈/모니터 아이콘", "screenshot": None, "note": "비파괴 유지"},
                {"n": 4, "action": "여러 Modifier 일괄 적용은 Object Convert", "hotkey": None, "menu": "Object > Convert > Mesh", "screenshot": None, "note": "스택 전체를 Mesh로 굳힘"},
            ],
        }, ensure_ascii=False),
        widget_id="",
        official_docs="https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html#applying",
    ),
]


def main() -> int:
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    template = TEMPLATE_PATH.read_text()
    cards = []

    for page in CARDS:
        card_id = page["properties"]["card_id"]["title"][0]["plain_text"]
        # write fixture
        fixture_path = FIXTURES_DIR / f"{card_id}.json"
        fixture_path.write_text(json.dumps(page, ensure_ascii=False, indent=2))
        # render
        card = normalize_card_page(page, video_pages_by_id={})
        html = render_card_html(card, template)
        (OUTPUT_DIR / f"{card_id}.html").write_text(html, encoding="utf-8")
        cards.append(card)
        print(f"  wrote course-site/assets/showme/{card_id}.html + fixture")

    REGISTRY_PATH.write_text(build_registry_js_merged(cards, REGISTRY_PATH), encoding="utf-8")
    CATALOG_PATH.write_text(build_catalog_json_merged(cards, CATALOG_PATH), encoding="utf-8")
    print(f"\nregenerated _registry.js (merged)")
    print(f"regenerated _catalog.json (merged)")
    print(f"total: {len(cards)} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
