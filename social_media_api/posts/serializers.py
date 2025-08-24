from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser

class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 
                 'followers_count', 'following_count', 'is_following')
        read_only_fields = ('id', 'username', 'email')
    
    def get_followers_count(self, obj):
        return obj.followers_count()
    
    def get_following_count(self, obj):
        return obj.following_count()
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False

class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

class UserSearchSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'is_following')
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False

from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Comment.author.field.related_model.objects.all(), 
        source='author', 
        write_only=True
    )
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.author.field.related_model.objects.all(), 
        source='author', 
        write_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'author_id', 'title', 'content', 'created_at', 
                 'updated_at', 'likes_count', 'comments_count', 'is_liked', 'comments')
        read_only_fields = ('id', 'created_at', 'updated_at', 'likes_count', 'comments_count', 'is_liked')
    
    def get_likes_count(self, obj):
        return obj.likes_count()
    
    def get_comments_count(self, obj):
        return obj.comments_count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content')

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)


