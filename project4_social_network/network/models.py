from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Follow(models.Model):
    follower=models.ForeignKey("User",related_name="following",on_delete=models.CASCADE)
    followed=models.ForeignKey("User",related_name="follower",on_delete=models.CASCADE)

class Post(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    content=models.CharField(max_length=400)
    timestamp=models.DateTimeField(auto_now_add=True)
    num_likes=models.IntegerField()

class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    username=models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes")