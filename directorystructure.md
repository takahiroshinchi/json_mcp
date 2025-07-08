# ディレクトリ構成

以下のディレクトリ構造に従って実装を行ってください：

```
gjson/
├── main.py                       # メインエントリーポイント
├── server.py                     # MCPサーバー実装（コア機能）
├── pyproject.toml                # プロジェクト設定・依存関係定義
├── uv.lock                       # 依存関係ロックファイル
├── project_data/                 # Grapes.jsプロジェクトデータ
│   ├── design_2.json             # Grapes.jsデザインデータ（バージョン2）
│   └── design_3.json             # Grapes.jsデザインデータ（バージョン3）
├── html/                         # HTMLファイル格納
│   ├── code.html                 # メインHTMLファイル
│   ├── code_1.html               # HTMLファイル（バリエーション1）
│   └── code_GQuuuuuuX.html       # HTMLファイル（バリエーション2）
├── README.md                     # プロジェクト説明
├── technologystack.md            # 技術スタック定義
├── directorystructure.md         # 本ファイル（ディレクトリ構成）
├── PYTHON_ENVIRONMENT_GUIDE.md   # Python環境設定ガイド
├── UV_DEVELOPMENT_GUIDE.md       # UV開発ガイド
├── CAROUSEL_ANALYSIS_REPORT.md   # カルーセル分析レポート
├── SWIPER_ANALYSIS_RESULTS.md    # Swiper分析結果
├── .git/                         # Gitリポジトリ
├── .cursor/                      # Cursor設定
├── .gitignore                    # Git除外設定
└── uv.lock                       # UV依存関係ロック
```

## ディレクトリ詳細説明

### `/` (ルートディレクトリ)
- **main.py**: プロジェクトのメインエントリーポイント
- **server.py**: MCPサーバーのコア実装。FastMCPを使用してMCPツールを提供
- **pyproject.toml**: プロジェクト設定、依存関係、メタデータを定義
- **uv.lock**: UV依存関係マネージャーのロックファイル

### `/project_data/`
Grapes.jsプロジェクトデータの格納場所
- **design_*.json**: Grapes.jsのプロジェクトデータ（JSON形式）
- 各ファイルには以下の構造が含まれる：
  - `styles`: CSSスタイル定義
  - `pages`: ページ構造とコンポーネント
  - `components`: UI コンポーネント定義

### `/html/`
HTMLファイルの格納場所
- **code.html**: メインのHTMLファイル
- **code_*.html**: 各種HTMLファイルのバリエーション
- 各ファイルには以下の技術が使用される：
  - Tailwind CSS (CDN)
  - JavaScript (ES6+)
  - Swiper.js
  - Font Awesome
  - Google Fonts

### ドキュメントファイル
- **README.md**: プロジェクト概要と使用方法
- **technologystack.md**: 使用技術スタックの詳細
- **directorystructure.md**: 本ファイル
- **PYTHON_ENVIRONMENT_GUIDE.md**: Python環境設定ガイド
- **UV_DEVELOPMENT_GUIDE.md**: UV使用ガイド
- **CAROUSEL_ANALYSIS_REPORT.md**: カルーセル機能分析
- **SWIPER_ANALYSIS_RESULTS.md**: Swiper.js分析結果

## 配置ルール

### MCPサーバー関連
- **MCPサーバー実装**: `server.py`に一元化
- **MCP Tools**: `server.py`内で定義・実装
- **データ処理ロジック**: `server.py`内で実装

### データファイル
- **Grapes.jsデータ**: `project_data/`フォルダに配置
- **HTMLファイル**: `html/`フォルダに配置
- **設定ファイル**: ルートディレクトリに配置

### 開発・設定ファイル
- **依存関係設定**: `pyproject.toml`で管理
- **環境設定**: UVを使用してpyproject.tomlベースで管理
- **バージョン管理**: `.git/`フォルダ（標準Git構成）

## 実装時の注意点

### ファイル配置
1. **新しいMCPツール**: `server.py`内で追加実装
2. **新しいGrapes.jsデータ**: `project_data/`フォルダに配置
3. **新しいHTMLファイル**: `html/`フォルダに配置
4. **新しい依存関係**: `pyproject.toml`に追加

### 開発規則
- **Pythonバージョン**: 3.13以上必須
- **依存関係管理**: UV使用を推奨
- **コード品質**: 非同期処理（asyncio）を適切に使用
- **データ形式**: JSONを基本とする

### 禁止事項
- **server.py以外でのMCPツール実装**: 機能が分散するため禁止
- **pyproject.toml以外での依存関係管理**: 環境の一貫性維持のため
- **project_data/以外でのデータファイル配置**: データ管理の一元化のため
