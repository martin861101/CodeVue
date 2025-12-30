import os
import subprocess
import sys
from pathlib import Path

class FileManager:
    def __init__(self, root_dir="."):
        self.root = Path(root_dir)
        self.write_allowed = False
        self.active_file = None

    def read_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(self, path, content):
        if not self.write_allowed:
            raise PermissionError("Write permission denied. Use /allow write")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    def execute_script(self, file_path):
        try:
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=15
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "exit_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False, 
                "output": "", 
                "error": "❌ Execution timed out (killed after 15s).",
                "exit_code": -1
            }
        except Exception as e:
            return {
                "success": False, 
                "output": "", 
                "error": f"❌ Execution failed: {str(e)}",
                "exit_code": -1
            }

    def scan_directory(self, path="."):
        path = Path(path)
        if not path.exists(): return []
        return [{"path": str(p), "type": "dir" if p.is_dir() else "file"} for p in path.iterdir()]
        
    def tree(self, path=".", level=0):
        # Simple tree implementation
        path = Path(path)
        tree_str = ""
        if level == 0:
            tree_str += f"{path.name}/\n"
        
        try:
            for entry in sorted(path.iterdir()):
                prefix = "  " * (level + 1)
                if entry.is_dir():
                    tree_str += f"{prefix}📁 {entry.name}/\n"
                    if level < 2: # Limit depth
                         tree_str += self.tree(entry, level + 1)
                else:
                    tree_str += f"{prefix}📄 {entry.name}\n"
        except PermissionError:
            pass
        return tree_str
    
    def create_project(self, name):
        p = Path(name)
        p.mkdir(exist_ok=True)
        (p / "main.py").touch()
        (p / "README.md").write_text(f"# {name}")
        return str(p)
