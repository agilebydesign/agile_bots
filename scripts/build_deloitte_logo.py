"""
One-off helper: build circular high-res Deloitte header logo from a flat PNG.
Flood-fills from corners to drop outer white/checkerboard, then circular mask.
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

OUT_SIZE = 1024


def main() -> int:
    src = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else r"C:\Users\thoma\.cursor\projects\c-dev-agile-bots\assets\c__Users_thoma_AppData_Roaming_Cursor_User_workspaceStorage_6e426b0b4653f6fcd89a78e214dc3bfa_images_image-ad53aa59-803d-44e3-82f9-831a8f21eec6.png"
    )
    repo = Path(__file__).resolve().parents[1]
    out_path = repo / "src" / "panel" / "img" / "deloitte" / "company_icon.png"

    im = Image.open(src).convert("RGBA")
    a = np.array(im)
    h, w = a.shape[:2]
    rgb = a[:, :, :3].astype(np.float32)
    lum = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]

    def is_wall(i: int, j: int) -> bool:
        if i < 0 or i >= h or j < 0 or j >= w:
            return True
        return lum[i, j] < 55

    outside = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for ci, cj in ((0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)):
        if not outside[ci, cj] and not is_wall(ci, cj):
            outside[ci, cj] = True
            q.append((ci, cj))

    while q:
        i, j = q.popleft()
        for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            ni, nj = i + di, j + dj
            if ni < 0 or ni >= h or nj < 0 or nj >= w:
                continue
            if outside[ni, nj] or is_wall(ni, nj):
                continue
            if lum[ni, nj] < 200:
                continue
            outside[ni, nj] = True
            q.append((ni, nj))

    inside = ~outside
    ys, xs = np.where(inside)
    if ys.size == 0:
        print("No inside region found", file=sys.stderr)
        return 1

    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    side = max(bw, bh)
    # Square crop centered on content bbox
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    x_off = cx - side // 2
    y_off = cy - side // 2
    x_off = max(0, min(x_off, w - side))
    y_off = max(0, min(y_off, h - side))

    crop = a[y_off : y_off + side, x_off : x_off + side].copy()
    ch, cw = crop.shape[:2]
    assert ch == cw == side

    # Circle radius: max distance from center to any inside pixel (in crop coords)
    cy_, cx_ = ch // 2, cw // 2
    iy, ix = np.where(inside[y_off : y_off + side, x_off : x_off + side])
    if iy.size:
        dx = ix.astype(np.float64) - cx_
        dy = iy.astype(np.float64) - cy_
        r_max = float(np.sqrt(dx * dx + dy * dy).max())
    else:
        r_max = min(cx_, cy_) - 1

    # Tight circle + 0.5 px for AA
    r_mask = min(r_max + 0.5, min(cx_, cy_) - 0.25)
    yy, xx = np.ogrid[:ch, :cw]
    dist = np.sqrt((xx - cx_) ** 2 + (yy - cy_) ** 2)
    alpha_ring = np.clip(r_mask - dist + 0.5, 0, 1)
    crop = crop.astype(np.float64)
    crop[:, :, 3] *= alpha_ring
    crop = np.clip(np.round(crop), 0, 255).astype(np.uint8)

    out = Image.fromarray(crop, "RGBA")
    out = out.resize((OUT_SIZE, OUT_SIZE), Image.Resampling.LANCZOS)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.save(out_path, "PNG", optimize=True)
    print(f"Wrote {out_path} ({OUT_SIZE}x{OUT_SIZE})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
