#!/bin/bash
#
# 将图片调整为 1284 × 2778px (App Store 截图尺寸)
# 适用于 iPhone 14/15/16 Pro Max 的 App Store 介绍图
#
# 使用方法:
#   ./resize_images_for_appstore.sh [输入图片路径] [输出目录]
#
# 示例:
#   ./resize_images_for_appstore.sh screenshot.png ./output
#   ./resize_images_for_appstore.sh *.png ./appstore_screenshots
#

set -e

# 目标分辨率
TARGET_WIDTH=2048
TARGET_HEIGHT=2732

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo "════════════════════════════════════════════════════════════════"
    echo "📱 App Store 图片调整脚本 - 1284 × 2778px"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "使用方法:"
    echo "  $0 [输入] [输出目录]"
    echo ""
    echo "参数:"
    echo "  输入        - 图片文件、文件夹路径或通配符（如 *.png）"
    echo "  输出目录    - 输出目录（可选，默认为 ./appstore_output）"
    echo ""
    echo "示例:"
    echo "  # 单张图片"
    echo "  $0 screenshot.png"
    echo "  $0 screenshot.png ./output"
    echo ""
    echo "  # 批量处理文件夹内所有 PNG"
    echo "  $0 ../screenshots"
    echo "  $0 ../screenshots ./appstore_output"
    echo ""
    echo "  # 使用通配符"
    echo "  $0 *.png"
    echo "  $0 ../screenshots/*.png ./output"
    echo ""
    echo "输出格式:"
    echo "  文件名格式: [原文件名]_1284x2778.png"
    echo "  分辨率: ${TARGET_WIDTH} × ${TARGET_HEIGHT}px"
    echo ""
}

# 检查依赖
check_dependencies() {
    local missing_deps=()
    
    # 检查 sips (macOS 内置)
    if ! command -v sips &> /dev/null; then
        missing_deps+=("sips (macOS 内置工具)")
    fi
    
    # 检查 ImageMagick (可选，但推荐)
    if ! command -v convert &> /dev/null; then
        echo -e "${YELLOW}⚠️  未找到 ImageMagick，将使用 macOS 内置的 sips 工具${NC}"
        echo "   提示: 安装 ImageMagick 可获得更好的图片质量"
        echo "   安装: brew install imagemagick"
        echo ""
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo -e "${RED}❌ 缺少依赖:${NC}"
        for dep in "${missing_deps[@]}"; do
            echo "   - $dep"
        done
        exit 1
    fi
}

# 使用 sips 调整图片 (macOS 内置)
resize_with_sips() {
    local input_file="$1"
    local output_file="$2"
    
    echo -e "${BLUE}📐 使用 sips 调整图片...${NC}"
    
    # sips 调整大小（保持宽高比，填充到目标尺寸）
    sips -z "$TARGET_HEIGHT" "$TARGET_WIDTH" "$input_file" --out "$output_file" 2>/dev/null || {
        # 如果失败，尝试先缩放再裁剪
        local temp_file="${output_file}.temp"
        
        # 计算缩放比例（取较大的比例以确保填满）
        local input_width=$(sips -g pixelWidth "$input_file" | tail -1 | awk '{print $2}')
        local input_height=$(sips -g pixelHeight "$input_file" | tail -1 | awk '{print $2}')
        
        local scale_w=$(echo "scale=10; $TARGET_WIDTH / $input_width" | bc)
        local scale_h=$(echo "scale=10; $TARGET_HEIGHT / $input_height" | bc)
        local scale=$(echo "scale=10; if ($scale_w > $scale_h) $scale_w else $scale_h" | bc)
        
        local new_width=$(echo "scale=0; $input_width * $scale / 1" | bc)
        local new_height=$(echo "scale=0; $input_height * $scale / 1" | bc)
        
        # 缩放
        sips -z "$new_height" "$new_width" "$input_file" --out "$temp_file"
        
        # 裁剪到目标尺寸（居中）
        local crop_x=$(( (new_width - TARGET_WIDTH) / 2 ))
        local crop_y=$(( (new_height - TARGET_HEIGHT) / 2 ))
        
        sips -c "$TARGET_HEIGHT" "$TARGET_WIDTH" "$temp_file" --cropOffset "$crop_y" "$crop_x" --out "$output_file"
        rm -f "$temp_file"
    }
}

# 使用 ImageMagick 调整图片（更高质量）
resize_with_imagemagick() {
    local input_file="$1"
    local output_file="$2"
    
    echo -e "${BLUE}📐 使用 ImageMagick 调整图片...${NC}"
    
    # 使用 ImageMagick 的高质量缩放
    convert "$input_file" \
        -resize "${TARGET_WIDTH}x${TARGET_HEIGHT}^" \
        -gravity center \
        -extent "${TARGET_WIDTH}x${TARGET_HEIGHT}" \
        -quality 95 \
        "$output_file"
}

