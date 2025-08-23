#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 2.5 Pro 视频分析工具
支持输入提示词和YouTube视频链接，返回AI分析结果
"""

import os
import sys
import requests
import json
from typing import Optional
import google.generativeai as genai

class GeminiVideoAnalyzer:
    """Gemini视频分析器"""
    
    def __init__(self, api_key: str):
        """初始化分析器
        
        Args:
            api_key: Google AI API密钥
        """
        genai.configure(api_key=api_key)
    
    def send_to_webhook(self, webhook_url: str, data: dict) -> bool:
        """发送数据到webhook
        
        Args:
            webhook_url: webhook地址
            data: 要发送的数据
            
        Returns:
            发送是否成功
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Gemini-Video-Analyzer/1.0'
            }
            
            response = requests.post(
                webhook_url,
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✓ 成功发送到webhook: {webhook_url}")
                return True
            else:
                print(f"✗ Webhook响应错误: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ 发送到webhook失败: {str(e)}")
            return False
        
    def analyze_youtube_video(self, prompt: str, youtube_url: str, model: str = "gemini-2.5-pro", webhook_url: Optional[str] = None) -> str:
        """分析YouTube视频
        
        Args:
            prompt: 用户提示词
            youtube_url: YouTube视频链接
            model: 使用的模型名称
            webhook_url: 可选的webhook地址，用于发送分析结果
            
        Returns:
            分析结果文本
        """
        try:
            # 构建请求内容 - 直接使用YouTube URL
            contents = [
                prompt,
                youtube_url
            ]
            
            # 调用Gemini API
            model_instance = genai.GenerativeModel(model)
            response = model_instance.generate_content(contents)
            
            result = response.text
            
            # 如果提供了webhook地址，发送结果
            if webhook_url:
                webhook_data = {
                    "type": "youtube_video_analysis",
                    "prompt": prompt,
                    "video_url": youtube_url,
                    "model": model,
                    "result": result,
                    "timestamp": __import__('datetime').datetime.now().isoformat()
                }
                self.send_to_webhook(webhook_url, webhook_data)
            
            return result
            
        except Exception as e:
            error_msg = f"分析过程中出现错误: {str(e)}"
            
            # 如果提供了webhook地址，也发送错误信息
            if webhook_url:
                webhook_data = {
                    "type": "youtube_video_analysis",
                    "prompt": prompt,
                    "video_url": youtube_url,
                    "model": model,
                    "error": error_msg,
                    "timestamp": __import__('datetime').datetime.now().isoformat()
                }
                self.send_to_webhook(webhook_url, webhook_data)
            
            return error_msg
    
    def analyze_local_video(self, prompt: str, video_path: str, model: str = "gemini-2.5-pro", webhook_url: Optional[str] = None) -> str:
        """分析本地视频文件
        
        Args:
            prompt: 用户提示词
            video_path: 本地视频文件路径
            model: 使用的模型名称
            webhook_url: 可选的webhook地址，用于发送分析结果
            
        Returns:
            分析结果文本
        """
        try:
            # 上传视频文件
            print("正在上传视频文件...")
            uploaded_file = genai.upload_file(path=video_path)
            
            # 等待文件处理完成
            print("等待文件处理完成...")
            file_info = genai.get_file(name=uploaded_file.name)
            while file_info.state.name == "PROCESSING":
                import time
                time.sleep(2)
                file_info = genai.get_file(name=uploaded_file.name)
            
            if file_info.state.name == "FAILED":
                return "视频文件处理失败"
            
            # 构建请求内容
            contents = [
                prompt,
                uploaded_file
            ]
            
            # 调用Gemini API
            model_instance = genai.GenerativeModel(model)
            response = model_instance.generate_content(contents)
            
            result = response.text
            
            # 清理上传的文件
            genai.delete_file(name=uploaded_file.name)
            
            # 如果提供了webhook地址，发送结果
            if webhook_url:
                webhook_data = {
                    "type": "local_video_analysis",
                    "prompt": prompt,
                    "video_path": video_path,
                    "model": model,
                    "result": result,
                    "timestamp": __import__('datetime').datetime.now().isoformat()
                }
                self.send_to_webhook(webhook_url, webhook_data)
            
            return result
            
        except Exception as e:
            error_msg = f"分析过程中出现错误: {str(e)}"
            
            # 如果提供了webhook地址，也发送错误信息
            if webhook_url:
                webhook_data = {
                    "type": "local_video_analysis",
                    "prompt": prompt,
                    "video_path": video_path,
                    "model": model,
                    "error": error_msg,
                    "timestamp": __import__('datetime').datetime.now().isoformat()
                }
                self.send_to_webhook(webhook_url, webhook_data)
            
            return error_msg

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
        
        # 如果选择分析模式，询问是否使用webhook
        webhook_url = None
        if choice in ['1', '2']:
            use_webhook = input("\n是否使用webhook发送结果? (y/n): ").strip().lower()
            if use_webhook in ['y', 'yes', '是']:
                webhook_url = input("请输入webhook地址: ").strip()
                if not webhook_url:
                    print("警告: webhook地址为空，将不发送结果")
                    webhook_url = None
        
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
            result = analyzer.analyze_youtube_video(prompt, youtube_url, webhook_url=webhook_url)
            
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
            result = analyzer.analyze_local_video(prompt, video_path, webhook_url=webhook_url)
            
            print("\n=== 分析结果 ===")
            print(result)
            
        elif choice == '3':
            print("\n感谢使用！")
            break
            
        else:
            print("\n无效选择，请重试")

if __name__ == "__main__":
    main()