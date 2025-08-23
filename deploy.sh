#!/bin/bash
# Gemini视频分析工具 - GitHub部署脚本

set -e

echo "=== Gemini视频分析工具 - GitHub部署脚本 ==="
echo

# 检查是否在git仓库中
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
    echo "Git仓库初始化完成"
else
    echo "检测到现有Git仓库"
fi

echo

# 添加所有文件
echo "添加文件到Git..."
git add .

# 检查是否有变更
if git diff --cached --quiet; then
    echo "没有检测到文件变更"
else
    echo "提交变更..."
    git commit -m "feat: 添加命令行版本和GitHub Actions支持
    
- 新增cli_analyzer.py命令行工具
- 添加GitHub Actions工作流
- 支持参数化视频分析
- 完善部署文档和项目结构"
    echo "变更提交完成"
fi

echo
echo "=== 部署完成 ==="
echo
echo "接下来的步骤："
echo "1. 在GitHub上创建新仓库 'gemini-video-analyzer'"
echo "2. 添加远程仓库："
echo "   git remote add origin https://github.com/your-username/gemini-video-analyzer.git"
echo "3. 推送代码："
echo "   git branch -M main"
echo "   git push -u origin main"
echo "4. 在GitHub仓库设置中添加Secret："
echo "   - GOOGLE_AI_API_KEY: 你的Google AI API密钥"
echo "5. 在Actions页面手动触发工作流进行视频分析"
echo
echo "命令行使用示例："
echo "python3 cli_analyzer.py --prompt '分析视频内容' --youtube 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'"
echo