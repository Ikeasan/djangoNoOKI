from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')  # ログイン後に遷移するページ
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# ログイン後に遷移するメイン画面のビュー
@login_required
def main_view(request):
    # ユーザーが作成した投稿を取得
    posts = Post.objects.filter(author=request.user)
    
    # 各投稿に対応するコメントを取得
    for post in posts:
      post.comments = Comment.objects.filter(post=post)
    return render(request, 'main.html', {'posts': posts})




@login_required
def add_comment(request, post_id):
  post = Post.objects.get(id=post_id)
    
  if request.method == 'POST':
      form = CommentForm(request.POST)
      if form.is_valid():
          comment = form.save(commit=False)
          comment.author = request.user  # コメントの投稿者を設定
          comment.post = post  # コメントがどの投稿に関連するか設定
          comment.save()
          return redirect('main')  # コメント投稿後、メイン画面にリダイレクト
  else:
      form = CommentForm()
    
  return render(request, 'add_comment.html', {'form': form, 'post': post})







# 投稿を作成するビュー
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # 画像を扱うためにrequest.FILESを使用
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 現在のユーザーを投稿者として設定
            post.save()
            return redirect('main')  # 投稿後、メイン画面にリダイレクト
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})
