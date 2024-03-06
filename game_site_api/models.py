import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey


class ProfilePic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img = models.ImageField(upload_to='profile_pics')

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pfp = models.ForeignKey(ProfilePic, on_delete=models.CASCADE, null=True, blank=False)
    username = models.CharField(max_length=30, unique=True, null=False, blank=True)
    hashed_password = models.CharField(max_length=30, null=False, blank=True)
    email = models.EmailField(unique=True, null=False, blank=True)
    gender = models.CharField(max_length=15, null=True, blank=False)
    age = models.DateField(auto_now_add=True, null=False, blank=True)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    views = models.IntegerField(default=0)


class PostPic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_post = models.ForeignKey(Post, on_delete=models.CASCADE,null=False, blank=True)
    url = models.CharField(max_length=150, null=False, blank=True)

class PostComent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = ForeignKey(User, on_delete=models.CASCADE,null=False, blank=True)
    user_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=True)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    counter = models.IntegerField(default=0)

