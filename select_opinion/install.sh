#!/bin/bash
# 观点筛选工具安装脚本

echo "开始安装观点筛选工具依赖..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "当前Python版本: $python_version"

# 检查是否有pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: pip3 未安装，请先安装pip3"
    exit 1
fi

# 升级pip
echo "升级pip..."
pip3 install --upgrade pip

# 安装依赖
echo "安装Python依赖..."
pip3 install -r requirements.txt

# 检查安装结果
echo "检查依赖安装..."
python3 -c "
try:
    import openai
    import requests
    print('✅ 所有依赖安装成功')
except ImportError as e:
    print(f'❌ 依赖安装失败: {e}')
    exit(1)
"

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  基本用法: python3 opinion_selector.py transcript.json"
echo "  指定模型: python3 opinion_selector.py transcript.json -m deepseek"
echo "  模拟模式: python3 opinion_selector.py transcript.json --mock"
echo ""
echo "配置说明:"
echo "  1. 复制 .env.template 为 .env"
echo "  2. 在 .env 文件中填入API密钥"
echo "  3. 或通过环境变量设置: export DEEPSEEK_API_KEY=your_key"
