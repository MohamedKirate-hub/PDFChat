from django.shortcuts import render, redirect, get_object_or_404
from loading.models import LoadingBase
from django.conf import settings
from rag_system.system import RagManager
from pathlib import Path
from django.contrib.auth.decorators import login_required
from user_auth.models import User, UserRole
from chatbot.models import Conversation, Message, ConversationRoom
from django.views.decorators.http import require_POST

def home_view(request):
    return render(request, 'home.html')

@login_required(login_url="login")
@require_POST
def create_conversation(request):
    room, _ = ConversationRoom.objects.get_or_create(user=request.user)
    conversation = Conversation.objects.create(room = room)
    return redirect('conversation-chat', pk=conversation.pk)

@login_required(login_url='login')
def converstaions_view(request):
    user_conversations = Conversation.objects.filter(room__user=request.user)
    context = {"conversations": user_conversations}
    return render(request, 'conversations.html', context)

@login_required(login_url='login')
def chatbot(request, pk):
    if LoadingBase.objects.filter(user=request.user).exists():
        data = LoadingBase.objects.get(user=request.user)
        conversation = Conversation.objects.get(room__user=request.user, pk=pk)
        upload_dir = Path(settings.UPLOAD_DIR)
        files_path = []

        for file in data.files.all():
            file_path = upload_dir / file.file_path
            files_path.append(str(file_path))

        if not files_path:
            return redirect('add-file')

        if request.method == 'POST':
            user_role = UserRole.objects.get(name="assistant")
            assistant = User.objects.get(role=user_role)
            query = request.POST.get("query", "").strip()
            model_name = request.POST.get("models","Qwen/Qwen3-0.6B")
            print(model_name)
            if query:
                # settings.MODEL_NAME = model_name
                user_message = Message.objects.create(
                    owner = request.user,
                    body = query)
        
                rag_system = RagManager(files_path)
                answer = rag_system.generate(query)

                assistant_message = Message.objects.create(
                    owner = assistant,
                    body = answer)

                conversation.conversations.add(assistant_message, user_message)

        context = {'conversations': conversation.conversations.all()}
        return render(request, "chatbot.html", context)

    return redirect('add-file')

@login_required(login_url="login")
@require_POST
def delete_conversation(request, pk):
    conversation = get_object_or_404(Conversation, room__user=request.user, pk=pk)
    conversation.delete()
    return redirect('conversations')
