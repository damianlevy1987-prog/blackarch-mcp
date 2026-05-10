# BlackArch MCP Server Dockerfile
FROM python:3.11-slim

LABEL maintainer="BlackArch"
LABEL description="BlackArch Tools MCP Server - 2863+ security tools"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nmap \
    sqlmap \
    nikto \
    dnsenum \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY blackarch_mcp_v2.py /app/
COPY blackarch_client.py /app/
COPY blackarch_full_db.json /app/

# Make scripts executable
RUN chmod +x /app/blackarch_mcp_v2.py

# Environment variables
ENV BLACKARCH_PATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import json; json.loads(open('/app/blackarch_full_db.json').read())" || exit 1

# Run MCP server
CMD ["python3", "/app/blackarch_mcp_v2.py"]