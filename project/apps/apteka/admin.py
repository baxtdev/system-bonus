import re
from django.contrib import admin
from .models import Pharmacy, Manager, History, DiscountItems

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('manager', 'pharmacy', 'contact')
    list_display_links = ('manager', 'pharmacy', 'contact')
    list_filter = ('pharmacy', )
    search_fields = ('manager', 'pharmacy', 'contact')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'manager', 'pharmacy', 'date', 'method', 'bonus','customer_bonus',)

    def has_add_permission(self, request):
        return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Pharmacy)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(DiscountItems)