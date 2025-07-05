# UV開発環境ガイド（本レポジトリ）

## 🎯 概要

このドキュメントは、Grapes.js Component MCP Serverプロジェクトでのuv環境構築、アクティベート、開発フローの実践的なガイドです。

## 📋 プロジェクト情報

- **プロジェクト名**: gjson
- **Python版本**: 3.13
- **パッケージマネージャー**: uv
- **主要依存関係**: mcp[cli]>=1.10.1

## 🚀 初期セットアップ

### 1. 環境要件確認

```bash
# Python版本の確認
python --version  # 3.13 が必要

# uvのインストール確認
uv --version

# インストールされていない場合
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. プロジェクトクローン

```bash
git clone <repository-url>
cd gjson
```

### 3. 環境構築

```bash
# 依存関係のインストール（初回またはuv.lock更新時）
uv sync

# 開発用依存関係も含めてインストール
uv sync --dev
```

## 🔧 日常的な開発フロー

### 仮想環境の管理

```bash
# 仮想環境の作成（初回のみ）
uv venv

# 仮想環境のアクティベート
uv shell

# 仮想環境内でのコマンド実行（アクティベート不要）
uv run python server.py
uv run python test_mcp.py
uv run python test_swiper.py
```

### パッケージ管理

```bash
# パッケージの追加
uv add package_name

# 開発用パッケージの追加
uv add --dev pytest black flake8

# パッケージの削除
uv remove package_name

# パッケージの更新
uv sync --upgrade
```

## 🏃 実行コマンド集

### MCPサーバーの起動

```bash
# メインサーバーの起動
uv run server.py

# 開発モードでの起動（デバッグ出力付き）
uv run --env PYTHONUNBUFFERED=1 server.py
```

### テストの実行

```bash
# MCP サーバーテスト
uv run test_mcp.py

# Swiper コンポーネント分析テスト
uv run test_swiper.py

# 全テストの実行（pytestがインストールされている場合）
uv run pytest
```

### VS Code統合の設定

```json
{
  "mcp": {
    "servers": {
      "grapes-component-server": {
        "type": "stdio",
        "command": "uv",
        "args": [
          "--directory",
          "/path/to/your/gjson",
          "run",
          "server.py"
        ],
        "alwaysAllow": [
          "get_component_by_id",
          "get_components_by_type",
          "get_components_by_class",
          "get_project_structure",
          "get_styles_for_selector"
        ],
        "env": {
          "PYTHONUNBUFFERED": "1"
        }
      }
    }
  }
}
```

## 📁 ファイル構成の理解

### 重要なファイル

| ファイル | 役割 | 編集可否 |
|---------|------|----------|
| `pyproject.toml` | プロジェクト設定・依存関係 | ✅ |
| `uv.lock` | ロックファイル | ❌ 自動生成 |
| `.python-version` | Python版本指定 | ✅ |
| `server.py` | MCPサーバー実装 | ✅ |
| `test_*.py` | テストファイル | ✅ |

### pyproject.toml の理解

```toml
[project]
name = "gjson"                    # プロジェクト名
version = "0.1.0"                 # バージョン
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"       # Python版本要求
dependencies = [
    "mcp[cli]>=1.10.1",          # 本番依存関係
]

[tool.uv]
# UV固有の設定（今後追加可能）
```

## 🔄 開発ワークフロー

### 新機能開発

```bash
# 1. 新しいブランチを作成
git checkout -b feature/new-feature

# 2. 必要な依存関係を追加
uv add new-dependency

# 3. コードの開発
# ... 開発作業 ...

# 4. テストの実行
uv run test_mcp.py
uv run test_swiper.py

# 5. コミットとプッシュ
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

### 依存関係の更新

```bash
# すべての依存関係を更新
uv sync --upgrade

# 特定のパッケージのみ更新
uv add package_name --upgrade

# ロックファイルの更新
uv lock --upgrade
```

## 🛠️ デバッグとトラブルシューティング

### 一般的な問題と解決策

#### 1. "Module not found" エラー

```bash
# 依存関係の再インストール
uv sync --reinstall

# 仮想環境の再作成
rm -rf .venv
uv venv
uv sync
```

#### 2. Python版本の不整合

```bash
# 現在のPython版本確認
uv python list

# 正しいPython版本をインストール
uv python install 3.13

# プロジェクトで使用する版本を設定
echo "3.13" > .python-version
```

#### 3. MCPサーバーの接続問題

```bash
# 詳細ログでの実行
uv run --env PYTHONUNBUFFERED=1 --env DEBUG=1 server.py

# ポート確認
netstat -lan | grep :8080
```

### デバッグ用コマンド

```bash
# 現在の環境情報表示
uv info

# 依存関係ツリーの表示
uv tree

# インストール済みパッケージの確認
uv pip list

# 仮想環境のパス確認
uv venv --show-path
```

## 📊 パフォーマンスモニタリング

### ベンチマーク

```bash
# インストール時間の測定
time uv sync

# サーバー起動時間の測定
time uv run server.py --test-mode
```

### リソース使用量の確認

```bash
# メモリ使用量の監視
uv run --env PYTHONUNBUFFERED=1 server.py &
ps aux | grep python
```

## 🔧 開発環境のカスタマイズ

### 開発用依存関係の追加

```bash
# リンター・フォーマッター
uv add --dev black flake8 isort

# テストツール
uv add --dev pytest pytest-cov

# 型チェック
uv add --dev mypy

# ドキュメント生成
uv add --dev sphinx
```

### pre-commit フックの設定

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
```

## 📚 参考コマンド早見表

| 操作 | コマンド |
|------|----------|
| 環境構築 | `uv sync` |
| 仮想環境入る | `uv shell` |
| サーバー起動 | `uv run server.py` |
| テスト実行 | `uv run test_mcp.py` |
| パッケージ追加 | `uv add package_name` |
| 依存関係更新 | `uv sync --upgrade` |
| 環境情報表示 | `uv info` |
| Pythonバージョン確認 | `uv python list` |

## 🔄 チーム開発での注意点

### 1. ロックファイルの管理

```bash
# uv.lockファイルは必ずコミットする
git add uv.lock
git commit -m "Update dependencies"
```

### 2. Python版本の統一

```bash
# .python-versionファイルで版本を固定
echo "3.13" > .python-version
```

### 3. 環境の再現性

```bash
# 新しい環境でのセットアップ
uv sync  # uv.lockから正確な版本を復元
```

---

**重要**: このガイドに従って開発することで、一貫性のある高速な開発環境を維持できます。問題が発生した場合は、まず`uv sync`を実行してください。