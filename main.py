# main.py
import argparse
import os
from dotenv import load_dotenv
from weather_advisor.advisor import get_weather, get_clothing_suggestion
from weather_advisor.utils import get_time_remark, format_weather_tip, get_city_by_ip, normalize_city
from weather_advisor.ai_suggester import get_ai_suggestion

def get_args():
    """
    解析命令行参数，支持自定义城市查询和语言选择
    """
    parser = argparse.ArgumentParser(description="天气穿衣助手 / Weather Clothing Advisor")
    parser.add_argument('--city', type=str, default='Tokyo', help='查询的城市名称（默认：Tokyo）')
    parser.add_argument('--ai-mode', choices=['ollama', 'local', 'openai'], 
                       help='启用 AI 推荐模式（ollama = Ollama+Gemma, openai = OpenAI API）')
    parser.add_argument('--lang', default='ja', choices=['ja', 'zh', 'en'], help='输出语言选择')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    return parser.parse_args()

def main():
    # 自动加载项目根目录下的 .env 文件
    load_dotenv()
    
    # 读取环境变量
    api_key = os.getenv("OPENWEATHER_API_KEY")
    debug_mode = os.getenv("DEBUG_MODE", "False") == "True"
    default_city = os.getenv("DEFAULT_CITY", "Tokyo")
    
    args = get_args()
    
    # 验证 API 密钥
    if not api_key:
        error_msg = {
            'ja': "❌ API キーが見つかりません。.env ファイルに OPENWEATHER_API_KEY を設定してください",
            'zh': "❌ 未找到 API 密钥，请在 .env 文件中设置 OPENWEATHER_API_KEY",
            'en': "❌ API key not found. Please set OPENWEATHER_API_KEY in .env file"
        }
        print(error_msg.get(args.lang, error_msg['en']))
        return
    
    # 使用映射后的城市名
    city = normalize_city(args.city) if args.city != 'Tokyo' else default_city
    
    if args.verbose:
        info_msg = {
            'ja': f"使用都市：{city}\n現在モード：{'デバッグ' if debug_mode else '本番'}\nAPI キー：{api_key[:5]}*****",
            'zh': f"使用城市：{city}\n当前模式：{'调试' if debug_mode else '正式'}\nAPI 密钥：{api_key[:5]}*****",
            'en': f"Using city: {city}\nCurrent mode: {'Debug' if debug_mode else 'Production'}\nAPI key: {api_key[:5]}*****"
        }
        print(info_msg.get(args.lang, info_msg['en']))

    # 获取天气数据
    temp, desc = get_weather(city, api_key)
    if temp is None:
        error_msg = {
            'ja': "申し訳ありませんが、天気データを取得できませんでした。",
            'zh': "抱歉，无法获取天气数据。",
            'en': "Sorry, unable to retrieve weather data."
        }
        print(error_msg.get(args.lang, error_msg['en']))
        return

    time_remark = get_time_remark(args.lang)

    # AI 模式激活判断
    if args.ai_mode:
        suggestion = get_ai_suggestion(city, temp, desc, time_remark, args.lang, args.ai_mode)
        if suggestion:
            ai_prefix = {
                'ja': "🌟 AI服装アドバイス：",
                'zh': "🌟 AI穿衣建议：",
                'en': "🌟 AI Clothing Suggestion:"
            }
            print(f"{ai_prefix.get(args.lang, ai_prefix['en'])}{suggestion}")
            return

    # 回退至传统推荐方式
    suggestion = get_clothing_suggestion(temp, desc, args.lang)
    result = format_weather_tip(city, temp, desc, suggestion, time_remark, args.lang)
    print(result)

if __name__ == "__main__":
    main()