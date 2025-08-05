# weather_advisor/utils.py
import datetime
import requests
import calendar
from typing import Tuple, Optional, Dict, Any


def get_time_greeting(lang: str = "ja") -> str:
    """根据时间段返回问候语"""
    current_hour = datetime.datetime.now().hour

    greetings = {
        "ja": {
            "morning": "おはようございます！☀️",  # 5-11
            "afternoon": "こんにちは！🌤️",  # 12-17
            "evening": "こんばんは！🌙",  # 18-23
            "night": "夜分遅くにすみません 🌃",  # 0-4
        },
        "zh": {
            "morning": "早上好！☀️",
            "afternoon": "下午好！🌤️",
            "evening": "晚上好！🌙",
            "night": "夜深了，注意休息 🌃",
        },
        "en": {
            "morning": "Good morning! ☀️",
            "afternoon": "Good afternoon! 🌤️",
            "evening": "Good evening! 🌙",
            "night": "Good night! 🌃",
        },
    }

    if 5 <= current_hour <= 11:
        period = "morning"
    elif 12 <= current_hour <= 17:
        period = "afternoon"
    elif 18 <= current_hour <= 23:
        period = "evening"
    else:
        period = "night"

    return greetings.get(lang, greetings["ja"])[period]


def get_time_remark(lang: str = "ja") -> str:
    """根据当前时间返回时间段描述 - 保持原有功能但增强内容"""
    current_hour = datetime.datetime.now().hour
    now = datetime.datetime.now()

    # 增强版时间描述，包含更多细节
    time_remarks = {
        "ja": {
            "early_morning": "早朝は肌寒く感じるでしょう",  # 5-7
            "morning": "朝は涼しく、過ごしやすい気温です",  # 8-11
            "noon": "正午頃が一日で最も暖かくなります",  # 12-13
            "afternoon": "午後は日差しが強く、暖かくなります",  # 14-17
            "evening": "夕方から気温が下がり始めます",  # 18-20
            "night": "夜は冷え込むでしょう",  # 21-23
            "late_night": "深夜は一日で最も寒くなります",  # 0-4
        },
        "zh": {
            "early_morning": "清晨会感到有些凉意",
            "morning": "早上凉爽舒适",
            "noon": "正午时分是全天最暖和的时候",
            "afternoon": "下午阳光较强，比较温暖",
            "evening": "傍晚开始降温",
            "night": "晚上气温会下降",
            "late_night": "深夜是全天最冷的时候",
        },
        "en": {
            "early_morning": "Early morning will feel quite cool",
            "morning": "Morning temperatures are cool and comfortable",
            "noon": "Noon will be the warmest time of day",
            "afternoon": "Afternoon will be warm with strong sunshine",
            "evening": "Evening temperatures start to drop",
            "night": "Night temperatures expected to drop",
            "late_night": "Late night will be the coolest time",
        },
    }

    remarks = time_remarks.get(lang, time_remarks["ja"])

    if 5 <= current_hour <= 7:
        return remarks["early_morning"]
    elif 8 <= current_hour <= 11:
        return remarks["morning"]
    elif 12 <= current_hour <= 13:
        return remarks["noon"]
    elif 14 <= current_hour <= 17:
        return remarks["afternoon"]
    elif 18 <= current_hour <= 20:
        return remarks["evening"]
    elif 21 <= current_hour <= 23:
        return remarks["night"]
    else:
        return remarks["late_night"]


