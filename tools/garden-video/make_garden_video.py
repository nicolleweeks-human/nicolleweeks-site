#!/usr/bin/env python3
"""
make_garden_video.py
--------------------
Build a short, polished slideshow video featuring a garden from a set of photos.

Features:
  - Auto-corrects photo orientation from EXIF (some phone photos are rotated).
  - Normalizes every photo to a consistent 16:9 canvas with a tasteful "cover" crop.
  - Gentle Ken Burns effect (slow zoom + pan), alternating in/out per photo.
  - Smooth crossfade transitions between photos, fade-in at start, fade-out at end.
  - Title card and closing card with a clean, readable font + soft drop shadow.
  - Optional per-photo captions in a lower corner (toggle below).
  - Optional background music: drop a `music.mp3` next to this script and it is
    mixed in automatically (trimmed + faded). No music file -> silent video, no error.

Output: garden.mp4 (H.264, configurable fps/resolution).

Run:
    python make_garden_video.py
"""

from __future__ import annotations

import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

from moviepy import (
    VideoClip,
    ImageClip,
    ColorClip,
    CompositeVideoClip,
    AudioFileClip,
    vfx,
    afx,
)

# ---------------------------------------------------------------------------
# CONFIG  -- tweak these freely
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(HERE, "images")
MUSIC_FILE = os.path.join(HERE, "music.mp3")        # optional; ignored if missing
OUTPUT_FILE = os.path.join(HERE, "garden.mp4")

WIDTH, HEIGHT = 1920, 1080                            # 16:9 output canvas
FPS = 30

PHOTO_DURATION = 4.0                                  # seconds each photo is on screen
TRANSITION = 0.8                                      # crossfade length (seconds)
TITLE_DURATION = 3.0                                  # opening card
CLOSING_DURATION = 3.0                                # closing card
INTRO_FADE = 1.0                                      # fade-in from black at very start
OUTRO_FADE = 1.2                                      # fade-out to black at very end

KEN_BURNS_ZOOM = 1.18                                 # max magnification (1.0 = none)

SHOW_CAPTIONS = True                                  # per-photo lower-corner labels

TITLE_TEXT = "My Garden"
TITLE_SUBTITLE = "Summer 2026"
CLOSING_TEXT = "Thanks for visiting"
CLOSING_SUBTITLE = "❀"                           # floral heart ornament

# Photos in display order: (filename, caption)
PHOTOS = [
    ("01_urn_impatiens.jpeg",          "Stone urn — impatiens & dracaena"),
    ("02_strawberry_pot_petunias.jpeg", "Petunias in the strawberry pot"),
    ("05_weigela.jpeg",                "Weigela in full bloom"),
    ("03_rose_campion.jpeg",           "Rose campion along the path"),
    ("04_garden_bed_path.jpeg",        "The silver border"),
]

# Color palette
BG_COLOR = (18, 24, 18)                               # deep garden green/black
TEXT_COLOR = (245, 245, 240)
SUBTITLE_COLOR = (210, 225, 205)
CAPTION_BG = (0, 0, 0, 110)                           # translucent caption pill


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/mnt/skills/examples/canvas-design/canvas-fonts/CrimsonPro-Bold.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    # Last resort: PIL's built-in bitmap font (won't scale, but never crashes).
    print("  ! No TrueType font found; falling back to default bitmap font.")
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------
def load_oriented(path: str) -> Image.Image:
    """Open an image and apply EXIF orientation so it is always upright."""
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)      # honor the camera's rotation tag
    return img.convert("RGB")


