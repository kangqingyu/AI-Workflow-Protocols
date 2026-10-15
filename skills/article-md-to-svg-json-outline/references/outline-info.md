# 独立说明 JSON 规范

唯一说明文件为 `outline-info.json`，与 `page-*.json`、`outline.txt` 位于同一目录。它提供定位、制作和溯源信息，不是一页 PPT。单页展示 JSON 是展示文字的权威来源；这里的结构和描述不得另写成一份内容不同的大纲。

## 根结构

| 字段 | 类型 | 内容 |
| --- | --- | --- |
| `schema_version` | string | 固定 `"3.0"`，只出现在本说明文件 |
| `metadata` | object | 整份大纲的 `title`、`language`、`source_files`、`section_count`、`slide_count` |
| `parts` | array | 去重后的章节定义，按原文顺序排列 |
| `pages` | array | 每个展示文件的映射与说明，按页码排列 |
| `assets` | array | 去重后的附件定义 |
| `issues` | array | 去重后的编辑问题、路径修正及待核实信息 |

`source_files` 每项为 `{ "id": "source-01", "path": "../文章.md" }`。所有本地路径相对于说明文件所在目录，URL 和保留原文写法的 `original_reference` 除外。

来源范围对象为 `{ "source_id": "source-01", "heading": "1.2 目标", "line_start": 60, "line_end": 111 }`，结束行包含在内。行号从 1 开始，按原文件 LF 分行，CRLF 的 CR 或行内孤立 CR 不另计行。

## 章节

`parts[]` 每项包含 `id`、`part_title`、`source`。`source` 为覆盖整个原文章节的来源范围数组。不同章节使用不同 ID；同一章节跨页复用一个 ID，只在本数组定义一次。

`metadata.section_count` 等于章节数；`metadata.slide_count` 等于 `page-*.json` 数量。说明文件本身不计入两者。

## 页面映射

`pages[]` 每项包含：

| 字段 | 类型 | 内容 |
| --- | --- | --- |
| `id` | string | 全局唯一页面 ID，例如 `slide-003` |
| `file` | string | 对应展示文件，例如 `page-003.json` |
| `page_number` | integer | 从 1 开始连续编号 |
| `type` | string | `cover` / `toc` / `content` / `question` / `exercise` / `ending` |
| `part_id` | string 或 null | 所属章节；封面、目录、额外结束页为 `null` |
| `key_message` | string | 本页核心观点或引导问题 |
| `source` | array | 本页来源范围；封面和目录可为 `[]` |
| `notes` | array | 不直接展示的案例、说明及编辑备注 |
| `content_structure` | array | 展示内容的结构映射节点；无节点时为 `[]` |
| `toc_entries` | array | 仅目录页使用，其他页面为 `[]` |
| `asset_refs` | array | 本页附件及内容位置，无附件时为 `[]` |
| `issue_ids` | array | 与本页有关的编辑问题 ID，无问题时为 `[]` |

`notes` 每项为 `{ "text": "说明文字", "source": [] }`，`source` 遵循来源范围数组。

所有 `content_index` 都从 **0** 开始，指向该页有效分支中的 `content` 数组：封面为 `cover.content`，目录为 `table_of_contents.content`，正文为 `parts[0].pages[0].content`，额外结束页为 `end_page.content`。

页面类型必须与展示有效分支对应。正文、问题和作业的 `part_id` 均须存在，并且章节的 `part_title` 与该展示文件一致。

## 层级、强调与目录

`content_structure` 使用节点树保留层级。每个节点包含：

- `content_index`：对应的展示字符串位置。每个展示文字节点对应一个索引，不重复指向其他文字。
- `kind`：`heading` / `bullet` / `text` / `quote` / `step`。
- `text`：展示文字去除 Markdown 格式符后的文本，不能与对应展示字符串表达不同内容。
- `level`：标题保留原 Markdown 级别；非标题为 `null`。
- `emphasis`：需要强调的 `text` 内子串数组。
- `children`：下属节点数组，叶子为 `[]`；子节点同样有自己的 `content_index`。
- `step` 额外包含 `order`，记录步骤次序。

生成时按节点阅读顺序输出展示字符串，再填入对应索引。这样层级仍可精确还原，但展示 `content` 中没有节点对象。仅用于讲述、不展示的内容放 `notes`，不要创建越界或虚构的索引。

目录页不使用正文节点树；其 `toc_entries` 每项包含 `content_index`、`part_ids`。索引对应目录的展示文字，章节 ID 指向本说明文件的 `parts`。按顺序展开后应完整覆盖全部章节。

## 附件

`assets[]` 每项包含 `id`、`kind`、`status`、`path`、`original_reference`、`description`、`source`：

- `kind`：`image` / `diagram` / `other`。
- `status`：本地已确认文件为 `available`，引用但未找到为 `missing`，仅提出制作需求为 `requested`，未检查远程链接为 `unverified`。
- `path`：实际文件的相对路径或原 URL；缺失或待制作时为 `null`。
- `original_reference`：原文路径、文件名或附件需求原文，不改写为修正后的引用。
- `description`：图片用途或附件需求，不描述原图没有表达的内容。
- `source`：引用出现位置的来源范围数组。

页面的 `asset_refs` 每项为 `{ "asset_id": "asset-01", "content_index": 2 }`。它将第 3 个展示字符串中的图片说明绑定到具体文件。一个附件可被多页引用；同一 ID 在 `assets` 中只定义一次。每条图片说明必须有可对应的引用，不能因路径暂缺而遗漏附件记录。

## 编辑问题

`issues[]` 每项包含 `id`、`kind`、`message`、`source`、`page_ids`、`resolution`：

- `kind`：`asset_resolution` / `missing_asset` / `source_claim` / `editorial_choice`。
- `message`：具体路径问题、待核实主张或编辑取舍。
- `source`：对应来源范围数组。
- `page_ids`：所有受影响页面的 ID；相应页面的 `issue_ids` 须包含该问题 ID。
- `resolution`：已经采用的处理方式；尚未解决的事项如实记录。

相同问题只定义一次，跨页通过 ID 引用。`source_claim` 表示原文尚待核实，不表示已证伪。

## 从旧格式迁移

当用户要求重新生成或迁移旧产物时，先检查实际文件和当前原文，不沿用记忆中的页数。将旧版每页重复的元信息集中到 `metadata`；章节集中到 `parts`；原页面 ID、类型、页码、来源、核心观点、节点及备注移到 `pages`；图片和问题去重进入根数组，再建立映射。展示文字与层级保留，附图补充可定位的展示说明。

用户只要求修改技能时，仅更新技能和规范，不自动覆盖已有大纲。格式验证可在临时目录进行。

校验所有页面文件、章节、来源、内容索引、目录、附件和问题引用可解析且双向一致；展示文件不再携带任何辅助字段。
