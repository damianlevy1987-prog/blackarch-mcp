#!/usr/bin/env python3
"""
BlackArch MCP Integration for Claude Code
MCP client configuration and integration guide.
"""

import json
import os
from pathlib import Path

class BlackArchMCPConfig:
    """Configuration generator for Claude Code MCP integration"""
    
    def __init__(self):
        self.tools_path = Path("/run/media/phoenix0/Ventoy/New Folder")
        self.config = {
            "mcpServers": {
                "blackarch": {
                    "command": "python3",
                    "args": [str(self.tools_path / "blackarch_mcp_v2.py")],
                    "env": {
                        "BLACKARCH_PATH": str(self.tools_path)
                    }
                }
            }
        }
    
    def generate_claude_desktop_config(self) -> str:
        """Generate Claude Desktop MCP config"""
        config_dir = Path.home() / ".config" / "claude"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Try different config locations
        configs = [
            config_dir / "claude_desktop_config.json",
            Path.home() / ".claude" / "settings.json",
            Path.home() / ".config" / "Claude" / "claude_desktop_config.json",
        ]
        
        for config_path in configs:
            if config_path.parent.exists():
                with open(config_path, 'w') as f:
                    json.dump(self.config, f, indent=2)
                return str(config_path)
        
        # Fallback: print to stdout
        return json.dumps(self.config, indent=2)
    
    def generate_nvim_config(self) -> str:
        """Generate Neovim MCP config"""
        return """Add to ~/.config/nvim/mcp.json:
{
  "mcpServers": {
    "blackarch": {
      "command": "python3",
      "args": ["/run/media/phoenix0/Ventoy/New Folder/blackarch_mcp_v2.py"]
    }
  }
}
"""
    
    def generate_vscode_config(self) -> str:
        """Generate VS Code MCP config"""
        return """Add to .vscode/mcp.json:
{
  "ervers": {
    "blackarch": {
      "command": "python3",
      "args": ["/run/media/phoenix0/Ventoy/New Folder/blackarch_mcp_v2.py"]
    }
  }
}
"""
    
    def test_mcp_connection(self) -> bool:
        """Test MCP server connection"""
        import subprocess
        try:
            result = subprocess.run(
                ['python3', str(self.tools_path / 'blackarch_mcp_v2.py')],
                input='{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n',
                capture_output=True,
                text=True,
                timeout=5
            )
            return '"result"' in result.stdout
        except:
            return False

def main():
    config = BlackArchMCPConfig()
    
    print("""
╔════════════════════════════════════════════════════════╗
║     BLACKARCH MCP INTEGRATION FOR CLAUDE CODE         ║
╚════════════════════════════════════════════════════════╝
""")
    
    # Test connection
    print("→ Testing MCP server connection...")
    if config.test_mcp_connection():
        print("  ✓ MCP server is running and accessible")
    else:
        print("  ✗ MCP server not responding. Start with: python3 blackarch_mcp_v2.py")
    
    # Generate configs
    print("\n📄 Claude Desktop Config:")
    print(config.generate_claude_desktop_config())
    
    print("\n📄 For Neovim, add to ~/.config/nvim/mcp.json:")
    print(config.generate_nvim_config())
    
    # Write config file
    config_path = Path("/run/media/phoenix0/Ventoy/New Folder/mcp_config.json")
    with open(config_path, 'w') as f:
        json.dump({
            "blackarch": {
                "server_path": str(config.tools_path / "blackarch_mcp_v2.py"),
                "database_path": str(config.tools_path / "blackarch_full_db.json"),
                "protocol": "json-rpc",
                "version": "1.0"
            }
        }, f, indent=2)
    
    print(f"\n✓ Config saved to {config_path}")

if __name__ == "__main__":
    main()