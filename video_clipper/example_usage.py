#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频裁剪示例脚本
快速裁剪观点片段
"""

import os
import sys
from video_clipper import VideoClipper

def main():
    # 配置文件路径
    result_file = "../select_opinion/result.json"  # 观点筛选结果
    source_video = "../video_to_text/test.mp4"    # 源视频文件
    output_dir = "clips"                          # 输出目录
    
    print("🎬 观点视频片段裁剪工具")
    print("=" * 40)
    
    # 检查文件是否存在
    if not os.path.exists(result_file):
        print(f"❌ 观点筛选结果文件不存在: {result_file}")
        print("请先运行观点筛选工具生成 result.json 文件")
        sys.exit(1)
    
    if not os.path.exists(source_video):
        print(f"❌ 源视频文件不存在: {source_video}")
        print("请确保 test.mp4 文件存在")
        sys.exit(1)
    
    try:
        # 创建视频裁剪器
        clipper = VideoClipper(source_video, output_dir)
        
        # 处理结果文件
        success = clipper.process_result_json(result_file)
        
        if success:
            print(f"\n🎉 所有观点视频片段已保存到: {output_dir}/")
            print("\n生成的文件:")
            if os.path.exists(output_dir):
                files = sorted([f for f in os.listdir(output_dir) if f.endswith('.mp4')])
                for i, file in enumerate(files, 1):
                    print(f"  {i}. {file}")
        else:
            print("\n❌ 视频裁剪失败！")
            
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
