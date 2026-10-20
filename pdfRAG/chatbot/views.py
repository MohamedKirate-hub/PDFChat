from django.shortcuts import render, redirect
from loading.models import LoadingBase
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rag_system.system import RagManager
from pathlib import Path
from django.contrib.auth.decorators import login_required

def see_files(request):
    data = LoadingBase.objects.get(user=request.user)
    upload_dir = Path(settings.UPLOAD_DIR)
    storage = FileSystemStorage(location=str(upload_dir))
    files_path = []
    for file in data.files.all():
        if storage.exists(file.file_path):
            files_path.append(upload_dir / file.file_path)

    return render(request, 'test.html')

@login_required(login_url='login')
def chatbot(request):
    if LoadingBase.objects.filter(user=request.user).exists():
        data = LoadingBase.objects.get(user=request.user)
        upload_dir = settings.UPLOAD_DIR
        files_path = []
        for file in data.files.all():
            file_path = upload_dir / file.file_path
            files_path.append(file_path)
        if request.method == 'POST':
            query = request.POST.get("query")
            rag_system = RagManager(files_path)
            answer = rag_system.generate(query)
            context = {"answer": answer}
        else:
            pass
    return redirect('add-file')