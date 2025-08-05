# 天气穿衣顾问 🌤️👔

基于 AI 的多语言天气穿衣建议应用程序。根据实时天气信息，为您提供最合适的穿衣建议。

## ✨ 核心功能

- 🌍 **多语言支持**: 支持中文、日语、英语三种语言
- 🤖 **AI 智能建议**: 使用 Ollama + Gemma 模型提供详细的穿衣建议
- 🌤️ **实时天气数据**: 集成 OpenWeatherMap API 获取准确天气信息
- 🏙️ **全球城市支持**: 支持世界各地城市（自动识别中文城市名）
- ⚡ **本地运行**: 完全私密且高效的 AI 处理，无需外部 API 调用

## 🛠️ 系统要求

### 基本要求
- Python 3.8+
- 8GB RAM 以上（使用 Gemma 7B 时）
- 网络连接（获取天气数据）

### 推荐配置
- 16GB RAM
- SSD 存储
- 多核 CPU

## 📦 安装教程

### 1. 克隆项目
```bash
git clone <your-repository-url>
cd weather-advisor
```

### 2. 创建虚拟环境
```bash
python -m venv weather-advisor
source weather-advisor/bin/activate  # Linux/macOS
# 或者
weather-advisor\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 安装和配置 Ollama

#### 安装 Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows 用户
# 请访问 https://ollama.ai/download/windows 下载安装
```

#### 下载 Gemma 模型
```bash
# 启动 Ollama 服务
ollama serve

# 在新终端中下载模型
ollama pull gemma:7b    # 推荐版本（性能与质量平衡）
# 或者
ollama pull gemma:2b    # 轻量版本（4GB RAM 也能运行）
```

### 5. 环境配置

创建 `.env` 文件并配置以下内容：

```env
# OpenWeather API 密钥（必需）
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Ollama 配置
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=gemma:7b

# 默认设置
DEFAULT_CITY=Tokyo
DEBUG_MODE=False
```

