#!/usr/bin/env python3
"""
BlackArch MCP Server - Web Interface
A simple web interface for the BlackArch MCP server.
"""

import json
import subprocess
import http.server
import socketserver
import urllib.parse
from pathlib import Path

PORT = 8080

class BlackArchHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for BlackArch MCP interface"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == '/' or path == '/index.html':
            self.send_html(self._get_index_html())
        elif path == '/api/categories':
            self.send_json(self._mcp_request({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "get_categories", "arguments": {}}
            }))
        elif path == '/api/stats':
            self.send_json(self._mcp_request({
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "stats", "arguments": {}}
            }))
        elif path.startswith('/api/tools/'):
            category = path.split('/')[-1]
            self.send_json(self._mcp_request({
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "get_tools", "arguments": {"category": category, "limit": 50}}
            }))
        elif path.startswith('/api/search?'):
            query = urllib.parse.parse_qs(parsed.query).get('q', [''])[0]
            self.send_json(self._mcp_request({
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "search", "arguments": {"query": query}}
            }))
        elif path.startswith('/api/cheatsheet?'):
            category = urllib.parse.parse_qs(parsed.query).get('category', [''])[0]
            self.send_json(self._mcp_request({
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {"name": "cheat_sheet", "arguments": {"category": category}}
            }))
        elif path == '/api/random':
            self.send_json(self._mcp_request({
                "jsonrpc": "2.0",
                "id": 6,
                "method": "tools/call",
                "params": {"name": "random", "arguments": {"count": 10}}
            }))
        else:
            self.send_error(404)
    
    def _mcp_request(self, request: dict) -> dict:
        """Send request to MCP server"""
        try:
            result = subprocess.run(
                ['python3', '/run/media/phoenix0/Ventoy/New Folder/blackarch_mcp_v2.py'],
                input=json.dumps(request),
                capture_output=True,
                text=True,
                timeout=10
            )
            lines = result.stdout.strip().split('\n')
            for line in reversed(lines):
                if line.strip().startswith('{'):
                    return json.loads(line)
            return {"error": "No response"}
        except Exception as e:
            return {"error": str(e)}
    
    def send_json(self, data: dict):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def send_html(self, html: str):
        """Send HTML response"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def _get_index_html(self) -> str:
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlackArch MCP Server</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #00ff00; text-align: center; margin: 20px 0; text-shadow: 0 0 10px #00ff00; }
        h2 { color: #00cc00; margin: 20px 0 10px; border-bottom: 1px solid #00ff00; padding-bottom: 5px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-card { background: #111; border: 1px solid #00ff00; padding: 15px; text-align: center; }
        .stat-value { font-size: 2em; color: #00ff00; }
        .stat-label { color: #009900; font-size: 0.8em; }
        .categories { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 10px; }
        .category { background: #111; border: 1px solid #003300; padding: 10px; cursor: pointer; transition: all 0.3s; }
        .category:hover { border-color: #00ff00; background: #1a1a1a; }
        .category-name { font-weight: bold; color: #00ff00; }
        .category-count { color: #009900; font-size: 0.8em; }
        .tools-list { display: none; background: #0d0d0d; border: 1px solid #00ff00; padding: 15px; margin: 10px 0; max-height: 400px; overflow-y: auto; }
        .tool { background: #111; padding: 10px; margin: 5px 0; border-left: 3px solid #00ff00; }
        .tool-name { color: #00ff00; font-weight: bold; }
        .tool-version { color: #009900; font-size: 0.8em; margin-left: 10px; }
        .tool-desc { color: #00cc00; font-size: 0.9em; margin-top: 5px; }
        .search-box { width: 100%; padding: 15px; background: #111; border: 1px solid #00ff00; color: #00ff00; font-family: inherit; margin: 20px 0; }
        .search-box::placeholder { color: #006600; }
        .btn { background: #003300; border: 1px solid #00ff00; color: #00ff00; padding: 10px 20px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #004400; }
        .nav { display: flex; gap: 10px; margin: 20px 0; flex-wrap: wrap; }
        .nav a { color: #00ff00; text-decoration: none; padding: 10px 20px; background: #111; border: 1px solid #003300; }
        .nav a:hover { border-color: #00ff00; }
        pre { background: #0d0d0d; padding: 15px; border: 1px solid #003300; overflow-x: auto; }
        code { color: #00ff00; }
    </style>
</head>
<body>
    <div class="container">
        <h1>█ BLACKARCH MCP SERVER █</h1>
        <p style="text-align:center;color:#009900">2863+ Security Tools • 48 Categories • MCP Protocol</p>
        
        <div class="nav">
            <a href="#" onclick="showSection('stats')">Statistics</a>
            <a href="#" onclick="showSection('categories')">Categories</a>
            <a href="#" onclick="showSection('search')">Search</a>
            <a href="#" onclick="showSection('random')">Random Tools</a>
            <a href="#" onclick="showSection('mcp')">MCP Protocol</a>
        </div>
        
        <div id="stats-section">
            <h2>📊 Statistics</h2>
            <div class="stats" id="stats-container">Loading...</div>
        </div>
        
        <div id="categories-section" style="display:none">
            <h2>📁 Categories</h2>
            <div class="categories" id="categories-container">Loading...</div>
        </div>
        
        <div id="search-section" style="display:none">
            <h2>🔍 Search</h2>
            <input type="text" class="search-box" id="search-input" placeholder="Search for tools (e.g., nmap, sql, exploit)..." onkeyup="if(event.key==='Enter')search()">
            <button class="btn" onclick="search()">Search</button>
            <div id="search-results"></div>
        </div>
        
        <div id="random-section" style="display:none">
            <h2>🎲 Random Tools</h2>
            <button class="btn" onclick="getRandom()">Get Random Tools</button>
            <div id="random-results"></div>
        </div>
        
        <div id="mcp-section" style="display:none">
            <h2>🔧 MCP Protocol</h2>
            <p>Use these JSON-RPC requests to integrate with Claude Code or other MCP clients:</p>
            <pre><code>{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_tools",
    "arguments": {"category": "scanner", "limit": 20}
  }
}</code></pre>
            <h3>Available Tools:</h3>
            <ul>
                <li><strong>get_categories</strong> - List all 48 categories</li>
                <li><strong>get_tools</strong> - Get tools in category</li>
                <li><strong>search</strong> - Search by name/description</li>
                <li><strong>get_tool</strong> - Get specific tool info</li>
                <li><strong>random</strong> - Get random tools</li>
                <li><strong>stats</strong> - Database statistics</li>
                <li><strong>cheat_sheet</strong> - Common commands</li>
            </ul>
        </div>
    </div>
    
    <script>
        function showSection(name) {
            ['stats', 'categories', 'search', 'random', 'mcp'].forEach(s => {
                document.getElementById(s + '-section').style.display = s === name ? 'block' : 'none';
            });
            if (name === 'stats') loadStats();
            if (name === 'categories') loadCategories();
            if (name === 'random') getRandom();
        }
        
        async function loadStats() {
            const res = await fetch('/api/stats');
            const data = await res.json();
            document.getElementById('stats-container').innerHTML = 
                `<div class="stat-card"><div class="stat-value">${data.total_tools || 0}</div><div class="stat-label">TOTAL TOOLS</div></div>
                 <div class="stat-card"><div class="stat-value">${data.total_categories || 0}</div><div class="stat-label">CATEGORIES</div></div>`;
        }
        
        async function loadCategories() {
            const res = await fetch('/api/categories');
            const data = await res.json();
            document.getElementById('categories-container').innerHTML = data.categories.map(c => 
                `<div class="category" onclick="loadTools('${c.name}')">
                    <div class="category-name">${c.name.toUpperCase()}</div>
                    <div class="category-count">${c.count} tools</div>
                </div>`
            ).join('');
        }
        
        async function loadTools(category) {
            const res = await fetch('/api/tools/' + category);
            const data = await res.json();
            document.getElementById('categories-container').innerHTML = 
                `<button class="btn" onclick="loadCategories()">← Back</button>
                 <h3>${category.toUpperCase()}</h3>
                 <div class="tools-list" style="display:block">` +
                (data.tools || []).map(t => 
                    `<div class="tool">
                        <span class="tool-name">${t.name}</span>
                        <span class="tool-version">${t.version}</span>
                        <div class="tool-desc">${t.description}</div>
                    </div>`
                ).join('') + '</div>';
        }
        
        async function search() {
            const q = document.getElementById('search-input').value;
            if (!q) return;
            const res = await fetch('/api/search?q=' + encodeURIComponent(q));
            const data = await res.json();
            document.getElementById('search-results').innerHTML = 
                `<h3>Results for "${q}":</h3><div class="tools-list" style="display:block">` +
                (data.results || []).map(t => 
                    `<div class="tool">
                        <span class="tool-name">${t.name}</span>
                        <span class="tool-version">[${t.category}]</span>
                        <div class="tool-desc">${t.description}</div>
                    </div>`
                ).join('') + '</div>';
        }
        
        async function getRandom() {
            const res = await fetch('/api/random');
            const data = await res.json();
            document.getElementById('random-results').innerHTML = 
                `<div class="tools-list" style="display:block">` +
                (data.tools || []).map(t => 
                    `<div class="tool">
                        <span class="tool-name">${t.name}</span>
                        <span class="tool-version">[${t.category}]</span>
                        <div class="tool-desc">${t.description}</div>
                    </div>`
                ).join('') + '</div>';
        }
        
        loadStats();
    </script>
</body>
</html>"""

def run_server():
    """Run the HTTP server"""
    with socketserver.TCPServer(("", PORT), BlackArchHandler) as httpd:
        print(f"""
╔═══════════════════════════════════════════════════════╗
║  BLACKARCH MCP WEB INTERFACE                         ║
║  Server running at http://localhost:{PORT}             ║
║  Press Ctrl+C to stop                               ║
╚═══════════════════════════════════════════════════════╝
        """)
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()