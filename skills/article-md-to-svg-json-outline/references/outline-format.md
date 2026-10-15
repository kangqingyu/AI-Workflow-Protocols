# JSON 字段规范

本规范使用 `schema_version: "2.0"`，交付单位为单页。路径以 JSON 文件所在目录为基准，URL 及保留原文写法的 `original_reference` 除外；行号从 1 开始，按原文件 LF 分行，CRLF 中的 CR 或行内孤立 CR 不另计行。

## 每页根对象

每组 `[PPT_OUTLINE]…[/PPT_OUTLINE]` 内恰好一个以下结构的 JSON 对象，同一对象单独保存为 `page-NNN.json`。`ppt_outline` 直接是一页，不再使用旧版整份大纲的 `cover`、`table_of_contents`、`parts[].pages`、`end_page` 嵌套结构。

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `schema_version` | string | 固定为 `2.0` |
| `metadata` | object | 整份大纲的标题、语言、来源及计数；每个文件包含相同的元信息 |
| `part` | object 或 null | 本页所属章节；封面、目录、额外结束页为 `null` |
| `ppt_outline` | object | 恰好一个页面对象 |
| `issues` | array | 与本页有关的路径问题、原文疑点及编辑取舍；没有时为 `[]` |

`metadata` 包含 `title`、`language`、`source_files`、`section_count`、`slide_count`。`source_files` 每项为 `{ "id": "source-01", "path": "../文章.md" }`。

`part` 为 `{ "id": "part-01", "part_title": "原文一级标题", "source": [] }`，其中 `source` 是指向整个原文章节的来源范围数组。原文的总结或作业属于正文，也填写所属 `part`。同一章节拆出的多页保留相同章节定义，不在 `part` 内嵌套其他页面。

`metadata.source_files` 在每页中保留完整来源表，使每个页面的来源 ID 可独立解析。`slide_count` 是整份大纲总页数，`section_count` 是正文一级标题对应的章节数；它们不是本文件中的页数或章节数。

- 封面：`ppt_outline.type: "cover"`，可另有 `sub_title`。
- 目录：`ppt_outline.type: "toc"`；`content` 为导航节点数组，每项包含 `text` 和 `part_ids`。章节 ID 指向整份单页文件集合中的 `part.id`。
- 正文、问题与作业：分别使用 `content`、`question`、`exercise` 类型。
- 用户另行要求的结束页：`ppt_outline.type: "ending"`；未要求时不创建该页或空文件。

## 标签与文件的一一对应

`outline.txt` 按顺序拼接单页块，块之间空一行，每个块包含开始标签、一个单页 JSON 对象、结束标签。解析时仅将**独占一行**的标签视为边界；JSON 字符串中的标签字样不作为分隔符。

独立文件采用 `page-001.json`、`page-002.json` 等名称，编号等于 `ppt_outline.page_number`。补零宽度为 `max(3, 总页数的十进制位数)`，全套保持一致。所有单页文件和汇总文本位于同一输出目录；不把汇总文本改名为 `.json`，也不在独立 JSON 外再添加标签。

以下是一个完整的单页块示例。`page-003.json` 只保存这两个标签之间的对象；其他页各自使用另一组标签及另一个 JSON 文件。

```text
[PPT_OUTLINE]
{
  "schema_version": "2.0",
  "metadata": {
    "title": "明确目标",
    "language": "zh-CN",
    "source_files": [{ "id": "source-01", "path": "../文章.md" }],
    "section_count": 1,
    "slide_count": 3
  },
  "part": {
    "id": "part-01",
    "part_title": "1.2 目标",
    "source": [{ "source_id": "source-01", "heading": "1.2 目标", "line_start": 60, "line_end": 111 }]
  },
  "ppt_outline": {
    "id": "slide-003",
    "page_number": 3,
    "type": "content",
    "title": "1.2 目标",
    "key_message": "先明确目标，再选择手段。",
    "source": [{ "source_id": "source-01", "heading": "1.2 目标", "line_start": 60, "line_end": 111 }],
    "content": [{ "kind": "bullet", "text": "区分想获得的结果与具体行动", "level": null, "emphasis": [], "children": [] }],
    "assets": [],
    "notes": []
  },
  "issues": []
}
[/PPT_OUTLINE]
```

