from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from loading.models import LoadFile, LoadingBase
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import Http404
from pathlib import Path
from utils.utils import get_file_size, file_caching

@login_required(login_url='login')
def availabel_files(request):
    data = LoadingBase.objects.filter(user=request.user).first()
    if data:
        upload_dir = Path(settings.UPLOAD_DIR)
        storage = FileSystemStorage(location=str(upload_dir))

        files_path = {"pdf": [],
                    "markdown": [],
                    "text": []}

        for file in data.files.all():
            if storage.exists(file.file_path):
                file_path = Path(upload_dir / file.file_path)
                suffix = file_path.suffix
                file_size = get_file_size(file_path)
                if suffix == ".pdf":
                    files_path["pdf"].append((str(file_path), file, file_size))
                elif suffix == ".md":
                    files_path["markdown"].append((str(file_path), file, file_size))
                else:
                    files_path["text"].append((str(file_path), file, file_size))

        context = {"files": files_path}
        return render(request, 'uploaded.html', context)
    return redirect('add-file')

@login_required(login_url='login')
def upload_files(request):
    allowed_files = {".md", ".txt", ".pdf"}
    MAX_FILE_SIZE = 10 * 1024 * 1024

    if request.method == 'POST':
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        storage = FileSystemStorage(location=upload_dir)
        data, _ = LoadingBase.objects.get_or_create(user=request.user)

        for file in request.FILES.getlist('files'):
            
            filename = Path(file.name).name
            suffix = Path(file.name).suffix.lower()

            if suffix not in allowed_files:
                continue

            if file.size > MAX_FILE_SIZE:
                continue

            if file_caching(file):
                continue

            saved_name = storage.save(filename, file)
            loaded_file = LoadFile.objects.create(file_path=saved_name)
            data.files.add(loaded_file)

        return redirect('uploaded-files')
    return render(request, 'upload_file.html')

@login_required(login_url='login')
@require_POST
def remove_file(request, pk):
    try:
        file = LoadFile.objects.get(pk=pk,
                                    loading_bases__user=request.user)
    except LoadFile.DoesNotExist:
        raise Http404("File not found")
    
    storage = FileSystemStorage(
        location=Path(settings.UPLOAD_DIR)
    )
    storage.delete(file.file_path)
    file.delete()
    return redirect('uploaded-files')
