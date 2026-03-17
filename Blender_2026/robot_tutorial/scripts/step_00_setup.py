"""
Step 0: 씬 정리 + 레퍼런스 이미지 세팅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
클립 예상 시간: ~3분
학습 포인트:
  1. 기본 오브젝트 정리
  2. M키로 컬렉션 생성 → Light/Camera 이동
  3. 눈 토글(hide_viewport)로 숨기기
  4. 레퍼런스 이미지 3장 추가 (정면/뒷면/측면)
  5. 이미지 Opacity 0.1, Selectable False 설정
  6. References 컬렉션으로 정리
  7. Robot 컬렉션 생성 — 모델링 준비
"""
import bpy
import sys
import os
import time

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

from helpers import *
from record import start_recording, stop_recording

# ══════════════════════════════════════════
#  녹화 시작
# ══════════════════════════════════════════
start_recording("step_00_setup")
pause(DELAY_NORMAL)   # 녹화 안정화


def make_collection(name, parent=None):
    """컬렉션 생성 + 씬에 연결. 이미 있으면 재사용."""
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    if parent:
        parent.children.link(col)
    else:
        bpy.context.scene.collection.children.link(col)
    return col


def hide_layer_col(name):
    """Layer Collection 뷰포트 숨기기 (아웃라이너 눈 토글 효과)"""
    def _recurse(layer_col):
        for child in layer_col.children:
            if child.name == name:
                child.hide_viewport = True
                return True
            if _recurse(child):
                return True
        return False
    _recurse(bpy.context.view_layer.layer_collection)
    force_redraw()


