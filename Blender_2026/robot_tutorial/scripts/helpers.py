"""
helpers.py — Robot Tutorial 공통 헬퍼 함수
"""
import bpy
import bmesh
import time
import math
import os

# ─── 타이밍 상수 ─────────────────────────────────────
DELAY_SHORT = 0.5
DELAY_NORMAL = 1.5
DELAY_LONG = 2.5
DELAY_STEP = 3.0

# ─── 색상 팔레트 ─────────────────────────────────────
MINT_GREEN    = (0.267, 0.761, 0.490, 1.0)   # #44C27D 더 정확한 민트
BLACK_JOINT   = (0.05,  0.05,  0.05,  1.0)
GOLD_TRIM     = (0.85,  0.65,  0.13,  1.0)
WHITE_EMIT    = (1.0,   1.0,   1.0,   1.0)
GRAY_BG       = (0.85,  0.85,  0.85,  1.0)

# ─── 뷰포트 갱신 ─────────────────────────────────────
def force_redraw():
    bpy.context.view_layer.update()
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

# ─── 뷰 앵글 ─────────────────────────────────────────
def set_view(direction='FRONT'):
    """FRONT / BACK / RIGHT / LEFT / TOP / BOTTOM"""
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                region = next((r for r in area.regions if r.type == 'WINDOW'), None)
                if region:
                    with bpy.context.temp_override(window=window, area=area, region=region):
                        bpy.ops.view3d.view_axis(type=direction)
                return
    time.sleep(DELAY_SHORT)

def set_view_quarter(rx=63.6, rz=46.0):
    """3/4 사선 앵글"""
    from mathutils import Euler
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            rv3d = area.spaces[0].region_3d
            rv3d.view_rotation = Euler(
                (math.radians(rx), 0, math.radians(rz))
            ).to_quaternion()
            break
    force_redraw()
    time.sleep(DELAY_SHORT)

def set_xray(on=True):
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].shading.show_xray = on
            break
    force_redraw()

def set_shading(mode='SOLID'):
    """WIREFRAME / SOLID / MATERIAL / RENDERED"""
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].shading.type = mode
            break
    force_redraw()

# ─── 오브젝트 헬퍼 ───────────────────────────────────
def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')

def select_only(name):
    deselect_all()
    obj = bpy.data.objects[name]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    return obj

def ensure_object_mode():
    obj = bpy.context.active_object
    if obj and obj.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

def apply_scale(name=None):
    if name:
        select_only(name)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

def move_to_collection(obj_name, col_name):
    obj = bpy.data.objects[obj_name]
    if col_name not in bpy.data.collections:
        col = bpy.data.collections.new(col_name)
        bpy.context.scene.collection.children.link(col)
    col = bpy.data.collections[col_name]
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)

# ─── 모디파이어 헬퍼 ─────────────────────────────────
def add_mirror(obj_name, clipping=True):
    obj = bpy.data.objects[obj_name]
    mod = obj.modifiers.new("Mirror", 'MIRROR')
    mod.use_clip = clipping
    mod.use_axis = (True, False, False)
    force_redraw()
    time.sleep(DELAY_SHORT)
    return mod

def add_subsurf(obj_name, levels=2):
    obj = bpy.data.objects[obj_name]
    mod = obj.modifiers.new("Subdivision", 'SUBSURF')
    mod.levels = levels
    mod.render_levels = levels
    force_redraw()
    time.sleep(DELAY_SHORT)
    return mod

def delete_half(obj_name, axis='X', keep_negative=True):
    """Mirror 준비 — 한쪽 반 삭제
    keep_negative=True → 음수 방향만 남김 (기본 X 축)
    """
    ensure_object_mode()
    obj = select_only(obj_name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    bm = bmesh.from_edit_mesh(obj.data)
    ai = {'X': 0, 'Y': 1, 'Z': 2}[axis]
    for v in bm.verts:
        val = v.co[ai]
        if keep_negative:
            v.select = val > 0.0001
        else:
            v.select = val < -0.0001
    bmesh.update_edit_mesh(obj.data)

    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    force_redraw()
    time.sleep(DELAY_SHORT)

# ─── 머티리얼 헬퍼 ───────────────────────────────────
def make_material(name, color, metallic=0.0, roughness=0.3):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

def make_glass(name):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.9, 0.95, 1.0, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.0
    bsdf.inputs["Transmission Weight"].default_value = 1.0
    bsdf.inputs["IOR"].default_value = 1.45
    return mat

def make_emission(name, color, strength=5.0):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    em = nodes.new('ShaderNodeEmission')
    em.inputs["Color"].default_value = color
    em.inputs["Strength"].default_value = strength
    out = nodes.new('ShaderNodeOutputMaterial')
    links.new(em.outputs[0], out.inputs[0])
    return mat

def assign_mat(obj_name, mat):
    obj = bpy.data.objects[obj_name]
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# ─── 체크포인트 ──────────────────────────────────────
def checkpoint(step_name):
    base = bpy.path.abspath("//checkpoints/")
    os.makedirs(base, exist_ok=True)
    path = os.path.join(base, f"{step_name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=path, copy=True)
    print(f"✅ checkpoint: {step_name}.blend")
    time.sleep(DELAY_SHORT)

# ─── 딜레이 래퍼 ─────────────────────────────────────
def pause(sec=DELAY_NORMAL):
    force_redraw()
    time.sleep(sec)
