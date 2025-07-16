import requests

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_cn"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return temp, desc
    else:
        print("天气数据获取失败：", data.get("message", "未知错误"))
        return None, None
    
def get_clothing_suggestion(temp, description):
    if temp is None:
        return "无法提供穿衣建议 🥲"

    if temp <= 5:
        suggestion = "穿羽绒服、围巾和帽子🧥🧣"
    elif temp <= 15:
        suggestion = "穿风衣或毛衣🧥"
    elif temp <= 25:
        suggestion = "穿长袖或薄外套👕"
    else:
        suggestion = "穿短袖、短裤，记得防晒😎"

    if "雨" in description:
        suggestion += "，记得带伞☔"

    return suggestion