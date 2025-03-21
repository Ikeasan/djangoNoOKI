"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.login_view,name='start'),#初期ページ
    path('admin/', admin.site.urls),#開発者
    path('accounts/login/', views.login_view, name='login'),  # ログイン
    path('accounts/signup/',views.signup, name='signup'),
    path('main/', views.main_view, name='main'),  # メイン画面のURL
    path('create/', views.create_post, name='create_post'),  # 投稿作成画面のURL
    path('add_comment/<uuid:post_id>/', views.add_comment, name='add_comment'),  # コメント追加画面のURL
    path('post/<uuid:post_id>/', views.post_detail, name='post_detail'),  # 投稿詳細ページ
    path('post/<uuid:post_id>/delete/', views.post_delete, name='post_delete'),  #
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
