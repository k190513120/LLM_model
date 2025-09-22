#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 2.5 Pro 视频分析示例
演示如何使用API分析YouTube视频
"""

import os
from gemini_video_analyzer import GeminiVideoAnalyzer

def analyze_youtube_video_example():
    """YouTube视频分析示例 - 使用默认的YouTube科技视频分析提示词"""
    
    # 设置API密钥 (请替换为您的实际API密钥)
    api_key = os.getenv('GOOGLE_AI_API_KEY') or "AIzaSyCFtj3d4KB_2kxO74Jf3nUxnNhFu_2Kir0"
    
    if not api_key or api_key == "AIzaSyCFtj3d4KB_2kxO74Jf3nUxnNhFu_2Kir0":
        print("请设置您的Google AI API密钥!")
        print("方法1: 设置环境变量 GOOGLE_AI_API_KEY")
        print("方法2: 直接修改此文件中的api_key变量")
        return
    
    # 初始化分析器
    analyzer = GeminiVideoAnalyzer(api_key)
    
    # 示例YouTube视频链接
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # 示例链接
    
    print("=== Gemini YouTube视频分析示例 ===")
    print(f"视频链接: {youtube_url}")
    print("使用默认的YouTube科技视频分析提示词")
    print("\n正在分析视频，请稍候...\n")
    
    try:
        # 使用默认提示词分析视频（不传入prompt参数）
        result = analyzer.analyze_youtube_video(
            youtube_url=youtube_url,
            model="gemini-2.5-flash"
        )
        
        # 输出结果
        print("=== 分析结果 ===")
        print(result)
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
    
    api_key = os.getenv('GOOGLE_AI_API_KEY') or "AIzaSyCFtj3d4KB_2kxO74Jf3nUxnNhFu_2Kir0"
    
    if not api_key or api_key == "AIzaSyCFtj3d4KB_2kxO74Jf3nUxnNhFu_2Kir0":
        print("请先设置API密钥!")
        return
    
    analyzer = GeminiVideoAnalyzer(api_key)
    
    # 获取用户输入
    print("\n=== 自定义视频分析 ===")
    youtube_url = input("请输入YouTube视频链接: ").strip()
    if not youtube_url:
        print("视频链接不能为空!")
        return
    
    prompt = input("请输入分析提示词 (留空使用默认的YouTube科技视频分析提示词): ").strip()
    
    print(f"\n正在分析视频: {youtube_url}")
    if prompt:
        print(f"使用自定义提示词: {prompt}")
    else:
        print("使用默认的YouTube科技视频分析提示词")
    print("\n分析中...\n")
    
    try:
        # 如果没有提供prompt，则使用默认提示词
        result = analyzer.analyze_youtube_video(
            youtube_url=youtube_url,
            prompt=prompt if prompt else None,
            model="gemini-2.5-flash"
        )
        
        print("=== 分析结果 ===")
        print(result)
        
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