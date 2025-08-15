#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 2.5 Pro 视频分析示例
演示如何使用API分析YouTube视频
"""

import os
from google import genai

def analyze_youtube_video_example():
    """YouTube视频分析示例"""
    
    # 设置API密钥 (请替换为您的实际API密钥)
    api_key = os.getenv('GOOGLE_AI_API_KEY') or "YOUR_API_KEY_HERE"
    
    if api_key == "YOUR_API_KEY_HERE":
        print("请设置您的Google AI API密钥!")
        print("方法1: 设置环境变量 GOOGLE_AI_API_KEY")
        print("方法2: 直接修改此文件中的api_key变量")
        return
    
    # 初始化客户端
    client = genai.Client(api_key=api_key)
    
    # 示例YouTube视频链接和提示词
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # 示例链接
    prompt = "请详细描述这个视频的内容，包括场景、人物、音乐和整体氛围。"
    
    print("=== Gemini 2.5 Pro 视频分析示例 ===")
    print(f"视频链接: {youtube_url}")
    print(f"分析提示: {prompt}")
    print("\n正在分析视频，请稍候...\n")
    
    try:
        # 构建请求内容
        contents = [
            prompt,
            {
                "type": "video",
                "video": {
                    "source": "youtube",
                    "url": youtube_url
                }
            }
        ]
        
        # 调用Gemini API
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",  # 使用最新的模型
            contents=contents
        )
        
        # 输出结果
        print("=== 分析结果 ===")
        print(response.text)
        print("\n=== 分析完成 ===")
        
    except Exception as e:
        print(f"分析过程中出现错误: {str(e)}")
        print("\n可能的解决方案:")
        print("1. 检查API密钥是否正确")
        print("2. 确认网络连接正常")
        print("3. 验证YouTube视频链接是否有效")
        print("4. 检查API配额是否充足")

def analyze_with_custom_prompt():
    """使用自定义提示词分析视频"""
    
    api_key = os.getenv('GOOGLE_AI_API_KEY') or "YOUR_API_KEY_HERE"
    
    if api_key == "YOUR_API_KEY_HERE":
        print("请先设置API密钥!")
        return
    
    client = genai.Client(api_key=api_key)
    
    # 获取用户输入
    print("\n=== 自定义视频分析 ===")
    youtube_url = input("请输入YouTube视频链接: ").strip()
    if not youtube_url:
        print("视频链接不能为空!")
        return
    
    prompt = input("请输入分析提示词 (留空使用默认): ").strip()
    if not prompt:
        prompt = "请描述这个视频的主要内容和特点。"
    
    print(f"\n正在分析视频: {youtube_url}")
    print(f"使用提示词: {prompt}")
    print("\n分析中...\n")
    
    try:
        contents = [
            prompt,
            {
                "type": "video",
                "video": {
                    "source": "youtube",
                    "url": youtube_url
                }
            }
        ]
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=contents
        )
        
        print("=== 分析结果 ===")
        print(response.text)
        
    except Exception as e:
        print(f"分析失败: {str(e)}")

def main():
    """主函数"""
    print("选择运行模式:")
    print("1. 运行示例分析")
    print("2. 自定义视频分析")
    print("3. 退出")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == '1':
        analyze_youtube_video_example()
    elif choice == '2':
        analyze_with_custom_prompt()
    elif choice == '3':
        print("再见!")
    else:
        print("无效选择")

if __name__ == "__main__":
    main()