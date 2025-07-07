from django.urls import path
from .views import (
    ArticleLikeToggleAPIView,
    ArticleUpdateAPIView,
    ArticleCreateAPIView,
    ArticleDetailAPIView,
    ArticleListAPIView,
    CategoryDetailAPIView,
    CategoryListAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
    ReadLaterDeleteAPIView,
    ReadLaterListCreateAPIView,
    ReadingHistoryListAPIView,
    TagDetailAPIView,
    TagListAPIView,
)

urlpatterns = [

    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    path("tags/", TagListAPIView.as_view(), name="tag-list"),
    path('tags/<int:pk>/', TagDetailAPIView.as_view(), name='tag-detail'),

    path("comments/create/", CommentListAPIView.as_view(), name="comment-create"),
    path("/comments/<comment_id>/delete/", CommentDetailAPIView.as_view(), name="comment-create"),

    path("articles/create/", ArticleCreateAPIView.as_view(), name="article-create"),
    path("articles/<slug:slug>/update/", ArticleUpdateAPIView.as_view(), name="article-update"),
    path(
        "article/<int:article_id>/comments/",
        CommentListAPIView.as_view(),
        name="comment-list",
    ),
    path('articles/history/', ReadingHistoryListAPIView.as_view(), name='article-history'),

    path("articles", ArticleListAPIView.as_view(), name="article-list"),
    path("articles/<slug:slug>/", ArticleDetailAPIView.as_view(), name="article-detail"),
    
    path('read-later/', ReadLaterListCreateAPIView.as_view(), name='read-later-list-create'),
    path('read-later/<int:article_id>/delete/', ReadLaterDeleteAPIView.as_view(), name='read-later-delete'),
    path('articles/<int:article_id>/like-toggle/', ArticleLikeToggleAPIView.as_view(), name='like-article'),


]

