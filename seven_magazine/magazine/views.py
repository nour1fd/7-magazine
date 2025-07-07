from django.shortcuts import get_object_or_404, render
from rest_framework import status
from articles.serializer import ArticleDetailSerializer, ArticleListSerializer
from core.permissions import IsSelf, IsSupervisor
from magazine.models import MagazineIssue, MagazinePurchase
from magazine.serializers import MagazineIssueSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class MagazineIssueListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        issues = MagazineIssue.objects.order_by("-issue_date")
        serializer = MagazineIssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request):

        if not request.user.is_authenticated or request.user.usertype != "supervisor":
            return Response(
                {"detail": "Only supervisors can perform this action."}, status=403
            )

        serializer = MagazineIssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MagazineIssueDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def get(self, request, pk):
        issue = get_object_or_404(MagazineIssue, pk=pk)
        serializer = MagazineIssueSerializer(issue)
        return Response(serializer.data)

    def put(self, request, pk):
        issue = get_object_or_404(MagazineIssue, pk=pk)
        serializer = MagazineIssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueArticlesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, issue_id):
        issue = get_object_or_404(MagazineIssue, id=issue_id)
        articles = issue.articles.filter(status="published")
        serializer = ArticleListSerializer(
            articles, many=True, context={"request": request}
        )
        return Response(serializer.data)


class IssueArticlesDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, issue_id):
        issue = get_object_or_404(MagazineIssue, id=issue_id)
        articles = issue.articles.filter(status="published")
        serializer = ArticleDetailSerializer(
            articles, many=True, context={"request": request}
        )
        return Response(serializer.data)


class PurchaseMagazineAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, issue_id):
        issue = get_object_or_404(MagazineIssue, id=issue_id)
        completed = MagazinePurchase.objects.filter(
            user=request.user, issue=issue, status="completed"
        ).exists()

        if completed:
            return Response(
                {"detail": "You already own this issue."}, status=status.HTTP_200_OK
            )

        MagazinePurchase.objects.create(
            user=request.user, issue=issue, status="pending"
        )

        return Response(
            {"detail": "Purchase created. Awaiting payment."},
            status=status.HTTP_201_CREATED,
        )


class CancelMagazinePurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSelf]

    def delete(self, request, issue_id):
        issue = get_object_or_404(MagazineIssue, id=issue_id)
        try:
            purchase = MagazinePurchase.objects.get(user=request.user, issue=issue)

            if purchase.status == "completed":
                return Response(
                    {"detail": "You cannot cancel a completed purchase."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            MagazinePurchase.objects.filter(user=request.user, issue=issue).exclude(
                status="completed"
            ).delete()

            # Update status instead of deleting
            purchase.status = "refunded"
            purchase.save()

            return Response(
                {"detail": "Purchase has been cancelled and marked as refunded."},
                status=status.HTTP_200_OK,
            )

        except MagazinePurchase.DoesNotExist:
            return Response(
                {"detail": "You have not purchased this issue."},
                status=status.HTTP_400_BAD_REQUEST,
            )
