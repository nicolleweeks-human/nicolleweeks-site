# Garden Video

A small Python tool that turns garden photos into a short, polished slideshow
video — with EXIF orientation fixing, a gentle Ken Burns (zoom + pan) effect,
crossfade transitions, title/closing cards, optional captions, and optional
background music.

## Quick start

```bash
cd tools/garden-video
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python make_garden_video.py
```

This produces `garden.mp4` in this folder.

> `imageio-ffmpeg` ships a bundled `ffmpeg`, so no system install is required.

## Photos

The five source photos live in `images/` and are listed (with display order and
captions) in the `PHOTOS` list near the top of `make_garden_video.py`. Reorder,
add, or remove entries there.

## Optional music

Drop an MP3 named `music.mp3` in this folder before running and it will be mixed
in automatically (trimmed to length, with fade in/out). No file → silent video,
no error. Use music you have the rights to.

## Tweaking

All the knobs are clearly labeled constants at the top of the script:

| Constant | What it controls |
|---|---|
| `WIDTH`, `HEIGHT`, `FPS` | Output resolution / frame rate |
| `PHOTO_DURATION` | Seconds each photo is shown |
| `TRANSITION` | Crossfade length |
| `TITLE_DURATION`, `CLOSING_DURATION` | Card lengths |
| `INTRO_FADE`, `OUTRO_FADE` | Fade from/to black |
| `KEN_BURNS_ZOOM` | Max zoom magnification (1.0 = off) |
| `SHOW_CAPTIONS` | Per-photo lower-corner labels on/off |
| `TITLE_TEXT`, `TITLE_SUBTITLE`, `CLOSING_TEXT` | Card text |

## Notes

- The `.venv` and the generated `garden.mp4` are git-ignored (see
  `.gitignore` in this folder); the source photos and script are committed.
