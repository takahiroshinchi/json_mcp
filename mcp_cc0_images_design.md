# CC0画像検索MCPサーバー設計書

## 概要
自然言語でデザインカンプを作成するLLMサービス向けに、CC0（パブリックドメイン）画像の検索・取得機能を提供するModel Context Protocol (MCP)サーバーを設計・実装します。

## 目的
- デザインカンプ作成時のプレースホルダー画像として利用
- 商用利用可能な高品質画像の提供
- 複数プロバイダーからの統一されたアクセス
- ライセンス情報の透明性確保

## 対象プロバイダー分析

### 1. Unsplash (最優先)
- **API**: Unsplash API v1
- **ライセンス**: Unsplash License (CC0相当)
- **利点**: 高品質、豊富なカテゴリ、優秀な検索機能
- **制限**: 月50リクエスト (無料)、商用利用は要クレジット表記
- **URL形式**: `https://images.unsplash.com/photo-[id]?w=[width]&h=[height]&fit=crop`

### 2. Pixabay (高優先)
- **API**: Pixabay API
- **ライセンス**: Pixabay Content License (CC0相当)
- **利点**: 完全無料、多様な画像タイプ（写真、イラスト、ベクター）
- **制限**: 1日5,000リクエスト (無料)
- **URL形式**: 直接画像URL提供

### 3. Pexels (中優先)
- **API**: Pexels API v1
- **ライセンス**: Pexels License (CC0相当)
- **利点**: 高品質、キュレーション済み
- **制限**: 月200リクエスト (無料)

### 4. Burst by Shopify (低優先)
- **API**: 公式API無し (スクレイピング必要)
- **ライセンス**: CC0
- **利点**: Eコマース特化画像
- **制限**: API未提供

## MCP機能仕様

### 提供ツール

#### 1. `search_cc0_images`
```json
{
  "name": "search_cc0_images",
  "description": "CC0ライセンス画像を検索",
  "parameters": {
    "query": {
      "type": "string",
      "description": "検索キーワード（英語推奨）"
    },
    "category": {
      "type": "string",
      "enum": ["nature", "technology", "business", "people", "architecture", "food", "travel", "abstract"],
      "description": "画像カテゴリ"
    },
    "orientation": {
      "type": "string",
      "enum": ["all", "horizontal", "vertical", "square"],
      "default": "all"
    },
    "size": {
      "type": "string", 
      "enum": ["small", "medium", "large"],
      "default": "medium"
    },
    "count": {
      "type": "integer",
      "minimum": 1,
      "maximum": 20,
      "default": 10
    },
    "provider": {
      "type": "string",
      "enum": ["unsplash", "pixabay", "pexels", "auto"],
      "default": "auto"
    }
  }
}
```

#### 2. `get_image_info`
```json
{
  "name": "get_image_info",
  "description": "画像の詳細情報とライセンス情報を取得",
  "parameters": {
    "image_id": {
      "type": "string",
      "description": "画像ID"
    },
    "provider": {
      "type": "string",
      "enum": ["unsplash", "pixabay", "pexels"]
    }
  }
}
```

#### 3. `get_optimized_url`
```json
{
  "name": "get_optimized_url",
  "description": "指定サイズに最適化された画像URLを取得",
  "parameters": {
    "image_id": {
      "type": "string",
      "description": "画像ID"
    },
    "provider": {
      "type": "string"
    },
    "width": {
      "type": "integer",
      "minimum": 100,
      "maximum": 2000
    },
    "height": {
      "type": "integer", 
      "minimum": 100,
      "maximum": 2000
    },
    "quality": {
      "type": "integer",
      "minimum": 50,
      "maximum": 100,
      "default": 80
    }
  }
}
```

#### 4. `suggest_design_images`
```json
{
  "name": "suggest_design_images",
  "description": "デザインカンプ作成に適した画像を提案",
  "parameters": {
    "design_type": {
      "type": "string",
      "enum": ["website_hero", "app_background", "product_showcase", "testimonial_bg", "blog_header", "portfolio_piece"],
      "description": "デザインの用途"
    },
    "color_scheme": {
      "type": "string",
      "enum": ["warm", "cool", "neutral", "vibrant", "monochrome"],
      "description": "カラースキーム"
    },
    "mood": {
      "type": "string",
      "enum": ["professional", "casual", "modern", "vintage", "minimalist", "bold"],
      "description": "デザインのムード"
    },
    "content_focus": {
      "type": "string",
      "description": "メインコンテンツの説明"
    }
  }
}
```

## アーキテクチャ設計

