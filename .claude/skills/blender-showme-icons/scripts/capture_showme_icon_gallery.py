import os
from pathlib import Path

import bpy


OUTPUT_PATH = Path(
    os.environ.get(
        "SHOWME_ICON_GALLERY_OUTPUT",
        "/tmp/blender-showme-icons-gallery.png",
    )
)

ICON_SPECS = [
    {"key": "edit-mode", "label": "Edit Mode", "icon_name": "ops.generic.select_box"},
    {"key": "edit-mode-tools", "label": "Tools", "icon_name": "ops.mesh.polybuild_hover"},
    {"key": "extrude", "label": "Extrude", "icon_name": "ops.mesh.extrude_region_move"},
    {"key": "loop-cut", "label": "Loop Cut", "icon_name": "ops.mesh.loopcut_slide"},
    {"key": "inset", "label": "Inset", "icon_name": "ops.mesh.inset"},
    {"key": "bevel-tool", "label": "Bevel", "icon_name": "ops.mesh.bevel"},
    {"key": "poly-circle", "label": "Poly Circle", "icon_name": "ops.mesh.spin"},
]

ICON_IDS = {}


def load_icons():
    icon_dir = Path(bpy.utils.system_resource("DATAFILES", path="icons"))
    for spec in ICON_SPECS:
        icon_path = icon_dir / f"{spec['icon_name']}.dat"
        ICON_IDS[spec["key"]] = bpy.app.icons.new_triangles_from_file(str(icon_path))


class WM_OT_showme_icon_gallery(bpy.types.Operator):
    bl_idname = "wm.showme_icon_gallery"
    bl_label = "Show Me Icon Gallery"

    def execute(self, _context):
        return {"FINISHED"}

    def invoke(self, context, _event):
        return context.window_manager.invoke_popup(self, width=1060)

    def draw(self, _context):
        layout = self.layout
        heading = layout.row()
        heading.alignment = "CENTER"
        heading.label(text="Show Me Blender Icons")
        layout.separator()

        grid = layout.grid_flow(columns=3, even_columns=True, even_rows=True, row_major=True)

        for spec in ICON_SPECS:
            box = grid.box()
            box_col = box.column(align=True)
            icon_row = box_col.row()
            icon_row.alignment = "CENTER"
            icon_row.template_icon(icon_value=ICON_IDS[spec["key"]], scale=6.4)
            box_col.separator()
            label_row = box_col.row()
            label_row.alignment = "CENTER"
            label_row.label(text=spec["label"])


def show_popup():
    bpy.context.preferences.view.show_splash = False
    bpy.context.preferences.view.ui_scale = 1.45
    bpy.ops.wm.showme_icon_gallery("INVOKE_DEFAULT")
    bpy.app.timers.register(capture, first_interval=0.9)
    return None


def capture():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.screen.screenshot(filepath=str(OUTPUT_PATH))
    bpy.app.timers.register(quit_blender, first_interval=0.2)
    return None


def quit_blender():
    bpy.ops.wm.quit_blender()
    return None


def register():
    bpy.utils.register_class(WM_OT_showme_icon_gallery)
    load_icons()
    bpy.app.timers.register(show_popup, first_interval=1.0)


register()
