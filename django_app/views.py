from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import PostForm, CommentForm,CustomUserCreationForm
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


#ユーザー追加
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main")
    else:
        form = CustomUserCreationForm()
        
    return render(request, "signup.html",{"form": form})

# ログイン後に遷移するメイン画面のビュー
@login_required
def main_view(request):
    # ユーザーが作成した投稿を取得
    # posts = Post.objects.filter(author=request.user)
    posts = Post.objects.all()

    # そのままpostsをテンプレートに渡す
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
          post.comments.add(comment)  # コメントを投稿に追加
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


# 投稿詳細ページ
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # 投稿を取得
    comment_form = CommentForm(request.POST or None)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user  # 現在のユーザーをコメントの投稿者に設定
        comment.post = post  # どの投稿にコメントするか設定
        comment.save()
        return redirect('post_detail', post_id=post.id)  # コメント追加後、投稿詳細ページにリダイレクト

    return render(request, 'details.html', {'post': post, 'comment_form': comment_form})
