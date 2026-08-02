from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("workspace", "0002_project_ai_brief_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectBriefRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[("success", "Success"), ("error", "Error")],
                        max_length=20,
                    ),
                ),
                ("model_id", models.CharField(blank=True, max_length=120)),
                ("brief_json", models.TextField(blank=True)),
                ("error_message", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="brief_runs",
                        to="workspace.project",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
