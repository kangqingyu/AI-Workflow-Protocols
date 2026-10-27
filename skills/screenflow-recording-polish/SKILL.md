---
name: screenflow-recording-polish
description: "Prepare an existing ScreenFlow recording with a camera overlay: adjust synchronized clip speed, canvas dimensions, camera audio volume, and automatic background blur through macOS Computer Use. Use when asked to apply this recorded ScreenFlow workflow or these preparation steps."
---

# ScreenFlow Recording Polish

Edit an already assembled ScreenFlow project containing a screen recording and a camera overlay. Leave the prepared project open for review. Recording/importing media, composing the camera overlay, saving under a new name, and exporting are separate tasks unless the user requests them.

## Inputs and defaults

Resolve the project and target clips from the user's request and the current interface. If more than one project or clip pair fits, ask which one to edit before making changes.

| Input | Default for the full recorded workflow |
| --- | --- |
| Project | Active ScreenFlow document, if unambiguous |
| Screen and camera clips | The corresponding synchronized pair in that document |
| Clip speed | 115% (1.15×), applied to both clips and their associated audio |
| Canvas width × height | 3456 × 1944 pixels |
| Screen recording scale & position | Scale: `100%`, Position: `X = 0, Y = 64` (exact full-bleed alignment for the 1944px PPT frame) |
| Camera overlay scale & position | Scale: `60%`, Position: `X = 1200, Y = 574` (top-right corner of the `3456 × 1944` canvas) |
| Camera clip audio volume | 190% |
| Camera background mode | Automatic Background Removal → Background: Blur |
| Blur amount | Preserve the existing/default amount unless specified |

These numeric defaults come from the demonstration and are overridable inputs, not universal editing recommendations. Apply only the requested subset when the user asks for a narrower change. Do not infer that 190% is suitable for every recording or that all projects should use the demonstrated resolution. If the user requests only a 16:9 aspect ratio, preserve the current width and derive the height; do not silently replace an explicit resolution.

## Tool choice and UI targeting (Codex vs. Antigravity)

Dispatch Computer Use operations based on the current AI Coding tool environment. No ScreenFlow editing connector was available when this skill was created; if a dedicated tool becomes available, use it only when it supports the same project edits and verification.

### A. Codex / ChatGPT Environment (with built-in `mcp__cua_repl` / `cua_repl`)

- **Keep the original built-in approach unchanged**: Use **Computer Use** directly through `mcp__cua_repl` (`cua.listApps()`, `getAXState()`, `setValue` / `paste`, native screenshots, semantic actions, and coordinate clicks) for ScreenFlow's native interface and visual checks.

### B. Antigravity Environment (without built-in `mcp__cua_repl`)

- **Core Principle 1 (Fast Single-Process Pipeline `polish`)**:
  - When applying the standard preparation workflow in Antigravity, **prefer running the single-process pipeline command `polish`** instead of 6–8 separate interactive round-trips:
    - `python3 /Users/kqy/.gemini/config/skills/screenflow-recording-polish/scripts/mac_cua.py polish --speed 115 --width 3456 --height 1944 --volume 190 --verify-shot "<output_verify.png>"`
  - It executes the entire 6-step workflow in ~3 seconds inside the standard sandbox (`BypassSandbox: false`), automatically handling secondary-display window relocation, per-clip speed verification, canvas resizing, camera-only selection, 190% audio volume, and `Automatic Background Removal -> Blur`.
- **Core Principle 2 (Never send `cmd+a` inside ScreenFlow numeric fields; use `field-type`)**:
  - **Root cause of speed commit failure**: In ScreenFlow, `cmd+a` is bound to `Edit -> Select All Clips` in the menu bar. Sending `cmd+a` while focused in `Clip Inspector` (or `Canvas Crop` / `Volume`) intercepts focus back to the timeline instead of selecting the text field. Furthermore, `Clip Inspector` is a floating child window (`[AXWindow/AXUnknown]`), so invoking `bring_to_front()` across separate CLI calls steals focus away from the text field.
  - **Standard action**: Always use `field-type <x> <y> "<value>"` (which double-clicks `(x, y)` with `focus_first=False` and sends individual hardware keycodes `1`, `1`, `5`, `return` in a single process).
