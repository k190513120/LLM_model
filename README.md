# Gemini 2.5 Pro 视频分析工具

这是一个基于Google Gemini 2.5 Pro模型的智能视频分析工具，支持分析YouTube视频和本地视频文件。

## 功能特性

- 🎥 **YouTube视频分析**: 直接输入YouTube链接进行视频内容分析
- 📁 **本地视频支持**: 上传本地视频文件进行分析
- 💻 **命令行工具**: 支持命令行模式使用
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

### 使用方法

1. 运行命令行工具:
```bash
python gemini_video_analyzer.py
```

2. 按照提示输入API密钥和选择分析模式

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

## 项目结构

```
海外大模型/
├── gemini_video_analyzer.py    # 命令行工具
├── example.py                  # 使用示例
├── requirements.txt           # 项目依赖
└── README.md                 # 项目说明
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

### v1.0.0
- 初始版本发布
- 支持YouTube视频分析
- 支持本地视频文件分析
- 提供Web界面和命令行工具