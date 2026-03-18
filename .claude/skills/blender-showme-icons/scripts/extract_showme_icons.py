#!/usr/bin/env python3
import argparse
from collections import deque
from pathlib import Path

from PIL import Image


SPECS = {
    "edit-mode": {
        "box": (620, 720, 1080, 1100),
        "mode": "edit",
        "trim": (0, 0, None, None),
    },
    "edit-mode-tools": {
        "box": (1320, 700, 1810, 1120),
        "mode": "mint",
        "trim": (0, 0, None, 330),
    },
    "extrude": {
        "box": (1990, 690, 2550, 1120),
        "mode": "mint",
        "trim": (0, 0, None, None),
    },
    "loop-cut": {
        "box": (700, 1080, 1140, 1450),
        "mode": "mint",
        "trim": (0, 34, None, None),
    },
    "inset": {
        "box": (1300, 1080, 1690, 1470),
        "mode": "mint",
        "trim": (0, 36, None, None),
    },
    "bevel-tool": {
        "box": (2140, 1070, 2520, 1470),
        "mode": "mint",
        "trim": (28, 48, None, None),
    },
    "poly-circle": {
        "box": (700, 1410, 1180, 1790),
        "mode": "mint",
        "trim": (18, 60, None, 352),
    },
}


def is_icon_pixel(pixel, mode):
    r, g, b, _a = pixel
    if mode == "edit":
        orange = r > 215 and g > 150 and b < 130
        white = r > 215 and g > 215 and b > 215
        return orange or white
    mint = g > 190 and b > 130 and r < 180
    white = r > 215 and g > 215 and b > 215
    orange = r > 215 and g > 150 and b < 130
    return mint or white or orange


def dilate(mask, width, height, iterations=2):
    for _ in range(iterations):
        new = [row[:] for row in mask]
        for y in range(height):
            for x in range(width):
                if not mask[y][x]:
                    continue
                for nx in range(max(0, x - 1), min(width, x + 2)):
                    for ny in range(max(0, y - 1), min(height, y + 2)):
                        new[ny][nx] = True
        mask = new
    return mask


def collect_large_components(mask, width, height):
    seen = set()
    keep = []
    for y in range(height):
        for x in range(width):
            if not mask[y][x] or (x, y) in seen:
                continue
            queue = deque([(x, y)])
            seen.add((x, y))
            points = []
            min_x = max_x = x
            min_y = max_y = y
            while queue:
                cx, cy = queue.popleft()
                points.append((cx, cy))
                min_x = min(min_x, cx)
                max_x = max(max_x, cx)
                min_y = min(min_y, cy)
                max_y = max(max_y, cy)
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < width and 0 <= ny < height and mask[ny][nx] and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        queue.append((nx, ny))
            area = len(points)
            comp_width = max_x - min_x + 1
            comp_height = max_y - min_y + 1
            center_y = (min_y + max_y) / 2
            if area > 120 and min(comp_width, comp_height) >= 10 and center_y < height * 0.9:
                keep.append(points)
    return keep


def masked_crop(image, mode):
    width, height = image.size
    mask = [[False] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if is_icon_pixel(image.getpixel((x, y)), mode):
                mask[y][x] = True
    mask = dilate(mask, width, height)
    keep = collect_large_components(mask, width, height)
    if not keep:
        return image

    final_mask = [[False] * width for _ in range(height)]
    for points in keep:
        for x, y in points:
            final_mask[y][x] = True

    coords = [(x, y) for y in range(height) for x in range(width) if final_mask[y][x]]
    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]
    left = max(min(xs) - 8, 0)
    top = max(min(ys) - 8, 0)
    right = min(max(xs) + 9, width)
    bottom = min(max(ys) + 9, height)

    output = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
    for y in range(top, bottom):
        for x in range(left, right):
            if final_mask[y][x]:
                output.putpixel((x - left, y - top), image.getpixel((x, y)))
    return output


def apply_trim(image, trim):
    left, top, right, bottom = trim
    right = image.width if right is None else right
    bottom = image.height if bottom is None else bottom
    return image.crop((left, top, right, bottom))


def extract_icons(gallery_path, output_dir):
    gallery = Image.open(gallery_path).convert("RGBA")
    output_dir.mkdir(parents=True, exist_ok=True)
    for key, spec in SPECS.items():
        crop = gallery.crop(spec["box"])
        icon = masked_crop(crop, spec["mode"])
        icon = apply_trim(icon, spec["trim"])
        icon.save(output_dir / f"{key}.png")


def main():
    parser = argparse.ArgumentParser(description="Extract Blender Show Me icons from a gallery screenshot.")
    parser.add_argument("--gallery", required=True, help="Absolute path to the gallery screenshot PNG.")
    parser.add_argument("--output-dir", required=True, help="Directory for extracted icon PNGs.")
    args = parser.parse_args()

    extract_icons(Path(args.gallery), Path(args.output_dir))


if __name__ == "__main__":
    main()
