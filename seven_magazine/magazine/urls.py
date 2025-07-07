from django.urls import path

from magazine.views import (
    CancelMagazinePurchaseAPIView,
    IssueArticlesAPIView,
    IssueArticlesDetailAPIView,
    MagazineIssueDetailAPIView,
    MagazineIssueListAPIView,
    PurchaseMagazineAPIView,
)


urlpatterns = [
    path("issues/", MagazineIssueListAPIView.as_view(), name="issue-list"),
    path("issues/<int:pk>/", MagazineIssueDetailAPIView.as_view(), name="issue-detail"),
    path("issues/<int:issue_id>/articles/",IssueArticlesAPIView.as_view,name="issue-articles",),
    path("issues/<int:issue_id>/articles/detail/",IssueArticlesDetailAPIView.as_view(),name="issue-articles",),
    path(
        "issues/<int:issue_id>/purchase/",
        PurchaseMagazineAPIView.as_view(),
        name="issue-purchase",
    ),
    path(
        "issues/<int:issue_id>/cancel/",
        CancelMagazinePurchaseAPIView.as_view(),
        name="issue-cancel",
    ),
]
