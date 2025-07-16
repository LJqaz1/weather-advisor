
import argparse
import os
from dotenv import load_dotenv
from weather_advisor.advisor import get_weather, get_clothing_suggestion
from weather_advisor.utils import get_time_remark, format_weather_tip, get_city_by_ip


def get_args():
    """
    解析命令行参数，支持自定义城市查询
    """
    parser = argparse.ArgumentParser(description="天气穿衣助手")
    parser.add_argument('--city', type=str, default='Tokyo', help='查询的城市名称（默认：Tokyo）')
    return parser.parse_args()

# 自动加载项目根目录下的 .env 文件
load_dotenv()

# 读取变量
api_key = os.getenv("OPENWEATHER_API_KEY")
debug_mode = os.getenv("DEBUG_MODE", "False") == "True"
default_city = os.getenv("DEFAULT_CITY", "Tokyo")

def run():
    args = get_args()
    city = args.city if args.city else get_city_by_ip()
    if not api_key:
            print("❌ 未找到 API 密钥，请在 .env 文件中设置 OPENWEATHER_API_KEY")
            return
    print(f"使用城市：{default_city}")
    print(f"当前模式：{'调试' if debug_mode else '正式'}")
    print(f"API 密钥：{api_key[:5]}*****")

    temp, desc = get_weather(city, api_key)
    if temp is None:
            print("抱歉，无法获取天气数据。")
            return

    wear_tip = get_clothing_suggestion(temp, desc)
    time_tip = get_time_remark()

    result = format_weather_tip(city, temp, desc, wear_tip, time_tip)
    print(result)

if __name__ == "__main__":
    run()