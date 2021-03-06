from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from Insta.models import Post, Like, InstaUser, UserConnection, Comment
from django.urls import reverse, reverse_lazy
#from django.contrib.auth.forms import UserCreationForm
from Insta.forms import CustomUserCreationForm
#basic authorization of django, u have to login first
from django.contrib.auth.mixins import LoginRequiredMixin
from annoying.decorators import ajax_request

# Create your views here.

class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostView(ListView):
    model = Post
    template_name = 'index.html'

    #自行定义get_queryset 去overrived 
    # 只从db里面把当前user的following的人的post显示出来而不是所有的
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return
        current_user = self.request.user
        following = set() #当前user follow的用户
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        #filter return的是一个set
        return Post.objects.filter(author__in=following)
        
        

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'



class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'
    
class EditProfile(LoginRequiredMixin, UpdateView):
    model = InstaUser
    template_name = 'edit_profile.html'
    fields = ['profile_pic', 'username']
    login_url = 'login'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'  #选中所有的Post的fields(author, title, image)，from 0001_initials.py
    login_url = 'login'
    """点击post后如果没有login, 要跳转到login的page"""

 
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")

class SignUp(CreateView):
    #sign up require form_class （model field)
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")



@ajax_request #function view 只响应ajax的函数
def addLike(request): #传入的request，request里面的data的value是post.pk
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk) 
    try:
        like = Like(post=post, user=request.user) #创建一个Like的object，需要提供Like的2个attributes
        like.save() #把这个object存在db里面, 如果db已经存在了一个这个object，user已经点过赞了
        #因为是1 user 只能点一个post ，如果存在了就调到exception, 就是取消
        result = 1 
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }

@ajax_request
def addComment(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    comment_text = request.POST.get('comment_text')
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()
        username = request.user.username
        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }
        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(creator=current_user, following=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }
