# Play Console graphics

- `feature-graphic-1024x500.png`: 1024 × 500, RGB PNG without alpha.
- `screenshots/01…06`: six 1080 × 1920 portrait RGB PNG files, ratio 9:16.
- `play-console-graphics.zip`: the feature graphic and all six screenshot panels.
- `screenshots-preview.jpg`: review contact sheet; do not upload as a screenshot.

These are promotional compositions, not unmodified device screenshots. Panels
include genuine Android companion captures from the tested 1.1.0 build. The first
panel and feature graphic use a photographic reference-watch mockup; the actual
app dial is shown in the companion preview and panels 2–4. The reference watch
and app interpretation have different subdial scales and hand/date positions.
No battery, weather, steps, stopwatch or unsupported platform features are shown.

Headlines are English for international use. The guide capture is Indonesian;
the language panel contains Indonesian and Arabic captures. App language coverage
is 21 translations with English fallback, not every language.

The watch cutout was edited with the built-in imagegen tool from the user's
second photograph. The prompt is preserved in `source/watch-mockup-prompt.txt`.
Source captures and the edited cutout are stored in `source/`. Layouts are
reproducible with `python tools/prepare_play_console_graphics.py` (Pillow,
Windows Arial fonts; use `--font-dir` to choose another font folder containing
`arial.ttf` and `arialbd.ttf`). Original app captures are only cropped/resized;
their UI content has not been synthesized.

Pixel dimensions and RGB mode are asserted by the export script. Store artwork
follows the supplied dark racing-layout reference, without copying its developer
name, status bar, unsupported features or API-level claim.

Use phone screenshots for the Android companion listing. The separate Wear OS
watch-face listing also requires genuine Wear OS screenshots; these phone panels
do not substitute for watch screenshots. See [Google Play preview asset guidance](https://support.google.com/googleplay/android-developer/answer/9866151).
