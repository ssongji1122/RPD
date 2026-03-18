# RPD Course Panel GUI Smoke Checklist

Use this checklist in a regular Blender GUI session after enabling the add-on.

## Basic Launch

1. Open Blender and enable `RPD Course Panel`.
2. Open the 3D View sidebar with `N`.
3. Confirm the `RPD Course` tab is visible.
4. Verify the selected week can be changed with the `Week` control.

## Local Course Links

1. Click `Open Week`.
2. Confirm the browser opens `week.html?week=...`.
3. Click `Course Hub`.
4. Confirm the browser opens `index.html`.
5. Click `Tool Library`.
6. Confirm the browser opens `library.html`.
7. Click `Shortcuts`.
8. Confirm the browser opens `shortcuts.html`.

## Official Blender Links

1. Click `Manual`.
2. Confirm it opens the Blender Manual.
3. Click `Python API`.
4. Confirm it opens the Blender Python API page.
5. Click `Developer`.
6. Confirm it opens Blender Developer Documentation.
7. Click `Projects`.
8. Confirm it opens Blender Projects.

## Show Me Deep Links

1. Choose `Week 03`.
2. In `Show Me Cards`, click `이미지 레퍼런스 설정`.
3. Confirm the browser opens `week.html?week=3&showme=image-reference`.
4. Confirm the Show Me modal opens automatically on that page.

## Progress Save

1. Enter a `Student ID`.
2. Optionally enter a `Student Name`.
3. Set `Status`, `Completed Steps`, and `Week Note`.
4. Click `Save Progress`.
5. Click the folder button next to the progress actions.
6. Confirm the JSON file opens and contains the current student and week entry.
7. Change the fields in Blender.
8. Click `Load Progress`.
9. Confirm the saved values are restored.
