# weather_advisor/ai_suggester.py
import argparse
import os
import json
import datetime
from typing import Optional


def build_enhanced_prompt(
    city: str, temp: float, desc: str, time_remark: str, lang: str = "ja"
) -> str:
    """
    构建增强版AI提示词，包含个性化信息
    """
    current_hour = datetime.datetime.now().hour
    month = datetime.datetime.now().month

    # 确定时间段和季节
    if 5 <= current_hour <= 11:
        time_period = "morning"
    elif 12 <= current_hour <= 17:
        time_period = "afternoon"
    elif 18 <= current_hour <= 23:
        time_period = "evening"
    else:
        time_period = "night"

    if month in [12, 1, 2]:
        season = "winter"
    elif month in [3, 4, 5]:
        season = "spring"
    elif month in [6, 7, 8]:
        season = "summer"
    else:
        season = "autumn"

    # 地域特色提示
    regional_context = {
        "tokyo": "high humidity area",
        "osaka": "windy conditions common",
        "kyoto": "temperature fluctuations due to basin location",
        "london": "frequent light rain",
        "paris": "cobblestone streets",
        "new york": "windy between buildings",
        "beijing": "dusty conditions and air quality concerns",
        "shanghai": "high humidity and frequent rain",
        "singapore": "extremely hot and humid year-round",
    }

    region_hint = ""
    for city_key, context in regional_context.items():
        if city_key in city.lower():
            region_hint = f" Note: {city} is known for {context}."
            break

    prompts = {
        "en": f"""You are a professional styling consultant with expertise in weather-appropriate fashion. 

Current Context:
- Location: {city}{region_hint}
- Temperature: {temp}℃
- Weather: {desc}
- Time: {time_period} ({time_remark})
- Season: {season}

Provide ONE concise, practical clothing recommendation that considers:
1. Temperature comfort and layering
2. Weather protection needs
3. Time-appropriate styling
4. Seasonal fashion trends
5. Regional climate characteristics

Response should be specific, actionable, and under 25 words.""",
        "zh": f"""你是专业的时尚造型顾问，专门提供适合天气的穿搭建议。

当前情况：
- 地点：{city}{region_hint}
- 气温：{temp}℃
- 天气：{desc}
- 时间：{time_period}（{time_remark}）
- 季节：{season}

请提供一条简洁实用的穿衣建议，需要考虑：
1. 温度舒适性和层次搭配
2. 天气防护需求
3. 时间段合适性
4. 季节时尚趋势
5. 地域气候特点

回答要具体、可行，控制在25字以内。""",
        "ja": f"""あなたは天候に適したファッションの専門スタイリストです。

現在の状況：
- 場所：{city}{region_hint}
- 気温：{temp}℃
- 天気：{desc}
- 時間帯：{time_period}（{time_remark}）
- 季節：{season}

以下を考慮した簡潔で実用的な服装提案を1つお願いします：
1. 気温による快適性と重ね着
2. 天候に対する防護
3. 時間帯に適したスタイル
4. 季節のトレンド
5. 地域の気候特性

25文字以内で、具体的で実行可能な提案をしてください。""",
    }

    return prompts.get(lang, prompts["ja"])


