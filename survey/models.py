from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE, related_name="surveys")

    def __str__(self):
        return self.name
