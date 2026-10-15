---
name: docx-to-svg-json-outline
description: Convert a chapter draft in DOCX format into the repository's PPT SVG JSON outline files by extracting Word Heading 1 and Heading 2 paragraphs, creating one directory JSON plus one JSON file per Heading 1, assigning stable chapter/section filenames, excluding body paragraphs, and extracting embedded images with JSON placeholder text and width-to-height ratios. Use when the user asks to generate, regenerate, split, or validate PPT SVG JSON outlines and image assets from a Word chapter draft, especially when origginSVG.json and earlier chapter output folders define the expected schema and naming convention.
---

# DOCX to SVG JSON Outline

Generate chapter-level PPT outline files and their image assets from Word. Treat the source DOCX, the supplied `origginSVG.json`, and existing chapter examples as the authorities.

## Workflow

1. Read the complete DOCX and presentation skills if they are available in the session.
2. Inspect the supplied SVG JSON template and at least one completed sibling chapter. Preserve the marker format `[PPT_OUTLINE] ... [/PPT_OUTLINE]` and any repository-specific conventions.
3. Use Word paragraph styles, not font size or visual guesses:
   - Heading 1 becomes a separate JSON file and its `cover.title`.
   - Heading 2 becomes a page `title` under the current Heading 1.
   - Normal paragraphs and all other body content must not appear in output.
   - TOC paragraphs inside Word are not source headings unless they actually use Heading 1 or Heading 2.
   - Embedded images attach to the nearest preceding Heading 2 page; before any Heading 2, attach them to the current Heading 1 cover.
   - Images before the first Heading 1 attach to the directory cover.
4. Read [references/schema-and-naming.md](references/schema-and-naming.md) before choosing filenames or changing the schema.
5. Resolve the bundled workspace Python runtime and run the generator in plan mode first:

   ```bash
   python scripts/build_outline.py \
     --input-docx "/absolute/path/chapter.docx" \
     --output-dir "/absolute/path/PPT/500" \
     --cover-title "第五章 读书上瘾模型" \
     --plan
   ```

6. Review the proposed filenames, Heading 1 covers, Heading 2 counts, directory order, image filenames, source names, and width-to-height ratios. If source styles are custom, pass `--heading1-style` and `--heading2-style` with the exact Word style names.
7. Generate the files. Add `--overwrite` only when replacement is explicitly authorized or the target files were created in the current task:

   ```bash
   python scripts/build_outline.py \
     --input-docx "/absolute/path/chapter.docx" \
     --output-dir "/absolute/path/PPT/500" \
     --cover-title "第五章 读书上瘾模型"
   ```

8. Inspect the generated directory and report the directory file count, Heading 1 count, Heading 2 count, directory entry count, extracted image count, and validation result.

## Guardrails

- Never copy body paragraphs into `content`. Permit only generated image-placeholder strings; otherwise use empty arrays.
- Extract every embedded image to the output directory. Convert formats such as TIFF or BMP to PNG when needed for downstream SVG use; preserve PNG, JPEG, GIF, WebP, and SVG when possible.
- Write each placeholder as `图片占位：<file>（宽高比 <ratio>:1）` in the cover or page that owns the image.
- Do not invent, rewrite, summarize, or correct heading text unless the user asks. Preserve punctuation and spacing from Word.
- Keep every Heading 1, including unnumbered ones. Use suffixes such as `503-2.json` for additional Heading 1 blocks associated with section `5.3`.
- Sort only the directory's numbered section entries by numeric section number. Preserve source order for headings and pages within each section file.
- Do not overwrite unrelated files. Stop on collisions unless `--overwrite` is justified.
- If the repository template conflicts with the bundled generator schema, follow the repository template and adapt the generator locally for that task.

## Generator

Use `scripts/build_outline.py`. It performs heading and image extraction, image conversion, naming, generation, marker/schema parsing, heading/image coverage checks, and body-content exclusion checks in one deterministic pass.
