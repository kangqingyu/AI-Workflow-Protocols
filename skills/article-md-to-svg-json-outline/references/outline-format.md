# 展示 JSON 规范

展示数据严格采用用户的标准结构。格式版本、来源、页码、类型、附件详情及备注集中在 [outline-info.json 说明规范](outline-info.md) 中；展示文件根字段只有 `ppt_outline`。

## 标准字段白名单

| 位置 | 仅允许的字段 / 类型 |
| --- | --- |
| 根对象 | `ppt_outline` |
| `ppt_outline` | `cover`、`table_of_contents`、`parts`、`end_page`，四个字段均保留 |
| 有效 `cover` | `title`、`sub_title`、`content` |
| 有效 `table_of_contents` / `end_page` | `title`、`content` |
| `parts[]` | `part_title`、`pages` |
| `parts[].pages[]` | `title`、`content` |
| 所有 `content` | 字符串数组；无展示内容时为 `[]` |

`title`、`sub_title`、`part_title` 均为字符串。有效页面的 `title`、有效章节的 `part_title` 不得为空；无副标题时 `sub_title` 为 `""`。

不在上述白名单中的字段不得进入展示文件，包括 `schema_version`、`metadata`、`part`、`id`、`page_number`、`type`、`key_message`、`source`、`assets`、`notes`、`issues` 及 `kind`、`text`、`level`、`emphasis`、`children` 等节点属性。

## 完整标准结构与单页规则

用户给出的标准结构可以表达整套演示稿；本技能仍按此前约定逐页输出。因此，每个文件保留四个标准分支，但**只允许一个分支承载一个页面**：

- 封面：`cover` 有值；`table_of_contents`、`end_page` 为 `null`；`parts` 为 `[]`。
- 目录：`table_of_contents` 有值；另外两个对象为 `null`；`parts` 为 `[]`。
- 正文、问题、原文总结或作业：`parts` 恰好包含一个章节，章节的 `pages` 恰好包含一页；其余三个对象为 `null`。
- 用户要求的额外结束页：`end_page` 有值；另外两个对象为 `null`；`parts` 为 `[]`。

`null` 和空数组只表示本页没有对应分支，不创建空白页。不要把封面、目录和多个正文页放进同一组标签，也不要照抄示例中的空标题占位页。

## 单页示例

封面 `page-001.json`：

```json
{
  "ppt_outline": {
    "cover": {
      "title": "螺旋式迭代的系统",
      "sub_title": "目标、反馈与底层原理",
      "content": []
    },
    "table_of_contents": null,
    "parts": [],
    "end_page": null
  }
}
```

目录 `page-002.json`：

```json
{
  "ppt_outline": {
    "cover": null,
    "table_of_contents": {
      "title": "目录",
      "content": ["为什么没有稳定的进步", "目标与反馈", "长期迭代与行动"]
    },
    "parts": [],
    "end_page": null
  }
}
```

正文单页示例：

```json
{
  "ppt_outline": {
    "cover": null,
    "table_of_contents": null,
    "parts": [
      {
        "part_title": "三个理论",
        "pages": [
          {
            "title": "峰终定律，容易遗忘痛苦的感受",
            "content": ["近视度数加深换眼镜", "节假日堵车没赶上火车"]
          }
        ]
      }
    ],
    "end_page": null
  }
}
```

仅在用户要求额外结束页时输出：

```json
{
  "ppt_outline": {
    "cover": null,
    "table_of_contents": null,
    "parts": [],
    "end_page": {
      "title": "抓住失败的机会，升级为经验",
      "content": []
    }
  }
}
```

以上文字仅示范数据形状，不加入用户文章没有的论点或页面。

## 字符串内容、层级与附件

- 简单要点直接写成字符串，与用户标准示例一致。
- 有层级时可写 `"## 二级标题"`、`"### 三级标题"`、`"- 要点"`、`"  - 子要点"`；按原文层级和阅读顺序排列。
- 重点可写成 `"**核心词**及其说明"`；连续步骤可写成 `"1. 第一步"`。这些是字符串内容，不是新增 JSON 字段。
- 如需保留精确层级，将节点结构保存到说明文件的 `pages[].content_structure`，通过 `content_index` 绑定展示字符串。
- 普通引文作为展示字符串或说明文件的备注保存，不能误判成附件需求。
- 图片在展示中用字符串说明，例如 `"图片（使用附件中图片：目标与手段）"`；在说明文件 `pages[].asset_refs` 中将该字符串索引绑定到实际附件。避免含糊地让多张图共用一个无法区分的占位说明。
- 图片路径、缺失状态、生成需求、出处和校验问题不混入展示字段；集中保留在说明文件。不要为了精简展示 JSON 而丢失这些信息。

## 标签与文件对应

输出目录中保存 `page-001.json`、`page-002.json`……、`outline.txt` 和一个 `outline-info.json`。

- `outline.txt` 按页码顺序拼接标签块：开始标签独占一行，下一行开始为该页完整 JSON，结束标签独占一行；块之间空一行。
- 每组 `[PPT_OUTLINE]…[/PPT_OUTLINE]` 只包裹一个上述标准对象，不添加整份大纲的外层标签。
- `page-NNN.json` 保存对应标签内的完整对象，不含标签或 Markdown 围栏。
- 序列化单页对象一次，将同一份 UTF-8、2 空格缩进的内容写入展示文件及汇总块。
- 只有独占一行的标签是分隔符；JSON 字符串中的标签字样不作为边界。
- 文件名编号等于说明文件中该页的 `page_number`；补零宽度为 `max(3, 总页数的十进制位数)`，全套一致。
- `outline-info.json` 不加标签，不计入页数，也不嵌入任何 `page-*.json`。

校验标签块数、展示文件数、说明文件的页面记录数与 `metadata.slide_count` 一致；再核对每组标签的内容与单页文件相同、每页只有一个有效分支，以及所有字段符合白名单。
