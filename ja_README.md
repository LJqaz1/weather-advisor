# 天気服装アドバイザー 🌤️👔

AI を活用した多言語対応の天気服装アドバイスアプリケーションです。現在の天気情報に基づいて、最適な服装を提案します。

## ✨ 主な機能

- 🌍 **多言語対応**: 日本語、中国語、英語に対応
- 🤖 **AI 服装アドバイス**: Ollama + Gemma モデルによる詳細な服装提案
- 🌤️ **リアルタイム天気情報**: OpenWeatherMap API 連携
- 🏙️ **都市名対応**: 世界中の都市に対応（中国語・日本語の都市名も自動変換）
- ⚡ **ローカル実行**: 完全にプライベートで高速な AI 処理

## 🛠️ システム要件

### 必須環境
- Python 3.8+
- 8GB RAM 以上（Gemma 7B 使用時）
- インターネット接続（天気情報取得用）

### 推奨環境
- 16GB RAM
- SSD ストレージ
- マルチコア CPU

## 📦 インストール手順

### 1. リポジトリのクローン
```bash
git clone <your-repository-url>
cd weather-advisor
```

### 2. Python 仮想環境の作成
```bash
python -m venv weather-advisor
source weather-advisor/bin/activate  # Linux/macOS
# または
weather-advisor\Scripts\activate  # Windows
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. Ollama のインストールと設定

#### Ollama のインストール
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows の場合
# https://ollama.ai/download/windows からダウンロード
```

#### Gemma モデルのダウンロード
```bash
# Ollama サービスの開始
ollama serve

# 別のターミナルで Gemma モデルをダウンロード
ollama pull gemma:7b    # 推奨（バランス型）
# または
ollama pull gemma:2b    # 軽量版（4GB RAM でも動作）
```

### 5. 環境設定

`.env` ファイルを作成し、以下の内容を設定：

```env
# OpenWeather API キー（必須）
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Ollama 設定
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=gemma:7b

# デフォルト設定
DEFAULT_CITY=Tokyo
DEBUG_MODE=False
```

#### OpenWeather API キーの取得
1. [OpenWeatherMap](https://openweathermap.org/api) にアクセス
2. 無料アカウントを作成
3. API キーを取得して `.env` ファイルに設定

## 🚀 使用方法

### 基本的な使用
```bash
# 基本実行（日本語、東京）
python main.py

# AI モードで実行
python main.py --ai-mode ollama --lang ja

# 都市を指定
python main.py --city Osaka --ai-mode ollama --lang ja
```

### コマンドオプション

| オプション | 説明 | 例 |
|-----------|------|-----|
| `--city` | 都市名を指定 | `--city Tokyo` |
| `--ai-mode` | AI モード選択 | `--ai-mode ollama` |
| `--lang` | 言語選択 | `--lang ja` |
| `--verbose` | 詳細情報表示 | `--verbose` |

### 使用例

```bash
# 日本語での基本使用
python main.py --city 東京 --ai-mode ollama --lang ja

# 英語でニューヨークの天気
python main.py --city "New York" --ai-mode ollama --lang en

# 中文で北京の天気
python main.py --city 北京 --ai-mode ollama --lang zh

# 詳細情報付きで実行
python main.py --city Tokyo --ai-mode ollama --lang ja --verbose
```

## 🎯 出力例

### 従来の服装アドバイス
```
🌤️  Tokyoの天気情報
気温: 21.5℃
天気: 曇り
💡 服装アドバイス: 薄手のジャケットや長袖シャツがおすすめです
⏰ 夜は冷え込むでしょう
```

### AI による服装アドバイス
```
🤖 調用 Ollama 模型中... (模型: gemma:latest)
🌟 AI服装アドバイス：短袖の速乾性素材を使用した軽度なトップと、ストレッチ性のあるジョガーパンツの組み合わせが最適です。
```

## 🔧 トラブルシューティング

### よくある問題と解決方法

#### 1. Ollama 接続エラー
```bash
❌ 無法连接到 Ollama 服务
```

**解決方法:**
```bash
# Ollama サービスが起動しているか確認
ollama serve

# 別のターミナルで接続テスト
curl http://localhost:11434/api/tags
```

#### 2. モデルが見つからない
```bash
❌ 模型 'gemma:7b' 未找到
```

**解決方法:**
```bash
# 利用可能なモデルを確認
ollama list

# 必要なモデルをダウンロード
ollama pull gemma:7b

# または .env ファイルのモデル名を更新
OLLAMA_MODEL=gemma:latest
```

#### 3. API キーエラー
```bash
❌ API キーが見つかりません
```

**解決方法:**
1. OpenWeatherMap でアカウント作成
2. API キーを取得
3. `.env` ファイルに `OPENWEATHER_API_KEY=your_key` を設定

#### 4. メモリ不足
```bash
❌ メモリが不足しています
```

**解決方法:**
```bash
# より小さなモデルを使用
ollama pull gemma:2b

# .env ファイルを更新
OLLAMA_MODEL=gemma:2b
```

## 🎛️ 高度な設定

### Gemma モデルの選択指針

| モデル | RAM 要件 | 速度 | 品質 | 用途 |
|--------|----------|------|------|------|
| gemma:2b | 4GB+ | 高速 | 良好 | 軽量環境 |
| gemma:7b | 8GB+ | 中程度 | 優秀 | 推奨 |
| gemma:9b | 16GB+ | やや遅い | 非常に優秀 | 高品質 |

### カスタム設定

#### 1. AI パラメータの調整
`weather_advisor/ai_suggester.py` の `call_ollama_gemma` 関数内：

```python
"options": {
    "temperature": 0.7,      # 創造性 (0.0-1.0)
    "top_p": 0.9,           # 核心サンプリング
    "num_predict": 150      # 最大出力長
}
```

#### 2. 都市名マッピングの追加
`weather_advisor/utils.py` の `normalize_city` 関数：

```python
city_mapping = {
    '東京': 'Tokyo',
    '大阪': 'Osaka',
    'カスタム都市': 'Custom City'
}
```

## 📋 開発・テスト

### 独立テスト
```bash
# AI 機能の単体テスト
python -m weather_advisor.ai_suggester --ai-mode ollama --lang ja

# 特定の条件でテスト
python -m weather_advisor.ai_suggester \
  --city Tokyo \
  --temp 25 \
  --desc "sunny" \
  --ai-mode ollama \
  --lang ja
```

### デバッグモード
```bash
# デバッグ情報を表示
DEBUG_MODE=True python main.py --verbose
```

## 🔮 今後の改善予定(1.2+)

- [ ] 週間予報対応
- [ ] 服装写真の生成
- [ ] ユーザー設定の保存
- [ ] 地域特有の服装文化対応
- [ ] モバイルアプリ版
- [ ] Web インターフェース

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します！

### 開発環境のセットアップ
```bash
# 開発用依存関係のインストール
pip install -r requirements-dev.txt

# コードフォーマット
black .
flake8 .

# テスト実行
pytest
```

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照

## 🙏 謝辞

- [OpenWeatherMap](https://openweathermap.org/) - 天気データ API
- [Ollama](https://ollama.ai/) - ローカル LLM 実行環境
- [Google Gemma](https://ai.google.dev/gemma) - AI モデル

## 📞 サポート

問題が発生した場合：

1. [トラブルシューティング](#-トラブルシューティング) を確認
2. [Issues](https://github.com/LJqaz1/weather-advisor.git) で既存の問題を検索
3. 新しい Issue を作成して詳細を報告

---

**楽しい天気服装アドバイスライフを！** 🌈👕