#### 获取 OpenWeather API 密钥
1. 访问 [OpenWeatherMap](https://openweathermap.org/api)
2. 注册免费账户
3. 获取 API 密钥并配置到 `.env` 文件

## 🚀 使用指南

### 基础使用
```bash
# 基本运行（中文，东京）
python main.py --lang zh

# 使用 AI 模式
python main.py --ai-mode ollama --lang zh

# 指定城市
python main.py --city 北京 --ai-mode ollama --lang zh
```

### 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--city` | 指定查询城市 | `--city 上海` |
| `--ai-mode` | 选择 AI 模式 | `--ai-mode ollama` |
| `--lang` | 选择语言 | `--lang zh` |
| `--verbose` | 显示详细信息 | `--verbose` |

### 使用示例

```bash
# 中文北京天气
python main.py --city 北京 --ai-mode ollama --lang zh

# 英文纽约天气
python main.py --city "New York" --ai-mode ollama --lang en

# 日语东京天气
python main.py --city 東京 --ai-mode ollama --lang ja

# 详细模式运行
python main.py --city 上海 --ai-mode ollama --lang zh --verbose
```

## 🎯 输出示例

### 传统穿衣建议
```
🌤️  北京天气信息
气温: 21.5℃
天气: 多云
💡 穿衣建议: 建议穿轻薄外套或长袖衬衫
⏰ 晚上气温会下降
```

### AI 智能穿衣建议
```
🤖 调用 Ollama 模型中... (模型: gemma:latest)
🌟 AI穿衣建议：建议穿透气的短袖衬衫搭配薄款防晒外套，下身选择轻便的休闲裤，别忘了佩戴遮阳帽和太阳镜。
```

## 🔧 常见问题解决

### 故障排除指南

#### 1. Ollama 连接失败
```bash
❌ 无法连接到 Ollama 服务
```

**解决方案:**
```bash
# 检查 Ollama 服务是否运行
ollama serve

# 在另一个终端测试连接
curl http://localhost:11434/api/tags
```

#### 2. 模型未找到
```bash
❌ 模型 'gemma:7b' 未找到
```

**解决方案:**
```bash
# 查看已安装的模型
ollama list

# 下载需要的模型
ollama pull gemma:7b

# 或更新 .env 文件中的模型名称
OLLAMA_MODEL=gemma:latest
```

#### 3. API 密钥错误
```bash
❌ 未找到 API 密钥
```

**解决方案:**
1. 在 OpenWeatherMap 创建账户
2. 获取免费 API 密钥
3. 在 `.env` 文件中设置 `OPENWEATHER_API_KEY=你的密钥`

#### 4. 内存不足
```bash
❌ 内存不足
```

**解决方案:**
```bash
# 使用更小的模型
ollama pull gemma:2b

# 更新 .env 文件
OLLAMA_MODEL=gemma:2b
```

## 🎛️ 高级配置

### Gemma 模型选择指南

| 模型版本 | 内存需求 | 运行速度 | 建议质量 | 适用场景 |
|----------|----------|----------|----------|----------|
| gemma:2b | 4GB+ | 快速 | 良好 | 低配置设备 |
| gemma:7b | 8GB+ | 中等 | 优秀 | 推荐使用 |
| gemma:9b | 16GB+ | 较慢 | 非常优秀 | 高质量需求 |

### 自定义配置

#### 1. AI 参数调优
在 `weather_advisor/ai_suggester.py` 的 `call_ollama_gemma` 函数中调整：

```python
"options": {
    "temperature": 0.7,     # 创造性 (0.0-1.0)
    "top_p": 0.9,          # 核心采样
    "num_predict": 150     # 最大输出长度
}
```

#### 2. 城市名映射扩展
在 `weather_advisor/utils.py` 的 `normalize_city` 函数中添加：

```python
city_mapping = {
    '北京': 'Beijing',
    '上海': 'Shanghai',
    '深圳': 'Shenzhen',
    '广州': 'Guangzhou'
}
```

## 📋 开发与测试

### 独立测试功能
```bash
# 测试 AI 建议功能
python -m weather_advisor.ai_suggester --ai-mode ollama --lang zh

# 自定义参数测试
python -m weather_advisor.ai_suggester \
  --city 北京 \
  --temp 25 \
  --desc "晴天" \
  --ai-mode ollama \
  --lang zh
```

### 调试模式
```bash
# 启用详细调试信息
DEBUG_MODE=True python main.py --verbose --lang zh
```

## 🌟 支持的城市

应用支持全球城市查询，并自动处理中文城市名：

### 国内主要城市
- 北京 → Beijing
- 上海 → Shanghai  
- 广州 → Guangzhou
- 深圳 → Shenzhen
- 杭州 → Hangzhou
- 成都 → Chengdu

### 国际城市
- 东京 → Tokyo
- 纽约 → New York
- 伦敦 → London
- 巴黎 → Paris

## 🔮 后续计划

- [ ] 添加一周天气预报
- [ ] 服装搭配图片生成
- [ ] 用户偏好设置保存
- [ ] 地区服装文化适配
- [ ] 手机应用版本
- [ ] Web 网页界面
- [ ] 微信小程序版本

## 🤝 参与贡献

欢迎提交 Pull Request 和 Issue！

### 开发环境设置
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 代码格式化
black .
flake8 .

# 运行测试
pytest
```

## 📄 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [OpenWeatherMap](https://openweathermap.org/) - 提供天气数据 API
- [Ollama](https://ollama.ai/) - 本地大语言模型运行环境
- [Google Gemma](https://ai.google.dev/gemma) - AI 模型支持

## 📞 技术支持

遇到问题时：

1. 查看[常见问题解决](#-常见问题解决)部分
2. 在 [Issues](https://github.com/your-repo/issues) 中搜索相关问题
3. 创建新 Issue 并提供详细信息

## 💡 使用技巧

### 提高响应速度
- 保持 Ollama 服务持续运行
- 首次使用时模型加载需要 1-2 分钟
- 使用 SSD 存储可显著提升模型加载速度

### 节省资源
- 在低配置设备上使用 `gemma:2b`
- 不使用时可以停止 Ollama 服务：`pkill ollama`

### 最佳体验
- 建议在 16GB RAM 设备上使用 `gemma:7b`
- 可以同时运行多个语言版本进行对比

---

**享受智能天气穿衣建议吧！** 🌈👕