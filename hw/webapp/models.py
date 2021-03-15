from django.db import models
# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        abstract = True


class Task(BaseModel):
    summary = models.CharField(max_length=100, null=False, blank=False, verbose_name='Summary')
    description = models.TextField(max_length=400, null=True, blank=True, verbose_name='Description')
    status_key = models.ForeignKey(
        'webapp.Status',
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name='Status',
        null=False,
        blank=False
    )
    type_key = models.ManyToManyField(
        'webapp.Type',
        related_name='tasks',
        verbose_name='Type',
        through='webapp.TaskType',
        through_fields=('task', 'types'),
        blank=True
    )

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f'{self.summary} {self.description}'

class Status(models.Model):
    status_choice = models.CharField(max_length=100, null=False, verbose_name='Status')

    class Meta:
        db_table = 'statuses'
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return f'{self.status_choice}'


class Type(models.Model):
    type_status = models.CharField(max_length=100, null=False, verbose_name='Type')

    class Meta:
        db_table = 'types'
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

    def __str__(self):
        return f'{self.type_status}'

class TaskType(models.Model):
    task = models.ForeignKey(
        'webapp.Task', 
        related_name='task_types',
         on_delete=models.CASCADE,
         verbose_name='Task'
         )
    types = models.ForeignKey(
        'webapp.Type',
        related_name='types_task',
        on_delete=models.PROTECT,
        verbose_name='Type'
    )

    def __str__(self):
        return f'{self.task} {self.types}'