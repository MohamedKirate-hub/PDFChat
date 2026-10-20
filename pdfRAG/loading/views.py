from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from loading.models import LoadFile, LoadingBase
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import Http404

@login_required(login_url='login')
def availabel_files(request):
    data = LoadingBase.objects.get(user=request.user)
    upload_dir = Path(settings.UPLOAD_DIR)
    storage = FileSystemStorage(location=str(upload_dir))

    files_path = {"pdf": [],
                  "markdown": [],
                  "text": []}

    for file in data.files.all():
        if storage.exists(file.file_path):
            file_path = Path(upload_dir / file.file_path)
            suffix = file_path.suffix
            if suffix == ".pdf":
                files_path["pdf"].append((str(file_path), file))
            elif suffix == ".md":
                files_path["markdown"].append((str(file_path), file))
            else:
                files_path["text"].append(str(file_path))

    context = {"files": files_path}
    return render(request, 'uploaded.html', context)

@login_required(login_url='login')
def upload_files(request):
    if request.method == 'POST':
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        storage = FileSystemStorage(location=upload_dir)
        data, created = LoadingBase.objects.get_or_create(user=request.user)

        for file in request.FILES.getlist('files'):
            filename = Path(file.name).name
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
