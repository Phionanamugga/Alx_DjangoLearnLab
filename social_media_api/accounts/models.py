from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Many-to-many relationship for followers (users who follow this user)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following_users',
        blank=True
    )
    
    # Many-to-many relationship for following (users that this user follows)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers_users',
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def followers_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()
    
    def is_following(self, user):
        return self.following.filter(id=user.id).exists()
    
    def is_followed_by(self, user):
        return self.followers.filter(id=user.id).exists()
    
    def follow(self, user):
        if not self.is_following(user) and self != user:
            self.following.add(user)
            user.followers.add(self)
            return True
        return False
    
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            user.followers.remove(self)
            return True
        return False

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def likes_count(self):
        return self.likes.count()
    
    def comments_count(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    

