from pathlib import Path
import os
import subprocess

class FileManager:
    def __init__(self, root: Path = None):
        self.root = root or Path.cwd()
        self.write_allowed = False
        self.active_file = None
    
    def resolve_path(self, path: str) -> Path:
        """Resolve and validate path within project root"""
        resolved = (self.root / path).resolve()
        if not str(resolved).startswith(str(self.root)):
            raise PermissionError(f"Access denied: {path} is outside project root")
        return resolved
    
    def scan_directory(self, path: str = ".") -> list:
        """List files in directory"""
        dir_path = self.resolve_path(path)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory")
        
        files = []
        for item in sorted(dir_path.iterdir()):
            if item.name.startswith('.'):
                continue
            files.append({
                'name': item.name,
                'type': 'dir' if item.is_dir() else 'file',
                'path': str(item.relative_to(self.root))
            })
        return files
    
    def read_file(self, path: str) -> str:
        """Read file contents"""
        file_path = self.resolve_path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        try:
            return file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            return f"[Binary file: {path}]"
    
    def write_file(self, path: str, content: str):
        """Write file contents (requires permission)"""
        if not self.write_allowed:
            raise PermissionError("Write permission denied. Use /allow write")
        
        file_path = self.resolve_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        return file_path
    
    def execute_python(self, path: str) -> str:
        """Execute Python file and return output"""
        file_path = self.resolve_path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        try:
            result = subprocess.run(
                ['python', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.root
            )
            output = result.stdout
            if result.stderr:
                output += f"\n[stderr]\n{result.stderr}"
            return output
        except subprocess.TimeoutExpired:
            return "❌ Execution timeout (30s)"
        except Exception as e:
            return f"❌ Execution error: {str(e)}"
    
    def create_project(self, name: str):
        """Create new project structure"""
        project_path = self.root / name
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create basic structure
        (project_path / "README.md").write_text(f"# {name}\n\nCreated by Neuroterm")
        (project_path / "src").mkdir(exist_ok=True)
        (project_path / "tests").mkdir(exist_ok=True)
        
        return project_path
    
    def tree(self, path: str = ".", max_depth: int = 3) -> str:
        """Generate directory tree"""
        def _tree(dir_path: Path, prefix: str = "", depth: int = 0):
            if depth >= max_depth:
                return ""
            
            lines = []
            try:
                items = sorted([p for p in dir_path.iterdir() if not p.name.startswith('.')])
            except PermissionError:
                return ""
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current = "└── " if is_last else "├── "
                lines.append(f"{prefix}{current}{item.name}")
                
                if item.is_dir():
                    extension = "    " if is_last else "│   "
                    lines.append(_tree(item, prefix + extension, depth + 1))
            
            return "\n".join(filter(None, lines))
        
        start_path = self.resolve_path(path)
        return f"{start_path.name}/\n" + _tree(start_path)
