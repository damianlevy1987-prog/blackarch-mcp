#!/usr/bin/env python3
"""
BlackArch Tools MCP Server v2.0
Full-featured MCP server with 2863+ security tools across 48 categories.
"""

import json
import sys
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Tool:
    name: str
    version: str
    description: str

class BlackArchDatabase:
    """BlackArch tools database manager"""
    
    def __init__(self, db_path: str = "/run/media/phoenix0/Ventoy/New Folder/blackarch_full_db.json"):
        self.db_path = db_path
        self.categories: Dict[str, List[Tool]] = {}
        self.metadata: Dict = {}
        self._load_database()
    
    def _load_database(self):
        """Load the full tool database"""
        if Path(self.db_path).exists():
            with open(self.db_path, "r") as f:
                data = json.load(f)
                self.metadata = data.get("metadata", {})
                self.categories = {
                    cat: [Tool(**t) for t in tools]
                    for cat, tools in data.get("categories", {}).items()
                }
        else:
            # Fallback to parsing the raw file
            self._load_from_raw()
    
    def _load_from_raw(self):
        """Parse from raw blackarch file"""
        raw_path = Path("/run/media/phoenix0/Ventoy/New Folder/blackarch")
        if raw_path.exists():
            with open(raw_path, "r") as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) >= 4:
                        tool = Tool(
                            name=parts[0].strip(),
                            version=parts[1].strip(),
                            description=parts[2].strip()
                        )
                        cat = parts[3].replace("blackarch-", "").strip()
                        if cat not in self.categories:
                            self.categories[cat] = []
                        self.categories[cat].append(tool)
            
            self.metadata = {
                "source": "raw_blackarch_file",
                "total_tools": sum(len(v) for v in self.categories.values()),
                "total_categories": len(self.categories)
            }
    
    def get_all_categories(self) -> List[Dict]:
        """Return all categories with counts"""
        return [
            {"name": cat, "count": len(tools), "description": f"Tools for {cat.replace('_', ' ')}"}
            for cat, tools in sorted(self.categories.items(), key=lambda x: -len(x[1]))
        ]
    
    def get_tools_by_category(self, category: str, limit: int = 50) -> List[Dict]:
        """Get tools in a specific category"""
        cat_lower = category.lower().replace(" ", "_")
        if cat_lower in self.categories:
            return [asdict(t) for t in self.categories[cat_lower][:limit]]
        return []
    
    def search_tools(self, query: str, limit: int = 50) -> List[Dict]:
        """Search tools by name, description, or category"""
        results = []
        q = query.lower()
        
        for cat, tools in self.categories.items():
            for tool in tools:
                if (q in tool.name.lower() or q in tool.description.lower() or q in cat):
                    r = asdict(tool)
                    r["category"] = cat
                    results.append(r)
                    if len(results) >= limit:
                        return results
        
        return results
    
    def get_tool_info(self, name: str) -> Optional[Dict]:
        """Get specific tool info by exact or partial name"""
        name_lower = name.lower()
        
        for cat, tools in self.categories.items():
            for tool in tools:
                if name_lower in tool.name.lower() or tool.name.lower() == name_lower:
                    r = asdict(tool)
                    r["category"] = cat
                    r["install_command"] = f"sudo pacman -S blackarch-{cat} {tool.name}"
                    r["description"] = tool.description
                    return r
        
        return None
    
    def get_random_tools(self, category: Optional[str] = None, count: int = 5) -> List[Dict]:
        """Get random tools, optionally from specific category"""
        import random
        
        tools_pool = []
        if category:
            cat_lower = category.lower().replace(" ", "_")
            if cat_lower in self.categories:
                tools_pool = self.categories[cat_lower]
        else:
            for cat_tools in self.categories.values():
                tools_pool.extend(cat_tools)
        
        selected = random.sample(tools_pool, min(count, len(tools_pool)))
        
        results = []
        for tool in selected:
            for cat, tools in self.categories.items():
                if tool in tools:
                    r = asdict(tool)
                    r["category"] = cat
                    results.append(r)
                    break
        
        return results
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        return {
            "total_tools": sum(len(v) for v in self.categories.values()),
            "total_categories": len(self.categories),
            "categories": [
                {"name": cat, "count": len(tools)}
                for cat, tools in sorted(self.categories.items(), key=lambda x: -len(x[1]))
            ]
        }
    
    def get_tools_by_tag(self, tags: List[str]) -> List[Dict]:
        """Get tools matching any of the given tags"""
        results = []
        tag_set = {t.lower() for t in tags}
        
        for cat, tools in self.categories.items():
            for tool in tools:
                for tag in tag_set:
                    if tag in tool.name.lower() or tag in tool.description.lower() or tag in cat:
                        r = asdict(tool)
                        r["category"] = cat
                        results.append(r)
                        break
        
        return results[:50]

