from rest_framework import serializers

from magazine.models import MagazinePurchase
from .models import Article, ArticleLike, Category, ReadLater, Tag, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ArticleListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    liked_by_me = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "author_name",
            "category",
            "tags",
            "status",
            "created_at",
            "is_premium",
            "like_count",
            "liked_by_me"
        ]
  
  
    def get_liked_by_me(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return ArticleLike.objects.filter(user=user, article=obj).exists()
        return False


class ArticleDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "author_name",
            "category",
            "tags",
            "content",
            "image",
            "status",
            "created_at",
            "updated_at",
            "is_premium",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request') 
        user = request.user if request  else None

        if instance.is_premium:
            if not user or not user.is_authenticated:
                data['content'] = None
            else:
                has_access = MagazinePurchase.objects.filter(
                    user=user,
                    issue=instance.issue,
                    status='completed'
                ).exists()
                if not has_access:
                    data['content'] = None
        return data

class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "title",
            "slug",
            "category",
            "tags",
            "content",
            "image",
        ]

    # def validate(self, data):
    #     is_premium = data.get("is_premium", False)
    #     issue = data.get("issue", None)
    #     status = data.get("status", "draft")  

        # if is_premium and status == "published" and not issue:
            # raise serializers.ValidationError("Published premium articles must be assigned to a magazine issue.")

        # return data


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField( read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "article",
            "author_name",
            "content",
            "created_at",
            "is_approved",
        ]
        read_only_fields = ["author_name", "created_at", "is_approved"]


class ReadLaterSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source='article.title', read_only=True)
    article_slug = serializers.SlugField(source='article.slug', read_only=True)

    class Meta:
        model = ReadLater
        fields = ['id', 'article', 'article_title', 'article_slug', 'saved_at']
        read_only_fields = ['saved_at']
        
class ArticleLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleLike
        fields = ['id', 'article', 'liked_at']