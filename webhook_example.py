#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Webhook使用示例
演示如何使用GeminiVideoAnalyzer的webhook功能
"""

import os
from gemini_video_analyzer import GeminiVideoAnalyzer

def main():
    """主函数"""
    print("=== Gemini视频分析工具 - Webhook示例 ===")
    
    # 获取API密钥
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        print("错误: 请设置GOOGLE_AI_API_KEY环境变量")
        return
    
    # 初始化分析器
    analyzer = GeminiVideoAnalyzer(api_key)
    
    # 示例1: 分析YouTube视频并发送到webhook
    print("\n=== 示例1: YouTube视频分析 + Webhook ===")
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # 示例链接
    webhook_url = "https://webhook.site/your-unique-url"  # 替换为你的webhook地址
    prompt = "请描述这个视频的主要内容和亮点"
    
    print(f"视频链接: {youtube_url}")
    print(f"Webhook地址: {webhook_url}")
    print(f"提示词: {prompt}")
    print("\n开始分析...")
    
    result = analyzer.analyze_youtube_video(
        prompt=prompt,
        youtube_url=youtube_url,
        webhook_url=webhook_url
    )
    
    print("\n分析完成!")
    print("结果已同时显示在控制台和发送到webhook")
    print(f"\n分析结果:\n{result}")
    
    # 示例2: 不使用webhook的普通分析
    print("\n\n=== 示例2: 普通分析（无Webhook） ===")
    result2 = analyzer.analyze_youtube_video(
        prompt="简单描述视频内容",
        youtube_url=youtube_url
        # 不传递webhook_url参数
    )
    
    print(f"普通分析结果:\n{result2}")
    
    print("\n=== 示例完成 ===")
    print("\n注意事项:")
    print("1. 请将webhook_url替换为你的实际webhook地址")
    print("2. 可以使用 https://webhook.site 来测试webhook功能")
    print("3. webhook会接收到包含分析结果的JSON数据")
    print("4. JSON数据格式包含: type, prompt, video_url, model, result, timestamp")

if __name__ == "__main__":
    main()