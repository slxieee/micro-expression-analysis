#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频片段裁剪工具
根据观点筛选结果，从原视频中裁剪出对应的片段
"""

import os
import json
import argparse
import sys
from pathlib import Path
import subprocess

class VideoClipper:
    def __init__(self, source_video: str, output_dir: str = "output"):
        """
        初始化视频裁剪器
        
        Args:
            source_video: 原视频文件路径
            output_dir: 输出目录
        """
        self.source_video = source_video
        self.output_dir = output_dir
        
        # 检查源视频是否存在
        if not os.path.exists(source_video):
            raise FileNotFoundError(f"源视频文件不存在: {source_video}")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"源视频: {self.source_video}")
        print(f"输出目录: {self.output_dir}")
    
    def clip_video(self, start_time: float, end_time: float, output_filename: str) -> bool:
        """
        裁剪视频片段
        
        Args:
            start_time: 开始时间（秒）
            end_time: 结束时间（秒）
            output_filename: 输出文件名
            
        Returns:
            bool: 是否成功
        """
        try:
            duration = end_time - start_time
            output_path = os.path.join(self.output_dir, output_filename)
            
            # 使用ffmpeg裁剪视频
            cmd = [
                'ffmpeg',
                '-i', self.source_video,
                '-ss', str(start_time),
                '-t', str(duration),
                '-c', 'copy',  # 快速复制，不重新编码
                '-avoid_negative_ts', 'make_zero',
                '-y',  # 覆盖输出文件
                output_path
            ]
            
            print(f"正在裁剪: {output_filename} ({start_time:.2f}s - {end_time:.2f}s)")
            
            # 执行命令
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ 成功生成: {output_filename}")
                return True
            else:
                print(f"❌ 裁剪失败: {output_filename}")
                print(f"错误信息: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 裁剪视频时发生错误: {e}")
            return False
    
    def process_result_json(self, result_file: str) -> bool:
        """
        处理观点筛选结果文件
        
        Args:
            result_file: 结果JSON文件路径
            
        Returns:
            bool: 是否成功处理
        """
        try:
            print(f"读取结果文件: {result_file}")
            with open(result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            sentences = data.get("sentences", [])
            if not sentences:
                print("结果文件中没有找到句子数据")
                return False
            
            print(f"找到 {len(sentences)} 个观点片段，开始裁剪...")
            
            success_count = 0
            total_count = len(sentences)
            
            for sentence in sentences:
                sentence_id = sentence.get("id")
                start_time = sentence.get("start_time")
                end_time = sentence.get("end_time")
                
                if sentence_id is None or start_time is None or end_time is None:
                    print(f"⚠️  跳过无效数据: {sentence}")
                    continue
                
                output_filename = f"{sentence_id}.mp4"
                
                if self.clip_video(start_time, end_time, output_filename):
                    success_count += 1
            
            print(f"\n📊 裁剪统计:")
            print(f"  总片段数: {total_count}")
            print(f"  成功裁剪: {success_count}")
            print(f"  失败片段: {total_count - success_count}")
            print(f"  成功率: {success_count/total_count*100:.1f}%")
            
            return success_count > 0
            
        except Exception as e:
            print(f"处理结果文件时发生错误: {e}")
            return False


def check_ffmpeg():
    """检查ffmpeg是否安装"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ffmpeg 已安装")
            return True
        else:
            print("❌ ffmpeg 未正确安装")
            return False
    except FileNotFoundError:
        print("❌ 未找到 ffmpeg，请先安装 ffmpeg")
        print("安装方法:")
        print("  Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg")
        print("  CentOS/RHEL: sudo yum install ffmpeg")
        print("  macOS: brew install ffmpeg")
        return False


def main():
    parser = argparse.ArgumentParser(description="视频片段裁剪工具")
    parser.add_argument("result_file", help="观点筛选结果JSON文件路径")
    parser.add_argument("-v", "--video", 
                       default="test.mp4",
                       help="源视频文件路径（默认: test.mp4）")
    parser.add_argument("-o", "--output", 
                       default="output",
                       help="输出目录（默认: output）")
    
    args = parser.parse_args()
    
    # 检查ffmpeg
    if not check_ffmpeg():
        sys.exit(1)
    
    # 检查输入文件
    if not os.path.exists(args.result_file):
        print(f"结果文件不存在: {args.result_file}")
        sys.exit(1)
    
    try:
        # 创建视频裁剪器
        clipper = VideoClipper(args.video, args.output)
        
        # 处理结果文件
        success = clipper.process_result_json(args.result_file)
        
        if success:
            print("\n🎉 视频裁剪完成！")
        else:
            print("\n❌ 视频裁剪失败！")
            sys.exit(1)
            
    except Exception as e:
        print(f"程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
