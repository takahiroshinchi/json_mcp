# カルーセル（Swiper）コンポーネント詳細レポート

## 📋 概要
grapes-component-server MCPを利用してGrapesJSプロジェクトのカルーセル（Swiper）コンポーネントを分析しました。

## 🎠 カルーセル基本情報

### メインコンテナ
- **コンポーネントタイプ**: `swiper-slider-container`
- **ID**: `ijg0h`
- **CSSクラス**: `swiper`, `swiper-container`
- **データ属性**: `data-apg="valid"`

### 🔧 Swiper設定オプション
以下の設定が有効になっています：
- ✅ **autoHeight**: 自動高さ調整
- ✅ **centeredSlides**: スライドを中央配置
- ✅ **loop**: 無限ループ
- ✅ **scrollbar**: スクロールバー表示
- ✅ **autoplay**: 自動再生
- ✅ **autoplayStopOnLastSlide**: 最後のスライドで自動再生停止
- ✅ **autoplayReverseDirection**: 自動再生逆方向

## 🎞️ スライド情報

### スライド数: 2枚

#### スライド 1
- **タイプ**: `swiper-slider-slide`
- **CSSクラス**: `swiper-slide`
- **コンテンツ**: 画像
- **画像URL**: `https://picsum.photos/520/230/?random`
- **画像設定**: `ratioDefault: 1` (アスペクト比1:1)

#### スライド 2
- **タイプ**: `swiper-slider-slide`
- **CSSクラス**: `swiper-slide`
- **コンテンツ**: 画像
- **画像URL**: `https://picsum.photos/520/231/?random`
- **画像設定**: `ratioDefault: 1` (アスペクト比1:1)

## 🎮 ナビゲーション要素

### 利用可能なナビゲーション（全て実装済み）
1. **前へボタン** (`swiper-slider-prev`)
   - CSSクラス: `swiper-button-prev`
   
2. **次へボタン** (`swiper-slider-next`)
   - CSSクラス: `swiper-button-next`
   
3. **ページネーション** (`swiper-slider-pagination`)
   - CSSクラス: `swiper-pagination`
   
4. **スクロールバー** (`swiper-slider-scrollbar`)
   - CSSクラス: `swiper-scrollbar`

## 🏗️ 構造図
```
swiper-slider-container (ijg0h)
├── swiper-slider-wrapper
│   ├── swiper-slider-slide
│   │   └── image (Picsum 520x230)
│   └── swiper-slider-slide
│       └── image (Picsum 520x231)
├── swiper-slider-prev
├── swiper-slider-next
├── swiper-slider-pagination
└── swiper-slider-scrollbar
```

## 📊 プロジェクト統計
- **総コンポーネント数**: 88
- **コンポーネントタイプ数**: 22
- **Swiperコンテナ数**: 1
- **Swiperスライド数**: 2
- **ナビゲーション要素数**: 4

## 💡 特徴・機能
- フル機能のSwiperカルーセル実装
- レスポンシブ対応（自動高さ調整）
- 完全なナビゲーション制御
- 自動再生機能（双方向対応）
- 無限ループ対応
- Picsum Photosを使用したデモ画像

このカルーセルは、最新のSwiper.jsライブラリの機能を活用した、完全に機能するインタラクティブなコンポーネントとして実装されています。
