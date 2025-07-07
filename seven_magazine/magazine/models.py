from django.conf import settings
from django.db import models

# Create your models here.
class MagazineIssue(models.Model):
    title = models.CharField(max_length=255,unique=True)
    issue_date = models.DateField(unique=True) 
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='uploads/magazine_covers/', blank=True, null=True)

    def __str__(self):
        return f"Issue {self.issue_date.strftime('%B %Y')}"
    

class MagazinePurchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey('MagazineIssue', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # ✅ NEW
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'issue')

    def __str__(self):
        return f"{self.user.email} - {self.issue.title} [{self.status}]"
    
  