# Gemini视频分析工具

一个基于Google Gemini AI的YouTube视频分析工具，专门用于分析科技类视频内容，提供结构化的分析报告。

## 🚀 主要功能

- **内置专业提示词**：集成了专门的YouTube科技视频分析专家提示词
- **多种触发方式**：支持命令行、GitHub Actions手动触发和HTTP API触发
- **结构化输出**：生成包含赞助信息、量化分析、内容摘要等维度的Markdown报告
- **灵活配置**：支持自定义提示词和webhook推送

## 📋 分析维度

### 1. 赞助信息分析
- 判断视频的商业合作性质
- 识别明确赞助、潜在合作或无赞助情况

### 2. 核心量化分析
- 品牌/产品提及时长统计
- 视频占比计算
- 好感度评分（1-5分）
- 正负面观点总结

### 3. 内容摘要与分类
- 视频类型识别
- 内容简介生成
- KOL情感倾向分析
- 关键引述摘录

### 4. 详细评测维度分析
- 设计外观、屏幕、性能等维度评价
- 产品对比分析
- 生态系统评估

## 🛠️ 安装和配置

### 1. 环境要求
- Python 3.7+
- Google AI API密钥

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置API密钥
创建 `.env` 文件并添加：
```
GOOGLE_AI_API_KEY=your_api_key_here
```

## 📖 使用方法

### 1. 命令行使用

#### 使用默认提示词（推荐）
```bash
# 分析YouTube视频
python3 cli_analyzer.py --youtube "https://www.youtube.com/watch?v=VIDEO_ID"

# 分析本地视频文件
python3 cli_analyzer.py --local "/path/to/video.mp4"

# 分析网络视频链接
python3 cli_analyzer.py --url "https://example.com/video.mp4"
```

#### 使用自定义提示词
```bash
python3 cli_analyzer.py --prompt "你的自定义提示词" --youtube "VIDEO_URL"
```

#### 配置webhook推送
```bash
python3 cli_analyzer.py --youtube "VIDEO_URL" --webhook "https://your-webhook-url.com"
```

### 2. GitHub Actions使用

#### 手动触发
1. 访问仓库的Actions页面
2. 选择 "Deploy Gemini Video Analyzer" 工作流
3. 点击 "Run workflow" 并填入参数：
   - `prompt`（可选）：自定义提示词
   - `video_type`：选择 `youtube`、`local` 或 `url`
   - `video_input`：视频链接或文件路径
   - `webhook_url`（可选）：结果推送地址

#### HTTP API触发
详细说明请查看 [HTTP_TRIGGER_GUIDE.md](HTTP_TRIGGER_GUIDE.md) 文件。

**快速示例：**
```bash
curl -X POST \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/dispatches" \
  -d '{
    "event_type": "analyze_video",
    "client_payload": {
      "video_type": "youtube",
      "video_input": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
  }'
```

### 3. Python代码集成

```python
from gemini_video_analyzer import GeminiVideoAnalyzer

# 初始化分析器
analyzer = GeminiVideoAnalyzer(api_key="your_api_key")

# 使用默认提示词分析
result = analyzer.analyze_youtube_video("https://www.youtube.com/watch?v=VIDEO_ID")

# 使用自定义提示词分析
result = analyzer.analyze_youtube_video(
    "https://www.youtube.com/watch?v=VIDEO_ID",
    prompt="你的自定义提示词"
)

print(result)
```

## 🔧 配置选项

### 环境变量
- `GOOGLE_AI_API_KEY`：Google AI API密钥（必需）
- `GEMINI_MODEL`：使用的模型名称（默认：gemini-1.5-flash）

### GitHub Secrets
在GitHub仓库设置中添加以下Secrets：
- `GOOGLE_AI_API_KEY`：你的Google AI API密钥

### Personal Access Token（HTTP触发需要）
1. 访问 GitHub Settings > Developer settings > Personal access tokens
2. 创建新token，至少需要 `repo` 权限
3. 在HTTP请求中使用该token进行认证

## 📁 项目结构

```
.
├── gemini_video_analyzer.py    # 核心分析器类
├── cli_analyzer.py             # 命令行工具
├── example.py                  # 使用示例
├── deploy.sh                   # 部署脚本
├── requirements.txt            # 依赖包列表
├── .github/workflows/
│   └── deploy.yml             # GitHub Actions工作流
├── HTTP_TRIGGER_GUIDE.md       # HTTP触发详细指南
└── README.md                   # 项目说明文档
```

## 🎯 输出格式

分析结果以结构化的Markdown格式输出，包含：

```markdown
# YouTube 视频分析报告

### **1. 赞助信息分析**
- **判断结果**: [明确赞助/可能存在合作/无明显赞助]
- **判断依据**: [具体依据]

### **2. 核心量化分析**
| 提及的品牌/产品 | 提及总时长 (秒) | 视频占比 (%) | 好感度评分 (1-5) | 核心观点 |

### **3. 内容摘要与分类**
- **视频类型**: [类型]
- **内容简介**: [简介]
- **KOL 总体情感倾向**: [倾向]
- **关键引述**: [引述]

### **4. 详细评测维度分析**
[各维度详细分析]
```

## 🚀 部署到GitHub

1. 运行部署脚本：
```bash
bash deploy.sh
```

2. 按照脚本提示完成GitHub仓库设置

3. 配置必要的Secrets和Personal Access Token

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

## 🔗 相关链接

- [Google AI Studio](https://aistudio.google.com/)
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [Gemini API文档](https://ai.google.dev/docs)