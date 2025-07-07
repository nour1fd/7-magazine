from django.utils import timezone 
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from articles.filter import ArticleFilter
from core.permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly, IsAuthor, IsOwnerOrReadOnly
from .models import Article, ArticleLike, Category, ReadLater, ReadingHistory, Tag, Comment
from .serializer import ArticleCreateUpdateSerializer, ArticleDetailSerializer, ArticleListSerializer, CategorySerializer, CommentSerializer, ReadLaterSerializer, TagSerializer
from rest_framework.permissions import IsAuthenticated

class CategoryListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({"detail": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class TagListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        return Response({"detail": "Tag deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class ArticleListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        base_queryset = Article.objects.filter(status='published').select_related('author', 'issue').prefetch_related('categories','tags', 'likes')
        queryset = ArticleFilter(request.GET, queryset=base_queryset).qs
        
        search_query = request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        serializer = ArticleListSerializer(queryset, many=True,context={"request":request})
        return Response(serializer.data)

class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug, status='published')
        if request.user.is_authenticated:
            ReadingHistory.objects.update_or_create(
                user=request.user, article=article,
                defaults={"viewed_at": timezone.now()}
            )

        serializer = ArticleDetailSerializer(article, context={'request': request})
        return Response(serializer.data)
       
class ArticleCreateAPIView(APIView):
    permission_classes = [IsAuthenticated,IsAuthor]
    def post(self, request):
        serializer = ArticleCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly,IsAuthor]

    def put(self, request, slug):
        article = get_object_or_404(Article, slug=slug, author=request.user)
        serializer = ArticleCreateUpdateSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentListAPIView(APIView):
    def get(self, request, article_id):
        comments = Comment.objects.filter(article_id=article_id, is_approved=True).select_related('author')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        serializer = CommentSerializer(comment, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        comment.delete()
        return Response({"detail": "Comment deleted."}, status=status.HTTP_204_NO_CONTENT)

class ReadLaterListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = ReadLater.objects.filter(user=request.user).select_related('article').prefetch_related('article__tags', 'article__category')
        serializer = ReadLaterSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        article_id = request.data.get('article')
        article = get_object_or_404(Article, id=article_id)
        obj, created = ReadLater.objects.get_or_create(user=request.user, article=article)
        if not created:
            return Response({'detail': 'Already in Read Later'}, status=200)
        return Response({'detail': 'Article added to Read Later'}, status=201)
class ReadLaterDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, article_id):
        try:
            item = ReadLater.objects.get(user=request.user, article_id=article_id)
            item.delete()
            return Response({'detail': 'Removed from Read Later'}, status=204)
        except ReadLater.DoesNotExist:
            return Response({'detail': 'Article not in Read Later'}, status=404)
        
class ArticleLikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        like, created = ArticleLike.objects.get_or_create(user=request.user, article=article)

        if not created:
            like.delete()
            return Response({'detail': 'Unliked'}, status=200)

        return Response({'detail': 'Liked'}, status=201)
    

class ReadingHistoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = ReadingHistory.objects.filter(user=request.user).select_related('article__author', 'article__category', 'article__issue').prefetch_related('article__tags', 'article__likes').order_by('-viewed_at')
        valid_articles = [item.article for item in history if item.article is not None]
        serializer = ArticleListSerializer(valid_articles, many=True, context={'request': request})
        return Response(serializer.data)