# 处理单张图片
process_image() {
    local input_file="$1"
    local output_dir="$2"
    
    # 检查输入文件是否存在
    if [ ! -f "$input_file" ]; then
        echo -e "${RED}❌ 文件不存在: $input_file${NC}"
        return 1
    fi
    
    # 获取文件名（不含路径和扩展名）
    local filename=$(basename "$input_file")
    local name_without_ext="${filename%.*}"
    local extension="${filename##*.}"
    
    # 生成输出文件名
    local output_file="${output_dir}/${name_without_ext}_${TARGET_WIDTH}x${TARGET_HEIGHT}.${extension}"
    
    echo ""
    echo "────────────────────────────────────────────────────────────"
    echo -e "${GREEN}处理图片: $filename${NC}"
    echo "  输入: $input_file"
    echo "  输出: $output_file"
    
    # 获取原始尺寸
    if command -v sips &> /dev/null; then
        local orig_width=$(sips -g pixelWidth "$input_file" | tail -1 | awk '{print $2}')
        local orig_height=$(sips -g pixelHeight "$input_file" | tail -1 | awk '{print $2}')
        echo "  原始尺寸: ${orig_width} × ${orig_height}px"
    fi
    echo "  目标尺寸: ${TARGET_WIDTH} × ${TARGET_HEIGHT}px"
    
    # 选择调整方法
    if command -v convert &> /dev/null; then
        resize_with_imagemagick "$input_file" "$output_file"
    else
        resize_with_sips "$input_file" "$output_file"
    fi
    
    if [ -f "$output_file" ]; then
        echo -e "${GREEN}✅ 成功: $output_file${NC}"
        
        # 显示输出文件信息
        if command -v sips &> /dev/null; then
            local out_width=$(sips -g pixelWidth "$output_file" | tail -1 | awk '{print $2}')
            local out_height=$(sips -g pixelHeight "$output_file" | tail -1 | awk '{print $2}')
            local file_size=$(ls -lh "$output_file" | awk '{print $5}')
            echo "  实际尺寸: ${out_width} × ${out_height}px"
            echo "  文件大小: $file_size"
        fi
        return 0
    else
        echo -e "${RED}❌ 失败: 无法创建输出文件${NC}"
        return 1
    fi
}

# 主函数
main() {
    # 显示帮助
    if [ "$1" == "-h" ] || [ "$1" == "--help" ] || [ $# -eq 0 ]; then
        show_help
        if [ $# -eq 0 ]; then
            exit 0
        fi
    fi
    
    # 检查依赖
    check_dependencies
    
    # 解析参数
    local input_pattern="$1"
    local output_dir="${2:-./appstore_output}"
    
    # 创建输出目录
    mkdir -p "$output_dir"
    
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo -e "${GREEN}📱 App Store 图片调整工具${NC}"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "目标分辨率: ${TARGET_WIDTH} × ${TARGET_HEIGHT}px"
    echo "输出目录: $output_dir"
    echo ""
    
    # 处理输入（支持文件夹、通配符、单文件）
    local processed=0
    local failed=0
    
    # 检查输入类型
    if [ -d "$input_pattern" ]; then
        # 文件夹模式：处理文件夹内所有 PNG 图片
        echo -e "${BLUE}📁 检测到文件夹，将处理所有 PNG 图片${NC}"
        echo ""
        
        local folder_path="$input_pattern"
        local png_files=$(find "$folder_path" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \))
        
        if [ -z "$png_files" ]; then
            echo -e "${RED}❌ 错误: 文件夹中没有找到图片文件 (PNG/JPG)${NC}"
            exit 1
        fi
        
        local file_count=$(echo "$png_files" | wc -l | tr -d ' ')
        echo "找到 $file_count 张图片，开始处理..."
        echo ""
        
        while IFS= read -r file; do
            if [ -f "$file" ]; then
                if process_image "$file" "$output_dir"; then
                    ((processed++))
                else
                    ((failed++))
                fi
            fi
        done <<< "$png_files"
        
    elif [[ "$input_pattern" == *"*"* ]]; then
        # 通配符模式
        for file in $input_pattern; do
            if [ -f "$file" ]; then
                if process_image "$file" "$output_dir"; then
                    ((processed++))
                else
                    ((failed++))
                fi
            fi
        done
    else
        # 单个文件
        if [ -f "$input_pattern" ]; then
            if process_image "$input_pattern" "$output_dir"; then
                ((processed++))
            else
                ((failed++))
            fi
        else
            echo -e "${RED}❌ 错误: 文件或文件夹不存在: $input_pattern${NC}"
            exit 1
        fi
    fi
    
    # 显示总结
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    if [ $processed -gt 0 ]; then
        echo -e "${GREEN}✅ 完成！${NC}"
        echo "  成功处理: $processed 张图片"
        if [ $failed -gt 0 ]; then
            echo -e "  ${RED}失败: $failed 张图片${NC}"
        fi
        echo "  输出目录: $output_dir"
    else
        echo -e "${RED}❌ 没有处理任何图片${NC}"
        exit 1
    fi
    echo "════════════════════════════════════════════════════════════════"
    echo ""
}

# 运行主函数
main "$@"

