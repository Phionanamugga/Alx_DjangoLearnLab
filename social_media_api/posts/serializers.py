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


