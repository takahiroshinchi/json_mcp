#!/usr/bin/env python3
"""
Swiper Components Analysis Script - Test MCP server specifically for Swiper components
"""
import json
import subprocess
import sys

def analyze_swiper_components():
    """Analyze Swiper components in the design files"""
    
    # サーバープロセスを開始
    process = subprocess.Popen(
        ['uv', 'run', 'server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd='/Users/takahiro.shinchi/Desktop/test/mcp/gjson'
    )
    
    try:
        # 初期化メッセージ
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "swiper-analyzer",
                    "version": "1.0.0"
                }
            }
        }
        
        # メッセージを送信
        process.stdin.write(json.dumps(init_message) + '\n')
        process.stdin.flush()
        
        # レスポンスを読み取り
        response = process.stdout.readline()
        
        # 初期化完了通知
        initialized_message = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        process.stdin.write(json.dumps(initialized_message) + '\n')
        process.stdin.flush()
        
        print("🔍 SWIPER COMPONENT ANALYSIS")
        print("=" * 50)
        
        # 1. プロジェクト構造を取得
        structure_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "get_project_structure",
                "arguments": {}
            }
        }
        
        process.stdin.write(json.dumps(structure_message) + '\n')
        process.stdin.flush()
        
        response = process.stdout.readline()
        structure_data = json.loads(response)
        
        if structure_data.get("result", {}).get("content"):
            project_info = json.loads(structure_data["result"]["content"][0]["text"])
            print("\n📊 PROJECT OVERVIEW:")
            print(f"   Total Components: {project_info.get('total_components', 0)}")
            print(f"   Component Types Found: {len(project_info.get('component_types', {}))}")
            
            # Show component types
            if project_info.get('component_types'):
                print("\n🧩 COMPONENT TYPES:")
                for comp_type, count in project_info['component_types'].items():
                    print(f"   {comp_type}: {count}")
        
        # 2. 具体的なSwiperコンテナコンポーネントを取得
        swiper_container_message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_components_by_type",
                "arguments": {
                    "component_type": "swiper-slider-container"
                }
            }
        }
        
        process.stdin.write(json.dumps(swiper_container_message) + '\n')
        process.stdin.flush()
        
        response = process.stdout.readline()
        swiper_data = json.loads(response)
        
        if swiper_data.get("result", {}).get("content"):
            swiper_info = json.loads(swiper_data["result"]["content"][0]["text"])
            print(f"\n🎠 SWIPER CONTAINERS FOUND: {swiper_info.get('count', 0)}")
            
            if swiper_info.get('components'):
                for i, container in enumerate(swiper_info['components'], 1):
                    print(f"\n   📦 Swiper Container #{i}:")
                    print(f"      ID: {container.get('attributes', {}).get('id', 'N/A')}")
                    print(f"      Classes: {', '.join(container.get('classes', []))}")
                    
                    # Swiper特有の設定を表示
                    settings = []
                    if container.get('autoHeight'): settings.append('Auto Height')
                    if container.get('centeredSlides'): settings.append('Centered Slides')
                    if container.get('loop'): settings.append('Loop')
                    if container.get('scrollbar'): settings.append('Scrollbar')
                    if container.get('autoplay'): settings.append('Autoplay')
                    
                    if settings:
                        print(f"      Settings: {', '.join(settings)}")
                    
                    # 子コンポーネントを分析
                    if container.get('components'):
                        print(f"      Child Components: {len(container['components'])}")
                        for comp in container['components']:
                            comp_type = comp.get('type', 'unknown')
                            classes = ', '.join(comp.get('classes', []))
                            print(f"        - {comp_type} ({classes})")
        
        # 3. スライドコンポーネントを取得
        slides_message = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "get_components_by_type",
                "arguments": {
                    "component_type": "swiper-slider-slide"
                }
            }
        }
        
        process.stdin.write(json.dumps(slides_message) + '\n')
        process.stdin.flush()
        
        response = process.stdout.readline()
        slides_data = json.loads(response)
        
        if slides_data.get("result", {}).get("content"):
            slides_info = json.loads(slides_data["result"]["content"][0]["text"])
            print(f"\n🎞️ SWIPER SLIDES FOUND: {slides_info.get('count', 0)}")
            
            if slides_info.get('components'):
                for i, slide in enumerate(slides_info['components'], 1):
                    print(f"\n   🖼️ Slide #{i}:")
                    print(f"      Classes: {', '.join(slide.get('classes', []))}")
                    
                    # スライド内のコンテンツを分析
                    if slide.get('components'):
                        for comp in slide['components']:
                            comp_type = comp.get('type', 'unknown')
                            if comp_type == 'image':
                                src = comp.get('attributes', {}).get('src', 'N/A')
                                print(f"      Content: Image ({src})")
                            else:
                                print(f"      Content: {comp_type}")
        
        # 4. ナビゲーション要素を取得
        nav_types = ['swiper-slider-prev', 'swiper-slider-next', 'swiper-slider-pagination', 'swiper-slider-scrollbar']
        
        print(f"\n🎮 SWIPER NAVIGATION ELEMENTS:")
        for nav_type in nav_types:
            nav_message = {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "get_components_by_type",
                    "arguments": {
                        "component_type": nav_type
                    }
                }
            }
            
            process.stdin.write(json.dumps(nav_message) + '\n')
            process.stdin.flush()
            
            response = process.stdout.readline()
            nav_data = json.loads(response)
            
            if nav_data.get("result", {}).get("content"):
                nav_info = json.loads(nav_data["result"]["content"][0]["text"])
                count = nav_info.get('count', 0)
                if count > 0:
                    print(f"   {nav_type}: {count} found")
        
        print("\n✅ Swiper analysis complete!")
        
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    analyze_swiper_components()
