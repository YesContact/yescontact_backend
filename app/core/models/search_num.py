from django.db import models


class SearchRecord(models.Model):
    searcher = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, null=True, blank=True, related_name="searcher_records"
    )
    searched_user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name='searched_user_records', null=True, blank=True)
    search_query = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)