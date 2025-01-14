from django.contrib import admin
from .models import Category, News, Comment

admin.site.register(Category)

class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'category', 'add_time', 'is_featured')  
    list_filter = ('is_featured',)  
    search_fields = ('title', 'description')  

    actions = ['make_featured', 'remove_featured']

    def make_featured(self, request, queryset):
        """Mark selected news articles as featured, ensuring only one is featured"""

        News.objects.update(is_featured=False)

        queryset.update(is_featured=True)

    def remove_featured(self, request, queryset):
        """Remove 'featured' status from selected news articles"""
        queryset.update(is_featured=False)

    make_featured.short_description = "Mark selected news as Featured"
    remove_featured.short_description = "Remove Featured status from selected news"

admin.site.register(News, AdminNews)

class AdminComment(admin.ModelAdmin):
    list_display = ('news', 'email', 'comment', 'status')

admin.site.register(Comment, AdminComment)