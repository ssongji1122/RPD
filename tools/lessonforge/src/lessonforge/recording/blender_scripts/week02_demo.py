"""Week 02 demo steps: Blender 인터페이스 & MCP 설정.

Each step is a dict loaded by BlenderAgent.run_demo_script():
  label : human-readable description shown in console
  code  : Python code executed inside Blender via blender-mcp
  wait  : seconds to pause AFTER executing code (gives viewer time to see result)

Corresponding lecture sections:
  Steps 1-4  → Step 1: 뷰 조작 연습 (View Navigation)
  Steps 5-9  → Step 2: Transform 기초
  Steps 10-11 → Step 3: Apply Transform
  Steps 12-13 → Step 4: Origin 설정
  Step 14    → Step 5: MCP 연결 확인 (informational only)
"""

STEPS = [
    # ───────────────────────────────────────────────────────
    # Step 1: 뷰 조작 연습 — 기본 씬 확인 및 UI 구조 소개
    # ───────────────────────────────────────────────────────
    {
        "label": "씬 초기화 — 기본 큐브 씬으로 시작",
        "code": (
            "import bpy\n"
            "# Reset to default scene with cube, camera, light\n"
            "bpy.ops.wm.read_homefile(use_empty=False)\n"
        ),
        "wait": 2.0,
    },
    {
        "label": "Solid 셰이딩 모드로 전환 (기본 작업 모드)",
        "code": (
            "import bpy\n"
            "for area in bpy.context.screen.areas:\n"
            "    if area.type == 'VIEW_3D':\n"
            "        for space in area.spaces:\n"
            "            if space.type == 'VIEW_3D':\n"
            "                space.shading.type = 'SOLID'\n"
            "                break\n"
            "print('Shading: SOLID')\n"
        ),
        "wait": 1.5,
    },
    {
        "label": "Material Preview 셰이딩 모드 확인 (Z키 파이 메뉴)",
        "code": (
            "import bpy\n"
            "for area in bpy.context.screen.areas:\n"
            "    if area.type == 'VIEW_3D':\n"
            "        for space in area.spaces:\n"
            "            if space.type == 'VIEW_3D':\n"
            "                space.shading.type = 'MATERIAL'\n"
            "                break\n"
            "print('Shading: MATERIAL')\n"
        ),
        "wait": 2.0,
    },
    {
        "label": "Solid 모드로 복귀 — 일반 실습 모드",
        "code": (
            "import bpy\n"
            "for area in bpy.context.screen.areas:\n"
            "    if area.type == 'VIEW_3D':\n"
            "        for space in area.spaces:\n"
            "            if space.type == 'VIEW_3D':\n"
            "                space.shading.type = 'SOLID'\n"
            "                break\n"
        ),
        "wait": 1.0,
    },

    # ───────────────────────────────────────────────────────
    # Step 2: Transform 기초 — G, R, S 시연
    # ───────────────────────────────────────────────────────
    {
        "label": "큐브 선택 확인",
        "code": (
            "import bpy\n"
            "cube = bpy.data.objects.get('Cube')\n"
            "if cube:\n"
            "    bpy.ops.object.select_all(action='DESELECT')\n"
            "    cube.select_set(True)\n"
            "    bpy.context.view_layer.objects.active = cube\n"
            "    print(f'Selected: {cube.name}')\n"
        ),
        "wait": 1.5,
    },
    {
        "label": "G (이동) — X축으로 2미터 이동",
        "code": (
            "import bpy\n"
            "cube = bpy.context.active_object\n"
            "if cube:\n"
            "    cube.location.x = 2.0\n"
            "    print(f'Location: {cube.location[:]}')\n"
        ),
        "wait": 2.0,
    },
    {
        "label": "R (회전) — Z축 기준 45도 회전",
        "code": (
            "import bpy, math\n"
            "cube = bpy.context.active_object\n"
            "if cube:\n"
            "    cube.rotation_euler.z = math.radians(45)\n"
            "    print(f'Rotation Z: 45 deg')\n"
        ),
        "wait": 2.0,
    },
    {
        "label": "S (스케일) — 전체 크기 2배 확대",
        "code": (
            "import bpy\n"
            "cube = bpy.context.active_object\n"
            "if cube:\n"
            "    cube.scale = (2.0, 2.0, 2.0)\n"
            "    print(f'Scale: {cube.scale[:]}')\n"
        ),
        "wait": 2.0,
    },
    {
        "label": "Properties Panel에서 현재 Transform 값 출력",
        "code": (
            "import bpy\n"
            "cube = bpy.context.active_object\n"
            "if cube:\n"
            "    loc = cube.location[:]\n"
            "    rot = [round(r * 57.2958, 1) for r in cube.rotation_euler]\n"
            "    scl = cube.scale[:]\n"
            "    print(f'Location: {loc}')\n"
            "    print(f'Rotation (deg): {rot}')\n"
            "    print(f'Scale: {scl}')\n"
        ),
        "wait": 2.5,
    },

    # ───────────────────────────────────────────────────────
    # Step 3: Apply Transform — Ctrl+A
    # ───────────────────────────────────────────────────────
    {
        "label": "Apply All Transforms (Ctrl+A) — Scale을 (1,1,1)로 초기화",
        "code": (
            "import bpy\n"
            "bpy.ops.object.transform_apply(\n"
            "    location=True, rotation=True, scale=True\n"
            ")\n"
            "cube = bpy.context.active_object\n"
            "if cube:\n"
            "    print(f'After Apply — Scale: {cube.scale[:]}')\n"
        ),
        "wait": 2.5,
    },
    {
        "label": "Apply Transform 전후 비교 확인",
        "code": (
            "import bpy\n"
            "cube = bpy.context.active_object\n"
            "if cube:\n"
            "    print('Apply Transform 완료!')\n"
            "    print(f'  Location: {cube.location[:]}')\n"
            "    print(f'  Scale: {cube.scale[:]} (모두 1이어야 함)')\n"
        ),
        "wait": 2.0,
    },

    # ───────────────────────────────────────────────────────
    # Step 4: Origin 설정
    # ───────────────────────────────────────────────────────
    {
        "label": "Origin to Geometry — Origin을 메시 중심으로 설정",
        "code": (
            "import bpy\n"
            "bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')\n"
            "cube = bpy.context.active_object\n"
            "if cube:\n"
            "    print(f'Origin: {cube.location[:]}')\n"
        ),
        "wait": 2.0,
    },
    {
        "label": "3D Cursor를 원점으로 리셋, Origin to 3D Cursor 시연",
        "code": (
            "import bpy\n"
            "# Reset 3D cursor to world origin\n"
            "bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)\n"
            "# Set origin to 3D cursor position\n"
            "bpy.ops.object.origin_set(type='ORIGIN_CURSOR')\n"
            "print('Origin moved to 3D Cursor (world origin)')\n"
        ),
        "wait": 2.5,
    },

    # ───────────────────────────────────────────────────────
    # Step 5: MCP 연결 확인 (정보용 — 코드는 Blender에서 이미 연결 중)
    # ───────────────────────────────────────────────────────
    {
        "label": "Blender MCP 연결 상태 확인 — 이 메시지가 보이면 연결 성공!",
        "code": (
            "import bpy\n"
            "print('=' * 50)\n"
            "print('Blender MCP 연결 확인 완료!')\n"
            "print(f'Blender Version: {bpy.app.version_string}')\n"
            "print(f'Scene Objects: {[o.name for o in bpy.context.scene.objects]}')\n"
            "print('Claude에서 Blender를 직접 조작할 수 있습니다.')\n"
            "print('=' * 50)\n"
        ),
        "wait": 3.0,
    },
]
