#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 2.5 Pro 视频分析工具
支持输入提示词和YouTube视频链接，返回AI分析结果
"""

import os
import sys
from typing import Optional
from google import genai

class GeminiVideoAnalyzer:
    """Gemini视频分析器"""
    
    def __init__(self, api_key: str):
        """初始化分析器
        
        Args:
            api_key: Google AI API密钥
        """
        self.client = genai.Client(api_key=api_key)
        
    def analyze_youtube_video(self, prompt: str, youtube_url: str, model: str = "gemini-2.0-flash-exp") -> str:
        """分析YouTube视频
        
        Args:
            prompt: 用户提示词
            youtube_url: YouTube视频链接
            model: 使用的模型名称
            
        Returns:
            分析结果文本
        """
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
            response = self.client.models.generate_content(
                model=model,
                contents=contents
            )
            
            return response.text
            
        except Exception as e:
            return f"分析过程中出现错误: {str(e)}"
    
    def analyze_local_video(self, prompt: str, video_path: str, model: str = "gemini-2.0-flash-exp") -> str:
        """分析本地视频文件
        
        Args:
            prompt: 用户提示词
            video_path: 本地视频文件路径
            model: 使用的模型名称
            
        Returns:
            分析结果文本
        """
        try:
            # 上传视频文件
            print("正在上传视频文件...")
            uploaded_file = self.client.files.upload(path=video_path)
            
            # 等待文件处理完成
            print("等待文件处理完成...")
            file_info = self.client.files.get(name=uploaded_file.name)
            while file_info.state.name == "PROCESSING":
                import time
                time.sleep(2)
                file_info = self.client.files.get(name=uploaded_file.name)
            
            if file_info.state.name == "FAILED":
                return "视频文件处理失败"
            
            # 构建请求内容
            contents = [
                prompt,
                uploaded_file
            ]
            
            # 调用Gemini API
            response = self.client.models.generate_content(
                model=model,
                contents=contents
            )
            
            # 清理上传的文件
            self.client.files.delete(name=uploaded_file.name)
            
            return response.text
            
        except Exception as e:
            return f"分析过程中出现错误: {str(e)}"

def main():
    """主函数"""
    print("=== Gemini 2.5 Pro 视频分析工具 ===")
    print()
    
    # 获取API密钥
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        api_key = input("请输入您的Google AI API密钥: ").strip()
        if not api_key:
            print("错误: 需要提供API密钥")
            sys.exit(1)
    
    # 初始化分析器
    analyzer = GeminiVideoAnalyzer(api_key)
    
    while True:
        print("\n选择分析模式:")
        print("1. 分析YouTube视频")
        print("2. 分析本地视频文件")
        print("3. 退出")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == '1':
            # YouTube视频分析
            youtube_url = input("\n请输入YouTube视频链接: ").strip()
            if not youtube_url:
                print("错误: YouTube链接不能为空")
                continue
                
            prompt = input("请输入您的提示词: ").strip()
            if not prompt:
                prompt = "请描述这个视频的内容"
            
            print("\n正在分析视频，请稍候...")
            result = analyzer.analyze_youtube_video(prompt, youtube_url)
            
            print("\n=== 分析结果 ===")
            print(result)
            
        elif choice == '2':
            # 本地视频分析
            video_path = input("\n请输入本地视频文件路径: ").strip()
            if not video_path or not os.path.exists(video_path):
                print("错误: 视频文件不存在")
                continue
                
            prompt = input("请输入您的提示词: ").strip()
            if not prompt:
                prompt = "请描述这个视频的内容"
            
            print("\n正在分析视频，请稍候...")
            result = analyzer.analyze_local_video(prompt, video_path)
            
            print("\n=== 分析结果 ===")
            print(result)
            
        elif choice == '3':
            print("\n感谢使用！")
            break
            
        else:
            print("\n无效选择，请重试")

if __name__ == "__main__":
    main()