from django.contrib import admin
from loading.models import LoadFile, LoadingBase

admin.site.register(LoadingBase)
admin.site.register(LoadFile)
