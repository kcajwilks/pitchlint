from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workspace", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="ai_brief",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="project",
            name="ai_brief_updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
