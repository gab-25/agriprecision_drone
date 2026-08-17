from django.db import models


class Report(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey("survey.Survey", on_delete=models.CASCADE, related_name="reports")

    def __str__(self):
        return self.title