def run():
    ensure_object_mode()

    # ──────────────────────────────────────
    # STEP 0-1  기본 Cube 삭제
    # ──────────────────────────────────────
    # [튜토리얼] 새 프로젝트를 시작할 때 항상 기본 Cube를 먼저 삭제합니다.
    # X 키 → Delete 로 삭제하는 습관을 들이세요.
    if 'Cube' in bpy.data.objects:
        select_only('Cube')
        bpy.ops.object.delete()
        force_redraw()
        pause(DELAY_NORMAL)

    # ──────────────────────────────────────
    # STEP 0-2  Light + Camera → Setup 컬렉션 이동
    # ──────────────────────────────────────
    # [튜토리얼] 기본 Light와 Camera는 지금 당장 필요 없습니다.
    # Shift+클릭으로 둘 다 선택한 뒤 M 키를 눌러
    # "Setup"이라는 새 컬렉션을 만들고 이동합니다.
    deselect_all()
    for name in ['Light', 'Camera']:
        if name in bpy.data.objects:
            bpy.data.objects[name].select_set(True)
    pause(DELAY_SHORT)  # 다중 선택 보여주기

    setup_col = make_collection('Setup')
    for name in ['Light', 'Camera']:
        if name in bpy.data.objects:
            move_to_collection(name, 'Setup')
    force_redraw()
    pause(DELAY_NORMAL)

    # ──────────────────────────────────────
    # STEP 0-3  Setup 컬렉션 눈 토글로 숨기기
    # ──────────────────────────────────────
    # [튜토리얼] 아웃라이너에서 컬렉션 옆 눈(👁) 아이콘을 클릭하면
    # 뷰포트에서 보이지 않게 됩니다. 작업 중 방해가 없어집니다.
    hide_layer_col('Setup')
    pause(DELAY_NORMAL)

    # ──────────────────────────────────────
    # STEP 0-4  References 컬렉션 생성
    # ──────────────────────────────────────
    # [튜토리얼] 레퍼런스 이미지는 별도 컬렉션으로 관리합니다.
    # 아웃라이너가 깔끔하게 유지되어 작업하기 편합니다.
    make_collection('References')
    pause(DELAY_SHORT)

    # ──────────────────────────────────────
    # STEP 0-5  레퍼런스 이미지 추가 (정면 / 뒷면 / 측면)
    # ──────────────────────────────────────
    # [튜토리얼] Shift+A → Image → Reference 로 이미지를 추가합니다.
    # 정면(Front), 뒷면(Back), 측면(Side) 3장을 각 평면에 정렬합니다.
    # 이후 투명도(Opacity)를 낮춰 작업 중 방해가 없게 합니다.

    ref_dir = os.path.abspath(os.path.join(_dir, "..", "references"))

    ref_configs = [
        {
            "path":     os.path.join(ref_dir, "robot_front.png"),
            "name":     "Ref_Front",
            "location": (0.0, -0.01, 0.0),
            "rotation": (1.5708, 0.0, 0.0),   # X +90° → 정면(XZ 평면)
            "view_align": "FRONT",
        },
        {
            "path":     os.path.join(ref_dir, "robot_back.png"),
            "name":     "Ref_Back",
            "location": (0.0,  0.01, 0.0),
            "rotation": (1.5708, 0.0, 3.1416),  # X +90°, Z +180° → 뒷면
            "view_align": "BACK",
        },
        {
            "path":     os.path.join(ref_dir, "robot_side.png"),
            "name":     "Ref_Side",
            "location": (-0.01, 0.0, 0.0),
            "rotation": (1.5708, 0.0, 1.5708),  # X +90°, Z +90° → 측면(YZ 평면)
            "view_align": "RIGHT",
        },
    ]

    for cfg in ref_configs:
        if not os.path.exists(cfg["path"]):
            print(f"⚠️  이미지 없음: {cfg['path']}")
            continue

        # Shift+A → Image → Reference
        bpy.ops.object.empty_image_add(
            filepath=cfg["path"],
            align='WORLD',
            location=cfg["location"],
            rotation=cfg["rotation"],
        )
        ref_obj = bpy.context.active_object
        ref_obj.name = cfg["name"]

        # ── 이미지 표시 설정 ──────────────────────────
        ref_obj.empty_display_size = 2.5

        # Opacity 0.1 — 작업 중 방해 최소화
        # [튜토리얼] Properties → Object Data(녹색) → Opacity 슬라이더
        if ref_obj.data:
            ref_obj.data.alpha = 0.1

        # 뒷면에 렌더 (메쉬 뒤로 밀어넣기)
        ref_obj.empty_image_depth = 'BACK'

        # 해당 방향에서만 보이도록
        ref_obj.empty_image_side = 'FRONT'

        # ── Selectable = False ────────────────────────
        # [튜토리얼] 레퍼런스를 실수로 선택하지 않도록
        # 아웃라이너에서 마우스 아이콘(☞)을 꺼줍니다.
        # 단축키: 아웃라이너 우클릭 → "Disable in Viewport"
        ref_obj.hide_select = True

        # References 컬렉션으로 이동
        move_to_collection(cfg["name"], 'References')

        force_redraw()
        pause(DELAY_NORMAL)

    # ──────────────────────────────────────
    # STEP 0-6  Robot 컬렉션 생성
    # ──────────────────────────────────────
    # [튜토리얼] 이제 로봇 파츠를 담을 "Robot" 컬렉션을 만듭니다.
    # 앞으로 모든 로봇 오브젝트는 이 컬렉션 안에 넣습니다.
    # 파츠별로 선택/숨기기가 편해집니다.
    make_collection('Robot')
    # Robot 컬렉션을 Active Collection으로 설정
    robot_layer = None
    def _find(lc, name):
        for c in lc.children:
            if c.name == name:
                return c
            found = _find(c, name)
            if found:
                return found
        return None
    robot_layer = _find(bpy.context.view_layer.layer_collection, 'Robot')
    if robot_layer:
        bpy.context.view_layer.active_layer_collection = robot_layer
    force_redraw()
    pause(DELAY_NORMAL)

    # ──────────────────────────────────────
    # STEP 0-7  뷰포트 정면 뷰로 전환 + 아웃라이너 확인
    # ──────────────────────────────────────
    # [튜토리얼] 레퍼런스 이미지를 확인하려면 정면(Front) 뷰로 전환합니다.
    # 숫자패드 1 또는 물결표(~) 키를 눌러 뷰를 전환하세요.
    set_view('FRONT')
    pause(DELAY_LONG)

    # 3/4 사선 뷰로 마무리
    set_view_quarter()
    pause(DELAY_NORMAL)

    # ──────────────────────────────────────
    # STEP 0-8  체크포인트 저장
    # ──────────────────────────────────────
    blend_path = os.path.abspath(
        os.path.join(_dir, "..", "checkpoints", "step_00_setup.blend")
    )
    bpy.ops.wm.save_as_mainfile(filepath=blend_path, copy=True)
    pause(DELAY_SHORT)
    print("✅ Step 0 완료!")
    pause(DELAY_STEP)


run()

# ══════════════════════════════════════════
#  녹화 종료
# ══════════════════════════════════════════
stop_recording()
print("🎬 step_00_setup.mp4 저장 완료")
