#!/usr/bin/env python3
"""
BlackArch Tools - API Wrapper
Python library for programmatic access to BlackArch tools.
"""

import json
import subprocess
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class Tool:
    name: str
    version: str
    description: str
    category: Optional[str] = None
    install_command: Optional[str] = None

class BlackArchAPI:
    """Python API for BlackArch tools"""
    
    def __init__(self, db_path: str = "/run/media/phoenix0/Ventoy/New Folder/blackarch_full_db.json"):
        self.db_path = Path(db_path)
        self._cache: Dict = {}
        self._load_db()
    
    def _load_db(self):
        """Load tool database"""
        if self.db_path.exists():
            with open(self.db_path) as f:
                data = json.load(f)
                self._cache = data.get("categories", {})
    
    def categories(self) -> List[str]:
        """List all categories"""
        return list(self._cache.keys())
    
    def tools(self, category: str, limit: int = 100) -> List[Tool]:
        """Get tools in category"""
        tools = self._cache.get(category.lower(), [])
        return [Tool(**t) for t in tools[:limit]]
    
    def search(self, query: str) -> List[Tool]:
        """Search for tools"""
        results = []
        q = query.lower()
        for cat, tools in self._cache.items():
            for t in tools:
                if q in t['name'].lower() or q in t['description'].lower():
                    results.append(Tool(**t, category=cat))
        return results
    
    def find(self, name: str) -> Optional[Tool]:
        """Find exact tool"""
        n = name.lower()
        for cat, tools in self._cache.items():
            for t in tools:
                if n in t['name'].lower():
                    return Tool(**t, category=cat)
        return None
    
    def random(self, count: int = 5) -> List[Tool]:
        """Get random tools"""
        import random
        all_tools = [(cat, t) for cat, tools in self._cache.items() for t in tools]
        selected = random.sample(all_tools, min(count, len(all_tools)))
        return [Tool(**t, category=cat) for cat, t in selected]
    
    def by_tag(self, tags: List[str]) -> List[Tool]:
        """Find tools by tags"""
        results = []
        tag_set = {t.lower() for t in tags}
        for cat, tools in self._cache.items():
            for t in tools:
                for tag in tag_set:
                    if tag in cat.lower() or tag in t['name'].lower() or tag in t['description'].lower():
                        results.append(Tool(**t, category=cat))
                        break
        return results
    
    def stats(self) -> Dict:
        """Get statistics"""
        return {
            "total_tools": sum(len(v) for v in self._cache.values()),
            "total_categories": len(self._cache),
            "categories": {cat: len(tools) for cat, tools in self._cache.items()}
        }
    
    def export(self, format: str = "json") -> str:
        """Export database"""
        if format == "json":
            return json.dumps(self._cache, indent=2)
        elif format == "markdown":
            md = "# BlackArch Tools\n\n"
            for cat in sorted(self._cache.keys()):
                md += f"## {cat.upper()}\n\n"
                for t in self._cache[cat]:
                    md += f"- **{t['name']}** `{t['version']}` - {t['description']}\n"
                md += "\n"
            return md
        return ""

# CLI interface
if __name__ == "__main__":
    api = BlackArchAPI()
    
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "list":
            print("\n".join(sorted(api.categories())))
        
        elif cmd == "search" and len(sys.argv) > 2:
            for t in api.search(sys.argv[2]):
                print(f"[{t.category:12}] {t.name} - {t.description}")
        
        elif cmd == "find" and len(sys.argv) > 2:
            t = api.find(sys.argv[2])
            if t:
                print(f"Name: {t.name}")
                print(f"Version: {t.version}")
                print(f"Category: {t.category}")
                print(f"Description: {t.description}")
            else:
                print("Not found")
        
        elif cmd == "stats":
            s = api.stats()
            print(f"Total tools: {s['total_tools']}")
            print(f"Categories: {s['total_categories']}")
        
        elif cmd == "random":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            for t in api.random(count):
                print(f"[{t.category:12}] {t.name}")
        
        else:
            print("Commands: list, search <query>, find <name>, stats, random [count]")
    else:
        print("BlackArch API v1.0")
        print("Commands: list, search <query>, find <name>, stats, random [count]")