from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os

class User(AbstractUser):
  REQUIRED_FIELDS = []
  # username = models.CharField(verbose_name='ユーザー名',max_length=50)
  # password = models.CharField(verbose_name='password',max_length=50)

class Post(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")  # UUIDを主キーに設定
  title = models.CharField(max_length=100, verbose_name="タイトル")  # 投稿のタイトル
  content = models.TextField(max_length=200, verbose_name="本文")  # 投稿の内容(本文)
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="投稿日時")  # 投稿日時
  updated_at = models.DateTimeField(auto_now=True, verbose_name="最終更新日時")  # 最終更新日時
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="投稿者")  # 投稿者 (ユーザー)
  is_published = models.BooleanField(default=True, verbose_name="公開/非公開フラグ")  # 公開/非公開フラグ
  image = models.ImageField(upload_to='posts/', null=True, blank=True, verbose_name="画像追加")  # 画像を追加
    
  def __str__(self):
    return self.title


  def delete(self, *args, **kwargs):
        if self.image:
            image_path = self.image.path
            print(f"Attempting to delete image at: {image_path}")  # 画像ファイルのパスを出力
            try:
              if os.path.isfile(image_path):
                  print(f"Image deleted: {image_path}") 
                  os.remove(image_path)  # 画像ファイルを削除
                  print(f"Image deleted: {image_path}")  # 削除後の確認
              else:
                  print(f"Image file not found: {image_path}")  # ファイルが見つからない場合
            except Exception as e:
              print(f"Error deleting file {image_path}: {e}")  # エラーの表示
        super().delete(*args, **kwargs)  # 親クラスのdeleteメソッドを呼び出してデータベースから削除
  
  
class Comment(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")  # UUIDを主キーに設定
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="関連する投稿")  # 関連する投稿
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="コメントの投稿者")  # コメントの投稿者
  content = models.TextField(max_length=200, verbose_name="コメントの内容")  # コメントの内容
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="コメントの投稿日時")  # コメント投稿日時

  def __str__(self):
    return f'Comment by {self.author.username} on {self.post.title}'