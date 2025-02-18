from django import forms  # formsモジュールは通常ここでインポート
from django.forms.widgets import Textarea  # Textareaをここでインポート
from .models import Post, Comment, User
from django.contrib.auth.forms import UserCreationForm 

class CustomUserCreationForm(UserCreationForm): #ユーザー追加
    class Meta:
        model = User  # デフォルトの User ではなく、カスタム User を指定
        fields = ['username', 'password1', 'password2']  # 必要なフィールドを追加


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_published', 'image']  # ユーザーが入力する項目
        widgets = {
            'content': Textarea(attrs={'rows': 5, 'cols': 40}),  # Textareaを直接使用
            'is_published': forms.CheckboxInput({'class': 'checkbox-inline'}),  # 公開/非公開のフラグをチェックボックスで表示
        }
        labels = {
            'title': 'タイトル',
            'content': '本文',
            'is_published': '公開/非公開フラグ',
            'image': '画像追加',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # コメントに必要なフィールドを指定
        widgets = {
            'content': Textarea(attrs={'rows': 3, 'cols': 40}),  # Textareaを直接使用
        }
        labels = {
            'content': 'コメントの内容',
        }
