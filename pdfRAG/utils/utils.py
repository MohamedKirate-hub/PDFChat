from django.conf import settings
import json
import hashlib
from pathlib import Path

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
        return {}

    with file_path.open('r') as file:
        data = json.load(file)
    return data

def save_json(file_path: str | Path, data):
    if not isinstance(file_path, str):
        file_path = Path(file_path)
    with file_path.open('w') as file:
        json.dump(data, file)

def file_caching(file_path: str) -> bool:
    print(f"file_path: {file_path}")
    files_cache_path = Path(settings.FILES_CACHE_PATH)
    files_cache_path.mkdir(parents=True, exist_ok=True)
    if not files_cache_path.is_dir():
        files_cache_path.touch(exist_ok=True)
    files_data = load_json(files_cache_path)

    content = Path(file_path).read_bytes()
    if file_path not in files_data.keys():
        files_data[file_path] = content_hash
        save_json(files_cache_path, files_data)
        return True

    content_hash = hashlib.sha256(content)
    if content_hash != files_data[file_path]:
        files_data[file_path] = content_hash
        save_json(files_cache_path, files_data)
        return True
    return False