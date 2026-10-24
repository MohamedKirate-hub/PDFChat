from django.conf import settings
import json
from pathlib import Path
from datetime import datetime

class LogsInfo:
    def __init__(self, content: str, type: str, status_code=None):
        self.content = content
        self.type = type
        self.status_code = status_code
        self.logs_dir = Path("data/logs")
        self.logs_path = self.logs_dir / Path("logs.txt")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        if not self.logs_path.exists():
            self.logs_path.touch()
    
    def _create_content(self):
        time = datetime.now()
        message = (f"Time: {time} | "
                   f"From: {self.type.upper()} | "
                   f"HTTP: {self.status_code or 'N/A'} | "
                   f"Issue: {self.content}")
        return message

    def _save_content(self, file_path: Path, content: str):
        with file_path.open('a', encoding='utf-8') as file:
            file.write(content)

    def _show_logs(self, file_path: Path):
        with file_path.open('r', encoding='utf-8') as file:
            return file.readlines()

    def save(self):
        message = self._create_content()
        self._save_content(self.logs_path, message)

    def show(self):
        return self._show_logs(self.logs_path)

def get_file_size(file_path: Path) -> str:
    size = file_path.stat().st_size
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.2f} {units[index]}"

def load_json(file_path: str | Path):
    if not isinstance(file_path, str):
        file_path = Path(file_path)

    if file_path.stat().st_size == 0:
        return dict()

    with file_path.open('r') as file:
        data = json.load(file)
    return data

def save_json(file_path: str | Path, data):
    if not isinstance(file_path, str):
        file_path = Path(file_path)

    if file_path.exists():
        file_path.touch()

    with file_path.open('w') as file:
        json.dump(data, file, indent=4)
