from django.contrib import admin
from .models import MagazineIssue, MagazinePurchase

@admin.register(MagazineIssue)
class MagazineIssueAdmin(admin.ModelAdmin):
    list_display = ("title", "issue_date")
    search_fields = ("title",)

@admin.register(MagazinePurchase)
class MagazinePurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "issue", "status", "purchased_at")
    list_filter = ("status", "issue")
