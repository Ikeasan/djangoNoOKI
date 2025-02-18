from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'is_published')
    search_fields = ('title', 'content')

    def delete_model(self, request, obj):
        # 投稿の画像を削除
        if obj.image:
            obj.image.delete()  # 画像を削除
        
        # 親クラスのdelete_modelを呼び出して、データベースから削除
        super().delete_model(request, obj)

admin.site.register(Post, PostAdmin)
