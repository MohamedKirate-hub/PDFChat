from django.contrib import admin
from user_auth.models import User
from chatbot.models import Conversation, ConversationRoom

class RAGAdminSite(admin.AdminSite):
    site_header = ""
    site_title = ""
    index_title = ""

admin_site = RAGAdminSite(name="rag_admin_site")