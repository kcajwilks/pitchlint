from django.urls import path

from . import views

app_name = "copilot"

urlpatterns = [
    path("info", views.info, name="info"),
    path("agent/<str:agent_id>/run", views.agent_run, name="agent_run"),
    path("agent/<str:agent_id>/stop/<str:thread_id>", views.agent_stop, name="agent_stop"),
    path("reset", views.reset, name="reset"),
    path("demo/inline/", views.CopilotDemoInlineView.as_view(), name="demo_inline"),
    path("demo/sidebar/", views.CopilotDemoSidebarView.as_view(), name="demo_sidebar"),
    path("demo/popup/", views.CopilotDemoPopupView.as_view(), name="demo_popup"),
]