def get_seasonal_reminder(lang: str = "ja") -> Dict[str, str]:
    """根据当前季节返回提醒"""
    month = datetime.datetime.now().month

    # 定义季节
    if month in [12, 1, 2]:
        season = "winter"
    elif month in [3, 4, 5]:
        season = "spring"
    elif month in [6, 7, 8]:
        season = "summer"
    else:
        season = "autumn"

    seasonal_tips = {
        "ja": {
            "winter": {
                "icon": "❄️",
                "tip": "乾燥対策も忘れずに！マスクやリップクリームをお持ちください",
                "clothing": "重ね着で体温調節を上手に行いましょう",
            },
            "spring": {
                "icon": "🌸",
                "tip": "花粉症の方はマスクを忘れずに！",
                "clothing": "朝晩の寒暖差にご注意ください。カーディガンがあると便利です",
            },
            "summer": {
                "icon": "🌻",
                "tip": "熱中症対策を！こまめな水分補給を心がけてください",
                "clothing": "UV対策も大切です。帽子や日焼け止めをお忘れなく",
            },
            "autumn": {
                "icon": "🍂",
                "tip": "朝晩が涼しくなってきました。風邪にご注意を",
                "clothing": "薄手のジャケットが活躍する季節です",
            },
        },
        "zh": {
            "winter": {
                "icon": "❄️",
                "tip": "注意保湿！建议携带口罩和润唇膏",
                "clothing": "多层穿搭，方便调节体温",
            },
            "spring": {
                "icon": "🌸",
                "tip": "花粉症患者请记得戴口罩！",
                "clothing": "注意早晚温差，建议准备开衫",
            },
            "summer": {
                "icon": "🌻",
                "tip": "预防中暑！请及时补充水分",
                "clothing": "注意防晒，别忘了帽子和防晒霜",
            },
            "autumn": {
                "icon": "🍂",
                "tip": "早晚转凉，小心感冒",
                "clothing": "薄外套是这个季节的好伙伴",
            },
        },
        "en": {
            "winter": {
                "icon": "❄️",
                "tip": "Stay hydrated! Consider bringing a mask and lip balm",
                "clothing": "Layer up for easy temperature adjustment",
            },
            "spring": {
                "icon": "🌸",
                "tip": "Allergy season! Don't forget your mask",
                "clothing": "Mind the temperature difference. A cardigan would be handy",
            },
            "summer": {
                "icon": "🌻",
                "tip": "Beat the heat! Stay hydrated regularly",
                "clothing": "UV protection matters. Hat and sunscreen recommended",
            },
            "autumn": {
                "icon": "🍂",
                "tip": "Getting cooler in mornings and evenings. Watch out for colds",
                "clothing": "Light jackets are perfect for this season",
            },
        },
    }

    return seasonal_tips.get(lang, seasonal_tips["ja"])[season]


