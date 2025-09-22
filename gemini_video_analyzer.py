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
import tempfile
import urllib.request
import urllib.parse
import mimetypes
from typing import Optional
import google.generativeai as genai

class GeminiVideoAnalyzer:
    """Gemini视频分析器"""
    
    # 默认的YouTube科技视频分析提示词
    DEFAULT_PROMPT = """你是YouTube科技视频分析专家。分析视频并输出Markdown格式报告。

分析要求：
1. 赞助信息：判断是否有赞助（明确赞助/可能合作/无赞助）
2. 品牌分析：统计提及的科技品牌，包括时长、占比、好感度评分(1-5分)
3. 内容分类：视频类型、简介、KOL情感倾向
4. 核心观点：提取正负面评价

输出格式：
# YouTube视频分析报告

## 1. 赞助信息
- 判断结果: [结果]
- 依据: [简要说明]

## 2. 品牌分析
| 品牌/产品 | 时长(秒) | 占比(%) | 好感度(1-5) | 核心观点 |
|---|---|---|---|---|
| [品牌] | [时长] | [占比] | [评分] | [观点] |

## 3. 内容摘要
- 视频类型: [类型]
- 内容简介: [简介]
- KOL情感: [1-5分]

## 4. 关键评价
- 正面: [观点]
- 负面: [观点]

请用中文分析，基于视频实际内容。"""
    
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
        
    def analyze_youtube_video(self, youtube_url: str, prompt: Optional[str] = None, model: str = "gemini-2.5-flash", webhook_url: Optional[str] = None) -> str:
        """分析YouTube视频
        
        Args:
            youtube_url: YouTube视频链接
            prompt: 用户提示词，如果不提供则使用默认的YouTube科技视频分析提示词
            model: 使用的模型名称
            webhook_url: 可选的webhook地址，用于发送分析结果
            
        Returns:
            分析结果文本
        """
        # 如果没有提供prompt，使用默认的YouTube科技视频分析提示词
        if prompt is None:
            prompt = self.DEFAULT_PROMPT
        try:
            # 构建请求内容 - 使用官方推荐的file_data格式
            contents = [{
                "parts": [
                    {"text": prompt},
                    {
                        "file_data": {
                            "file_uri": youtube_url
                        }
                    }
                ]
            }]
            
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
    
    def analyze_local_video(self, video_path: str, prompt: Optional[str] = None, model: str = "gemini-2.5-flash", webhook_url: Optional[str] = None) -> str:
        """分析本地视频文件
        
        Args:
            video_path: 本地视频文件路径
            prompt: 用户提示词，如果不提供则使用默认的YouTube科技视频分析提示词
            model: 使用的模型名称
            webhook_url: 可选的webhook地址，用于发送分析结果
            
        Returns:
            分析结果文本
        """
        # 如果没有提供prompt，使用默认的YouTube科技视频分析提示词
        if prompt is None:
            prompt = self.DEFAULT_PROMPT
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
            
            # 构建请求内容 - 使用官方推荐的file_data格式
            contents = [{
                "parts": [
                    {"text": prompt},
                    {
                        "file_data": {
                            "mime_type": uploaded_file.mime_type,
                            "file_uri": uploaded_file.uri
                        }
                    }
                ]
            }]
            
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
    
    def download_video(self, video_url: str) -> str:
        """从网络链接下载视频到临时文件
        
        Args:
            video_url: 视频链接
            
        Returns:
            临时文件路径
        """
        try:
            print(f"正在下载视频: {video_url}")
            
            # 获取文件扩展名
            parsed_url = urllib.parse.urlparse(video_url)
            path = parsed_url.path
            
            # 尝试从URL获取文件扩展名
            if '.' in path:
                ext = os.path.splitext(path)[1]
                if ext.lower() not in ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv']:
                    ext = '.mp4'  # 默认扩展名
            else:
                ext = '.mp4'  # 默认扩展名
            
            # 创建临时文件
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            temp_path = temp_file.name
            temp_file.close()
            
            # 下载视频
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            req = urllib.request.Request(video_url, headers=headers)
            
            with urllib.request.urlopen(req) as response:
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                
                with open(temp_path, 'wb') as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r下载进度: {progress:.1f}%", end='', flush=True)
            
            print(f"\n✓ 视频下载完成: {temp_path}")
            return temp_path
            
        except Exception as e:
            print(f"\n✗ 视频下载失败: {str(e)}")
            raise
    
    def analyze_video_url(self, video_url: str, prompt: Optional[str] = None, model: str = "gemini-2.5-flash", webhook_url: Optional[str] = None) -> str:
        """分析网络视频链接
        
        Args:
            video_url: 网络视频链接
            prompt: 用户提示词，如果不提供则使用默认的YouTube科技视频分析提示词
            model: 使用的模型名称
            webhook_url: 可选的webhook地址，用于发送分析结果
            
        Returns:
            分析结果文本
        """
        # 如果没有提供prompt，使用默认的YouTube科技视频分析提示词
        if prompt is None:
            prompt = self.DEFAULT_PROMPT
        temp_path = None
        try:
            # 下载视频到临时文件
            temp_path = self.download_video(video_url)
            
            # 使用本地视频分析方法
            result = self.analyze_local_video(
                video_path=temp_path,
                prompt=prompt,
                model=model,
                webhook_url=None  # 不在这里发送webhook，在最后统一发送
            )
            
            # 如果提供了webhook地址，发送结果
            if webhook_url:
                webhook_data = {
                    "type": "video_url_analysis",
                    "prompt": prompt,
                    "video_url": video_url,
                    "model": model,
                    "result": result,
                    "timestamp": __import__('datetime').datetime.now().isoformat()
                }
                self.send_to_webhook(webhook_url, webhook_data)
            
            return result
            
        except Exception as e:
            error_msg = f"分析网络视频时出现错误: {str(e)}"
            
            # 如果提供了webhook地址，也发送错误信息
            if webhook_url:
                webhook_data = {
                    "type": "video_url_analysis",
                    "prompt": prompt,
                    "video_url": video_url,
                    "model": model,
                    "error": error_msg,
                    "timestamp": __import__('datetime').datetime.now().isoformat()
                }
                self.send_to_webhook(webhook_url, webhook_data)
            
            return error_msg
            
        finally:
            # 清理临时文件
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                    print(f"✓ 临时文件已清理: {temp_path}")
                except Exception as e:
                    print(f"⚠ 清理临时文件失败: {str(e)}")

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
        print("3. 分析网络视频链接")
        print("4. 退出")
        
        choice = input("\n请选择 (1-4): ").strip()
        
        # 如果选择分析模式，询问是否使用webhook
        webhook_url = None
        if choice in ['1', '2', '3']:
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
            # 网络视频链接分析
            video_url = input("\n请输入网络视频链接: ").strip()
            if not video_url:
                print("错误: 视频链接不能为空")
                continue
                
            prompt = input("请输入您的提示词: ").strip()
            if not prompt:
                prompt = "请描述这个视频的内容"
            
            print("\n正在下载并分析视频，请稍候...")
            result = analyzer.analyze_video_url(prompt, video_url, webhook_url=webhook_url)
            
            print("\n=== 分析结果 ===")
            print(result)
            
        elif choice == '4':
            print("\n感谢使用！")
            break
            
        else:
            print("\n无效选择，请重试")

if __name__ == "__main__":
    main()