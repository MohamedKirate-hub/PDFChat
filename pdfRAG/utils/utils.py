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
        return dict()

    with file_path.open('r') as file:
        data = json.load(file)
    return data

def save_json(file_path: str | Path, data):
    if not isinstance(file_path, str):
        file_path = Path(file_path)
    with file_path.open('w') as file:
        json.dump(data, file, indent=4)

def file_caching(file_path: str) -> bool:
    cache_path = Path(settings.FILES_CACHE_PATH)
    cache_path.mkdir(parents=True, exist_ok=True)
    cache_path = cache_path / settings.CACHE_FILE

    if not cache_path.exists():
        cache_path.touch()

    files_data = load_json(cache_path)

    content = Path(file_path).read_bytes()
    content_hash = hashlib.sha256(content).hexdigest()
    cache_key = file_path.name

    if content_hash in files_data.values():
        return False

    files_data[cache_key] = content_hash
    save_json(cache_path, files_data)
    return True

def delete_cache(file_path: str):
    cache_path = Path(settings.FILES_CACHE_PATH) / settings.CACHE_FILE
    cache = load_json(cache_path)
    if file_path in cache:
        cache.pop(file_path)
    save_json(cache_path, cache)