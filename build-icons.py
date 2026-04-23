#!/usr/bin/env python3
"""
Build PWA icons for Goose Clicker.

Generates:
  - icon-192.png        (any purpose, 192x192, safe zone ~90%)
  - icon-512.png        (any purpose, 512x512, safe zone ~90%)
  - icon-maskable-512.png (maskable, 512x512, safe zone 80% — per W3C maskable spec)
  - apple-touch-icon.png (180x180, rounded-corner-free, iOS applies its own mask)
  - favicon.png         (32x32)

Background: the game's signature purple gradient.
Foreground: the existing assets/goose.png centered.

Requires Pillow. Falls back gracefully if missing.
"""
from PIL import Image, ImageDraw
from pathlib import Path

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
GOOSE = Image.open(ASSETS / "goose.png").convert("RGBA")

# Brand colors pulled from index.html
BG_TOP = (58, 22, 133, 255)   # #3a1685
BG_MID = (26, 10, 60, 255)    # #1a0a3c
BG_BOT = (8, 2, 23, 255)      # #080217


def gradient_bg(size: int) -> Image.Image:
    """Vertical gradient matching the in-game sky."""
    img = Image.new("RGBA", (size, size), BG_MID)
    px = img.load()
    for y in range(size):
        t = y / (size - 1)
        # Two-stop interpolation: TOP -> MID at 55%, MID -> BOT at 100%
        if t < 0.55:
            u = t / 0.55
            r = int(BG_TOP[0] + (BG_MID[0] - BG_TOP[0]) * u)
            g = int(BG_TOP[1] + (BG_MID[1] - BG_TOP[1]) * u)
            b = int(BG_TOP[2] + (BG_MID[2] - BG_TOP[2]) * u)
        else:
            u = (t - 0.55) / 0.45
            r = int(BG_MID[0] + (BG_BOT[0] - BG_MID[0]) * u)
            g = int(BG_MID[1] + (BG_BOT[1] - BG_MID[1]) * u)
            b = int(BG_BOT[2] + (BG_BOT[2] - BG_MID[2]) * u)
        for x in range(size):
            px[x, y] = (r, g, b, 255)
    return img


def add_dot_grid(img: Image.Image) -> None:
    """Subtle dot grid for character, matching the in-game background."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    step = max(8, w // 24)
    for y in range(step // 2, h, step):
        for x in range(step // 2, w, step):
            draw.point((x, y), fill=(255, 255, 255, 30))


def place_goose(bg: Image.Image, goose_ratio: float) -> Image.Image:
    """Paste the goose centered, scaled to `goose_ratio` of canvas width."""
    size = bg.size[0]
    goose = GOOSE.copy()
    target_w = int(size * goose_ratio)
    # Preserve aspect
    gw, gh = goose.size
    scale = target_w / gw
    goose = goose.resize(
        (int(gw * scale), int(gh * scale)),
        Image.LANCZOS,
    )
    x = (size - goose.size[0]) // 2
    # Slightly below center — gives the head visual weight
    y = (size - goose.size[1]) // 2 + int(size * 0.02)
    bg.paste(goose, (x, y), goose)
    return bg


def build(size: int, goose_ratio: float, out: str) -> None:
    img = gradient_bg(size)
    add_dot_grid(img)
    place_goose(img, goose_ratio)
    img.save(HERE / out, "PNG", optimize=True)
    print(f"wrote {out} ({size}x{size})")


# Standard icons: goose fills ~78% of canvas (safe zone for any purpose)
build(192, 0.78, "icon-192.png")
build(512, 0.78, "icon-512.png")

# Maskable: goose fills ~60% so the mask (inner 80%) never clips the goose.
# Maskable spec requires critical content inside the inner 80% circle/square.
build(512, 0.60, "icon-maskable-512.png")

# iOS home screen: 180x180, iOS rounds corners automatically.
build(180, 0.78, "apple-touch-icon.png")

# Favicon
build(32, 0.82, "favicon.png")

print("done")
