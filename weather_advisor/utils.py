from datetime import datetime

def get_time_remark():
    """
    根据当前系统时间判断是早上、中午或晚上，返回提示语。
    """
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "早上出门，气温可能偏凉，要注意保暖🌅"
    elif 12 <= hour < 17:
        return "中午气温较稳定，适合出行🌤"
    else:
        return "晚上可能降温，建议多带一件备用衣物🌃"

def is_weekend():
    """
    判断今天是否是周六或周日，返回布尔值。
    """
    weekday = datetime.now().weekday()  # 0=周一，6=周日
    return weekday >= 5

def format_weather_tip(city, temp, desc, wear_tip, time_tip):
    """
    构造完整的天气提示语句，将各部分信息格式化组合。
    """
    weekend_label = "（周末）" if is_weekend() else ""
    tip = f"{city} 当前气温：{temp}°C，天气：{desc} {weekend_label}\n"
    tip += f"穿衣建议：{wear_tip}。{time_tip}"
    return tip

import requests

def get_city_by_ip():
    try:
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()
        return data.get("city", "Tokyo")
    except Exception:
        return "Tokyo"  # 默认城市