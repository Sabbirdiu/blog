from django.contrib import admin
from .models import Author,Category, Post,About
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    # list_display = ('title')
    prepopulated_fields = {'slug': ('title',)}
class CatAdmin(admin.ModelAdmin):
    # list_display = ('title')
    prepopulated_fields = {'slug': ('title',)}    
admin.site.register(Author)

admin.site.register(Category,CatAdmin)

admin.site.register(Post,ArticleAdmin)
admin.site.register(About)