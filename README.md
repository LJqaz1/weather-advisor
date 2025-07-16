# 天气穿衣助手（Weather Clothing Advisor）

一个基于 Python 的命令行小工具，可自动获取城市天气，并根据气温和时间段智能推荐穿衣建议。

---

## 🚀 功能概述

- 实时天气查询（接入 OpenWeatherMap API）
- 根据气温 + 天气状况给出穿衣建议
- 自动判断早/中/晚时间段，提示注意事项
- 支持命令行参数自定义城市
- 支持 IP 地理定位，自动识别当前城市
- 使用 `.env` 文件安全读取密钥

---

## 🧰 项目结构
your_project/ 
├── main.py                  # 程序入口
├── weather_advisor/         # 核心模块目录 
│   ├── advisor.py           # 获取天气 + 穿衣逻辑
│   └── utils.py             # 时间段判断 + 格式化输出 ├── .env                     # 环境变量
├── requirements.txt         # 项目依赖清单

---

## 🛠️ 安装使用

### 1️⃣ 克隆项目 & 创建虚拟环境

git clone https://your-repo-url
cd your_project
python3 -m venv venv
source venv/bin/activate

### 2️⃣ 安装依赖
pip install -r requirements.txt


### 3️⃣ 配置 .env 文件（在项目根目录）
OPENWEATHER_API_KEY=你的API密钥


### 4️⃣ 运行程序
自动识别当前城市：
python3 main.py

指定城市运行：
python3 main.py --city "Osaka"

---

## 📸 示例演示

输入命令：
python3 main.py --city "Tokyo"

输出结果示例：
Tokyo 当前气温：28°C，天气：晴朗 ☀️
穿衣建议：穿短袖、短裤，记得防晒😎。中午气温较稳定，适合出行🌤


自动定位城市运行：
python3 main.py


输出示例（根据当前 IP）：
Shinjuku 当前气温：22°C，天气：小雨 🌧
穿衣建议：穿长袖或薄外套👕，记得带伞☔。晚上可能降温，建议多带一件备用衣物🌃


## 📦 依赖清单
- requests
- python-dotenv
更多依赖见 requirements.txt

## 🔮 计划迭代功能（v1.1+）
- 命令行支持单位切换（摄氏 / 华氏）
- 中文城市名自动转英文拼写
- GUI 图形界面版本
- 天气趋势预测模块
- 接入 IP 识别库以增强定位准确性

## 📬 作者信息
开发者：LJ
联系方式：可按需要添加 GitHub / 邮箱链接