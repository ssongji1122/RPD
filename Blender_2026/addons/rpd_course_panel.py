bl_info = {
    "name": "RPD Course Panel",
    "author": "OpenAI Codex",
    "version": (0, 3, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > RPD Course",
    "description": "Open weekly Robot Product Design lesson pages and reference links inside Blender's sidebar workflow.",
    "category": "3D View",
}

import json
import re
import textwrap
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty, PointerProperty
from bpy.types import AddonPreferences, Operator, Panel, PropertyGroup


ADDON_MODULE = __package__ or __name__
DEFAULT_SITE_URL = "http://127.0.0.1:8000/course-site"
_CACHE = {"path": None, "mtime": None, "data": []}
_SHOWME_CACHE = {"path": None, "mtime": None, "data": {}}
OFFICIAL_DOCS = {
    "manual": "https://docs.blender.org/manual/en/latest/",
    "api": "https://docs.blender.org/api/current/",
    "developer": "https://developer.blender.org/docs/",
    "projects": "https://projects.blender.org/",
}


def detect_course_site_root():
    here = Path(__file__).resolve()
    candidates = []

    for parent in [here] + list(here.parents):
        candidates.append(parent / "course-site")

    candidates.append(Path.home() / "Developer" / "Workspace" / "RPD" / "course-site")

    for candidate in candidates:
        if (candidate / "data" / "curriculum.json").exists():
            return str(candidate)

    return ""


def get_preferences(context):
    addon = context.preferences.addons.get(ADDON_MODULE)
    return addon.preferences if addon else None


def get_scene_settings(scene):
    return getattr(scene, "rpd_course_settings", None)


def normalize_base_url(value):
    url = (value or "").strip()
    return url[:-1] if url.endswith("/") else url


def build_page_url(context, filename, query=None):
    root = get_course_site_root(context)
    if root:
        return build_file_url(root / filename, query)

    prefs = get_preferences(context)
    base = normalize_base_url(prefs.site_base_url if prefs else "")
    if not base:
        return ""
    return "{0}/{1}{2}".format(base, filename, "?" + query if query else "")


def get_course_site_root(context):
    prefs = get_preferences(context)
    if not prefs or not prefs.course_site_root:
        return None
    root = Path(bpy.path.abspath(prefs.course_site_root)).expanduser()
    return root if (root / "data" / "curriculum.json").exists() else None


def get_curriculum_path(context):
    root = get_course_site_root(context)
    if root:
        return root / "data" / "curriculum.json"
    return None


def load_curriculum_data(context):
    path = get_curriculum_path(context)
    if not path or not path.exists():
        _CACHE.update({"path": None, "mtime": None, "data": []})
        return []

    mtime = path.stat().st_mtime
    if _CACHE["path"] == str(path) and _CACHE["mtime"] == mtime:
        return _CACHE["data"]

    try:
        data = json.loads(path.read_text(encoding="utf8"))
    except Exception:
        data = []

    _CACHE.update({"path": str(path), "mtime": mtime, "data": data})
    return data


def get_week_data(context):
    settings = get_scene_settings(context.scene)
    weeks = load_curriculum_data(context)
    if not settings or not weeks:
        return None

    for week in weeks:
        if int(week.get("week", 0)) == int(settings.week_number):
            return week
    return None


def build_file_url(path, query=None):
    url = path.resolve().as_uri()
    if query:
        url += "?" + query
    return url


def build_index_url(context):
    return build_page_url(context, "index.html")


def build_week_url(context, week_number):
    return build_page_url(context, "week.html", urlencode({"week": int(week_number)}))


def build_library_url(context):
    return build_page_url(context, "library.html")


def build_shortcuts_url(context):
    return build_page_url(context, "shortcuts.html")


def build_showme_url(context, widget_id, week_number):
    query = urlencode({"week": int(week_number), "showme": widget_id})
    return build_page_url(context, "week.html", query)


def open_external_url(url):
    if not url:
        return False
    try:
        return webbrowser.open(url)
    except Exception:
        return False


def collect_showme_ids(week):
    ids = []
    seen = set()

    for step in week.get("steps", []):
        showme = step.get("showme")
        if showme:
            items = showme if isinstance(showme, list) else [showme]
            for item in items:
                if item and item not in seen:
                    seen.add(item)
                    ids.append(item)

        for widget in step.get("widgets", []):
            widget_id = widget.get("id") if isinstance(widget, dict) else None
            if widget_id and widget_id not in seen:
                seen.add(widget_id)
                ids.append(widget_id)

    return ids


def get_showme_registry_path(context):
    root = get_course_site_root(context)
    if not root:
        return None
    path = root / "assets" / "showme" / "_registry.js"
    return path if path.exists() else None


def load_showme_registry(context):
    path = get_showme_registry_path(context)
    if not path or not path.exists():
        _SHOWME_CACHE.update({"path": None, "mtime": None, "data": {}})
        return {}

    mtime = path.stat().st_mtime
    if _SHOWME_CACHE["path"] == str(path) and _SHOWME_CACHE["mtime"] == mtime:
        return _SHOWME_CACHE["data"]

    try:
        source = path.read_text(encoding="utf8")
    except Exception:
        source = ""

    data = {}
    pattern = re.compile(
        r'"(?P<id>[^"]+)":\s*\{\s*label:\s*"(?P<label>[^"]+)"\s*,\s*icon:\s*"(?P<icon>[^"]+)"',
        re.MULTILINE,
    )
    for match in pattern.finditer(source):
        data[match.group("id")] = {
            "label": match.group("label"),
            "icon": match.group("icon"),
        }

    _SHOWME_CACHE.update({"path": str(path), "mtime": mtime, "data": data})
    return data


def format_showme_label(widget_id):
    return " ".join(part.capitalize() for part in str(widget_id).split("-"))


def get_showme_label(context, widget_id):
    registry = load_showme_registry(context)
    meta = registry.get(widget_id) or {}
    return meta.get("label") or format_showme_label(widget_id)


def draw_wrapped_label(layout, text, icon="NONE", width=54):
    chunks = textwrap.wrap(text or "", width=width) or [text or ""]
    for index, line in enumerate(chunks):
        layout.label(text=line, icon=icon if index == 0 else "NONE")


def get_progress_store_path():
    config_root = bpy.utils.user_resource("CONFIG") or str(Path.home())
    return Path(config_root) / "rpd_course" / "student_progress.json"


def ensure_progress_store_parent():
    path = get_progress_store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_progress_store():
    path = get_progress_store_path()
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf8"))
    except Exception:
        return {}


def write_progress_store(data):
    path = ensure_progress_store_parent()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf8")
    return path


def normalize_student_id(value):
    return (value or "").strip()


def get_week_step_count(week):
    return len((week or {}).get("steps", []))


def get_saved_progress_entry(context):
    settings = get_scene_settings(context.scene)
    week = get_week_data(context)
    student_id = normalize_student_id(settings.student_id if settings else "")
    if not student_id or not week:
        return None

    store = load_progress_store()
    student = store.get(student_id) or {}
    weeks = student.get("weeks") or {}
    return weeks.get(str(int(week.get("week", 0))))


def build_progress_payload(context):
    settings = get_scene_settings(context.scene)
    week = get_week_data(context)
    student_id = normalize_student_id(settings.student_id if settings else "")
    if not student_id or not week or not settings:
        return None

    total_steps = get_week_step_count(week)
    completed_steps = max(0, min(int(settings.completed_steps), total_steps))
    return {
        "student_name": (settings.student_name or "").strip(),
        "week": int(week.get("week", 0)),
        "week_title": week.get("title", ""),
        "status": settings.progress_status,
        "completed_steps": completed_steps,
        "total_steps": total_steps,
        "note": (settings.week_note or "").strip(),
        "blend_file": bpy.data.filepath or "",
        "lesson_url": build_week_url(context, settings.week_number),
        "updated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    }


class RPDCoursePreferences(AddonPreferences):
    bl_idname = ADDON_MODULE

    course_site_root: StringProperty(
        name="Course Site Folder",
        subtype="DIR_PATH",
        default=detect_course_site_root(),
        description="Folder that contains index.html, week.html, and data/curriculum.json",
    )
    site_base_url: StringProperty(
        name="Fallback Site URL",
        default=DEFAULT_SITE_URL,
        description="Optional browser URL to use when the local course-site folder is unavailable",
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Robot Product Design", icon="BOOKMARKS")
        layout.prop(self, "course_site_root")
        layout.prop(self, "site_base_url")
        layout.label(text="Install this add-on, then open the RPD Course tab in the 3D View sidebar.", icon="INFO")


class RPDCourseSceneSettings(PropertyGroup):
    week_number: IntProperty(
        name="Week",
        min=1,
        max=15,
        default=2,
        description="Selected lesson week",
    )
    show_steps: BoolProperty(
        name="Show Steps",
        default=True,
    )
    show_resources: BoolProperty(
        name="Show Resources",
        default=True,
    )
    show_assignment: BoolProperty(
        name="Show Assignment",
        default=True,
    )
    show_showme: BoolProperty(
        name="Show Show Me",
        default=True,
    )
    student_id: StringProperty(
        name="Student ID",
        default="",
        description="Identifier used for saving course progress",
    )
    student_name: StringProperty(
        name="Student Name",
        default="",
        description="Optional display name saved alongside the student ID",
    )
    progress_status: EnumProperty(
        name="Status",
        items=[
            ("not_started", "Not Started", "No work has been recorded yet"),
            ("in_progress", "In Progress", "Work is underway"),
            ("review", "Needs Review", "Ready for feedback or QA"),
            ("done", "Done", "Week work is complete"),
        ],
        default="not_started",
    )
    completed_steps: IntProperty(
        name="Completed Steps",
        min=0,
        max=30,
        default=0,
        description="Manual progress count for the current week",
    )
    week_note: StringProperty(
        name="Week Note",
        default="",
        description="Short note saved with the current week's progress",
    )


class RPD_OT_OpenURL(Operator):
    bl_idname = "rpd_course.open_url"
    bl_label = "Open URL"
    bl_description = "Open the target lesson page or reference link in your browser"

    url: StringProperty(name="URL")

    def execute(self, context):
        if not self.url:
            self.report({"ERROR"}, "No URL is configured.")
            return {"CANCELLED"}

        if not open_external_url(self.url):
            self.report({"ERROR"}, "Unable to open the URL.")
            return {"CANCELLED"}

        return {"FINISHED"}


class RPD_OT_ReloadCurriculum(Operator):
    bl_idname = "rpd_course.reload_curriculum"
    bl_label = "Reload Curriculum"
    bl_description = "Reload curriculum.json from the configured course-site folder"

    def execute(self, context):
        _CACHE.update({"path": None, "mtime": None, "data": []})
        count = len(load_curriculum_data(context))
        self.report({"INFO"}, "Reloaded {0} week entries.".format(count))
        return {"FINISHED"}


class RPD_OT_SaveProgress(Operator):
    bl_idname = "rpd_course.save_progress"
    bl_label = "Save Progress"
    bl_description = "Save student progress for the selected week into a local JSON file"

    def execute(self, context):
        settings = get_scene_settings(context.scene)
        payload = build_progress_payload(context)
        student_id = normalize_student_id(settings.student_id if settings else "")

        if not student_id:
            self.report({"ERROR"}, "Enter a Student ID before saving progress.")
            return {"CANCELLED"}

        if not payload:
            self.report({"ERROR"}, "No week is selected for saving.")
            return {"CANCELLED"}

        store = load_progress_store()
        student_entry = store.setdefault(student_id, {"student_name": "", "weeks": {}})
        student_entry["student_name"] = payload["student_name"]
        student_entry["updated_at"] = payload["updated_at"]
        student_entry.setdefault("weeks", {})[str(payload["week"])] = payload
        path = write_progress_store(store)

        settings.completed_steps = payload["completed_steps"]
        self.report({"INFO"}, "Saved progress to {0}".format(path))
        return {"FINISHED"}


class RPD_OT_LoadProgress(Operator):
    bl_idname = "rpd_course.load_progress"
    bl_label = "Load Progress"
    bl_description = "Load saved student progress for the selected week"

    def execute(self, context):
        settings = get_scene_settings(context.scene)
        week = get_week_data(context)
        student_id = normalize_student_id(settings.student_id if settings else "")

        if not student_id:
            self.report({"ERROR"}, "Enter a Student ID before loading progress.")
            return {"CANCELLED"}

        if not week:
            self.report({"ERROR"}, "No week is selected.")
            return {"CANCELLED"}

        entry = get_saved_progress_entry(context)
        if not entry:
            self.report({"WARNING"}, "No saved progress found for this student and week.")
            return {"CANCELLED"}

        settings.student_name = entry.get("student_name", "")
        settings.progress_status = entry.get("status", "not_started")
        settings.completed_steps = int(entry.get("completed_steps", 0))
        settings.week_note = entry.get("note", "")
        self.report({"INFO"}, "Loaded saved progress for Week {0:02d}.".format(int(week.get("week", 0))))
        return {"FINISHED"}


class RPD_OT_OpenProgressStore(Operator):
    bl_idname = "rpd_course.open_progress_store"
    bl_label = "Open Progress File"
    bl_description = "Open the local JSON file that stores student progress"

    def execute(self, context):
        path = ensure_progress_store_parent()
        if not path.exists():
            path.write_text("{}\n", encoding="utf8")

        if not open_external_url(path.as_uri()):
            self.report({"ERROR"}, "Unable to open the progress file.")
            return {"CANCELLED"}

        return {"FINISHED"}


class RPD_PT_CourseSidebar(Panel):
    bl_label = "RPD Course"
    bl_idname = "RPD_PT_course_sidebar"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RPD Course"

    def draw(self, context):
        layout = self.layout
        prefs = get_preferences(context)
        settings = get_scene_settings(context.scene)
        week = get_week_data(context)
        weeks = load_curriculum_data(context)
        showme_ids = collect_showme_ids(week) if week else []

        header = layout.box()
        header.label(text="Robot Product Design", icon="BOOKMARKS")
        header.label(text="In-Blender lesson launcher", icon="INFO")

        nav = layout.box()
        nav_row = nav.row(align=True)
        nav_row.prop(settings, "week_number")
        nav_row.operator("rpd_course.reload_curriculum", text="", icon="FILE_REFRESH")

        quick = nav.row(align=True)
        open_week = quick.operator("rpd_course.open_url", text="Open Week", icon="URL")
        open_week.url = build_week_url(context, settings.week_number)
        open_index = quick.operator("rpd_course.open_url", text="Course Hub", icon="HOME")
        open_index.url = build_index_url(context)

        utilities = nav.row(align=True)
        open_library = utilities.operator("rpd_course.open_url", text="Tool Library", icon="ASSET_MANAGER")
        open_library.url = build_library_url(context)
        open_shortcuts = utilities.operator("rpd_course.open_url", text="Shortcuts", icon="EVENT_A")
        open_shortcuts.url = build_shortcuts_url(context)

        official = nav.box()
        official.label(text="Official Blender Links", icon="URL")
        official_row = official.row(align=True)
        manual = official_row.operator("rpd_course.open_url", text="Manual", icon="HELP")
        manual.url = OFFICIAL_DOCS["manual"]
        api = official_row.operator("rpd_course.open_url", text="Python API", icon="SCRIPT")
        api.url = OFFICIAL_DOCS["api"]
        official_row = official.row(align=True)
        developer = official_row.operator("rpd_course.open_url", text="Developer", icon="FILE_TEXT")
        developer.url = OFFICIAL_DOCS["developer"]
        projects = official_row.operator("rpd_course.open_url", text="Projects", icon="OUTLINER_COLLECTION")
        projects.url = OFFICIAL_DOCS["projects"]

        if not get_course_site_root(context) and not normalize_base_url(prefs.site_base_url if prefs else ""):
            warn = layout.box()
            warn.label(text="Set a course-site folder or fallback URL in the add-on preferences.", icon="ERROR")
            return

        if not weeks:
            empty = layout.box()
            empty.label(text="No curriculum data found.", icon="ERROR")
            return

        if not week:
            missing = layout.box()
            missing.label(text="The selected week is missing from curriculum.json.", icon="ERROR")
            return

        summary = layout.box()
        summary.label(text="Week {0:02d} · {1}".format(int(week.get("week", 0)), week.get("title", "Untitled")), icon="BOOKMARKS")
        draw_wrapped_label(summary, week.get("subtitle", ""))
        summary.label(text="{0} steps · {1} docs · {2} videos".format(
            len(week.get("steps", [])),
            len(week.get("docs", [])),
            len(week.get("videos", [])),
        ), icon="INFO")

        progress_entry = get_saved_progress_entry(context)
        progress_box = layout.box()
        progress_box.label(text="Student Progress", icon="CHECKMARK")
        progress_box.prop(settings, "student_id")
        progress_box.prop(settings, "student_name")
        progress_box.prop(settings, "progress_status", text="Status")
        steps_row = progress_box.row(align=True)
        steps_row.prop(settings, "completed_steps", text="Completed Steps")
        steps_row.label(text="/ {0}".format(get_week_step_count(week)))
        progress_box.prop(settings, "week_note")
        progress_actions = progress_box.row(align=True)
        progress_actions.operator("rpd_course.save_progress", icon="CHECKMARK")
        progress_actions.operator("rpd_course.load_progress", icon="IMPORT")
        progress_actions.operator("rpd_course.open_progress_store", text="", icon="FILE_FOLDER")
        if progress_entry:
            draw_wrapped_label(
                progress_box,
                "Saved: {0} · {1}/{2} steps".format(
                    progress_entry.get("status", "not_started"),
                    int(progress_entry.get("completed_steps", 0)),
                    int(progress_entry.get("total_steps", get_week_step_count(week))),
                ),
                icon="INFO",
                width=48,
            )
            if progress_entry.get("updated_at"):
                draw_wrapped_label(progress_box, "Updated at " + progress_entry["updated_at"], width=48)
            if progress_entry.get("blend_file"):
                draw_wrapped_label(progress_box, "Blend file: " + progress_entry["blend_file"], width=48)

        if settings.show_steps:
            steps_box = layout.box()
            steps_header = steps_box.row()
            steps_header.prop(settings, "show_steps", text="Practice Flow", icon="TRIA_DOWN", emboss=False)
            for index, step in enumerate(week.get("steps", []), start=1):
                draw_wrapped_label(
                    steps_box,
                    "{0}. {1}".format(index, step.get("title", "Untitled step")),
                    icon="DOT",
                    width=48,
                )

            if showme_ids:
                draw_wrapped_label(
                    steps_box,
                    "Show Me cards: " + ", ".join(showme_ids[:6]) + (" ..." if len(showme_ids) > 6 else ""),
                    icon="SHADERFX",
                    width=48,
                )
        else:
            collapsed = layout.box()
            collapsed.prop(settings, "show_steps", text="Practice Flow", icon="TRIA_RIGHT", emboss=False)

        if showme_ids and settings.show_showme:
            showme_box = layout.box()
            showme_header = showme_box.row()
            showme_header.prop(settings, "show_showme", text="Show Me Cards", icon="TRIA_DOWN", emboss=False)
            for widget_id in showme_ids:
                op = showme_box.operator("rpd_course.open_url", text=get_showme_label(context, widget_id), icon="SHADERFX")
                op.url = build_showme_url(context, widget_id, settings.week_number)
        elif showme_ids:
            collapsed = layout.box()
            collapsed.prop(settings, "show_showme", text="Show Me Cards", icon="TRIA_RIGHT", emboss=False)

        if settings.show_resources:
            resources_box = layout.box()
            resources_header = resources_box.row()
            resources_header.prop(settings, "show_resources", text="Resources", icon="TRIA_DOWN", emboss=False)

            if week.get("docs"):
                resources_box.label(text="Official docs", icon="FILE_TEXT")
                for doc in week["docs"][:4]:
                    op = resources_box.operator("rpd_course.open_url", text=doc.get("title", "Documentation"), icon="URL")
                    op.url = doc.get("url", "")

            if week.get("videos"):
                resources_box.label(text="Videos", icon="PLAY")
                for video in week["videos"][:3]:
                    op = resources_box.operator("rpd_course.open_url", text=video.get("title", "Video"), icon="URL")
                    op.url = video.get("url", "")
        else:
            collapsed = layout.box()
            collapsed.prop(settings, "show_resources", text="Resources", icon="TRIA_RIGHT", emboss=False)

        if settings.show_assignment:
            assignment = week.get("assignment") or {}
            assignment_box = layout.box()
            assignment_header = assignment_box.row()
            assignment_header.prop(settings, "show_assignment", text="Assignment", icon="TRIA_DOWN", emboss=False)
            if assignment:
                draw_wrapped_label(assignment_box, assignment.get("title", "Untitled assignment"), icon="CHECKMARK", width=48)
                if assignment.get("description"):
                    draw_wrapped_label(assignment_box, assignment["description"], width=50)
                for item in assignment.get("checklist", [])[:6]:
                    draw_wrapped_label(assignment_box, item, icon="CHECKBOX_DEHLT", width=48)
        else:
            collapsed = layout.box()
            collapsed.prop(settings, "show_assignment", text="Assignment", icon="TRIA_RIGHT", emboss=False)

        footer = layout.box()
        footer.label(text="Configured source", icon="PREFERENCES")
        if get_course_site_root(context):
            draw_wrapped_label(footer, str(get_course_site_root(context)), width=50)
        else:
            draw_wrapped_label(footer, normalize_base_url(prefs.site_base_url if prefs else ""), width=50)


CLASSES = (
    RPDCoursePreferences,
    RPDCourseSceneSettings,
    RPD_OT_OpenURL,
    RPD_OT_ReloadCurriculum,
    RPD_OT_SaveProgress,
    RPD_OT_LoadProgress,
    RPD_OT_OpenProgressStore,
    RPD_PT_CourseSidebar,
)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.rpd_course_settings = PointerProperty(type=RPDCourseSceneSettings)


def unregister():
    del bpy.types.Scene.rpd_course_settings
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
