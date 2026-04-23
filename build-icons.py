#!/usr/bin/env python3
"""
Build PWA icons for Goose Clicker.

Icon style: Apple squircle, soft peachy-yellow gradient, cute white goose.
Source: icon-1024.png (AI-generated, pre-composed).

Generates:
  - icon-192.png         (any purpose, 192x192)
  - icon-512.png         (any purpose, 512x512)
  - icon-maskable-512.png (maskable, peach gradient extended to full bleed)
  - apple-touch-icon.png  (180x180, opaque — iOS applies its own mask)
  - apple-touch-icon-{120,152,167,180}.png (Safari fallbacks)
  - favicon.png (32x32)
"""
from PIL import Image
from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE / "icon-1024.png"

# Peach gradient used for maskable full-bleed background.
# Matches the AI-generated squircle background tone.
PEACH_TOP = (74, 91, 168, 255)    # twilight indigo (top)
PEACH_BOT = (232, 155, 184, 255)  # warm pink (bottom)


def load_source(size: int) -> Image.Image:
    img = Image.open(SOURCE).convert("RGBA")
    if img.size != (size, size):
        img = img.resize((size, size), Image.LANCZOS)
    return img


def peach_bg(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), PEACH_TOP)
    px = img.load()
    for y in range(size):
        t = y / max(1, size - 1)
        r = int(PEACH_TOP[0] + (PEACH_BOT[0] - PEACH_TOP[0]) * t)
        g = int(PEACH_TOP[1] + (PEACH_BOT[1] - PEACH_TOP[1]) * t)
        b = int(PEACH_TOP[2] + (PEACH_BOT[2] - PEACH_TOP[2]) * t)
        for x in range(size):
            px[x, y] = (r, g, b, 255)
    return img


def build_standard(size: int, out: str, flatten: bool = False) -> None:
    """Standard icon: just resize the composed squircle source."""
    img = load_source(size)
    if flatten:
        bg = Image.new("RGB", img.size, PEACH_TOP[:3])
        bg.paste(img, (0, 0), img)
        img = bg
    img.save(HERE / out, "PNG", optimize=True)
    print(f"wrote {out} ({size}x{size})")


def build_maskable(size: int, out: str) -> None:
    """Maskable: peach gradient full-bleed, goose scaled into 60% safe zone."""
    bg = peach_bg(size)
    src = load_source(1024)
    # Scale source down so its visual content fits inside the 60% safe zone.
    inner = int(size * 0.60)
    src_small = src.resize((inner, inner), Image.LANCZOS)
    off = (size - inner) // 2
    bg.paste(src_small, (off, off), src_small)
    bg.save(HERE / out, "PNG", optimize=True)
    print(f"wrote {out} ({size}x{size})")


# Any-purpose icons
build_standard(192, "icon-192.png")
build_standard(512, "icon-512.png")

# Maskable
build_maskable(512, "icon-maskable-512.png")

# iOS home screen (opaque, iOS rounds corners itself)
for s in (120, 152, 167, 180):
    build_standard(s, f"apple-touch-icon-{s}.png", flatten=True)
build_standard(180, "apple-touch-icon.png", flatten=True)

# Favicon
build_standard(32, "favicon.png")

print("done")
