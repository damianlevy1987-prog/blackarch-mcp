#!/usr/bin/env python3
"""Stdio handshake test for blackarch_mcp_v2 against the MCP wire contract."""
import json
import subprocess
import sys
from pathlib import Path

SERVER = Path(__file__).resolve().parent / "blackarch_mcp_v2.py"


def main() -> int:
    proc = subprocess.Popen(
        [sys.executable, str(SERVER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    failures = []

    def send(msg):
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()

    def recv():
        line = proc.stdout.readline()
        if not line:
            return None
        # Every stdout line must be valid JSON (protocol purity).
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            failures.append(f"stdout not JSON: {line!r}")
            return None

    # 1. initialize
    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2025-06-18",
                     "capabilities": {},
                     "clientInfo": {"name": "verify", "version": "0"}}})
    r = recv()
    if not r or r.get("id") != 1:
        failures.append("initialize: no/invalid response")
    else:
        res = r.get("result", {})
        if "protocolVersion" not in res or "serverInfo" not in res:
            failures.append(f"initialize: bad result shape {res}")

    # 2. notification (no id) -> must produce NO response
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    send({"jsonrpc": "2.0", "id": 2, "method": "ping"})
    r = recv()
    if not r or r.get("id") != 2:
        failures.append(f"notification leaked a response or ping failed: {r}")

    # 3. tools/list
    send({"jsonrpc": "2.0", "id": 3, "method": "tools/list"})
    r = recv()
    tools = (r or {}).get("result", {}).get("tools", [])
    if len(tools) < 8:
        failures.append(f"tools/list: expected 8 tools, got {len(tools)}")

    # 4. tools/call search -> MCP content array
    send({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
          "params": {"name": "search", "arguments": {"query": "nmap", "limit": 5}}})
    r = recv()
    res = (r or {}).get("result", {})
    content = res.get("content")
    if not isinstance(content, list) or not content or content[0].get("type") != "text":
        failures.append(f"tools/call: bad content shape {res}")
    elif res.get("isError"):
        failures.append(f"tools/call search errored: {content}")
    else:
        payload = json.loads(content[0]["text"])
        if not payload.get("results"):
            failures.append("tools/call search: empty results for 'nmap'")

    # 5. stats call (database must actually be loaded)
    send({"jsonrpc": "2.0", "id": 5, "method": "tools/call",
          "params": {"name": "stats", "arguments": {}}})
    r = recv()
    text = (r or {}).get("result", {}).get("content", [{}])[0].get("text", "{}")
    stats = json.loads(text)
    if stats.get("total_tools", 0) < 2000:
        failures.append(f"stats: DB not loaded properly -> {stats.get('total_tools')}")

    # 6. unknown method -> JSON-RPC error
    send({"jsonrpc": "2.0", "id": 6, "method": "no/such"})
    r = recv()
    if not r or "error" not in r:
        failures.append(f"unknown method: expected error, got {r}")

    # 7. params: null must not crash (AttributeError regression guard)
    send({"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": None})
    r = recv()
    if not r or r.get("id") != 7:
        failures.append(f"params:null: expected id-7 reply, got {r}")

    # 8. malformed JSON -> -32700 parse error
    proc.stdin.write("this is not json\n")
    proc.stdin.flush()
    r = recv()
    if not r or r.get("error", {}).get("code") != -32700:
        failures.append(f"parse error: expected -32700, got {r}")

    # 9. error replies must carry the request id (correlation guard)
    send({"jsonrpc": "2.0", "id": 99, "method": "tools/call",
          "params": {"name": "no_such_tool", "arguments": {}}})
    r = recv()
    if not r or r.get("id") != 99:
        failures.append(f"id correlation: expected id 99, got {r}")

    proc.stdin.close()
    proc.wait(timeout=10)
    stderr = proc.stderr.read()
    if stderr:
        print(f"[stderr captured, {len(stderr)} bytes] OK (logs off stdout)")

    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("PASS: all 9 handshake checks green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
