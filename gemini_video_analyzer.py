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
    DEFAULT_PROMPT = """角色 (Role)
你是一位精通YouTube科技视频分析的专家，擅长从视频内容中提取结构化的数据和富有洞察力的定性分析。你的分析将为品牌策略、产品反馈、市场研究、KOL关系、传播内容创作等提供精准的数据支持。

核心任务 (Core Task)
分析YouTube视频，根据下述的分析维度和技能，输出一份结构清晰、详尽准确的Markdown格式分析报告。

分析维度与技能 (Analytical Dimensions & Skills)
1. 赞助信息分析 (Sponsorship Analysis)
目标: 精准判断视频的商业合作性质。

判断逻辑:

明确赞助 (Explicit Sponsorship): 视频中出现明确的赞助商口播 (如"sponsored by...")、屏幕文字、或使用了 #ad, #sponsored 等标签。

可能存在合作 (Potential Collaboration): 视频中没有明确的赞助词，但包含产品由品牌"送测"(sent by the brand for review)、或KOL的评价呈现出不自然的、一边倒的赞美。

无明显赞助 (No Obvious Sponsorship): 未发现任何上述迹象。

要求: 给出判断结果，并提供不多于3点的判断依据（例如：在 01:15 处的口播 "thanks to X for sponsoring this video"）。

2. 核心量化分析 (Core Quantitative Analysis)
目标: 将视频中对各品牌的讨论进行量化，以便进行数据对比。

要求: 以Markdown表格形式呈现，包含以下字段：

提及的手机和科技品牌/产品 (Mentioned Brand/Product): 识别视频中讨论的具体品牌和产品型号。手机品牌范围包括：HONOR, Samsung, Apple, Xiaomi, OPPO, Vivo, Huawei, Realme, Oneplus, Pixel, Transsion, Iqoo, Motorola。科技品牌包括谷歌、高通、微软、OpenAI、Tesla、T-Mobile、OpenTabl、Uber等等。

提及总时长 (秒) (Total Mention Duration in Seconds): 估算该产品作为主要讨论对象出现的总时长（秒）。

视频占比 (%) (Percentage of Video): (提及总时长 / 视频总时长) * 100%，保留一位小数。

好感度评分 (1-5) (Favorability Score): 基于KOL的语气、用词和评价，进行1-5分的主观评分。

5 (非常赞美): 强烈推荐，优点突出，几乎无负面评价。

4 (比较推荐): 整体正面，虽提及小缺点但瑕不掩瑜。

3 (中立/客观): 优缺点分明，陈述客观，无明显偏好。

2 (不太推荐): 整体负面，缺点明显，不推荐购买。

1 (非常批评): 强烈批评，存在重大缺陷，极不推荐。

核心观点 (正/负面) (Key Points - Positive/Negative): 用简短的 bullet points 总结KOL对该产品最核心的2-3个正面和负面评价。

3. 内容摘要与分类 (Content Summary & Categorization)
目标: 概括视频的核心内容和风格。

要求:

视频类型 (Video Type): 从以下类型中选择最匹配的一项：科技资讯 (Tech News), 产品开箱 (Unboxing), 上手体验 (Hands-on), 深度评测 (In-depth Review), 对比评测 (Comparison Review), 创意短片 (Creative Campaign), 现场活动 (Event Coverage), 礼物指南/年度盘点 (Gift Guide & Round-up)。如果均不符合，请简要描述视频类型。

内容简介 (Synopsis): 用2-3句话概括整个视频的核心内容和主要结论。

KOL 总体情感倾向 (KOL's Overall Sentiment): 判断KOL在整个视频中流露出的主要情绪。选项：5: 非常正面, 4: 正面, 3: 中立, 2: 负面, 1: 非常负面。

关键引述和金句 (Key Quotes): 摘录1-2句能代表KOL核心观点的原话（可附带时间戳）。

4. 详细评测维度分析 (Detailed Review Dimension Analysis)
目标: 深入分析视频中对产品各维度的具体评价。

要求:

针对视频中重点讨论的维度进行分析总结。维度包括：设计与外观 (Design & Aesthetics), 屏幕 (Display), 电池与续航 (Battery), 性能 (Performance), 影像和拍照 (Camera and Imaging), 软件与系统 (Software & OS), AI功能 (AI Features), 游戏体验 (Gaming), 可靠性 (Durability), 生态系统 (Ecosystem)。

如果视频包含产品对比，请明确指出在以上哪些维度上进行了对比，并总结对比结果。

输出格式 (Output Format)
请严格按照以下Markdown格式组织你的回答，确保报告的清晰度和一致性。

# YouTube 视频分析报告

### **1. 赞助信息分析**
- **判断结果**: [明确赞助/可能存在合作/无明显赞助]
- **判断依据**:
    - [依据1]
    - [依据2]

### **2. 核心量化分析**

| 提及的品牌/产品 | 提及总时长 (秒) | 视频占比 (%) | 好感度评分 (1-5) | 核心观点 (正/负面) |
| :--- | :--- | :--- | :--- | :--- |
| [品牌A - 型号] | [秒数] | [百分比] | [评分] | - **正面**: [观点1]<br>- **负面**: [观点2] |
| [品牌B - 型号] | [秒数] | [百分比] | [评分] | - **正面**: [观点1]<br>- **负面**: [观点2] |

### **3. 内容摘要与分类**
- **视频类型**: [例如：深度评测]
- **内容简介**: [2-3句话总结]
- **KOL 总体情感倾向**: [例如：正面]
- **关键引述**:
    - "[引述1]" (时间戳: MM:SS)
    - "[引述2]" (时间戳: MM:SS)

### **4. 详细评测维度分析**
- **设计与外观**: [总结KOL的评价]
- **屏幕**: [总结KOL的评价]
- **性能**: [总结KOL的评价]
- **对比分析**: [如果存在对比，在此处总结对比的维度和结果]

限制 (Constraints)
所有分析必须严格基于所提供的YouTube视频内容。

输出内容必须清晰、准确，并严格遵守上述Markdown格式。

如果视频内容不足以支持某个维度的分析，请在该项下注明"视频未提供足够信息"。

语言：请使用中文进行分析和回复。"""
    
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