import json

from django.utils import timezone
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .ai import generate_project_brief, get_project_brief_model_id
from .models import Project, ProjectBriefRun


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "ai_brief",
            "ai_brief_updated_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["ai_brief", "ai_brief_updated_at", "created_at", "updated_at"]


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"], url_path="generate-brief")
    def generate_brief(self, request, pk=None):
        project = self.get_object()
        model_id = get_project_brief_model_id()
        try:
            brief = generate_project_brief(project)
        except Exception as exc:
            ProjectBriefRun.objects.create(
                project=project,
                status=ProjectBriefRun.Status.ERROR,
                model_id=model_id,
                error_message=str(exc),
            )
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        brief_json = brief.model_dump_json(indent=2)
        ProjectBriefRun.objects.create(
            project=project,
            status=ProjectBriefRun.Status.SUCCESS,
            model_id=model_id,
            brief_json=brief_json,
        )
        project.ai_brief = brief_json
        project.ai_brief_updated_at = timezone.now()
        project.save(update_fields=["ai_brief", "ai_brief_updated_at", "updated_at"])
        return Response(self.get_serializer(project).data)
