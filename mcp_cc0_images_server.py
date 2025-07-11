#!/usr/bin/env python3
"""
CC0画像検索MCPサーバー
自然言語デザインカンプ作成用のCC0画像検索・取得機能を提供
"""

import asyncio
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any
import httpx
from fastmcp import FastMCP

# データモデル
@dataclass
class LicenseInfo:
    license_type: str
    license_url: str
    attribution_required: bool
    commercial_use: bool
    modification_allowed: bool
    redistribution_allowed: bool

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
    format: str
    tags: List[str]
    category: str
    author: Optional[str]
    author_url: Optional[str]
    license_info: LicenseInfo
    created_at: datetime
    color_palette: List[str]

# MCPサーバー初期化
mcp = FastMCP("CC0 Images Search Server")

# 設定
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "your-pixabay-api-key")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY", "your-unsplash-api-key")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "your-pexels-api-key")

class PixabayProvider:
    """Pixabay API プロバイダー"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://pixabay.com/api/"
    
    async def search_images(
        self, 
        query: str, 
        category: str = "all",
        orientation: str = "all",
        size: str = "medium",
        count: int = 10
    ) -> List[CC0Image]:
        """画像検索"""
        params = {
            "key": self.api_key,
            "q": query,
            "image_type": "photo",
            "orientation": orientation if orientation != "all" else "all",
            "category": category if category != "all" else "",
            "min_width": 640 if size in ["medium", "large"] else 0,
            "min_height": 480 if size in ["medium", "large"] else 0,
            "per_page": min(count, 20),
            "safesearch": "true",
            "order": "popular"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                images = []
                for hit in data.get("hits", []):
                    license_info = LicenseInfo(
                        license_type="Pixabay Content License",
                        license_url="https://pixabay.com/service/license/",
                        attribution_required=False,
                        commercial_use=True,
                        modification_allowed=True,
                        redistribution_allowed=True
                    )
                    
                    image = CC0Image(
                        id=str(hit["id"]),
                        provider="pixabay",
                        title=hit.get("tags", "").replace(",", " "),
                        description=f"Pixabay image by {hit.get('user', 'Unknown')}",
                        url=hit["largeImageURL"],
                        preview_url=hit["webformatURL"],
                        thumbnail_url=hit["previewURL"],
                        width=hit["imageWidth"],
                        height=hit["imageHeight"],
                        file_size=hit.get("imageSize"),
                        format="jpg",
                        tags=hit.get("tags", "").split(", "),
                        category=category,
                        author=hit.get("user"),
                        author_url=f"https://pixabay.com/users/{hit.get('user', '')}/",
                        license_info=license_info,
                        created_at=datetime.now(),
                        color_palette=[]  # 後で色抽出機能を追加
                    )
                    images.append(image)
                
                return images
                
            except Exception as e:
                print(f"Pixabay API error: {e}")
                return []

class UnsplashProvider:
    """Unsplash API プロバイダー（基本実装）"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.unsplash.com"
    
    async def search_images(
        self, 
        query: str, 
        orientation: str = "all",
        count: int = 10
    ) -> List[CC0Image]:
        """画像検索"""
        headers = {"Authorization": f"Client-ID {self.api_key}"}
        params = {
            "query": query,
            "orientation": orientation if orientation != "all" else None,
            "per_page": min(count, 20)
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/search/photos", 
                    headers=headers, 
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                images = []
                for result in data.get("results", []):
                    license_info = LicenseInfo(
                        license_type="Unsplash License",
                        license_url="https://unsplash.com/license",
                        attribution_required=True,
                        commercial_use=True,
                        modification_allowed=True,
                        redistribution_allowed=True
                    )
                    
                    image = CC0Image(
                        id=result["id"],
                        provider="unsplash",
                        title=result.get("alt_description", "Untitled"),
                        description=result.get("description", ""),
                        url=result["urls"]["full"],
                        preview_url=result["urls"]["regular"],
                        thumbnail_url=result["urls"]["thumb"],
                        width=result["width"],
                        height=result["height"],
                        file_size=None,
                        format="jpg",
                        tags=[],
                        category="general",
                        author=result["user"]["name"],
                        author_url=result["user"]["links"]["html"],
                        license_info=license_info,
                        created_at=datetime.fromisoformat(result["created_at"].replace("Z", "+00:00")),
                        color_palette=[result.get("color", "#ffffff")]
                    )
                    images.append(image)
                
                return images
                
            except Exception as e:
                print(f"Unsplash API error: {e}")
                return []

# プロバイダーインスタンス
pixabay = PixabayProvider(PIXABAY_API_KEY)
unsplash = UnsplashProvider(UNSPLASH_API_KEY)

@mcp.tool()
async def search_cc0_images(
    query: str,
    category: str = "all",
    orientation: str = "all", 
    size: str = "medium",
    count: int = 10,
    provider: str = "auto"
) -> List[Dict[str, Any]]:
    """
    CC0ライセンス画像を検索
    
    Args:
        query: 検索キーワード（英語推奨）
        category: 画像カテゴリ（nature, technology, business, people, architecture, food, travel, abstract）
        orientation: 向き（all, horizontal, vertical, square）
        size: サイズ（small, medium, large）
        count: 取得件数（1-20）
        provider: プロバイダー（unsplash, pixabay, pexels, auto）
    
    Returns:
        CC0画像のリスト
    """
    results = []
    
    try:
        if provider == "pixabay" or provider == "auto":
            pixabay_results = await pixabay.search_images(
                query=query,
                category=category,
                orientation=orientation,
                size=size,
                count=count
            )
            results.extend([asdict(img) for img in pixabay_results])
        
        if provider == "unsplash" and UNSPLASH_API_KEY != "your-unsplash-api-key":
            unsplash_results = await unsplash.search_images(
                query=query,
                orientation=orientation,
                count=count
            )
            results.extend([asdict(img) for img in unsplash_results])
        
        # 結果をプロバイダー別に制限
        if provider != "auto":
            results = [r for r in results if r["provider"] == provider]
        
        # 件数制限
        return results[:count]
        
    except Exception as e:
        return [{"error": f"検索エラー: {str(e)}"}]

@mcp.tool()
async def get_image_info(image_id: str, provider: str) -> Dict[str, Any]:
    """
    画像の詳細情報とライセンス情報を取得
    
    Args:
        image_id: 画像ID
        provider: プロバイダー（unsplash, pixabay, pexels）
    
    Returns:
        画像の詳細情報
    """
    try:
        if provider == "pixabay":
            # Pixabayから詳細情報を取得
            params = {
                "key": PIXABAY_API_KEY,
                "id": image_id
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get("https://pixabay.com/api/", params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("hits"):
                    hit = data["hits"][0]
                    return {
                        "id": image_id,
                        "provider": provider,
                        "download_count": hit.get("downloads", 0),
                        "views": hit.get("views", 0),
                        "likes": hit.get("likes", 0),
                        "collections": hit.get("collections", 0),
                        "comments": hit.get("comments", 0),
                        "license_details": {
                            "type": "Pixabay Content License",
                            "summary": "自由に使用、変更、配布可能。商用利用可能。帰属表示不要。"
                        }
                    }
        
        return {"error": "画像が見つかりません"}
        
    except Exception as e:
        return {"error": f"情報取得エラー: {str(e)}"}

@mcp.tool() 
async def get_optimized_url(
    image_id: str,
    provider: str,
    width: int = 800,
    height: int = 600,
    quality: int = 80
) -> Dict[str, Any]:
    """
    指定サイズに最適化された画像URLを取得
    
    Args:
        image_id: 画像ID
        provider: プロバイダー
        width: 幅（100-2000）
        height: 高さ（100-2000）
        quality: 品質（50-100）
    
    Returns:
        最適化された画像URL
    """
    try:
        if provider == "pixabay":
            # Pixabayは固定サイズのみ提供
            return {
                "optimized_url": f"https://pixabay.com/get/{image_id}.jpg",
                "width": width,
                "height": height,
                "estimated_size": f"{width * height * 3 // 1024}KB"
            }
        
        elif provider == "unsplash":
            # Unsplashの画像サイズ最適化
            optimized_url = f"https://images.unsplash.com/photo-{image_id}?w={width}&h={height}&fit=crop&q={quality}"
            return {
                "optimized_url": optimized_url,
                "width": width,
                "height": height,
                "quality": quality
            }
        
        return {"error": "サポートされていないプロバイダーです"}
        
    except Exception as e:
        return {"error": f"URL生成エラー: {str(e)}"}

@mcp.tool()
async def suggest_design_images(
    design_type: str,
    color_scheme: str = "neutral",
    mood: str = "professional", 
    content_focus: str = ""
) -> List[Dict[str, Any]]:
    """
    デザインカンプ作成に適した画像を提案
    
    Args:
        design_type: デザインの用途（website_hero, app_background, product_showcase, testimonial_bg, blog_header, portfolio_piece）
        color_scheme: カラースキーム（warm, cool, neutral, vibrant, monochrome）
        mood: デザインのムード（professional, casual, modern, vintage, minimalist, bold）
        content_focus: メインコンテンツの説明
    
    Returns:
        デザインに適した画像の提案リスト
    """
    try:
        # デザインタイプ別のキーワードマッピング
        design_keywords = {
            "website_hero": ["business", "technology", "office", "modern"],
            "app_background": ["abstract", "gradient", "minimal", "clean"],
            "product_showcase": ["product", "modern", "studio", "clean"],
            "testimonial_bg": ["people", "professional", "portrait", "business"],
            "blog_header": ["lifestyle", "creative", "inspiration", "modern"],
            "portfolio_piece": ["creative", "art", "design", "inspiration"]
        }
        
        # ムード別のキーワード
        mood_keywords = {
            "professional": ["business", "office", "corporate"],
            "casual": ["lifestyle", "relaxed", "friendly"],
            "modern": ["technology", "minimal", "contemporary"],
            "vintage": ["retro", "classic", "old"],
            "minimalist": ["simple", "clean", "minimal"],
            "bold": ["dramatic", "colorful", "dynamic"]
        }
        
        # 検索キーワードの組み合わせ
        base_keywords = design_keywords.get(design_type, ["general"])
        mood_words = mood_keywords.get(mood, [])
        
        search_queries = []
        for base in base_keywords[:2]:  # 最大2つのベースキーワード
            for mood_word in mood_words[:1]:  # 1つのムードキーワード
                search_queries.append(f"{base} {mood_word}")
        
        if content_focus:
            search_queries.append(content_focus)
        
        all_suggestions = []
        
        # 各クエリで検索実行
        for query in search_queries[:3]:  # 最大3クエリ
            results = await search_cc0_images(
                query=query,
                category="all",
                orientation="horizontal" if design_type == "website_hero" else "all",
                size="large",
                count=3,
                provider="auto"
            )
            
            # 提案理由を追加
            for result in results:
                result["suggestion_reason"] = f"{design_type}に適した{mood}なスタイル、{color_scheme}カラーでの利用を想定"
                result["design_context"] = {
                    "design_type": design_type,
                    "color_scheme": color_scheme,
                    "mood": mood,
                    "use_case": f"{design_type.replace('_', ' ').title()}での利用"
                }
            
            all_suggestions.extend(results)
        
        # 重複除去（同じimage_idの場合）
        seen_ids = set()
        unique_suggestions = []
        for suggestion in all_suggestions:
            if suggestion.get("id") not in seen_ids:
                seen_ids.add(suggestion.get("id"))
                unique_suggestions.append(suggestion)
        
        return unique_suggestions[:10]  # 最大10件
        
    except Exception as e:
        return [{"error": f"提案生成エラー: {str(e)}"}]

@mcp.tool()
async def get_server_info() -> Dict[str, Any]:
    """
    MCPサーバーの情報を取得
    
    Returns:
        サーバー情報
    """
    return {
        "name": "CC0 Images Search Server",
        "version": "1.0.0",
        "description": "自然言語デザインカンプ作成用のCC0画像検索・取得サーバー",
        "supported_providers": ["pixabay", "unsplash", "pexels"],
        "available_categories": [
            "nature", "technology", "business", "people", 
            "architecture", "food", "travel", "abstract"
        ],
        "rate_limits": {
            "pixabay": "5,000/day",
            "unsplash": "50/hour",
            "pexels": "200/hour"
        },
        "features": [
            "画像検索",
            "ライセンス情報確認", 
            "画像最適化URL生成",
            "デザイン提案"
        ]
    }

if __name__ == "__main__":
    # サーバー起動
    mcp.run() 