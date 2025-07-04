#!/usr/bin/env python3
"""
Grapes.js Component MCPサーバーをテストするためのシンプルなクライアント
"""
import json
import subprocess
import sys

def test_mcp_server():
    """MCPサーバーをテストする"""
    
    # サーバープロセスを開始
    process = subprocess.Popen(
        ['uv', 'run', 'server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd='/Users/takahiro.shinchi/Desktop/test/mcp/gjson'
    )
    
    # 初期化メッセージ
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    # メッセージを送信
    try:
        process.stdin.write(json.dumps(init_message) + '\n')
        process.stdin.flush()
        
        # レスポンスを読み取り
        response = process.stdout.readline()
        print("Initialize response:", response.strip())
        
        # 初期化完了通知
        initialized_message = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        process.stdin.write(json.dumps(initialized_message) + '\n')
        process.stdin.flush()
        
        # ツールリストを取得
        tools_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        process.stdin.write(json.dumps(tools_message) + '\n')
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("Tools list response:", response.strip())
        
        # プロジェクト構造を取得
        structure_message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_project_structure",
                "arguments": {}
            }
        }
        
        process.stdin.write(json.dumps(structure_message) + '\n')
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("Project structure:", response.strip())
        
        # 特定のIDでコンポーネントを取得
        component_message = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "get_component_by_id",
                "arguments": {
                    "component_id": "in43"
                }
            }
        }
        
        process.stdin.write(json.dumps(component_message) + '\n')
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("Component by ID (in43):", response.strip())
        
        # セクション要素を取得
        sections_message = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "get_components_by_type",
                "arguments": {
                    "component_type": "section"
                }
            }
        }
        
        process.stdin.write(json.dumps(sections_message) + '\n')
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("Sections:", response.strip())
        
        # スタイルを取得
        style_message = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "get_styles_for_selector",
                "arguments": {
                    "selector": "#in43"
                }
            }
        }
        
        process.stdin.write(json.dumps(style_message) + '\n')
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("Styles for #in43:", response.strip())
        
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_mcp_server()
