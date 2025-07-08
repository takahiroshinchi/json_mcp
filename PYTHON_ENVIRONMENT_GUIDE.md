# Python環境統一ガイド: pip禁止 & uv統一

## 🎯 概要

このドキュメントは、Python環境をpipからuvに統一し、一貫した高速で信頼性のある開発環境を構築するためのガイドです。

## 🚫 pip禁止の理由

### pipの問題点
- **依存関係解決の遅さ**: 複雑な依存関係の解決に時間がかかる
- **環境の非再現性**: 異なる環境で同じパッケージバージョンが保証されない
- **セキュリティリスク**: ロックファイルがない場合、意図しないバージョンがインストールされる
- **パフォーマンス**: インストール・アンインストールが遅い

### uvの利点
- **高速性**: Rustで書かれており、pipより10-100倍高速
- **再現性**: 自動的にロックファイル（uv.lock）を生成
- **統一性**: プロジェクト管理、依存関係管理、Python version管理を一元化
- **セキュリティ**: ハッシュベースの検証とロックファイルによる依存関係の固定

## 📋 移行チェックリスト

### 1. uv のインストール

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# pipx経由（既存のpipxがある場合）
pipx install uv
```

### 2. 既存プロジェクトの移行

```bash
# 既存の requirements.txt から pyproject.toml への変換
uv add --requirements requirements.txt

# 既存の仮想環境の削除
rm -rf venv/
rm -rf .venv/

# uv環境の初期化
uv init
uv sync
```

### 3. pip使用を禁止する設定

#### a. シェル設定での禁止

```bash
# ~/.bashrc または ~/.zshrc に追加
pip() {
    echo "❌ pip の使用は禁止されています。代わりに uv を使用してください。"
    echo "📚 ヘルプ: https://docs.astral.sh/uv/"
    return 1
}

export PIP_DISABLE_PIP_VERSION_CHECK=1
export PIP_NO_CACHE_DIR=1
```

#### b. pre-commit フックでの禁止

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: no-pip
        name: Prevent pip usage
        entry: sh -c 'if grep -r "pip install" . --exclude-dir=.git --exclude="*.md"; then echo "❌ pip install found! Use uv instead."; exit 1; fi'
        language: system
        pass_filenames: false
```

#### c. GitHub Actions での禁止

```yaml
# .github/workflows/check-no-pip.yml
name: Prevent pip usage
on: [push, pull_request]
jobs:
  check-no-pip:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for pip usage
        run: |
          if grep -r "pip install" . --exclude-dir=.git --exclude="*.md"; then
            echo "❌ pip install found! Use uv instead."
            exit 1
          fi
```

## 📖 uv基本コマンド対応表

| pip コマンド | uv コマンド | 説明 |
|-------------|-------------|-----|
| `pip install package` | `uv add package` | パッケージの追加 |
| `pip install -r requirements.txt` | `uv sync` | 全依存関係のインストール |
| `pip uninstall package` | `uv remove package` | パッケージの削除 |
| `pip freeze` | `uv pip freeze` | インストール済みパッケージ一覧 |
| `pip list` | `uv pip list` | パッケージ一覧の表示 |
| `python -m venv venv` | `uv venv` | 仮想環境の作成 |
| `source venv/bin/activate` | `uv shell` | 仮想環境のアクティベート |
| `pip install -e .` | `uv pip install -e .` | 開発モードでのインストール |

## 🛠️ プロジェクト構成のベストプラクティス

### 必須ファイル

1. **pyproject.toml** - プロジェクト設定とメタデータ
2. **uv.lock** - ロックファイル（自動生成、コミット推奨）
3. **.python-version** - Python版本指定
4. **.gitignore** - uvキャッシュ等の除外設定

### 推奨ディレクトリ構成

```
project/
├── pyproject.toml          # プロジェクト設定
├── uv.lock                 # ロックファイル
├── .python-version         # Python版本
├── .gitignore              # Git除外設定
├── src/                    # ソースコード
│   └── package_name/
├── tests/                  # テストコード
└── docs/                   # ドキュメント
```

## 🔧 トラブルシューティング

### よくある問題と解決策

#### 1. "uv: command not found"
```bash
# パス設定の確認
echo $PATH
# uvの再インストール
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # または ~/.zshrc
```

#### 2. "python version not found"
```bash
# 利用可能なPythonバージョンの確認
uv python list
# 特定バージョンのインストール
uv python install 3.13
```

#### 3. "lock file out of date"
```bash
# ロックファイルの更新
uv lock --upgrade
```

#### 4. "dependency resolution failed"
```bash
# 依存関係の詳細表示
uv add package --verbose
# 競合する依存関係の確認
uv tree
```

## 📚 参考資料

- [uv公式ドキュメント](https://docs.astral.sh/uv/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [pyproject.toml設定リファレンス](https://peps.python.org/pep-0621/)

## ✅ 移行完了チェックリスト

- [ ] uvがインストールされている
- [ ] pipコマンドが無効化されている
- [ ] pyproject.tomlが正しく設定されている
- [ ] uv.lockファイルが生成されている
- [ ] CIパイプラインがuvを使用している
- [ ] チーム全体がuvに移行している
- [ ] ドキュメントが更新されている

---

**重要**: このガイドに従って移行することで、より高速で信頼性のある開発環境を構築できます。チーム全体での統一が成功の鍵となります。