def get_regional_advice(city: str, temp: float, lang: str = "ja") -> str:
    """根据地域特色返回建议"""
    city_lower = city.lower()

    regional_tips = {
        "ja": {
            # 日本主要城市
            "tokyo": "東京は湿度が高めです。通気性の良い素材をおすすめします",
            "osaka": "大阪は風が強い日が多いです。髪型が崩れないよう帽子があると安心",
            "kyoto": "京都は盆地のため寒暖差が激しいです。調節しやすい服装を",
            "hokkaido": "北海道は予想以上に寒くなることが。厚手のコートをお忘れなく",
            "sapporo": "札幌は雪道が滑りやすいです。滑り止めのある靴がおすすめ",
            "okinawa": "沖縄の紫外線は本土より強力です。しっかりとした日焼け対策を",
            "nagoya": "名古屋は乾燥しやすい地域です。保湿対策をお願いします",
            "fukuoka": "福岡は黄砂の影響を受けやすいです。マスクの準備を",
            "hiroshima": "広島は瀬戸内海の影響で湿度が高めです",
            "sendai": "仙台は東北の中では温暖ですが、風が強い日があります",
            # 海外都市
            "london": "ロンドンは急な雨が多いです。折りたたみ傘をお持ちください",
            "paris": "パリの石畳は歩きにくいです。履きなれた靴がおすすめ",
            "new york": "ニューヨークは風が強いエリアがあります。風対策を",
            "shanghai": "上海は湿度が高く、汗をかきやすいです。替えのシャツがあると安心",
            "seoul": "ソウルは大気汚染に注意。マスクの着用をおすすめします",
            "singapore": "シンガポールは一年中高温多湿。軽くて通気性の良い服装を",
        },
        "zh": {
            "beijing": "北京风沙较大，建议戴口罩保护",
            "shanghai": "上海湿度较高，选择透气面料",
            "guangzhou": "广州紫外线强烈，注意防晒",
            "shenzhen": "深圳多雨，建议携带雨具",
            "chengdu": "成都湿气重，注意防潮",
            "hangzhou": "杭州四季分明，注意温差变化",
            "nanjing": "南京夏热冬冷，选择合适厚度的衣物",
            "tokyo": "东京湿度偏高，建议选择透气材质",
            "osaka": "大阪风力较强，注意帽子固定",
            "london": "伦敦多阵雨，记得带伞",
            "paris": "巴黎石板路较多，选择舒适鞋子",
            "new york": "纽约部分区域风大，注意防风",
            "seoul": "首尔空气质量需关注，建议戴口罩",
        },
        "en": {
            "london": "London has frequent showers. Bring an umbrella!",
            "paris": "Paris cobblestones can be tricky. Wear comfortable shoes",
            "new york": "NYC can be windy between buildings. Layer up!",
            "tokyo": "Tokyo tends to be humid. Choose breathable fabrics",
            "beijing": "Beijing can be dusty. Consider wearing a mask",
            "shanghai": "Shanghai is quite humid. Moisture-wicking clothes recommended",
            "sydney": "Sydney sun is strong. Don't forget sunscreen!",
            "singapore": "Singapore is hot and humid year-round. Light, airy clothes work best",
            "seoul": "Seoul air quality varies. A mask might be helpful",
            "bangkok": "Bangkok is extremely hot and humid. Lightest possible clothing recommended",
        },
    }

    # 温度相关地域建议
    temp_based_tips = {
        "ja": {
            "hot_humid": "高温多湿の地域では、速乾性のある素材がおすすめです",
            "cold_dry": "寒冷乾燥地域では、保温と保湿の両方が大切です",
            "moderate": "過ごしやすい気候ですが、急な天候変化にご注意を",
        },
        "zh": {
            "hot_humid": "高温高湿地区建议选择快干面料",
            "cold_dry": "寒冷干燥地区请注意保温保湿",
            "moderate": "气候宜人，但需防范天气突变",
        },
        "en": {
            "hot_humid": "For hot humid areas, quick-dry fabrics work best",
            "cold_dry": "Cold dry regions require both warmth and moisture protection",
            "moderate": "Pleasant weather, but watch for sudden changes",
        },
    }

    # 查找城市特定建议
    tips = regional_tips.get(lang, regional_tips["en"])
    for city_key in tips:
        if city_key in city_lower:
            return f"🗺️ {tips[city_key]}"

    # 根据温度返回通用地域建议
    temp_tips = temp_based_tips.get(lang, temp_based_tips["en"])
    if temp > 25:
        return f"🗺️ {temp_tips['hot_humid']}"
    elif temp < 10:
        return f"🗺️ {temp_tips['cold_dry']}"
    else:
        return f"🗺️ {temp_tips['moderate']}"


def format_weather_tip(
    city: str, temp: float, desc: str, suggestion: str, time_tip: str, lang: str = "ja"
) -> str:
    """格式化天气提示信息 - 增强版显示"""
    separator = "─" * 35

    templates = {
        "ja": f"""{separator}
🌤️  {city}の天気情報
🌡️ 気温: {temp}℃
☁️ 天気: {desc}
⏰ {time_tip}

{separator}
💡 服装アドバイス
{suggestion}

{separator}""",
        "zh": f"""{separator}
🌤️  {city}天气信息
🌡️ 气温: {temp}℃
☁️ 天气: {desc}
⏰ {time_tip}

{separator}
💡 穿衣建议
{suggestion}

{separator}""",
        "en": f"""{separator}
🌤️  Weather in {city}
🌡️ Temperature: {temp}℃
☁️ Weather: {desc}
⏰ {time_tip}

{separator}
💡 Clothing Advice
{suggestion}

{separator}""",
    }

    return templates.get(lang, templates["ja"])


