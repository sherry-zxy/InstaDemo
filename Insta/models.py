from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
# Create your models here.
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
    upload_to = 'static/images/profiles',
    format = 'JPEG',
    options = {'quality':100},
    blank = True,
    null =True
    )
    #获得user's following
    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections
    
     #获得user's followers
    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers
    
    #我自己有没有被follower所follow
    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

#记录了关系的model
# A(createor) follows B(following)
# connection 1 -> A follows B
# connection 2 -> A follows c
# connection 3 -> D follows A
# A(creator) A.friendship_creator_set -> (connection1, connection2)
# A.friend_set ->(connection3)
class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username

class Post(models.Model):
    author = models.ForeignKey(
        InstaUser,
        blank=True,
        null=True,
        on_delete = models.CASCADE,
        related_name='my_posts'
        
    )
    """没有title也能发，没有title这个field也能用"""
    title = models.TextField(blank=True, null=True) 
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality':100},
        blank = True,
        null =True
        )
    #用当前post的object.likes.count获得所有这个post的赞
    #post1.likes ->(like1, like2)
    def get_like_count(self):
        return self.likes.count()
    
#get_absolute_url作用, 当有人create新的post，就调用这个 reverse: 调用post_detail名字 reverse成一个url 在url.py中去找这个名字'
#post_detail -> www.xxx->page(template)'
#class的object 去调用这个 比如post1, post2'
    def get_absolute_url(self):
        return reverse("post_detail", args= [str(self.id)])

#哪个用户喜欢哪个post，like是关系型model,连接了instaUser和post的关系
class Like(models.Model):
    post = models.ForeignKey(
        Post,#指向Post这个model
        on_delete = models.CASCADE,
        #attri: 如果post被删除，like也被删除
        related_name ='likes')
        #related_name 是like的一个object: 
           # like1 ->user1 like post1,
           # like2 ->user2 like post1 当你处于post1这个object的时候通过 post1.likes -> (like1, like2)
           #当你处于一个post的object中可以通过 .likes 去获得这个object的所有的like的关系
    user = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'likes'
        #user.like -> 所有user点过的赞
    )

     #一个user只能给一个post点一个赞，1(post)：M (user) relationship
    class Meta:
        unique_together = ("post", "user")
    
    #如果用一个string表达like这个object就是Like: 这个like object的user 喜欢 这个like的post的名字
    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' +self.post.title

    
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name ='comment'
    )
    user = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name= 'comment'
    )
    comment = models.CharField(max_length=100)
    post_one = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.comment

    
    



