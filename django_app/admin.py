from django.contrib import admin
from .models import Post

# 管理者側で削除やデータ更新できるようにした！！
class PostAdmin(admin.ModelAdmin):
  
  list_display = ('title', 'author', 'created_at', 'updated_at', 'is_published')
  search_fields = ('title', 'content')  # 投稿内容で検索できるようにする
  
  # 投稿削除時に画像も削除する
  def delete_model(self, request, obj):
      # カスタムdeleteメソッドを呼び出す
      obj.delete()  # 画像を削除するために、Postのdelete()メソッドを呼び出す
      super().delete_model(request, obj)  # 親クラスのdelete_modelを呼び出して、データベースから削除

admin.site.register(Post, PostAdmin)
