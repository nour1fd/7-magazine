from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("READER", "Reader"),
        ("AUTHOR", "Author"),
        ("SUPERVISOR", "Supervisor"),  
    )

    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="READER"
    )
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="uploads/profile_images/", blank=True, null=True
    )
    has_access = models.BooleanField(default=False)

    def __str__(self):
        return self.username
