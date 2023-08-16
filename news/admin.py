from django.contrib import admin
from .models import CommentModel, NewsModel


class CommentInline(admin.TabularInline):
    model = CommentModel
    extra = 5


class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "news_content", "created_at", "has_comments"]
    inlines = [CommentInline]


admin.site.register(NewsModel, NewsAdmin)