def format_personalized_weather_display(
    city: str,
    temp: float,
    desc: str,
    suggestion: str,
    time_remark: str,
    lang: str = "ja",
) -> str:
    """整合所有个性化元素的完整显示"""

    # 1. 时间问候
    greeting = get_time_greeting(lang)

    # 2. 季节提醒
    seasonal = get_seasonal_reminder(lang)

    # 3. 地域建议
    regional = get_regional_advice(city, temp, lang)

    # 组装完整信息
    separator = "─" * 35

    weather_labels = {
        "ja": "📊 本日の天気情報",
        "zh": "📊 今日天气信息",
        "en": "📊 Today's Weather Info",
    }

    styling_labels = {
        "ja": "🌟 本日のスタイリング提案",
        "zh": "🌟 今日造型建议",
        "en": "🌟 Today's Styling Suggestion",
    }

    seasonal_labels = {
        "ja": "季節のワンポイント",
        "zh": "季节小贴士",
        "en": "Seasonal Tips",
    }

    closing_labels = {
        "ja": "✨ 素敵な一日をお過ごしください！",
        "zh": "✨ 祝您有美好的一天！",
        "en": "✨ Have a wonderful day!",
    }

    output = f"""
{greeting}

{separator}
{weather_labels.get(lang, weather_labels['ja'])}
🏙️ {city} | 🌡️ {temp}°C | {desc}
{f"⏰ {time_remark}" if time_remark else ""}

{separator}
{styling_labels.get(lang, styling_labels['ja'])}
💡 {suggestion}

{separator}
{seasonal['icon']} {seasonal_labels.get(lang, seasonal_labels['ja'])}
💭 {seasonal['tip']}
👔 {seasonal['clothing']}

{separator}
{regional}

{separator}
{closing_labels.get(lang, closing_labels['ja'])}
"""

    return output.strip()


def get_city_by_ip() -> str:
    """通过IP获取城市信息 - 增强版实现"""
    try:
        # 尝试多个IP定位服务，提高成功率
        services = [
            "http://ipapi.co/city/",
            "https://ipinfo.io/city",
            "http://ip-api.com/line?fields=city",
        ]

        for service in services:
            try:
                response = requests.get(service, timeout=3)
                if response.status_code == 200:
                    city = response.text.strip()
                    if city and city != "Unknown":
                        return normalize_city(city)
            except:
                continue

        return "Tokyo"  # 默认城市
    except:
        return "Tokyo"


def normalize_city(city: str) -> str:
    """城市名称标准化映射 - 扩展版"""
    city_mapping = {
        # 中文映射
        "东京": "Tokyo",
        "北京": "Beijing",
        "上海": "Shanghai",
        "广州": "Guangzhou",
        "深圳": "Shenzhen",
        "成都": "Chengdu",
        "杭州": "Hangzhou",
        "南京": "Nanjing",
        "大阪": "Osaka",
        "纽约": "New York",
        "伦敦": "London",
        "巴黎": "Paris",
        "首尔": "Seoul",
        "新加坡": "Singapore",
        # 日文映射
        "とうきょう": "Tokyo",
        "おおさか": "Osaka",
        "きょうと": "Kyoto",
        "なごや": "Nagoya",
        "ふくおか": "Fukuoka",
        "さっぽろ": "Sapporo",
        "ひろしま": "Hiroshima",
        "せんだい": "Sendai",
        # 英文别名映射
        "NYC": "New York",
        "LA": "Los Angeles",
        "SF": "San Francisco",
        "DC": "Washington",
        # 处理大小写不敏感
        "tokyo": "Tokyo",
        "beijing": "Beijing",
        "shanghai": "Shanghai",
        "london": "London",
        "paris": "Paris",
        "new york": "New York",
        "los angeles": "Los Angeles",
    }

    # 先尝试直接映射
    if city in city_mapping:
        return city_mapping[city]

    # 尝试小写映射
    city_lower = city.lower()
    if city_lower in city_mapping:
        return city_mapping[city_lower]

    # 首字母大写处理
    return city.title()


