#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频语音转文字工具
功能：从MP4视频文件中提取语音，转换为中文文字，并保留时间戳
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
import whisper
from moviepy.editor import VideoFileClip
import torch

class VideoToTextConverter:
    def __init__(self, model_size: str = "base"):
        """
        初始化视频转文字转换器
        
        Args:
            model_size: Whisper模型大小 ("tiny", "base", "small", "medium", "large")
        """
        self.model_size = model_size
        self.model = None
        self.load_model()
    
    def load_model(self):
        """加载Whisper模型"""
        try:
            print(f"正在加载 Whisper {self.model_size} 模型...")
            self.model = whisper.load_model(self.model_size)
            print("模型加载完成")
        except Exception as e:
            print(f"模型加载失败: {e}")
            sys.exit(1)
    
    def extract_audio_from_video(self, video_path: str, audio_path: str) -> bool:
        """
        从视频文件中提取音频
        
        Args:
            video_path: 视频文件路径
            audio_path: 输出音频文件路径
            
        Returns:
            bool: 是否成功提取音频
        """
        try:
            print(f"正在从视频文件提取音频: {video_path}")
            
            # 加载视频文件
            video = VideoFileClip(video_path)
            
            # 提取音频
            audio = video.audio
            
            # 保存为WAV格式（Whisper支持的格式）
            audio.write_audiofile(audio_path, verbose=False, logger=None)
            
            # 清理资源
            audio.close()
            video.close()
            
            print(f"音频提取完成: {audio_path}")
            return True
            
        except Exception as e:
            print(f"音频提取失败: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        使用Whisper转录音频为文字
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            Dict: 包含转录结果和时间戳的字典
        """
        try:
            print("正在进行语音识别...")
            
            # 使用Whisper进行转录，指定中文
            result = self.model.transcribe(
                audio_path, 
                language="zh",  # 指定中文
                word_timestamps=True,  # 启用词级时间戳
                verbose=False
            )
            
            print("语音识别完成")
            return result
            
        except Exception as e:
            print(f"语音识别失败: {e}")
            return {}
    
    def format_timestamp(self, seconds: float) -> str:
        """
        将秒数转换为时间戳格式 (HH:MM:SS.mmm)
        
        Args:
            seconds: 秒数
            
        Returns:
            str: 格式化的时间戳
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def process_transcription_result(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        处理转录结果，提取句子和时间戳
        
        Args:
            result: Whisper转录结果
            
        Returns:
            List[Dict]: 包含句子和时间戳的列表
        """
        sentences = []
        
        if "segments" in result:
            for segment in result["segments"]:
                sentence_data = {
                    "id": segment.get("id", 0),
                    "text": segment.get("text", "").strip(),
                    "start_time": segment.get("start", 0),
                    "end_time": segment.get("end", 0),
                    "start_timestamp": self.format_timestamp(segment.get("start", 0)),
                    "end_timestamp": self.format_timestamp(segment.get("end", 0)),
                    "duration": segment.get("end", 0) - segment.get("start", 0)
                }
                
                if sentence_data["text"]:  # 只添加非空文本
                    sentences.append(sentence_data)
        
        return sentences
    
    def merge_short_sentences(self, sentences: List[Dict[str, Any]], 
                            min_duration: float = 8.0, 
                            max_gap: float = 2.0) -> List[Dict[str, Any]]:
        """
        合并较短的句子，创建更长的段落
        
        Args:
            sentences: 原始句子列表
            min_duration: 最小段落持续时间（秒）
            max_gap: 句子间最大间隔时间（秒），超过此间隔不合并
            
        Returns:
            List[Dict]: 合并后的句子列表
        """
        if not sentences:
            return sentences
        
        merged_sentences = []
        current_sentence = None
        
        for sentence in sentences:
            if current_sentence is None:
                # 第一个句子
                current_sentence = sentence.copy()
            else:
                # 检查是否应该合并
                gap = sentence["start_time"] - current_sentence["end_time"]
                current_duration = current_sentence["end_time"] - current_sentence["start_time"]
                
                # 合并条件：
                # 1. 当前段落持续时间小于最小要求 或
                # 2. 句子间隔小于最大允许间隔 且 当前段落不太长（避免过长）
                should_merge = (
                    current_duration < min_duration or 
                    (gap <= max_gap and current_duration < min_duration * 2)
                )
                
                if should_merge:
                    # 合并句子
                    current_sentence["text"] += sentence["text"]
                    current_sentence["end_time"] = sentence["end_time"]
                    current_sentence["end_timestamp"] = sentence["end_timestamp"]
                    current_sentence["duration"] = (
                        current_sentence["end_time"] - current_sentence["start_time"]
                    )
                else:
                    # 不合并，保存当前句子并开始新的句子
                    merged_sentences.append(current_sentence)
                    current_sentence = sentence.copy()
        
        # 添加最后一个句子
        if current_sentence is not None:
            merged_sentences.append(current_sentence)
        
        # 重新编号
        for i, sentence in enumerate(merged_sentences):
            sentence["id"] = i
        
        return merged_sentences
    
    def save_results(self, sentences: List[Dict[str, Any]], output_path: str, format_type: str = "json"):
        """
        保存转录结果到文件
        
        Args:
            sentences: 句子列表
            output_path: 输出文件路径
            format_type: 输出格式 ("json", "txt", "srt")
        """
        try:
            if format_type.lower() == "json":
                self.save_as_json(sentences, output_path)
            elif format_type.lower() == "txt":
                self.save_as_txt(sentences, output_path)
            elif format_type.lower() == "srt":
                self.save_as_srt(sentences, output_path)
            else:
                print(f"不支持的输出格式: {format_type}")
                
        except Exception as e:
            print(f"保存文件失败: {e}")
    
    def save_as_json(self, sentences: List[Dict[str, Any]], output_path: str):
        """保存为JSON格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "total_sentences": len(sentences),
                "sentences": sentences
            }, f, ensure_ascii=False, indent=2)
        print(f"结果已保存为JSON格式: {output_path}")
    
    def save_as_txt(self, sentences: List[Dict[str, Any]], output_path: str):
        """保存为TXT格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("视频语音转文字结果\n")
            f.write("=" * 50 + "\n\n")
            
            for sentence in sentences:
                f.write(f"[{sentence['start_timestamp']} --> {sentence['end_timestamp']}]\n")
                f.write(f"{sentence['text']}\n\n")
        
        print(f"结果已保存为TXT格式: {output_path}")
    
    def save_as_srt(self, sentences: List[Dict[str, Any]], output_path: str):
        """保存为SRT字幕格式"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, sentence in enumerate(sentences, 1):
                # SRT格式时间戳 (HH:MM:SS,mmm)
                start_time = sentence['start_timestamp'].replace('.', ',')
                end_time = sentence['end_timestamp'].replace('.', ',')
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{sentence['text']}\n\n")
        
        print(f"结果已保存为SRT格式: {output_path}")
    
    def convert_video_to_text(self, video_path: str, output_dir: str = None, 
                            output_formats: List[str] = None, 
                            min_duration: float = 8.0, 
                            max_gap: float = 2.0, 
                            merge_sentences: bool = True) -> bool:
        """
        完整的视频转文字流程
        
        Args:
            video_path: 视频文件路径
            output_dir: 输出目录
            output_formats: 输出格式列表
            min_duration: 最小段落持续时间（秒）
            max_gap: 句子间最大合并间隔（秒）
            merge_sentences: 是否合并短句子
            
        Returns:
            bool: 是否成功完成转换
        """
        if output_formats is None:
            output_formats = ["json", "txt"]
        
        # 检查视频文件是否存在
        if not os.path.exists(video_path):
            print(f"视频文件不存在: {video_path}")
            return False
        
        # 设置输出目录
        if output_dir is None:
            output_dir = os.path.dirname(video_path)
            # 如果视频文件在当前目录，dirname会返回空字符串，设置为当前目录
            if not output_dir:
                output_dir = "."
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成临时音频文件路径
        video_name = Path(video_path).stem
        audio_path = os.path.join(output_dir, f"{video_name}_temp_audio.wav")
        
        try:
            # 步骤1: 提取音频
            if not self.extract_audio_from_video(video_path, audio_path):
                return False
            
            # 步骤2: 语音识别
            result = self.transcribe_audio(audio_path)
            if not result:
                return False
            
            # 步骤3: 处理结果
            sentences = self.process_transcription_result(result)
            if not sentences:
                print("未识别到任何文字内容")
                return False
            
            print(f"原始识别到 {len(sentences)} 个语句")
            
            # 步骤3.5: 合并短句子
            if merge_sentences:
                merged_sentences = self.merge_short_sentences(sentences, min_duration, max_gap)
                print(f"合并后得到 {len(merged_sentences)} 个段落")
                final_sentences = merged_sentences
            else:
                print("跳过句子合并")
                final_sentences = sentences
            
            # 步骤4: 保存结果
            for format_type in output_formats:
                if format_type.lower() == "json":
                    output_path = os.path.join(output_dir, f"{video_name}_transcript.json")
                elif format_type.lower() == "txt":
                    output_path = os.path.join(output_dir, f"{video_name}_transcript.txt")
                elif format_type.lower() == "srt":
                    output_path = os.path.join(output_dir, f"{video_name}_transcript.srt")
                else:
                    continue
                
                self.save_results(final_sentences, output_path, format_type)
            
            return True
            
        finally:
            # 清理临时音频文件
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print("已清理临时音频文件")


