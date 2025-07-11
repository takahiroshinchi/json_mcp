#!/usr/bin/env python3
"""
CC0画像検索MCPサーバー 使用例とテストケース
自然言語デザインカンプ作成での利用シナリオを示します
"""

import asyncio
import json
from typing import Dict, Any

# MCPクライアントの使用例（疑似コード）
class DesignCompService:
    """デザインカンプ作成サービスのサンプル実装"""
    
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
    
    async def create_website_hero_design(self, user_prompt: str) -> Dict[str, Any]:
        """Webサイトヒーローセクションのデザインカンプ作成"""
        
        # 1. ユーザープロンプトを解析
        design_context = self.parse_user_prompt(user_prompt)
        
        # 2. MCPサーバーから適切な画像を提案
        suggested_images = await self.mcp_client.call_tool(
            "suggest_design_images",
            design_type="website_hero",
            color_scheme=design_context.get("color_scheme", "neutral"),
            mood=design_context.get("mood", "professional"),
            content_focus=design_context.get("content", "")
        )
        
        # 3. 最適化された画像URLを取得
        optimized_images = []
        for image in suggested_images[:3]:  # 上位3つの画像
            optimized = await self.mcp_client.call_tool(
                "get_optimized_url",
                image_id=image["id"],
                provider=image["provider"],
                width=1200,
                height=600,
                quality=85
            )
            optimized_images.append(optimized)
        
        # 4. デザインカンプのHTMLを生成
        design_comp = self.generate_hero_html(optimized_images, design_context)
        
        return {
            "design_comp": design_comp,
            "suggested_images": suggested_images,
            "optimized_urls": optimized_images,
            "design_context": design_context
        }
    
    def parse_user_prompt(self, prompt: str) -> Dict[str, Any]:
        """ユーザープロンプトを解析してデザインコンテキストを抽出"""
        # 実際の実装では、NLPやLLMを使用してプロンプトを解析
        context = {
            "color_scheme": "neutral",
            "mood": "professional",
            "content": prompt
        }
        
        # キーワードベースの簡単な解析例
        if any(word in prompt.lower() for word in ["warm", "orange", "red"]):
            context["color_scheme"] = "warm"
        elif any(word in prompt.lower() for word in ["cool", "blue", "green"]):
            context["color_scheme"] = "cool"
        elif any(word in prompt.lower() for word in ["vibrant", "colorful", "bright"]):
            context["color_scheme"] = "vibrant"
        
        if any(word in prompt.lower() for word in ["casual", "friendly", "relaxed"]):
            context["mood"] = "casual"
        elif any(word in prompt.lower() for word in ["modern", "contemporary", "sleek"]):
            context["mood"] = "modern"
        elif any(word in prompt.lower() for word in ["minimal", "simple", "clean"]):
            context["mood"] = "minimalist"
        
        return context
    
    def generate_hero_html(self, images: list, context: Dict[str, Any]) -> str:
        """ヒーローセクションのHTMLを生成"""
        main_image = images[0] if images else {"optimized_url": ""}
        
        return f"""
        <!-- 自動生成されたヒーローセクション -->
        <section class="hero-section relative h-screen flex items-center justify-center overflow-hidden">
            <!-- 背景画像 -->
            <div class="absolute inset-0 z-0">
                <img 
                    src="{main_image.get('optimized_url', '')}" 
                    alt="Hero Background"
                    class="w-full h-full object-cover"
                />
                <div class="absolute inset-0 bg-black bg-opacity-40"></div>
            </div>
            
            <!-- コンテンツ -->
            <div class="relative z-10 text-center text-white max-w-4xl mx-auto px-6">
                <h1 class="text-5xl md:text-6xl font-bold mb-6 leading-tight">
                    {context.get('title', 'Your Amazing Product')}
                </h1>
                <p class="text-xl md:text-2xl mb-8 leading-relaxed opacity-90">
                    {context.get('content', 'Transform your business with our innovative solutions')}
                </p>
                <div class="space-x-4">
                    <button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-8 rounded-lg transition-colors">
                        Get Started
                    </button>
                    <button class="border-2 border-white text-white hover:bg-white hover:text-gray-900 font-semibold py-4 px-8 rounded-lg transition-colors">
                        Learn More
                    </button>
                </div>
            </div>
        </section>
        """

