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
    git commit -m "feat: 更新视频分析工具，支持默认prompt和HTTP触发
    
- 添加默认的YouTube科技视频分析提示词
- 支持通过HTTP请求触发GitHub Actions
- 更新命令行工具，prompt参数变为可选
- 完善API接口和错误处理
- 添加HTTP触发使用指南"
    echo "变更提交完成"
fi

echo
echo "=== 部署完成 ==="
echo
echo "接下来的步骤："
echo "1. 在GitHub上创建新仓库或推送到现有仓库"
echo "2. 添加远程仓库（如果尚未添加）："
echo "   git remote add origin https://github.com/your-username/your-repo-name.git"
echo "3. 推送代码："
echo "   git branch -M main"
echo "   git push -u origin main"
echo "4. 在GitHub仓库设置中添加Secret："
echo "   - GOOGLE_AI_API_KEY: 你的Google AI API密钥"
echo "5. 创建GitHub Personal Access Token（用于HTTP触发）"
echo "   - 访问 Settings > Developer settings > Personal access tokens"
echo "   - 创建token，至少需要 'repo' 权限"
echo
echo "=== 使用方法 ==="
echo
echo "1. 命令行使用（使用默认YouTube科技视频分析提示词）："
echo "   python3 cli_analyzer.py --youtube 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'"
echo
echo "2. 命令行使用（自定义提示词）："
echo "   python3 cli_analyzer.py --prompt '分析视频内容' --youtube 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'"
echo
echo "3. GitHub Actions手动触发："
echo "   - 访问仓库的Actions页面"
echo "   - 选择 'Deploy Gemini Video Analyzer' 工作流"
echo "   - 点击 'Run workflow' 并填入参数"
echo
echo "4. HTTP API触发："
echo "   详细说明请查看 HTTP_TRIGGER_GUIDE.md 文件"
echo
echo "=== 新功能特性 ==="
echo "✓ 内置YouTube科技视频分析专家提示词"
echo "✓ 支持HTTP请求触发GitHub Actions"
echo "✓ 命令行prompt参数变为可选"
echo "✓ 完善的错误处理和API接口"
echo "✓ 支持webhook结果推送"
echo