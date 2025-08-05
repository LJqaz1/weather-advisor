# weather_advisor/utils.py
import datetime
import requests
from typing import Tuple, Optional

def get_time_remark(lang: str = 'ja') -> str:
    """
    根据当前时间返回时间段描述
    """
    current_hour = datetime.datetime.now().hour
    
    time_remarks = {
        'ja': {
            'morning': '朝は涼しいです',
            'afternoon': '日中は暖かくなります', 
            'evening': '夜は冷え込むでしょう'
        },
        'zh': {
            'morning': '早上比较凉爽',
            'afternoon': '下午会比较温暖',
            'evening': '晚上气温会下降'
        },
        'en': {
            'morning': 'Morning temperatures are cool',
            'afternoon': 'Afternoon will be warmer',
            'evening': 'Evening temperatures expected to drop'
        }
    }
    
    remarks = time_remarks.get(lang, time_remarks['ja'])
    
    if 6 <= current_hour < 12:
        return remarks['morning']
    elif 12 <= current_hour < 18:
        return remarks['afternoon']
    else:
        return remarks['evening']

def format_weather_tip(city: str, temp: float, desc: str, suggestion: str, 
                      time_tip: str, lang: str = 'ja') -> str:
    """
    格式化天气提示信息
    """
    templates = {
        'ja': f"""🌤️  {city}の天気情報
気温: {temp}℃
天気: {desc}
💡 服装アドバイス: {suggestion}
⏰ {time_tip}""",

        'zh': f"""🌤️  {city}天气信息
气温: {temp}℃
天气: {desc}
💡 穿衣建议: {suggestion}
⏰ {time_tip}""",

        'en': f"""🌤️  Weather in {city}
Temperature: {temp}℃
Weather: {desc}
💡 Clothing Advice: {suggestion}
⏰ {time_tip}"""
    }
    
    return templates.get(lang, templates['ja'])

def get_city_by_ip() -> str:
    """
    通过IP获取城市信息（简单实现）
    """
    try:
        response = requests.get('http://ipapi.co/city/', timeout=5)
        return response.text.strip() or "Tokyo"
    except:
        return "Tokyo"

def normalize_city(city: str) -> str:
    """
    城市名称标准化映射
    """
    city_mapping = {
        '东京': 'Tokyo',
        '北京': 'Beijing',
        '上海': 'Shanghai',
        '大阪': 'Osaka',
        '纽约': 'New York',
        '伦敦': 'London',
        'とうきょう': 'Tokyo',
        'おおさか': 'Osaka'
    }
    
    return city_mapping.get(city, city)