from django.db import models
from django.conf import settings

from accounts.models import CustomUser
from magazine.models import MagazineIssue


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("review", "In Review"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="articles"
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to="uploads/article_images/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_premium = models.BooleanField(default=False) 
    issue = models.ForeignKey(
        MagazineIssue, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='articles'
    )
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author.email} on {self.article.title}"

class ReadLater(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='read_later')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='read_later_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article') 

    def __str__(self):
        return f"{self.user.username} → {self.article.title}"
    
class ArticleLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_articles')
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"
    
class ReadingHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reading_history')
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='reads')
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} read {self.article.title}"