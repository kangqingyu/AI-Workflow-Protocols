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
| Camera clip audio volume | 190% |
| Camera background mode | Automatic Background Removal → Background: Blur |
| Blur amount | Preserve the existing/default amount unless specified |

These numeric defaults come from the demonstration and are overridable inputs, not universal editing recommendations. Apply only the requested subset when the user asks for a narrower change. Do not infer that 190% is suitable for every recording or that all projects should use the demonstrated resolution. If the user requests only a 16:9 aspect ratio, preserve the current width and derive the height; do not silently replace an explicit resolution.

## Tool choice and UI targeting (Codex vs. Antigravity)

Dispatch Computer Use operations based on the current AI Coding tool environment. No ScreenFlow editing connector was available when this skill was created; if a dedicated tool becomes available, use it only when it supports the same project edits and verification.

### A. Codex / ChatGPT Environment (with built-in `mcp__cua_repl` / `cua_repl`)

- **Keep the original built-in approach unchanged**: Use **Computer Use** directly through `mcp__cua_repl` (`cua.listApps()`, `getAXState()`, `setValue` / `paste`, native screenshots, semantic actions, and coordinate clicks) for ScreenFlow's native interface and visual checks.

### B. Antigravity Environment (without built-in `mcp__cua_repl`)

- **Use the bundled CLI tool `scripts/mac_cua.py`** (located relative to this `SKILL.md`, e.g., `/Users/kqy/.gemini/antigravity/skills/screenflow-recording-polish/scripts/mac_cua.py`), which provides 1:1 equivalents to `mcp__cua_repl` via macOS native `ApplicationServices` and `CoreGraphics` (zero third-party dependencies, runs in the standard sandbox, and automatically relocates off-screen secondary-display windows with `y < 0` back to the main screen):
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
    - Semantic press: `ax-press "<keyword>"` (matches `AXTitle`, `AXDescription`, `AXHelp`, or `AXIdentifier`)
  - **Keyboard & Numeric Field Entry** (maps to `setValue` / `paste` / key commit):
    - Direct Unicode/numeric entry: `type "<value>" --select-all --enter` (sends `cmd+a`, injects UTF-16 characters via `CGEvent`, and commits with `Return`)
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

Replace the **Speed** field with the requested absolute percentage and commit it with Return or the control's supported commit action (in Antigravity: click the Speed field whose `help="Adjusts the relative speed of the clip."`, then run `type "115" --select-all --enter --ax --ax-filter "speed"`). Reopen or refocus the inspector and read the stored speed of each target clip. Do not multiply an already adjusted speed by 1.15 on repeated runs.

Check that synchronization is preserved. For an unchanged source range, expected new duration is approximately `old duration × old speed / target speed`, allowing frame rounding. A displayed typed value alone is not proof that ScreenFlow applied the edit. If the new value fails to persist, re-identify the field and retry its commit once; if it still fails, stop this step and report the observed state. Do not compensate by trimming, moving clips, or changing duration fields.

### 3. Set canvas dimensions

Open `Canvas Crop`. Set width and height to the resolved dimensions; when width already matches, change height only. Commit and reopen the popover to verify both values. The demonstration changed height from 2232 to 1944 while leaving width at 3456.

Inspect the resulting frame for the screen content and camera overlay. Canvas resizing may crop content; do not silently rescale or reposition clips to compensate. Report visibly cut-off intended content if it needs a separate composition decision.

### 4. Set camera audio volume

Close the crop popover and select **only the camera clip**. Open `Audio Properties Tab`, set its **Volume** field to the requested percentage, commit, and read it back. Typing the numeric value is preferable to reproducing the demonstrated slider drag.

If the camera clip has no editable audio, identify whether the user intended a separate narration track before changing any other track. Leave ducking, normalization, noise removal, and effects at their existing settings. Verify the committed volume by reading the field back; audio audition is not part of this workflow.

### 5. Apply automatic background blur

Keep only the camera clip selected and open `Video Properties Tab`. Reuse an existing `Automatic Background Removal` filter when present. Otherwise choose `Add Video Filter`, select `Automatic` within the **Background Removal** category, and click `Add` or confirm the sheet.

Ensure the filter is enabled, then set its **Background** popup to **Blur**. Re-read the popup after the menu closes. `Clear` removes the background; it is not the demonstrated final mode. Preserve the existing/default blur amount unless the user supplies one. Avoid stacking duplicate filters on repeated runs.

Check the static canvas preview without starting playback: the camera subject should remain visible with a blurred camera background, while the screen recording remains unaffected. If the app needs processing time, wait briefly and check again; report a processing error or persistent lack of effect instead of claiming success.

### 6. Verify and hand back

Check the stored speed on each target, clip start times and durations for timeline alignment, canvas dimensions, camera volume, enabled filter, and **Blur** mode. Use setting readbacks, the timeline, and the static canvas preview for verification. Do not start trial playback, audition audio, or toggle preview speaker mute unless the user explicitly asks for playback. Preserve the current playhead and preview mute state. Leave the project open and state which settings were applied and any unverified result. Save or export only when included in the user's request; existing authorization does not require reconfirmation.

## Evidence limits

The source recording showed entry of `115` in Speed, but subsequent duration text remained unchanged and no successful speed commit was captured. Treat 115% as the demonstrated intended setting and verify persistence during execution. The recording captured selecting `Blur`, but no later ScreenFlow snapshot confirmed the final popup value or rendered effect; verify both during execution. Canvas dimensions and 190% camera volume were visible after editing. No save or export was demonstrated.

This skill was derived from recorded UI events. Structural validation does not establish successful end-to-end replay.