## 页面与来源

每个文件的 `ppt_outline` 包含以下字段；不适用的数组使用 `[]`，不省略字段。

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `id` | string | 全文唯一，例如 `slide-003` |
| `page_number` | integer | 从封面开始连续编号 |
| `type` | string | `cover` / `toc` / `content` / `question` / `exercise` / `ending` |
| `title` | string | 页面标题 |
| `key_message` | string | 本页核心观点或引导问题 |
| `source` | array | 本页来源范围；封面和目录可为 `[]` |
| `content` | array | 展示节点；目录使用导航节点 |
| `assets` | array | 本页附件，无附件时为 `[]` |
| `notes` | array | 不直接展示的案例、说明及编辑备注 |

来源范围对象为 `{ "source_id": "source-01", "heading": "1.2 目标", "line_start": 60, "line_end": 111 }`，结束行包含在内。正文页可引用多个范围；页面主要范围应位于所属章节内。`notes` 每项包含 `text` 和 `source`（来源范围数组）。

## 展示节点与层级

节点包含 `kind`、`text`、`level`、`emphasis`、`children`：

- `kind`：`heading` / `bullet` / `text` / `quote` / `step`。
- `text`：去掉 Markdown 格式符的展示文字。
- `level`：标题节点保留原 Markdown 级别，例如 `2`、`3`、`4`；非标题节点为 `null`。
- `emphasis`：需要强调的 `text` 内子串数组；保留原文粗体的含义，不把整页全部加粗。
- `children`：下属节点数组。标题下的列表和子标题放在其内部，叶子为 `[]`；不可用虚构的标题改变来源层级。
- `step` 节点额外包含 `order`（从 1 开始的整数）；引文出处可直接包含在 `text` 中。

```json
{
  "kind": "heading",
  "text": "大学期间的一些活动",
  "level": 2,
  "emphasis": [],
  "children": [
    {
      "kind": "bullet",
      "text": "买书是手段，理解新知识才是目的",
      "level": null,
      "emphasis": ["理解新知识"],
      "children": []
    }
  ]
}
```

## 附件

每项包含 `id`、`kind`、`status`、`path`、`original_reference`、`description`、`source`。

- `kind`：`image` / `diagram` / `other`。
- `status`：本地文件已验证为 `available`；引用但未找到为 `missing`；仅提出制作需求为 `requested`；远程链接未检查为 `unverified`。
- `path`：相对 JSON 文件的实际文件路径或原 URL。未找到、待制作时为 `null`。
- `original_reference`：原文所用的原始路径、文件名或附件需求文字，不替换成修正后的引用。
- `description`：图片用途或附件需求，不能声称原图没有表达的内容。
- `source`：引用出现位置的来源范围数组。
- 一个附件若被多页使用可沿用同一附件 ID，定义必须一致。

## 编辑问题记录

每项包含 `id`、`kind`、`message`、`source`、`page_ids`、`resolution`。

- `kind`：`asset_resolution` / `missing_asset` / `source_claim` / `editorial_choice`。
- `message`：具体路径问题、待核实原文主张或摘要取舍。
- `source`：对应来源范围数组；`page_ids` 定位整份大纲中所有受影响页面。将该问题的相同定义复制到每个受影响页面的 `issues` 中；该数组中的每项都应包含当前页面 ID，其他页面可通过其文件定位。
- `resolution`：已采用的处理方式，例如“保留原章节标题；正文只概括渐进挑战思想，15% 的研究归属未核实”。

JSON 校验不仅检查语法，还应核对标签块与单页文件的一一对应、元信息一致性、章节归属、目录及问题的跨页引用。全局计数按独立页面及不同章节 ID 统计，不因同一章节重复出现而重复计数。`source_claim` 表示原文尚待核实，不表示已经证伪；无需为了填满此数组而逐句挑错。
