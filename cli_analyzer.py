#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini视频分析工具 - 命令行版本
支持通过命令行参数传入prompt、YouTube地址和webhook
"""

import argparse
import os
import sys
from gemini_video_analyzer import GeminiVideoAnalyzer

def main():
    """主函数 - 支持命令行参数"""
    parser = argparse.ArgumentParser(
        description='Gemini视频分析工具 - 支持YouTube视频分析',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python cli_analyzer.py --prompt "请分析这个视频的主要内容" --youtube "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  python cli_analyzer.py --prompt "总结视频要点" --youtube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --webhook "https://webhook.site/your-id"
  python cli_analyzer.py --prompt "分析视频" --local "/path/to/video.mp4" --webhook "https://your-webhook.com/endpoint"
        """
    )
    
    # 必需参数
    parser.add_argument(
        '--prompt', '-p',
        required=True,
        help='分析提示词（必需）'
    )
    
    # 视频源参数（二选一）
    video_group = parser.add_mutually_exclusive_group(required=True)
    video_group.add_argument(
        '--youtube', '-y',
        help='YouTube视频链接'
    )
    video_group.add_argument(
        '--local', '-l',
        help='本地视频文件路径'
    )
    
    # 可选参数
    parser.add_argument(
        '--webhook', '-w',
        help='Webhook地址（可选）'
    )
    parser.add_argument(
        '--model', '-m',
        default='gemini-2.5-pro',
        help='使用的模型名称（默认: gemini-2.5-pro）'
    )
    parser.add_argument(
        '--api-key', '-k',
        help='Google AI API密钥（可选，优先使用环境变量GOOGLE_AI_API_KEY）'
    )
    
    args = parser.parse_args()
    
    # 获取API密钥
    api_key = args.api_key or os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        print("错误: 需要提供API密钥")
        print("请设置环境变量GOOGLE_AI_API_KEY或使用--api-key参数")
        sys.exit(1)
    
    # 初始化分析器
    try:
        analyzer = GeminiVideoAnalyzer(api_key)
        print("=== Gemini视频分析工具 - 命令行版本 ===")
        print(f"模型: {args.model}")
        print(f"提示词: {args.prompt}")
        
        if args.youtube:
            print(f"YouTube视频: {args.youtube}")
            if args.webhook:
                print(f"Webhook: {args.webhook}")
            print("\n开始分析YouTube视频...")
            
            result = analyzer.analyze_youtube_video(
                prompt=args.prompt,
                youtube_url=args.youtube,
                model=args.model,
                webhook_url=args.webhook
            )
            
        elif args.local:
            print(f"本地视频: {args.local}")
            if args.webhook:
                print(f"Webhook: {args.webhook}")
            
            # 检查文件是否存在
            if not os.path.exists(args.local):
                print(f"错误: 文件不存在 - {args.local}")
                sys.exit(1)
            
            print("\n开始分析本地视频...")
            
            result = analyzer.analyze_local_video(
                prompt=args.prompt,
                video_path=args.local,
                model=args.model,
                webhook_url=args.webhook
            )
        
        print("\n=== 分析结果 ===")
        print(result)
        print("\n分析完成！")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()