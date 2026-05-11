# BlackArch MCP Server

**2,863+ security tools** organized across **48 categories** with MCP server, CLI, Web UI, and Python API.

[![Tests](https://img.shields.io/badge/tests-16%20passed-brightgreen)](https://github.com/damianlevy1987-prog/blackarch-mcp)
[![Tools](https://img.shields.io/badge/tools-2863-blue)](https://github.com/damianlevy1987-prog/blackarch-mcp)
[![Categories](https://img.shields.io/badge/categories-48-orange)](https://github.com/damianlevy1987-prog/blackarch-mcp)

## Features

- ✅ **MCP Server** - Model Context Protocol server for AI integration
- ✅ **CLI Tools** - Bash CLI with colored output
- ✅ **Python API** - Full Python library
- ✅ **Web Interface** - HTTP server on port 8080
- ✅ **Test Suite** - 16/16 tests passing
- ✅ **Docker Support** - Ready for containerization

---

## 🚀 Quick Start

### Clone & Run MCP Server

```bash
git clone https://github.com/damianlevy1987-prog/blackarch-mcp.git
cd blackarch-mcp
python3 blackarch_mcp_v2.py
```

### MCP Server Endpoints

| Method | Description |
|--------|-------------|
| `tools/list` | List all available tools |
| `tools/call` | Execute a tool |

### Available Tools

| Tool | Description |
|------|-------------|
| `get_categories` | List all 48 categories |
| `get_tools` | Get tools by category |
| `search` | Search by name/description |
| `get_tool` | Detailed tool info |
| `random` | Random tool selector |
| `stats` | Database statistics |
| `by_tags` | Find by keywords |
| `cheat_sheet` | Common commands |

---

## 📊 Database

- **2,863 tools** across **48 categories**
- Top: WEBAPP(309), SCANNER(305), RECON(257)

---

## 🔧 Installation

```bash
# Clone or download
git clone https://github.com/damianlevy1987-prog/blackarch-mcp.git
cd blackarch-mcp

# Run installer
./install.sh

# Or use directly
python3 blackarch_mcp_v2.py
```

---

## 📦 Files

| File | Description |
|------|-------------|
| `blackarch_mcp_v2.py` | **Main MCP server** |
| `blackarch_client.py` | Python MCP client |
| `blackarch.sh` | Bash CLI |
| `blackarch_api.py` | Python API |
| `blackarch_web.py` | Web interface |
| `blackarch_full_db.json` | Tool database (2863 tools) |
| `test_blackarch.py` | Test suite (16 tests) |
| `Dockerfile` | Docker image |
| `docker-compose.yml` | Docker Compose setup |
| `install.sh` | Installation wizard |

---

## 🧪 Testing

```bash
python3 test_blackarch.py
# 16/16 tests passed
```

---

## 🐳 Docker

```bash
# Build and run
docker-compose up -d

# Or build manually
docker build -t blackarch-mcp .
docker run -p 8080:8080 blackarch-mcp
```

---

## 📄 License

MIT License

## 🔗 Links

- [BlackArch Linux](https://blackarch.org)
- [MCP Protocol](https://modelcontextprotocol.io)
- [GitHub Repository](https://github.com/damianlevy1987-prog/blackarch-mcp)
- [Releases](https://github.com/damianlevy1987-prog/blackarch-mcp/releases)