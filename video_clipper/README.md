# 视频片段裁剪工具

根据观点筛选结果，从原视频中自动裁剪出对应的观点片段。

## 功能特点

- 🎬 自动从原视频裁剪观点片段
- 📝 基于观点筛选结果的时间戳
- ⚡ 使用ffmpeg快速裁剪（不重新编码）
- 📁 自动生成有序的视频文件

## 安装依赖

### 自动安装
```bash
./install.sh
```

### 手动安装ffmpeg
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install epel-release
sudo yum install ffmpeg

# macOS
brew install ffmpeg
```

## 使用方法

### 方法1：使用主程序
```bash
python video_clipper.py result.json -v source_video.mp4 -o output_dir
```

参数说明：
- `result.json`: 观点筛选结果文件路径
- `-v`: 源视频文件路径（默认: test.mp4）
- `-o`: 输出目录（默认: output）

### 方法2：使用示例脚本
```bash
python example_usage.py
```

这会自动：
- 读取 `../select_opinion/result.json`
- 使用 `../video_to_text/test.mp4` 作为源视频
- 输出到 `clips/` 目录

## 输出结果

程序会根据观点筛选结果中的每个句子ID生成对应的视频片段：

```
clips/
├── 2.mp4    # ID为2的观点片段
├── 3.mp4    # ID为3的观点片段
├── 5.mp4    # ID为5的观点片段
├── 8.mp4    # ID为8的观点片段
├── 12.mp4   # ID为12的观点片段
└── ...
```

每个视频片段包含：
- 对应观点的完整时间段
- 原视频的画质和音质
- 精确的开始和结束时间

## 工作原理

1. 读取观点筛选结果JSON文件
2. 提取每个观点的时间信息（start_time, end_time）
3. 使用ffmpeg从原视频中裁剪对应时间段
4. 按照观点ID命名保存视频文件

## 示例

假设观点筛选结果包含以下片段：
```json
{
  "id": 22,
  "start_time": 936.8,
  "end_time": 978.22,
  "text": "我个人觉得白酒一定会是整个消费..."
}
```

程序会生成 `22.mp4`，包含从 936.8秒 到 978.22秒 的视频片段。

## 注意事项

- 确保源视频文件存在且可访问
- 需要足够的磁盘空间存储裁剪后的视频
- ffmpeg必须正确安装并在PATH中
- 视频裁剪使用复制模式，速度快但需要原视频格式支持

## 错误处理

程序会自动处理常见错误：
- 源视频文件不存在
- ffmpeg未安装
- 无效的时间戳数据
- 输出目录创建失败

失败的片段会被跳过，成功的片段正常保存。
