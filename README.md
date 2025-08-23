# Gemini 2.5 Pro 视频分析工具

这是一个基于Google Gemini 2.5 Pro模型的智能视频分析工具，支持分析YouTube视频和本地视频文件。

## 功能特性

- 🎥 **YouTube视频分析**: 直接输入YouTube链接进行视频内容分析
- 📁 **本地视频支持**: 上传本地视频文件进行分析
- 💻 **命令行工具**: 支持命令行模式使用
- 🔗 **Webhook支持**: 分析结果可自动发送到指定的webhook地址
- 🤖 **智能分析**: 基于Gemini 2.5 Pro的强大视频理解能力

## 安装依赖

```bash
pip install -r requirements.txt
```

## 获取API密钥

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 创建新的API密钥
3. 复制密钥备用

## 使用方法

### 交互式使用

1. 运行程序：
```bash
python gemini_video_analyzer.py
```

2. 选择分析模式：
   - 输入 `1` 分析YouTube视频
   - 输入 `2` 分析本地视频文件
   - 输入 `3` 退出程序

3. 根据提示输入相应信息：
   - YouTube链接或本地文件路径
   - 分析提示词
   - 是否使用webhook（可选）

### 命令行使用

使用 `cli_analyzer.py` 进行命令行操作：

#### 分析YouTube视频
```bash
# 基本使用
python cli_analyzer.py --prompt "请分析这个视频的主要内容" --youtube "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 使用webhook
python cli_analyzer.py --prompt "总结视频要点" --youtube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --webhook "https://webhook.site/your-id"

# 指定模型
python cli_analyzer.py --prompt "分析视频" --youtube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --model "gemini-2.5-flash"
```

#### 分析本地视频
```bash
# 分析本地视频文件
python cli_analyzer.py --prompt "分析这个视频" --local "/path/to/video.mp4" --webhook "https://your-webhook.com/endpoint"
```

#### 命令行参数说明
- `--prompt, -p`: 分析提示词（必需）
- `--youtube, -y`: YouTube视频链接
- `--local, -l`: 本地视频文件路径
- `--webhook, -w`: Webhook地址（可选）
- `--model, -m`: 使用的模型名称（默认: gemini-2.0-flash-exp）
- `--api-key, -k`: Google AI API密钥（可选，优先使用环境变量）
- `--help, -h`: 显示帮助信息

### Webhook功能

Webhook功能允许将分析结果自动发送到指定的HTTP端点，适用于集成到其他系统或自动化工作流程中。

#### Webhook数据格式

发送到webhook的JSON数据包含以下字段:

