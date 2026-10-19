from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from loading.models import LoadFile, LoadingBase
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.conf import settings

@login_required(login_url='login')
def upload_files(request):
    if request.method == 'POST':
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        storage = FileSystemStorage(location=upload_dir)
        data = LoadingBase.objects.get_or_create(user=request.user)

        for file in request.FILES.getlist('files'):
            filename = Path(file.name).name
            saved_name = storage.save(filename, file)
            loaded_file = LoadFile.objects.create(file_path=saved_name)
            data.files.add(loaded_file)
        return redirect('home')
    return render(request, 'upload_file.html')

@login_required(login_url='login')
def remove_file(request, pk):
    file = LoadFile.objects.get(id=pk)
    if request.method == 'POST':
        file.delete()
        return redirect('home')
    return redirect('home')