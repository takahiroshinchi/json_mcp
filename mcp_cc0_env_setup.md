# CC0画像検索MCPサーバー 環境設定・セットアップガイド

## 概要
自然言語デザインカンプ作成LLMサービス向けのCC0画像検索MCPサーバーの環境構築、設定、運用方法を説明します。

## 必要要件

### システム要件
- Python 3.11+
- メモリ: 最小512MB、推奨1GB
- ディスク容量: 100MB（キャッシュ含む）
- ネットワーク: インターネット接続（API呼び出し用）

### API アクセスキー
以下のプロバイダーのAPIキーを取得してください：

#### 1. Pixabay（推奨・最優先）
- **取得方法**: [Pixabay API](https://pixabay.com/api/docs/) でアカウント作成
- **無料枠**: 5,000リクエスト/日
- **制限**: なし（完全無料）
- **設定名**: `PIXABAY_API_KEY`

#### 2. Unsplash（オプション）
- **取得方法**: [Unsplash Developers](https://unsplash.com/developers) でアプリ登録
- **無料枠**: 50リクエスト/時間
- **制限**: 商用利用時は帰属表示必要
- **設定名**: `UNSPLASH_API_KEY`

#### 3. Pexels（オプション）
- **取得方法**: [Pexels API](https://www.pexels.com/api/) でアカウント作成
- **無料枠**: 200リクエスト/時間
- **制限**: 帰属表示推奨
- **設定名**: `PEXELS_API_KEY`

## インストール

### 1. プロジェクトのクローン
```bash
# プロジェクトディレクトリの作成
mkdir cc0_images_mcp
cd cc0_images_mcp

# 必要ファイルのコピー
cp mcp_cc0_images_server.py server.py
cp mcp_cc0_requirements.txt requirements.txt
```

### 2. Python仮想環境の作成
```bash
# 仮想環境作成
python -m venv venv

# 仮想環境アクティベート（macOS/Linux）
source venv/bin/activate

# 仮想環境アクティベート（Windows）
venv\Scripts\activate
```

### 3. 依存関係のインストール
```bash
# 基本パッケージのインストール
pip install -r requirements.txt

# 開発環境の場合（テスト・リンター含む）
pip install pytest pytest-asyncio black flake8
```

## 環境設定

### 1. 環境変数ファイル作成
`.env`ファイルを作成し、APIキーを設定：
```bash
# .env ファイル
PIXABAY_API_KEY=your_pixabay_api_key_here
UNSPLASH_API_KEY=your_unsplash_api_key_here
PEXELS_API_KEY=your_pexels_api_key_here

# オプション設定
CACHE_ENABLED=true
CACHE_TTL=3600
MAX_SEARCH_RESULTS=20
DEFAULT_IMAGE_QUALITY=80
```

### 2. 設定ファイル（config.py）
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API設定
    PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
    UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY") 
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
    
    # サーバー設定
    HOST = os.getenv("MCP_HOST", "localhost")
    PORT = int(os.getenv("MCP_PORT", 8000))
    
    # キャッシュ設定
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))
    
    # 検索設定
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", 20))
    DEFAULT_IMAGE_QUALITY = int(os.getenv("DEFAULT_IMAGE_QUALITY", 80))
    
    # レート制限設定
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 60  # seconds
```

## サーバー起動

### 1. 開発環境での起動
```bash
# 基本起動
python server.py

# デバッグモード
python server.py --debug

# ポート指定
python server.py --port 8001
```

### 2. プロダクション環境での起動
```bash
# uvicornを使用した起動
uvicorn server:mcp --host 0.0.0.0 --port 8000

# ワーカー数指定
uvicorn server:mcp --host 0.0.0.0 --port 8000 --workers 4

# リロード機能付き（開発時）
uvicorn server:mcp --reload
```

## テスト

### 1. ユニットテスト実行
```bash
# 全テスト実行
pytest

# 詳細出力
pytest -v

# カバレッジ付き
pytest --cov=server
```

### 2. 機能テスト
```bash
# 使用例の実行
python mcp_cc0_usage_examples.py

# 接続テスト
curl http://localhost:8000/health
```

### 3. APIキーテスト
```bash
# 環境変数確認
python -c "from config import Config; print('Pixabay:', bool(Config.PIXABAY_API_KEY))"

# API疎通確認
python -c "
import asyncio
from server import pixabay
async def test():
    results = await pixabay.search_images('test', count=1)
    print(f'Test successful: {len(results)} results')
asyncio.run(test())
"
```

## MCPクライアント連携

### 1. MCP接続設定例
```json
{
  "mcp_servers": {
    "cc0_images": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/cc0_images_mcp"
    }
  }
}
```

### 2. クライアントからの呼び出し例
```python
# MCPクライアント使用例
import mcp_client

