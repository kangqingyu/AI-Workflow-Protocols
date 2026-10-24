---
name: json-to-svg-ptt20261015
description: 根据 JSON 大纲生成 SVG 格式的 PPT 演示文稿。
---

# JSON 大纲转 SVG 演示文稿

## 核心约束

- 画布固定为 `viewBox="0 0 1280 720"`。
- 每个页面大纲 JSON 单独输出一页 `.svg` 文件；`outline-info.json` 是辅助元数据，不生成页面。
- 保持 JSON 中的正文文字与内容结构，避免添加额外解释；图片提示指令应转化为图片，不作为正文显示。
- 使用内容驱动的 Bento Grid：卡片数量与组合按信息结构决定，用卡片尺寸体现主次，卡片间距至少 `20px`。
- 有图片要求时必须使用原文真实图片，并以 Base64 Data URI 内嵌；最终文件不得保留外部图片路径、未替换的占位符，也不得以手绘或文字占位替代原图。

## 执行流程与按需加载

所有规范路径均相对于本 `SKILL.md` 所在目录。

1. 读取页面大纲；若同目录存在 `outline-info.json`，核对各页的 `asset_refs` 与图片资源信息。
2. 根据用户指定的编号或名称匹配下方风格索引；未指定时使用默认风格。指定风格无法匹配时先澄清，不擅自替换。
3. 生成前必须读取选中风格的规范文件；仅加载这一种风格，不遍历或预读其他风格。同一份演示文稿保持风格一致，除非用户要求切换。
4. 当某页 JSON 包含图片提示（如 `图片（使用附件中图片：xxx）`），或该页 `asset_refs` 非空时，必须读取并执行 [图片内嵌规范](references/image-embedding.md)。没有图片要求时跳过该文件。
5. 按大纲和已加载规范生成各页 SVG，交付前核对画布、文字、布局和输出页数；有图片的页面同时完成图片内嵌校验。

已读取且仍在上下文中的规范可复用，无需逐页重读；需要恢复上下文时只补读当前任务所需规范。

## 风格索引

| 编号 | 名称 / 别名 | 规范文件 |
|---|---|---|
| 1 / 风格一 | Apple 暗黑毛玻璃风 / Dark Glassmorphism（默认） | [apple-dark-glass.md](styles/apple-dark-glass.md) |
| 2 / 风格二 | 圆角立体几何撞色 / Soft 3D Clay & Geometric Color-Blocking | [rounded-3d-colorblock.md](styles/rounded-3d-colorblock.md) |
| 3 / 风格三 | Teenage Engineering 精密工业机能风 / Industrial Retro-Tech | [te-industrial-retro.md](styles/te-industrial-retro.md) |
