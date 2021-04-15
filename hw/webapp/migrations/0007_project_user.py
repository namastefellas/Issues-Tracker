# Generated by Django 3.1.7 on 2021-04-15 07:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0006_task_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ManyToManyField(default=1, related_name='projects', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