# 使用例1: 基本的な画像検索
async def example_basic_search():
    """基本的な画像検索の例"""
    print("=== 基本的な画像検索例 ===")
    
    # 疑似MCPクライアント呼び出し
    search_result = {
        "query": "modern office",
        "results": [
            {
                "id": "12345",
                "provider": "pixabay",
                "title": "modern office workspace",
                "url": "https://pixabay.com/photos/office-modern-workspace-12345/",
                "width": 1920,
                "height": 1080,
                "license_info": {
                    "license_type": "Pixabay Content License",
                    "commercial_use": True,
                    "attribution_required": False
                }
            }
        ]
    }
    
    print(f"検索クエリ: {search_result['query']}")
    print(f"検索結果: {len(search_result['results'])}件")
    for result in search_result['results']:
        print(f"- {result['title']} ({result['provider']})")
        print(f"  ライセンス: {result['license_info']['license_type']}")
        print(f"  商用利用: {'可能' if result['license_info']['commercial_use'] else '不可'}")

# 使用例2: デザイン提案
async def example_design_suggestion():
    """デザインに適した画像提案の例"""
    print("\n=== デザイン提案例 ===")
    
    # 疑似的なデザイン提案結果
    suggestion_result = {
        "design_type": "website_hero",
        "color_scheme": "professional",
        "mood": "modern",
        "suggestions": [
            {
                "id": "hero_001",
                "title": "Modern Business Team",
                "suggestion_reason": "プロフェッショナルなビジネス環境を表現",
                "design_context": {
                    "use_case": "Website Hero section",
                    "color_compatibility": "Neutral tones work well with brand colors",
                    "layout_fit": "Horizontal composition suitable for hero layout"
                }
            },
            {
                "id": "hero_002", 
                "title": "Sleek Technology Setup",
                "suggestion_reason": "現代的なテクノロジー感をアピール",
                "design_context": {
                    "use_case": "Website Hero section",
                    "color_compatibility": "Cool tones for tech-forward brand",
                    "layout_fit": "Clean composition with space for overlay text"
                }
            }
        ]
    }
    
    print(f"デザインタイプ: {suggestion_result['design_type']}")
    print(f"カラースキーム: {suggestion_result['color_scheme']}")
    print(f"ムード: {suggestion_result['mood']}")
    print(f"提案数: {len(suggestion_result['suggestions'])}件")
    
    for i, suggestion in enumerate(suggestion_result['suggestions'], 1):
        print(f"\n提案 {i}: {suggestion['title']}")
        print(f"理由: {suggestion['suggestion_reason']}")
        print(f"用途: {suggestion['design_context']['use_case']}")

# 使用例3: 完全なデザインカンプ作成フロー
async def example_complete_design_flow():
    """完全なデザインカンプ作成フローの例"""
    print("\n=== 完全なデザイン作成フロー例 ===")
    
    # ユーザーの自然言語プロンプト
    user_prompt = "現代的でプロフェッショナルなSaaSプロダクトのランディングページを作成してください。青を基調とした落ち着いたデザインで、信頼感を与える画像を使いたいです。"
    
    print(f"ユーザープロンプト: {user_prompt}")
    
    # 疑似的なデザインサービス実行
    service = DesignCompService(None)  # 実際の実装ではMCPクライアントを渡す
    
    # プロンプト解析結果
    context = service.parse_user_prompt(user_prompt)
    print(f"\n解析されたデザインコンテキスト:")
    print(f"- カラースキーム: {context['color_scheme']}")
    print(f"- ムード: {context['mood']}")
    print(f"- コンテンツフォーカス: {context['content']}")
    
    # 生成されるデザインカンプのサンプル
    sample_design = service.generate_hero_html(
        [{"optimized_url": "https://images.unsplash.com/photo-example?w=1200&h=600"}],
        {"title": "Next-Gen SaaS Platform", "content": user_prompt}
    )
    
    print(f"\n生成されたHTMLデザインカンプ:")
    print("```html")
    print(sample_design[:300] + "...")
    print("```")