def main():
    parser = argparse.ArgumentParser(description="从MP4视频文件中提取语音并转换为中文文字")
    parser.add_argument("video_path", help="输入视频文件路径")
    parser.add_argument("-o", "--output", help="输出目录（默认为视频文件所在目录）")
    parser.add_argument("-m", "--model", choices=["tiny", "base", "small", "medium", "large"], 
                       default="base", help="Whisper模型大小（默认: base）")
    parser.add_argument("-f", "--formats", nargs="+", choices=["json", "txt", "srt"], 
                       default=["json", "txt"], help="输出格式（默认: json txt）")
    parser.add_argument("--min-duration", type=float, default=20.0,
                       help="最小段落持续时间（秒），默认: 20.0")
    parser.add_argument("--max-gap", type=float, default=3.0,
                       help="句子间最大合并间隔（秒），默认: 3.0")
    parser.add_argument("--no-merge", action="store_true",
                       help="禁用句子合并，保留原始短句子")
    
    args = parser.parse_args()
    
    # 创建转换器
    converter = VideoToTextConverter(model_size=args.model)
    
    # 执行转换
    success = converter.convert_video_to_text(
        video_path=args.video_path,
        output_dir=args.output,
        output_formats=args.formats,
        min_duration=args.min_duration,
        max_gap=args.max_gap,
        merge_sentences=not args.no_merge
    )
    
    if success:
        print("\n视频转文字完成！")
    else:
        print("\n视频转文字失败！")
        sys.exit(1)


if __name__ == "__main__":
    main()
