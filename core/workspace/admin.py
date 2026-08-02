from django.contrib import admin

from .models import Project, ProjectBriefRun


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "updated_at", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "owner__email", "owner__username")


@admin.register(ProjectBriefRun)
class ProjectBriefRunAdmin(admin.ModelAdmin):
    list_display = ("project", "status", "model_id", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("project__name", "project__owner__email", "model_id")
