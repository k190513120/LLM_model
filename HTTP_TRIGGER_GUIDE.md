# HTTP 触发 GitHub Actions 指南

本指南说明如何通过HTTP请求触发GitHub Actions工作流来分析YouTube视频。

## 前提条件

1. **GitHub Personal Access Token (PAT)**
   - 访问 GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
   - 创建新token，至少需要 `repo` 权限
   - 保存生成的token（格式：`ghp_xxxxxxxxxxxx`）

2. **仓库设置**
   - 确保仓库中已设置 `GOOGLE_AI_API_KEY` secret
   - 工作流文件已正确配置（支持 `repository_dispatch` 事件）

## HTTP 请求格式

### 基本信息
- **URL**: `https://api.github.com/repos/{owner}/{repo}/dispatches`
- **方法**: POST
- **认证**: Bearer Token (GitHub PAT)
- **Content-Type**: application/json

### 请求示例

#### 1. 使用默认提示词分析YouTube视频

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "analyze-video",
    "client_payload": {
      "video_type": "youtube",
      "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
  }' \
  https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO_NAME/dispatches
```

#### 2. 使用自定义提示词分析YouTube视频

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "analyze-video",
    "client_payload": {
      "prompt": "请详细分析这个视频的技术内容和创新点",
      "video_type": "youtube",
      "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
  }' \
  https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO_NAME/dispatches
```

#### 3. 分析网络视频并发送到Webhook

```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "analyze-video",
    "client_payload": {
      "video_type": "network_url",
      "network_url": "https://example.com/video.mp4",
      "webhook_url": "https://webhook.site/your-unique-id"
    }
  }' \
  https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO_NAME/dispatches
```

## 参数说明

### 必需参数
- `event_type`: 固定为 `"analyze-video"`
- `video_type`: 视频类型，可选值：
  - `"youtube"`: YouTube视频
  - `"network_url"`: 网络视频链接

### 可选参数
- `prompt`: 分析提示词（留空使用默认的YouTube科技视频分析提示词）
- `youtube_url`: YouTube视频链接（当video_type为youtube时使用）
- `network_url`: 网络视频链接（当video_type为network_url时使用）
- `webhook_url`: Webhook地址，分析完成后将结果发送到此地址

## 使用JavaScript发送请求

```javascript
const triggerAnalysis = async (params) => {
  const response = await fetch('https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO_NAME/dispatches', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_GITHUB_TOKEN',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      event_type: 'analyze-video',
      client_payload: params
    })
  });
  
  if (response.ok) {
    console.log('工作流已触发');
  } else {
    console.error('触发失败:', await response.text());
  }
};

// 使用示例
triggerAnalysis({
  video_type: 'youtube',
  youtube_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
});
```

## 使用Python发送请求

```python
import requests
import json

def trigger_video_analysis(github_token, repo_owner, repo_name, **params):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/dispatches"
    
    headers = {
        'Authorization': f'Bearer {github_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'event_type': 'analyze-video',
        'client_payload': params
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 204:
        print("工作流已成功触发")
    else:
        print(f"触发失败: {response.status_code} - {response.text}")

# 使用示例
trigger_video_analysis(
    github_token='YOUR_GITHUB_TOKEN',
    repo_owner='YOUR_USERNAME',
    repo_name='YOUR_REPO_NAME',
    video_type='youtube',
    youtube_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'
)
```

## 监控工作流状态

触发工作流后，可以通过以下方式监控执行状态：

1. **GitHub网页界面**
   - 访问仓库的 Actions 标签页
   - 查看最新的工作流运行状态

2. **GitHub API**
   ```bash
   curl -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
        https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO_NAME/actions/runs
   ```

## 注意事项

1. **API限制**: GitHub API有速率限制，请避免频繁触发
2. **Token安全**: 请妥善保管GitHub Personal Access Token
3. **视频格式**: 确保视频链接可访问且格式受支持
4. **Webhook**: 如果使用webhook，确保目标地址可接收POST请求
5. **默认提示词**: 不提供prompt参数时，将使用内置的YouTube科技视频分析提示词

## 故障排除

- **401 Unauthorized**: 检查GitHub Token是否正确且有足够权限
- **404 Not Found**: 检查仓库路径是否正确
- **422 Unprocessable Entity**: 检查请求体格式是否正确
- 工作流不执行: 检查仓库是否有GOOGLE_AI_API_KEY secret配置