# 视频转文字工具使用指南

输入命令：python3 video_to_text.py test.mp4 --min-duration 10.0 --max-gap 3.0 -f json txt

## 快速开始

### 1. 运行环境检测
```bash
python3 test_environment.py
```
这会检查所有依赖是否正确安装。

### 2. 基本使用
```bash
# 转换单个视频文件
python3 video_to_text.py your_video.mp4

# 查看所有可用选项
python3 video_to_text.py --help
```

### 3. 高级使用
```bash
# 指定输出目录和格式
python3 video_to_text.py video.mp4 -o ./output -f json txt srt

# 使用更大的模型获得更高精度
python3 video_to_text.py video.mp4 -m large

# 完整示例
python3 video_to_text.py /path/to/video.mp4 -o /path/to/output -m medium -f json txt srt
```

## 模型选择指南

| 模型    | 大小    | 速度 | 精度 | 适用场景 |
|---------|---------|------|------|----------|
| tiny    | ~32MB   | 最快 | 一般 | 快速预览 |
| base    | ~74MB   | 快   | 好   | 日常使用（推荐） |
| small   | ~244MB  | 中等 | 很好 | 高质量要求 |
| medium  | ~769MB  | 慢   | 优秀 | 专业用途 |
| large   | ~1550MB | 最慢 | 最佳 | 最高精度要求 |

## 输出格式对比

### JSON格式
- 结构化数据，包含完整时间戳信息
- 适合程序化处理
- 可以轻松提取特定时间段的文字

### TXT格式
- 纯文本格式，易于阅读
- 包含时间戳，方便查找
- 适合人工审阅

### SRT格式
- 标准字幕格式
- 可直接用于视频播放器
- 适合制作字幕文件


## 常见用例

### 视频会议记录
```bash
python3 video_to_text.py meeting.mp4 -m base -f txt srt
```

### 讲座/课程视频
```bash
python3 video_to_text.py lecture.mp4 -m medium -f json txt
```

### 快速预览
```bash
python3 video_to_text.py video.mp4 -m tiny -f txt
```

