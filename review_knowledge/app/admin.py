from django.contrib import admin
from .models import Client, Post
# Register your models here.
# admin.site.register(Client)
# admin.site.register(Post)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender', 'active', 'createdAt', 'lastAccess')
    list_filter = ('gender', 'active')
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'createdAt')
    list_filter = ('author','createdAt')
    search_fields = ('title', 'content', 'author__name') 
    # author__name cú pháp 2 dấu gạch dưới để truy vấn xuyên bảng 