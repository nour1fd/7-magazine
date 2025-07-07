from django.shortcuts import get_object_or_404
from accounts.models import CustomUser
from articles.models import Article
from core.permissions import IsSupervisor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from magazine.models import MagazineIssue
from magazine.serializers import MagazineIssueSerializer
# Create your views here.
class PromoteUserToAuthorAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user.user_type = "AUTHOR"
        user.save()
        return Response({"detail": f"{user.username} has been promoted to AUTHOR."}, status=200)

class SupervisorPublishArticleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)

        is_premium = request.data.get("is_premium", False)
        status = request.data.get("status", "draft")
        issue_id = request.data.get("issue")  

        if is_premium and (status == "published") and not issue_id:
            return Response({"error": "Premium articles must be assigned to a magazine issue."}, status=400)

        article.is_premium = is_premium
        article.status = status

        if is_premium and issue_id:
            issue = get_object_or_404(MagazineIssue, id=issue_id)
            article.issue = issue

        article.save()

        return Response({"detail": "Article updated and published."}, status=200)
    

class SupervisorCreateMagazineIssueAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def post(self, request):
        serializer = MagazineIssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)