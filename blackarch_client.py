#!/usr/bin/env python3
"""
BlackArch MCP Client
Simple client for interacting with the BlackArch MCP server.
"""

import json
import subprocess
import sys
from typing import Optional, Dict, List, Any

class BlackArchClient:
    """Client for BlackArch MCP Server"""
    
    def __init__(self, server_path: str = "blackarch_mcp_v2.py"):
        self.server_path = server_path
    
    def _send_request(self, request: dict) -> dict:
        """Send JSON-RPC request to MCP server"""
        try:
            result = subprocess.run(
                ['python3', self.server_path],
                input=json.dumps(request),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse last JSON line (skip banner)
            lines = result.stdout.strip().split('\n')
            for line in reversed(lines):
                if line.strip().startswith('{'):
                    return json.loads(line)
            
            return {"error": "No JSON response"}
        except subprocess.TimeoutExpired:
            return {"error": "Request timeout"}
        except Exception as e:
            return {"error": str(e)}
    
    def list_tools(self) -> List[Dict]:
        """List available MCP tools"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        })
        return response.get("result", {}).get("tools", [])
    
    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "get_categories", "arguments": {}}
        })
        return response.get("result", {}).get("categories", [])
    
    def get_tools(self, category: str, limit: int = 50) -> List[Dict]:
        """Get tools in category"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "get_tools", "arguments": {"category": category, "limit": limit}}
        })
        return response.get("result", {}).get("tools", [])
    
    def search(self, query: str, limit: int = 50) -> List[Dict]:
        """Search tools"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "search", "arguments": {"query": query, "limit": limit}}
        })
        return response.get("result", {}).get("results", [])
    
    def get_tool(self, name: str) -> Optional[Dict]:
        """Get specific tool info"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {"name": "get_tool", "arguments": {"name": name}}
        })
        return response.get("result", {}).get("tool")
    
    def get_random(self, category: Optional[str] = None, count: int = 5) -> List[Dict]:
        """Get random tools"""
        args = {"count": count}
        if category:
            args["category"] = category
        
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {"name": "random", "arguments": args}
        })
        return response.get("result", {}).get("tools", [])
    
    def get_stats(self) -> Dict:
        """Get statistics"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {"name": "stats", "arguments": {}}
        })
        return response.get("result", {})
    
    def get_cheat_sheet(self, category: str) -> Dict:
        """Get cheat sheet"""
        response = self._send_request({
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {"name": "cheat_sheet", "arguments": {"category": category}}
        })
        return response.get("result", {})

def print_banner():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║          BLACKARCH MCP CLIENT v1.0                    ║
    ║          2863+ Security Tools • 48 Categories         ║
    ╚═══════════════════════════════════════════════════════╝
    """)

def main():
    print_banner()
    
    client = BlackArchClient()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "categories":
            cats = client.get_categories()
            print(f"\n📁 Available Categories ({len(cats)}):\n")
            for cat in cats[:20]:
                print(f"  {cat['name'].upper():20} {cat['count']:4} tools")
            if len(cats) > 20:
                print(f"\n  ... and {len(cats)-20} more categories")
        
        elif cmd == "search" and len(sys.argv) > 2:
            results = client.search(sys.argv[2])
            print(f"\n🔍 Search results for '{sys.argv[2]}':\n")
            for r in results[:10]:
                print(f"  [{r.get('category', 'unknown'):12}] {r['name']}")
                print(f"    {r['description'][:60]}...")
        
        elif cmd == "tool" and len(sys.argv) > 2:
            tool = client.get_tool(sys.argv[2])
            if tool:
                print(f"\n🔧 {tool['name']}")
                print(f"   Version: {tool.get('version', 'N/A')}")
                print(f"   Category: {tool.get('category', 'N/A')}")
                print(f"   {tool.get('description', 'No description')}")
                if 'install_command' in tool:
                    print(f"\n   Install: {tool['install_command']}")
            else:
                print(f"\n❌ Tool not found: {sys.argv[2]}")
        
        elif cmd == "stats":
            stats = client.get_stats()
            print(f"\n📊 Database Statistics:\n")
            print(f"   Total Tools: {stats.get('total_tools', 'N/A')}")
            print(f"   Categories: {stats.get('total_categories', 'N/A')}")
        
        elif cmd == "random":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            tools = client.get_random(count=count)
            print(f"\n🎲 Random Tools:\n")
            for t in tools:
                print(f"  [{t.get('category', 'unknown'):12}] {t['name']}")
        
        else:
            print_help()
    else:
        print_help()

def print_help():
    print("""
    Usage: python3 blackarch_client.py <command> [args]
    
    Commands:
      categories              List all categories
      search <query>          Search tools
      tool <name>             Get tool details
      stats                   Database statistics
      random [count]          Random tools (default: 5)
      
    Examples:
      python3 blackarch_client.py categories
      python3 blackarch_client.py search sqlmap
      python3 blackarch_client.py tool nmap
      python3 blackarch_client.py stats
      python3 blackarch_client.py random 10
    """)

if __name__ == "__main__":
    main()