### ディレクトリ構造
```
mcp_cc0_images/
├── server.py              # FastMCP メインサーバー
├── providers/             # プロバイダー別実装
│   ├── __init__.py
│   ├── base_provider.py   # 基底クラス
│   ├── unsplash.py        # Unsplash API実装
│   ├── pixabay.py         # Pixabay API実装
│   └── pexels.py          # Pexels API実装
├── models/                # データモデル
│   ├── __init__.py
│   ├── image.py           # 画像データクラス
│   └── search_result.py   # 検索結果データクラス
├── utils/                 # ユーティリティ
│   ├── __init__.py
│   ├── cache.py           # キャッシュ機能
│   ├── image_processor.py # 画像最適化
│   └── license_checker.py # ライセンス検証
├── config/
│   ├── __init__.py
│   └── settings.py        # 設定管理
├── requirements.txt
└── README.md
```

### データモデル

#### Image
```python
@dataclass
class CC0Image:
    id: str
    provider: str
    title: str
    description: str
    url: str
    preview_url: str
    thumbnail_url: str
    width: int
    height: int
    file_size: Optional[int]
    format: str  # jpg, png, webp
    tags: List[str]
    category: str
    author: Optional[str]
    author_url: Optional[str]
    license_info: LicenseInfo
    created_at: datetime
    color_palette: List[str]  # 主要色の抽出
    
@dataclass 
class LicenseInfo:
    license_type: str  # "CC0", "Unsplash", "Pixabay"
    license_url: str
    attribution_required: bool
    commercial_use: bool
    modification_allowed: bool
    redistribution_allowed: bool
```

## 実装計画

### Phase 1: 基盤実装 (Week 1)
- [ ] FastMCPサーバーセットアップ
- [ ] 基底プロバイダークラス設計
- [ ] データモデル定義
- [ ] 基本的な設定管理

### Phase 2: プロバイダー実装 (Week 2-3)
- [ ] Unsplash API統合
- [ ] Pixabay API統合  
- [ ] Pexels API統合
- [ ] エラーハンドリング

### Phase 3: 高度な機能 (Week 4)
- [ ] 画像最適化機能
- [ ] キャッシュシステム
- [ ] デザイン提案アルゴリズム
- [ ] パフォーマンス最適化

### Phase 4: 統合・テスト (Week 5)
- [ ] 統合テスト
- [ ] パフォーマンステスト
- [ ] ドキュメント整備
- [ ] デプロイ準備

## API使用料金と制限

### Unsplash
- **無料枠**: 50リクエスト/時間
- **有料プラン**: $99/月で5,000リクエスト/時間
- **推奨**: キャッシュ強化で制限内利用

### Pixabay  
- **無料枠**: 5,000リクエスト/日
- **制限なし**: 完全無料
- **推奨**: メインプロバイダーとして活用

### Pexels
- **無料枠**: 200リクエスト/時間
- **制限**: クレジット表記推奨
- **推奨**: 補助的な利用

## セキュリティ考慮

### APIキー管理
- 環境変数による管理
- プロバイダー別ローテーション
- レート制限監視

### 画像検証
- ライセンス情報の二重チェック
- 不適切コンテンツフィルタリング
- ウイルススキャン（必要に応じて）

## パフォーマンス最適化

### キャッシュ戦略
- Redis/Memcachedによる検索結果キャッシュ
- 画像メタデータの永続化
- CDN経由での画像配信検討

### 並行処理
- 複数プロバイダー同時検索
- 非同期画像処理
- バックグラウンドでの画像最適化

## 利用例

### デザインカンプ作成シナリオ
```
User: "Eコマースサイトのヒーローセクション用に、モダンでプロフェッショナルな商品画像を探してください"

LLM → MCP: suggest_design_images(
  design_type="website_hero",
  color_scheme="neutral", 
  mood="professional",
  content_focus="product showcase"
)

MCP Response: [
  {
    "id": "abc123",
    "provider": "unsplash",
    "title": "Modern Laptop on Desk",
    "url": "https://images.unsplash.com/photo-abc123?w=1200&h=600",
    "license_info": {...},
    "suggestion_reason": "プロフェッショナルな商品配置、ニュートラルな背景"
  },
  ...
]
```

## 今後の拡張可能性

### AI画像生成統合
- Stable Diffusion API
- DALL-E 3 API  
- Midjourney API

### カスタム画像生成
- ブランドカラー適用
- ロゴ・テキスト挿入
- レイアウト自動調整

### デザインシステム連携
- Figma Plugin開発
- Sketch Integration
- Adobe Creative Suite連携 