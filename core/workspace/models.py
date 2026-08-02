from django.conf import settings
from django.db import models


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    ai_brief = models.TextField(blank=True)
    ai_brief_updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="unique_project_name_per_owner"),
        ]

    def __str__(self) -> str:
        return self.name


class ProjectBriefRun(models.Model):
    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        ERROR = "error", "Error"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="brief_runs")
    status = models.CharField(max_length=20, choices=Status.choices)
    model_id = models.CharField(max_length=120, blank=True)
    brief_json = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