def build_prompt(
    city: str, temp: float, desc: str, time_remark: str, lang: str = "ja"
) -> str:
    """
    构建AI提示词，支持多语言 - 保持向后兼容性
    """
    # 使用增强版提示词
    return build_enhanced_prompt(city, temp, desc, time_remark, lang)


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

        if os.getenv("DEBUG_MODE") == "True":
            print(f"🤖 调用 Ollama Gemma 模型中... (模型: {model_name})")

        # 构建请求数据
        data = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,  # 不使用流式输出，直接获取完整响应
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 150,
                "stop": ["\n\n", "。。", ".."],  # 防止过长回答
            },
        }

        # 发送请求到 Ollama
        response = requests.post(
            f"{ollama_url}/api/generate",
            json=data,
            timeout=30,  # 本地模型可能需要较长时间
        )

        if response.status_code == 200:
            result = response.json()
            suggestion = result.get("response", "").strip()

            if suggestion:
                # 清理可能的格式问题
                suggestion = suggestion.replace("\n", " ").strip()
                return suggestion
            else:
                print("❌ Ollama 返回空响应")
                return None
        else:
            print(f"❌ Ollama API 错误: {response.status_code} - {response.text}")
            return None

    except ImportError:
        print("❌ 未安装 requests 库，请运行: pip install requests")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 Ollama 服务，请确保 Ollama 正在运行")
        print("   启动 Ollama: ollama serve")
        print(f"   下载模型: ollama pull {os.getenv('OLLAMA_MODEL', 'gemma:7b')}")
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
            print("❌ 未找到 OpenAI API 密钥，请设置 OPENAI_API_KEY 环境变量")
            return None

        client = openai.OpenAI(api_key=openai_api_key)

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and concise clothing advisor.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
            temperature=0.7,
        )

        suggestion = response.choices[0].message.content.strip()
        return suggestion

    except ImportError:
        print("❌ 未安装 openai 库，请运行: pip install openai")
        return None
    except Exception as e:
        print(f"❌ OpenAI API 调用失败: {e}")
        return None


def get_ai_suggestion(
    city: str,
    temp: float,
    desc: str,
    time_remark: str,
    lang: str = "ja",
    ai_mode: str = "ollama",
) -> Optional[str]:
    """
    获取AI建议
    """
    prompt = build_enhanced_prompt(city, temp, desc, time_remark, lang)

    if ai_mode == "ollama" or ai_mode == "local":  # 兼容原有的 'local' 参数
        return call_ollama_gemma(prompt)
    elif ai_mode == "openai":
        return call_openai_api(prompt)
    else:
        print(f"❌ 不支持的AI模式: {ai_mode}")
        return None


def parse_args():
    """命令行参数解析（用于独立测试）"""
    parser = argparse.ArgumentParser(description="AI 服装建议工具")
    parser.add_argument(
        "--ai-mode",
        default="ollama",
        choices=["ollama", "local", "openai"],
        help="AI模式选择 (ollama=本地Ollama+Gemma, openai=OpenAI API)",
    )
    parser.add_argument("--city", default="Tokyo")
    parser.add_argument("--lang", default="ja", choices=["ja", "zh", "en"])
    parser.add_argument("--temp", type=float, default=21)
    parser.add_argument("--desc", default="cloudy")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    return parser.parse_args()


def main():
    """独立测试功能"""
    args = parse_args()

    # 模拟天气数据
    time_remarks = {
        "ja": "夜は冷え込むでしょう",
        "zh": "晚上气温会下降",
        "en": "Evening temperatures expected to drop",
    }

    time_remark = time_remarks.get(args.lang, time_remarks["ja"])

    if args.verbose:
        print("🌟 增强版AI提示词:")
        prompt = build_enhanced_prompt(
            args.city, args.temp, args.desc, time_remark, args.lang
        )
        print(prompt)
        print("\n" + "=" * 50)

    suggestion = get_ai_suggestion(
        args.city, args.temp, args.desc, time_remark, args.lang, args.ai_mode
    )
    if suggestion:
        success_msgs = {
            "ja": f"🤖 AI建議: {suggestion}",
            "zh": f"🤖 AI建议: {suggestion}",
            "en": f"🤖 AI Suggestion: {suggestion}",
        }
        print(success_msgs.get(args.lang, success_msgs["ja"]))
    else:
        error_msgs = {
            "ja": "❌ AI建議を取得できませんでした",
            "zh": "❌ 無法获取AI建议",
            "en": "❌ Unable to get AI suggestion",
        }
        print(error_msgs.get(args.lang, error_msgs["ja"]))


if __name__ == "__main__":
    main()
