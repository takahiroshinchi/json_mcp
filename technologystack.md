# 技術スタック

## プロジェクト概要
- **プロジェクト名**: gjson
- **バージョン**: 0.1.0
- **説明**: Grapes.jsプロジェクトデータを扱うMCPサーバー

## コア技術
- **Python**: >=3.13
- **MCP CLI**: >=1.10.1 (Model Context Protocol)
- **FastMCP**: MCPサーバーフレームワーク
- **UV**: Pythonパッケージマネージャー

## フロントエンド
- **HTML5**: セマンティックマークアップ
- **CSS3**: スタイリング
- **Tailwind CSS**: ユーティリティファーストCSSフレームワーク（CDN）
- **JavaScript (ES6+)**: フロントエンドロジック
- **Swiper.js**: スライダー/カルーセルライブラリ
- **Grapes.js**: Web Page Builderコンポーネント
- **Font Awesome**: アイコンライブラリ
- **Google Fonts**: タイポグラフィ

## バックエンド/サーバー
- **Python 3.13**: メインランタイム
- **FastMCP**: MCPサーバー実装
- **asyncio**: 非同期処理
- **JSON**: データストレージ形式

## データ構造
- **design_*.json**: Grapes.jsプロジェクトデータ
- **HTMLファイル**: 静的ページ
- **CSS**: スタイル定義
- **JavaScript**: インタラクティブ機能

## 開発ツール
- **UV**: 依存関係管理・パッケージマネージャー
- **Git**: バージョン管理
- **pyproject.toml**: プロジェクト設定

## サーバー機能
- **MCP Tools**: 以下のツールを提供
  - `get_component_by_id`: ID指定でコンポーネント取得
  - `get_components_by_type`: タイプ別コンポーネント取得
  - `get_components_by_class`: CSS class別コンポーネント取得
  - `get_project_structure`: プロジェクト構造取得
  - `get_styles_for_selector`: CSSセレクター別スタイル取得

## プロジェクト構成
```
gjson/
├── main.py              # メインエントリーポイント
├── server.py            # MCPサーバー実装
├── pyproject.toml       # プロジェクト設定
├── uv.lock             # 依存関係ロック
├── project_data/        # Grapes.jsデータ
│   ├── design_2.json
│   └── design_3.json
├── html/               # HTMLファイル
│   ├── code.html
│   ├── code_1.html
│   └── code_GQuuuuuuX.html
└── README.md
```

## 重要な制約事項
- **Pythonバージョン**: 3.13以上必須
- **MCPバージョン**: 1.10.1以上必須
- **データファイル**: JSON形式のGrapes.jsデータを使用
- **開発環境**: UV使用を推奨

## 実装規則
- MCPサーバーはserver.pyで一元管理
- データはproject_data/フォルダで管理
- HTMLファイルはhtml/フォルダで管理
- 依存関係はpyproject.tomlで定義
