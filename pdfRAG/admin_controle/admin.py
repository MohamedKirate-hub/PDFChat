from django.contrib import admin
from user_auth.models import User
from loading.models import LoadFile
from django.db.models import Count

class RAGAdminSite(admin.AdminSite):
    site_header = "DocuRAG Administration"
    site_title = "DocuRAG Admin Portal"
    index_title = "RAG Control Center"

admin_site = RAGAdminSite(name="rag_admin_site")

class UserRoleFilter(admin.SimpleListFilter):
    title = "User Role"
    parameter_name = "user_role"
    
    def lookups(self, request, model_admin):
        return (
            ('user', 'Customer'),
            ('admin', 'Admin'),
            ('assistant', 'Assistant'),
        )
    
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'user':
            return queryset.filter(role__name = 'user')
        if val == 'admin':
            return queryset.filter(role__name = 'admin')
        if val == 'assistant':
            return queryset.filter(role__name = 'assistant')
        return queryset

@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email',
                    'loaded_files', 'conversations')
    list_filter = (UserRoleFilter,)
    
    @admin.display(description="Loaded Files")
    def loaded_files(self, obj):
        return obj.uploaded_files
    
    @admin.display(description="Conversations")
    def conversations(self, obj):
        return obj.conversations
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            uploaded_files = Count("loaded__files", distinct=True),
            conversations = Count("rooms__conversations", distinct=True),
            )

@admin.register(LoadFile, site=admin_site)
class LoadedFilesAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ('file_path', 'file_owner', 'created_at')
    
    @admin.display(description="Files Owner")
    def file_owner(self, obj):
        return ", ".join(
            obj.loading_bases.values_list("user__username", flat=True)
        )
