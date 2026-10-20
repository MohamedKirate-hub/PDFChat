from django.shortcuts import render, redirect
from loading.models import LoadingBase
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rag_system.system import RagManager
from pathlib import Path
from django.contrib.auth.decorators import login_required
from user_auth.models import User, UserRole
from chatbot.models import ConversationRoom, Message

def see_files(request):
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
                files_path["pdf"].append(str(file_path))
            elif suffix == ".md":
                files_path["markdown"].append(str(file_path))
            else:
                files_path["text"].append(str(file_path))

    context = {"files": files_path}
    return render(request, 'uploaded.html', context)

@login_required(login_url='login')
def chatbot(request):
    if LoadingBase.objects.filter(user=request.user).exists():
        data = LoadingBase.objects.get(user=request.user)
        conversation, _ = ConversationRoom.objects.get_or_create(owner=request.user)
        upload_dir = Path(settings.UPLOAD_DIR)
        files_path = []

        for file in data.files.all():
            file_path = upload_dir / file.file_path
            files_path.append(str(file_path))

        if request.method == 'POST':
            user_role = UserRole.objects.get(name="assistant")
            assistant = User.objects.get(role=user_role)
            query = request.POST.get("query")
            user_message = Message.objects.create(
                owner = request.user,
                body = query)
    
            rag_system = RagManager(files_path)
            answer = rag_system.generate(query)

            assistant_message = Message.objects.create(
                owner = assistant,
                body = answer)

            conversation.conversations.add(user_message, assistant_message)
        context = {'conversations': conversation.conversations.all()}
        return render(request, "chatbot.html", context)

    return redirect('add-file')