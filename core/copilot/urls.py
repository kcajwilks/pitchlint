from django.urls import path

from . import views

app_name = "copilot"

urlpatterns = [
    path("", views.runtime, name="runtime"),
    path("info", views.info, name="info"),
    path("agent/<str:agent_id>/run", views.agent_run, name="agent_run"),
    path("agent/<str:agent_id>/stop/<str:thread_id>", views.agent_stop, name="agent_stop"),
    path("reset", views.reset, name="reset"),
]
