from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from utils.utils import save_json
from pathlib import Path
from django.conf import settings

@staff_member_required
@require_POST
def rag_control(request):
    config_dir = Path(settings.RAG_CONFIG_DIR)
    config_path = config_dir / settings.RAG_CONFIG_PATH
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path.touch(exist_ok=True)

    retrieve_type = request.POST.get("retriever", "hybrid")
    top_k = int(request.POST.get("top_k", 5))
    chunk_size = int(request.POST.get("chunk_size", 1000))
    overlap_size = int(request.POST.get("overlap_size", 200))
    data = {
        "chunk_conf": {"chunk_size": chunk_size, "overlap_size": overlap_size},
        "retriever_conf":{"type": retrieve_type, 'top_k': top_k}
        }

    if retrieve_type in {"hybrid", "bm25"}:
        try:
            b = float(request.POST.get("b", 0.75))
            k1 = float(request.POST.get("k1", 1.5))
            data["retriever_conf"]["b"] = b
            data["retriever_conf"]["k1"] = k1

        except ValueError:
            return redirect("rag-settings")

    save_json(config_path, data)
    print(data)
    return redirect("conversations")

@staff_member_required
def rag_setting(request):
    return render(request, "rag_settings.html")

@staff_member_required
def log_info_view(request):
    logs_dir = Path(settings.LOGS_DIR)
    logs_path = logs_dir / settings.LOGS_PATH
    logs_dir.mkdir(parents=True, exist_ok=True)
    logs_path.touch(exist_ok=True)

    with logs_path.open('r') as file:
        logs = file.readlines()

    context = {"logs": logs}
    return render(request, 'logs.html', context)
