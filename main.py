# main.py
import argparse
import os
from dotenv import load_dotenv
from weather_advisor.advisor import get_weather, get_clothing_suggestion
from weather_advisor.utils import (
    get_time_remark,
    format_weather_tip,
    get_city_by_ip,
    normalize_city,
    get_time_greeting,
    get_seasonal_reminder,
    get_regional_advice,
    format_personalized_weather_display,
)
from weather_advisor.ai_suggester import get_ai_suggestion


def get_args():
    """
    解析命令行参数，支持自定义城市查询和语言选择
    """
    parser = argparse.ArgumentParser(
        description="天気穿衣助手 / Weather Clothing Advisor"
    )
    parser.add_argument(
        "--city", type=str, default="", help="查询的城市名称（留空自动检测）"
    )
    parser.add_argument(
        "--ai-mode",
        choices=["ollama", "local", "openai", "off"],
        default="auto",  # 默认自动选择AI模式
        help="AI 推荐模式（auto=自动选择, ollama=Ollama+Gemma, openai=OpenAI API, off=禁用AI）",
    )
    parser.add_argument(
        "--lang", default="ja", choices=["ja", "zh", "en"], help="输出语言选择"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    parser.add_argument("--config", action="store_true", help="显示配置文件信息")
    parser.add_argument(
        "--no-ai", action="store_true", help="强制禁用AI模式，直接使用传统模式"
    )
    return parser.parse_args()


def load_user_preferences():
    """加载用户偏好设置"""
    import json
    import os

    config_file = os.path.expanduser("~/.weather_advisor_config.json")
    default_config = {
        "preferred_lang": "ja",
        "default_city": "Tokyo",
        "default_ai_mode": "ollama",  # 默认启用ollama
        "ai_fallback_enabled": True,  # 启用AI失败回退
        "show_seasonal_tips": True,
        "show_regional_advice": True,
        "preferred_greeting_style": "formal",
        "ollama_model": "gemma:7b",
        "ai_timeout": 30,  # AI请求超时时间
    }

    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                return {**default_config, **user_config}
        except Exception as e:
            print(f"⚠️ 配置文件读取失败，使用默认设置: {e}")
            return default_config
    else:
        # 创建默认配置文件
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            if os.getenv("DEBUG_MODE") == "True":
                print(f"✅ 已创建默认配置文件: {config_file}")
        except Exception as e:
            print(f"⚠️ 无法创建配置文件: {e}")
        return default_config


def detect_available_ai_mode():
    """
    自动检测可用的AI模式
    返回: (ai_mode, is_available)
    """
    import requests

    # 1. 检查Ollama是否可用
    try:
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        response = requests.get(f"{ollama_url}/api/tags", timeout=3)
        if response.status_code == 200:
            return "ollama", True
    except:
        pass

    # 2. 检查OpenAI API Key是否设置
    if os.getenv("OPENAI_API_KEY"):
        return "openai", True

    # 3. 都不可用
    return None, False


def try_ai_suggestion(city, temp, desc, time_remark, lang, ai_mode, verbose=False):
    """
    尝试获取AI建议，包含重试逻辑
    返回: (suggestion, success, error_msg)
    """
    if ai_mode == "off":
        return None, False, "AI模式已禁用"

    # 如果是auto模式，自动检测
    if ai_mode == "auto":
        detected_mode, is_available = detect_available_ai_mode()
        if not is_available:
            return None, False, "未检测到可用的AI服务"
        ai_mode = detected_mode

    if verbose:
        mode_names = {"ollama": "Ollama (本地)", "openai": "OpenAI API"}
        print(f"🤖 尝试使用 {mode_names.get(ai_mode, ai_mode)} 模式...")

    try:
        suggestion = get_ai_suggestion(city, temp, desc, time_remark, lang, ai_mode)
        if suggestion and suggestion.strip():
            return suggestion.strip(), True, None
        else:
            return None, False, f"{ai_mode}模式返回空结果"
    except Exception as e:
        return None, False, f"{ai_mode}模式调用失败: {str(e)}"


def display_ai_mode_result(
    city, temp, desc, suggestion, time_remark, lang, ai_mode_used
):
    """AI模式结果显示"""
    separator = "─" * 35

    # 基本信息
    weather_labels = {
        "ja": "📊 本日の天気情報",
        "zh": "📊 今日天气信息",
        "en": "📊 Today's Weather Info",
    }

    print(f"\n{separator}")
    print(weather_labels.get(lang, weather_labels["en"]))
    print(f"🏙️ {city} | 🌡️ {temp}°C | {desc}")
    if time_remark:
        print(f"⏰ {time_remark}")

    # AI 建议 - 显示使用的AI模式
    ai_labels = {
        "ja": f"🌟 AIスタイリスト提案 ({ai_mode_used.upper()})",
        "zh": f"🌟 AI造型师建议 ({ai_mode_used.upper()})",
        "en": f"🌟 AI Stylist Recommendation ({ai_mode_used.upper()})",
    }
    print(f"\n{separator}")
    print(ai_labels.get(lang, ai_labels["en"]))
    print(f"💡 {suggestion}")

    # 季节提醒
    seasonal = get_seasonal_reminder(lang)
    print(f"\n{separator}")
    seasonal_headers = {"ja": "季節のポイント", "zh": "季节要点", "en": "Seasonal Tips"}
    print(f"{seasonal['icon']} {seasonal_headers.get(lang, seasonal_headers['ja'])}")
    print(f"💭 {seasonal['tip']}")
    print(f"👔 {seasonal['clothing']}")

    # 地域建议
    regional = get_regional_advice(city, temp, lang)
    print(f"\n{regional}")

    # 结尾
    closing_messages = {
        "ja": f"\n{separator}\n✨ 素敵な一日をお過ごしください！\n💬 他にご質問がございましたら、お気軽にどうぞ！",
        "zh": f"\n{separator}\n✨ 祝您有美好的一天！\n💬 如有其他问题，请随时询问！",
        "en": f"\n{separator}\n✨ Have a wonderful day!\n💬 Feel free to ask if you have any questions!",
    }
    print(closing_messages.get(lang, closing_messages["en"]))


def handle_ai_failure(lang, error_msg, config):
    """AI失败时的处理"""
    fallback_messages = {
        "ja": f"\n⚠️ AI建議の取得に失敗しました：{error_msg}\n📋 基本的なおすすめに切り替えます。",
        "zh": f"\n⚠️ AI建议获取失败：{error_msg}\n📋 切换到基础建议模式。",
        "en": f"\n⚠️ AI suggestion failed: {error_msg}\n📋 Switching to basic recommendations.",
    }
    print(fallback_messages.get(lang, fallback_messages["en"]))

    # 如果配置允许，显示故障排除提示
    if config.get("ai_fallback_enabled", True):
        troubleshooting = {
            "ja": "\n💡 AI機能を有効にするには：\n   • Ollama: ollama serve を実行してください\n   • OpenAI: OPENAI_API_KEY 環境変数を設定してください",
            "zh": "\n💡 要启用AI功能：\n   • Ollama: 运行 ollama serve\n   • OpenAI: 设置 OPENAI_API_KEY 环境变量",
            "en": "\n💡 To enable AI features:\n   • Ollama: run 'ollama serve'\n   • OpenAI: set OPENAI_API_KEY environment variable",
        }
        print(troubleshooting.get(lang, troubleshooting["en"]))


def display_traditional_mode(city, temp, desc, time_remark, lang, is_fallback=False):
    """传统模式显示"""
    # 问候
    greeting = get_time_greeting(lang)
    print(f"{greeting}\n")

    # 获取传统建议
    suggestion = get_clothing_suggestion(temp, desc, lang)

    separator = "─" * 35

    # 模式标识
    if is_fallback:
        mode_labels = {
            "ja": "📋 基本おすすめモード（AIフォールバック）",
            "zh": "📋 基础建议模式（AI回退）",
            "en": "📋 Basic Mode (AI Fallback)",
        }
    else:
        mode_labels = {
            "ja": "📋 基本おすすめモード",
            "zh": "📋 基础建议模式",
            "en": "📋 Basic Recommendation Mode",
        }
    print(f"{mode_labels.get(lang, mode_labels['en'])}")

    # 天气信息
    print(f"\n{separator}")
    print(f"🏙️ {city} | 🌡️ {temp}°C | {desc}")
    if time_remark:
        print(f"⏰ {time_remark}")

    # 基础建议
    print(f"\n💡 {suggestion}")

    # 季节和地域信息
    seasonal = get_seasonal_reminder(lang)
    regional = get_regional_advice(city, temp, lang)

    print(f"\n{separator}")
    print(f"{seasonal['icon']} {seasonal['tip']}")
    print(f"👔 {seasonal['clothing']}")

    print(f"\n{regional}")

    # 结尾
    closing_messages = {
        "ja": f"\n{separator}\n✨ 素敵な一日をお過ごしください！",
        "zh": f"\n{separator}\n✨ 祝您有美好的一天！",
        "en": f"\n{separator}\n✨ Have a wonderful day!",
    }
    print(closing_messages.get(lang, closing_messages["en"]))

    # 只有在非回退模式下才显示AI推广
    if not is_fallback:
        ai_promo = {
            "ja": "\n💡 より詳細な提案をご希望の場合は AI機能をお試しください（自動的に最適なAIを選択します）",
            "zh": "\n💡 如需更详细的建议，AI功能会自动选择最佳的AI服务",
            "en": "\n💡 For more detailed suggestions, AI features will automatically select the best available AI service",
        }
        print(ai_promo.get(lang, ai_promo["en"]))


def display_config_info(config, lang):
    """显示配置信息"""
    config_labels = {
        "ja": {
            "title": "📄 現在の設定",
            "lang": "優先言語",
            "city": "デフォルト都市",
            "ai_mode": "デフォルトAIモード",
            "ai_fallback": "AI失敗時の回退",
            "seasonal": "季節提醒",
            "regional": "地域アドバイス",
            "greeting": "挨拶スタイル",
            "model": "Ollamaモデル",
            "timeout": "AIタイムアウト",
            "config_file": "設定ファイル",
            "enabled": "有効",
            "disabled": "無効",
        },
        "zh": {
            "title": "📄 当前配置",
            "lang": "首选语言",
            "city": "默认城市",
            "ai_mode": "默认AI模式",
            "ai_fallback": "AI失败回退",
            "seasonal": "季节提醒",
            "regional": "地域建议",
            "greeting": "问候风格",
            "model": "Ollama模型",
            "timeout": "AI超时时间",
            "config_file": "配置文件",
            "enabled": "启用",
            "disabled": "禁用",
        },
        "en": {
            "title": "📄 Current Configuration",
            "lang": "Preferred Language",
            "city": "Default City",
            "ai_mode": "Default AI Mode",
            "ai_fallback": "AI Fallback",
            "seasonal": "Seasonal Tips",
            "regional": "Regional Advice",
            "greeting": "Greeting Style",
            "model": "Ollama Model",
            "timeout": "AI Timeout",
            "config_file": "Config File",
            "enabled": "Enabled",
            "disabled": "Disabled",
        },
    }

    labels = config_labels.get(lang, config_labels["ja"])
    separator = "─" * 35

    print(f"\n{labels['title']}")
    print(separator)
    print(f"🌐 {labels['lang']}: {config['preferred_lang']}")
    print(f"🏙️ {labels['city']}: {config['default_city']}")
    print(f"🤖 {labels['ai_mode']}: {config['default_ai_mode']}")
    print(
        f"🔄 {labels['ai_fallback']}: {labels['enabled'] if config['ai_fallback_enabled'] else labels['disabled']}"
    )
    print(
        f"🌸 {labels['seasonal']}: {labels['enabled'] if config['show_seasonal_tips'] else labels['disabled']}"
    )
    print(
        f"🗺️ {labels['regional']}: {labels['enabled'] if config['show_regional_advice'] else labels['disabled']}"
    )
    print(f"👋 {labels['greeting']}: {config['preferred_greeting_style']}")
    print(f"⚙️ {labels['model']}: {config['ollama_model']}")
    print(f"⏱️ {labels['timeout']}: {config['ai_timeout']}s")
    print(f"\n📁 {labels['config_file']}: ~/.weather_advisor_config.json")


def main():
    # 自动加载项目根目录下的 .env 文件
    load_dotenv()

    # 加载用户配置
    config = load_user_preferences()

    # 读取环境变量
    api_key = os.getenv("OPENWEATHER_API_KEY")
    debug_mode = os.getenv("DEBUG_MODE", "False") == "True"

    args = get_args()

    # 应用配置文件的默认值
    if not args.city:
        args.city = config.get("default_city", "Tokyo")
    if args.lang == "ja" and not any("--lang" in arg for arg in os.sys.argv):
        args.lang = config.get("preferred_lang", "ja")

    # AI模式处理：如果用户没有明确指定，使用配置文件的默认值
    if args.ai_mode == "auto" and not args.no_ai:
        args.ai_mode = config.get("default_ai_mode", "ollama")
    elif args.no_ai:
        args.ai_mode = "off"

    # 显示配置信息
    if args.config:
        display_config_info(config, args.lang)
        return

    # 验证 API 密钥
    if not api_key:
        error_msg = {
            "ja": "❌ API キーが見つかりません。.env ファイルに OPENWEATHER_API_KEY を設定してください",
            "zh": "❌ 未找到 API 密钥，请在 .env 文件中设置 OPENWEATHER_API_KEY",
            "en": "❌ API key not found. Please set OPENWEATHER_API_KEY in .env file",
        }
        print(error_msg.get(args.lang, error_msg["en"]))
        return

    # 城市处理
    if not args.city or args.city.lower() == "auto":
        city = get_city_by_ip()
        if args.verbose:
            auto_detect_msg = {
                "ja": f"🌐 自動検出された都市: {city}",
                "zh": f"🌐 自动检测到城市: {city}",
                "en": f"🌐 Auto-detected city: {city}",
            }
            print(auto_detect_msg.get(args.lang, auto_detect_msg["en"]))
    else:
        city = normalize_city(args.city)

    if args.verbose:
        info_msg = {
            "ja": f"🏙️ 使用都市：{city}\n🤖 AIモード：{args.ai_mode}\n🔧 モード：{'デバッグ' if debug_mode else '本番'}",
            "zh": f"🏙️ 使用城市：{city}\n🤖 AI模式：{args.ai_mode}\n🔧 当前模式：{'调试' if debug_mode else '正式'}",
            "en": f"🏙️ Using city: {city}\n🤖 AI mode: {args.ai_mode}\n🔧 Mode: {'Debug' if debug_mode else 'Production'}",
        }
        print(info_msg.get(args.lang, info_msg["en"]))

    # 获取天气数据
    temp, desc = get_weather(city, api_key)
    if temp is None:
        error_msg = {
            "ja": "申し訳ありませんが、天気データを取得できませんでした。都市名を確認してください。",
            "zh": "抱歉，无法获取天气数据。请检查城市名称。",
            "en": "Sorry, unable to retrieve weather data. Please check the city name.",
        }
        print(error_msg.get(args.lang, error_msg["en"]))
        return

    time_remark = get_time_remark(args.lang)

    # 显示个性化问候
    greeting = get_time_greeting(args.lang)
    print(f"{greeting}\n")

    # 主要逻辑：默认尝试AI，失败则回退到传统模式
    if args.ai_mode != "off":
        # 显示加载提示
        loading_messages = {
            "ja": "🤖 AIスタイリストが最適なコーディネートを考案中...",
            "zh": "🤖 AI造型师正在为您搭配最佳着装...",
            "en": "🤖 AI stylist is creating your perfect outfit...",
        }
        print(loading_messages.get(args.lang, loading_messages["en"]))

        # 尝试获取AI建议
        suggestion, success, error_msg = try_ai_suggestion(
            city, temp, desc, time_remark, args.lang, args.ai_mode, args.verbose
        )

        if success:
            # AI成功
            display_ai_mode_result(
                city, temp, desc, suggestion, time_remark, args.lang, args.ai_mode
            )
            return
        else:
            # AI失败，处理回退
            if config.get("ai_fallback_enabled", True):
                handle_ai_failure(args.lang, error_msg, config)
                display_traditional_mode(
                    city, temp, desc, time_remark, args.lang, is_fallback=True
                )
            else:
                # 不允许回退，直接显示错误
                print(f"❌ AI建议获取失败：{error_msg}")
                return
    else:
        # 直接使用传统模式
        display_traditional_mode(
            city, temp, desc, time_remark, args.lang, is_fallback=False
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 さようなら！")
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}")
        print("詳細な情報が必要な場合は --verbose フラグを使用してください。")
