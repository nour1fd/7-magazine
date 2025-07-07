import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='categories__name', lookup_expr='icontains')
    date = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Article
        fields = ['author', 'category', 'date', 'status']