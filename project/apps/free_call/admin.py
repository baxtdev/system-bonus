from django.contrib import admin
from .models import FreeCall


class FreeCallAdmin(admin.ModelAdmin):
    list_display = ('theme', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('theme', 'name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'theme', 'message')
    

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    

admin.site.register(FreeCall, FreeCallAdmin)
