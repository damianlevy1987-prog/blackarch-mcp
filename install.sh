#!/bin/bash
# BlackArch Tools - Installation Script

set -e

echo "
╔═══════════════════════════════════════════════════════════╗
║         BLACKARCH TOOLS - INSTALLATION WIZARD               ║
╚═══════════════════════════════════════════════════════════╝
"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Detect OS
detect_os() {
    if [ -f /etc/arch-release ]; then
        echo "Arch Linux"
    elif [ -f /etc/debian_version ]; then
        echo "Debian/Ubuntu"
    elif [ -f /etc/redhat-release ]; then
        echo "RedHat/CentOS"
    elif [ -f /etc/fedora-release ]; then
        echo "Fedora"
    elif [ -f /etc/alpine-release ]; then
        echo "Alpine"
    else
        echo "Unknown"
    fi
}

# Install dependencies
install_deps() {
    echo -e "${CYAN}Installing dependencies...${NC}"
    
    if command -v pacman &> /dev/null; then
        echo "Using pacman..."
        sudo pacman -Sy --noconfirm python python-pip curl nmap sqlmap nikto
    elif command -v apt-get &> /dev/null; then
        echo "Using apt..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip curl nmap sqlmap nikto
    elif command -v dnf &> /dev/null; then
        echo "Using dnf..."
        sudo dnf install -y python3 python3-pip curl nmap sqlmap
    elif command -v apk &> /dev/null; then
        echo "Using apk..."
        apk add --no-cache python3 py3-pip curl nmap
    fi
    
    echo -e "${GREEN}✓ Dependencies installed${NC}"
}

# Setup bash aliases
setup_aliases() {
    echo -e "${CYAN}Setting up aliases...${NC}"
    
    ALIAS_LINE="alias blackarch='/run/media/phoenix0/Ventoy/New Folder/blackarch.sh'"
    BASHRC="$HOME/.bashrc"
    
    if ! grep -q "blackarch.sh" "$BASHRC" 2>/dev/null; then
        echo "$ALIAS_LINE" >> "$BASHRC"
        echo -e "${GREEN}✓ Added alias to ~/.bashrc${NC}"
    else
        echo -e "${YELLOW}✓ Alias already exists${NC}"
    fi
    
    # Zsh support
    if [ -f "$HOME/.zshrc" ]; then
        if ! grep -q "blackarch.sh" "$HOME/.zshrc" 2>/dev/null; then
            echo "$ALIAS_LINE" >> "$HOME/.zshrc"
            echo -e "${GREEN}✓ Added alias to ~/.zshrc${NC}"
        fi
    fi
}

# Setup systemd service
setup_service() {
    echo -e "${CYAN}Setting up systemd service...${NC}"
    
    if command -v systemctl &> /dev/null; then
        sudo cp /run/media/phoenix0/Ventoy/New\ Folder/blackarch-mcp.service /etc/systemd/system/
        sudo systemctl daemon-reload
        echo -e "${GREEN}✓ Systemd service installed${NC}"
        echo -e "${YELLOW}Run: sudo systemctl enable --now blackarch-mcp${NC}"
    else
        echo -e "${YELLOW}⚠ systemctl not found, skipping service setup${NC}"
    fi
}

# Setup Docker
setup_docker() {
    echo -e "${CYAN}Setting up Docker...${NC}"
    
    if command -v docker &> /dev/null; then
        echo "Building Docker image..."
        docker build -t blackarch-mcp .
        echo -e "${GREEN}✓ Docker image built${NC}"
        echo -e "${YELLOW}Run: docker-compose up -d${NC}"
    else
        echo -e "${YELLOW}⚠ Docker not found, skipping${NC}"
    fi
}

# Create symlinks
setup_symlinks() {
    echo -e "${CYAN}Creating symlinks...${NC}"
    
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
    
    ln -sf /run/media/phoenix0/Ventoy/New\ Folder/blackarch.sh "$BIN_DIR/blackarch"
    ln -sf /run/media/phoenix0/Ventoy/New\ Folder/blackarch_client.py "$BIN_DIR/ba"
    
    if [ -d "$BIN_DIR" ] && [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        echo -e "${GREEN}✓ Symlinks created in ~/.local/bin${NC}"
    fi
}

# Verify installation
verify() {
    echo -e "${CYAN}Verifying installation...${NC}"
    
    if python3 -c "import json; print('✓ Python OK')" 2>/dev/null; then
        :
    fi
    
    if [ -f "/run/media/phoenix0/Ventoy/New Folder/blackarch_full_db.json" ]; then
        echo -e "${GREEN}✓ Database present${NC}"
    fi
    
    if [ -x "/run/media/phoenix0/Ventoy/New Folder/blackarch_mcp_v2.py" ]; then
        echo -e "${GREEN}✓ MCP server executable${NC}"
    fi
    
    if [ -x "/run/media/phoenix0/Ventoy/New Folder/blackarch.sh" ]; then
        echo -e "${GREEN}✓ CLI executable${NC}"
    fi
    
    echo -e "${GREEN}✓ Installation complete!${NC}"
}

# Main menu
main() {
    echo ""
    echo "Detected OS: $(detect_os)"
    echo ""
    
    options=("Full Install" "CLI Only" "MCP Server" "Docker" "Verify" "Exit")
    select opt in "${options[@]}"; do
        case $opt in
            "Full Install")
                install_deps
                setup_aliases
                setup_symlinks
                setup_service
                verify
                break
                ;;
            "CLI Only")
                install_deps
                setup_aliases
                setup_symlinks
                verify
                break
                ;;
            "MCP Server")
                install_deps
                setup_service
                verify
                break
                ;;
            "Docker")
                setup_docker
                break
                ;;
            "Verify")
                verify
                break
                ;;
            "Exit")
                echo "Goodbye!"
                exit 0
                ;;
        esac
    done
    
    echo ""
    echo -e "${CYAN}Quick Start:${NC}"
    echo "  ./blackarch.sh stats"
    echo "  python3 blackarch_mcp_v2.py"
    echo "  python3 blackarch_client.py categories"
    echo ""
}

main