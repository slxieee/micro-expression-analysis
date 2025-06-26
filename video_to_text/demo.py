#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试用的音频文件和演示脚本
由于没有真实的MP4视频文件，我们创建一个包含中文语音的示例音频文件进行测试
"""

import os
import sys
from pathlib import Path

def create_sample_audio():
    """创建一个示例音频文件用于测试"""
    print("由于没有真实的MP4视频文件，这里提供几种测试方法：")
    print("\n方法1: 使用你自己的MP4视频文件")
    print("  将你的MP4文件放在当前目录，然后运行：")
    print("  python3 video_to_text.py your_video.mp4")
    
    print("\n方法2: 下载示例视频进行测试")
    print("  你可以从以下来源获取测试视频：")
    print("  - YouTube上的中文视频（使用yt-dlp下载）")
    print("  - 录制一段包含中文语音的短视频")
    print("  - 使用手机录制几句中文对话")
    
    print("\n方法3: 使用命令行工具创建测试视频")
    print("  如果有ffmpeg，可以创建一个包含音频的测试文件：")
    print("  ffmpeg -f lavfi -i 'sine=frequency=1000:duration=5' -ac 2 test_audio.wav")

def demo_usage():
    """演示工具的使用方法"""
    print("\n" + "="*60)
    print("视频转文字工具演示")
    print("="*60)
    
    # 检查是否有MP4文件
    mp4_files = list(Path('.').glob('*.mp4'))
    
    if mp4_files:
        print(f"发现 {len(mp4_files)} 个MP4文件:")
        for i, file in enumerate(mp4_files, 1):
            print(f"  {i}. {file.name}")
        
        try:
            choice = int(input(f"\n请选择要处理的文件 (1-{len(mp4_files)}): ")) - 1
            if 0 <= choice < len(mp4_files):
                selected_file = mp4_files[choice]
                process_video_demo(str(selected_file))
            else:
                print("无效的选择")
        except (ValueError, KeyboardInterrupt):
            print("\n取消操作")
    else:
        print("当前目录没有找到MP4文件")
        create_sample_audio()

def process_video_demo(video_path):
    """处理视频的演示"""
    print(f"\n开始处理视频: {video_path}")
    
    # 导入转换器
    try:
        from video_to_text import VideoToTextConverter
    except ImportError:
        print("错误: 无法导入 VideoToTextConverter")
        print("请确保 video_to_text.py 文件存在")
        return
    
    # 询问用户选择模型
    models = {
        '1': 'tiny',
        '2': 'base', 
        '3': 'small',
        '4': 'medium',
        '5': 'large'
    }
    
    print("\n选择Whisper模型:")
    print("1. tiny   (最快，精度一般)")
    print("2. base   (推荐，平衡速度和精度)")
    print("3. small  (较好精度)")
    print("4. medium (高精度)")
    print("5. large  (最高精度，最慢)")
    
    try:
        model_choice = input("请选择模型 (1-5, 默认为2): ").strip()
        if not model_choice:
            model_choice = '2'
        
        if model_choice in models:
            model_size = models[model_choice]
        else:
            print("无效选择，使用默认的base模型")
            model_size = 'base'
    except KeyboardInterrupt:
        print("\n取消操作")
        return
    
    # 询问输出格式
    print("\n选择输出格式:")
    print("1. JSON + TXT (推荐)")
    print("2. 所有格式 (JSON + TXT + SRT)")
    print("3. 仅JSON")
    print("4. 仅TXT")
    print("5. 仅SRT")
    
    format_choices = {
        '1': ['json', 'txt'],
        '2': ['json', 'txt', 'srt'],
        '3': ['json'],
        '4': ['txt'],
        '5': ['srt']
    }
    
    try:
        format_choice = input("请选择输出格式 (1-5, 默认为1): ").strip()
        if not format_choice:
            format_choice = '1'
        
        if format_choice in format_choices:
            output_formats = format_choices[format_choice]
        else:
            print("无效选择，使用默认格式")
            output_formats = ['json', 'txt']
    except KeyboardInterrupt:
        print("\n取消操作")
        return
    
    # 设置输出目录
    output_dir = "./output"
    
    print(f"\n配置信息:")
    print(f"  输入文件: {video_path}")
    print(f"  模型大小: {model_size}")
    print(f"  输出格式: {', '.join(output_formats)}")
    print(f"  输出目录: {output_dir}")
    
    try:
        confirm = input("\n是否开始处理? (y/n): ").lower().strip()
        if confirm != 'y':
            print("取消处理")
            return
    except KeyboardInterrupt:
        print("\n取消操作")
        return
    
    # 创建转换器并处理
    try:
        print(f"\n正在初始化 {model_size} 模型...")
        converter = VideoToTextConverter(model_size=model_size)
        
        print("开始处理视频...")
        success = converter.convert_video_to_text(
            video_path=video_path,
            output_dir=output_dir,
            output_formats=output_formats
        )
        
        if success:
            print("\n🎉 处理完成！")
            print(f"输出文件保存在: {output_dir}")
            
            # 显示生成的文件
            video_name = Path(video_path).stem
            print("\n生成的文件:")
            for fmt in output_formats:
                filename = f"{video_name}_transcript.{fmt}"
                filepath = os.path.join(output_dir, filename)
                if os.path.exists(filepath):
                    file_size = os.path.getsize(filepath)
                    print(f"  ✅ {filename} ({file_size} bytes)")
                    
                    # 如果是txt文件，显示部分内容
                    if fmt == 'txt' and file_size > 0:
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()[:200]
                                print(f"     预览: {content}...")
                        except:
                            pass
        else:
            print("\n❌ 处理失败！请检查错误信息")
            
    except Exception as e:
        print(f"\n❌ 处理过程中发生错误: {e}")

def show_help():
    """显示帮助信息"""
    print("视频转文字工具演示脚本")
    print("\n使用方法:")
    print("  python3 demo.py")
    print("\n功能:")
    print("  1. 自动检测当前目录的MP4文件")
    print("  2. 交互式选择处理参数")
    print("  3. 演示完整的转换流程")
    print("\n准备工作:")
    print("  1. 将要处理的MP4视频文件放在当前目录")
    print("  2. 确保已安装所有依赖 (运行 test_environment.py 检查)")
    print("  3. 确保网络连接正常 (首次使用需要下载模型)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        show_help()
    else:
        demo_usage()
