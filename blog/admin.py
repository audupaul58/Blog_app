from django.contrib import admin
from .models import Article, Category, Comment
# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    prepopulated_fields = {"slug": ("title",)} 
    inlines = [
        CommentInline
    ]
    
admin.site.register(Article, ArticleAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)} 
    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)

