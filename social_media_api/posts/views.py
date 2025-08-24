from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    # Get users that the current user follows
    following_users = request.user.following.all()
    
    # Get posts from followed users
    feed_posts = Post.objects.filter(author__in=following_users)
    
    # Apply search if provided
    search_query = request.query_params.get('search', None)
    if search_query:
        feed_posts = feed_posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    # Order by creation date (newest first)
    feed_posts = feed_posts.order_by('-created_at')
    
    # Serialize the posts
    serializer = PostSerializer(feed_posts, many=True, context={'request': request})
    return Response(serializer.data)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Add this to your existing PostViewSet
class PostViewSet(viewsets.ModelViewSet):
    # ... existing code ...
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def feed(self, request):
        # Get users that the current user follows
        following_users = request.user.following.all()
        
        # Get posts from followed users
        feed_posts = Post.objects.filter(author__in=following_users)
        
        # Apply search and ordering if provided
        search_query = request.query_params.get('search', None)
        if search_query:
            feed_posts = feed_posts.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )
        
        # Order by creation date (newest first)
        feed_posts = feed_posts.order_by('-created_at')
        
        # Paginate the results
        page = self.paginate_queryset(feed_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(feed_posts, many=True)
        return Response(serializer.data)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .serializers import UserProfileSerializer, FollowSerializer, UserSearchSerializer

CustomUser = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        user_to_follow = get_object_or_404(CustomUser, id=serializer.validated_data['user_id'])
        
        if request.user == user_to_follow:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.follow(user_to_follow):
            return Response({
                'message': f'You are now following {user_to_follow.username}',
                'following': True,
                'followers_count': user_to_follow.followers_count(),
                'following_count': request.user.following_count()
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Already following this user.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        user_to_unfollow = get_object_or_404(CustomUser, id=serializer.validated_data['user_id'])
        
        if request.user.unfollow(user_to_unfollow):
            return Response({
                'message': f'You have unfollowed {user_to_unfollow.username}',
                'following': False,
                'followers_count': user_to_unfollow.followers_count(),
                'following_count': request.user.following_count()
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Not following this user.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    user = request.user
    followers = user.followers.all()
    serializer = UserProfileSerializer(followers, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    user = request.user
    following = user.following.all()
    serializer = UserProfileSerializer(following, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.query_params.get('q', '')
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    users = CustomUser.objects.filter(
        Q(username__icontains=query) | 
        Q(email__icontains=query) |
        Q(bio__icontains=query)
    ).exclude(id=request.user.id)
    
    serializer = UserSearchSerializer(users, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer
from .permissions import IsAuthorOrReadOnly

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'likes_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            message = 'Post unliked'
        else:
            post.likes.add(user)
            message = 'Post liked'
        
        return Response({'status': message, 'likes_count': post.likes_count()})
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)
        
        if page is not None:
            serializer = CommentSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id')
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        post_id = self.request.data.get('post') or self.request.data.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


