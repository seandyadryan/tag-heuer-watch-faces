# McLaren red dial — 1.1.0

New default dial based on the watch photo supplied by the user: brushed red McLaren bezel, textured black face, silver applied indices, TAG Heuer shield, three circular subdial wells and angled date aperture. This is a generated interpretation of the reference, not an exact scan of the physical watch.

The built-in imagegen tool generated only the background, without hands, hubs or date digits. The full generation prompt is preserved in [the prompt file](../assets/source/mclaren_red_prompt.txt). The original generated master is [mclaren_red_background.png](../assets/source/mclaren_red_background.png). The supplied photograph was used as a visual reference and is not redistributed in this repository.

Runtime exports in both modules:

- `dial_mclaren_red.png`: 450×450 dial background.
- `subdial_hand.png`: separate 6×45 silver indicator.
- `metal_cap.png`: separate silver hub, 16×16.
- `preview_mclaren_red.png`: composed picker/launcher preview, 450×450.
- Existing hour/minute/second PNGs remain separate live layers. Original `dial.png`/`accent.png`/`preview.png` remain available; the new red assets use sibling filenames.

The left subdial displays current seconds, the right displays current minutes, and the lower subdial displays the current 12-hour time. These are clock indicators, not an elapsed-time stopwatch. The angled date window shows the device's current day of month. The red bezel is fixed artwork; the editor changes the main second-hand color. The phone preview follows the same geometry. Ambient hides the textured dial, date, subdials and seconds, keeping dim main hands and digital time.

Regenerate optimized exports after replacing the master:

```powershell
python tools/prepare_mclaren_assets.py
python tools/verify_project.py
```

Commercial trademark/logo authorization remains required as described in [Play preparation](PLAY-STORE.md). Generated images do not grant trademark authorization.
