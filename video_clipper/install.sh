#!/bin/bash

echo "🎬 视频裁剪工具安装脚本"
echo "========================"

# 检查操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        echo "检测到 Ubuntu/Debian 系统"
        echo "正在安装 ffmpeg..."
        sudo apt update
        sudo apt install -y ffmpeg
    elif command -v yum &> /dev/null; then
        echo "检测到 CentOS/RHEL 系统"
        echo "正在安装 ffmpeg..."
        sudo yum install -y epel-release
        sudo yum install -y ffmpeg
    elif command -v dnf &> /dev/null; then
        echo "检测到 Fedora 系统"
        echo "正在安装 ffmpeg..."
        sudo dnf install -y ffmpeg
    else
        echo "未识别的 Linux 发行版，请手动安装 ffmpeg"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "检测到 macOS 系统"
    if command -v brew &> /dev/null; then
        echo "正在通过 Homebrew 安装 ffmpeg..."
        brew install ffmpeg
    else
        echo "请先安装 Homebrew，然后运行: brew install ffmpeg"
        exit 1
    fi
else
    echo "未支持的操作系统: $OSTYPE"
    exit 1
fi

# 验证安装
echo ""
echo "验证 ffmpeg 安装..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg 安装成功！"
    ffmpeg -version | head -1
else
    echo "❌ ffmpeg 安装失败"
    exit 1
fi

echo ""
echo "🎉 安装完成！现在可以使用视频裁剪工具了"
echo ""
echo "使用方法:"
echo "  python video_clipper.py ../select_opinion/result.json -v ../video_to_text/test.mp4"
echo "  或者运行: python example_usage.py"
