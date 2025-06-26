#!/bin/bash
# 视频转文字工具安装脚本

echo "开始安装视频转文字工具依赖..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "当前Python版本: $python_version"

# 检查是否有pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: pip3 未安装，请先安装pip3"
    exit 1
fi

# 检查FFmpeg
echo "检查FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "警告: FFmpeg未安装"
    echo "请安装FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg"
    echo "  CentOS/RHEL: sudo yum install ffmpeg"
    echo "  或使用conda: conda install ffmpeg"
    read -p "是否继续安装Python依赖? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ FFmpeg已安装"
fi

# 升级pip
echo "升级pip..."
pip3 install --upgrade pip

# 安装依赖
echo "安装Python依赖..."
pip3 install -r requirements.txt

# 检查torch是否支持CUDA
echo "检查CUDA支持..."
python3 -c "
import torch
print(f'PyTorch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA设备数量: {torch.cuda.device_count()}')
    print(f'当前CUDA设备: {torch.cuda.get_device_name(0)}')
else:
    print('将使用CPU进行处理（速度较慢）')
"

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  基本用法: python3 video_to_text.py your_video.mp4"
echo "  查看帮助: python3 video_to_text.py --help"
echo "  运行示例: python3 example_usage.py"
echo ""
echo "注意事项:"
echo "  1. 首次运行会下载Whisper模型，需要网络连接"
echo "  2. 模型大小约几十MB到1.5GB不等"
echo "  3. 建议先用短视频测试效果"