```json
{
  "type": "youtube_video_analysis",  // 或 "local_video_analysis"
  "prompt": "用户输入的提示词",
  "video_url": "视频链接",  // YouTube分析时
  "video_path": "视频路径",  // 本地视频分析时
  "model": "gemini-2.0-flash-exp",
  "result": "AI分析结果文本",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

#### 错误情况

如果分析过程中出现错误，webhook将接收包含错误信息的数据:

```json
{
  "type": "youtube_video_analysis",
  "prompt": "用户输入的提示词",
  "video_url": "视频链接",
  "model": "gemini-2.0-flash-exp",
  "error": "错误信息",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

#### 编程方式使用Webhook

```python
from gemini_video_analyzer import GeminiVideoAnalyzer

analyzer = GeminiVideoAnalyzer(api_key="your-api-key")

# 分析YouTube视频并发送到webhook
result = analyzer.analyze_youtube_video(
    prompt="描述视频内容",
    youtube_url="https://www.youtube.com/watch?v=example",
    webhook_url="https://your-webhook-url.com/endpoint"
)

# 分析本地视频并发送到webhook
result = analyzer.analyze_local_video(
    prompt="分析视频场景",
    video_path="/path/to/video.mp4",
    webhook_url="https://your-webhook-url.com/endpoint"
)
```

## 环境变量配置（可选）

为了避免每次都输入API密钥，可以设置环境变量:

```bash
export GOOGLE_AI_API_KEY="your-api-key-here"
```

## 支持的视频格式

### YouTube视频
- 支持标准YouTube链接格式
- 示例: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

### 本地视频文件
- MP4 (.mp4)
- MOV (.mov)
- AVI (.avi)
- MKV (.mkv)
- WebM (.webm)

## 提示词示例

以下是一些有效的分析提示词示例:

### 基础分析
- "请描述这个视频的主要内容"
- "总结视频中的关键信息"
- "分析视频的主题和要点"

### 详细分析
- "详细描述视频中的场景、人物和动作"
- "分析视频的情感色彩和氛围"
- "识别视频中的文字和标识"

### 专业分析
- "从教育角度分析这个视频的价值"
- "评估视频的制作质量和技术特点"
- "分析视频中的商业元素和营销策略"

## GitHub部署

### 1. 克隆或Fork项目
```bash
git clone https://github.com/your-username/gemini-video-analyzer.git
cd gemini-video-analyzer
```

### 2. 设置GitHub Secrets
在GitHub仓库设置中添加以下Secret：
- `GOOGLE_AI_API_KEY`: 你的Google AI API密钥

### 3. 使用GitHub Actions

#### 手动触发视频分析
1. 进入GitHub仓库的Actions页面
2. 选择"Deploy Gemini Video Analyzer"工作流
3. 点击"Run workflow"
4. 输入参数：
   - **prompt**: 分析提示词
   - **youtube_url**: YouTube视频链接
   - **webhook_url**: Webhook地址（可选）
5. 点击"Run workflow"开始分析

#### 自动触发
- 推送代码到main/master分支时自动运行测试
- Pull Request时自动运行测试

## 项目结构

```
gemini-video-analyzer/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions工作流
├── gemini_video_analyzer.py    # 主程序文件
├── cli_analyzer.py             # 命令行版本
├── example.py                  # 使用示例
├── webhook_example.py          # Webhook功能示例
├── requirements.txt            # 依赖包列表
├── .gitignore                  # Git忽略文件
└── README.md                   # 项目说明文档
```

## 注意事项

1. **API配额**: Google AI API有使用配额限制，请合理使用
2. **视频大小**: 本地视频文件建议小于100MB
3. **网络连接**: 分析YouTube视频需要稳定的网络连接
4. **隐私保护**: 请勿上传包含敏感信息的视频

## 故障排除

### 常见错误

1. **API密钥无效**
   - 检查API密钥是否正确
   - 确认API密钥已启用Gemini API访问权限

2. **YouTube视频无法访问**
   - 确认视频链接格式正确
   - 检查视频是否为公开状态
   - 确认网络连接正常

3. **本地视频上传失败**
   - 检查视频文件格式是否支持
   - 确认文件大小不超过限制
   - 检查文件路径是否正确

### 获取帮助

如果遇到问题，请检查:
1. Python版本 (推荐3.8+)
2. 依赖包是否正确安装
3. API密钥权限设置
4. 网络连接状态

## 技术说明

本工具基于以下技术构建:
- **Google Gemini 2.5 Pro**: 提供强大的视频理解能力
- **Flask**: Web框架，提供用户界面
- **Google AI Python SDK**: 官方Python SDK

## 更新日志

### v1.2.0
- 新增命令行版本 `cli_analyzer.py`，支持参数化调用
- 添加GitHub Actions工作流，支持自动化部署和测试
- 支持通过GitHub Actions手动触发视频分析
- 完善项目结构，添加.gitignore和部署文档
- 修复YouTube视频分析API格式问题

### v1.1.0
- 新增Webhook功能支持
- 分析结果可自动发送到指定HTTP端点
- 支持成功和错误状态的webhook通知
- 添加webhook使用示例和文档
- 优化错误处理机制

### v1.0.0
- 初始版本发布
- 支持YouTube视频分析
- 支持本地视频文件分析
- 提供交互式命令行工具