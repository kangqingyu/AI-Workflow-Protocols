# Schema and naming rules

## Output schema

Each file is UTF-8 text containing a JSON object between the repository markers:

```text
[PPT_OUTLINE]
{
  "ppt_outline": {
    "cover": {
      "title": "Heading 1 text",
      "content": []
    },
    "parts": [
      {
        "pages": [
          {
            "title": "Heading 2 text",
            "content": ["图片占位：501-image-01.png（宽高比 1.78:1）"]
          }
        ]
      }
    ]
  }
}
[/PPT_OUTLINE]
```

Omit `parts` when a Heading 1 has no Heading 2 children. Do not insert Normal-style paragraphs into any `content` array. A `content` array may contain only generated image-placeholder strings.

The directory file uses the same markers and contains only `cover` plus `table_of_contents`:

```json
{
  "ppt_outline": {
    "cover": {"title": "第五章 读书上瘾模型", "content": []},
    "table_of_contents": {
      "title": "目录",
      "content": ["5.1 ...", "5.2 ..."]
    }
  }
}
```

## Filenames

Let `base = chapter_number * 100`.

- Directory: `<base>.json`; chapter 5 becomes `500.json`.
- Numbered Heading 1 `5.1`: `<base + section>.json`, or `501.json`.
- First additional unnumbered Heading 1 after `5.1`: `501-2.json`.
- Further unnumbered Heading 1 blocks: `501-3.json`, `501-4.json`, and so on.
- A repeated numbered Heading 1 uses the same suffix sequence rather than overwriting.
- An unnumbered Heading 1 before the first numbered section uses `<base>-2.json`, then `<base>-3.json`.

Numbered headings may appear out of order in the DOCX. Derive filenames from their explicit section numbers. Sort the directory entries numerically, while leaving each file's child pages in source order.

## Images

- Associate an image with the nearest preceding Heading 2. If no Heading 2 has appeared under the current Heading 1, associate it with that file's cover. Associate images before the first Heading 1 with the directory cover.
- Extract each occurrence as a separate output asset, even when Word reuses the same underlying image relationship.
- Name content images `<json-stem>-image-01.<ext>`, `<json-stem>-image-02.<ext>`, and so on in document order.
- Name directory-cover images `<base>-image-01.<ext>` and so on.
- Use the displayed Word extent for the width-to-height ratio when available; otherwise use intrinsic pixel dimensions.
- Round the displayed ratio to two decimals and format the placeholder exactly as `图片占位：501-image-01.png（宽高比 1.78:1）`.
- Preserve PNG, JPEG, GIF, WebP, and SVG. Convert TIFF, BMP, and other Pillow-readable raster formats to PNG for SVG compatibility.

## Required validation

- Every output parses as JSON after removing markers.
- Number of content JSON files equals the number of nonempty Heading 1 paragraphs.
- Every Heading 1 appears exactly once as a content-file cover.
- Every Heading 2 appears exactly once as a page under its nearest preceding Heading 1.
- Every nonempty content array contains only image-placeholder strings.
- Every DOCX image occurrence produces a nonempty extracted asset and exactly one matching placeholder with its ratio.
- Directory entries equal the first occurrence of every numbered Heading 1 in the chapter.