def get_weather_emoji(desc: str, temp: float) -> str:
    """根据天气描述和温度返回合适的emoji"""
    desc_lower = desc.lower()

    # 天气状况emoji
    if any(word in desc_lower for word in ["sunny", "晴", "clear"]):
        return "☀️"
    elif any(word in desc_lower for word in ["cloudy", "云", "曇"]):
        return "☁️"
    elif any(word in desc_lower for word in ["rain", "雨", "雨"]):
        return "🌧️"
    elif any(word in desc_lower for word in ["snow", "雪", "雪"]):
        return "❄️"
    elif any(word in desc_lower for word in ["storm", "暴", "嵐"]):
        return "⛈️"
    elif any(word in desc_lower for word in ["fog", "霧", "雾"]):
        return "🌫️"
    elif any(word in desc_lower for word in ["wind", "风", "風"]):
        return "💨"
    else:
        # 根据温度返回默认emoji
        if temp > 25:
            return "🌤️"
        elif temp < 10:
            return "🌨️"
        else:
            return "⛅"


def validate_temperature(temp: float) -> bool:
    """验证温度范围是否合理"""
    return -50 <= temp <= 60  # 地球上合理的温度范围


def get_comfort_level(temp: float, desc: str, lang: str = "ja") -> str:
    """根据温度和天气返回舒适度评级"""
    comfort_labels = {
        "ja": {
            "very_hot": "🔥 非常に暑い",
            "hot": "🌡️ 暑い",
            "warm": "😊 暖かい",
            "comfortable": "😌 快適",
            "cool": "🍃 涼しい",
            "cold": "🧊 寒い",
            "very_cold": "🥶 非常に寒い",
        },
        "zh": {
            "very_hot": "🔥 非常炎热",
            "hot": "🌡️ 炎热",
            "warm": "😊 温暖",
            "comfortable": "😌 舒适",
            "cool": "🍃 凉爽",
            "cold": "🧊 寒冷",
            "very_cold": "🥶 严寒",
        },
        "en": {
            "very_hot": "🔥 Very Hot",
            "hot": "🌡️ Hot",
            "warm": "😊 Warm",
            "comfortable": "😌 Comfortable",
            "cool": "🍃 Cool",
            "cold": "🧊 Cold",
            "very_cold": "🥶 Very Cold",
        },
    }

    labels = comfort_labels.get(lang, comfort_labels["ja"])

    if temp > 35:
        return labels["very_hot"]
    elif temp > 28:
        return labels["hot"]
    elif temp > 22:
        return labels["warm"]
    elif temp > 18:
        return labels["comfortable"]
    elif temp > 12:
        return labels["cool"]
    elif temp > 5:
        return labels["cold"]
    else:
        return labels["very_cold"]


# 工具函数测试
if __name__ == "__main__":
    print("=== Utils 功能测试 ===")

    # 测试时间问候
    print("1. 时间问候:")
    print(get_time_greeting("ja"))

    # 测试季节提醒
    print("\n2. 季节提醒:")
    seasonal = get_seasonal_reminder("ja")
    print(f"{seasonal['icon']} {seasonal['tip']}")

    # 测试地域建议
    print("\n3. 地域建议:")
    print(get_regional_advice("Tokyo", 20, "ja"))

    # 测试城市标准化
    print("\n4. 城市标准化:")
    print(f"东京 -> {normalize_city('东京')}")
    print(f"とうきょう -> {normalize_city('とうきょう')}")

    # 测试完整显示
    print("\n5. 完整个性化显示:")
    result = format_personalized_weather_display(
        "Tokyo",
        22,
        "晴れ",
        "ライトブルーのシャツがおすすめです",
        "午後から雲が多くなる予報",
        "ja",
    )
    print(result)