async def use_cc0_images():
    client = mcp_client.connect("cc0_images")
    
    # 画像検索
    results = await client.call_tool(
        "search_cc0_images",
        query="modern office",
        category="business",
        count=5
    )
    
    # デザイン提案
    suggestions = await client.call_tool(
        "suggest_design_images", 
        design_type="website_hero",
        mood="professional"
    )
    
    return results, suggestions
```

## デプロイ

### 1. Dockerデプロイ
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "server:mcp", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# ビルド・実行
docker build -t cc0-images-mcp .
docker run -p 8000:8000 --env-file .env cc0-images-mcp
```

### 2. クラウドデプロイ
```yaml
# docker-compose.yml
version: '3.8'
services:
  cc0-images-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PIXABAY_API_KEY=${PIXABAY_API_KEY}
      - UNSPLASH_API_KEY=${UNSPLASH_API_KEY}
      - PEXELS_API_KEY=${PEXELS_API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 監視・ログ

### 1. ログ設定
```python
# logging_config.py
import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'cc0_images_mcp.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### 2. ヘルスチェック
```python
# health_check.py
@mcp.tool()
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "providers": {
            "pixabay": bool(PIXABAY_API_KEY),
            "unsplash": bool(UNSPLASH_API_KEY),
            "pexels": bool(PEXELS_API_KEY)
        }
    }
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. APIキーエラー
```
症状: "Authentication failed" エラー
解決: .envファイルのAPIキーを確認、有効期限をチェック
```

#### 2. レート制限エラー
```
症状: "Rate limit exceeded" エラー
解決: リクエスト頻度を調整、キャッシュ機能を有効化
```

#### 3. ネットワークエラー
```
症状: "Connection timeout" エラー
解決: ネットワーク接続確認、プロキシ設定の確認
```

#### 4. メモリ不足
```
症状: サーバーが応答しない
解決: メモリ使用量監視、キャッシュサイズ調整
```

## パフォーマンス最適化

### 1. キャッシュ設定
```python
# キャッシュ有効化
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1時間

# Redis使用（オプション）
REDIS_URL = "redis://localhost:6379"
```

### 2. 並行処理設定
```python
# 同時リクエスト数制限
MAX_CONCURRENT_REQUESTS = 10

# プロバイダー別タイムアウト
PROVIDER_TIMEOUTS = {
    "pixabay": 5.0,
    "unsplash": 3.0,
    "pexels": 4.0
}
```

## セキュリティ

### 1. APIキー管理
- 環境変数での管理
- 定期的なローテーション
- アクセス権限の最小化

### 2. レート制限
- IP別制限
- ユーザー別制限
- プロバイダー別制限

### 3. 入力検証
- SQLインジェクション対策
- XSS対策
- パラメータ検証

## 運用監視

### 1. メトリクス収集
- リクエスト数
- レスポンス時間
- エラー率
- プロバイダー別統計

### 2. アラート設定
- サーバーダウン
- レスポンス時間劣化
- エラー率上昇
- API制限到達

---

このセットアップガイドに従って、CC0画像検索MCPサーバーを確実に構築・運用できます。追加の質問や設定についてはドキュメントを参照してください。 