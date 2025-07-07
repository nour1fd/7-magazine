from rest_framework import serializers

from articles.serializer import ArticleDetailSerializer
from .models import MagazineIssue

class MagazineIssueSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()

    class Meta:
        model = MagazineIssue
        fields = ['id', 'title', 'issue_date', 'description', 'cover_image','articles']
    
    def get_articles(self, issue):
        request = self.context.get('request')
        user = request.user if request else None

        articles = issue.articles.filter(status='published')
        serializer = ArticleDetailSerializer(articles, many=True, context={'request': request})
        return serializer.data