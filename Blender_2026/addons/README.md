# RPD Course Panel

`rpd_course_panel.py` is a Blender add-on draft for the Robot Product Design course.

## Install

1. Open Blender.
2. Go to `Edit > Preferences > Add-ons > Install...`.
3. Select [rpd_course_panel.py](/Users/ssongji/Developer/Workspace/RPD/Blender_2026/addons/rpd_course_panel.py).
4. Enable `RPD Course Panel`.

## Configure

1. In the add-on preferences, set `Course Site Folder` to:
   `/Users/ssongji/Developer/Workspace/RPD/course-site`
2. Open the 3D View sidebar with `N`.
3. Use the `RPD Course` tab to select a week and open the lesson page, tool library, shortcuts DB, and official references.

## Current Scope

- Shows weekly lesson metadata from `course-site/data/curriculum.json`
- Opens local `index.html`, `week.html`, `library.html`, and `shortcuts.html`
- Opens official Blender Manual, Python API, Developer Docs, and Projects
- Lists steps, assignment, docs, videos, and linked Show Me cards
- Opens a selected Show Me card directly with `week.html?week=...&showme=...`
- Saves per-student weekly progress to Blender's local config area as JSON

## Next Candidate Features

- Starter `.blend` launcher per week
- Assignment snapshot export
- Blender scene checklist sync
