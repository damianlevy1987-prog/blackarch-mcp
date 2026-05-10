#!/usr/bin/env python3
"""
BlackArch MCP Server - Test Suite
Validates MCP server functionality.
"""

import json
import subprocess
import sys
from typing import Dict, List, Any

class BlackArchTestRunner:
    """Test runner for BlackArch MCP server"""
    
    def __init__(self):
        self.server_path = "/run/media/phoenix0/Ventoy/New Folder/blackarch_mcp_v2.py"
        self.db_path = "/run/media/phoenix0/Ventoy/New Folder/blackarch_full_db.json"
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_run = 0
    
    def send_request(self, request: dict) -> dict:
        """Send MCP request to server"""
        try:
            result = subprocess.run(
                ['python3', self.server_path],
                input=json.dumps(request) + '\n',
                capture_output=True,
                text=True,
                timeout=10
            )
            lines = result.stdout.strip().split('\n')
            for line in reversed(lines):
                if line.strip().startswith('{'):
                    return json.loads(line)
            return {"error": "No JSON response"}
        except subprocess.TimeoutExpired:
            return {"error": "Timeout"}
        except Exception as e:
            return {"error": str(e)}
    
    def test(self, name: str, condition: bool, message: str = ""):
        """Run a test"""
        self.tests_run += 1
        if condition:
            print(f"  ✅ {name}")
            self.tests_passed += 1
        else:
            print(f"  ❌ {name}")
            if message:
                print(f"     {message}")
            self.tests_failed += 1
    
    def run_tests(self):
        """Run all tests"""
        print("""
╔═══════════════════════════════════════════════════════════╗
║           BLACKARCH MCP SERVER - TEST SUITE                 ║
╚═══════════════════════════════════════════════════════════╝
""")
        
        # Test 1: Database exists
        print("\n[1] Database Tests")
        import os
        self.test("Database file exists", os.path.exists(self.db_path))
        if os.path.exists(self.db_path):
            with open(self.db_path) as f:
                data = json.load(f)
                self.test("Database is valid JSON", True)
                self.test("Database has categories", "categories" in data)
                self.test("Has at least 40 categories", len(data.get("categories", {})) >= 40)
                self.test("Has at least 2000 tools", sum(len(v) for v in data.get("categories", {}).values()) >= 2000)
        
        # Test 2: MCP Server
        print("\n[2] MCP Server Tests")
        response = self.send_request({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list"
        })
        self.test("tools/list returns result", "result" in response)
        
        # Test 3: get_categories
        print("\n[3] get_categories Tool")
        response = self.send_request({
            "jsonrpc": "2.0", "id": 2,
            "method": "tools/call",
            "params": {"name": "get_categories", "arguments": {}}
        })
        cats = response.get("result", {}).get("categories", [])
        self.test("Returns categories", len(cats) > 0)
        self.test("Has required fields", len(cats) > 0 and "name" in cats[0] and "count" in cats[0])
        
        # Test 4: get_tools
        print("\n[4] get_tools Tool")
        response = self.send_request({
            "jsonrpc": "2.0", "id": 3,
            "method": "tools/call",
            "params": {"name": "get_tools", "arguments": {"category": "scanner", "limit": 10}}
        })
        tools = response.get("result", {}).get("tools", [])
        self.test("Returns scanner tools", len(tools) > 0)
        if tools:
            self.test("Tool has name", "name" in tools[0])
            self.test("Tool has description", "description" in tools[0])
        
        # Test 5: search
        print("\n[5] search Tool")
        response = self.send_request({
            "jsonrpc": "2.0", "id": 4,
            "method": "tools/call",
            "params": {"name": "search", "arguments": {"query": "nmap", "limit": 5}}
        })
        results = response.get("result", {}).get("results", [])
        self.test("Search finds results", len(results) > 0)
        
        # Test 6: get_tool
        print("\n[6] get_tool Tool")
        response = self.send_request({
            "jsonrpc": "2.0", "id": 5,
            "method": "tools/call",
            "params": {"name": "get_tool", "arguments": {"name": "nmap"}}
        })
        tool = response.get("result", {}).get("tool")
        # nmap might not be in the DB, so check for any valid tool lookup
        self.test("get_tool returns tool info", tool is not None)
        
        # Test 7: random
        print("\n[7] random Tool")
        response = self.send_request({
            "jsonrpc": "2.0", "id": 6,
            "method": "tools/call",
            "params": {"name": "random", "arguments": {"count": 5}}
        })
        tools = response.get("result", {}).get("tools", [])
        self.test("Returns random tools", len(tools) == 5)
        
        # Test 8: stats
        print("\n[8] stats Tool")
        response = self.send_request({
            "jsonrpc": "2.0", "id": 7,
            "method": "tools/call",
            "params": {"name": "stats", "arguments": {}}
        })
        stats = response.get("result", {})
        self.test("Returns statistics", "total_tools" in stats or "total_categories" in stats)
        
        # Test 9: cheat_sheet
        print("\n[9] cheat_sheet Tool")
        response = self.send_request({
            "jsonrpc": "2.0", "id": 8,
            "method": "tools/call",
            "params": {"name": "cheat_sheet", "arguments": {"category": "scanner"}}
        })
        result = response.get("result", {})
        self.test("Returns cheat sheet", "category" in result or "commands" in result or "error" not in response)
        
        # Print summary
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║                    TEST RESULTS                           ║
╠═══════════════════════════════════════════════════════════╣
║  Tests Run:    {self.tests_run:3}                                      ║
║  Passed:       {self.tests_passed:3}  ✅                               ║
║  Failed:       {self.tests_failed:3}  {'❌' if self.tests_failed > 0 else ' '}                               ║
╚═══════════════════════════════════════════════════════════╝
""")
        
        if self.tests_failed > 0:
            sys.exit(1)
        else:
            print("🎉 All tests passed!")
            sys.exit(0)

if __name__ == "__main__":
    runner = BlackArchTestRunner()
    runner.run_tests()