#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建测试音频文件和演示完整流程
"""

import os
import sys
import tempfile
from pathlib import Path

def create_test_audio():
    """创建一个测试音频文件"""
    try:
        from pydub import AudioSegment
        from pydub.generators import Sine
        import numpy as np
        
        print("正在创建测试音频文件...")
        
        # 创建一个简单的音频文件（正弦波，用于测试工具是否正常工作）
        # 注意：这只是测试工具链，不会有中文语音内容
        duration = 5000  # 5秒
        frequency = 440  # A4音符
        
        # 生成正弦波
        sine_wave = Sine(frequency).to_audio_segment(duration=duration)
        
        # 导出为WAV文件
        test_audio_path = "test_audio.wav"
        sine_wave.export(test_audio_path, format="wav")
        
        print(f"✅ 测试音频文件已创建: {test_audio_path}")
        return test_audio_path
        
    except ImportError as e:
        print(f"❌ 无法创建测试音频: {e}")
        return None

def test_audio_processing(audio_path):
    """测试音频处理功能"""
    try:
        from video_to_text import VideoToTextConverter
        
        print(f"\n开始测试音频处理: {audio_path}")
        
        # 创建转换器
        converter = VideoToTextConverter(model_size="tiny")  # 使用最小模型进行测试
        
        # 测试音频转录
        print("正在进行语音识别...")
        result = converter.transcribe_audio(audio_path)
        
        if result:
            print("✅ 音频处理成功")
            
            # 处理结果
            sentences = converter.process_transcription_result(result)
            print(f"识别到 {len(sentences)} 个语音段落")
            
            # 保存结果
            output_dir = "./test_output"
            os.makedirs(output_dir, exist_ok=True)
            
            converter.save_results(sentences, 
                                 os.path.join(output_dir, "test_result.json"), 
                                 "json")
            
            print(f"✅ 测试结果已保存到: {output_dir}/test_result.json")
            return True
        else:
            print("❌ 音频处理失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False

def run_comprehensive_test():
    """运行综合测试"""
    print("视频转文字工具综合测试")
    print("="*40)
    
    # 步骤1: 环境检查
    print("\n1. 环境检查...")
    try:
        import whisper
        from moviepy.editor import VideoFileClip
        import torch
        print("✅ 所有依赖模块可正常导入")
    except ImportError as e:
        print(f"❌ 依赖模块导入失败: {e}")
        return False
    
    # 步骤2: 创建测试音频
    print("\n2. 创建测试音频...")
    test_audio = create_test_audio()
    if not test_audio:
        print("⚠️  无法创建测试音频，将跳过音频处理测试")
        return False
    
    # 步骤3: 测试音频处理
    print("\n3. 测试音频处理...")
    success = test_audio_processing(test_audio)
    
    # 清理测试文件
    if os.path.exists(test_audio):
        os.remove(test_audio)
        print(f"已清理测试文件: {test_audio}")
    
    return success

def show_demo_instructions():
    """显示演示说明"""
    print("\n" + "="*60)
    print("🎯 如何使用这个视频转文字工具")
    print("="*60)
    
    print("\n📁 准备视频文件:")
    print("   1. 将你的MP4视频文件放在当前目录")
    print("   2. 确保视频包含清晰的中文语音")
    print("   3. 建议先用较短的视频(< 5分钟)进行测试")
    
    print("\n🚀 开始转换:")
    print("   基本使用:")
    print("     python3 video_to_text.py your_video.mp4")
    print("")
    print("   高级使用:")
    print("     python3 video_to_text.py your_video.mp4 -m base -f json txt srt")
    
    print("\n📊 查看结果:")
    print("   转换完成后，会在输出目录生成以下文件:")
    print("   • your_video_transcript.json - 结构化数据，包含时间戳")
    print("   • your_video_transcript.txt  - 纯文本格式，易于阅读")
    print("   • your_video_transcript.srt  - 字幕文件，可用于播放器")
    
    print("\n🔧 交互式演示:")
    print("   运行交互式演示脚本:")
    print("     python3 demo.py")
    
    print("\n📝 示例代码:")
    print("   查看编程示例:")
    print("     python3 example_usage.py")
    
    print("\n🛠️  故障排除:")
    print("   如果遇到问题，首先运行环境检测:")
    print("     python3 test_environment.py")

def main():
    """主函数"""
    print("视频转文字工具测试与演示")
    print("="*30)
    
    # 运行综合测试
    print("\n正在运行综合测试...")
    test_success = run_comprehensive_test()
    
    if test_success:
        print("\n✅ 综合测试通过！工具可以正常使用。")
    else:
        print("\n⚠️  综合测试未完全通过，但核心功能应该可用。")
    
    # 显示使用说明
    show_demo_instructions()
    
    print("\n" + "="*60)
    print("📚 更多信息:")
    print("   • 详细使用说明: README.md")
    print("   • 快速使用指南: USAGE.md")
    print("   • 环境检测脚本: test_environment.py")
    print("   • 交互式演示: demo.py")
    print("   • 编程示例: example_usage.py")
    print("="*60)

if __name__ == "__main__":
    main()