# 使用例4: ライセンス情報の確認
async def example_license_check():
    """ライセンス情報確認の例"""
    print("\n=== ライセンス情報確認例 ===")
    
    # 疑似的な画像ライセンス情報
    license_examples = [
        {
            "provider": "Pixabay",
            "license_type": "Pixabay Content License",
            "summary": "完全無料、商用利用可能、帰属表示不要、改変可能",
            "details": {
                "commercial_use": True,
                "attribution_required": False,
                "modification_allowed": True,
                "redistribution_allowed": True
            }
        },
        {
            "provider": "Unsplash", 
            "license_type": "Unsplash License",
            "summary": "無料、商用利用可能、帰属表示推奨、改変可能",
            "details": {
                "commercial_use": True,
                "attribution_required": True,
                "modification_allowed": True,
                "redistribution_allowed": True
            }
        }
    ]
    
    for license_info in license_examples:
        print(f"\n{license_info['provider']} ライセンス:")
        print(f"- タイプ: {license_info['license_type']}")
        print(f"- 概要: {license_info['summary']}")
        print(f"- 商用利用: {'可能' if license_info['details']['commercial_use'] else '不可'}")
        print(f"- 帰属表示: {'必要' if license_info['details']['attribution_required'] else '不要'}")

# パフォーマンステスト例
async def example_performance_test():
    """パフォーマンステストの例"""
    print("\n=== パフォーマンステスト例 ===")
    
    # 複数の並行検索をシミュレート
    search_queries = [
        "business team", "modern office", "technology setup",
        "creative workspace", "professional portrait"
    ]
    
    print(f"並行検索テスト: {len(search_queries)}クエリ")
    
    # 実際の実装では asyncio.gather を使用
    start_time = asyncio.get_event_loop().time()
    
    # 疑似的な結果
    results = []
    for query in search_queries:
        results.append({
            "query": query,
            "count": 10,
            "time_ms": 250  # 疑似的なレスポンス時間
        })
    
    end_time = asyncio.get_event_loop().time()
    total_time = (end_time - start_time) * 1000
    
    print(f"総実行時間: {total_time:.2f}ms")
    print(f"平均クエリ時間: {total_time / len(search_queries):.2f}ms")
    
    for result in results:
        print(f"- '{result['query']}': {result['count']}件 ({result['time_ms']}ms)")

# エラーハンドリング例
async def example_error_handling():
    """エラーハンドリングの例"""
    print("\n=== エラーハンドリング例 ===")
    
    error_scenarios = [
        {
            "scenario": "APIキー無効",
            "error": "Authentication failed: Invalid API key",
            "handling": "フォールバックプロバイダーに切り替え"
        },
        {
            "scenario": "レート制限超過", 
            "error": "Rate limit exceeded: 5000 requests per day",
            "handling": "キャッシュされた結果を返すか、他のプロバイダーを使用"
        },
        {
            "scenario": "ネットワークエラー",
            "error": "Connection timeout",
            "handling": "リトライ機構で再試行、失敗時はローカル画像を提案"
        }
    ]
    
    for scenario in error_scenarios:
        print(f"\nシナリオ: {scenario['scenario']}")
        print(f"エラー: {scenario['error']}")
        print(f"対処: {scenario['handling']}")

# メイン実行関数
async def main():
    """すべての使用例を実行"""
    print("CC0画像検索MCPサーバー 使用例とテストケース")
    print("=" * 60)
    
    await example_basic_search()
    await example_design_suggestion()
    await example_complete_design_flow()
    await example_license_check()
    await example_performance_test()
    await example_error_handling()
    
    print("\n" + "=" * 60)
    print("すべての例が完了しました。")
    print("実際の実装では、MCPクライアントを通じてこれらの機能を利用できます。")

if __name__ == "__main__":
    asyncio.run(main()) 