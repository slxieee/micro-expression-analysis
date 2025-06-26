#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境测试脚本
检查视频转文字工具所需的依赖是否正确安装
"""

import sys
import subprocess
from importlib import import_module

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    version = sys.version_info
    print(f"  Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ❌ 警告: 建议使用Python 3.8或更高版本")
        return False
    else:
        print("  ✅ Python版本符合要求")
        return True

def check_ffmpeg():
    """检查FFmpeg是否安装"""
    print("\n检查FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ {version_line}")
            return True
        else:
            print("  ❌ FFmpeg未正确安装")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ❌ FFmpeg未安装或不在PATH中")
        return False

def check_python_dependencies():
    """检查Python依赖包"""
    print("\n检查Python依赖包...")
    
    dependencies = [
        ('whisper', 'OpenAI Whisper'),
        ('moviepy', 'MoviePy'),
        ('torch', 'PyTorch'),
        ('torchaudio', 'TorchAudio'),
        ('pydub', 'PyDub'),
        ('ffmpeg', 'FFmpeg-Python')
    ]
    
    all_good = True
    
    for module, name in dependencies:
        try:
            mod = import_module(module)
            version = getattr(mod, '__version__', 'unknown')
            print(f"  ✅ {name}: {version}")
        except ImportError:
            print(f"  ❌ {name}: 未安装")
            all_good = False
    
    return all_good

def check_torch_cuda():
    """检查PyTorch CUDA支持"""
    print("\n检查CUDA支持...")
    try:
        import torch
        print(f"  PyTorch版本: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"  ✅ CUDA可用")
            print(f"  GPU数量: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
        else:
            print("  ⚠️  CUDA不可用，将使用CPU（处理速度较慢）")
        
        return True
    except ImportError:
        print("  ❌ PyTorch未安装")
        return False

def test_whisper_model():
    """测试Whisper模型加载"""
    print("\n测试Whisper模型加载...")
    try:
        import whisper
        
        print("  正在加载tiny模型进行测试...")
        model = whisper.load_model("tiny")
        print("  ✅ Whisper模型加载成功")
        
        # 测试模型可用的语言
        print("  支持的语言包括: zh (中文), en (英文) 等")
        return True
        
    except Exception as e:
        print(f"  ❌ Whisper模型加载失败: {e}")
        return False

def provide_installation_help():
    """提供安装帮助信息"""
    print("\n" + "="*50)
    print("安装帮助")
    print("="*50)
    
    print("\n如果检测到问题，请按以下步骤解决:")
    
    print("\n1. 安装FFmpeg:")
    print("   Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
    print("   CentOS/RHEL: sudo yum install ffmpeg")
    print("   或使用conda: conda install ffmpeg")
    
    print("\n2. 安装Python依赖:")
    print("   pip install -r requirements.txt")
    print("   或运行安装脚本: ./install.sh")
    
    print("\n3. 如果需要GPU加速:")
    print("   安装CUDA版本的PyTorch:")
    print("   访问 https://pytorch.org/ 获取适合你系统的安装命令")
    
    print("\n4. 测试工具:")
    print("   python3 video_to_text.py --help")

def main():
    """主测试函数"""
    print("视频转文字工具环境检测")
    print("="*30)
    
    results = []
    
    # 执行各项检查
    results.append(check_python_version())
    results.append(check_ffmpeg())
    results.append(check_python_dependencies())
    results.append(check_torch_cuda())
    results.append(test_whisper_model())
    
    # 总结结果
    print("\n" + "="*30)
    print("检测结果总结")
    print("="*30)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ 所有检查通过 ({passed}/{total})")
        print("环境配置正确，可以开始使用视频转文字工具！")
        print("\n使用示例:")
        print("  python3 video_to_text.py your_video.mp4")
    else:
        print(f"❌ 部分检查失败 ({passed}/{total})")
        print("请根据上述提示解决问题后重新运行检测")
        provide_installation_help()

if __name__ == "__main__":
    main()
