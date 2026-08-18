from django.db import models
from django.db.models import F, Func


class Workspace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="workspaces")

    def __str__(self):
        return self.name
