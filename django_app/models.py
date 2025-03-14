from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
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
  audio = models.FileField(upload_to='audio/',null=True,blank=True,verbose_name="BGM",
                           validators=[FileExtensionValidator(allowed_extensions=['mp3'])])  # メディアフォルダ内のaudio/に保存
    
  def __str__(self):
    return self.title


  # def delete(self, *args, **kwargs):
  #       # 画像が存在する場合は削除
  #       if self.image:
  #           # ファイルの削除
  #           if os.path.isfile(self.image.path):
  #               os.remove(self.image.path)
  #       super().delete(*args, **kwargs)  # 投稿をデータベースから削除
  
  def delete(self, *args, **kwargs):
    # 画像ファイルの削除
    if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)


    # 音楽ファイルの削除
    if self.audio:
        try:
            print(f"削除する音楽のパス: {self.audio.path}")  # パス確認
            self.audio.close()  # ← これを追加！
            if os.path.isfile(self.audio.path):
                os.remove(self.audio.path)
        except Exception as e:
            print(f"音楽削除エラー: {e}")

    super().delete(*args, **kwargs)
  
  
class Comment(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")  # UUIDを主キーに設定
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="関連する投稿")  # 関連する投稿
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="コメントの投稿者")  # コメントの投稿者
  content = models.TextField(max_length=200, verbose_name="コメントの内容")  # コメントの内容
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="コメントの投稿日時")  # コメント投稿日時

  def __str__(self):
    return f'Comment by {self.author.username} on {self.post.title}'