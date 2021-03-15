# Generated by Django 3.1.7 on 2021-03-11 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_choice', models.CharField(max_length=100, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
                'db_table': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_status', models.CharField(max_length=100, verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
                'db_table': 'types',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('summary', models.CharField(max_length=100, verbose_name='Summary')),
                ('description', models.TextField(blank=True, max_length=400, null=True, verbose_name='Description')),
                ('task_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='status', to='webapp.status', verbose_name='Status')),
                ('type_key', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='type', to='webapp.type', verbose_name='Type')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'db_table': 'tasks',
            },
        ),
    ]