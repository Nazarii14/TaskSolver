# Generated by Django 4.2.4 on 2023-09-13 19:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tasksolver", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="max_number",
        ),
    ]
