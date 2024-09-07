from django.contrib import admin
from .models import Blog, Comment, Tag

# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "title", "publish_on"]
    exclude = ["id"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "body", "created_on"]


class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)