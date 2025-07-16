import sys
import os

# 添加项目根目录到 Python 路径（解决模块导入问题）
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_advisor.utils import get_time_remark, is_weekend, format_weather_tip

# 模拟输入
city = "Tokyo"
temperature = 21
description = "晴朗"
wear_tip = "穿长袖或薄外套👕"
time_tip = get_time_remark()

# 输出测试结果
print("是否周末：", is_weekend())
print("时间段提醒：", time_tip)
print("天气提示：")
print(format_weather_tip(city, temperature, description, wear_tip, time_tip))