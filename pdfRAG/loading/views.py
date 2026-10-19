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
        storage = FileSystemStorage(location=upload_dir)
        data = LoadingBase.objects.get_or_create(user=request.user)
        for file in request.FILES.getlist('files'):
            filename = str(Path(file.name).name)
            loaded_file = LoadFile.objects.get_or_create(file_path=filename)
            data.add(loaded_file)
            storage.save(filename, file)
        return redirect('home')

    return render(request, 'upload_file.html')

@login_required(login_url='login')
def remove_file(request, pk):
    pass