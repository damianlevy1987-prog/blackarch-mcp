#!/usr/bin/env python3
"""
BlackArch Security Tools - Complete Package
Installs, configures, and provides quick access to all BlackArch tools.
"""

import subprocess
import sys
import os

class BlackArchInstaller:
    """Installer and configuration manager for BlackArch tools"""
    
    def __init__(self):
        self.config = {
            "install_path": "/opt/blackarch",
            "tool_path": "/usr/bin",
            "config_dir": "~/.blackarch"
        }
    
    def check_blackarch_installed(self) -> bool:
        """Check if BlackArch is installed"""
        try:
            result = subprocess.run(['pacman', '-Qs', 'blackarch'], 
                                   capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def install_base_tools(self, categories: list = None):
        """Install common BlackArch tool categories"""
        if categories is None:
            categories = ['scanner', 'webapp', 'exploitation', 'cracker', 'wireless']
        
        print(f"Installing BlackArch categories: {', '.join(categories)}")
        
        for cat in categories:
            print(f"\n→ Installing blackarch-{cat}...")
            try:
                subprocess.run(['sudo', 'pacman', '-S', f'blackarch-{cat}', '--noconfirm'])
            except Exception as e:
                print(f"⚠ Could not install {cat}: {e}")
    
    def setup_config(self):
        """Setup configuration files"""
        config_dir = os.path.expanduser(self.config['config_dir'])
        os.makedirs(config_dir, exist_ok=True)
        
        # Create config file
        config = {
            "default_scanner": "nmap",
            "wordlists_path": "/usr/share/wordlists",
            "exploits_path": "/usr/share/exploitdb",
            "tools_installed": []
        }
        
        config_file = os.path.join(config_dir, 'config.json')
        import json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Configuration saved to {config_file}")
    
    def quick_scan(self, target: str, scan_type: str = "basic"):
        """Run quick security scan"""
        print(f"\n🎯 Starting {scan_type} scan on {target}...")
        
        if scan_type == "basic":
            commands = [
                f"nmap -sV {target}",
                f"nmap -sC {target}",
            ]
        elif scan_type == "full":
            commands = [
                f"nmap -sV -sC -p- -A {target}",
                f"nikto -h {target}",
            ]
        elif scan_type == "web":
            commands = [
                f"nikto -h {target}",
                f"dirb http://{target}",
                f"sqlmap -u http://{target} --batch",
            ]
        
        for cmd in commands:
            print(f"\n→ Running: {cmd}")
            os.system(cmd)
    
    def create_tool_scripts(self):
        """Create quick-access scripts for common tools"""
        scripts_dir = os.path.expanduser("~/.blackarch/scripts")
        os.makedirs(scripts_dir, exist_ok=True)
        
        # Nmap quick scan
        nmap_script = """#!/bin/bash
# Quick Nmap Scan
target=$1
[ -z "$target" ] && echo "Usage: $0 <target>" && exit 1
nmap -sV -sC -oA nmap_scan_$target $target
echo "Scan complete. Results in nmap_scan_$target.*"
"""
        
        # SQLMap scan
        sqlmap_script = """#!/bin/bash
# SQLMap Scan
url=$1
[ -z "$url" ] && echo "Usage: $0 <url>" && exit 1
sqlmap -u "$url" --batch --dbs
"""
        
        # Web scan
        web_script = """#!/bin/bash
# Web Security Scan
target=$1
[ -z "$target" ] && echo "Usage: $0 <target>" && exit 1
echo "Running web security scan on $target..."
nikto -h $target
dirb http://$target
nuclei -u http://$target
"""
        
        for name, content in [('nmap-scan', nmap_script), ('sqlmap-scan', sqlmap_script), ('web-scan', web_script)]:
            path = os.path.join(scripts_dir, name)
            with open(path, 'w') as f:
                f.write(content)
            os.chmod(path, 0o755)
            print(f"✓ Created {path}")
        
        print(f"\nScripts installed to {scripts_dir}")
        print("Add to PATH: export PATH=$PATH:~/.blackarch/scripts")
    
    def menu(self):
        """Interactive menu"""
        while True:
            print("""
╔═══════════════════════════════════════════════════════╗
║           BLACKARCH TOOLS MANAGER                    ║
╚═══════════════════════════════════════════════════════╝

  1. Install tool categories
  2. Quick scan (basic)
  3. Quick scan (full)
  4. Quick scan (web-focused)
  5. Create quick scripts
  6. MCP Server (start)
  7. MCP Client (interactive)
  8. Exit

""")
            choice = input("Select option: ").strip()
            
            if choice == '1':
                print("\nAvailable categories:")
                cats = ['scanner', 'webapp', 'exploitation', 'cracker', 'wireless', 
                       'forensic', 'recon', 'mobile', 'binary', 'defensive']
                for i, cat in enumerate(cats, 1):
                    print(f"  {i}. {cat}")
                selected = input("\nEnter category numbers (1,2,3): ").split(',')
                to_install = [cats[int(s.strip())-1] for s in selected if s.strip().isdigit()]
                self.install_base_tools(to_install)
            
            elif choice == '2':
                target = input("Target IP/hostname: ").strip()
                self.quick_scan(target, "basic")
            
            elif choice == '3':
                target = input("Target IP/hostname: ").strip()
                self.quick_scan(target, "full")
            
            elif choice == '4':
                target = input("Target IP/hostname: ").strip()
                self.quick_scan(target, "web")
            
            elif choice == '5':
                self.create_tool_scripts()
            
            elif choice == '6':
                print("\nStarting MCP Server...")
                os.system("python3 blackarch_mcp_v2.py")
            
            elif choice == '7':
                os.system("python3 blackarch_client.py")
            
            elif choice == '8':
                print("\nGoodbye!")
                break

def main():
    installer = BlackArchInstaller()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "install":
            categories = sys.argv[2:] if len(sys.argv) > 2 else None
            installer.install_base_tools(categories)
        
        elif cmd == "scan":
            if len(sys.argv) > 3:
                installer.quick_scan(sys.argv[2], sys.argv[3])
            else:
                print("Usage: python3 blackarch_manager.py scan <target> <basic|full|web>")
        
        elif cmd == "mcp":
            os.system("python3 blackarch_mcp_v2.py")
        
        elif cmd == "client":
            os.system("python3 blackarch_client.py")
        
        elif cmd == "web":
            os.system("python3 blackarch_web.py")
        
        elif cmd == "assistant":
            os.system("python3 blackarch_assistant.py")
        
        else:
            print(f"Unknown command: {cmd}")
            print("Available: install, scan, mcp, client, web, assistant")
    
    else:
        installer.menu()

if __name__ == "__main__":
    main()