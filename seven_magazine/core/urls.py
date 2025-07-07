from django.urls import path
from .views import (
    PromoteUserToAuthorAPIView,
    SupervisorPublishArticleAPIView,
    SupervisorCreateMagazineIssueAPIView
)

urlpatterns = [
    path('supervisor/promote/<int:user_id>/', PromoteUserToAuthorAPIView.as_view()),
    path('supervisor/publish-article/<int:article_id>/', SupervisorPublishArticleAPIView.as_view()),
    path('supervisor/create-issue/', SupervisorCreateMagazineIssueAPIView.as_view()),
]