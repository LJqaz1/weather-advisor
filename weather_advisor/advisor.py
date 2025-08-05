# weather_advisor/advisor.py
import requests
from typing import Tuple, Optional

def get_weather(city: str, api_key: str) -> Tuple[Optional[float], Optional[str]]:
    """
    获取天气信息
    返回: (温度, 天气描述)
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',  # 使用摄氏度
            'lang': 'ja'  # 日语描述
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        
        return temp, desc
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求错误: {e}")
        return None, None
    except KeyError as e:
        print(f"❌ API响应格式错误: {e}")
        return None, None
    except Exception as e:
        print(f"❌ 获取天气数据失败: {e}")
        return None, None

def get_clothing_suggestion(temp: float, desc: str, lang: str = 'ja') -> str:
    """
    根据温度和天气描述给出穿衣建议
    """
    suggestions = {
        'ja': {
            'very_cold': 'ダウンジャケットやコート、手袋、マフラーをお忘れなく',
            'cold': 'ジャケットやセーターで暖かく過ごしましょう',
            'cool': '薄手のジャケットや長袖シャツがおすすめです',
            'mild': '長袖シャツや軽いカーディガンが快適です',
            'warm': '半袖シャツや薄手の服装で十分です',
            'hot': '涼しい服装と日焼け対策をお忘れなく',
            'rainy': '雨具をお持ちください'
        },
        'zh': {
            'very_cold': '建议穿羽绒服或大衣，别忘了手套和围巾',
            'cold': '建议穿夹克或毛衣保暖',
            'cool': '建议穿轻薄外套或长袖衬衫',
            'mild': '长袖衬衫或轻薄开衫比较舒适',
            'warm': '短袖衬衫或薄衣服就足够了',
            'hot': '穿凉爽服装，注意防晒',
            'rainy': '请携带雨具'
        },
        'en': {
            'very_cold': 'Wear a down jacket or coat, don\'t forget gloves and scarf',
            'cold': 'A jacket or sweater will keep you warm',
            'cool': 'A light jacket or long-sleeve shirt is recommended',
            'mild': 'Long-sleeve shirt or light cardigan is comfortable',
            'warm': 'Short-sleeve shirt or light clothing is sufficient',
            'hot': 'Wear cool clothing and don\'t forget sun protection',
            'rainy': 'Please bring rain gear'
        }
    }
    
    suggestion_set = suggestions.get(lang, suggestions['ja'])
    
    # 温度分级判断
    if temp < 5:
        suggestion = suggestion_set['very_cold']
    elif temp < 10:
        suggestion = suggestion_set['cold']
    elif temp < 15:
        suggestion = suggestion_set['cool']
    elif temp < 20:
        suggestion = suggestion_set['mild']
    elif temp < 25:
        suggestion = suggestion_set['warm']
    else:
        suggestion = suggestion_set['hot']
    
    # 天气特殊情况处理
    if 'rain' in desc.lower() or '雨' in desc:
        suggestion += f"。{suggestion_set['rainy']}"
    
    return suggestion