- **Core Principle 3 (Keep `Clip Inspector` open to verify/apply speed across each synchronized clip)**:
  - Right-clicking a clip can sometimes reduce a multi-clip selection to a single clip. However, while `Clip Inspector` remains open, single-clicking any timeline clip immediately updates `Clip Inspector` to inspect that clip (note that `Clip Inspector`'s `y` coordinate shifts dynamically with the selected track). Click each target clip (`FaceTime HD Camera` and `Screen Recording`), read the current `help="Adjusts the relative speed of the clip."` field position, and apply `field-type` if its value is not yet `115%`. Confirm both `AXLayoutItem` widths match (`1342.0`).
- **Core Principle 4 (Click empty timeline area to deselect before selecting only the camera clip)**:
  - When multiple clips are highlighted in yellow, single-clicking one clip (or clicking the main window while `Clip Inspector` is active) may keep both clips selected. Before Step 4 (Camera Audio Volume), close `Clip Inspector` via `AXPress` on its close button, **click an empty timeline area (e.g., `(500, 990)`) to deselect all**, and then click `FaceTime HD Camera` `(500, 854)`.
- **Core Principle 5 (Filter by `AXMenuItem` when selecting `Blur` to avoid `Blur Size:` static text)**:
  - `Video Properties Tab` contains a static label `value="Blur Size:"` under Drop Shadow. `find_and_press_ax` skips `AXStaticText` and supports `role_filter="AXMenuItem"` so clicking the `Background:` popup (`Clear` → `Blur`) targets `[AXMenuItem] title="Blur"` directly.
- **Core Principle 6 (Exact PPT Frame Alignment `(0, 64)` & Top-Right 60% Camera Placement `(1200, 574)` + Backspace Clearing)**:
  - **PPT Frame Full-Bleed Fit**: On a 16-inch MacBook Pro (`3456 × 2232` recording), the top menu bar + PowerPoint title bar + top border occupy `208 px`, the 16:9 PPT slide occupies `1944 px`, and the bottom border occupies `80 px` (`208 + 1944 + 80 = 2232`). After cropping the canvas to `3456 × 1944` (which trims `144 px` top and bottom by default), setting the **Screen Recording** clip's `Position` to `X = 0, Y = 64` (`208 - 144 = 64`) at `Scale = 100%` aligns the `1944 px` PPT slide edge-to-edge with zero top/bottom bars.
  - **Camera Overlay Top-Right at 60%**: The native `FaceTime HD Camera` clip is `1760 × 1328`. At `Scale = 60%`, its scaled size is `1056 × 796.8` (half-size `528 × 398.4`). In ScreenFlow's Cartesian canvas coordinates (`+X` right, `+Y` up; canvas top-right corner is `(+1728, +972)`), setting the camera clip's `Position` to `X = 1200, Y = 574` (`1728 - 528 = 1200`, `972 - 398.4 = 573.6 ≈ 574`) places the camera overlay flush in the top-right corner.
  - **Clear Minus Signs & Commas via Right-Arrow + Backspaces**: macOS word double-click on `-652` or `1,122` only selects digits after `-` or `,`. `type_keys_in_field` sends `right` followed by 8 `delete` keystrokes after double-clicking so negative signs and thousands separators are completely cleared without using `cmd+a`.
- **Step-by-step / Custom CLI Commands** (`scripts/mac_cua.py`, 1:1 equivalent to `mcp__cua_repl`):
  - **List / Activate ScreenFlow** (maps to `cua.listApps()` and app connection):
    - `python3 <skill_dir>/scripts/mac_cua.py list-apps`
    - `python3 <skill_dir>/scripts/mac_cua.py activate`
  - **Read Accessibility Tree** (maps to `getAXState()`, outputting `title`, `desc`, `help`, `value`, `id`, logical `rect=(x,y,w,h)`, and `center=(cx,cy)`):
    - `python3 <skill_dir>/scripts/mac_cua.py ax-state --depth 12` (supports `--filter "<keyword>"`, `--bbox x1,y1,x2,y2`, `--head N`, and `--include-menubar`)
  - **1:1 Logical-Coordinate Screenshot** (pair with `read_file` for visual verification; pixel `(x, y)` maps 1:1 to logical click coordinates):
    - `python3 <skill_dir>/scripts/mac_cua.py screenshot <output.png>` (supports `--rect x,y,w,h` for region crops)
  - **Mouse, Selection & Context Menu Actions**:
    - Clicks: `click <x> <y>` (supports `--shift` or `--cmd` for additive multi-clip selection), `double-click <x> <y>`, `right-click <x> <y>` (opens clip context menu such as `Show Clip Inspector...`)
    - Drag / Marquee selection: `drag <x1> <y1> <x2> <y2>`
    - Scroll: `scroll <x> <y> <dy>` (negative `dy` scrolls down)
    - Semantic press: `ax-press "<keyword>"` (matches `AXTitle`, `AXDescription`, `AXHelp`, or `AXIdentifier`, automatically skipping `AXStaticText`)
  - **Keyboard & Numeric Field Entry** (maps to `setValue` / `paste` / key commit):
    - **ScreenFlow numeric field entry (Recommended)**: `field-type <x> <y> "<value>"` (double-clicks `(x, y)` and types key-by-key + `Return` in one process without `cmd+a`)
    - Direct Unicode entry: `type "<value>" --enter`
    - Clipboard paste: `paste "<value>" --enter`
    - Key combos: `key return`, `key escape`, `key tab`, `key cmd+a`
  - **Chained Post-Action Inspection** (reduces round-trips):
    - Append `--ax --ax-filter "<keyword>"` or `--shot <output.png>` to any action command to execute the edit and read back the updated state in a single step.

### Common UI Targeting Rules (Both Codex and Antigravity)

Select ScreenFlow by app name (`/Applications/ScreenFlow.app`); the demonstrated version used bundle ID `net.telestream.screenflow10`. Follow the current Computer Use tool documentation (`mcp__cua_repl` in Codex; `scripts/mac_cua.py` in Antigravity). Read the live accessibility tree and screenshots before acting. Target controls by labels, help text (`AXHelp`), and role, using current screenshot coordinates only where a control lacks a semantic target. Recorded element IDs, window IDs, timeline zoom, and pixel positions are not reusable locators.

Useful targets from the demonstration:

- Timeline clips: `Screen Recording …` and `FaceTime HD Camera`. These are examples; match the actual clip roles and names in the current project.
- Clip context menu: `Show Clip Inspector...`; inspector speed field help: `Adjusts the relative speed of the clip.`
- Toolbar: `Canvas Crop`; popover: `Canvas:` with width and height fields separated by `x`.
- `Audio Properties Tab`: volume field help begins `The Volume of the selected clip(s).` Distinguish it from ducking and effect amount fields.
- `Video Properties Tab` → `Filters & Effects` → `Add Video Filter` → `Background Removal` → `Automatic` → `Add`.
- Added filter: checkbox `Automatic Background Removal`, `Background:` popup with `Clear` and `Blur`.

## Procedure

### 1. Identify the composition

Inspect the active project, timeline, and canvas. Identify the screen clip, camera clip, and any separate audio that must stay synchronized. Record current speeds, start times, durations, canvas size, camera volume, and existing background effect state as available.

The demonstration starts with a composed camera overlay. Preserve its scale, position, and layer order; the visible camera scale and position were existing settings, not actions to reproduce. Likewise, preview speaker mute is not a request to mute the rendered video.

### 2. Apply clip speed

Select the intended synchronized clips, using additive selection (in Antigravity: `click <x> <y> --shift` or `drag` marquee) or a selection rectangle with visual verification. Use Select All only if every timeline clip is in scope. Open the context menu (`right-click <x> <y>`) and choose `Show Clip Inspector...`.

Replace the **Speed** field with the requested absolute percentage and commit it with Return or the control's supported commit action (in Antigravity: locate the Speed field whose `help="Adjusts the relative speed of the clip."`, then run `field-type <cx> <cy> "115" --ax --ax-filter "speed"`—never send `cmd+a`, which triggers `Select All Clips`). Reopen or refocus the inspector and read the stored speed of each target clip. Do not multiply an already adjusted speed by 1.15 on repeated runs.

Check that synchronization is preserved. For an unchanged source range, expected new duration is approximately `old duration × old speed / target speed`, allowing frame rounding. A displayed typed value alone is not proof that ScreenFlow applied the edit. If the new value fails to persist, re-identify the field and retry its commit once; if it still fails, stop this step and report the observed state. Do not compensate by trimming, moving clips, or changing duration fields.

### 3. Set canvas dimensions and align PPT screen recording frame

Open `Canvas Crop`. Set width and height to the resolved dimensions; when width already matches, change height only. Commit and reopen the popover to verify both values. The demonstration changed height from 2232 to 1944 while leaving width at 3456.

After setting the canvas height to `1944`, select **only the screen recording clip**, open `Video Properties Tab`, ensure **Scale** is `100%`, and set **Position** to `X = 0, Y = 64` so that the `3456 × 1944` PPT slide area fills the `3456 × 1944` canvas edge-to-edge without top menu bars or bottom borders.

### 4. Set camera audio volume

Close the crop popover, deselect all clips by clicking an empty timeline area, and select **only the camera clip**. Open `Audio Properties Tab`, set its **Volume** field to the requested percentage, commit, and read it back. Typing the numeric value is preferable to reproducing the demonstrated slider drag.

If the camera clip has no editable audio, identify whether the user intended a separate narration track before changing any other track. Leave ducking, normalization, noise removal, and effects at their existing settings. Verify the committed volume by reading the field back; audio audition is not part of this workflow.

### 5. Position camera overlay at top-right (60%) and apply automatic background blur

Keep only the camera clip selected and open `Video Properties Tab`:

1. Set **Scale** to `60%` and **Position** to `X = 1200, Y = 574` (clearing any leading `-` sign on Y) to place the camera overlay flush in the top-right corner of the `3456 × 1944` canvas.
2. Reuse an existing `Automatic Background Removal` filter when present. Otherwise choose `Add Video Filter`, select `Automatic` within the **Background Removal** category, and click `Add` or confirm the sheet.

Ensure the filter is enabled, then set its **Background** popup to **Blur**. Re-read the popup after the menu closes. `Clear` removes the background; it is not the demonstrated final mode. Preserve the existing/default blur amount unless the user supplies one. Avoid stacking duplicate filters on repeated runs.

Check the static canvas preview without starting playback: the camera subject should remain visible with a blurred camera background, while the screen recording remains unaffected. If the app needs processing time, wait briefly and check again; report a processing error or persistent lack of effect instead of claiming success.

### 6. Verify and hand back

Check the stored speed on each target, clip start times and durations for timeline alignment, canvas dimensions, camera volume, enabled filter, and **Blur** mode. Use setting readbacks, the timeline, and the static canvas preview for verification. Do not start trial playback, audition audio, or toggle preview speaker mute unless the user explicitly asks for playback. Preserve the current playhead and preview mute state. Leave the project open and state which settings were applied and any unverified result. Save or export only when included in the user's request; existing authorization does not require reconfirmation.

## Evidence limits

The source recording showed entry of `115` in Speed, but subsequent duration text remained unchanged and no successful speed commit was captured. Treat 115% as the demonstrated intended setting and verify persistence during execution. The recording captured selecting `Blur`, but no later ScreenFlow snapshot confirmed the final popup value or rendered effect; verify both during execution. Canvas dimensions and 190% camera volume were visible after editing. No save or export was demonstrated.

This skill was derived from recorded UI events. Structural validation does not establish successful end-to-end replay.
