#!/usr/bin/env python3
"""
BlackArch Tools MCP Server
Provides access to all BlackArch penetration testing tools organized by category.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class Tool:
    name: str
    version: str
    description: str
    category: str

class BlackArchMCPServer:
    def __init__(self):
        self.tools: Dict[str, List[Tool]] = {}
        self._load_tools()
    
    def _load_tools(self):
        """Load and categorize tools from blackarch file"""
        blackarch_file = Path("/run/media/phoenix0/Ventoy/New Folder/blackarch")
        
        if not blackarch_file.exists():
            # Use embedded data if file not found
            self._load_embedded_data()
            return
            
        with open(blackarch_file, "r") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 4:
                    tool = Tool(
                        name=parts[0].strip(),
                        version=parts[1].strip(),
                        description=parts[2].strip(),
                        category=parts[3].replace("blackarch-", "").strip()
                    )
                    
                    if tool.category not in self.tools:
                        self.tools[tool.category] = []
                    self.tools[tool.category].append(tool)
    
    def _load_embedded_data(self):
        """Fallback embedded tool data"""
        self.tools = {
            "scanner": [
                Tool("nmap", "7.94", "Network discovery and security auditing", "scanner"),
                Tool("masscan", "1.3.2", "TCP port scanner", "scanner"),
                Tool("amass", "2559", "Subdomain enumeration", "scanner"),
                Tool("naabu", "2.1.5", "Fast port scanner", "scanner"),
                Tool("rustscan", "2.0.1", "Modern port scanner", "scanner"),
                Tool("dnmap", "0.6", "Distributed nmap framework", "scanner"),
                Tool("autorecon", "288", "Multi-threaded network reconnaissance", "scanner"),
                Tool("nuclei", "3.3.0", "Vulnerability scanner templates", "scanner"),
                Tool("knock", "0.8.0", "Subdomain scanner", "scanner"),
                Tool("dirbuster", "1.0", "Web directory brute forcer", "scanner"),
            ],
            "webapp": [
                Tool("burpsuite", "2025.9.4", "Web application testing platform", "webapp"),
                Tool("sqlmap", "1.8", "SQL injection automation", "webapp"),
                Tool("nikto", "2.5.0", "Web server scanner", "webapp"),
                Tool("dirb", "2.22", "Web content scanner", "webapp"),
                Tool("dirsearch", "2521", "HTTP directory brute forcer", "webapp"),
                Tool("ffuf", "2.1.0", "Fast web fuzzer", "webapp"),
                Tool("gobuster", "3.6", "Directory/file DNS brute forcer", "webapp"),
                Tool("xsstrike", "475", "Advanced XSS detection", "webapp"),
                Tool("dalfox", "2049", "XSS scanning tool", "webapp"),
                Tool("commix", "2322", "Command injection tool", "webapp"),
                Tool(" XSSTeR", "1.0", "XSS vulnerability scanner", "webapp"),
                Tool("nuclei", "3.3.0", "Vulnerability templates", "webapp"),
                Tool("wpscan", "3.8.25", "WordPress security scanner", "webapp"),
                Tool("joomscan", "83.2", "Joomla vulnerability scanner", "webapp"),
                Tool("drupwn", "59.8", "Drupal exploitation tool", "webapp"),
            ],
            "exploitation": [
                Tool("metasploit", "6.4.0", "Penetration testing framework", "exploitation"),
                Tool("exploitdb", "1.6", "Exploit database", "exploitation"),
                Tool("searchsploit", "6.2.4", "Exploit search tool", "exploitation"),
                Tool("msfvenom", "6.4.0", "Payload generator", "exploitation"),
                Tool("empire", "6.2.1", "PowerShell post-exploitation", "exploitation"),
                Tool("covenant", "0.8", "C# command framework", "exploitation"),
                Tool("koadic", "0.8", "Powershell RAT", "exploitation"),
                Tool("pwntools", "8.0.0", "Exploit development library", "exploitation"),
                Tool("ropper", "2.7.0", "ROP gadget finder", "exploitation"),
                Tool("angr", "9.1.11752", "Binary analysis platform", "exploitation"),
                Tool("one_gadget", "1.8.2", "One gadget finder for libc", "exploitation"),
            ],
            "cracker": [
                Tool("hashcat", "6.2.6", "Password cracker (GPU)", "cracker"),
                Tool("john", "1.9.0", "Password cracker", "cracker"),
                Tool("hydra", "9.5", "Network login cracker", "cracker"),
                Tool("crowbar", "4.2", "Brute forcing tool", "cracker"),
                Tool("medusa", "2.2", "Parallel network cracker", "cracker"),
                Tool("ncrack", "0.9", "Network authentication cracker", "cracker"),
                Tool("crunch", "3.6", "Wordlist generator", "cracker"),
                Tool("cewl", "199", "Custom wordlist generator", "cracker"),
                Tool("cupp", "77.5", "Common User Password Profiler", "cracker"),
                Tool("pipal", "2.0", "Wordlist analyzer", "cracker"),
                Tool("maskprocessor", "0.73", "Wordlist generator", "cracker"),
            ],
            "wireless": [
                Tool("aircrack-ng", "1.7", "WiFi security auditing", "wireless"),
                Tool("wifite", "2.7.0", "Wireless attack automation", "wireless"),
                Tool("wifiphisher", "799", "WiFi phishing tool", "wireless"),
                Tool("hostapd", "2.10", "Access point software", "wireless"),
                Tool("reaver", "1.6.6", "WPS attack tool", "wireless"),
                Tool("bully", "1.1.0", "WPS brute force tool", "wireless"),
                Tool("wpa-supplicant", "2.10", "WiFi client", "wireless"),
                Tool("cowpatty", "6.0", "Wireless password attack", "wireless"),
                Tool("pyrit", "0.5.0", "GPU password cracking", "wireless"),
                Tool("hashcat", "6.2.6", "WPA/WPA2 cracker", "cracker"),
            ],
            "reverse_engineering": [
                Tool("ghidra", "10.4", "Software reverse engineering", "binary"),
                Tool("radare2", "5.9.4", "Command line debugger", "binary"),
                Tool("binja", "5.1.8104", "Binary analysis platform", "binary"),
                Tool("ida", "8.4", "Disassembler and debugger", "binary"),
                Tool("objdump", "2.42", "Binary disassembler", "binary"),
                Tool("strace", "6.10", "System call tracer", "binary"),
                Tool("ltrace", "0.7.1", "Library call tracer", "binary"),
                Tool("upx", "4.2.4", "Executable packer", "binary"),
                Tool("yara", "4.4.0", "Pattern matching tool", "binary"),
                Tool("cutter", "2.3.0", "GUI for radare2", "binary"),
            ],
            "forensics": [
                Tool("autopsy", "4.22.1", "Digital forensics platform", "forensic"),
                Tool("binwalk", "2.4.2", "Firmware analysis", "forensic"),
                Tool("foremost", "1.5.7", "File carver", "forensic"),
                Tool("volatility", "3.2.0", "Memory forensics", "forensic"),
                Tool("sleuthkit", "4.12.2", "Forensics toolkit", "forensic"),
                Tool("photorec", "7.2", "File recovery", "forensic"),
                Tool("testdisk", "7.2", "Partition recovery", "forensic"),
                Tool("dd", "8.27", "Data dump tool", "forensic"),
                Tool("dc3dd", "7.2.646", "Forensic dd", "forensic"),
                Tool("extundelete", "0.2.4", "Ext3/4 recovery", "forensic"),
            ],
            "mobile": [
                Tool("frida", "17.3.2", "Dynamic instrumentation", "mobile"),
                Tool("objection", "1.11.0", "Mobile pentest framework", "mobile"),
                Tool("apktool", "2.7.0", "Android reverse engineering", "mobile"),
                Tool("jadx", "1.4.7", "Dex to Java decompiler", "mobile"),
                Tool("drozer", "2.4.4", "Android security testing", "mobile"),
                Tool("needle", "579", "iOS security testing", "mobile"),
                Tool("mobSF", "3.9.0", "Mobile analysis framework", "mobile"),
                Tool("andriller", "3.8", "Android forensics", "mobile"),
                Tool("apkx", "1.3", "APK extractor", "mobile"),
                Tool("android-tools", "33.0.4", "ADB and fastboot", "mobile"),
            ],
            "networking": [
                Tool("tcpdump", "4.99.4", "Network packet analyzer", "sniffer"),
                Tool("wireshark", "4.2.6", "Network protocol analyzer", "sniffer"),
                Tool("ettercap", "0.8.3", "Man-in-the-middle", "sniffer"),
                Tool("bettercap", "1.3.0", "Network reconnaissance", "sniffer"),
                Tool("mitmproxy", "10.1.8", "HTTPS proxy", "sniffer"),
                Tool("dsniff", "2.4", "Password sniffer", "sniffer"),
                Tool("netsniff", "0.2", "Network sniffer", "sniffer"),
                Tool("ngrep", "1.47", "Network grep", "sniffer"),
                Tool("netcat", "1.11", "Network Swiss army knife", "networking"),
                Tool("socat", "1.7.4.4", "Relay tool", "networking"),
            ],
            "recon": [
                Tool("recon-ng", "5.3.0", "Web reconnaissance", "recon"),
                Tool("maltego", "4.6.0", "Link analysis", "recon"),
                Tool("theHarvester", "9.0", "Email harvesting", "recon"),
                Tool("shodan", "2.2.0", "Internet scanning", "recon"),
                Tool("censys", "0.0.6", "Censys search", "recon"),
                Tool("amass", "2559", "Subdomain enumeration", "recon"),
                Tool("subfinder", "2.6.1", "Subdomain discovery", "recon"),
                Tool("assetfinder", "19.4", "Asset discovery", "recon"),
                Tool("findomain", "9.0", "Subdomain finder", "recon"),
                Tool("dnsenum", "1.2.4.2", "DNS enumeration", "recon"),
                Tool("dnsrecon", "1.5.1", "DNS reconnaissance", "recon"),
                Tool("sublist3r", "1.0", "Subdomain enumeration", "recon"),
            ],
            "crypto": [
                Tool("openssl", "3.2.0", "SSL/TLS toolkit", "crypto"),
                Tool("gpg", "2.4.5", "Encryption tool", "crypto"),
                Tool("hashcat", "6.2.6", "Hash cracker", "crypto"),
                Tool("john", "1.9.0", "Password cracker", "crypto"),
                Tool("pdfcrack", "0.20", "PDF password cracker", "crypto"),
                Tool("steghide", "0.5.1", "Steganography tool", "crypto"),
                Tool("zipcrack", "1.2", "ZIP password cracker", "crypto"),
                Tool("ssh-audit", "2.5.0", "SSH audit tool", "crypto"),
                Tool("testssl", "3.0.8", "SSL test tool", "crypto"),
                Tool("sslyze", "5.1.3", "SSL scanner", "crypto"),
            ],
            "misc": [
                Tool("tmux", "3.4a", "Terminal multiplexer", "misc"),
                Tool("screen", "4.9.0", "Terminal multiplexer", "misc"),
                Tool("vim", "9.1", "Text editor", "misc"),
                Tool("git", "2.43.0", "Version control", "misc"),
                Tool("curl", "8.7.1", "HTTP client", "misc"),
                Tool("wget", "1.24.5", "Download tool", "misc"),
                Tool("ping", "8.0", "Network ping", "misc"),
                Tool("traceroute", "2.1.4", "Network tracer", "misc"),
                Tool("nslookup", "8.18.1", "DNS lookup", "misc"),
                Tool("dig", "9.18.28", "DNS tool", "misc"),
            ],
        }
    
    def get_all_categories(self) -> List[str]:
        """Return all available categories"""
        return list(self.tools.keys())
    
    def get_tools_by_category(self, category: str) -> List[Dict]:
        """Get all tools in a specific category"""
        tools = self.tools.get(category.lower(), [])
        return [asdict(t) for t in tools]
    
    def search_tools(self, query: str) -> List[Dict]:
        """Search tools by name or description"""
        results = []
        query_lower = query.lower()
        
        for category, tools in self.tools.items():
            for tool in tools:
                if (query_lower in tool.name.lower() or 
                    query_lower in tool.description.lower() or
                    query_lower in category.lower()):
                    result = asdict(tool)
                    result['category'] = category
                    results.append(result)
        
        return results
    
    def get_tool_by_name(self, name: str) -> Optional[Dict]:
        """Get specific tool by name"""
        for category, tools in self.tools.items():
            for tool in tools:
                if tool.name.lower() == name.lower():
                    result = asdict(tool)
                    result['category'] = category
                    return result
        return None
    
    def get_random_tool(self, category: Optional[str] = None) -> Optional[Dict]:
        """Get a random tool, optionally from a specific category"""
        import random
        
        if category:
            tools = self.tools.get(category.lower(), [])
            if tools:
                tool = random.choice(tools)
                result = asdict(tool)
                result['category'] = category.lower()
                return result
        else:
            all_tools = []
            for cat, tools in self.tools.items():
                for tool in tools:
                    result = asdict(tool)
                    result['category'] = cat
                    all_tools.append(result)
            
            if all_tools:
                return random.choice(all_tools)
        
        return None
    
    def get_tools_count(self) -> Dict[str, int]:
        """Get count of tools per category"""
        return {cat: len(tools) for cat, tools in self.tools.items()}

# MCP Protocol Implementation
def handle_mcp_request(request: dict) -> dict:
    """Handle MCP protocol requests"""
    server = BlackArchMCPServer()
    method = request.get("method", "")
    params = request.get("params", {})
    
    response = {"jsonrpc": "2.0", "id": request.get("id")}
    
    if method == "tools/list":
        response["result"] = {
            "tools": [
                {
                    "name": "get_categories",
                    "description": "Get all BlackArch tool categories",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "get_tools",
                    "description": "Get tools by category",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Category name"}
                        },
                        "required": ["category"]
                    }
                },
                {
                    "name": "search_tools",
                    "description": "Search tools by name or description",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_tool",
                    "description": "Get specific tool info",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Tool name"}
                        },
                        "required": ["name"]
                    }
                },
                {
                    "name": "random_tool",
                    "description": "Get random tool from category",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string", "description": "Optional category"}
                        }
                    }
                },
                {
                    "name": "get_stats",
                    "description": "Get tool counts per category",
                    "inputSchema": {"type": "object", "properties": {}}
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        
        if tool_name == "get_categories":
            response["result"] = {"categories": server.get_all_categories()}
        elif tool_name == "get_tools":
            response["result"] = {"tools": server.get_tools_by_category(tool_args.get("category", ""))}
        elif tool_name == "search_tools":
            response["result"] = {"results": server.search_tools(tool_args.get("query", ""))}
        elif tool_name == "get_tool":
            response["result"] = {"tool": server.get_tool_by_name(tool_args.get("name", ""))}
        elif tool_name == "random_tool":
            response["result"] = {"tool": server.get_random_tool(tool_args.get("category"))}
        elif tool_name == "get_stats":
            response["result"] = {"stats": server.get_tools_count()}
        else:
            response["error"] = {"code": -32601, "message": f"Unknown tool: {tool_name}"}
    
    return response

if __name__ == "__main__":
    import sys
    
    # Load full tool database
    server = BlackArchMCPServer()
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ███████╗██╗  ██╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗  ║
    ║   ██╔════╝██║  ██║██╔═══██╗██╔══██╗████╗  ██║██╔════╝██║   ██║  ║
    ║   ███████╗███████║██║   ██║██████╔╝██╔██╗ ██║███████╗██║   ██║  ║
    ║   ╚════██║██╔══██║██║   ██║██╔══██╗██║╚██╗██║╚════██║██║   ██║  ║
    ║   ███████║██║  ██║╚██████╔╝██║  ██║██║ ╚████║███████║╚██████╔╝  ║
    ║   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ║
    ║                                                               ║
    ║            BLACKARCH TOOLS MCP SERVER v1.0                   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print(f"Loaded {sum(len(v) for v in server.tools.values())} tools across {len(server.tools)} categories")
    print("\nAvailable Categories:")
    for cat in sorted(server.tools.keys()):
        print(f"  • {cat.upper()} ({len(server.tools[cat])} tools)")
    
    print("\nStarting MCP Server on stdin/stdout...")
    print("Waiting for MCP requests...\n")
    
    # MCP server loop
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            response = handle_mcp_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": str(e)}
            }), flush=True)