class BlackArchMCPServer:
    """MCP Server implementation"""
    
    def __init__(self):
        self.db = BlackArchDatabase()
        self.mcp_tools = self._define_mcp_tools()
    
    def _define_mcp_tools(self) -> List[Dict]:
        """Define available MCP tools"""
        return [
            {
                "name": "get_categories",
                "description": "Get all BlackArch tool categories with tool counts",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_tools",
                "description": "Get all tools in a specific category",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Category name (e.g., webapp, scanner, exploitation)"},
                        "limit": {"type": "integer", "description": "Max number of tools to return (default: 50)", "default": 50}
                    },
                    "required": ["category"]
                }
            },
            {
                "name": "search",
                "description": "Search tools by name, description, or category",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "limit": {"type": "integer", "description": "Max results (default: 50)", "default": 50}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_tool",
                "description": "Get detailed information about a specific tool",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Tool name (exact or partial)"}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "random",
                "description": "Get random tool(s), optionally from a specific category",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Optional category filter"},
                        "count": {"type": "integer", "description": "Number of tools (default: 5)", "default": 5}
                    }
                }
            },
            {
                "name": "stats",
                "description": "Get database statistics and category breakdown",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "by_tags",
                "description": "Find tools matching specific tags/keywords",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tags": {"type": "array", "items": {"type": "string"}, "description": "List of tags to search"}
                    },
                    "required": ["tags"]
                }
            },
            {
                "name": "cheat_sheet",
                "description": "Get a category-specific cheat sheet for common tools",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Category for cheat sheet"}
                    },
                    "required": ["category"]
                }
            }
        ]
    
    def handle_request(self, request: dict) -> dict:
        """Handle MCP request"""
        method = request.get("method", "")
        req_id = request.get("id")
        
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": self.mcp_tools}}
        
        if method == "tools/call":
            tool_name = request.get("params", {}).get("name", "")
            tool_args = request.get("params", {}).get("arguments", {})
            
            result = self._execute_tool(tool_name, tool_args)
            return {"jsonrpc": "2.0", "id": req_id, "result": result}
        
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Unknown method"}}
    
    def _execute_tool(self, name: str, args: dict) -> dict:
        """Execute a tool with given arguments"""
        try:
            if name == "get_categories":
                return {"categories": self.db.get_all_categories()}
            
            elif name == "get_tools":
                return {"tools": self.db.get_tools_by_category(
                    args.get("category", ""), 
                    args.get("limit", 50)
                )}
            
            elif name == "search":
                return {"results": self.db.search_tools(
                    args.get("query", ""),
                    args.get("limit", 50)
                )}
            
            elif name == "get_tool":
                return {"tool": self.db.get_tool_info(args.get("name", ""))}
            
            elif name == "random":
                return {"tools": self.db.get_random_tools(
                    args.get("category"),
                    args.get("count", 5)
                )}
            
            elif name == "stats":
                return self.db.get_stats()
            
            elif name == "by_tags":
                return {"tools": self.db.get_tools_by_tag(args.get("tags", []))}
            
            elif name == "cheat_sheet":
                return self._generate_cheatsheet(args.get("category", ""))
            
            else:
                return {"error": f"Unknown tool: {name}"}
        
        except Exception as e:
            return {"error": str(e)}

    def _generate_cheatsheet(self, category: str) -> dict:
        """Generate a cheat sheet for a category"""
        cat_lower = category.lower().replace(" ", "_")
        tools = self.db.get_tools_by_category(cat_lower, 20)
        
        cheat_sheet = {
            "category": category,
            "description": f"Common tools for {category}",
            "commands": []
        }
        
        # Add example commands based on category
        category_commands = {
            "scanner": [
                ("nmap -sV -sC target.com", "Basic scan"),
                ("nmap -p- -A target.com", "Full port scan"),
                ("masscan -p1-65535 target.com --rate=10000", "Fast mass scan"),
            ],
            "webapp": [
                ("sqlmap -u target.com --batch", "SQL injection scan"),
                ("dirb http://target.com", "Directory busting"),
                ("nikto -h target.com", "Web server scan"),
            ],
            "exploitation": [
                ("msfconsole", "Start Metasploit"),
                ("searchsploit keyword", "Search exploits"),
                ("msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=PORT -f elf > shell.elf", "Generate payload"),
            ],
            "cracker": [
                ("hashcat -m 0 -a 0 hash.txt wordlist.txt", "Basic hashcat"),
                ("john --wordlist=wordlist.txt hash.txt", "John the Ripper"),
                ("hydra -l admin -P passwords.txt ssh://target.com", "SSH brute force"),
            ],
            "wireless": [
                ("airmon-ng start wlan0", "Enable monitor mode"),
                ("airodump-ng wlan0mon", "Capture packets"),
                ("aireplay-ng -0 5 -a MAC target", "Deauth attack"),
            ],
            "recon": [
                ("theHarvester -d target.com -b google", "Email harvest"),
                ("amass enum -passive -d target.com", "Subdomain enum"),
                ("recon-ng", "Start ReconNG framework"),
            ],
            "forensic": [
                ("binwalk firmware.bin", "Analyze firmware"),
                ("autopsy", "Start Autopsy forensic tool"),
                ("volatility -f memory.dmp --profile=Win10x64 pslist", "Memory analysis"),
            ]
        }
        
        if cat_lower in category_commands:
            for cmd, desc in category_commands[cat_lower]:
                cheat_sheet["commands"].append({"command": cmd, "description": desc})
        
        return cheat_sheet

def main():
    """Main MCP server loop"""
    server = BlackArchMCPServer()
    
    # Print startup banner
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗       ║
    ║   ██╔════╝██╔═══██╗██╔══██╗████╗  ██║██║████╗  ██║██╔═══██╗      ║
    ║   ███████╗██║   ██║██████╔╝██╔██╗ ██║██║██╔██╗ ██║██║   ██║      ║
    ║   ╚════██║██║   ██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██║   ██║      ║
    ║   ███████║╚██████╔╝██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝      ║
    ║   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝       ║
    ║                                                                   ║
    ║            BLACKARCH TOOLS MCP SERVER v2.0                        ║
    ║            2863+ Security Tools • 48 Categories                  ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """, flush=True)
    
    print(f"Database loaded: {server.db.metadata.get('total_tools', 0)} tools")
    print("Waiting for MCP requests...\n", flush=True)
    
    # MCP protocol loop
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            response = server.handle_request(request)
            print(json.dumps(response), flush=True)
            
        except json.JSONDecodeError:
            pass
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": str(e)}
            }), flush=True)

if __name__ == "__main__":
    main()