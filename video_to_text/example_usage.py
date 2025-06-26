#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频转文字示例脚本
演示如何使用 VideoToTextConverter 类
"""

import os
from pathlib import Path
from video_to_text import VideoToTextConverter

def example_usage():
    """示例使用方法"""
    
    # 示例视频文件路径（请替换为你的实际视频文件路径）
    video_path = "example_video.mp4"
    
    # 检查示例视频是否存在
    if not os.path.exists(video_path):
        print(f"示例视频文件不存在: {video_path}")
        print("请将你的MP4视频文件重命名为 'example_video.mp4' 或修改脚本中的路径")
        return
    
    print("开始视频转文字处理...")
    print(f"输入视频: {video_path}")
    
    # 创建转换器实例
    # 可选模型: "tiny", "base", "small", "medium", "large"
    # tiny: 最快但精度最低
    # base: 平衡速度和精度（推荐）
    # large: 最高精度但速度较慢
    converter = VideoToTextConverter(model_size="base")
    
    # 设置输出目录
    output_dir = "./output"
    
    # 执行转换
    # 支持的输出格式: ["json", "txt", "srt"]
    success = converter.convert_video_to_text(
        video_path=video_path,
        output_dir=output_dir,
        output_formats=["json", "txt", "srt"]  # 生成所有格式
    )
    
    if success:
        print("\n🎉 转换成功完成！")
        print(f"输出文件保存在: {output_dir}")
        
        # 列出生成的文件
        video_name = Path(video_path).stem
        output_files = [
            f"{video_name}_transcript.json",
            f"{video_name}_transcript.txt", 
            f"{video_name}_transcript.srt"
        ]
        
        print("\n生成的文件:")
        for file in output_files:
            file_path = os.path.join(output_dir, file)
            if os.path.exists(file_path):
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} (未生成)")
                
    else:
        print("\n❌ 转换失败，请检查错误信息")

def batch_process_example():
    """批量处理示例"""
    print("\n" + "="*50)
    print("批量处理示例")
    print("="*50)
    
    # 视频文件目录
    video_dir = "./videos"
    output_dir = "./batch_output"
    
    if not os.path.exists(video_dir):
        print(f"视频目录不存在: {video_dir}")
        print("请创建 './videos' 目录并放入MP4文件")
        return
    
    # 查找所有MP4文件
    video_files = list(Path(video_dir).glob("*.mp4"))
    
    if not video_files:
        print(f"在 {video_dir} 目录中未找到MP4文件")
        return
    
    print(f"找到 {len(video_files)} 个视频文件")
    
    # 创建转换器
    converter = VideoToTextConverter(model_size="base")
    
    # 批量处理
    success_count = 0
    for video_file in video_files:
        print(f"\n处理: {video_file.name}")
        
        success = converter.convert_video_to_text(
            video_path=str(video_file),
            output_dir=output_dir,
            output_formats=["json", "txt"]
        )
        
        if success:
            success_count += 1
            print(f"✅ {video_file.name} 处理完成")
        else:
            print(f"❌ {video_file.name} 处理失败")
    
    print(f"\n批量处理完成: {success_count}/{len(video_files)} 个文件成功")

if __name__ == "__main__":
    print("视频转文字工具示例")
    print("="*30)
    
    # 单个文件处理示例
    example_usage()
    
    # 批量处理示例
    batch_process_example()
    
    print("\n使用提示:")
    print("1. 确保已安装所有依赖: pip install -r requirements.txt")
    print("2. 确保系统已安装 FFmpeg")
    print("3. 首次运行会下载Whisper模型，需要网络连接")
    print("4. 可以通过命令行直接使用: python video_to_text.py your_video.mp4")
