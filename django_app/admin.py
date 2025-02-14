from django.contrib import admin
from .models import Post

# 管理者側で削除やデータ更新できるようにした！！
class PostAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'created_at', 'updated_at', 'is_published')
  search_fields = ('title', 'content')  # 投稿内容で検索できるようにする

admin.site.register(Post, PostAdmin)
