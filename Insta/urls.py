"""InstaPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
'当访问这个app的url的时候希望用class-based view 来处理，then render templates'
from Insta.views import (HelloWorld, PostView, PostDetailView, PostCreateView, 
                         PostUpdateView, PostDeleteView, addLike,
                                UserDetailView,addComment,toggleFollow, EditProfile)
'从insta 中views.py import 一个view，view的名字'
'当传递empty string url进来，调用helloWorld的as_view func 这个func是去render template html'


urlpatterns = [ 
    path('helloworld/', HelloWorld.as_view(), name='helloworld'),    
    path('', PostView.as_view(), name= 'posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name ='post_detail'),
    path('post/new/', PostCreateView.as_view(), name = 'make_post'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name ='post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name ='post_delete'),
    path('like', addLike, name ='addLike'),
    path('user/<int:pk>/', UserDetailView.as_view(), name ='user_detail'),
    path('edit_profile/<int:pk>/', EditProfile.as_view(), name='edit_profile'),
    path('comment', addComment, name ='addComment'),
    path('togglefollow', toggleFollow, name='togglefollow'),

]