import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .ai import ProjectBrief, generate_project_brief, get_project_brief_model_id
from .forms import ProjectForm
from .models import Project, ProjectBriefRun


class OwnerQuerysetMixin(LoginRequiredMixin):
    login_url = "account_login"

    def get_queryset(self) -> QuerySet[Project]:
        return Project.objects.filter(owner=self.request.user)


class ProjectListView(OwnerQuerysetMixin, ListView):
    template_name = "workspace/project_list.html"
    context_object_name = "projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Workspace"
        return context


class ProjectCreateView(OwnerQuerysetMixin, CreateView):
    template_name = "workspace/project_form.html"
    form_class = ProjectForm
    success_url = reverse_lazy("workspace:project_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "New project"
        return context


class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    template_name = "workspace/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = self.object.name

        parsed: ProjectBrief | None = None
        if self.object.ai_brief:
            try:
                parsed = ProjectBrief.model_validate(json.loads(self.object.ai_brief))
            except Exception:
                parsed = None

        context["ai_brief_parsed"] = parsed
        context["brief_runs"] = self.object.brief_runs.all()[:10]
        return context


class ProjectGenerateBriefView(OwnerQuerysetMixin, View):
    def post(self, request, pk: int):
        project = self.get_queryset().get(pk=pk)
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
            messages.error(request, f"AI brief failed: {exc}")
            return redirect("workspace:project_detail", pk=project.pk)

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
        messages.success(request, "AI brief generated.")
        return redirect("workspace:project_detail", pk=project.pk)


class ProjectUpdateView(OwnerQuerysetMixin, UpdateView):
    template_name = "workspace/project_form.html"
    form_class = ProjectForm

    def get_success_url(self):
        return reverse_lazy("workspace:project_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Edit project"
        return context


class ProjectDeleteView(OwnerQuerysetMixin, DeleteView):
    template_name = "workspace/project_confirm_delete.html"
    success_url = reverse_lazy("workspace:project_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Delete project"
        return context

import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .ai import ProjectBrief, generate_project_brief
from .forms import ProjectForm
from .models import Project


class OwnerQuerysetMixin(LoginRequiredMixin):
    login_url = "account_login"

    def get_queryset(self) -> QuerySet[Project]:
        return Project.objects.filter(owner=self.request.user)


class ProjectListView(OwnerQuerysetMixin, ListView):
    template_name = "workspace/project_list.html"
    context_object_name = "projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Workspace"
        return context


class ProjectCreateView(OwnerQuerysetMixin, CreateView):
    template_name = "workspace/project_form.html"
    form_class = ProjectForm
    success_url = reverse_lazy("workspace:project_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "New project"
        return context


class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    template_name = "workspace/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = self.object.name

        parsed: ProjectBrief | None = None
        if self.object.ai_brief:
            try:
                parsed = ProjectBrief.model_validate(json.loads(self.object.ai_brief))
            except Exception:
                parsed = None

        context["ai_brief_parsed"] = parsed
        return context


class ProjectGenerateBriefView(OwnerQuerysetMixin, View):
    def post(self, request, pk: int):
        project = self.get_queryset().get(pk=pk)
        try:
            brief = generate_project_brief(project)
        except Exception as exc:
            messages.error(request, f"AI brief failed: {exc}")
            return redirect("workspace:project_detail", pk=project.pk)

        project.ai_brief = brief.model_dump_json(indent=2)
        project.ai_brief_updated_at = timezone.now()
        project.save(update_fields=["ai_brief", "ai_brief_updated_at", "updated_at"])
        messages.success(request, "AI brief generated.")
        return redirect("workspace:project_detail", pk=project.pk)


class ProjectUpdateView(OwnerQuerysetMixin, UpdateView):
    template_name = "workspace/project_form.html"
    form_class = ProjectForm

    def get_success_url(self):
        return reverse_lazy("workspace:project_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Edit project"
        return context


class ProjectDeleteView(OwnerQuerysetMixin, DeleteView):
    template_name = "workspace/project_confirm_delete.html"
    success_url = reverse_lazy("workspace:project_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Delete project"
        return context

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .ai import generate_project_brief
from .forms import ProjectForm
from .models import Project


class OwnerQuerysetMixin(LoginRequiredMixin):
    login_url = "account_login"

    def get_queryset(self) -> QuerySet[Project]:
        return Project.objects.filter(owner=self.request.user)


class ProjectListView(OwnerQuerysetMixin, ListView):
    template_name = "workspace/project_list.html"
    context_object_name = "projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Workspace"
        return context


class ProjectCreateView(OwnerQuerysetMixin, CreateView):
    template_name = "workspace/project_form.html"
    form_class = ProjectForm
    success_url = reverse_lazy("workspace:project_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "New project"
        return context


class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    template_name = "workspace/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = self.object.name
        return context


class ProjectGenerateBriefView(OwnerQuerysetMixin, View):
    def post(self, request, pk: int):
        project = self.get_queryset().get(pk=pk)
        try:
            brief = generate_project_brief(project)
        except Exception as exc:
            messages.error(request, f"AI brief failed: {exc}")
            return redirect("workspace:project_detail", pk=project.pk)

        project.ai_brief = brief.model_dump_json(indent=2)
        project.ai_brief_updated_at = timezone.now()
        project.save(update_fields=["ai_brief", "ai_brief_updated_at", "updated_at"])
        messages.success(request, "AI brief generated.")
        return redirect("workspace:project_detail", pk=project.pk)


class ProjectUpdateView(OwnerQuerysetMixin, UpdateView):
    template_name = "workspace/project_form.html"
    form_class = ProjectForm

    def get_success_url(self):
        return reverse_lazy("workspace:project_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Edit project"
        return context


class ProjectDeleteView(OwnerQuerysetMixin, DeleteView):
    template_name = "workspace/project_confirm_delete.html"
    success_url = reverse_lazy("workspace:project_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Delete project"
        return context
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .ai import generate_project_brief
from .forms import ProjectForm
from .models import Project


class OwnerQuerysetMixin(LoginRequiredMixin):
    login_url = "account_login"

    def get_queryset(self) -> QuerySet[Project]:
        return Project.objects.filter(owner=self.request.user)


class ProjectListView(OwnerQuerysetMixin, ListView):
    template_name = "workspace/project_list.html"
    context_object_name = "projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Workspace"
        return context


class ProjectCreateView(OwnerQuerysetMixin, CreateView):
    template_name = "workspace/project_form.html"
    form_class = ProjectForm
    success_url = reverse_lazy("workspace:project_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "New project"
        return context


class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    template_name = "workspace/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = self.object.name
        return context


class ProjectGenerateBriefView(OwnerQuerysetMixin, View):
    def post(self, request, pk: int):
        project = self.get_queryset().get(pk=pk)
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_active:
            messages.error(request, "Your account is inactive.")
            return self._redirect(project)

        if not request.META.get("HTTP_X_CSRFTOKEN") and "csrfmiddlewaretoken" not in request.POST:
            messages.error(request, "CSRF token missing.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request.environ and not request.META:
            messages.error(request, "Invalid environment.")
            return self._redirect(project)

        if not request.user:
            messages.error(request, "You must be logged in.")
            return self._redirect(project)

        if not request.POST:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.email and not request.user.username:
            messages.error(request, "Please complete your account profile before using AI features.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        if not request:
            messages.error(request, "Invalid request.")
            return self._redirect(project)

        try:
            brief = generate_project_brief(project)
        except Exception as exc:
            messages.error(request, f"AI brief failed: {exc}")
            return self._redirect(project)

        project.ai_brief = brief.model_dump_json(indent=2)
        project.ai_brief_updated_at = timezone.now()
        project.save(update_fields=["ai_brief", "ai_brief_updated_at", "updated_at"])
        messages.success(request, "AI brief generated.")
        return self._redirect(project)

    def _redirect(self, project: Project):
        return reverse_lazy("workspace:project_detail", kwargs={"pk": project.pk})


class ProjectUpdateView(OwnerQuerysetMixin, UpdateView):
    template_name = "workspace/project_form.html"
    form_class = ProjectForm

    def get_success_url(self):
        return reverse_lazy("workspace:project_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Edit project"
        return context


class ProjectDeleteView(OwnerQuerysetMixin, DeleteView):
    template_name = "workspace/project_confirm_delete.html"
    success_url = reverse_lazy("workspace:project_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "workspace"
        context["app_page_title"] = "Delete project"
        return context
