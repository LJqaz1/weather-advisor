# weather_advisor/ai_suggester.py
import argparse
import os
import json
from typing import Optional

def build_prompt(city: str, temp: float, desc: str, time_remark: str, lang: str = 'ja') -> str:
    """
    构建AI提示词，支持多语言
    """
    prompts = {
        'en': f"""You are a professional clothing advisor. Based on the weather information below, provide a concise one-sentence clothing recommendation in English:

City: {city}
Temperature: {temp}℃
Weather: {desc}
Time of Day: {time_remark}

Please provide practical, specific clothing advice considering the temperature, weather conditions, and time of day.""",

        'zh': f"""你是一位专业的穿衣顾问。请根据以下天气信息，用中文提供一句简洁的穿衣建议：

城市：{city}
气温：{temp}℃
天气：{desc}
时间段：{time_remark}

请提供实用、具体的穿衣建议，考虑气温、天气状况和时间段。""",

        'ja': f"""あなたは服装の専門アドバイザーです。以下の天気情報に基づいて、日本語で1文の実用的な服装提案をしてください：

都市：{city}
気温：{temp}℃
天気：{desc}
時間帯：{time_remark}

気温、天気状況、時間帯を考慮した具体的で実用的な服装アドバイスをお願いします。"""
    }
    
    return prompts.get(lang, prompts['ja'])

def call_ollama_gemma(prompt: str) -> Optional[str]:
    """
    调用 Ollama + Gemma 模型
    """
    try:
        import requests
        import json
        
        # Ollama 默认运行在 localhost:11434
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        model_name = os.getenv("OLLAMA_MODEL", "gemma:7b")  # 可配置模型版本
        
        print(f"🤖 调用 Ollama Gemma 模型中... (模型: {model_name})")
        
        # 构建请求数据
        data = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,  # 不使用流式输出，直接获取完整响应
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 150
            }
        }
        
        # 发送请求到 Ollama
        response = requests.post(
            f"{ollama_url}/api/generate",
            json=data,
            timeout=30  # 本地模型可能需要较长时间
        )
        
        if response.status_code == 200:
            result = response.json()
            suggestion = result.get("response", "").strip()
            
            if suggestion:
                return suggestion
            else:
                print("❌ Ollama 返回空响应")
                return None
        else:
            print(f"❌ Ollama API 错误: {response.status_code} - {response.text}")
            return None
            
    except ImportError:
        print("❌ 未安装 requests 库")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 Ollama 服务，请确保 Ollama 正在运行")
        print("   启动 Ollama: ollama serve")
        print("   下载 Gemma: ollama pull gemma:7b")
        return None
    except requests.exceptions.Timeout:
        print("❌ Ollama 请求超时，模型可能正在加载中...")
        return None
    except Exception as e:
        print(f"❌ Ollama 调用失败: {e}")
        return None

def call_openai_api(prompt: str) -> Optional[str]:
    """
    调用 OpenAI API
    """
    try:
        import openai
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            print("❌ 未找到 OpenAI API 密钥")
            return None
        
        client = openai.OpenAI(api_key=openai_api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful clothing advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except ImportError:
        print("❌ 未安装 openai 库，请运行: pip install openai")
        return None
    except Exception as e:
        print(f"❌ OpenAI API 调用失败: {e}")
        return None

def get_ai_suggestion(city: str, temp: float, desc: str, time_remark: str, 
                     lang: str = 'ja', ai_mode: str = 'ollama') -> Optional[str]:
    """
    获取AI建议
    """
    prompt = build_prompt(city, temp, desc, time_remark, lang)
    
    if ai_mode == 'ollama' or ai_mode == 'local':  # 兼容原有的 'local' 参数
        return call_ollama_gemma(prompt)
    elif ai_mode == 'openai':
        return call_openai_api(prompt)
    else:
        print(f"❌ 不支持的AI模式: {ai_mode}")
        return None

def parse_args():
    """命令行参数解析（用于独立测试）"""
    parser = argparse.ArgumentParser(description="AI 服装建议工具")
    parser.add_argument('--ai-mode', default='ollama', choices=['ollama', 'local', 'openai'], 
                       help='AI模式选择 (ollama=本地Ollama+Gemma, openai=OpenAI API)')
    parser.add_argument('--city', default='Tokyo')
    parser.add_argument('--lang', default='ja', choices=['ja', 'zh', 'en'])
    parser.add_argument('--temp', type=float, default=21)
    parser.add_argument('--desc', default='cloudy')
    return parser.parse_args()

def main():
    """独立测试功能"""
    args = parse_args()
    
    # 模拟天气数据
    time_remarks = {
        'ja': '夜は冷え込むでしょう',
        'zh': '晚上气温会下降',
        'en': 'Evening temperatures expected to drop'
    }
    
    time_remark = time_remarks.get(args.lang, time_remarks['ja'])
    
    prompt = build_prompt(args.city, args.temp, args.desc, time_remark, args.lang)
    print("🌟 AI提示词:")
    print(prompt)
    print("\n" + "="*50)
    
    suggestion = get_ai_suggestion(args.city, args.temp, args.desc, time_remark, args.lang, args.ai_mode)
    if suggestion:
        print(f"🤖 AI建议: {suggestion}")
    else:
        print("❌ 无法获取AI建议")

if __name__ == '__main__':
    main()