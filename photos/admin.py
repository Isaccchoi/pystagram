from django.contrib import admin
from .models import Post
from .models import Comment

# Register your models here.

class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1
    #추가할 갯수, 화면에 보이는 숫자가 보임

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'created_at', )
    list_display_links = ('id', 'created_at', )
    ordering = ('-id', '-created_at', )
    inlines = (CommentInlineAdmin, )
    search_fields = ('id', 'content', )
    list_filter = ('category', 'tags', )
    date_hierarchy = 'created_at'
    # pytz를 설치하지 않으면 오류 발생 

admin.site.register(Post, PostAdmin)