def cover_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Scale + center-crop so the image exactly fills target_w x target_h."""
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = round(src_w * scale), round(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def ease_in_out(p: float) -> float:
    """Smoothstep easing for gentle starts/stops."""
    return p * p * (3 - 2 * p)


def draw_caption(frame: Image.Image, text: str) -> None:
    """Draw a translucent caption pill in the lower-left corner (in place)."""
    if not text:
        return
    draw = ImageDraw.Draw(frame, "RGBA")
    font = load_font(40)
    pad_x, pad_y = 26, 16
    margin = 56

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    box_w, box_h = tw + 2 * pad_x, th + 2 * pad_y
    x0, y0 = margin, HEIGHT - margin - box_h

    draw.rounded_rectangle(
        [x0, y0, x0 + box_w, y0 + box_h], radius=box_h // 2, fill=CAPTION_BG
    )
    tx = x0 + pad_x - bbox[0]
    ty = y0 + pad_y - bbox[1]
    # soft shadow then text
    draw.text((tx + 2, ty + 2), text, font=font, fill=(0, 0, 0, 160))
    draw.text((tx, ty), text, font=font, fill=TEXT_COLOR)


# ---------------------------------------------------------------------------
# Ken Burns clip
# ---------------------------------------------------------------------------
def make_ken_burns_clip(path: str, caption: str, zoom_in: bool) -> VideoClip:
    """Return a VideoClip that slowly zooms/pans across one photo."""
    # Base canvas is larger than the output so we have room to zoom and pan.
    base_w = round(WIDTH * KEN_BURNS_ZOOM)
    base_h = round(HEIGHT * KEN_BURNS_ZOOM)
    base = cover_crop(load_oriented(path), base_w, base_h)

    # Diagonal pan endpoints (centers), kept gentle and within bounds after clamp.
    cx0, cy0 = base_w * 0.45, base_h * 0.45
    cx1, cy1 = base_w * 0.55, base_h * 0.55
    if not zoom_in:  # reverse the pan direction on alternate slides
        cx0, cx1 = cx1, cx0
        cy0, cy1 = cy1, cy0

    aspect = HEIGHT / WIDTH

    def frame_function(t: float) -> np.ndarray:
        p = ease_in_out(min(t / PHOTO_DURATION, 1.0))
        # Crop width travels between full base (wide) and output width (tight).
        if zoom_in:
            cw = base_w + (WIDTH - base_w) * p          # base_w -> WIDTH (zoom in)
        else:
            cw = WIDTH + (base_w - WIDTH) * p            # WIDTH -> base_w (zoom out)
        ch = cw * aspect

        cx = cx0 + (cx1 - cx0) * p
        cy = cy0 + (cy1 - cy0) * p
        left = min(max(cx - cw / 2, 0), base_w - cw)
        top = min(max(cy - ch / 2, 0), base_h - ch)

        crop = base.crop((round(left), round(top),
                          round(left + cw), round(top + ch)))
        crop = crop.resize((WIDTH, HEIGHT), Image.LANCZOS)
        if SHOW_CAPTIONS:
            draw_caption(crop, caption)
        return np.asarray(crop)

    return VideoClip(frame_function=frame_function, duration=PHOTO_DURATION)


# ---------------------------------------------------------------------------
# Title / closing cards
# ---------------------------------------------------------------------------
def make_card(title: str, subtitle: str, duration: float) -> ImageClip:
    """Render a centered title card (with soft drop shadow) as a still clip."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    title_font = load_font(120)
    sub_font = load_font(54)

    def centered(text, font, y, color):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        x = (WIDTH - tw) // 2 - bbox[0]
        draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0))      # shadow
        draw.text((x, y), text, font=font, fill=color)

    centered(title, title_font, HEIGHT // 2 - 110, TEXT_COLOR)
    if subtitle:
        centered(subtitle, sub_font, HEIGHT // 2 + 50, SUBTITLE_COLOR)

    return ImageClip(np.asarray(img), duration=duration)


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------
def build() -> None:
    missing = [f for f, _ in PHOTOS if not os.path.exists(os.path.join(IMAGES_DIR, f))]
    if missing:
        sys.exit(f"ERROR: missing image(s) in {IMAGES_DIR}: {missing}")

    print("Building clips...")
    clips = [make_card(TITLE_TEXT, TITLE_SUBTITLE, TITLE_DURATION)]
    for i, (fname, caption) in enumerate(PHOTOS):
        print(f"  - photo {i + 1}/{len(PHOTOS)}: {fname}")
        clips.append(
            make_ken_burns_clip(
                os.path.join(IMAGES_DIR, fname), caption, zoom_in=(i % 2 == 0)
            )
        )
    clips.append(make_card(CLOSING_TEXT, CLOSING_SUBTITLE, CLOSING_DURATION))

    # Lay clips on a timeline, overlapping by TRANSITION for crossfades.
    timeline, starts = [], []
    prev_end = 0.0
    for i, c in enumerate(clips):
        start = 0.0 if i == 0 else prev_end - TRANSITION
        if i > 0:
            c = c.with_effects([vfx.CrossFadeIn(TRANSITION)])
        c = c.with_start(start)
        timeline.append(c)
        starts.append(start)
        prev_end = start + c.duration
    total = prev_end

    # Black base layer guarantees clean fades to/from black.
    bg = ColorClip((WIDTH, HEIGHT), color=BG_COLOR, duration=total)
    video = CompositeVideoClip([bg] + timeline, size=(WIDTH, HEIGHT)).with_duration(total)

    # Whole-video fade in / out.
    video = video.with_effects([vfx.FadeIn(INTRO_FADE), vfx.FadeOut(OUTRO_FADE)])

    # Optional music.
    if os.path.exists(MUSIC_FILE):
        print(f"Adding music: {os.path.basename(MUSIC_FILE)}")
        audio = AudioFileClip(MUSIC_FILE)
        if audio.duration > total:
            audio = audio.subclipped(0, total)
        audio = audio.with_effects([afx.AudioFadeIn(1.0), afx.AudioFadeOut(2.0)])
        video = video.with_audio(audio)
    else:
        print("No music.mp3 found - producing a silent video.")

    print(f"Rendering -> {OUTPUT_FILE}  ({total:.1f}s, {WIDTH}x{HEIGHT}, {FPS}fps)")
    video.write_videofile(
        OUTPUT_FILE,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="6000k",
        ffmpeg_params=["-pix_fmt", "yuv420p"],
        threads=os.cpu_count() or 4,
    )
    print("Done.")


if __name__ == "__main__":
    build()
