from django.contrib import admin
from .models import Article, Category, Tag

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "is_premium", "issue")
    list_filter = ("status", "is_premium", "issue", "created_at")
    search_fields = ("title", "author__username")

admin.site.register(Category)
admin.site.register(Tag)
