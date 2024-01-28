from django.contrib import admin


from .models import News,  Categories


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'published']

    search_fields = ['title', 'slug', 'description']
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['edited_at', 'created_at', 'author']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(News, NewsAdmin)
admin.site.register(Categories)
