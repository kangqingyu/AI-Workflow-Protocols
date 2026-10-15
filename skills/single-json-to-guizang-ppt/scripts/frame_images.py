#!/usr/bin/env python3
"""
CleanShot X 风格配图画框合成脚本 (16:10 / 1600x1000)
将原稿配图与 guizang-ppt-skill 内置背景图合成为带白色内衬、圆角与柔和投影的演示配图。

用法示例:
  python3 frame_images.py \
    --input /path/to/pictures/source.png \
    --output /path/to/ppt/images/01-framed.jpg \
    --bg /Users/kqy/.gemini/config/skills/guizang-ppt-skill/assets/backgrounds/warm_01.jpg
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


DEFAULT_BG_DIR = Path("/Users/kqy/.gemini/config/skills/guizang-ppt-skill/assets/backgrounds")


def center_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    w, h = img.size
    target_ratio = target_w / target_h
    src_ratio = w / h
    if src_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)


def make_rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def frame_image(
    src_path: Path,
    bg_path: Path,
    out_path: Path,
    canvas_w: int = 1600,
    canvas_h: int = 1000,
    pad_ratio: float = 0.84,
    radius: int = 24,
) -> None:
    bg = Image.open(bg_path).convert("RGBA")
    canvas = center_crop(bg, canvas_w, canvas_h)

    fg_raw = Image.open(src_path).convert("RGBA")
    card_w = int(canvas_w * pad_ratio)
    card_h = int(canvas_h * pad_ratio)

    # 白色圆角卡片基底，确保任意比例或透明背景的原稿配图都干净利落
    card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 255))

    inner_pad = 36
    avail_w = card_w - inner_pad * 2
    avail_h = card_h - inner_pad * 2
    fw, fh = fg_raw.size
    scale = min(avail_w / fw, avail_h / fh)
    new_fw = max(1, int(fw * scale))
    new_fh = max(1, int(fh * scale))
    fg_resized = fg_raw.resize((new_fw, new_fh), Image.Resampling.LANCZOS)

    fx = (card_w - new_fw) // 2
    fy = (card_h - new_fh) // 2
    card.paste(fg_resized, (fx, fy), fg_resized)

    # 圆角遮罩
    mask = make_rounded_mask((card_w, card_h), radius=radius)

    # 绘制柔和投影
    shadow_offset = (0, 20)
    shadow_blur = 34
    shadow_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    cx = (canvas_w - card_w) // 2
    cy = (canvas_h - card_h) // 2
    shadow_box = Image.new("RGBA", (card_w, card_h), (20, 18, 15, 90))
    shadow_layer.paste(shadow_box, (cx + shadow_offset[0], cy + shadow_offset[1]), mask)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur))

    canvas = Image.alpha_composite(canvas, shadow_layer)
    canvas.paste(card, (cx, cy), mask)

    # 细微高光描边增强精致感
    border_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(border_layer)
    draw.rounded_rectangle(
        (cx, cy, cx + card_w - 1, cy + card_h - 1),
        radius=radius,
        outline=(255, 255, 255, 160),
        width=2,
    )
    canvas = Image.alpha_composite(canvas, border_layer)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out_path, "JPEG", quality=92, optimize=True)
    print(f"Framed: {src_path.name} -> {out_path} ({canvas_w}x{canvas_h})")


def main() -> None:
    parser = argparse.ArgumentParser(description="CleanShot X 风格配图合成工具")
    parser.add_argument("--input", required=True, type=Path, help="源图片路径")
    parser.add_argument("--output", required=True, type=Path, help="输出图片路径 (.jpg)")
    parser.add_argument(
        "--bg",
        type=Path,
        default=DEFAULT_BG_DIR / "warm_01.jpg",
        help="背景图片路径（默认使用 guizang-ppt-skill 内置 warm_01.jpg）",
    )
    args = parser.parse_args()
    frame_image(args.input, args.bg, args.output)


if __name__ == "__main__":
    main()
